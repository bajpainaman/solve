# Anti-patterns and guards

Check your own tests against this list before you show them, and use it when you review someone else's tests. The first table comes first because an agent that writes tests makes these mistakes more often than a person does.

## Tests written by an LLM

| Anti-pattern | Symptom | Guard |
|---|---|---|
| The expected value is copied from the code under test | The tests pass on buggy code. They assert what the code does and not what it should do. | Write the spec first. Check with a planted bug or a mutant. |
| The same model writes the code and the tests | Both share one mistaken assumption. Coverage is high while most mutants survive. | A separate spec step, a review in a fresh context, mutation testing |
| The assertion is on a mock only | "The mock was called with X", where X is whatever the code passes | The smell scan in `test-quality-review` |
| Exact example values where an invariant exists | A passing suite misses permutations of the input | `test-property` |
| A failing test is deleted or skipped | The build passes with fewer tests | The deletion guard in `test-quality-review` |
| A failing test is "fixed" by changing its expected value | The suite now protects the bug | Never edit an assertion to match new output without a reason from the spec in the PR |
| A generated test is never checked for flakiness | It fails intermittently weeks later | Step 3 of assured generation: 5 runs in random order |

## Authored tests in general

| Anti-pattern | Symptom | Guard |
|---|---|---|
| Mocks or in-memory fakes stand in for the DB | The suite passes in CI and the code fails on real SQL, constraints or transactions | `test-integration`: real containers |
| Fixed sleeps in UI tests | Slow and flaky tests | Web-first assertions. Lint for `waitForTimeout`. |
| Retries hide flakes | A test passes on retry, and nobody fixes the flake | Fail CI on a test that passes only on retry |
| Large snapshots that people update without reading | A bug is approved into the baseline | A size limit, and an explanation in the PR for each update |
| Golden masters that stay forever | Nobody reviews them, and updates become automatic | Retire each one when real tests cover the behaviour |
| E2E tests for everything | A slow, flaky suite that the team stops trusting | `test-strategy` limits E2E to critical journeys |
| A coverage target for the whole repo | Teams reach it with low-value tests, and an untested diff hides behind the existing suite | Diff coverage plus mutation testing |

## Steps that produce results

| Anti-pattern | Symptom | Guard |
|---|---|---|
| Mutation testing of the whole codebase on every PR | Hours of CI, and results that nobody reads | Mutate only the diff. Run the full set nightly. |
| Every surviving mutant is shown to reviewers | Alert fatigue | Show 1 to 3 actionable survivors per PR |
| A quarantine entry with no expiry or owner | Coverage shrinks and nobody notices | An owner and an expiry date, with a weekly review |
| Soak or stress tests in PR CI | PRs take hours, and the team disables the job | A smoke run on the PR. Heavier runs on a schedule. |
| Thresholds on average latency | Regressions in the tail ship | Thresholds on p95 and p99 |
| A chaos experiment with no hypothesis or stop condition | The experiment becomes an incident | `chaos-experiment` refuses to finish without steady state, blast radius and stop conditions |
| The eval dataset is edited in the same change as the prompt | The score rises because the test got easier | Version the dataset, and record its version in every run |
| Regression evals that sit at 100% for weeks | They no longer catch anything | Promote harder capability cases into the regression set |
