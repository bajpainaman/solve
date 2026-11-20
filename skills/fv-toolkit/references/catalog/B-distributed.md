# Catalog B — Distributed and cloud patterns

This is where behavioral model checkers pay off most: almost every pattern here is a protocol between processes that can crash, retry, and see messages late or twice. Default to Quint/TLA+ or P for the design, then link to code with model-based tests, trace validation, or deterministic simulation.

### B1. Messaging and integration

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Pub/sub, event notification | Duplicates, reordering, consumers missing events after restart | Quint/TLA+, P | Broker log, per-consumer offsets, at-least-once delivery | Every published event eventually processed; effect applied once | MBT: replay traces against consumer with a fake broker |
| Event-carried state transfer | Consumers apply stale snapshots over newer ones | Quint/TLA+ | Versioned events, out-of-order delivery | Consumer state version is monotonic | Hypothesis: shuffle events, check final state |
| Competing consumers | Same message processed by two workers after visibility timeout | TLA+/P with timeout fault | Queue with leases/visibility timeouts, slow worker | No double effect (with idempotency key) | Integration test with paused worker |
| Idempotent receiver (inbox) | Dedup record written after effect, crash between them | TLA+/Quint, FizzBee | Effect write and dedup write as separate steps + crash | Exactly-once effect despite redelivery | Crash-injection test at each step |
| Transactional outbox | Commit without event, or event without commit; relay publishes twice | TLA+/Quint | DB txn, outbox table, relay, broker, crash points | Committed change ⇔ eventually published; consumers dedupe | Trace validation on relay logs |
| Claim check | Payload deleted before consumer reads it | TLA+ | Blob store + message + GC | Referenced blobs are never collected | Test GC vs. slow consumer |
| Dead-letter queue / poison message | Message stranded forever; DLQ replay re-poisons | P or TLA+ | Retry counter, DLQ, replay action | Every message is processed or explicitly parked | Stateful test of retry policy |
| Request–reply over queues | Reply correlated to wrong request; orphaned replies | P | Correlation ids, timeouts | Reply matches request; timed-out requests release resources | MBT on the client library |
| Webhooks (outbound) | Lost on receiver downtime; reordering; retries flood | P or TLA+ | Delivery attempts, backoff, receiver state | Each event eventually delivered or dead-lettered; bounded attempts | Schemathesis on receiver + replay |

