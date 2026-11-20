# Pattern catalog index

Find the pattern here, then read only the catalog file that holds it. Each row of a catalog gives what breaks, the tool, the model, the properties and the link to code. A row can name a tool that is outside the core toolkit; `../tools.md` maps each one to its core substitute.

## [Catalog A — In-process code architecture](A-in-process.md)

- A1. Structural / layering: Layered / N-tier; Hexagonal (ports & adapters) / Clean / Onion; Modular monolith / bounded contexts; Plugin / microkernel; Middleware / interceptor chain
- A2. Data access: Repository; Unit of Work; Active Record vs Data Mapper; Optimistic locking (version column); Caching (memoize, LRU, read-through)
- A3. Domain logic: DDD aggregate; Domain events; State pattern / explicit FSM; Specification pattern; Rules engine / decision table; Interpreter / DSL; Strategy / policy objects
- A4. Concurrency inside a process: Mutex / RW lock; Producer–consumer / bounded queue; Thread pool / executor; async/await, event loop; Actor model; CSP channels (Go); Lock-free structures; Reactive streams

## [Catalog B — Distributed and cloud patterns](B-distributed.md)

- B1. Messaging and integration: Pub/sub, event notification; Event-carried state transfer; Competing consumers; Idempotent receiver (inbox); Transactional outbox; Claim check; Dead-letter queue / poison message; Request–reply over queues; Webhooks (outbound)
- B2. Workflows and transactions: Saga (orchestrated); Saga (choreographed); Two-phase commit; Workflow engine / durable execution (Temporal, Step Functions, Airflow); Distributed cron / scheduler; Compensating transaction
- B3. Coordination and replication: Leader election; Leases + fencing tokens; Consensus (Raft, Paxos, VSR); Primary–backup / async replication; Leaderless / quorum (Dynamo-style); Multi-leader / active-active multi-region; CRDTs; Gossip / anti-entropy (Merkle trees); Vector clocks / HLC; Consistency guarantees exposed to clients
- B4. Partitioning and scaling: Sharding / partition rebalancing; Consistent hashing; Service discovery; Autoscaling / scale-in
- B5. Resilience: Retry with backoff + jitter; Circuit breaker; Bulkhead / rate limiter / token bucket; Timeouts + cancellation; Health check / load shedding
- B6. Edge, API, and deployment: API gateway / BFF / gateway aggregation; Sidecar / service mesh; Strangler fig / anti-corruption layer; Blue-green / canary / rolling deploy; Feature flags / config propagation; Serverless / FaaS

## [Catalog C — Data systems](C-data.md)

- C1. Batch and orchestration: Batch ETL / ELT stage; SQL transform / dbt model; DAG orchestration (Airflow, Dagster, Prefect); Incremental load (watermark / cursor); Backfill / reprocessing; Idempotent re-runs (partition overwrite); Reconciliation jobs; Data contracts / schema evolution
- C2. Streaming: Stream windowing + watermarks; Exactly-once via checkpoints (Flink-style); Kafka transactions / EOS; Consumer groups / rebalancing; Stream–table join / enrichment; Lambda architecture; Kappa / replay from log
- C3. Change data capture and storage formats: CDC (log-based); Lakehouse commits (Iceberg, Delta, Hudi); Compaction / vacuum; Medallion (bronze/silver/gold); Partitioned tables / late partitions
- C4. Modeling and analytics correctness: Slowly changing dimensions (SCD2); Upsert / MERGE / dedup; Incremental materialized views; Feature store (point-in-time joins); Data lineage / PII propagation; Multi-tenant pipelines; Ledger / double-entry
- C5. Integration, identity, and signal data: Entity resolution / identity merge; Bi-directional sync with external systems (CRM, ticketing, calendars); Third-party API ingestion (rate-limited, paginated); Inbound webhook ingestion; Enrichment pipelines; Activity / event aggregation (signals, analytics counters); Segmentation / audience rules

## [Catalog D — Storage and database internals](D-storage.md)

- Transactions at a given isolation level; Read-modify-write without locks; SELECT … FOR UPDATE / pessimistic locking; Optimistic concurrency (version / ETag / CAS); MVCC / snapshot reads; WAL / commit log; LSM tree / B-tree / custom storage engine; ID / sequence generation (Snowflake ids, ULIDs); Soft delete / tombstones; Row-level security / multi-tenant schemas; Migrations (expand/contract); Distributed SQL / Raft-replicated KV

## [Catalog E — Infrastructure, security, and policy](E-infra-security.md)

- IAM / access policies; RBAC; ABAC / policy languages (Cedar, OPA/Rego); ReBAC (Zanzibar-style); Network reachability (VPC, security groups, k8s NetworkPolicy); Infrastructure as code (Terraform, CDK); Kubernetes controllers / operators (reconcile loops); Secrets / certificate / key rotation; OAuth / OIDC / session protocols; Webhook signatures / HMAC verification; Multi-account / landing-zone guardrails (SCPs); Disaster recovery / backups

## [Catalog F — APIs, frontend, and domain logic](F-api-frontend-domain.md)

- F1. APIs and protocols: REST / OpenAPI contract; Stateful API workflows (create → get → update → delete); Idempotency keys on POST; Cursor pagination; API versioning; gRPC / event schema evolution (protobuf, Avro); Rate-limited public API
- F2. Frontend and client: UI flows as state machines (XState); Redux / reducers / Elm architecture; Optimistic UI updates; Offline-first sync / local-first (CRDT or op log); Forms and multi-step wizards; Auth session handling in client
- F3. Domain logic (any industry): Rule / eligibility / decision tables; Pricing, fee, and discount calculation; Promotion / coupon stacking; Inventory and reservations; Order / fulfillment lifecycle; Subscriptions and entitlements; Quotas, limits, and threshold accumulators; Matching and allocation; Approval and submission workflows; Permissions on shared content; Collaborative editing / versioning; Notification and messaging dedup; Counters, leaderboards, voting, polls; Game and simulation state; Money and rounding; Units and measurement; Time zones, calendars, periods; Scheduling and recurrence; Search, ranking, recommendation rules; Reports and exports

## [Catalog G — Real-time communication and collaboration](G-realtime.md)

- Session / meeting lifecycle; Signaling (SDP offer/answer, ICE, renegotiation); SFU / media routing control plane; Presence; Chat / message delivery and ordering; Typing indicators / ephemeral state; Recording and transcription pipelines; Permissions in live sessions (waiting room, breakout rooms, screen-share rights); Shared whiteboard / co-editing; Notifications and calendar integration
