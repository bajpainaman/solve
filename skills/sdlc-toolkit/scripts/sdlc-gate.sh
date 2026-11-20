#!/usr/bin/env bash
# sdlc-gate.sh — the sdlc loop's checks that don't depend on Claude following prose.
#
# As a Claude Code PreToolUse hook for the Bash tool, it backs three rules:
#   1. Nothing commits on the default branch. The hook denies the command.
#   2. A human approves and merges a PR. The hook makes Claude Code ask the user.
#   3. A stage is approved only when sdlc.yaml accounts for each tool the stage requires.
#      The hook denies the commit that approves it.
# sdlc:setup copies this file to .claude/hooks/ in a repo that opts in. Hook mode requires jq.
#
# It has two other modes:
#   sdlc-gate.sh status         prints one line per feature in flight. The plugin runs it at session start.
#   sdlc-gate.sh tools <stage>  prints the tools that stage requires.
#
# Test with: bash tests/test_gate.sh

set -uo pipefail

STAGES="intent spec rfc plan build test ship adr maintain"
SEP=$'\037'                           # joins the lines of one stage entry, so a value never runs into the next line

# The tools a stage accounts for before it's approved. references/stage-rules.md has the same table, and
# tests/test_structure.sh fails when the two differ.
required_tools() {
  case "$1" in
    intent|spec|adr) echo "goldfish" ;;
    plan)  echo "testing goldfish" ;;
    rfc)   echo "rfc-skill formal-verification goldfish" ;;
    build) echo "ponytail testing pr-review" ;;
    test)  echo "testing test-audit verifier pr-review demo" ;;
    ship)  echo "pr-review" ;;
  esac
}

# A feature that modelled its design at RFC also owes Test a second model, written from the code.
conditional_tools() {                 # args: stage feature-dir
  [ "$1" = test ] && [ -e "$2/fv/design/README.md" ] && echo "fv-verifier"
}

