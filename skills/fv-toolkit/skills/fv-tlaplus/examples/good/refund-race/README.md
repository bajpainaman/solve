# Refund race

**Pattern:** read-modify-write without a lock (catalog D), idempotency on retries (catalog F1).
**Teaches:** one action per atomic step, a design knob as a constant, one config per design, a witness, a mutations file.

## The system

A customer paid 10. Refund code reads how much is still refundable and then refunds that amount. Two jobs run at once, because an agent clicks refund while a webhook delivers the same refund. Each job reads before the other has written. Both read 10 and both refund 10.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| A customer is never refunded more than they paid | safety | `NeverOverRefund` |
| Every refund job finishes | liveness | `EventuallyDone`, under weak fairness on each job |
| The full refund can happen | reachability | `WitnessFullRefund.cfg` must violate `NeverFullyRefunded` |

## Configs

| Config | Design | Declared outcome |
|---|---|---|
| `CheckThenRefund.cfg` | Read, then refund in a later step | violated `NeverOverRefund` |
| `AtomicRefund.cfg` | Check and refund in one step | holds |
| `WitnessFullRefund.cfg` | The atomic design | violated `NeverFullyRefunded` |

The configs are named for their mechanism. No config is named for a verdict.

## Run

```bash
fv-tlc --trace RefundRace.tla
fv-mutate RefundRace.mutations
```

## The counterexample, as the user reads it

```text
1. Both jobs are idle and nothing is refunded.
2. Job a reads 10 refundable.
3. Job b reads 10 refundable.
4. Job a refunds 10.
5. Job b refunds 10. The customer has 20 back on a payment of 10.
```

## Bounds and limits

The model checks two jobs and one payment of 10. It has no crash and no partial refund. It describes a design, so a regression test on the real refund code is still needed.
