# Primary-backup replication: a seed sweep over crash, loss and duplication

**Pattern:** primary-backup / async replication (catalog B3).
**Teaches:** one seeded scheduler that owns task order, message delay, loss, duplication, crash and restart; a chosen design checked beside its rejected design; exact replay from a seed.

## The system

A primary and a backup node replicate writes. Two policies decide when the client is told a write succeeded. `commit-after-replicate` is the chosen design: the client is acked only once the backup has applied the entry. `ack-then-replicate` is the rejected design: the client is acked as soon as the primary appends locally. The primary can crash and restart, losing only its volatile state; its log is durable. Replicate messages can be delayed, lost or duplicated. At the end of a run the primary crashes permanently and the backup is promoted.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Every write the client was told succeeded survives a failover to the backup | safety | `NeverAckedWriteLost` |

## Commands

| Command | Design | Expectation |
|---|---|---|
| `simulate.py --policy commit-after-replicate --sweep 500` | ack waits for the backup | holds for every seed |
| `simulate.py --policy ack-then-replicate --sweep 500` | ack is immediate (rejected) | violated |

The second command is the rejected design's check, and it is also the witness that `NeverAckedWriteLost` can be violated at all: it fails at the first seed on this build.

## Run

```bash
python3 simulate.py --policy commit-after-replicate --sweep 500
python3 simulate.py --policy ack-then-replicate --sweep 500
fv-mutate simulate.mutations
```

```text
PASS sweep NeverAckedWriteLost: holds for 500 seeds
```

```text
FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed 0
  tick 11: primary appends (0, 'v0') and acks it immediately
  ...
  tick 23: replicate(0, 'v0') arrives at a dead backup and is dropped
  ...
  tick 40: primary crashes permanently; the backup is promoted
  tick 40: acked indices [0, 1, 2, 3, 5] are missing from the backup's log
```

```text
DETECTED the chosen policy acks before the backup applies the write: FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed 0
DETECTED a backup restart wipes its durable log instead of keeping it: FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed 1
GREEN a trace message is reworded
SUMMARY detected=2 missed=0 error=0 green=1 brittle=0 uncovered=0
```

## The counterexample, replayed from its seed

`python3 simulate.py --policy ack-then-replicate --replay 0` prints the same trace on every run, because the scheduler draws from one `random.Random(seed)` and nothing else varies.

1. At tick 11, the primary appends write 0 and tells the client it succeeded, without waiting for the backup.
2. The backup crashes before the replicate message for write 0 arrives. The message reaches the backup only at tick 23, while it is still dead, and is dropped.
3. At tick 40, the primary crashes permanently and the backup is promoted.
4. The backup's log has no entry for write 0, even though the client was already told it succeeded.

## Bounds and limits

Each run covers 40 ticks of one primary and one backup. A seed sweep of 500 seeds is a search, not a proof: it can show that the chosen design holds for every seed it tried, and it can find a seed where the rejected design fails, but it says nothing about a seed outside the sweep. The model has no second backup, no network partition separate from a node crash, and no retry of a message dropped at a dead node.
