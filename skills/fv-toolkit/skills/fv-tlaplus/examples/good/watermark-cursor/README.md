# Watermark cursor

**Pattern:** incremental load by watermark cursor (catalog C1).
**Teaches:** a dedup set bundled with the comparison operator as one design, a slow commit bounded to the model's own run window.

## The system

Two runs load rows by commit time against a cursor. Row r1 commits at 1,
row r2 commits at 2, and row rl also commits at 2, but its transaction is
slow: it can become visible at any point up to and including the second
run, including after the first run has already moved the cursor past 2.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| A row that is visible by the end of the second run was loaded exactly once | safety | `ExactlyOnce` |
| Both runs eventually happen | liveness | `EventuallyBothRan`, under weak fairness on the loader and the slow commit |
| rl's late commit really can land after the first run | reachability | `WitnessSlowCommit.cfg` must violate `NeverCommitsLate` |

## Configs

| Config | Design | Slow commit | Declared outcome |
|---|---|---|---|
| `GteWithDedup.cfg` | `>=`, with a dedup set | on | holds |
| `GtNoDedup.cfg` | `>`, no dedup | on | violated `ExactlyOnce` |
| `GteNoDedup.cfg` | `>=`, no dedup | on | violated `ExactlyOnce` |
| `NoSlowCommit.cfg` | `>`, no dedup | off | holds |
| `WitnessSlowCommit.cfg` | `>=`, with a dedup set | on | violated `NeverCommitsLate` |

`GtNoDedup.cfg` and `GteNoDedup.cfg` fail the same property for opposite
reasons. `>` never re-examines the cursor's own value, so rl's late commit
at exactly that value is never matched by either run. `>=` does
re-examine it and catches rl, but with no dedup set it also recounts r2,
which the first run already loaded at the same value. `NoSlowCommit.cfg`
uses the same rejected design as `GtNoDedup.cfg`: with the fault off, rl
is visible from the start, so the first run catches it before the cursor
ever moves past it.

## Run

```bash
fv-tlc --trace WatermarkCursor.tla
fv-mutate WatermarkCursor.mutations
```

## The counterexample, as the user reads it

```text
1. r1 and r2 are visible. rl's transaction has started but not committed.
   incremental_load.py:11
2. The first run loads r1 and r2 with commit_time > 0, and moves the
   cursor to 2.                                           incremental_load.py:19
3. rl's transaction commits. It carries commit_time = 2, the cursor's own
   value.                                                  incremental_load.py:27
4. The second run queries commit_time > 2. rl is never matched, by this
   run or by any other, because the cursor has already passed it.
```

## Bounds and limits

The model has three rows and two runs. A row that commits after the
second run is out of scope: a third run would be needed to say anything
about it. The model does not represent clock skew between the writer and
the loader.
