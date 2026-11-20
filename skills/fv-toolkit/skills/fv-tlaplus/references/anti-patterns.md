# TLA+ anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Tool | Anti-pattern | Symptom | Fix / check | Source |
| --- | --- | --- | --- | --- |
| TLA+ | One action per function instead of per atomic step | Spec passes; real interleavings are unreachable | One action per DB write / message; trace-validate | [SIGOPS 2026](https://sigops.org/2026/can-llms-model-real-world-systems-in-tla) |
| TLA+ | Liveness checked with no fairness | Liveness fails on stuttering, or is never meaningfully checked | Add WF on the processes that must progress | [learntla](https://learntla.com/core/temporal-logic.html) |
| TLA+ | Strong fairness sprinkled on every action | Liveness "proved" under assumptions no implementation provides | Use SF only where justified; prefer WF | [tlaplus group](https://groups.google.com/g/tlaplus/c/V3XJGR1n67U) |
| TLA+ | Vacuous fairness: action is never continuously enabled | WF holds trivially; property proves nothing | Check enabledness; use SF or restructure | [Sergey course notes](https://ilyasergey.net/CS6213/week-06-tla.html) |
| TLA+ | Symmetry sets used with liveness checking | Unsound liveness results | Symmetry for safety only | [Loncaric slides](https://conferences.mpi-inf.mpg.de/rg1/vtsa25/slides/Loncaric-2.pdf) |
| TLA+ | Unbounded state space (queues, counters) | TLC never finishes | State constraints or bounded constants; say so in report | [Sergey course notes](https://ilyasergey.net/PFM24/week-06-tla.html) |
| TLA+ | Invariants only, no action properties | Implementation violates the spec while the invariant still holds | Add action/refinement properties | [Datadog](https://www.datadoghq.com/blog/engineering/continuous-formal-spec-validation) |
| TLA+ | Trivially true property | "Passes" forever | Mutate the property; it must fail | [TLA-Prover](https://ai4fm.cs.luc.edu/papers/tla-prover/) |
| Any | LLM writes spec, runs checker once, reports success | Syntax passes, semantics wrong | Progressive, checker-in-the-loop generation; mutation checks; human review of properties | [AI4FM](https://ai4fm.cs.luc.edu/papers/llm-tla-evaluation/) |
