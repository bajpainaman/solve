#!/usr/bin/env bash
#
# pr-review.sh
# Review code with Claude Code (headless), three modes:
#   --repo owner/name --pr N   review that one PR (whoever it's assigned to)
#   --local [--base BRANCH]    review the current branch of the repo you're in,
#                              before any push; never touches your working copy
#   no arguments               review every open PR awaiting review from ME or
#                              MY TEAMS, scoped to specific repos or whole orgs
# For each review it saves:
#   - the review as markdown  -> ~/pr-reviews/<date>/<repo>_PR<n>.md
#   - the Claude session id, so you can resume and ask clarifying questions.
#
# Efficiency:
#   - one reusable clone per repo (not per PR)  -> bounded disk
#   - each repo is fetched at most once per run
#   - PRs whose head commit is unchanged since the last review are skipped
#
# Nothing is ever posted to GitHub.
# Requirements: gh (authenticated), git, jq, claude (Claude Code CLI).

set -uo pipefail

# --- PATH (launchd/cron start with a bare PATH) -----------------------------
# Fallbacks go after the caller's PATH so an explicit PATH always wins.
export PATH="${PATH:+${PATH}:}${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Keep gh's stdout strictly JSON: no update banner, prompts, or color codes.
export GH_NO_UPDATE_NOTIFIER=1
export GH_PROMPT_DISABLED=1
export GH_PAGER=cat
export NO_COLOR=1
export CLICOLOR=0
unset GH_FORCE_TTY CLICOLOR_FORCE     # these force color even when piped

# --- Config -----------------------------------------------------------------
# Override any of these in ~/.config/pr-review/config.sh (or $PR_REVIEW_CONFIG)
# instead of editing this file.
BASE_DIR="${PR_REVIEW_DIR:-${HOME}/pr-reviews}"

# Which repos to review in batch mode, and under what assignment:
#   MINE_REPOS - scopes where PRs requesting MY OWN review are included
#   TEAM_REPOS - scopes where PRs requesting one of MY TEAMS' review are ALSO included
# An entry is either "owner/name" for a single repo, or a bare "owner" to cover
# EVERY repo in that org (still pinned to @me / my teams). MINE_REPOS=() means
# every repo GitHub can see. TEAM_REPOS=() disables team pickup.
MINE_REPOS=()
TEAM_REPOS=()

# Read-only toolset. Swap for (--dangerously-skip-permissions) to let the agent
# run arbitrary read commands. Safe either way: nothing is written/pushed/posted.
CLAUDE_PERM=(--allowedTools 'Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),Bash(git status:*),Bash(git branch:*)')
MODEL="opus"                          # set to "sonnet" to cut cost at volume
SEARCH_LIMIT=100
EXTRA_PROMPT_FILE=""                  # extra review rules appended to every prompt
PANEL_FILE=""                         # replaces the default reviewer panel

CONFIG_FILE="${PR_REVIEW_CONFIG:-${HOME}/.config/pr-review/config.sh}"
# shellcheck source=/dev/null
[ -f "$CONFIG_FILE" ] && . "$CONFIG_FILE"

DATE="$(date +%Y-%m-%d)"
OUT_DIR="${BASE_DIR}/${DATE}"         # markdown reviews (tiny)
REPO_CACHE="${BASE_DIR}/repos"        # one reusable clone per repo
STATE_DIR="${BASE_DIR}/state"         # per-PR head-SHA markers (skip unchanged)
LOG_FILE="${BASE_DIR}/pr-review.log"
INDEX="${OUT_DIR}/index.md"

