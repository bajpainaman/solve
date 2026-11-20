# Dafny examples

`tests/test_examples.sh` in the repository runs every example in this table. A good example meets its declared outcome and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/allocation](good/allocation/README.md) | good | Pricing, fee, and discount calculation (F3) | A proved core, compiled, and checked against an independent reference with a mutations file |
| [bad/unsound-proof](bad/unsound-proof/README.md) | bad | Pricing, fee, and discount calculation (F3) | An `assume` with no `{:axiom}` warns; a contradictory precondition does not warn at all |
| [bad/masked-timeout](bad/masked-timeout/README.md) | bad | Pricing, fee, and discount calculation (F3) | Raising the time limit until a proof passes does not make the proof better structured |
