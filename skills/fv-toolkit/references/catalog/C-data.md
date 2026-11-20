# Catalog C — Data systems

Data-system bugs are mostly silent: rows dropped, double-counted, or landing in the wrong window, with no crash. So the most useful checks here are conservation and oracle-equivalence properties on real transforms, plus TLA+/Quint models of the cursors, commits, and orchestration around them.

### C1. Batch and orchestration

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Batch ETL / ELT stage | Rows dropped or duplicated by joins, filters, dedup | Hypothesis (dataframes), Z3 for transform predicates | Random input tables through the real transform | Conservation: in = out + rejected; key uniqueness; types/nullability | Property tests in CI on each transform |
| SQL transform / dbt model | Rewrite changes semantics; NULL handling | VeriEQL / SQLSolver; Hypothesis-generated tables | Old query vs. new query | Equivalent on all (bounded) databases | Run equivalence check on refactor PRs |
| DAG orchestration (Airflow, Dagster, Prefect) | Task runs twice after scheduler restart; downstream runs on partial upstream | Quint/TLA+ | Tasks, dependencies, states, scheduler crash | Dependencies respected; every run terminates; no task runs twice concurrently | MBT against a fake executor |
| Incremental load (watermark / cursor) | Boundary rows missed (`>` vs `>=`), late-committing rows skipped, clock skew | TLA+/Quint | Source rows with commit times, cursor, concurrent commits | Every source row loaded exactly once across all runs | Hypothesis: random commit timings vs. full reload oracle |
| Backfill / reprocessing | Backfill overwrites newer live data | TLA+/Quint | Live writer + backfill writer, versions | No regression to older data | Trace validation on writes |
| Idempotent re-runs (partition overwrite) | Re-run appends instead of replaces | Hypothesis | Run job twice | run(run(x)) == run(x) | Property test |
| Reconciliation jobs | Reconciler "fixes" in-flight writes, fights live path | TLA+ | Live path + reconciler + delays | Converges; never reverts a newer write | Fault test |
| Data contracts / schema evolution | Producer change breaks a consumer; nullability drift | Alloy or Z3 | Schema versions, compatibility rules (backward/forward/full) | Every live producer–consumer pair compatible | Schema-registry check in CI |

