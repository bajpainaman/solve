# Transactional outbox

**Pattern:** transactional outbox (catalog B1).
**Teaches:** three designs behind one knob, a resume point computed from durable state, a relay that retries from a durable flag and can deliver twice, a consumer dedup knob.

## The system

A handler makes one business change and must get one event to a consumer. The
process can crash at any step and resumes from whatever it wrote durably. A
relay reads an outbox row that is not yet marked published and sends it to
the broker, then marks it. The relay does not remember a publish it made
before a crash, so after a crash it reads the still-unmarked row again and
sends it again.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| An event never reaches the broker for a change that never committed | safety | `NoEventWithoutCommit` |
| The consumer applies the business effect at most once | safety | `AtMostOnceApplied` |
| A committed change is eventually delivered to the consumer | liveness | `EventuallyApplied`, under weak fairness on the process and the consumer, none on crashes |
| The relay can deliver the same row twice | reachability | `WitnessDuplicateDelivery.cfg` must violate `NeverDuplicateDelivery` |

## Configs

| Config | Design | Dedup | Crashes | Declared outcome |
|---|---|---|---|---|
| `OneTransaction.cfg` | both writes in one transaction | on | up to 2 | holds |
| `SeparateWrites.cfg` | business commit, then a later outbox write | on | 1 | deadlock |
| `SeparateWritesNoCrash.cfg` | business commit, then a later outbox write | on | 0 | holds |
| `DirectPublish.cfg` | publish to the broker, then commit | on | 0 | violated `NoEventWithoutCommit` |
| `NoDedup.cfg` | one transaction | off | up to 2 | violated `AtMostOnceApplied` |
| `WitnessDuplicateDelivery.cfg` | one transaction | on | up to 2 | violated `NeverDuplicateDelivery` |

`SeparateWrites.cfg` and `SeparateWritesNoCrash.cfg` differ only in the crash
bound. The design deadlocks only with the fault on, so the fault is what
causes it: a crash between the two writes leaves the change committed with
no event, and nothing in the model ever triggers the missing write again.

## Run

```bash
fv-tlc --trace TransactionalOutbox.tla
fv-mutate TransactionalOutbox.mutations
```

## The counterexample, as the user reads it

```text
1. Nothing has happened: the change is uncommitted, and the outbox is empty.
2. The handler commits the business row.                outbox.py:33
3. The process crashes before it writes the outbox row.  outbox.py:41
4. On restart, nothing calls write_outbox_row() again, because the only
   thing that remembers to call it was the crashed process's own stack.
   The change stays committed with no event, forever.
```

## Bounds and limits

The model has one business change, one relay and one consumer, with at most
two crashes. It does not model a second change, a second relay instance, or
the outbox table's own storage faults.
