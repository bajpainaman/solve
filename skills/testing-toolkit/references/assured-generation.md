# Assured generation

Every authoring skill in this plugin runs its tests through these steps before it shows them to the user. A model that reads buggy code tends to write tests that assert the bug. The steps make sure that each expected value comes from outside the code, and that each test has been seen to fail.

A step that you could not run is not a pass. Name it in the report.

Keep the steps cheap. Run the five repeats of step 3 in one shell command. In step 4, plant one bug for each rule that matters, up to five in total, and prefer one command that plants the bug, runs the tests and restores the file.

## Step 0. Decide whether the test should exist

Answer four questions for each test before you write it. Drop the test when you can't answer one of them.

1. **What contract does it protect?** Name the behaviour, invariant, API or regression in one line.
2. **What credible bug would make it fail?** Describe one concrete wrong change to the code.
3. **Why doesn't an existing test already catch that bug?** Each contract has one owning test at the strongest boundary. When a near-duplicate exists, add a row to its table of cases.
4. **Does it need a hook in production code that no real caller uses?** If it does, test at the real boundary.

A test that breaks when someone refactors without changing behaviour asserts the implementation. Rewrite it at the public boundary or drop it.

## Step 1. Write the spec before you read the code

Write down the expected behaviour first. Take it from the ticket, the docstring, the API spec, the README or the user. Read the implementation afterwards, and only for names, signatures and seams.

- Every expected value in an assertion comes from the spec. Never run the code to learn what to assert. Characterization tests are the one exception, because they record current behaviour on purpose.
- When the spec says nothing about a case, ask the user or leave the case out. List it under "Unspecified" in the report.
- When a test written from the spec fails on the current code, you may have found a product bug. Keep the assertion. Report the spec sentence, the expected value and the observed value, and let the user decide. Never change an expected value to match the code's output without a reason from the spec.

## Step 2. The test builds and passes

The test compiles and passes on the current code. For a bug fix, it fails on the old code and passes on the fix, and you show both runs.

A test that fails because the code disagrees with the spec stays in the report as a finding. Mark it as an expected failure with the reason, so that the suite stays green and the finding stays visible.

## Step 3. The test is not flaky

Run the new tests 5 times, in random order where the runner supports it. Any run that differs makes the test flaky. Fix the cause: a sleep, the wall clock, the network, shared state or test order. When you can't find the cause, keep the test, flag it as flaky with the reason in a comment on the test and in the report, and hand it to `test-flaky-triage`. Never add a retry or a sleep to make it pass.

| Runner | Command |
|---|---|
| pytest | `pytest -p randomly` when pytest-randomly is installed. Otherwise run the file 5 times and run each new test once alone. |
| Vitest | `vitest run --sequence.shuffle`, 5 times |
| Jest | `jest --randomize`, 5 times |
| Go | `go test -count=5 -shuffle=on ./...` |
| JUnit 5 | `junit.jupiter.testmethod.order.default=org.junit.jupiter.api.MethodOrderer$Random`, 5 times |
| cargo | `cargo test`, 5 times |
| Playwright | `npx playwright test --repeat-each=5 --retries=0` |

## Step 4. The test adds value

A test stays only when it can fail for a reason that nothing else catches. Collect one piece of evidence per test, and prefer the first that is available:

1. **A killed mutant.** The test kills a mutant on the changed lines that the existing suite does not kill. `test-mutation` runs this.
2. **A planted bug.** Make the wrong change from question 2 of step 0 in the code, run the test, and see it fail. Restore the code and confirm that the working tree holds no leftover change.
3. **A covered line.** The test covers a changed line that no other test covers. This is the weakest evidence, because coverage shows that a line ran and not that anything checked it.

Discard a test that has none of these, however good it looks.

## Step 5. The test is readable

Each test checks one behaviour, and its name states that behaviour. No assertion restates the implementation.

## Step 6. Report

Show only the tests that passed every step. Give one row per test:

| Test | Contract it protects | Bug that would make it fail | Evidence |
|---|---|---|---|
| `test_discount_applies_at_ten_items` | "Orders of 10 or more items get 10% off" (README) | The comparison becomes `> 10` | Planted that change, and the test failed |

Then add the sections that apply:

- **Findings.** Each place where the code disagrees with the spec, with the spec sentence, the expected value and the observed value.
- **Unspecified.** Each case the spec does not decide, as a question for the user.
- **Dropped.** How many tests you wrote and discarded, and at which step.
- **Not run.** Each step you could not run and why, such as "no Docker, so the integration tests were written and never executed".
- **How to run.** One command.