### C2. Streaming

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Stream windowing + watermarks | Late events dropped or double-counted; windows close too early | TLA+/Quint for watermark logic; Hypothesis for aggregates | Event time vs. processing time, out-of-order arrival, allowed lateness | Final result == batch recompute on the same events (within lateness bound) | Oracle test: streaming vs. batch |
| Exactly-once via checkpoints (Flink-style) | Sink writes not tied to checkpoint; duplicates after restore | TLA+ | Operators, barriers, checkpoint store, two-phase sink | Output after restore == output without failure | Fault-injection in DST |
| Kafka transactions / EOS | Zombie producers; aborted records visible | TLA+ ([Vanlightly's spec](https://jack-vanlightly.com/analyses/2024/12/2/verifying-kafka-transactions-diary-entry-1-a-first-step)) or FizzBee | Producers, coordinators, txn log, fencing | read\_committed consumers never see aborted data | Integration test |
| Consumer groups / rebalancing | Two consumers own a partition; offsets committed before processing | TLA+/Quint | Members, generation ids, offset commits | One owner per partition per generation; at-least-once | MBT on the consumer wrapper |
| Stream–table join / enrichment | Join against wrong version of the table | Quint/TLA+ | Versioned table + stream timestamps | Join uses table state as of event time | Hypothesis oracle |
| Lambda architecture | Batch and speed layers disagree at handoff | Hypothesis | Same input to both paths | Merged view == batch view after catch-up | Oracle test |
| Kappa / replay from log | Replay not deterministic (wall clock, random, external calls) | Hypothesis + CrossHair | Replay twice | replay(log) is deterministic and == live state | Replay test |

### C3. Change data capture and storage formats

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| CDC (log-based) | Gaps or reorders on connector restart or snapshot-to-stream switch | TLA+/Quint | Source log, snapshot, connector offset, restart | Downstream eventually equals source; no gap at handoff | Trace validation on connector offsets |
| Lakehouse commits (Iceberg, Delta, Hudi) | Concurrent writers conflict; retries after "unknown" commit state duplicate data | TLA+ ([Vanlightly's Delta/Hudi models](https://jack-vanlightly.com/analyses)) | Writers, catalog pointer swap (OCC), retries, status checks | Serializable/snapshot commits; no duplicate commit on retry | Multi-writer integration test |
| Compaction / vacuum | Files deleted while a reader's snapshot uses them | TLA+ | Snapshots, retention, readers | No live snapshot references a deleted file | Fault test |
| Medallion (bronze/silver/gold) | Layer contracts drift; gold double-counts | Hypothesis per layer + Alloy for contracts | Each hop is a transform with a contract | Conservation and uniqueness at each hop | Layer-level property tests |
| Partitioned tables / late partitions | Late data lands in a closed partition and is never re-aggregated | TLA+ | Partitions, closure, late arrivals | Every row is eventually in the aggregate | Oracle test |

### C4. Modeling and analytics correctness

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Slowly changing dimensions (SCD2) | Overlapping or gappy validity intervals; two current rows | Alloy; Hypothesis | Rows with \[valid\_from, valid\_to) per key | Intervals contiguous and non-overlapping; exactly one current row | Property test on the merge |
| Upsert / MERGE / dedup | Order-dependent results; key collisions | Hypothesis; Z3 for key design | Random duplicates and orderings | Result independent of input order; last-writer rule applied | Property test |
| Incremental materialized views | Incremental result ≠ full recompute after deletes/updates | Hypothesis | Random change streams | incremental == full recompute | Oracle test |
| Feature store (point-in-time joins) | Label leakage from future feature values | Hypothesis; Alloy | Entities, feature timestamps, label times | Feature time ≤ label time for every training row | Property test on training-set builder |
| Data lineage / PII propagation | PII flows into an unmasked output | Alloy | Columns, transforms, `derives_from` relation | No path from PII column to unmasked sink | Generate relation from lineage metadata |
| Multi-tenant pipelines | Tenant data mixed in shared jobs or caches | Alloy | Tenants, datasets, jobs, outputs | No output depends on another tenant's input | Lineage-derived check |
| Ledger / double-entry | Unbalanced entries; mutation of posted entries | Hypothesis; Dafny for core posting logic; TLA+ if concurrent | Accounts, entries, postings | Sum of debits == sum of credits; posted entries immutable; balance = sum of entries | Property + stateful tests |

### C5. Integration, identity, and signal data

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Entity resolution / identity merge | Merges not transitive; unmerge loses data; two golden records for one person | Alloy (merge graph) + Hypothesis | Records, match edges, merge/unmerge actions | Each record in exactly one cluster; merge order-independent; unmerge restores originals | Property tests on merge engine with random match orders |
| Bi-directional sync with external systems (CRM, ticketing, calendars) | Ping-pong update loops; last-writer clobbers; deletes resurrect | TLA+/Quint | Two stores, sync jobs both ways, change markers, conflict rule | No infinite echo; convergence; deletes stay deleted | MBT with fake external API |
| Third-party API ingestion (rate-limited, paginated) | Gaps when rate-limited mid-page; duplicate pages after token refresh | TLA+/Quint; Hypothesis stateful | Cursor, rate-limit backoff, token expiry, crash | Every remote record ingested once; ingestion resumes after limits | Stateful test against a fake API with injected 429s |
| Inbound webhook ingestion | Duplicate and out-of-order deliveries; missed events with no replay | TLA+ + periodic reconciliation model | Webhook stream + reconciliation poll | Final state == source of truth after reconciliation | Oracle test vs. full pull |
| Enrichment pipelines | Enrichment overwrites user-entered data; stale enrichment wins | Alloy (field precedence) + Hypothesis | Sources with precedence and timestamps | Higher-precedence source never overwritten by lower | Property tests on merge-by-precedence |
| Activity / event aggregation (signals, analytics counters) | Double-counting on replay; late events missed | Hypothesis oracle | Event streams with duplicates and lateness | Aggregate == dedup'd batch recompute | Streaming vs. batch oracle |
| Segmentation / audience rules | Segment membership disagrees between UI, API, and exports | Z3 + Hypothesis differential | Rule expressions over profile fields | Same membership from every evaluator | Differential tests across evaluators |
