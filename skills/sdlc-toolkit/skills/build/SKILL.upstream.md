---
name: build
description: SDLC stage 5. Implements an approved docs/sdlc/<slug>/plan.md phase by phase in ponytail mode, test first with the testing toolkit, with a verify loop and a pr-review --local run at the end of each phase. Use when the user runs /sdlc:build or the sdlc skill routes here.
argument-hint: "<slug> [phase]"
---

# Stage 5 — Build

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/pr-review.md`, `${CLAUDE_PLUGIN_ROOT}/references/ponytail.md` and `${CLAUDE_PLUGIN_ROOT}/references/testing-toolkit.md`.

The engineer already approved the plan, so Claude works through it without asking about each edit. A session checks and fixes its own work before anyone else sees it. Because pr-review reads the code without this session's context, it catches what the session talked itself into.

Feature: `$ARGUMENTS`

## Before you start

- Stop if `plan.md` isn't approved.
- Work on the feature branch recorded in `sdlc.yaml`.
- Run the verify command once, so you know the starting state.
- **Turn on ponytail mode.** Invoke `ponytail:ponytail` with the Skill tool, at its default level, before the first phase. It shapes every edit toward the smallest change that works. `ponytail.md` says what it may not change.

## Each phase

1. **Pick the phase.** Take the phase that's `in_progress` in the plan's Phases table. If it has a `Resume:` line, start from there and don't redo a checked todo. If no phase is in progress, take the first `pending` phase whose dependencies are `done`, or the phase the user named. Set it to `in_progress` and write its todos under `## Todos`.

2. **Test first.** Invoke `testing-toolkit:testing` for the phase, in its building phase, with the inputs and overrides in `testing-toolkit.md`. Invoke it even when the plan names every test, because the skill does more than write them. It takes each expected value from the spec, and after the code passes it proves that each test is stable and fails on a planted bug. It writes the phase's Build tests, which are the tests the plan chose to drive this phase's code. The plan's final tests wait for the Test stage. Write the Build tests yourself only when the session doesn't list that skill. Run the tests, confirm each one fails for the expected reason, and commit them.

3. **Make it pass.** Write the smallest change that makes the test pass, and don't edit the test to make it pass. If the test itself is wrong, stop and tell the user.

4. **Refactor and verify.** Run the verify command and paste the last lines of its output. A phase isn't done until the verify command passes. Then let the testing skill finish its checks on the phase's tests, and add its report to `docs/sdlc/<slug>/testing/build.md` under a heading for the phase.

5. **Review with pr-review.** Commit, then run `pr-review --local` with the ponytail lens and the feature's perspectives, as `pr-review.md` describes. Apply the SIMPLE cuts the owner agrees with now, while the code is cheap to change. Fix the blocking findings, commit the fixes, and run it again until none is open. Report what's fixed, new and still open.

6. **Keep `plan.md` true.** Check off each todo when it's done. When a phase's todos are all checked, the testing report has the phase's section, no test of the phase is flagged as flaky, and its review has no open blocking finding, set the phase to `done`. When the work has to depart from the plan, update `plan.md` in the same commit as the code and say what changed. If the departure changes a requirement or the RFC's design, stop and go back to that stage.

## Stopping mid-phase

When the session has to stop before a phase is done, stop where the verify command passes, or back out the last edit. Commit what's there as one `wip:` commit. Then write a `Resume:` line under the phase's todos that says what's verified, what comes next, and anything the next session wouldn't guess.

## Parallel phases

When the Phases table gives two phases a worktree each and neither depends on the other, offer to run them in separate worktrees. Use `claude --worktree <name>` in another terminal, or Agent with `isolation: "worktree"`. Start with two or three at a time. Each worktree runs its own verify loop and its own `pr-review --local`, and is merged back only after both pass.

## Finish

Build is done when every phase in `plan.md` is `done` and the verify command passes on the whole branch. Set the stage to approved in `sdlc.yaml`, commit, and hand off to `sdlc:test`.
