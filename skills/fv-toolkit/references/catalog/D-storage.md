# Catalog D — Storage and database internals

Treat the database as a component with a stated contract (isolation level, durability), and check that your application only relies on what that contract gives. Jepsen's MySQL analysis is the cautionary case: Repeatable Read there still allows G2-item, G-single, and lost updates ([Jepsen](https://jepsen.io/analyses/mysql-8.0.34)).

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Transactions at a given isolation level | App assumes serializable but runs on read committed / snapshot; write skew | TLA+ app model over an abstract store parameterized by isolation; Elle on real histories | Concurrent app transactions; store allows the anomalies of the chosen level | App invariant (e.g. balance ≥ 0, one booking per seat) holds under that level | Run Elle on histories from integration tests |
| Read-modify-write without locks | Lost update | TLA+/FizzBee (FizzBee's wire-transfer example) | Two clients interleaving read and write | No lost update | Concurrency test from counterexample |
| SELECT … FOR UPDATE / pessimistic locking | Deadlocks across tables; lock order inversions | TLA+/PlusCal | Lock acquisition order per code path | Deadlock freedom (global lock order) | Static check of lock order + test |
| Optimistic concurrency (version / ETag / CAS) | ABA; retries livelock under contention | TLA+ | Readers, CAS writers, retry loop | Linearizable updates; progress under bounded contention | Stateright / linearizability checker |
| MVCC / snapshot reads | Long-running snapshot sees inconsistent cross-table state (if app splits reads) | TLA+ | Versions, snapshots, GC | Reads within one snapshot are consistent | Elle |
| WAL / commit log | Torn write or lost fsync after crash | TLA+ for protocol; DST for code | Log, fsync, crash at any point | Recovered state = prefix of acknowledged writes | DST with storage faults |
| LSM tree / B-tree / custom storage engine | Lost keys after compaction or split | Hypothesis stateful vs. dict; Kani/Shuttle in Rust | Random put/get/delete/compact | Engine == dict model; crash consistency | ShardStore-style PBT ([AWS](https://aws.amazon.com/blogs/storage/how-automated-reasoning-helps-us-innovate-at-s3-scale)) |
| ID / sequence generation (Snowflake ids, ULIDs) | Duplicates across nodes or after clock rollback | TLA+ with clock skew; Hypothesis | Nodes, clocks, counters | Uniqueness; monotonic per node | Property test with fake clocks |
| Soft delete / tombstones | Deleted rows resurface in queries or replication | Alloy (query coverage) + Hypothesis | Queries × deleted filter | No query returns tombstoned rows | Lint queries |
| Row-level security / multi-tenant schemas | Missing tenant predicate on one query path | Alloy or Z3 over policy definitions | Roles, tenants, policies | No principal reads another tenant's rows | Generated negative tests |
| Migrations (expand/contract) | Code version N and schema version N+1 incompatible mid-deploy | Alloy (version matrix), TLA+ (rollout order) | Code versions × schema versions over time | Every co-existing pair works | Run old-code tests against new schema |
| Distributed SQL / Raft-replicated KV | Stale reads after leader change | TLA+ + Jepsen/Elle | Leader leases, follower reads | Linearizable reads where claimed | Jepsen-style tests |
