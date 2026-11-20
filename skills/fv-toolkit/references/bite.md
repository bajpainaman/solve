# Make the check bite

A green run shows that nothing bad was observed. It does not show that the check would have noticed. Do every item below before you report a pass.

## Two-sided

A check must be red on the bad version and green on a named good version. A check that is green everywhere cannot see the bug.

- For a design model, the bad version is the config of the rejected design, and the good version is the config of the chosen design.
- For a test on real code, the bad version is the code under review or the commit before a fix. The good version is the fixing commit, the base of the PR, or your patch, in that order of preference.
- Red on both sides means a defect that existed before the change, or a wrong check. A patch that fixes only the suspect tells which one you have.

Record both commands and both outputs.

## Plant bugs

Write a `<Name>.mutations` file beside the model or the test, and run `fv-mutate` on it. The script applies each edit to a temporary copy, so the real files never change.

```text
run fv-tlc RefundRace.tla AtomicRefund.cfg WitnessFullRefund.cfg
properties NeverOverRefund
file RefundRace.tla

mutation the atomic refund ignores what was already refunded
detects NeverOverRefund
-     /\ refunded' = refunded + (Paid - refunded)
+     /\ refunded' = refunded + Paid

harmless a comment on the invariant
- NeverOverRefund == refunded <= Paid
+ NeverOverRefund == refunded <= Paid  \* the cap is the payment
```

Rules for the list:

- **One mutation per claim at least.** Use the smallest edit that breaks the claim: flip a comparison, drop a guard, skip a status, swap two writes, replace `while` with `if`, remove a broadcast.
- **One mutation per past fix.** For each commit that fixed a bug in the covered code, restore the behaviour from before the fix and put the commit's short hash in the label. A check that passes on the code before a fix would not have caught that bug.
- **One mutation outside the suspect.** Plant at least one bug in something the suspect depends on, such as a caller, a config value or a filter.
- **One harmless edit.** Add an edit that changes nothing a caller can observe. It must stay green. A check that turns red on every edit is not evidence either.
- **List the properties.** Put every property on the `properties` line, so the script reports `UNCOVERED` for a property that no mutation detects.

Read the verdicts this way:

| Verdict | What to do |
|---|---|
| `DETECTED` | Nothing. The property fails on this bug |
| `MISSED` | The property lets this bug pass. Strengthen the property or the inputs, and rerun. If the edit changes nothing observable, replace the mutation |
| `ERROR` | The check failed for another reason, or the text to replace did not occur once. Fix the mutation |
| `UNCOVERED` | No mutation detects this property. Add one |
| `BRITTLE` | A harmless edit turned the check red. Find what the check really depends on |

For a property test, the mutation edits the code under test, and the `run` line calls the test runner. Set `root` to the project directory, so the copy holds both the code and the tests. The copy leaves out `.git`, `.venv` and `node_modules`. When the test runner lives in the project's own environment, name it through `FV_ROOT`, which holds the path of the original root: `run "$FV_ROOT/.venv/bin/python" -m pytest -q tests`.

## Not vacuous

- **Every case asserts.** Count the cases that reach each assertion and assert that the count is above zero. A case that a guard in the test skips asserts nothing.
- **TLA+.** Each model has a witness config whose invariant says that the interesting state is never reached. That config must be violated.
- **Alloy.** Each `check` has a satisfiable `run` beside it. An assertion that the signature multiplicities already force is a tautology.
- **Hypothesis.** A strategy that an `assume` filters almost empty exercises nothing. Build the constraint into the strategy.

## Draw the cases from outside the change

Define the cases of a claim by something the change cannot move: the files under a folder, the statuses a record can take, the row types in a table. "The cases that reach the changed function" shrinks when the change is wrong.

## Probe the boundaries

Give every comparison an input exactly on it: the instant a range opens and the instant it closes, a value equal to a limit, an empty collection, a key that two rows share.

## Re-runnable

Leave one command per check that reproduces it from a clean checkout. A hand-written model cannot see an edit to the code, so say that in the report. A test that drives the real entry point can.
