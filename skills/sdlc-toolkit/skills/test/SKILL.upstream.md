---
name: test
description: SDLC stage 6, Test & Prove. Tests the finished feature, then proves it to the approver. Writes the final tests and audits the suite with the testing toolkit, runs a final pr-review --local, dispatches the fresh-context verifier subagent, asks the approver whether they want a demo, and commits docs/sdlc/<slug>/verify.md with the proof page beside it. Use when the user runs /sdlc:test or the sdlc skill routes here.
argument-hint: "<slug>"
---

# Stage 6 — Test & Prove

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/pr-review.md`, `${CLAUDE_PLUGIN_ROOT}/references/testing-toolkit.md` and `${CLAUDE_PLUGIN_ROOT}/references/proof.md`. When the feature has a property ledger in `fv/design/`, it uses `${CLAUDE_PLUGIN_ROOT}/references/fv-toolkit.md` too.

The build session already ran its own checks. This stage has two halves, and each one answers its own question.

- **Test** asks whether the checks pass. A green suite proves only what its tests check, so this half finishes the testing first. It writes the tests that need the whole feature, checks the tests Build wrote, audits the suite, and has pr-review read the whole branch.
- **Prove** asks whether the approver can see the feature work. Agents that didn't write the code run it and model it. The approver gets a demo when they want one. Then one proof page puts the evidence in front of them, so they can decide without rerunning anything.

Feature: `$ARGUMENTS`

## Test

1. **Run the final tests and check the rest.** Invoke `testing-toolkit:testing` on the whole branch, in its testing phase, with the inputs and overrides in `testing-toolkit.md`. It writes and runs the tests the plan left for this stage, such as an end-to-end or a load test. It checks Build's tests against the plan's Tests section, finds changed code that no test checks, and writes the missing tests. Commit the tests it adds. Without the toolkit, write the final tests yourself and record why the check didn't run.

2. **Audit the tests.** Invoke `testing-toolkit:test-audit` on the test files the branch added or changed, as `testing-toolkit.md` describes. It removes or merges a test only when a stronger test covers the same contract, and it writes a ledger that says so. This is the stage's last change to the tests, so every later step sees the suite that ships.

3. **Run the verify command** on a clean checkout of the feature branch, and keep the literal output.

4. **Check the UI if there is one.** Open it with the browser tools, take screenshots, and compare them against the spec or the mockups.

5. **Run the final `pr-review --local`** on the whole branch, as `pr-review.md` describes, and compare it with the last Build run. A blocking finding sends the feature back to Build. This run also catches over-engineering that only shows across phases, such as an option no phase ended up using, so record its "Net:" line in `verify.md`.

6. **Run the agent evals if the diff changes them.** When the diff touches `CLAUDE.md`, `.claude/**` or skills, and the repo has an eval suite, run it and record the pass rate.

## Prove

7. **Dispatch the `verifier` subagent.** Pass it the paths to `spec.md` and `plan.md` and the verify command. It runs the app, exercises each acceptance criterion and reports what it saw. It never fixes anything. Dispatch it even when the testing report has a `Verified:` line, because that run came from the session that tested the code, and the verifier's comes from a fresh context. Wait for its report before you write `verify.md`.

8. **Model the code afresh, when the design was modelled.** If the feature has a property ledger, check its pins and dispatch the `fv-verifier` subagent, as `fv-toolkit.md` describes. It writes its own model from the code, without the RFC's model or the plan in view. Compare the two models property by property, and commit the model it wrote. A feature with no ledger skips this step.

9. **Ask the approver whether they want a demo.** Ask for every feature, with a UI or without one, and ask before you build the proof page. Say what the demo would be: a recording of the change for a feature with a UI, or a walkthrough with its real output for a feature without one. On a yes, invoke `sdlc:demo`. On a no, the approver's answer is the skip reason, such as "Lee declined". Never answer for them. When nobody can answer during the run, carry on with the next steps, leave `demo` out of the stage's `tools`, and say that the stage waits on that answer.

10. **Write `docs/sdlc/<slug>/verify.md`** from the template. Every acceptance criterion needs evidence a reader can check, such as a test name, command output or a screenshot path. When the repo has a verification skill, add or update its feature file for this feature on the same branch, so the next change to the feature is checked the same way.

11. **Build the proof page**, `docs/sdlc/<slug>/proof/proof.html`, as `proof.md` describes. Every feature gets one, with a demo or without. It shows each criterion with its evidence, the demo or the reason there isn't one, and the parts of the formal checks that the approver needs to see. A stage that fails gets its page too, so the approver sees what failed.

12. **Gate.** If any criterion fails, a test the testing skill wrote fails on the code, the code breaks a confirmed property, or the verifier sees behavior that doesn't match the plan, add a phase to `plan.md` for the failures and go back to `sdlc:build`. If everything passes, give the approver the proof page and ask for approval. Then commit `verify.md`, everything in `proof/`, the testing report, the audit ledger, the pr-review report and `sdlc.yaml` together.

## Template

~~~markdown
# <Feature title> — verification

## Verify command
`<command>`

```
<last 20 lines of literal output>
```

## Acceptance criteria
| Id | Evidence | Result |
|---|---|---|
| AC1 | `<test name>` passes, and the verifier saw <what> | pass |

## Tests
- Report: `testing/test.md`, for the scenario <scenario>
- Verified: <the report's `Verified:` line, as it reads>
- Done when: <the playbook's condition, and whether it holds>
- Final tests: <test names, each with its result>
- Tests added to close a gap: <test names, or none>
- Audit: `testing/audit.md`, with <n> tests removed or merged

## Formal checks
Leave this section out when the feature has no property ledger.

| Property | Design model | Code model | Bounds and faults |
|---|---|---|---|
| <the property as one sentence> | holds | holds | <the sizes checked, and the faults switched on> |

- Report: `fv/code-report.md`
- Left open: <what the two passes don't cover>

## Verifier report
<The verifier subagent's report, verbatim.>

## pr-review
- Report: `pr-review/test-1.md`, with verdict <verdict> and totals <Critical n, High n, Medium n, Low n>
- Net: <the ponytail lens's "-N lines and -M dependencies possible", or "lean already">
- SIMPLE cuts left in, with reasons: <fingerprint — reason>
- Fixed since Build: <fingerprints>
- Open, with reasons: <fingerprint — reason>

## Proof
- Page: `proof/proof.html`
- Demo: <`proof/demo.md`, with its kind and recorder. Or "none", with the approver's reason. Or "waiting on <approver>'s answer">

## Gaps
- <anything untested, and why>
~~~