# --- Arguments ----------------------------------------------------------------
FORCE_REPO=""
FORCE_PR=""
LOCAL=""
LOCAL_BASE=""
CLI_PANEL=""
CLI_LENSES=()
usage() { echo "Usage: $0 [--repo owner/name --pr N | --local [--base BRANCH]] [--panel FILE] [--lens FILE]..." >&2; exit 1; }
need_file() { [ -f "${1:-}" ] || { echo "no such file: ${1:-}" >&2; exit 1; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --repo)  FORCE_REPO="${2:-}"; shift 2 || usage ;;
    --pr)    FORCE_PR="${2:-}";   shift 2 || usage ;;
    --local) LOCAL=1;             shift ;;
    --base)  LOCAL_BASE="${2:-}"; shift 2 || usage ;;
    --panel) need_file "${2:-}"; CLI_PANEL="$2"; shift 2 ;;
    --lens)  need_file "${2:-}"; CLI_LENSES+=("$2"); shift 2 ;;
    *) usage ;;
  esac
done
if { [ -n "$FORCE_REPO" ] && [ -z "$FORCE_PR" ]; } || { [ -z "$FORCE_REPO" ] && [ -n "$FORCE_PR" ]; }; then
  echo "--repo and --pr must be given together" >&2; exit 1
fi
if [ -n "$LOCAL" ] && [ -n "$FORCE_REPO" ]; then
  echo "--local cannot be combined with --repo/--pr" >&2; exit 1
fi
LOCAL_CWD="$PWD"

mkdir -p "$OUT_DIR" "$REPO_CACHE" "$STATE_DIR"
exec 4>&1                             # keep the terminal for --local's result line
exec >>"$LOG_FILE" 2>&1
echo "===== $(date) : PR review run starting ====="

# --- Review one checked-out change ------------------------------------------
# The default panel. Swap it with --panel, a repo .pr-review/panel.md, or PANEL_FILE.
read -r -d '' DEFAULT_PANEL <<'PANEL_EOF' || true
Review as a panel of three senior engineers. Focus on technical debt, bugs,
scalability, and architectural flaws affecting the broader system; ignore pure
formatting nits. Finally, an agent acting as the tech lead who owns the code this
change touches reviews the panel's output. It confirms that each issue is real and
judges it against the codebase as a whole, so that established patterns are
followed and similar components keep behaving consistently.
PANEL_EOF

# Replace every PAT in S with REP literally. Bash's ${s//pat/rep} treats & in REP
# as the match on bash 5.2, and keeps quotes literally on 3.2, so it's unsafe here.
subst() {                             # args: s pat rep
  local s="$1" out=""
  while [[ "$s" == *"$2"* ]]; do out+="${s%%"$2"*}$3"; s="${s#*"$2"}"; done
  printf '%s' "$out$s"
}

# args: repo repo_dir head_branch base_branch head_sha out_file title url
review() {
  local repo="$1" repo_dir="$2" head_branch="$3" base_branch="$4" head_sha="$5"
  local out_file="$6" title="$7" url="$8"
  local prompt extra="" panel f resp result session_id cost tokens

  # Repo files come from the BASE branch, so a PR can't rewrite its own review.
  base_file() { git -C "$repo_dir" show "origin/${base_branch}:$1" 2>/dev/null; }
  add_rules() {                       # args: label text
    [ -n "$2" ] || return 0
    extra+=$'\n'"ADDITIONAL REVIEW RULES (from $1). Apply them when deciding what"
    extra+=$'\n'"counts as an issue, but keep the severity scale above."$'\n'"$2"$'\n'
  }

  # Panel: --panel, then the repo's .pr-review/panel.md, then PANEL_FILE, then the default.
  if [ -n "$CLI_PANEL" ]; then panel="$(cat "$CLI_PANEL")"
  else panel="$(base_file .pr-review/panel.md)"; fi
  [ -z "$panel" ] && [ -n "$PANEL_FILE" ] && [ -f "$PANEL_FILE" ] && panel="$(cat "$PANEL_FILE")"
  [ -z "$panel" ] && panel="$DEFAULT_PANEL"

  # Lenses add up: repo REVIEW.md, repo .pr-review/lenses/*.md, EXTRA_PROMPT_FILE, --lens.
  add_rules REVIEW.md "$(base_file REVIEW.md)"
  while IFS= read -r f; do
    case "$f" in *.md) add_rules "$f" "$(base_file "$f")" ;; esac
  done < <(git -C "$repo_dir" ls-tree --name-only "origin/${base_branch}" .pr-review/lenses/ 2>/dev/null)
  for f in "$EXTRA_PROMPT_FILE" ${CLI_LENSES[@]+"${CLI_LENSES[@]}"}; do
    [ -n "$f" ] && [ -f "$f" ] && add_rules "${f##*/}" "$(cat "$f")"
  done

  # Structured, corroborable review prompt. The template is a QUOTED heredoc so
  # the shell interprets nothing (no backtick/${} surprises); run-specific values
  # are substituted into the placeholder tokens immediately afterward.
  read -r -d '' prompt <<'PROMPT_EOF' || true
