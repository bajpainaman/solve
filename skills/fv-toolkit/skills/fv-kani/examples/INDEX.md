# Kani examples

`tests/examples.d/kani.sh` in the repository runs every example in this
table. A good example meets its declared outcomes and detects its
mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/allocate-bonus](good/allocate-bonus/README.md) | good | Domain logic: pricing and fee calculation (A3) | A bounded loop, a `kani::cover!` witness, and `kani::assume` built from the real input domain |
| [bad/narrow-assume](bad/narrow-assume/README.md) | bad | Domain logic: pricing and fee calculation (A3) | An assume not derived from how the function is called can narrow the proof past the exact bug it should catch |
| [bad/unbounded-loop](bad/unbounded-loop/README.md) | bad | Domain logic (A3) | A loop bound that depends on a symbolic input has no unwind bound that covers it |
