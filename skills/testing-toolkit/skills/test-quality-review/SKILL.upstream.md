---
name: test-quality-review
description: "Reviews the tests in a diff with three cheap checks: coverage of the changed lines, a guard on deleted or skipped tests, and a scan for test smells such as no assertions, assertions only on mocks, sleeps, catch-all handlers, large snapshots, and use of the clock or the network. Use to review tests in a PR, check tests an agent wrote, set up a diff coverage gate, answer \"are these tests any good\", or when the testing skill routes here. Not for a mutation run (use test-mutation) or for pruning an existing suite (use test-audit)."
---

# Test quality review

This skill writes no tests. It runs three checks on the tests in a diff, separates the findings that matter from the noise, and hands real gaps to an authoring skill.

## Check 1. Coverage of the changed lines

Measure coverage of the lines the PR changed, never a percentage for the whole repo. A number for the whole repo hides an untested change behind a large existing suite. Teams commonly gate at 70% to 80% of changed lines.

```bash
diff-cover coverage.xml --compare-branch origin/main --fail-under 80
```

Coverage shows that a line ran. It does not show that a test checked the result. Report uncovered changed lines as gaps, and never report covered lines as tested. Pair this check with `test-mutation`.

## Check 2. The deletion guard

List every test that the diff deletes, skips, marks as an expected failure or comments out, and every assertion whose expected value changed. Each one needs a reason:

- A deletion is acceptable with an evidence ledger from `test-audit`, or when the code it tested is deleted in the same diff.
- A changed expected value is acceptable with a reason from the spec in the PR.
- Anything else is a blocking finding. Removing a failing test is the easiest way to make a build pass.

## Check 3. The smell scan

| Smell | Why it matters |
|---|---|
| A test with no assertion, or only "does not throw" | It passes on any behaviour |
| Assertions only on mocks | It checks the call and not the result |
| An expected value computed by the code under test | It can't fail |
| `sleep` or a fixed wait | Slow and flaky |
| A catch-all exception handler in a test | It hides the failure it should report |
| A snapshot file above about 50 lines | Nobody reads the update |
| Reads of the system clock or the network | The result depends on when and where it runs |
| The module under test is itself mocked | The test checks the mock |

`${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` holds the longer list with the guard for each.

## Workflow

1. **Compute the diff** against the base branch, and split it into production code and tests.
2. **Run the three checks.** When no coverage report exists, run the suite with coverage on. If that isn't possible, say that check 1 did not run.
3. **Rank the findings**: blocking first, then gaps, then smells. Keep the list short enough to act on, and merge repeats of one smell into one finding with a count.
4. **Report** each finding with its file and line, the reason, and the skill that closes it.

## Report format

```text
BLOCKING  tests/test_refund.py:88   test_partial_refund is now skipped, and the PR gives no reason.
GAP       src/refund.py:41-47       The changed lines are not covered. Hand to test-unit: the branch for a refund above the payment.
SMELL     tests/test_notify.py:12   The only assertion is mock.assert_called_once(). Assert the message that was sent.
```
