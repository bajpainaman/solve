# Elle anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Anti-pattern | Symptom | Fix / check | Source |
| --- | --- | --- | --- |
| `-a` names fewer anomalies than the claimed isolation level forbids | `valid? true` on a history with a real anomaly the claimed level does not allow | Declare every anomaly in `--help`'s list for the claimed level, not only the ones already suspected | `examples/bad/weak-model/` in this plugin |
| A predicate anomaly encoded as `list-append`/`rw-register` operations | `valid? true` on a history whose real system has a bug, because the model has no delete or update to represent it | Pick a model with the needed operations, or check the real table directly | `examples/bad/predicate-anomaly/` in this plugin, and the model descriptions in [the elle-cli README](https://github.com/ligurio/elle-cli) |
| A history recorded at a weaker isolation level than the one declared in `-c` | A real anomaly is attributed to the wrong cause, or missed because the wrong anomalies were searched for | Record `-c` from the system's actual configuration, not from what the application assumes it set | [Jepsen's MySQL analysis](https://jepsen.io/analyses/mysql-8.0.34), which found repeatable-read in MySQL still allows G2-item and G-single |
| Checking only one short history and generalizing | A real anomaly exists under load but this one short, hand-written or lightly-loaded run never triggers it | Treat a clean mechanical check on a short history as a sanity check, not proof that production traffic cannot trigger the anomaly | [the Elle paper](https://arxiv.org/pdf/2003.10554) |
| Any history generated without a mutations file | No evidence the checker would have caught the anomaly it is meant to catch | Plant the anomaly directly, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes | `${CLAUDE_PLUGIN_ROOT}/references/bite.md` |

## A symptom and where to look first

| Symptom | Look at |
|---|---|
| `valid? true` and you expected an anomaly | The `-a` list first, then whether the operation values were transcribed from a real run |
| `valid? false` and you did not expect it | The anomaly named in `anomaly-types`, then the operations in its `cycle` |
| `:unknown` | `-s`/`--cycle-search-timeout`, or the history is too large for the default timeout |
| Two runs of the same history disagree | A different `-a` or `-c` flag between the two runs, not a change in the history |
