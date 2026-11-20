# A path test that asserts nothing at each step

**Symptom:** the same bug that `examples/good/checkout`'s mutations file detects is missed here.

## The bug

`weak-run.cjs` replays every generated path against the real `Checkout` class, like the good example does, but the check at each step asks only whether `impl.step` has a shape, never whether it is the state the path says it should be:

```js
if (typeof impl.step !== "string") {
  failed = true;
}
```

`impl.step` is a string in every reachable state of this class, correct or wrong, so this condition can never be true.

## The real output

```text
$ node weak-run.cjs
PASS path ConformsToMachine: xstate.init -> cart
...
PASS path ConformsToMachine: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> SET_PAYMENT -> NEXT -> confirmed
```

```text
$ fv-mutate weak-run.mutations
MISSED setting the payment flag is dropped
UNCOVERED ConformsToMachine
SUMMARY detected=0 missed=1 error=0 green=0 brittle=0 uncovered=1
```

`examples/good/checkout/run-paths.mutations` plants the same mutation, dropping `this.hasPayment = true;`, and its `run-paths.cjs` detects it, because it compares `impl.step` and the context flags against the value the path actually declares at each step.

## The fix

Compare against the path's own state at each step, as `examples/good/checkout/run-paths.cjs`'s `conforms()` does: `impl.step !== step.state.value`, and the same comparison on the context fields the machine tracks.

## The check that catches it

`fv-mutate` catches it directly, by running the same mutation against this weaker check and reporting `MISSED`. The lesson is in the comparison: a path test must assert equality with the path's own expected value at every step, not merely that some value exists.
