# Slowly changing dimension, type 2

**Pattern:** slowly changing dimensions (catalog C4).
**Teaches:** ordering time points with `util/ordering` instead of arithmetic, a merge procedure as a predicate, two properties checked under the chosen design and under no design at all.

## The system

Each key has a history of rows. A row is valid from one instant and, unless it is current, up to another. The question is whether the history can ever show two rows of the same key active at once, or leave a key with no active row.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| At most one row of a key is active at any instant | safety | `NoOverlap_MergeClosesPriorRowAtomically` |
| A key with any history has exactly one current row | safety | `OneCurrentRow_MergeClosesPriorRowAtomically` |
| A key's history actually has more than one row | reachability | `run SomeKeyHasAHistory ... expect 1` |

## Commands

| Command | Design | Expectation |
|---|---|---|
| `run SomeKeyHasAHistory for 5 but 4 Instant` | the merge closes the prior row atomically | SAT: a real history exists |
| `check NoOverlap_MergeClosesPriorRowAtomically for 5 but 4 Instant` | the merge closes the prior row atomically | UNSAT: no counterexample |
| `check OneCurrentRow_MergeClosesPriorRowAtomically for 5 but 4 Instant` | the merge closes the prior row atomically | UNSAT: no counterexample |
| `check NoOverlap_NoRule for 5 but 4 Instant` | no design rule in force | SAT: a counterexample exists |
| `check OneCurrentRow_NoRule for 5 but 4 Instant` | no design rule in force | SAT: a counterexample exists |

`MergeClosesPriorRowAtomically` is the merge procedure this project ships: at most one current row per key, the successor of a closed row is unique, and every closed row has a successor. The last two commands drop that rule. Each must find a counterexample, because nothing then stops two overlapping rows or a key with no current row.

## Run

```bash
fv-alloy --show scd2.als
fv-mutate scd2.mutations
```

## The counterexample, as the user reads it

```text
this/Row<:key={Row$0->Key$0, Row$1->Key$0}
this/Row<:validFrom={Row$0->Instant$3, Row$1->Instant$3}
this/Row<:validTo={}
```

1. Row 0 and Row 1 both belong to the same key.
2. Both rows start at the same instant, Instant 3.
3. Neither row has a `validTo`, so both are current at once.
4. With no merge rule in force, a query for "the current row" of this key finds two rows instead of one.

## Bounds and limits

The checks cover five rows, up to four keys and users (unused here) and four instants. The model has no arithmetic on time, because Alloy's built-in integers run from -8 to 7 and `util/ordering` orders the `Instant` atoms instead. It has no out-of-order backfill, where a row for an earlier instant is inserted after a later one already exists.
