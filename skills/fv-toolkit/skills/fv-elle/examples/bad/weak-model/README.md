# Checked against a weaker model than the application assumes

**Pattern:** transactions at a given isolation level (catalog D).
**Teaches:** the `-a` anomaly list, not the `-c` consistency-model label, decides what `elle-cli` looks for. A check that names the right isolation level but the wrong anomaly list still misses the anomaly that level forbids.

## The history

The same two transactions as `../../good/write-skew/History.edn`: process 0 appends to cart 1 and reads cart 2 as empty; process 1 appends to cart 2 and reads cart 1 as empty, concurrently. Neither process observes the other's append, so the two transactions cannot be ordered consistently: a write skew.

## The real output

This file's header declares `anomalies: G0,G1a,G1b,G1c`, the set `read-committed` forbids. Checked against that list, the history passes:

```text
PASS History.edn: valid
```

The cart service's code assumes strict-serializable isolation, under which write skew (`G2-item`) is forbidden. Checked against the anomaly list that level needs, the identical history fails:

```text
PASS History.edn: invalid G2-item
```

(this second line is `../../good/write-skew/History.edn`, the same transactions with the complete anomaly list declared)

## Why the artifact is wrong

`elle-cli`'s `-a` flag is the set of anomalies it searches for. `-c` only labels the result; it does not restrict or widen the search. A header that declares `consistency-models: read-committed` and an anomaly list that only covers read-committed's own anomalies (`G0`, `G1a`, `G1b`, `G1c`) will never find a `G2-item` write skew, because `G2-item` was never in the list to search for. The check passes, but it never looked.

## The fix

Declare the anomaly list the application's actual isolation level needs, as `../../good/write-skew/History.edn` does: `G0,G1a,G1b,G1c,G-single,G-single-process,G-single-realtime,G2-item` for strict-serializable.

## The check that catches the error

None, on this file. `fv-elle` only runs the anomaly list the header declares; it has no way to know the header under-declared it. Catching this means reading the header against the isolation level the calling code actually assumes, which is a review step, not a mechanical one.

## Run

```bash
fv-elle History.edn
fv-elle ../../good/write-skew/History.edn
```
