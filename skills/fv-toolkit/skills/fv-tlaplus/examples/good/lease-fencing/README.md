# Lease fencing

**Pattern:** leases with fencing tokens (catalog B3).
**Teaches:** a ground-truth property kept separate from the mechanism under test, a high-water mark set at grant time rather than at write time.

## The system

Holder h1 has a lease carrying token 1. The lease times out without a
renewal, which is the same shape as a GC pause: h1 takes no steps for an
unbounded period and comes back believing it still holds token 1. The lease
service grants the lease to h2 with a higher token. h1 can still try to
write using its old token after that.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Storage rejects a write whose token is below the token the lease is on now | safety | `StaleWriteRejected` |
| The lease is eventually granted to a new holder | liveness | `EventuallyGranted`, under weak fairness on the lease service and h1 |
| The lease really does move to a second holder | reachability | `WitnessGranted.cfg` must violate `NeverGranted` |

## Configs

| Config | Design | Declared outcome |
|---|---|---|
| `Fencing.cfg` | storage keeps the highest granted token and checks it | holds |
| `NoFencing.cfg` | storage accepts a write whatever token it carries | violated `StaleWriteRejected` |
| `WitnessGranted.cfg` | storage keeps the highest granted token and checks it | violated `NeverGranted` |

`StaleWriteRejected` compares a write against the lease's current token,
not against whatever the storage happens to have recorded. That keeps the
check honest: a design that never updates its own record would otherwise
look safe by never having anything to compare against.

## Run

```bash
fv-tlc --trace LeaseFencing.tla
fv-mutate LeaseFencing.mutations
```

## The counterexample, as the user reads it

```text
1. h1 holds the lease on token 1.                        lease.py:12
2. h1 stops renewing. The lease expires.                  lease.py:19
3. The lease service grants the lease to h2 with token 2. Storage never
   hears about this token, because this design does not fence.
   lease.py:27
4. h1 resumes and writes with token 1. Storage has nothing to check it
   against and accepts it, even though token 2 is now the only valid one.
```

## Bounds and limits

The model has one lease, one expiry and one stale write attempt from h1. It
does not model a renewal that arrives just before expiry, or a third holder.
