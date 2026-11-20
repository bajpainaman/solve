# A true invariant that is not inductive

**Pattern:** mutex / lock (catalog A4).
**Teaches:** TLC confirming an invariant proves it only for the states TLC actually reached. It does not prove the invariant is inductive, and a non-inductive invariant breaks the moment something reuses it as a starting point.

## The system

The same lease slot as `../../good/lease-induction/`. `WeakInv == leases \in {0, 1} /\ phase \in {"idle", "held"}` is the invariant someone writes first, because it is the most direct restatement of "the count never goes above 1".

## The real output

TLC explores every state reachable from `Init` and finds no violation:

```text
PASS Bounded.cfg: holds (2 distinct states)
```

Apalache's inductive step starts from any state that satisfies `WeakInv`, not only a reachable one, and finds one in two steps:

```text
FAIL Step.icfg: expected holds, got violated WeakInv
  1: <Initial predicate>
  /\ leases = 1
  /\ phase = "idle"

  2: <Next>
  /\ leases = 2
  /\ phase = "held"
```

## Why the artifact is wrong

`WeakInv` says nothing about `phase`, so a state with `leases = 1` and `phase = "idle"` satisfies it. That state is never reached from the real `Init` (`Acquire` always sets `phase` to `"held"`), so TLC's search, which only visits reachable states, never finds it. Apalache's inductive step is not limited to reachable states: `INIT WeakInv` asks the solver for any state satisfying `WeakInv`, and it is free to pick the unreachable one. From there, `Acquire`'s guard (`phase = "idle"`) is satisfied, and `leases` reaches 2.

## The fix

Strengthen the invariant so it names every variable the guard depends on: `StrongInv == (phase = "idle" /\ leases = 0) \/ (phase = "held" /\ leases = 1)`, in `../../good/lease-induction/`. `StrongInv` fixes `phase` to the one value that is consistent with each value of `leases`, so an arbitrary `StrongInv`-satisfying state is always one `Acquire` or `Release` can act on safely.

## The check that catches the error

`fv-apalache` with `INIT` set to the invariant's own name, as in `Step.icfg`. A TLC run against `Init`, bounded or not, cannot catch this, because it only ever starts from states the real system can reach.

## Run

```bash
fv-tlc Lease.tla Bounded.cfg
fv-apalache --trace Lease.tla Step.icfg
```