You are reviewing branch `@@HEAD_BRANCH@@` at commit @@HEAD_SHA@@ in @@REPO@@,
against base `@@BASE_BRANCH@@`. Run `git diff origin/@@BASE_BRANCH@@...HEAD` for
the change set and open the full files at branch head for context.

@@PANEL@@

Verify every finding against source before asserting; mark confidence.

CATEGORIES (assign each issue exactly one):
  SEC    — Security & Correctness
  PERF   — Performance & Maintainability
  DESIGN — Business logic & design/conventions (must respect CLAUDE.md and
           other documented rules)

SEVERITY (by worst-case impact × likelihood):
  Critical — exploitable vulnerability, data loss/corruption, or will break prod.
  High     — correctness bug reachable with realistic inputs, significant perf
             regression, or violates a documented contract/rule.
  Medium   — latent bug on edge cases, real maintainability risk, notable debt.
  Low      — minor improvement or convention nit.

REFERENCES (mandatory per issue, so it can be corroborated on GitHub):
  - full repo-relative file path
  - enclosing function/class/symbol
  - line number(s) AS THEY APPEAR AT COMMIT @@HEAD_SHA@@ (not diff-hunk numbers);
    read them from the file via Read/Grep — do NOT estimate
  - the exact offending lines, quoted verbatim
  - a permalink: https://github.com/@@REPO@@/blob/@@HEAD_SHA@@/<path>#L<line>
  Before finalizing, re-open each referenced file at HEAD and confirm the quoted
  lines match the stated numbers; if you cannot confirm, suffix the line with
  "~approx" and keep the symbol + quoted code as the anchor.

STABILITY:
  - ID: <CAT>-<n>, numbered within category (SEC-1, SEC-2, PERF-1, …).
  - Fingerprint: <CAT>|<repo-relative-path>|<symbol>|<kebab-summary>, derived
    only from location and root cause so the same issue yields the same
    fingerprint across runs.

CONFIDENCE:
 - SCORE: 0 is complete guess, 100 is absolute certainty
 - METHOD: This is the process you used to verify the issue (2 sentences max).
  e.g: "Ran script to validate foo() generates the date string in ISO8601 format"

