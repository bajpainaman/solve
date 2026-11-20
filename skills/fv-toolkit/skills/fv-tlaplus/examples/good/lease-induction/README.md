# Lease induction

**Pattern:** mutex / lock (catalog A4).
**Teaches:** checking an inductive invariant in three steps with Apalache, instead of exploring a bounded model with TLC.

## The system

A single lease slot. One client holds it at a time. `Acquire` only runs while the slot is free, and sets `phase` to `"held"`. `Release` only runs while it is held, and frees it.

## Why Apalache, not TLC

TLC explores every state *reachable from `Init`*. Apalache's `check` command can instead start from any state that satisfies a named operator, reachable or not. Setting `INIT` to an invariant's own name turns a check into an inductive step: if Apalache finds no violation, the invariant holds no matter how it was reached, which is a stronger guarantee than a bounded, explicit search gives. `../../bad/non-inductive-invariant/` shows the gap between the two: an invariant that TLC confirms on every reachable state, but that is not inductive on its own.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The slot's count and its phase agree | inductive invariant | `StrongInv` |
| At most one lease is outstanding | safety | `Safety`, implied by `StrongInv` |

## The three steps

| Check | Verification condition | Declared outcome |
|---|---|---|
| `Init.icfg` | `Init => StrongInv` | holds |
| `Step.icfg` | `StrongInv /\ Next => StrongInv'` | holds |
| `Safety.icfg` | `StrongInv => Safety` | holds |

All three together prove `Safety` for every reachable state, for any number of `Acquire`/`Release` steps, not only the ones TLC's bounded search visits.

## Run

```bash
fv-apalache --trace Lease.tla
fv-mutate Lease.mutations
```

```text
PASS Init.icfg: holds
PASS Safety.icfg: holds
PASS Step.icfg: holds
```

## A counterexample, as the user reads it

`Lease.mutations` plants a bug that drops the `Acquire` guard, so `Acquire` can run even while the slot is already held:

```text
FAIL Step.icfg: expected holds, got violated StrongInv
  1: <Initial predicate>
  /\ leases = 1
  /\ phase = "held"

  2: <Next>
  /\ leases = 2
  /\ phase = "held"
```

1. The slot already holds one lease.
2. `Acquire` runs anyway, because its guard no longer checks `phase`.
3. `leases` reaches 2. Two clients now believe they hold the same slot.

## Bounds and limits

The model has one slot and two actions. `Safety` follows from `StrongInv` for any number of steps, because the proof is inductive, not because TLC explored every one of them. The model describes a design, so a regression test on the real lease code is still needed.
