# Elle examples

`tests/test_examples.sh` in the repository runs every example in this table. A good example meets its declared outcome and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/list-append-serializable](good/list-append-serializable/README.md) | good | Transactions at a given isolation level (D) | A header that declares the model and the outcome, with a mutations file |
| [good/write-skew](good/write-skew/README.md) | good | Transactions at a given isolation level (D) | A declared anomaly is the witness: the example also proves the anomaly is reachable |
| [bad/weak-model](bad/weak-model/README.md) | bad | Transactions at a given isolation level (D) | `-a`, not `-c`, decides what gets searched for |
| [bad/predicate-anomaly](bad/predicate-anomaly/README.md) | bad | Transactions at a given isolation level (D) | `list-append` and `rw-register` have no delete or update, so some anomalies cannot be posed to either model |
