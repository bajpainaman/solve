# CDC snapshot handoff

**Pattern:** change data capture, snapshot-to-stream handoff (catalog C3).
**Teaches:** a fenced choice of candidate values standing in for a timing race, an invariant gated on completion so it says nothing about a run still in progress.

## The system

A source table takes three changes, c1 through c3, in order. A connector
takes a snapshot that always reflects c1, then streams the rest of the log
starting at the position it noted at snapshot time. A restart mid-stream
redetermines that position the same way, so the same race applies there
too.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Once the stream finishes, every change has landed downstream exactly once | safety | `ExactlyOnce` |
| Downstream eventually equals the source | liveness | `EventuallyCaughtUp`, under weak fairness on the connector |
| The handoff really does finish | reachability | `WitnessCaughtUp.cfg` must violate `NeverFinishes` |

## Configs

| Config | Design | Race window | Declared outcome |
|---|---|---|---|
| `CorrectOffset.cfg` | the position is noted in the same step as the snapshot | on | holds |
| `WrongOffset.cfg` | the position is noted by a separate read | on | violated `ExactlyOnce` |
| `WrongOffsetNoRace.cfg` | the position is noted by a separate read | off | holds |
| `WitnessCaughtUp.cfg` | the position is noted in the same step as the snapshot | on | violated `NeverFinishes` |

`WrongOffset.cfg` and `WrongOffsetNoRace.cfg` differ only in whether the
noted position can actually drift from the true boundary. With the race
switched off, the separate read always happens to land on c2 anyway, so
the design looks safe for the wrong reason: nothing in it stops the drift,
the model's own fault switch just never exercises it.

## Run

```bash
fv-tlc --trace CdcSnapshotHandoff.tla
fv-mutate CdcSnapshotHandoff.mutations
```

## The counterexample, as the user reads it

```text
1. The source table takes c1, then c2, then c3.          connector.py:9
2. The connector snapshots the table, which reflects c1. A separate read
   of the log position lands on 3, one past the true boundary of 2.
   connector.py:21
3. Streaming starts at position 3. c2 is never streamed, because nothing
   else is watching for it once the connector believes it is caught up.
```

## Bounds and limits

The model has one table, three changes and one snapshot. It does not model
a second snapshot, a schema change mid-stream, or a connector that falls
behind the log's retention window.
