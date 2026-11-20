# An independent review of the properties

A property can pass every check and still promise less than the callers of the code rely on. The author of a model reads the properties through the model. A reviewer who sees only the code and the properties reads them fresh.

## When to offer it

Offer the review after the first run in which every check meets its declared outcome and every mutation is detected. The review costs one more agent per model, so ask the user once whether they want it. When the user cannot answer, skip the review and say in the report that the properties were not reviewed.

## Who reviews

Start one agent per model, with a fresh context. When the host offers a choice, use a different model from the one that wrote the check.

Give the reviewer these things:

- the claims table and the property ledger;
- the source files, with their line ranges;
- the model or the test files, with their configs and their mutations file;
- this file.

Do not give the reviewer your report, your reasoning or your counterexamples. The reviewer writes no files.

## The four questions

The reviewer reads each source file in full, then the properties, and asks these questions of every property.

1. **Does a caller rely on a guarantee that no property states?** Name the guarantee and the calling function.
2. **Does an assumption exclude inputs or schedules that shipped callers produce?** An assumption is a fairness condition, a constraint, a scope, a precondition, a strategy bound or an `assume`. Cite the caller's `file:line`.
3. **Would a plausible bug still pass?** Try an off-by-one at a boundary, a lost wakeup, a step done twice, results in the wrong order, and each past fix undone.
4. **Does the check leave out a branch, an error path or a step that the code has?** Name the line.

## What the reviewer returns

- Each finding that a planted bug can show, written as a mutation in the format of `bite.md`, with the question it answers and the `file:line` it rests on.
- Each finding that no mutation can express, such as a guarantee that no property states, with its `file:line`.
- "No findings", when there are none.

The reviewer does not restate the model, grade it or rewrite it.

## What to do with the result

Append the proposed mutations to the mutations file and run `fv-mutate`.

| Verdict | Action |
|---|---|
| `DETECTED` | Keep the mutation |
| `ERROR`, because the edit does not apply | Drop the mutation |
| `MISSED`, and the edit changes nothing a caller can observe | Drop the mutation, and say so |
| `MISSED` otherwise | The property lets a plausible bug pass. Strengthen the property or add the missing step, then rerun. A pinned property changes only with the user's agreement |

Run one round of review per model. Report each finding that no mutation can express as an open question, and leave the model as it is.
