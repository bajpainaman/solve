# Alloy anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Tool | Anti-pattern | Symptom | Fix / check | Source |
| --- | --- | --- | --- | --- |
| Alloy | Overconstraint via facts | No instances at all, so every `check` passes | `run` each predicate first; use unsat cores | [Alloy tutorial](https://alloytools.org/tutorials/online/sidenote-overconstraint.html) |
| Alloy | Facts that forbid the illegal states you need to handle | Model can't show how the system reaches a bad state | Move constraints from facts into predicates and assertions | [Hillel Wayne](https://hillelwayne.com/post/alloy-facts/) |
| Alloy | `x.f in S` when `x.f` can be empty | Vacuously true | Add `some x.f` | [Alloy forum](https://alloytools.discourse.group/t/tip-pitfalls-with-using-in-for-typechecking/420) |
| Alloy 6 | Missing or lax frame conditions | Unrelated mutable fields change arbitrarily | Frame every `var` per event; per-element, not union | [Alloy forum](https://alloytools.discourse.group/t/hello-learning-alloy-can-someone-help-me-with-a-basic-question-on-temporal-models/288) |
| Any | LLM writes spec, runs checker once, reports success | Syntax passes, semantics wrong | Progressive, checker-in-the-loop generation; mutation checks; human review of properties | [AI4FM](https://ai4fm.cs.luc.edu/papers/llm-tla-evaluation/) |