PROSE STYLE (mandatory for every prose field — issue titles, Problem, Fix,
Verification method):
  - Write every sentence as a finite clause: a grammatical subject plus a
    finite verb that asserts the claim. Issue titles too — "The query has no
    LIMIT, unlike the sibling it mirrors", never "No LIMIT, unlike the sibling".
  - Never open with a verbless fragment or headline label (a noun phrase plus
    a colon or dash). Convert the label into the sentence's subject or verb.
  - Attach rationale with an explicit connective (because, so, so that, which
    is why), never by welding two clauses with a colon or dash. A colon may
    only introduce an enumeration, and only after a complete clause.
  - Keep one claim per sentence. Never chain three clauses with because/and/so
    in one sentence. Contractions are welcome.
  - Avoid nominalizations: keep actors as subjects and actions as verbs
    ("the CSP blocks the popup", not "a CSP-blocked modal fails silently").
  - Never stack three or more content words as premodifiers, and never coin a
    new compound or nickname for this document ("the history twin", "dedup
    premise"); name the actual file, symbol, or commit instead. Established
    two-word technical terms (foreign key, partial index) are fine.
  - Describe a missing safeguard as something nothing does ("nothing stops
    closed stints from overlapping"), never as "no" plus a capability noun
    ("no overlap prevention").
  - Give evidence its own sentence; never wedge it into the middle of a claim
    with parentheses or paired dashes. Parentheses may hold only a short
    identifier (a filename, line number, or id), never a clause with a verb.
  - Start verification prose with a subject ("We grepped the migrations…",
    "A grep of the migrations finds no lock_timeout"), never with a bare
    participle or log-style verb ("Grepped the migrations…").
  - Use an "X, not Y" contrast only when ruling out Y is itself part of the
    argument, and then give it its own sentence. Drop attitude-only punch
    ("with zero trace") in favor of the plain claim ("and leaves no trace").
  - When a finding applies in more than one file or place, list each site as
    its own line item, never as a parenthetical ("(same omission at …)").
  - Fix lines may open imperatively ("Add a field_validator…"), matching
    docstring convention; any explanatory sentence after the imperative
    follows the rules above.
@@EXTRA_RULES@@
OUTPUT: Emit ONLY the Markdown below — no preamble, no closing remarks. Sort
issues by severity (Critical→Low), then path (A→Z), then line ascending. Always
print all four severity counts even if zero. If a category has no issues, write
"None." under it. Keep Problem ≤ 2 sentences and Fix ≤ 2 sentences, concrete.

# Code Review — @@REPO@@ `@@HEAD_BRANCH@@` @ @@HEAD_SHA@@

## Summary
- Base: `@@BASE_BRANCH@@`
- Totals: Critical <n>, High <n>, Medium <n>, Low <n> (Total <n>)
- Verdict: <blocking | needs-work | minor | ship-ready>

## Issues
| ID | Sev | Cat | Location | Issue |
|----|-----|-----|----------|-------|
| SEC-1 | Critical | SEC | `path/file.py:123` `func()` | short title |

## Details
### SEC-1 — <short title>
- Severity: Critical
- Confidence Score: 85
- Verification method: <= 2 sentences, concrete & specific.
- Category: SEC — Security & Correctness
- Location: `path/file.py:123` in `func()`
- Permalink: https://github.com/@@REPO@@/blob/@@HEAD_SHA@@/path/file.py#L123
- Code: `exact offending lines`
- Fingerprint: `SEC|path/file.py|func|short-summary`
- Problem: <= 2 sentences.
- Fix: <= 2 sentences, concrete.
PROMPT_EOF
  prompt="$(subst "$prompt" @@PANEL@@ "$panel")"
  prompt="$(subst "$prompt" @@EXTRA_RULES@@ "$extra")"
  prompt="$(subst "$prompt" @@HEAD_BRANCH@@ "$head_branch")"
  prompt="$(subst "$prompt" @@BASE_BRANCH@@ "$base_branch")"
  prompt="$(subst "$prompt" @@HEAD_SHA@@ "$head_sha")"
  prompt="$(subst "$prompt" @@REPO@@ "$repo")"

  # Headless run with JSON output so we can capture the resumable session id.
  # </dev/null: never let claude read from the loop's input.
  resp="$( cd "$repo_dir" && claude -p "$prompt" \
             --model "$MODEL" "${CLAUDE_PERM[@]}" \
             --output-format json </dev/null )" || return 1

  result="$(printf '%s' "$resp"     | jq -r '.result // empty')"
  session_id="$(printf '%s' "$resp" | jq -r '.session_id // empty')"
  cost="$(printf '%s' "$resp"       | jq -r '.total_cost_usd // empty')"
  tokens="$(printf '%s' "$resp"     | jq -r '[.modelUsage // {} | .[]] |
    "in \([.[].inputTokens] | add // 0) · out \([.[].outputTokens] | add // 0) · cache-read \([.[].cacheReadInputTokens] | add // 0) · cache-write \([.[].cacheCreationInputTokens] | add // 0)"')"

  {
    echo "# Review: ${repo} ${title}"
    echo
    echo "- Source: ${url}"
    echo "- Branch: \`${head_branch}\` vs \`${base_branch}\`"
    echo "- Head: \`${head_sha}\`"
    echo "- Reviewed: $(date)"
    [ -n "$cost" ] && echo "- Session cost: \$${cost}"
    [ -n "$tokens" ] && echo "- Tokens: ${tokens}"
    echo
    echo "## Ask Claude follow-up questions about this review"
    if [ -n "$LOCAL" ]; then
      echo "This review ran in your working copy, so resume it from there."
      echo '```bash'
      echo "cd \"${repo_dir}\""
    else
      echo "The clone below is shared and may have moved to another PR since this"
      echo "review — the checkout line restores this PR's exact code first."
      echo '```bash'
      echo "cd \"${repo_dir}\""
      echo "git fetch --quiet origin && gh pr checkout ${title#PR #} --force"
    fi
    echo "claude --resume ${session_id}"
    echo '```'
    echo
    echo "---"
    echo
    echo "$result"
  } > "$out_file"

  echo "   wrote ${out_file} (session ${session_id}, ${tokens:-no token data}, \$${cost})"
  [ -f "$INDEX" ] || printf '# PR reviews — %s\n\n' "$DATE" > "$INDEX"
  echo "- [${repo} ${title}](${out_file##*/}) · resume: \`${session_id}\`" >> "$INDEX"
}

# --- Local mode: review the current branch in place ----------------------------
# It never checks out, resets or stashes, so uncommitted work is safe. It reviews
# committed HEAD only.
if [ -n "$LOCAL" ]; then
  die() { echo "!! $1"; echo "pr-review --local failed: $1 (log: ${LOG_FILE})" >&4; exit 1; }
  repo_dir="$(git -C "$LOCAL_CWD" rev-parse --show-toplevel 2>/dev/null)" || die "not inside a git repo"
  read -r repo default_base <<< "$(cd "$repo_dir" && gh repo view \
      --json nameWithOwner,defaultBranchRef -q '.nameWithOwner + " " + .defaultBranchRef.name')"
  [ -n "${repo:-}" ] || die "gh repo view could not identify the GitHub repo"
  base_branch="${LOCAL_BASE:-$default_base}"
  head_branch="$(git -C "$repo_dir" branch --show-current)"
  head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
  git -C "$repo_dir" fetch --quiet origin "$base_branch" || die "could not fetch origin/${base_branch}"
  [ -z "$(git -C "$repo_dir" status --porcelain)" ] || echo "   note: uncommitted changes are not reviewed"
  echo "--- local ${repo} ${head_branch} @ ${head_sha:0:8} vs ${base_branch}"
  out_file="${OUT_DIR}/${repo//\//_}_${head_branch//\//_}_local.md"
  review "$repo" "$repo_dir" "$head_branch" "$base_branch" "$head_sha" "$out_file" \
         "branch ${head_branch} (local)" "local working copy, head not necessarily pushed" \
    || die "claude review failed"
  echo "$out_file" >&4
  exit 0
fi

# Single-run lock (mkdir is atomic; macOS lacks flock). Stops overlapping runs —
# scheduled or manual — from fighting over the shared clones. The holder's
# pid is recorded so a lock orphaned by a SIGKILL'd run is reclaimed instead of
# blocking every future run until someone rm's it by hand.
LOCK_DIR="${BASE_DIR}/.lock"
take_lock() { mkdir "$LOCK_DIR" 2>/dev/null && echo $$ > "${LOCK_DIR}/pid"; }
if ! take_lock; then
  holder="$(cat "${LOCK_DIR}/pid" 2>/dev/null)"
  if [ -n "$holder" ] && kill -0 "$holder" 2>/dev/null; then
    echo "Another run holds the lock (pid ${holder}); exiting."
    exit 0
  fi
  echo "Stale lock (holder pid ${holder:-unknown} is dead); reclaiming."
  rm -rf "$LOCK_DIR"
  take_lock || { echo "Lost the lock race; exiting."; exit 0; }
fi
trap 'rm -rf "$LOCK_DIR" 2>/dev/null' EXIT

# --- Helper: one gh search, sanitized + JSON-validated ----------------------
run_search() {                        # args: extra gh search flags
  local out err rc
  err="$(mktemp)"
  out="$(gh search prs --state=open --limit "$SEARCH_LIMIT" \
           --json number,repository,url,title "$@" 2>"$err")"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "   !! gh search ($*) failed: $(tr '\n' ' ' <"$err")" >&2
    rm -f "$err"; echo '[]'; return
  fi
  rm -f "$err"
  out="$(printf '%s' "$out" | sed $'s/\033\\[[0-9;]*[A-Za-z]//g')"   # strip ANSI
  if printf '%s' "$out" | jq -e . >/dev/null 2>&1; then
    printf '%s' "$out"
  else
    echo "   !! gh search ($*) returned non-JSON; ignoring" >&2
    echo '[]'
  fi
}

# "owner/name" scopes one repo (--repo); a bare "owner" scopes the whole org (--owner).
# The ${arr[@]+...} form keeps empty arrays safe under `set -u` on bash 3.2.
scope_flags() { local r; for r in "$@"; do case "$r" in */*) echo "--repo"; echo "$r" ;; *) echo "--owner"; echo "$r" ;; esac; done; }

# --- Gather PRs: either one forced PR, or mine (MINE_REPOS) + my teams'
# (TEAM_REPOS), deduped by URL --------------------------------------------
if [ -n "$FORCE_REPO" ]; then
  echo "   forced review: ${FORCE_REPO} PR #${FORCE_PR}"
  pr_json="$(gh pr view "$FORCE_PR" --repo "$FORCE_REPO" \
               --json number,title,url 2>/dev/null)" || {
    echo "!! failed to fetch ${FORCE_REPO} PR #${FORCE_PR}"; exit 1; }
  PRS_JSON="[$(printf '%s' "$pr_json" | jq --arg repo "$FORCE_REPO" '. + {repository: {nameWithOwner: $repo}}')]"
else
  mine_flags=()
  while IFS= read -r f; do [ -n "$f" ] && mine_flags+=("$f"); done \
    < <(scope_flags ${MINE_REPOS[@]+"${MINE_REPOS[@]}"})
  echo "   my review requests in: ${MINE_REPOS[*]:-every repo}"
  mine="$(run_search --review-requested=@me ${mine_flags[@]+"${mine_flags[@]}"})"

  team_json='[]'
  if [ "${#TEAM_REPOS[@]}" -gt 0 ]; then
    team_flags=()
    while IFS= read -r f; do [ -n "$f" ] && team_flags+=("$f"); done \
      < <(scope_flags "${TEAM_REPOS[@]}")
    # Auto-discover every team you belong to (needs the token to have read:org).
    teams="$(gh api user/teams --jq '.[] | .organization.login + "/" + .slug' 2>/dev/null || true)"
    if [ -n "${teams:-}" ]; then
      while IFS= read -r t; do
        [ -z "$t" ] && continue
        echo "   team ${t} review requests in: ${TEAM_REPOS[*]}"
        tj="$(run_search --review-requested="$t" "${team_flags[@]}")"
        team_json="$(jq -s 'add' <(printf '%s' "$team_json") <(printf '%s' "$tj"))"
      done <<< "$teams"
    else
      echo "   (no teams discovered — token may lack 'read:org'; reviewing only my own requests)"
    fi
  fi

  PRS_JSON="$(jq -s 'add | unique_by(.url)' \
                <(printf '%s' "$mine") <(printf '%s' "$team_json"))"
fi
COUNT="$(printf '%s' "$PRS_JSON" | jq 'length')"
echo "Found ${COUNT:-0} PR(s) awaiting review (scoped, deduped)."
[ "${COUNT:-0}" -eq 0 ] && { echo "Nothing to do."; exit 0; }

# Fresh index for today's run
printf '# PR reviews — %s\n\n' "$DATE" > "$INDEX"

# --- Review each PR ---------------------------------------------------------
reviewed=0; skipped=0; failed=0
fetched=""    # repos already fetched this run (space-delimited slugs)

# FD 3 feeds the loop so claude -p (which reads stdin) can't drain the list and
# stop it after the first PR.
while read -r pr <&3; do
  number="$(printf '%s' "$pr" | jq -r '.number')"
  repo="$(printf '%s' "$pr"   | jq -r '.repository.nameWithOwner')"
  url="$(printf '%s' "$pr"    | jq -r '.url')"
  title="$(printf '%s' "$pr"  | jq -r '.title')"
  repo_slug="${repo//\//_}"
  repo_dir="${REPO_CACHE}/${repo_slug}"
  echo "--- PR #${number} (${repo}): ${title}"

  meta="$(gh pr view "$number" --repo "$repo" \
            --json headRefName,baseRefName,headRefOid 2>/dev/null)" || {
    echo "   !! metadata read failed; skipping"; failed=$((failed+1)); continue; }

  head_branch="$(printf '%s' "$meta" | jq -r '.headRefName')"
  base_branch="$(printf '%s' "$meta" | jq -r '.baseRefName')"
  head_sha="$(printf '%s' "$meta"    | jq -r '.headRefOid')"

  # Skip if this exact head commit was already reviewed.
  marker="${STATE_DIR}/${repo_slug}_PR${number}.sha"
  if [ -z "$FORCE_REPO" ] && [ -f "$marker" ] && [ "$(cat "$marker")" = "$head_sha" ]; then
    echo "   unchanged since last review (${head_sha:0:8}); skipping"
    skipped=$((skipped+1)); continue
  fi

  # Reusable clone; fetch each repo at most once per run.
  case " $fetched " in
    *" $repo_slug "*) : ;;
    *)
      if [ -d "${repo_dir}/.git" ]; then
        echo "   updating cached clone"
        git -C "$repo_dir" fetch --prune --quiet origin || {
          echo "   !! fetch failed; skipping"; failed=$((failed+1)); continue; }
      else
        echo "   first-time clone of ${repo}"
        gh repo clone "$repo" "$repo_dir" -- --quiet || {
          echo "   !! clone failed; skipping"; failed=$((failed+1)); continue; }
      fi
      fetched="$fetched $repo_slug"
      ;;
  esac

  # Check out this PR's head in the cached clone (never your working copy);
  # ensure the base ref is present for an accurate diff.
  ( cd "$repo_dir" \
      && git reset --hard --quiet \
      && gh pr checkout "$number" --force \
      && git fetch --quiet origin "$base_branch" ) || {
    echo "   !! checkout failed; skipping"; failed=$((failed+1)); continue; }

  out_file="${OUT_DIR}/${repo_slug}_PR${number}.md"
  review "$repo" "$repo_dir" "$head_branch" "$base_branch" "$head_sha" "$out_file" \
         "PR #${number}" "${url} — ${title}" || {
    echo "   !! claude review failed; skipping"; failed=$((failed+1)); continue; }

  # Record the reviewed head SHA so we skip it next run unless new commits land.
  printf '%s' "$head_sha" > "$marker"
  reviewed=$((reviewed+1))
done 3< <(printf '%s' "$PRS_JSON" | jq -c '.[]')

echo "Summary: ${reviewed} reviewed, ${skipped} unchanged/skipped, ${failed} failed."
echo "===== $(date) : PR review run done ====="
