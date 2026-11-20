---
name: plan
description: SDLC stage 4. Turns the approved RFC's phases into an executable plan in plan mode, decides the tests with the testing toolkit, has EGM's implementation-readiness Goldfish check it, and commits docs/sdlc/<slug>/plan.md. Also adopts or reviews a plan someone else wrote. Use when the user runs /sdlc:plan or the sdlc skill routes here.
argument-hint: "<slug> [--adopt <path|url>] [--review]"
---

# Stage 4 — Plan

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/egm.md`, `${CLAUDE_PLUGIN_ROOT}/references/ponytail.md` and `${CLAUDE_PLUGIN_ROOT}/references/testing-toolkit.md`.

The RFC says which phases and PRs exist. The plan says exactly which files change, in what order, with which test first. Build is test first, so the plan is where the tests get decided. Planning happens in plan mode, where Claude can read the code but can't change it.

Feature: `$ARGUMENTS`

## Author mode

1. **Enter plan mode** with EnterPlanMode. Stop if the RFC isn't approved or skipped. When the RFC was skipped, take the design from the spec and the code.

2. **Read `spec.md`, the RFC and every file the change touches,** along with the tests around those files.

3. **Decide the tests.** Invoke `testing-toolkit:testing`, with the inputs and overrides in `testing-toolkit.md`. It classifies the change and picks a kind of test for each component, and it writes no test in this stage. Then sort each test into the Build tests, which drive a phase's code, or the final tests, which need the whole feature. `testing-toolkit.md` has the rule, and the two final tests that are the default: an end-to-end check for each criterion with a user path, and a differential test for each change that must keep behaviour. When the RFC stage left a property ledger in `fv/design/`, pass it too, so each confirmed property gets its tests, as `${CLAUDE_PLUGIN_ROOT}/references/fv-toolkit.md` describes. Without the toolkit, choose and sort the tests yourself.

4. **Draft the plan** with the template's sections. Keep the RFC's phases and PR boundaries. Put the chosen tests in the Tests section. Every acceptance criterion must map to a test, and every phase takes its first failing test from its Build rows. Describe every phase, and write todos for the first phase only.

5. **Challenge the plan.** Before showing it, take these two passes and fold the answers into the phases:
   - **Risk.** Ask what could break that the tests won't catch, and which step is riskiest.
   - **Size.** Run the ladder in `ponytail.md` on every new file, class, dependency and config option in the plan. Replace each one that fails the ladder with the smaller option it names, such as an existing helper, a standard library call, or nothing. Keep everything `spec.md` requires.

6. **Apply the stranger test.** Someone who has never seen this conversation should be able to implement the plan from the file alone.

7. **Present it** with ExitPlanMode. Revise until the engineer accepts it.

8. **Write `docs/sdlc/<slug>/plan.md`** after leaving plan mode. From here on it's the feature's one plan file and its todo list. The draft that plan mode kept is no longer used.

9. **Gate.** The Goldfish review is `egm-review` with the `implementation` preset, using the inputs in `egm.md`. Commit `plan.md`, its report and `sdlc.yaml` together.

## Adopt and review modes

Follow `stage-rules.md`, using the same Goldfish review.

## Template

```markdown
# <Feature title> — plan

Verify command: `<from CLAUDE.md>`

## Files to change
| File | Change |
|---|---|
| `path/to/file` | <what changes and why> |

## Phases
| # | Phase | Covers | Depends on | First failing test | Runs in | Status |
|---|---|---|---|---|---|---|
| 1 | <name> | AC1, PR 1 in the RFC | — | `<test file>::<test name>` | main session | in_progress |
| 2 | <name> | AC2, PR 1 in the RFC | 1 | `<test file>::<test name>` | worktree `<name>` | pending |

Status is `pending`, `in_progress` or `done`. One phase is in progress per session or worktree.

### Phase 1 — <name>
<What this phase builds, in enough detail for a stranger to implement it.>

### Phase 2 — <name>
<...>

## Todos
Only a phase that's in progress has todos here. Build writes the next phase's todos when it starts that phase.

### Phase 1 — <name>
- [ ] Write the failing test `<test name>` and watch it fail
- [ ] Implement <thing> until the test passes
- [ ] Refactor, run the verify command, and run pr-review

## Tests
Build writes each Build test before the code it tests. Test writes the final tests, which need the whole feature.

- Scenario: <the testing toolkit's scenario for the change>. Done when: <the playbook's condition for it>.
- Left out: <kind of test — reason>

| Acceptance criterion | Test | Kind | Written in | Where the bug would be |
|---|---|---|---|---|
| AC1 | `<test file>::<test name>` | <unit, integration, ...> | Build, phase 1 | <the component's own logic, or the boundary it crosses> |
| AC2 | `<test file>::<test name>` | <end-to-end, load, ...> | Test | <the user's journey, or the hot path under load> |
```
