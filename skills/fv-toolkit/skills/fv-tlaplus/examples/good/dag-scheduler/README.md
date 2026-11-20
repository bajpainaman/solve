# DAG scheduler

**Pattern:** DAG orchestration, restart and dependency checking (catalog C1).
**Teaches:** a worker action that keeps running regardless of the scheduler's own crash flag, a restart that reads a durable effect count instead of guessing, two unrelated checks bundled into one rejected design.

## The system

Task B depends on task A. The scheduler can crash after it marks A
running but before it marks A done, so on restart it does not know
whether A's own side effect already happened.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| A's side effect never runs more than once | safety | `NeverRunsTwice` |
| B never runs while A is only partly done | safety | `NeverRunsOnPartialUpstream` |
| Both tasks eventually finish | liveness | `EventuallyBothDone`, under weak fairness on the scheduler and the worker, none on the crash |
| Both tasks really do finish | reachability | `WitnessBothDone.cfg` must violate `NeverBothDone` |

## Configs

| Config | Design | Crashes | Declared outcome |
|---|---|---|---|
| `Checked.cfg` | a restart checks the effect count; B waits for A to be done | 1 | holds |
| `NaiveRestart.cfg` | a restart always resumes A as running; B waits for A to start | 1 | violated `NeverRunsTwice` |
| `NaivePartialUpstream.cfg` | a restart always resumes A as running; B waits for A to start | 1 | violated `NeverRunsOnPartialUpstream` |
| `NaiveNoCrash.cfg` | a restart always resumes A as running; B waits for A to start | 0 | holds |
| `WitnessBothDone.cfg` | a restart checks the effect count; B waits for A to be done | 1 | violated `NeverBothDone` |

The naive design bundles two separate mistakes: a restart that guesses
instead of checking, and a dependency check that accepts "started" for
"done". `NaiveRestart.cfg` and `NaivePartialUpstream.cfg` each expose one
of the two without needing the other: the partial-upstream bug needs no
crash at all, and the double-run bug needs no help from the weak
dependency check. `NaiveNoCrash.cfg` shows the restart mistake alone does
no harm without a crash to trigger it.

## Run

```bash
fv-tlc --trace DagScheduler.tla
fv-mutate DagScheduler.mutations
```

## The counterexample, as the user reads it

```text
1. The scheduler marks A running and dispatches the worker.
   scheduler.py:14
2. The worker runs A's side effect once.                 scheduler.py:22
3. The scheduler crashes before it marks A done.          scheduler.py:27
4. The scheduler restarts. It sees A was running and, without checking
   whether the work already happened, dispatches the worker again.
   scheduler.py:33
5. The worker runs A's side effect a second time.
```

## Bounds and limits

The model has two tasks and one crash. It does not model a third task, a
worker that itself crashes mid-execution, or a scheduler that crashes more
than once.
