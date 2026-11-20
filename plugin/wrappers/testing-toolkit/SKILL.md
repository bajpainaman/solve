---
name: testing-toolkit
description: "Decides which tests a change needs and writes, audits or plans them: unit, integration, contract, E2E, characterization, data, property, fuzz, load, LLM evals, mutation, test review, flaky triage, suite pruning, chaos experiments and release safety. Use when asked to add or improve tests, choose a test strategy, review tests in a diff, prune a suite, or plan canaries, SLOs or game days. Not for running a suite once or debugging one failing test."
license: MIT
---

# Testing toolkit

Vendored from [aasimsani/testing-toolkit](https://github.com/aasimsani/testing-toolkit) (MIT, see `LICENSE`) at the commit in `SOURCE`. Change it only through `bin/vendor-sync testing-toolkit` in the solve repository.

`TOOLKIT_ROOT` is the directory that contains this file. The upstream skills say `${CLAUDE_PLUGIN_ROOT}`; read that as `TOOLKIT_ROOT`. Where one says to invoke `testing-toolkit:<name>` with the Skill tool, read `TOOLKIT_ROOT/skills/<name>/SKILL.md` instead.

## Route

Start with `skills/testing/SKILL.md` unless the request names one kind of test. It classifies the change and calls the others in order. Read one sub-skill at a time, only when the playbook reaches it.

| Need | Read |
|---|---|
| Kind of test not decided yet, "add tests for this change" | `skills/testing/SKILL.md` |
| A test plan or strategy for a repo or feature, no tests written yet | `skills/test-strategy/SKILL.md` |
| Pure logic from a spec | `skills/test-unit/SKILL.md` |
| Bugs at a database, cache, queue or filesystem boundary | `skills/test-integration/SKILL.md` |
| Two services or a client and an API keep breaking each other | `skills/test-contract/SKILL.md` |
| A user journey whose failure is an incident | `skills/test-e2e/SKILL.md` |
| Legacy code with no tests, before a refactor | `skills/test-characterization/SKILL.md` |
| dbt models, ETL and warehouse tables | `skills/test-data/SKILL.md` |
| Rules over a large input space, refactor equivalence | `skills/test-property/SKILL.md` |
| Parsers and code that read untrusted bytes | `skills/test-fuzz/SKILL.md` |
| Latency and capacity thresholds | `skills/test-load/SKILL.md` |
| Prompts, RAG chains, agents, model upgrades | `skills/test-llm-evals/SKILL.md` |
| "Do these tests catch anything?" on a diff | `skills/test-mutation/SKILL.md` |
| Review the tests in a PR | `skills/test-quality-review/SKILL.md` |
| Intermittent CI failures | `skills/test-flaky-triage/SKILL.md` |
| Shrink a bloated or agent-written suite | `skills/test-audit/SKILL.md` |
| Fault injection in staging or production, DR drills | `skills/chaos-experiment/SKILL.md` |
| Canaries, SLOs, burn-rate alerts, rollback plans | `skills/release-safety/SKILL.md` |

## Boundaries with neighbours

- A claim of "never", "always", "exactly once" or a race goes to `fv-toolkit`. A counterexample comes back here as a regression test.
- A whole-PR code review goes to `pr-review`. This toolkit reviews only the tests.
- One failing bug to reproduce goes to the host's debugging workflow, not here.

## After the work

End with one line that offers the next step that fits: `fv-toolkit` when the change makes a concurrency, retry or permission claim; `pr-review --local` before a push; `solve` make mode (`test-plan`-style page) when a reviewer needs the plan as a page.
