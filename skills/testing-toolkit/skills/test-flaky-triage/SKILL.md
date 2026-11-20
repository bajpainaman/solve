---
name: test-flaky-triage
description: "Finds flaky tests from CI history, groups them by shared root cause (time, test order, shared state, network, async waits), quarantines them with an owner and an expiry date, and proposes the fix for the largest group. Use for flaky tests, intermittent CI failures, rising retry rates, \"just re-run it\", a quarantine list, or when the testing skill routes here. Not for one test that fails every time (that is a bug or a wrong test)."
---

# Flaky-test triage

Flakiness is a problem of the whole suite. A small share of runs fail for no reason, a larger share of tests show it over time, and most changes from pass to fail in CI are then flakes. Flaky tests also fail in groups that share one root cause, so one fix often clears many tests.

This skill writes no new tests. It finds the flaky ones, groups them, quarantines them safely, and proposes fixes.

## Three rules

1. **Decide from evidence.** A test is flaky when it has both passed and failed on the same commit. One failure is not evidence.
2. **Fix groups.** Group the flaky tests by root cause, and work on the largest group first.
3. **Give every quarantine an owner and an expiry date.** A quarantine with no expiry removes coverage for good, and nobody notices.

## Workflow

1. **Mine the CI history.** Collect the tests that passed and failed on the same commit over the last few weeks, with the count of each. Use the CI provider's API or stored JUnit reports. For GitHub Actions, `gh run list` and `gh run view --log-failed` give the raw data.
2. **Reproduce where it is cheap.** Run a suspect test many times, alone and in shuffled order, to learn whether it fails alone or only with other tests.
3. **Group by root cause**, with the table below.
4. **Quarantine** the tests that block merges. Mark each with the repo's mechanism, such as a tag or a skip list, and record the owner, the date, the expiry date and the issue link beside it. A quarantined test still runs, and its result does not block.
5. **Propose the fix for the largest group.** One root cause usually has one fix: a fake clock, isolated state, a wait on a condition.
6. **Report** the flake rate, the groups with their sizes, the quarantine list with owners and expiry dates, and the proposed fix.

## Root causes

| Cause | Signs | Fix |
|---|---|---|
| Time | Fails near midnight, at month end or in another timezone. Uses the wall clock or a sleep. | Inject or freeze the clock |
| Test order | Passes alone and fails in a shuffled run, or the reverse | Give each test its own state, and remove module-level state |
| Shared state | Fails only in parallel runs. Uses a fixed port, file, row or queue. | A unique resource per test |
| Network | Fails with timeouts or DNS errors against a real host | A local fake or a container, with no call to an external host |
| Async waits | Fails under load. Uses a fixed wait or checks too early. | Wait on the condition, with a timeout |
| Resource limits | Fails only on CI runners. Runs out of memory or handles. | Close resources, or lower the parallelism |

## Guardrails

- Never raise the retry count to hide a flake. A test that passes only on retry should fail the run.
- Never delete a flaky test to make the suite pass. Fix it or quarantine it with an expiry date.
- Review the quarantine list every week. An entry past its expiry date is either fixed or removed with a `test-audit` evidence ledger.
