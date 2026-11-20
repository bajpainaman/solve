---
name: pr-review
description: "Runs a headless, read-only code review of one GitHub PR, of the current local branch before a push, or of every PR waiting on the user, through the bundled pr-review.sh. Saves structured Markdown with severities, quotes, permalinks and a resumable session, and never posts to GitHub. Use when asked for a headless PR review, a pre-push review of a branch, a batch of pending reviews, or a follow-up on one of those reviews. Needs gh, git, jq and the claude CLI."
license: MIT
---

# PR review

Vendored from [aasimsani/pr-review](https://github.com/aasimsani/pr-review) (MIT, see `LICENSE`) at the commit in `SOURCE`. Change it only through `bin/vendor-sync pr-review` in the solve repository.

`TOOLKIT_ROOT` is the directory that contains this file. Read `TOOLKIT_ROOT/skills/pr-review/SKILL.upstream.md`, the upstream instructions, and follow it. Its `${CLAUDE_PLUGIN_ROOT}` is `TOOLKIT_ROOT`; the script is `TOOLKIT_ROOT/skills/pr-review/pr-review.sh`. Panel and lens examples are under `examples/`.

Each run starts a separate `claude -p` session that spends model usage. Say which mode will run and ask before the first run in a session, unless the user asked for it in those words. Without the `claude` CLI, `gh` or `jq`, say the review did not run.

## Boundaries with neighbours

| Request | Goes to |
|---|---|
| Review a whole diff for bugs, security and design | this skill |
| Review only the tests in a diff | `testing-toolkit` (`test-quality-review`) |
| Review an architecture, API or schema against DPI principles | `cdpi` |
| Review a UI's design quality | `impeccable` (`critique` or `audit`) |
| Check a "never" or "exactly once" claim in the PR | `fv-toolkit` |
| Turn findings into a page others review | `solve` make mode (`pr-review` template) |

## After the work

Offer the next step that fits the findings: fix the blocking ones, add the missing tests with `testing-toolkit`, or check a concurrency claim with `fv-toolkit`.
