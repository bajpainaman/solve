# TLA+ examples

`tests/test_examples.sh` in the repository runs every example in this table. A good example meets its declared outcomes and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/refund-race](good/refund-race/README.md) | good | Read-modify-write without a lock (D), idempotency on retries (F1) | One action per atomic step. One knob, one config per design, one witness |
| [good/idempotent-receiver](good/idempotent-receiver/README.md) | good | Idempotent receiver (B1) | A crash is a fault switch. The same design holds with the fault off and breaks with it on |
| [good/cache-invalidation](good/cache-invalidation/README.md) | good | Cache-aside read fills a stale entry (A2) | A version mark on an empty cache entry tells a stale fill from a fresh one. A variable keeps one type, because TLC stops on a comparison of mixed types |
| [good/cdc-snapshot-handoff](good/cdc-snapshot-handoff/README.md) | good | Change data capture, snapshot-to-stream handoff (C3) | A fenced choice of candidate values stands in for a timing race. An invariant that is gated on completion says nothing about a run still in progress |
| [good/dag-scheduler](good/dag-scheduler/README.md) | good | DAG orchestration, restart and dependency checking (C1) | A worker action keeps running while the scheduler is crashed. A restart reads a durable effect count and does not guess |
| [good/leader-election](good/leader-election/README.md) | good | Leader election under a partition (B3) | A candidate's view of the cluster is kept apart from the cluster's real size. A partition fault splits reachability and leaves the node set unchanged |
| [good/lease-fencing](good/lease-fencing/README.md) | good | Leases with fencing tokens (B3) | The ground-truth property is kept apart from the mechanism under test. A high-water mark that is set at grant time closes the race |
| [good/reconciler](good/reconciler/README.md) | good | Kubernetes-style reconcile loop over a stale cache (E) | The controller's expectation count stands in for ground truth that it cannot read. A watch event lowers that count |
| [good/release-ordering](good/release-ordering/README.md) | good | Rolling deploy across an expand-and-contract migration (D) | A fault switch covers only the one action that it affects. A deploy that is not rolling still needs an ordering guard against the step it races |
| [good/saga-orchestrated](good/saga-orchestrated/README.md) | good | Saga, orchestrated (B2) | A timeout fault lets a step settle before every attempt resolves. A fencing flag closes that window, and a ghost variable catches a late change |
| [good/transactional-outbox](good/transactional-outbox/README.md) | good | Transactional outbox (B1) | Three designs sit behind one knob, and the resume point is computed from durable state. A relay that retries from a durable flag can deliver the same row twice |
| [good/two-phase-commit](good/two-phase-commit/README.md) | good | Two-phase commit (B3) | The coordinator's durable vote record is kept apart from a manager's current state. A crash with no recovery is a real deadlock, and the config declares it |
| [good/watermark-cursor](good/watermark-cursor/README.md) | good | Incremental load by watermark cursor (C1) | A dedup set and the comparison operator form one design. A slow commit is bounded to the model's own run window |
| [good/lease-induction](good/lease-induction/README.md) | good | Mutex or lock (A4), with Apalache | An inductive invariant is checked in three steps: it holds initially, a step preserves it, and it implies the safety property |
| [bad/merged-atomicity](bad/merged-atomicity/README.md) | bad | Read-modify-write without a lock (D) | One action per function passes on a design that fails in production |
| [bad/liveness-without-fairness](bad/liveness-without-fairness/README.md) | bad | Any pattern with a progress property | Liveness without fairness fails on a stuttering trace and says nothing about the design |
| [bad/unreachable-state](bad/unreachable-state/README.md) | bad | Two-phase commit (B2) | A property holds when its state is unreachable, and only a witness shows it |
| [bad/strong-fairness-everywhere](bad/strong-fairness-everywhere/README.md) | bad | Any pattern with a progress property | Liveness that holds only under strong fairness assumes a scheduler guarantee that most implementations do not give |
| [bad/vacuous-fairness](bad/vacuous-fairness/README.md) | bad | Any | Fairness on an action whose guard is unreachable holds for free and supports nothing |
| [bad/symmetry-with-liveness](bad/symmetry-with-liveness/README.md) | bad | Any pattern with symmetric processes | `SYMMETRY` with a liveness `PROPERTY` prints no warning, and TLC can report a counterexample that breaks the spec's own fairness |
| [bad/unbounded-state](bad/unbounded-state/README.md) | bad | Any | An unbounded counter or queue makes TLC run without end. A `CONSTRAINT` bounds the search |
| [bad/invariants-only](bad/invariants-only/README.md) | bad | Any | An `INVARIANT` cannot relate two consecutive states. Only an action property catches a forbidden step |
| [bad/non-inductive-invariant](bad/non-inductive-invariant/README.md) | bad | Mutex or lock (A4), with Apalache | TLC confirms an invariant on the states it reaches. That does not make the invariant inductive |
