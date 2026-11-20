# A serializable list-append history

**Pattern:** transactions at a given isolation level (catalog D).
**Teaches:** the smallest complete `list-append` history: a header that declares the model and the outcome, a mutations file, and a run that actually calls `elle-cli`.

## The system

Two shopping carts, keyed 1 and 2. Process 0 appends item 10 to cart 1 and reads cart 2. Process 1 appends item 20 to cart 2 and reads cart 1, after process 0's transaction has already committed. Process 0 then rereads both carts.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The history is strict-serializable | consistency model | the header's `expect: valid`, checked with `consistency-models: strict-serializable` |

## Run

```bash
fv-elle History.edn
fv-mutate History.mutations
```

```text
PASS History.edn: valid
```

## A counterexample, as the user reads it

`History.mutations` plants a bug that makes process 1's own read lie about what it saw:

```text
FAIL History.edn: expected valid, got invalid G2-item
```

1. Process 0 appends item 10 to cart 1.
2. Process 0 reads cart 2 as empty, which puts process 0 before process 1 (process 1 is the one that appends to cart 2).
3. Process 1 appends item 20 to cart 2.
4. Process 1's read of cart 1 now also claims it is empty, which puts process 1 before process 0 (process 0 is the one that appended to cart 1): a cycle with step 2.

## Bounds and limits

The history has two carts and three transactions. `elle-cli` checks it in polynomial time in the size of the history; it says nothing about carts or transactions this history does not contain.
