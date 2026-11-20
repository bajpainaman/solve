# Hypothesis anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Tool | Anti-pattern | Symptom | Fix / check | Source |
| --- | --- | --- | --- | --- |
| Hypothesis | Heavy `assume()` / filters | `Unsatisfied` or `filter_too_much` health check; few real cases | Build constrained strategies | [guide](https://helpmetest.com/blog/hypothesis-python-guide/) |
| Hypothesis | Weak property ("doesn't crash", or one fixed value) | Green suite, no bug-finding power | Round-trip, metamorphic, oracle, or invariant properties | [Tessl reference](https://tessl.io/registry/testland/hypothesis-testing/1.2.16/files/references/hypothesis-reference.md) |
| Hypothesis | Mocks inside the property | Property tests the mock | Real implementations or pure functions | same |
| Hypothesis | Testing properties the code never claims | False alarms | Only claimed properties; check callers for input domain | [Agentic PBT](https://arxiv.org/pdf/2510.09907) |
| Hypothesis | Random seed in CI, `.hypothesis/` not kept | Flaky, unreproducible failures | Fixed seed or `derandomize`; pin failures with `@example` | [Tessl](https://tessl.io/registry/testland/hypothesis-testing/files) |
| Any | LLM writes spec, runs checker once, reports success | Syntax passes, semantics wrong | Progressive, checker-in-the-loop generation; mutation checks; human review of properties | [AI4FM](https://ai4fm.cs.luc.edu/papers/llm-tla-evaluation/) |
