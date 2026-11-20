---
name: pr-review
description: >
  Headless Claude code review using the bundled pr-review.sh script. Three modes:
  review ONE specific PR (--repo owner/name --pr N), review the CURRENT local branch
  before it's pushed (--local), or batch-review every open PR awaiting the user's
  (or their teams') review. Each review is saved as structured markdown with a
  resumable Claude session, and nothing is ever posted to GitHub. Use when the user
  wants a headless review of a PR or of their branch, wants to review the PRs waiting
  on them, wants to set up or schedule pr-review, or asks a follow-up question about
  a review the script produced.
---

# PR Review (headless)

## Overview

`pr-review.sh` (in this skill's directory) runs a headless `claude -p` review with a
structured prompt that a reader can corroborate. The prompt sets up a panel of three
senior engineers, and then a tech lead checks the panel's findings against the wider
codebase. Each issue gets a category (SEC/PERF/DESIGN), a severity, verbatim code
quotes and a permalink pinned to the head SHA. It also gets a stable fingerprint, so
the same issue keeps the same fingerprint across runs.

| Mode | Command | Reviews |
|---|---|---|
| Targeted | `--repo owner/name --pr N` | That one PR, whoever it's assigned to. It always re-reviews. |
| Local | `--local [--base BRANCH]` | The committed HEAD of the current branch in the repo you're in, against `origin/<base>`. The default base is the repo's default branch. Use it before a push. |
| Batch | no arguments | Every open PR where you, or one of your GitHub teams, is a requested reviewer. It skips a PR whose head hasn't changed since its last review. |

Targeted and batch modes check the PR out in a shared clone under
`~/pr-reviews/repos/`. Local mode runs in your working copy and never checks out,
resets or stashes, so uncommitted work is safe. It doesn't review uncommitted work.

Per review it saves:

- the review as markdown in `~/pr-reviews/<date>/`, named `<owner>_<repo>_PR<n>.md`
  for a PR or `<owner>_<repo>_<branch>_local.md` for a local review
- the Claude **session id**, so the review can be resumed conversationally
- the token usage and cost of the review session

It also writes a per-day `index.md` and a log at `~/pr-reviews/pr-review.log`.
Local mode prints the review file's path on stdout, so a caller can pick it up.

**It never posts to GitHub.** The Claude run is restricted to read-only tools
(`Read`, `Grep`, `Glob`, and read-only `git` subcommands).

## Requirements

`gh` (authenticated; team discovery needs a token with `read:org`), `git`, `jq` and
the `claude` CLI. It's written for macOS, using launchd and mkdir-based locking, but
it runs anywhere bash 3.2+ and those tools exist.

## Running

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/pr-review/pr-review.sh" --repo owner/name --pr 123
"${CLAUDE_PLUGIN_ROOT}/skills/pr-review/pr-review.sh" --local
"${CLAUDE_PLUGIN_ROOT}/skills/pr-review/pr-review.sh"
```

Every mode also takes `--panel FILE` and repeatable `--lens FILE`, which change the
review's perspective for one run. See Perspectives below.

A review takes several minutes. Run it in the background and read the file when it
finishes. Progress and errors go to `~/pr-reviews/pr-review.log`. Run `tail -f` on
the log to watch a run.

## Perspectives: panels and lenses

A review has one **panel** and any number of **lenses**. The panel says who reviews
and what they focus on. A lens adds rules or a reviewer on top of the panel. Repo files
are always read from the **base** branch, so a PR can't rewrite the rules it's reviewed
against.

| Source | Kind | Scope |
|---|---|---|
| `--panel FILE` | panel | This run only. It wins over every other panel. |
| `.pr-review/panel.md` in the repo | panel | Every review of that repo |
| `PANEL_FILE` in the config | panel | Every repo without its own panel |
| The built-in panel | panel | Used when nothing above sets one. Three senior engineers, then a tech lead. |
| `REVIEW.md` in the repo | lens | Every review of that repo |
| `.pr-review/lenses/*.md` in the repo | lens | Every review of that repo |
| `EXTRA_PROMPT_FILE` in the config | lens | Every repo you review |
| `--lens FILE`, repeatable | lens | This run only |

Lenses add up in that order, and the severity scale and output format never change.
The examples folder has a ready-made panel and lens:

- `${CLAUDE_PLUGIN_ROOT}/examples/panel-security-red-team.md` swaps in two attackers and a defender.
- `${CLAUDE_PLUGIN_ROOT}/examples/data-integration-lens.md` adds an integration-platform reviewer and a DATA category.
- `${CLAUDE_PLUGIN_ROOT}/examples/ponytail-lens.md` adds an over-engineering reviewer and a SIMPLE category, based on [ponytail](https://github.com/DietrichGebert/ponytail). SIMPLE findings are never High or Critical, so the lens suggests cuts without blocking a merge.

## Configuration

Put overrides in `~/.config/pr-review/config.sh`, or point `PR_REVIEW_CONFIG` at
another file. The script sources it, so you don't need to edit the script.

```bash
MINE_REPOS=(my-org)               # default () means every repo GitHub can see
TEAM_REPOS=(my-org/api)           # default () disables team pickup
MODEL=sonnet                      # default opus
EXTRA_PROMPT_FILE="$HOME/.config/pr-review/extra.md"
PANEL_FILE="$HOME/.config/pr-review/panel.md"
```

`${CLAUDE_PLUGIN_ROOT}/examples/team-setup.md` shows a full team setup with a sample
review.

| Variable | Meaning |
|---|---|
| `MINE_REPOS` | Scopes where PRs requesting **your own** review are picked up. An entry is `owner/name` for one repo, or a bare `owner` for every repo in that org. |
| `TEAM_REPOS` | Scopes where PRs requesting one of **your teams'** review are also picked up. Teams are discovered with `gh api user/teams`. |
| `MODEL` | `opus` by default. `sonnet` cuts cost at volume. |
| `CLAUDE_PERM` | Read-only allowlist. |
| `EXTRA_PROMPT_FILE` | A lens added to every review. |
| `PANEL_FILE` | The default panel for repos without `.pr-review/panel.md`. |
| `BASE_DIR` | Root for reviews, clones, state and the log. The default is `~/pr-reviews`, and `PR_REVIEW_DIR` overrides it. |

## Resuming a review conversationally

Every review file has an "Ask Claude follow-up questions" block. For a PR review it
restores the PR's exact code in the shared clone first, then resumes the saved
session. For a local review it resumes from your working copy. When the user asks a
follow-up about a specific review, read the review file, take the session id from
that block, and run exactly those steps.

## Scheduling

The script works under launchd or cron. It appends fallback directories to `PATH`
and locks against overlapping runs. This cron entry runs at 9am and noon on weekdays:

```cron
0 9,12 * * 1-5 $HOME/bin/pr-review.sh
```

## Reporting results to the user

After a run, summarize from `~/pr-reviews/<today>/index.md` and the tail of the log.
Report how many PRs were reviewed, skipped as unchanged or failed, each review's
verdict line from its `## Summary`, and the total cost. Point the user at the
markdown files rather than pasting whole reviews.
