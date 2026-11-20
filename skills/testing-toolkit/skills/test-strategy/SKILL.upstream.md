---
name: test-strategy
description: "Plans how a repo or a feature should be tested. Picks a test shape per component (pyramid, trophy, honeycomb or diamond) from where that component's bugs are, names the skills that apply, lists the CI stages to install, and ranks the gaps by risk. Use for a test strategy, a test plan, \"how should we test this\", \"add tests to this repo\", bootstrapping testing or CI on a codebase, a greenfield service, an audit of existing tests, or when the testing skill routes here. Not for writing the tests themselves."
---

# Test strategy

This skill produces a plan and no test code. Its job is to make one decision explicit for every component: where would the bug be?

It refuses to finish without a named risk for each component. A shape with no risk behind it is a guess.

## Workflow

1. **List the components.** Read the repo layout, the entry points and the dependencies. A component is something that can break on its own: a module of rules, a service, a pipeline, a UI flow.
2. **Name the risk for each.** Ask where the bug is most likely if the component breaks: in its own logic, at a boundary with a DB, a queue or another service, or in the user flow. Use the history when it exists: past incidents, bug-fix commits and files that change often.
3. **Pick the shape** from `${CLAUDE_PLUGIN_ROOT}/references/strategy-models.md`. One repo usually holds more than one shape.
4. **Record what exists.** Count the tests per layer, note whether static analysis and types are on, and note which CI stages run. Measure coverage only as a map of untested areas.
5. **Rank the gaps by risk**: the chance that the bug happens, times the cost when it does. A critical component with no test at its risky layer ranks first.
6. **Name the skills and the CI stages.** For each gap, give the authoring skill that closes it. For the pipeline, give the stages from `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` that the repo is missing, in the order of adoption that file lists.
7. **Write the plan** in the format below, and ask the user to confirm the risks before any test is written.

## Output

| Component | Where the bug would be | Shape | Exists today | Gap | Skill | Rank |
|---|---|---|---|---|---|---|
| `pricing/` rules | Its own logic: boundaries of discount tiers | Pyramid | 4 unit tests, no boundary cases | Tier boundaries, rounding | `test-unit`, then `test-property` | 1 |
| `orders` service | The Postgres boundary: upserts and locks | Honeycomb | Unit tests with a mocked repository | No test runs real SQL | `test-integration` | 2 |
| Checkout flow | The user journey | Trophy plus one E2E | None | The paid-order journey | `test-e2e` | 3 |

Then list:

- **CI stages to add**, in order.
- **What not to test**, with the reason. Wiring with no logic, generated code and thin pass-through layers need no test of their own.
- **Open questions** for the user.

## Rules

- Turn on static analysis and types first. They are the bottom layer of every shape.
- Limit E2E tests to the few journeys whose failure would be an incident.
- For a repo with legacy code, gate new code with diff coverage and make the legacy debt visible. Never block merges on the legacy debt.
- When a component involves concurrency, distributed state, retries, permissions or rule tables, say that the `formal-verification` skill of the fv-toolkit plugin covers what tests can't.
