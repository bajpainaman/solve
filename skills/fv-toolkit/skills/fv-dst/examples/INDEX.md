# DST examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its declared outcomes and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/primary-backup](good/primary-backup/README.md) | good | Primary-backup / async replication (B3) | One seeded scheduler owns task order, delay, loss, duplication, crash and restart; the rejected design is checked beside the chosen one |
| [bad/unseeded-rng](bad/unseeded-rng/README.md) | bad | Any | A sweep that shares one `random.Random` across its runs reports failing seeds that do not replay on their own |
| [bad/fault-never-injected](bad/fault-never-injected/README.md) | bad | Any | A fault the sweep declares but never wires in leaves the rejected design passing |