# Reads an sdlc.yaml on stdin and prints "<stage>\t<that stage's entry on one line>" for each stage.
# It goes by indentation, so a one-line `{...}` entry and a nested block entry both work.
stage_entries() {
  awk '
    function flush() { if (cur != "") printf "%s\t%s\n", cur, buf; cur = "" }
    /^[^ \t#]/ { flush(); in_stages = ($0 ~ /^stages:/); ind = -1; next }
    !in_stages { next }
    {
      match($0, /^[ \t]*/); n = RLENGTH
      key = substr($0, n + 1)
      if (key ~ /^(intent|spec|rfc|plan|build|test|ship|adr|maintain):/ && (ind < 0 || n == ind)) {
        flush(); ind = n; cur = key; sub(/:.*/, "", cur); buf = key
      } else if (cur != "") buf = buf "\037" key
    }
    END { flush() }
  '
}
entry_of()    { awk -F '\t' -v s="$1" '$1 == s { print $2 }'; }               # args: stage; entries on stdin
is_approved() { grep -Eq 'status:[[:space:]]*"?approved' <<<"$1"; }
is_done()     { grep -Eq 'status:[[:space:]]*"?(approved|skipped)' <<<"$1"; }
field()       { sed -nE "s/.*(^|[^[:alnum:]_-])$2:[[:space:]]*[\"']?([^,}\"'${SEP}]*[^,}\"'${SEP}[:space:]]).*/\2/p" <<<"$1"; }   # args: entry key

# A tool is accounted for when the entry maps it to a file that exists in the feature folder,
# or to the word "skipped" followed by a reason.
tool_ok() {                           # args: entry tool feature-dir
  local val
  grep -Eq "(^|[^[:alnum:]_-])$2:[[:space:]]*[\"']?skipped[^,}\"'${SEP}]*[[:alnum:]]" <<<"$1" && return 0
  val="$(field "$1" "$2")"
  [ -n "$val" ] && [ "$val" != skipped ] && [ -e "$3/$val" ]
}

# --- status mode --------------------------------------------------------------
print_status() {
  local root="${CLAUDE_PROJECT_DIR:-$PWD}" f dir entries stage entry line lines="" plan total owner approver
  for f in "$root"/docs/sdlc/*/sdlc.yaml; do
    [ -f "$f" ] || continue
    dir="$(dirname "$f")"
    entries="$(stage_entries < "$f")"
    for stage in $STAGES; do
      entry="$(entry_of "$stage" <<<"$entries")"
      is_done "$entry" && continue
      line="- $(basename "$dir"): at $stage"
      [ -n "$entry" ] && line="$line ($(field "$entry" status))"
      plan="$dir/plan.md"
      if [ "$stage" = build ] && [ -f "$plan" ]; then
        total="$(grep -cE '\|[[:space:]]*(pending|in_progress|done)[[:space:]]*\|[[:space:]]*$' "$plan")"
        [ "$total" -gt 0 ] && line="$line, $(grep -cE '\|[[:space:]]*done[[:space:]]*\|[[:space:]]*$' "$plan") of $total phases done"
      fi
      if [ -n "$entry" ]; then
        line="$line."
        owner="$(field "$entry" owner)"; approver="$(field "$entry" approver)"
        [ -n "$owner" ] && line="$line Owner $owner."
        [ -n "$approver" ] && line="$line Approver $approver."
      else
        line="$line, not started."
      fi
      lines="$lines$line"$'\n'
      break
    done
  done
  [ -n "$lines" ] || return 0
  printf 'This repo runs the sdlc loop. These features are in flight under docs/sdlc/. Use the sdlc skill to report on them or to continue one.\n%s' "$lines"
}

case "${1:-}" in
  status) print_status; exit 0 ;;
  tools)  required_tools "${2:-}"; exit 0 ;;
esac

# --- hook mode ----------------------------------------------------------------
# Without jq the hook can't read its input. It allows the command, because a
# hook that blocks every Bash call would stop all work in the repo.
command -v jq >/dev/null || exit 0

input="$(cat)"
cmd="$(jq -r '.tool_input.command // empty' <<<"$input")"
cwd="$(jq -r '.cwd // empty' <<<"$input")"
[ -n "$cmd" ] || exit 0

decide() {                            # args: allow|ask|deny reason
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$d,permissionDecisionReason:$r}}'
  exit 0
}

start='(^|[;&|({[:space:]])'          # where a command word may begin

# --- Rule 2: approving or merging a PR is the human's call --------------------
# ponytail: this matches the gh CLI only. Add `gh api .../merge` or another
# forge's CLI here if the team merges that way.
if [[ "$cmd" =~ ${start}gh[[:space:]]+pr[[:space:]]+merge([[:space:]]|$) ]] ||
   [[ "$cmd" =~ ${start}gh[[:space:]]+pr[[:space:]]+review[^\;\&\|]*[[:space:]](--approve|-a)([[:space:]]|$) ]]; then
  decide ask "The sdlc loop leaves approving and merging a PR to a human. Confirm only if you asked Claude to do this."
fi

# Rules 1 and 3 apply to commits. Global git options such as `-C dir`, `-c key=value`
# and `--no-pager` may sit between `git` and the subcommand.
commit_re="${start}git([[:space:]]+(-[Cc][[:space:]]+[^[:space:]]+|-[^[:space:]]+))*[[:space:]]+commit([[:space:]]|\$)"
[[ "$cmd" =~ $commit_re ]] || exit 0

# Find the repo the commit runs in.
# ponytail: this reads `git -C dir` and the first `cd dir`. A command that changes
# directory some other way (pushd, a subshell, a variable) is checked against the
# session's cwd instead. Parse the command properly if that ever lets one through.
dir="$cwd"
if [[ "$cmd" =~ git[[:space:]]+-C[[:space:]]+([^[:space:]]+) ]]; then
  dir="${BASH_REMATCH[1]}"
elif [[ "$cmd" =~ ${start}cd[[:space:]]+([^[:space:]\;\&\|]+) ]]; then
  dir="${BASH_REMATCH[2]}"
fi
dir="${dir%\"}"; dir="${dir#\"}"; dir="${dir%\'}"; dir="${dir#\'}"
dir="${dir/#\~/$HOME}"
dir="$(cd "${cwd:-.}" 2>/dev/null && cd "$dir" 2>/dev/null && pwd)" || exit 0

current="$(git -C "$dir" branch --show-current 2>/dev/null)" || exit 0
[ -n "$current" ] || exit 0           # not a repo, or a detached HEAD
git -C "$dir" rev-parse --verify --quiet HEAD >/dev/null || exit 0   # a new repo's first commit

# --- Rule 1: no commits on the default branch ---------------------------------
default="$(git -C "$dir" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)"
default="${default#origin/}"
# With no origin/HEAD to read, the conventional names are the only clue.
[ -n "$default" ] || case "$current" in main|master) default="$current" ;; esac
if [ "$current" = "$default" ]; then
  decide deny "The sdlc loop never commits on the default branch (${current}). Switch to the feature branch recorded in docs/sdlc/<slug>/sdlc.yaml, or create one with \`git switch -c <branch>\`, then commit again."
fi

# --- Rule 3: an approved stage accounts for its tools --------------------------
# The check covers each stage that the working tree approves and HEAD doesn't, so a stage
# approved before this rule existed never blocks a commit.
# ponytail: the hook sees the working tree before the command runs. A command that edits
# sdlc.yaml and commits in one line isn't checked. A git pre-commit hook would see the index,
# if that ever lets one through.
root="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null)" || exit 0
missing=""
for f in "$root"/docs/sdlc/*/sdlc.yaml; do
  [ -f "$f" ] || continue
  rel="${f#"$root"/}"
  work="$(stage_entries < "$f")"
  head="$(git -C "$root" show "HEAD:$rel" 2>/dev/null | stage_entries)"
  for stage in $STAGES; do
    entry="$(entry_of "$stage" <<<"$work")"
    is_approved "$entry" || continue
    is_approved "$(entry_of "$stage" <<<"$head")" && continue
    for tool in $(required_tools "$stage") $(conditional_tools "$stage" "$(dirname "$f")"); do
      tool_ok "$entry" "$tool" "$(dirname "$f")" || missing="$missing $stage needs $tool in $rel."
    done
  done
done
[ -z "$missing" ] || decide deny "The sdlc loop approves a stage only when each tool it requires is on record.${missing} Under the stage's \`tools:\`, map each one to the file it produced, or to \"skipped: <reason>\" when the approver skipped it or it isn't installed. Then commit again."
exit 0
