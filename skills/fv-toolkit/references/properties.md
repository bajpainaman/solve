# Property families

Pick the families that apply, then phrase each one as a sentence about the system under check.

| Family | Statement | Kind | Typical tools |
| --- | --- | --- | --- |
| Conservation | Nothing created or lost: rows in = rows out + rejected; debits = credits | Safety | Hypothesis, Z3, TLA+ |
| Idempotence | f(f(x)) = f(x); redelivery has no extra effect | Safety | Hypothesis stateful, TLA+ |
| Order independence | Result is the same for any permutation of inputs | Safety | Hypothesis, Z3 |
| Oracle equivalence | Optimized = naive; streaming = batch; incremental = full recompute; replay = live | Safety | Hypothesis, CrossHair `diffbehavior`, VeriEQL |
| Mutual exclusion | At most one leader, owner, or writer per resource | Safety | TLA+/Quint, P |
| Monotonicity | Offsets, watermarks, versions, terms never go backward | Safety | TLA+/Quint |
| Structural integrity | Keys unique, references resolve, intervals don't overlap, tenants isolated | Safety | Alloy, Z3 |
| Consistency model | Linearizable / serializable / snapshot / causal / read-your-writes | Safety | TLA+ refinement, Elle, Stateright |
| Convergence | Replicas, caches, projections, reconcilers eventually agree | Liveness | TLA+/Quint, P, FizzBee |
| Progress | Every request is eventually completed, rejected, or parked; nothing stuck | Liveness | TLA+/Quint, P |
| Bounded resources | Queues, retries, memory stay within limits | Safety | TLA+, UPPAAL |
| Non-vacuity | The model actually reaches the interesting states ("sometimes" checks) | Sanity | Every model checker |
