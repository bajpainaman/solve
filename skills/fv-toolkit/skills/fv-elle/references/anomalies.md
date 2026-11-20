# Models, consistency and anomalies

## Models

| Model | What it checks | Needs |
|---|---|---|
| `list-append` | Append and read of named lists. Catches most write-write and write-read anomalies | Every key's history of appends is enough to derive its version order |
| `rw-register` | Plain read/write of named registers | A value per key per write |

Both models support only reading a whole key and writing (or appending to) it. Neither has a delete or an update. See `anti-patterns.md`.

## Consistency models and the anomalies that break them

`-c` only labels what the history is checked against, in the report's `not` and `also-not` fields; it does not change what `-a` searches for. An anomaly not named in `-a` is never looked for, no matter what `-c` says. `examples/bad/weak-model/` reproduces this directly: `-a G0,G1a,G1b,G1c` reports a write skew as `valid`, because `G2-item` was never in the search list, even though the header names `read-committed`, which `G2-item` does not violate.

`--help` lists every anomaly name `-a` accepts. When in doubt, declare the full list this plugin's `strict-serializable` examples use (`G0,G1a,G1b,G1c,G-single,G-single-process,G-single-realtime,G2-item`) rather than guess which subset a weaker level needs; a wider `-a` list only ever finds more, never fewer, real anomalies.

## Measured on elle-cli 0.1.9

Each fact below was reproduced with this plugin's examples.

| Fact | Consequence |
|---|---|
| `elle-cli` exits 0 for `valid? true`, 1 for `valid? false`, and a nonzero code with a Java stack trace for a missing or unreadable file | `fv-elle` reads the `-v` JSON report, not the exit code alone, so it can also name the anomaly |
| The report's `anomaly-types` field names the anomaly `elle-cli` actually found, which can differ from the name passed to `-a` | `-a write-skew` on a genuine write skew still reports `"anomaly-types":["G2-item", ...]`. Declare the name the report uses in the `expect` header, not the flag passed to `-a` |
| A write skew between two keys that each transaction only reads once and appends to once is found as plain `G2-item`, with no `-realtime` suffix | `G2-item` comes from the per-key version order the appends define, not from wall-clock or `:time` fields. A variant with `-realtime` in its name needs real-time evidence, which this plugin's histories do not record |
| The elle-cli 0.1.11 release needs `java.util.SequencedCollection`, added in JDK 21 (`NoClassDefFoundError`) | The pin in `scripts/installers/elle` stays at 0.1.9, the newest release this plugin found that runs on a JDK no newer than 20 |
| Elle-cli is a standalone uberjar; it needs no Clojure or Leiningen install | `scripts/installers/elle` only downloads and verifies the jar |

## From the Elle documentation, not reproduced here

- `knossos` (via `cas-register` and `mutex`) checks a single register or lock against every possible history, which is exponential; it is practical only for a short history.
- `-s`/`--cycle-search-timeout` bounds how long `elle-cli` searches a single strongly connected component for a cycle. A `:unknown` result on a large history usually means this timeout, not a clean history.
