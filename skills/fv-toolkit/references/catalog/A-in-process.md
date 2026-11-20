# Catalog A — In-process code architecture

Most local patterns are about structure or single-threaded logic, so property-based tests and Alloy cover them. Model checkers come in only where threads, async tasks, or actors share state. Purely structural patterns with no invariants of their own (Factory, Builder, Adapter, Decorator, DI containers) are listed at the end as low-value targets.

### A1. Structural / layering

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Layered / N-tier | Lower layers call upward; domain imports infra | Alloy (or import-linter / ArchUnit) | Modules as atoms, `imports` relation | No dependency from domain to infra; acyclic | Generate the relation from the real import graph |
| Hexagonal (ports & adapters) / Clean / Onion | Adapters leak into core; port contract drifts between adapters | Alloy for dependencies; Hypothesis for port contracts | One contract test suite per port, run against every adapter | All adapters satisfy the same contract | Shared parametrized test over all adapters |
| Modular monolith / bounded contexts | Context reaches into another's tables | Alloy | Contexts, tables, access relation | Each table owned by exactly one context | Generate from SQL access logs or ORM metadata |
| Plugin / microkernel | Plugin breaks host invariants; load-order bugs | Hypothesis stateful | Random load/unload/call sequences | Host invariants hold for any plugin order | Stateful test with fake plugins |
| Middleware / interceptor chain | Order-sensitive bugs (auth after logging of secrets) | Alloy or Z3 | Chain as a sequence; required orderings as constraints | Required precedences always hold | Assert on the configured chain at startup |

### A2. Data access

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Repository | In-memory and DB implementations disagree; query semantics drift | Hypothesis stateful (model = dict) | `RuleBasedStateMachine` with add/get/remove/query rules against a dict model | Repository == dict model after every step | Same test runs against in-memory and real-DB repos |
| Unit of Work | Partial commits; identity map returns stale objects | Hypothesis stateful; TLA+ if concurrent | Begin/register/commit/rollback actions | Commit is all-or-nothing; rollback restores prior state | Stateful test with injected failure on Nth write |
| Active Record vs Data Mapper | Save hooks fire twice; dirty tracking misses changes | Hypothesis | Random field mutations then save/reload | reload(save(x)) == x | Round-trip property |
| Optimistic locking (version column) | Lost update when two sessions save | TLA+/Quint or FizzBee | Two clients, read-modify-write, version check | No lost update; version strictly increases | Concurrent integration test replaying counterexample |
| Caching (memoize, LRU, read-through) | Stale entries; wrong eviction; key collisions | Hypothesis stateful vs. uncached oracle | Cache + backing store + invalidations | Cached read == uncached read (after invalidation) | Oracle comparison test |

### A3. Domain logic

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| DDD aggregate | Invariants broken across a sequence of commands | Hypothesis stateful; Dafny for core math | Commands as rules, aggregate invariant as `@invariant` | Invariant holds after every command | Stateful test on the aggregate class |
| Domain events | Event emitted but state not changed (or the reverse) | Hypothesis stateful | Fold events into a shadow state | fold(events) == aggregate state | Compare projection with the aggregate |
| State pattern / explicit FSM | Illegal transitions; unreachable or dead states | Alloy, XState graph, or TLA+ | States + allowed transitions | Only allowed transitions; every state reachable; terminal states final | Generate the transition table from code (enum + map) |
| Specification pattern | Composed specs contradict or are always-false | Z3 | Each spec as a predicate | Satisfiable; and/or/not behave as expected | Encode predicates from code |
| Rules engine / decision table | Overlaps, gaps, contradictory rules, order dependence | Z3 (or Alloy) | Rule conditions as constraints over input fields | Completeness (some rule fires), uniqueness (one fires), determinism | Generate SMT from the rule table |
| Interpreter / DSL | Evaluator crashes or diverges on valid programs | Hypothesis + Lean/Dafny reference model | Grammar-based generators | Evaluator == reference semantics; well-typed programs don't error | Differential testing (the Cedar approach) |
| Strategy / policy objects | Strategies disagree on shared guarantees | Hypothesis | One property suite for all strategies | Each strategy meets the shared contract | Parametrized tests |

### A4. Concurrency inside a process

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Mutex / RW lock | Deadlock; forgotten release on error path | TLA+/PlusCal; Shuttle/Loom (Rust) | Processes + lock variable, one step per lock op | Mutual exclusion; deadlock freedom | Controlled-scheduler test on real code |
| Producer–consumer / bounded queue | Lost items; deadlock on full/empty; spurious wakeups | TLA+/PlusCal | Buffer, producers, consumers, condition waits | Conservation; no deadlock; bounded size | Shuttle/Loom or stress test with counterexample schedule |
| Thread pool / executor | Starvation; task lost on shutdown | TLA+ | Workers, queue, shutdown flag | Every submitted task runs or is rejected | Shutdown-race test |
| async/await, event loop | Lost wakeups; interleaving across `await` points; cancellation leaks | FizzBee or TLA+ (each `await` = a step) | Tasks yield at awaits | No shared-state invariant broken across awaits | Deterministic event-loop test |
| Actor model | Mailbox ordering assumptions; lost messages on restart | P or Stateright | Actors + mailboxes + supervisor restarts | No message lost; state consistent after restart | Stateright runs the same actor code |
| CSP channels (Go) | Goroutine leaks; deadlock on unbuffered channels | TLA+/PlusCal or Spin | Channels as sequences with capacity | Deadlock freedom; all goroutines terminate | `go test -race` + counterexample replay |
| Lock-free structures | ABA; memory-order bugs | Loom (Rust), CDSChecker (C++), TLA+ for algorithm | Atomic ops as steps | Linearizability | Linearizability checker on recorded history |
| Reactive streams | Backpressure violations; out-of-order emission | TLA+ or Hypothesis stateful | Demand counter + emissions | Never emit more than requested | Stateful test on the operator |

### A5. Low-value targets

Factory, Builder, Adapter, Decorator, Facade, Proxy, Singleton, DI containers. Verify only the contract of what they wrap. The skill should say so and skip them, so the toolkit doesn't spend effort where no property exists.
