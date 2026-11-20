# Allocation: a proved core, checked against an independent reference

**Pattern:** pricing, fee, and discount calculation (catalog F3).
**Teaches:** a small Dafny proof, compiled to Python, and a differential test against a hand-written Python function that never consulted the Dafny source. `skills/fv-hypothesis/examples/allocation/` is the same pattern on plain Python, with no proof underneath.

## The system

`Allocate.Split(total, n)` splits `total` cents evenly across `n` recipients. Every recipient gets `total / n`, and the `total % n` leftover cents go one each to the first recipients, so the parts always sum to exactly `total`.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The parts sum to the total | safety, proved | `ensures Sum(parts) == total` in `Allocate.dfy` |
| Every part is within one cent of the even share | safety, proved | `ensures forall i :: ... parts[i] == total/n \|\| parts[i] == total/n + 1` |
| The compiled core agrees with an independent Python implementation | oracle equivalence, tested | `test_dafny_matches_reference` in `test_differential.py` |

The first two are proved once, for every `total` and `n`, by `dafny verify`. The third is a search over 300 generated inputs, because `reference.py` is not proved; it is the thing the proof is checked against.

## Run

```bash
fv-dafny Allocate.dfy
dafny build --solver-path=<z3> --allow-warnings --target:py Allocate.dfy   # regenerates Allocate-py/
python -m pytest -q test_differential.py
fv-mutate Allocate.mutations
```

```text
PASS Allocate.dcfg: verified
```

```text
.                                                                        [100%]
1 passed in 0.15s
```

## A counterexample, as the user reads it

`Allocate.mutations` plants a bug in `reference.py`, not in the proved core, to confirm the differential test would catch the same disagreement either way:

```text
DETECTED the leftover cents go to one index too many: FAILED test_differential.py::test_dafny_matches_reference - assert [0] == [1]
```

1. `total = 0`, `n = 1`. The proved core gives one recipient `0` cents.
2. The mutated reference moves the `<` to `<=`, so it hands out a leftover cent even when there is none to hand out (`leftover = 0`, and `i <= 0` is true at `i = 0`).
3. The two disagree on the one case that exists: `[0]` from the core, `[1]` from the reference.

## Bounds and limits

`dafny verify` proves the two `ensures` clauses for every `total >= 0` and `n > 0`, not only the ones a test would generate. The third property, oracle equivalence, is still a search over 300 generated `(total, n)` pairs with `total` up to 10,000 and `n` up to 20; it is evidence, not a proof, that `reference.py` matches the proved core.
