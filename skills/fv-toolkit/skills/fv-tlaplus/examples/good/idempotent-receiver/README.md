# Idempotent receiver

**Pattern:** idempotent receiver, or inbox (catalog B1).
**Teaches:** a fault switch, a crash that loses volatile state, three designs behind one knob, liveness with a bounded fault.

## The system

A broker delivers a message at least once. The consumer applies a business effect and records the message id, so that a redelivery is skipped. The effect and the dedup record are two writes, and the consumer can crash between them.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The effect is applied at most once, despite redelivery | safety | `AtMostOnce` |
| A message that left the queue had its effect applied | safety | `AckedImpliesApplied` |
| The message is eventually acked | liveness | `EventuallyAcked`, under weak fairness on the consumer's work and none on crashes |
| A run that crashes can still ack | reachability | `WitnessAckAfterCrash.cfg` must violate `NeverAckedAfterCrash` |

## Configs

| Config | Design | Crashes | Declared outcome |
|---|---|---|---|
| `EffectThenRecordNoCrash.cfg` | effect, then dedup record | 0 | holds |
| `EffectThenRecord.cfg` | effect, then dedup record | up to 2 | violated `AtMostOnce` |
| `RecordThenEffect.cfg` | dedup record, then effect | up to 2 | violated `AckedImpliesApplied` |
| `OneTransaction.cfg` | both writes in one transaction | up to 2 | holds |
| `WitnessAckAfterCrash.cfg` | both writes in one transaction | up to 2 | violated `NeverAckedAfterCrash` |

The first two rows differ only in the fault switch. The design holds without a crash and breaks with one, so the crash is the cause.

## Run

```bash
fv-tlc --trace IdempotentReceiver.tla
fv-mutate IdempotentReceiver.mutations
```

## Bounds and limits

The model has one message, one consumer and at most two crashes. It does not model two consumers that compete for the message, and it treats the transaction as one step without modelling the database.
