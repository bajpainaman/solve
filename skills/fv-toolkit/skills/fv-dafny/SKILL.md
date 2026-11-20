---
name: fv-dafny
description: "Proves a small calculation core correct for every input, in Dafny, and links it to real code by compiling it to Python, Java, Go or JS and comparing it with a hand-written reference on generated inputs. Covers ensures clauses, lemmas, a check file that declares the outcome, and spotting an assume or a contradictory precondition that makes a proof pass for the wrong reason. Use when the question is whether a calculation is correct for every input and the stakes justify a proof, for .dfy files or Dafny output, or when the formal-verification skill routes here. Not for concurrency or distributed behavior (use fv-tlaplus) or when a property-based test is cheap enough (use fv-hypothesis)."
---

# Dafny

`dafny verify` proves that every method meets its `ensures` clauses, for every input its `requires` clause allows, not only the ones a test would generate. It compiles a proved method to a real language so the proof can be checked against, or wired into, real code.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger that this skill encodes.

## Five rules

1. **An `assume` with no `{:axiom}` lets Z3 prove anything afterward.** Dafny warns about it; a check that only reads the exit code or the error count misses the warning. See `examples/bad/unsound-proof/`.
2. **A contradictory precondition makes every `ensures` clause vacuously true**, with no warning at all. Nothing here catches this mechanically; review every precondition against what the caller actually passes.
3. **A proof that only passes after raising the time limit, or the fuel, is not more correct than before**, only slower to disprove if it is wrong. Look for the missing lemma before accepting the bigger limit. See `examples/bad/masked-timeout/`.
4. **Compile the proved core to the differential test's language, and write the reference by hand, never by copying or simplifying the Dafny source.** A reference derived from the proof cannot disagree with it.
5. **A check that has never failed on a planted bug proves nothing.** Plant the bug in the hand-written reference, and confirm the differential test catches the disagreement it would also catch in the proved core.

## Files to write

| File | Holds |
|---|---|
| `<Name>.dfy` | The module: functions, methods and lemmas. The header comment carries `Source read at:` and `Covers:` |
| `<Name>.dcfg` | One per declared outcome, with the `\* expect:` header and an optional `TIME-LIMIT` |
| `<Name>-py/` | The compiled output of `dafny build --target:py`, checked in and regenerated after every change to the `.dfy` file |
| `reference.py`, `test_differential.py` | The independent reference and the oracle-equivalence test |
| `<Name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the run commands, the bounds and the limits |

Copy `examples/good/allocation/` to start.

## Workflow

1. **Write the method header: `requires`, `ensures`, and nothing else.** Run it before writing the body.

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-dafny <Name>.dfy
   ```

2. **Write the body, and add a lemma for every step Z3 cannot see on its own**, such as how a `Sum` changes under a sequence update.
3. **Write the `.dcfg` files**, one per outcome you must demonstrate.
4. **Compile for the differential link.**

   ```bash
   dafny build --solver-path=<z3> --allow-warnings --target:py <Name>.dfy
   ```

5. **Write the independent reference and the differential test**, following `examples/good/allocation/test_differential.py`.
6. **Plant bugs in the reference.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <Name>.mutations
   ```

## Reading the output

| Line | Meaning |
|---|---|
| `PASS X.dcfg: verified` | Every method verified, with no error, timeout, or un-annotated `assume` |
| `FAIL X.dcfg: expected verified, got failed` | A candidate bug, or a proof step Z3 needs a lemma for |
| `FAIL X.dcfg: expected verified, got unsound` | An `assume` with no `{:axiom}` is doing the proving |
| `PASS X.dcfg: failed` | The declared outcome was `failed`, and the proof did not go through |
| `ERROR X.dcfg: ...` | `dafny` could not check the file. This is never a violation |
| `UNAVAILABLE dafny: ...` | `dotnet`, the Dafny tool, or the Z3 solver is missing |

## Telling a counterexample

A differential test failure names the two disagreeing values directly:

```text
DETECTED the leftover cents go to one index too many: FAILED test_differential.py::test_dafny_matches_reference - assert [0] == [1]
```

1. `total = 0`, `n = 1`. The proved core gives one recipient `0` cents.
2. The planted bug in the reference hands out a leftover cent that does not exist.
3. The two disagree on the one case that exists.

## Examples

`examples/INDEX.md` lists every example with its pattern and its lesson.

- `examples/good/allocation/` is the complete pattern: a proof, a compiled core, and a differential test with a mutations file.
- `examples/bad/` holds proofs that verify while they prove nothing, each with the real output and the fix.

## References

| File | Read when |
|---|---|
| `references/notes.md` | You install, invoke, or read the output of `dafny` or `z3` |
| `references/anti-patterns.md` | You review a proof, yours or someone else's |
