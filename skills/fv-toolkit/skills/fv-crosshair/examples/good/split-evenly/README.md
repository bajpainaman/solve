# Split evenly: a contract beside a diffbehavior comparison

**Pattern:** money and rounding (catalog F3), oracle equivalence between a function and its refactor (catalog A3, C1).
**Teaches:** a contract check paired with `diffbehavior`, and a rejected design that the diff, not the contract, tells apart.

## The system

`split_evenly(total, parts)` splits an amount of cents into `parts` shares that sum back to `total`, with no share more than one cent apart from another and the extra cents going to the first few shares. `split_evenly_refactored` is the same split, written as an explicit loop. `split_evenly_rejected` is a design that gives the extra cents to the last few shares instead.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| `split_evenly` meets its own contract | contract | `check SplitEvenlyHoldsItsContract`, `expect holds` |
| The loop refactor changes nothing a caller can observe | oracle equivalence | `diff RefactorPreservesOutput`, `expect holds` |
| The rejected design can still be told apart | witness | `diff RejectedDesignPutsExtraCentsLast`, `expect differs` |

The third command does not test a bug. `split_evenly_rejected` satisfies the same aggregate contract as `split_evenly` (same length, same sum, same 1-cent bound); only `diffbehavior`, comparing the two functions directly, shows that they place the extra cents differently.

## Run

```bash
fv-crosshair money.crosshair
fv-mutate money.mutations
```

Real output, from the pinned crosshair-tool 0.0.113:

```text
PASS check SplitEvenlyHoldsItsContract: holds
PASS diff RefactorPreservesOutput: holds
PASS diff RejectedDesignPutsExtraCentsLast: differs
```

## Bounds and limits

Each command searches for the default `--per_condition_timeout` (10 seconds here). "Holds" means no counterexample turned up in that time, not that one cannot exist; see `references/anti-patterns.md` for what reading it as a proof leads to.
