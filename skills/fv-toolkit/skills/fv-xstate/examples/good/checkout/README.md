# Checkout wizard: generated paths against the real implementation

**Pattern:** forms and multi-step wizards (catalog F2).
**Teaches:** `getShortestPaths` to cover every reachable (state, context), a path replayed against the real code as a conformance check, a rejected design checked beside the chosen one.

## The system

A three-step checkout: `cart`, `shipping`, `payment`, `confirmed`. `shipping`'s `NEXT` only leaves once an address is set; `payment`'s `NEXT` only leaves once a payment method is set. `checkout.machine.cjs` declares two versions of this machine: the chosen design (`checkoutMachine`, `NEXT` guarded) and the rejected design (`checkoutMachineUnguarded`, `NEXT` unguarded). `checkout.cjs` is the real implementation, a plain class with no XState at runtime, and it is always guarded.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The real implementation follows every step of every generated path exactly, in state and in context | safety | `ConformsToMachine` |

## Commands

| Command | Design | Expectation |
|---|---|---|
| `run-paths.cjs --machine guarded` | `NEXT` requires the field it depends on | every path conforms |
| `run-paths.cjs --machine unguarded` | `NEXT` leaves `shipping` unconditionally (rejected) | some path does not conform |

The second command is the rejected design's check, and it is the witness that skipping validation is a state a model can describe: the real implementation refuses to follow the unguarded machine's shortcut, so the comparison fails.

## Run

```bash
node run-paths.cjs --machine guarded
node run-paths.cjs --machine unguarded
fv-mutate run-paths.mutations
```

```text
PASS path ConformsToMachine: xstate.init -> cart
PASS path ConformsToMachine: xstate.init -> NEXT -> shipping
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> shipping
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> payment
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> BACK -> cart
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT -> payment
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT -> NEXT -> confirmed
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT -> BACK -> shipping
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT -> BACK -> BACK -> cart
```

```text
FAIL path ConformsToMachine: expected payment, got shipping on xstate.init -> NEXT -> NEXT
```

```text
DETECTED setting the payment flag is dropped: FAIL path ConformsToMachine: expected {"hasAddress":true,"hasPayment":true}, got {"hasAddress":true,"hasPayment":false} on xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT
DETECTED back from payment returns to the wrong step: FAIL path ConformsToMachine: expected shipping, got cart on xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT -> BACK
GREEN the header comment is reworded
SUMMARY detected=2 missed=0 error=0 green=1 brittle=0 uncovered=0
```

## The counterexample, as the generator found it

```text
1. The unguarded machine lets `NEXT` leave "shipping" with no address set, reaching "payment" in two events: xstate.init -> NEXT -> NEXT.
2. The real Checkout class, replayed on that same event sequence, refuses the second NEXT because hasAddress is still false.
3. It stays in "shipping" where the unguarded machine says "payment", so the check reports the divergence.
```

## Bounds and limits

`getShortestPaths` returns one path per distinct (state, context) pair it can reach by exploring the machine's own transitions, so a check built on it only ever replays events the model itself would take. It cannot generate a path that violates the model's own guards; the rejected-design machine exists so that an illegal path has somewhere to come from. The machine has no network calls and no asynchronous steps; every event is applied and answered inside the same tick.
