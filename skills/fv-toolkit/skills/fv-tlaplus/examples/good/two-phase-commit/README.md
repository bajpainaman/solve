# Two-phase commit

**Pattern:** two-phase commit (catalog B3).
**Teaches:** the coordinator's own durable vote record against a manager's current state, a true deadlock as the declared outcome, a boolean fault switch separate from the count it gates.

## The system

A coordinator runs two-phase commit over a fixed set of resource managers.
Each manager prepares once. The coordinator records every prepare vote it
receives and never revises that record, even if a manager later changes its
own mind. The coordinator can crash after votes start coming in but before
it decides.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No manager commits while another aborts | safety | `AllOrNothing` |
| Every manager eventually reaches a decision | liveness | `EventuallyDecided`, under weak fairness on the managers and the coordinator, none on the crash |
| Every manager committing is reachable | reachability | `WitnessAllCommitted.cfg` must violate `NeverAllCommitted` |

## Configs

| Config | Design | Recovers | Declared outcome |
|---|---|---|---|
| `BlockOnCrash.cfg` | a prepared manager waits for the coordinator | yes | holds |
| `BlockOnCrashNoRecovery.cfg` | a prepared manager waits for the coordinator | no | deadlock |
| `TimeoutAbort.cfg` | a prepared manager aborts on its own after a wait | yes | violated `AllOrNothing` |
| `WitnessAllCommitted.cfg` | a prepared manager waits for the coordinator | yes | violated `NeverAllCommitted` |

`BlockOnCrashNoRecovery.cfg` is not a bug in the blocking design. It is the
blocking that gives two-phase commit its name: a coordinator that crashes
before it decides and never comes back leaves every prepared manager with no
move, which TLC reports as a real deadlock.

## Run

```bash
fv-tlc --trace TwoPhaseCommit.tla
fv-mutate TwoPhaseCommit.mutations
```

## The counterexample, as the user reads it

```text
1. Both managers prepare. The coordinator has recorded both votes.
   coordinator.py:18
2. The coordinator crashes before it decides.            coordinator.py:24
3. Manager r1 has been waiting long enough and aborts on its own.
   coordinator.py:41
4. The coordinator recovers. Its own record still shows both managers
   voted to prepare, so it commits.                       coordinator.py:28
5. Manager r2 learns the commit. Manager r1 already aborted, and the
   coordinator has no way to tell it otherwise now.
```

## Bounds and limits

The model has two resource managers and at most one coordinator crash. It
does not model a manager that votes to abort its own prepare, or a manager
that itself crashes.
