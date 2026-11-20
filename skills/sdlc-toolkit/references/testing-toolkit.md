# Running the testing toolkit

The [testing toolkit](https://github.com/aasimsani/testing-toolkit) decides which kinds of test a change needs and writes them from the spec. Its `testing` skill classifies the change, picks a kind of test for each component and calls the toolkit's other skills in order. Invoke `testing-toolkit:testing` with the Skill tool, and let it choose the other skills. The one skill a stage names itself is `test-audit`, at the end of Test. `sdlc:setup` installs the toolkit.

The skill names a phase before it picks a kind of test, and the phase decides which kinds it may pick. This loop builds test first, so it splits the job across three stages. Plan decides the tests. Build writes the ones that drive the code. Test writes the ones that need the whole feature, checks all of them and audits the suite. So pass the skill the stage's phase, inputs and overrides each time you invoke it.

## Two sets of tests

The plan sorts every test into one of two sets. Each set matches one of the skill's phases, so the stage that writes a test also tells the skill which phase it is in.

| | Build tests | Final tests |
|---|---|---|
| What they're for | Each one drives one phase's code | Each one checks the feature once every phase is on the branch |
| A test belongs here when | It can fail before the phase's code exists, and it runs inside the verify command | It needs the whole feature, it takes a long run, or it measures the tests themselves |
| The skill's phase | Building, test-first | Testing code that exists |
| Written | Before the code, one phase at a time | In the Test stage |
| When one fails | The phase isn't done | The feature goes back to Build as a new phase |

The skill's phase table decides which kinds of test fit each set, and in the testing phase it ranks them. So this file names the phase and leaves the kinds to the skill.

## Plan decides the tests

Invoke it after you've read the spec, the RFC and the code the change touches.

| Input | What to pass |
|---|---|
| The change | The RFC's phases, and the files each phase touches |
| The spec | `spec.md`, and the RFC for an interface |

1. **The skill stops after its choice.** It classifies the change, and writes down the kind of test each component gets and the kinds it leaves out. It writes no test in this stage. Ask it for both phases: the building phase's tests for each RFC phase, and the testing phase's tests for the finished feature.
2. **Each test gets a stage.** Sort every chosen test into the Build tests or the final tests with the table above. The testing phase ranks the kinds an agent's own assumptions can't satisfy first, so two final tests are the default. Each acceptance criterion that a user or a caller can drive, through a page, a command or an endpoint, gets an end-to-end check. Each change that must keep behaviour, such as a refactor or a migration, gets a differential test. Leave either one out only with a reason in the Tests section.
3. **The choice goes in `plan.md`.** Fill the plan's Tests section from it: the scenario, the playbook's "Done when" condition, one row per test with the stage that writes it, and the kinds left out. Each acceptance criterion maps to at least one row, and each phase takes its first failing test from its Build rows.
4. **Adopt and review modes compare.** Run the skill the same way, and give the approver each difference between its choice and the plan's tests.

## Build writes the Build tests first

Invoke it at each phase's test-first step.

| Input | What to pass |
|---|---|
| The phase | Building, test-first |
| The change | The phase's section of `plan.md`, and the phase's Build rows in the Tests section |
| The spec | `spec.md`, and the RFC for an interface. Every expected value comes from them. |

1. **The plan already made the choice.** The skill skips its classification, takes the scenario and the kinds of test from the plan, and writes the phase's Build tests from the spec. It leaves the final tests to the Test stage.
2. **The phase's order wins over the playbook's.** A new test fails at the test-first step, because the code doesn't exist yet. A test that pins current behaviour, such as one written before a refactor, passes at this point. After the phase's code passes, the skill finishes its checks on each test. Each one passes, gives the same result over five runs, and fails on a planted bug or a mutant.
3. **A flaky test holds the phase.** When a test gives different results over the five runs and the skill can't find the cause, it keeps the test and flags it as flaky, and it never adds a retry or a sleep. The phase isn't done while a test is flagged. Find the cause with `testing-toolkit:test-flaky-triage` and fix it, or take the test to the user. A flaky test that drives the code is a test the next phase can't trust.
4. **The phase writes the code.** The playbook's fix, change and refactor steps are the phase's own steps. A playbook step that acts on a running system, such as a canary or a chaos experiment, waits for Ship, and the report lists it as not run.
5. **A change to the tests is a departure from the plan.** When the skill's checks drop a planned test or call for another one, update the plan's Tests section in the same commit and say what changed.
6. **The report is a file.** Add the skill's report to `docs/sdlc/<slug>/testing/build.md`, under a heading for the phase.

## Test writes the final tests, checks all of them and audits

Invoke `testing-toolkit:testing` at the stage's first step, and `testing-toolkit:test-audit` at its second.

| Input | What to pass |
|---|---|
| The phase | Testing code that exists |
| The change | The branch's diff against the default branch |
| The spec | `spec.md`, and the Tests section of `plan.md` |

1. **The skill writes and runs the final tests.** These are the rows the plan gave to Test. The whole feature is on the branch now, so each one should pass. A committed end-to-end test is only for a journey whose failure would be an incident. Every other change with a user path gets one run of the real system, and the skill's report says what that run showed.
2. **It checks the tests Build wrote.** It runs the playbook's analysis steps on the diff, such as `test-quality-review` and `test-mutation`. Then it checks that the plan's "Done when" condition holds, and that every row in the Tests section has its test.
3. **It adds tests and changes no product code.** Let it write the tests that close a gap, and commit them on the feature branch.
4. **A test that fails on the code sends the feature back to Build.** The toolkit would keep such a test as an expected failure. Here it becomes a phase in `plan.md`.
5. **The report is a file.** Save it as `docs/sdlc/<slug>/testing/test.md`. Copy its `Verified:` line into the Tests section of `verify.md`, and its "Not run" and "Unspecified" lists into the Gaps section. The `Verified:` line is the testing session's own run of the feature, so it doesn't replace the `verifier` subagent, which runs the feature again from a fresh context.
6. **The audit comes after every other change to the tests.** Invoke `testing-toolkit:test-audit` in its audit mode, on the test files the branch added or changed. It removes or merges a test only when its ledger names the stronger test that covers the same contract. Save the ledger as `docs/sdlc/<slug>/testing/audit.md`, and write "no candidates" in it when the audit removes nothing. When the audit removes or merges a test the plan names, update the plan's Tests section in the same commit.

## When the toolkit isn't installed

The session lists `testing-toolkit:testing` among its skills when the toolkit is installed. Without it, Plan chooses the tests itself, Build writes each failing test itself, and Test writes the final tests itself and skips the check and the audit. Record the stage's `testing` tool as skipped, and the Test stage's `test-audit` tool too, with that reason. Tell the user that `sdlc:setup` installs the toolkit.
