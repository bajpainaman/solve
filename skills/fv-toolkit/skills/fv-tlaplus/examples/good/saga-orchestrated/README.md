# Saga orchestrated

**Pattern:** saga, orchestrated (catalog B2).
**Teaches:** a timeout fault that lets a step settle before every attempt resolves, a fencing flag that closes that window, a ghost variable that snapshots a decision so a later change can be caught.

## The system

An orchestrator holds inventory at one participant as one step of a larger
saga. The request can be retried once while the orchestrator is still
waiting. On a timeout, the orchestrator must decide whether to compensate
the step. A request that is still in flight at that moment can still land
afterward, because the participant or the network was only slow, not down.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Compensation never runs for a step whose effect never landed | safety | `CompensateImpliesRan` |
| Once the saga settles, nothing it already decided changes underneath it | safety | `SettledEffectIsFinal` |
| Every saga ends committed or aborted | liveness | `EventuallyDone`, under weak fairness on the orchestrator and the participant |
| An abort can skip compensation, because the step never ran | reachability | `WitnessSkipCompensation.cfg` must violate `NeverSkipsCompensation` |

## Configs

| Config | Design | Late apply | Declared outcome |
|---|---|---|---|
| `ConfirmedCompensate.cfg` | confirm the effect, fence, then decide | on | holds |
| `BlindCompensate.cfg` | always compensate on timeout | on | violated `CompensateImpliesRan` |
| `BlindCompensateRace.cfg` | always compensate on timeout | on | violated `SettledEffectIsFinal` |
| `BlindCompensateNoFault.cfg` | always compensate on timeout | off | holds |
| `WitnessSkipCompensation.cfg` | confirm the effect, fence, then decide | on | violated `NeverSkipsCompensation` |

`BlindCompensate.cfg` fails even without the fault, because a request the
network simply dropped also never ran, and the blind design compensates it
anyway. `BlindCompensateRace.cfg` and `BlindCompensateNoFault.cfg` isolate
the other failure: a request still landing after the orchestrator settled.
With the fault off, the orchestrator never settles until every attempt has
already resolved, so `SettledEffectIsFinal` holds.

## Run

```bash
fv-tlc --trace SagaOrchestrated.tla
fv-mutate SagaOrchestrated.mutations
```

## The counterexample, as the user reads it

```text
1. The orchestrator sends the hold-inventory request. Nothing has happened
   at the participant yet.                                saga.py:22
2. The orchestrator times out before any answer, while the request is
   still on the wire.                                      saga.py:31
3. The orchestrator compensates the step, believing it never ran.
   saga.py:35
4. The slow request lands at the participant right after. The inventory
   is now held, and nothing is watching to compensate it a second time.
```

## Bounds and limits

The model has one saga step, one participant and at most one retry. It does
not model a second concurrent saga instance or a participant crash.
