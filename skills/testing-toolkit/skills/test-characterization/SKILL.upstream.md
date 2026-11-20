---
name: test-characterization
description: "Pins the current behaviour of legacy code that has no tests, before a refactor or a migration. Records behaviour on untouched code, removes time, IDs and randomness from the output first, proves each pin can fail with a planted bug, and marks the pins as scaffolding to retire. Also covers approval, golden-master and snapshot tests. Use for characterization tests, golden master, approval tests, snapshot tests, \"I need to refactor this and it has no tests\", \"pin the behaviour first\", or when the testing skill routes here. Not for new code that has a spec (use test-unit)."
---

# Characterization tests

A characterization test records what the code does today, so that a refactor can be checked against it. It is the one kind of test whose expected values come from running the code. That makes two things necessary: the recorded output must be the same on every run, and the pin must be shown to fail when the behaviour changes.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md`, except that step 1 does not apply to the recorded values. This file adds the rules that are specific to characterization tests.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| ApprovalTests.Python, syrupy | Jest or Vitest snapshots, ApprovalTests.NodeJS | ApprovalTests.Java | go-approval-tests, cupaloy | insta |

A plain assertion on a recorded value needs no library. Use one only when the repo already has it or the output is too large for an inline value.

## Five rules

1. **Record on untouched code.** Confirm that the file under test has no uncommitted change before you record. Do not fix anything you notice.
2. **Remove time, IDs and randomness first.** Freeze the clock, seed the random source, and replace generated IDs at the seam. Where a value can't be controlled, mask it in the output before you compare.
3. **Prove that each pin can fail.** Plant a behaviour change in the code, see the pin fail, and restore the code. A pin that survives every change records nothing.
4. **Keep each recorded output small enough to review.** Pin one behaviour per test. A snapshot above about 50 lines gets approved without being read.
5. **Mark the pins as scaffolding.** Name or mark them as characterization tests, and say in a comment that they record current behaviour, which may include bugs. They retire when tests written from a spec cover the same behaviour.

## Reject the test if

- Two runs record different output.
- The snapshot is too large for a person to review.
- An update to a snapshot has no explanation.

## Workflow

1. **Check the working tree.** The code under test has no uncommitted change.
2. **Find the seams.** List the inputs, the outputs, and the side effects: files, calls, rows, messages. List each source of non-determinism.
3. **Control the non-determinism** from the test where you can. When the code needs a seam, make the smallest mechanical change, such as an injected clock with the old behaviour as its default, and tell the user.
4. **Choose inputs that reach every branch.** Reading the code to choose inputs is correct here. Use branch coverage to find the branches no input reaches yet.
5. **Record, then run twice more.** The recorded values must match on every run.
6. **Plant bugs.** Change one branch at a time, confirm that a pin fails, and restore the code.
7. **Report.** Use the table from step 6 of assured generation. In place of a spec sentence, each row says which behaviour the pin records. Add a section named "Pinned and possibly wrong" for behaviour that looks like a bug. Leave that behaviour in place, because the refactor must not change it by accident.

## Snapshots

A snapshot that people regenerate without reading protects nothing. Keep snapshots small, mask dynamic values, and require an explanation in the PR for every update. Prefer an assertion on the fields that matter over a snapshot of a whole object or page.

## The report

End your reply with this table, even when you wrote one pin. The user reads it to decide whether each row earns its place.

| Pin | Behaviour it records | Change that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```python
# Bad. The receipt holds the current time and a random id, so the recorded
# text differs on every run, and the whole receipt sits in one snapshot.
def test_receipt(snapshot):
    assert render_receipt(order) == snapshot
```

```python
# Good. Time and id are fixed at the seam, each test pins one behaviour, and
# the marker says what the test is for.
@pytest.mark.characterization  # Records current behaviour. Retire when spec tests cover receipts.
def test_receipt_totals_round_each_line_before_summing(frozen_clock, fixed_ids):
    receipt = render_receipt(order_with(lines=[("A1", 3, 0.335)]))
    assert receipt.total == "1.02"  # 3 x 0.34; a sum-then-round version gives 1.01
```

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` | Before you show the tests |