### B2. Workflows and transactions

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Saga (orchestrated) | Compensation for a step that never happened; compensation races retry | P (AWS's sweet spot) or TLA+ | Orchestrator FSM + participants + compensations + crashes | Every saga ends fully committed or fully compensated | MBT against orchestrator; PObserve-style log check |
| Saga (choreographed) | No one owns completion; cycles of events | TLA+/Quint | Participants reacting to events | Termination; no orphaned partial state | Trace validation across services |
| Two-phase commit | Coordinator crash leaves participants blocked | TLA+ (classic example), Stateright | TM, RMs, prepare/commit/abort | Atomicity; liveness only if TM recovers ([Demirbas](https://muratbuffalo.blogspot.com/2018/12/2-phase-commit-and-beyond.html)) | Stateright runs the same actors |
| Workflow engine / durable execution (Temporal, Step Functions, Airflow) | Non-deterministic workflow code breaks replay; activities run twice; tasks stuck "running" | Quint/TLA+ for the workflow; Hypothesis for replay determinism | Workflow as FSM; activity retries; worker crash | Each step runs ≥ 1 time with idempotent effect; workflow terminates; replay(history) == state | Replay tests against recorded histories |
| Distributed cron / scheduler | Job runs twice across nodes or never after failover | TLA+ | Scheduler leases, clock skew | At most once per period (with lease); at least once eventually | Fault-injection test |
| Compensating transaction | Compensation not inverse (fees, rounding) | Hypothesis | Random op + compensation | compensate(apply(s)) == s on business fields | Property test on domain code |

### B3. Coordination and replication

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Leader election | Two leaders after partition | TLA+/Quint | Nodes, terms, votes, partitions | At most one leader per term | Trace validation (etcd did this) |
| Leases + fencing tokens | Paused holder writes after lease expiry | TLA+ with clock skew + pause | Lease grant, expiry, storage checking token | Storage rejects any write with a stale token | Integration test with forced GC pause |
| Consensus (Raft, Paxos, VSR) | Log divergence, lost commits on membership change | TLA+ (+ TLAPS); DST for code | Standard Raft spec, extended per feature | Log matching; leader completeness; state-machine safety | Trace validation ([CCF, etcd](https://arxiv.org/pdf/2404.16075)); DST |
| Primary–backup / async replication | Acknowledged writes lost on failover | TLA+ | Primary, replicas, ack policy, failover | No acknowledged write is lost (under chosen ack policy) | Jepsen-style test |
| Leaderless / quorum (Dynamo-style) | Stale reads when R + W ≤ N; sloppy quorum anomalies | TLA+, Stateright | Replicas, quorum reads/writes, hinted handoff | Read-your-writes under R + W > N | Stateright linearizability tester |
| Multi-leader / active-active multi-region | Write conflicts; divergence | TLA+, Alloy for conflict rules | Regions, async replication, conflict resolution | Convergence; resolution is deterministic | Hypothesis: random concurrent ops, check convergence |
| CRDTs | Merge not commutative/associative/idempotent | Hypothesis (or Dafny/Lean proof) | Random states and merges | merge is commutative, associative, idempotent; convergence | Property test on merge function |
| Gossip / anti-entropy (Merkle trees) | Never converges under churn | FizzBee (its quick-start is gossip), TLA+ | Nodes exchanging digests | Eventual convergence with fair exchange | Simulation |
| Vector clocks / HLC | Wrong causality ordering | Hypothesis | Random message histories | Happens-before preserved by timestamps | Property test |
| Consistency guarantees exposed to clients | Docs and implementation disagree on what clients can observe | TLA+ client-centric spec + refinement ([Cosmos DB](https://arxiv.org/pdf/2210.13661)) | Clients + abstract store, no internals | Session/prefix/bounded-staleness/strong as stated | Elle or linearizability checker on histories |

### B4. Partitioning and scaling

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Sharding / partition rebalancing | Two owners during handoff; data lost in move | TLA+/Quint | Partitions, owners, migration steps, crash | One active writer per partition; no key lost | Trace validation on rebalance logs |
| Consistent hashing | Excess movement on node join/leave | Hypothesis | Random ring changes | Only ~K/N keys move; every key has an owner | Property test |
| Service discovery | Clients route to dead or draining instances | TLA+ | Registry, health checks, client caches, TTL | Traffic to draining node eventually stops | Fault test |
| Autoscaling / scale-in | Work lost when instance terminated mid-task | TLA+ | Instances, tasks, termination hook | Every task completes or is re-queued | Termination test |

### B5. Resilience

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Retry with backoff + jitter | Retry storms; metastable failure | TLA+/P + probabilistic simulation (AWS does this) | Clients, server capacity, retry policy | Load stays bounded; system recovers after spike | Load test with the failing parameters |
| Circuit breaker | Never closes; half-open lets a flood through | Alloy or TLA+ (small FSM) | Closed/Open/Half-open + counters + timer | Half-open admits ≤ N probes; eventually closes when healthy | XState-style path tests |
| Bulkhead / rate limiter / token bucket | Limit exceeded under concurrency | TLA+; Hypothesis for the bucket math | Concurrent acquires | Never more than N in flight / R per window | Concurrency test |
| Timeouts + cancellation | Work continues after caller gave up; resources leak | TLA+ | Caller, callee, cancel signal | Cancelled work releases resources eventually | Fault test |
| Health check / load shedding | Healthy-but-overloaded nodes kill themselves in a loop | TLA+/P | Health signal, load, restart | No restart cascade | Chaos test |

### B6. Edge, API, and deployment

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| API gateway / BFF / gateway aggregation | Partial failure produces inconsistent response; auth skipped on some routes | Alloy (route × policy coverage); Schemathesis | Routes, middleware, policies | Every route has auth; aggregation handles each sub-failure | Schemathesis on gateway |
| Sidecar / service mesh | mTLS gaps; retry at two layers multiplies load | Alloy (config), TLA+ (retry amplification) | Hops × retry policies | Total attempts ≤ budget | Config lint generated from model |
| Strangler fig / anti-corruption layer | Old and new paths disagree during migration | Hypothesis differential | Same request to both | new(x) == old(x) on shared fields | Shadow traffic comparison |
| Blue-green / canary / rolling deploy | Mixed versions break wire or schema compatibility | Alloy (version pairs), TLA+ (rollout steps) | Versions in flight, schema versions | Every co-existing version pair is compatible | Contract tests per pair |
| Feature flags / config propagation | Inconsistent flag state across services mid-rollout | TLA+ | Flag store, caches, TTLs | Dependent flags never observed in a forbidden combination | Runtime assertion |
| Serverless / FaaS | At-least-once triggers; cold-start ordering; concurrency limits | P or TLA+ | Trigger source, retries, concurrent invocations | Effects idempotent; no lost event | Same as idempotent receiver |
