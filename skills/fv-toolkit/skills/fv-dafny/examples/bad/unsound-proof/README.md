# Two ways to "verify" something false

**Pattern:** pricing, fee, and discount calculation (catalog F3).
**Teaches:** `dafny verify` reports "verified" for a method whose `ensures` clause is false for almost every input, when the body short-circuits the proof instead of satisfying it.

## AssumeFalse.dfy

`Refund` claims `y == 2 * x` but sets `y := x`. The body then runs `assume false`, which tells the prover "treat the rest of this path as unreachable." Z3 can derive any conclusion, true or false, from a false assumption, so the `ensures` clause is "proved."

### The real output

```text
PASS AssumeFalse.dcfg: unsound
```

Dafny's own run shows why: an `assume` with no `{:axiom}` annotation prints a warning, even though the method still counts as verified.

```text
AssumeFalse.dfy(8,2): Warning: assume statement has no {:axiom} annotation
  |
8 |   assume false;
  |   ^^^^^^


Dafny program verifier finished with 1 verified, 0 errors
```

### The fix

Delete the `assume`, and either prove the real postcondition or correct it to what the method actually does (`ensures y == x`).

### The check that catches the error

`fv-dafny` reports this check's outcome as `unsound`, not `verified`, because it looks for `Warning: assume statement has no {:axiom} annotation` in Dafny's own output. A check that only reads the exit code, or only reads "N errors", would report this as a clean pass.

## ContradictoryPrecondition.dfy

`Refund` requires `x > 10 && x < 5`, which no integer satisfies. Under an unsatisfiable precondition, every `ensures` clause is vacuously true, so Dafny verifies `y == x + 999999` with no warning at all.

### The real output

```text
PASS ContradictoryPrecondition.dcfg: verified
```

### Why the artifact is wrong

The method can never run; the precondition excludes every input. A caller cannot actually invoke `Refund` under any `x`, so verifying what it does when called is true but empty.

### The fix

Narrow or correct the precondition to the set of inputs the method must actually handle.

### The check that catches the error

None. Say so plainly: Dafny prints no warning for a contradictory precondition, unlike an un-annotated `assume`, so nothing in this plugin catches it mechanically. Review the precondition against the cases the caller actually passes.

## Run

```bash
fv-dafny AssumeFalse.dfy AssumeFalse.dcfg
fv-dafny ContradictoryPrecondition.dfy ContradictoryPrecondition.dcfg
```
