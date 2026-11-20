---
name: fv-toolkit
description: "Settles correctness claims that tests cannot cover: whether a race, double charge, lost update, crash between writes, leaked permission or wrong-for-some-input calculation can ever happen. Picks and runs the cheapest checker (TLA+, Alloy, Hypothesis, Z3, Dafny, Kani, Shuttle, Stateright, Tamarin, Cedar, CrossHair, Schemathesis, Elle, XState, deterministic simulation, SQL equivalence) and keeps models in step with code. Use when a design or PR claims never, always, at most once or exactly once, or before recommending a formal tool. Not for ordinary unit tests, lint or type errors."
license: MIT
---

# Formal-verification toolkit

Vendored from [aasimsani/formal-verification-toolkit](https://github.com/aasimsani/formal-verification-toolkit) (MIT, see `LICENSE` and `NOTICE.md`) at the commit in `SOURCE`. Change it only through `bin/vendor-sync fv-toolkit` in the solve repository.

`TOOLKIT_ROOT` is the directory that contains this file. The upstream skills say `${CLAUDE_PLUGIN_ROOT}`; read that as `TOOLKIT_ROOT`. Where one says to load `fv-<tool>` with the Skill tool, read `TOOLKIT_ROOT/skills/fv-<tool>/SKILL.md`.

## Route

Always start with `skills/formal-verification/SKILL.md`. It triages the claims, and it says when no claim earns a formal check. Load one tool skill only after triage picks it:

| The claim is about | Tool skill |
|---|---|
| Orderings, retries, crashes, message loss, leases | `skills/fv-tlaplus/SKILL.md` |
| Shapes of data, permissions, tenancy, schemas | `skills/fv-alloy/SKILL.md` |
| A Python function over all inputs, stateful sequences | `skills/fv-hypothesis/SKILL.md` |
| Rule tables, policy diffs, pricing arithmetic | `skills/fv-z3/SKILL.md` |
| A small calculation core that needs a proof | `skills/fv-dafny/SKILL.md` |
| Rust arithmetic, panics, bounds | `skills/fv-kani/SKILL.md` |
| Rust threads and shared state | `skills/fv-shuttle/SKILL.md` |
| A Rust actor protocol | `skills/fv-stateright/SKILL.md` |
| An auth or key-exchange protocol under an attacker | `skills/fv-tamarin/SKILL.md` |
| Cedar authorization policies | `skills/fv-cedar/SKILL.md` |
| A Python function's docstring contract, old vs new | `skills/fv-crosshair/SKILL.md` |
| An OpenAPI service's real responses | `skills/fv-schemathesis/SKILL.md` |
| A recorded transaction history and its isolation level | `skills/fv-elle/SKILL.md` |
| An XState machine and its implementation | `skills/fv-xstate/SKILL.md` |
| A cluster under crashes and message loss | `skills/fv-dst/SKILL.md` |
| Two SQL queries that should return the same rows | `skills/fv-sqlequiv/SKILL.md` |
| A model that may have drifted from the code | `skills/fv-maintain/SKILL.md` |

`scripts/fv-install` downloads pinned checkers. Tell the user what it will fetch before the first run. A missing tool is "not checked", never a pass.

## Boundaries with neighbours

- Choosing *whether* to adopt a design is `solve` decide. This toolkit checks one design's claims and feeds the result in as evidence.
- Ordinary example-based tests are `testing-toolkit`.

## After the work

Offer the next step that fits: turn each counterexample into a regression test with `testing-toolkit`; render the verdicts for reviewers with `solve` make mode; or, when the check refuted the design, `solve` decide on the alternatives.
