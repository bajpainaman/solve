# A write skew, reported as G2-item

**Pattern:** transactions at a given isolation level (catalog D).
**Teaches:** a history with a genuine anomaly, declared and detected, instead of only a clean one. `elle-cli` names this anomaly `G2-item` even when `-a write-skew` is requested; the report always uses the checker's own name.

## The system

Two shopping carts, keyed 1 and 2, start empty. Process 0 appends item 10 to cart 1 and reads cart 2 as empty. Process 1 appends item 20 to cart 2 and reads cart 1 as empty, concurrently.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The history is strict-serializable | consistency model | the header's `expect: invalid G2-item` |

Declaring `invalid G2-item` here plays the role a witness config plays for TLA+: it is the check that must find the counterexample, so the example also proves the anomaly is reachable, not merely theoretical.

## Run

```bash
fv-elle History.edn
fv-mutate History.mutations
```

```text
PASS History.edn: invalid G2-item
```

## A counterexample, as the user reads it

1. Process 0 appends item 10 to cart 1.
2. Process 0 reads cart 2 as empty, which puts process 0 before process 1.
3. Process 1 appends item 20 to cart 2.
4. Process 1 reads cart 1 as empty, which puts process 1 before process 0: a cycle with step 2.

Each process observed the other's cart before that cart's append, so no order of the two transactions is consistent with both reads.

## Bounds and limits

The history has two carts and two transactions, the smallest write skew `list-append` can show. A real cart service's history would need many more transactions before a cycle this short becomes likely to occur by itself; this example plants it directly instead of generating load and hoping for one.
