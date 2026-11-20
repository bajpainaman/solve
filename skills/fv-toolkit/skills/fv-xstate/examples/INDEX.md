# XState examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its declared outcomes and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/checkout](good/checkout/README.md) | good | Forms and multi-step wizards (F2) | A path replayed against the real code is a conformance check; a rejected design's machine supplies the illegal paths a correct model never generates |
| [bad/unreachable-state](bad/unreachable-state/README.md) | bad | Any | A state with no incoming transition has no generated path, and nothing says it was skipped |
| [bad/asserts-nothing](bad/asserts-nothing/README.md) | bad | Any | A path test that checks a step's shape instead of its expected value misses every wrong transition |
