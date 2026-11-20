---
name: test-audit
description: "Keeps a test suite as small as it can be while it still catches every credible regression. Three modes: a gate on each new test, an audit of named files, and a campaign with a numeric target across a subsystem. Finds dead, assertion-free, tautological, over-mocked, duplicate and implementation-coupled tests, and removes one only with an evidence ledger that names the stronger test that still covers the contract. Use for \"clean up these tests\", \"make the suite lean\", a slow or bloated suite, pruning tests an agent added, a test deletion that needs justification, or when the testing skill routes here. Not for fixing flaky tests (use test-flaky-triage)."
---

# Test audit

A test earns its place by catching a credible regression that no other test catches. Agents add tests easily, one per small change. This skill makes each test justify itself and removes the ones that don't.

## Three modes

| Mode | Trigger | Scope | Done when |
|---|---|---|---|
| **Gate** | An authoring skill is about to add or change a test | The new or changed tests in the diff | Each test answers the four gate questions, or is dropped |
| **Audit** | "Clean up these tests", a slow or noisy directory | Named files or one directory | A few high-confidence candidates, each with full evidence, are deleted in one batch and the validation passes |
| **Campaign** | "Make the suite lean", a numeric target, a quarterly schedule | A subsystem or the whole repo | The target is met or the ledger explains why not, coverage and mutation score are within tolerance, and the preservation review passed |

Every mode starts read-only. Collect the evidence before you edit anything.

## The gate

The four questions are step 0 of `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md`: which contract the test protects, which credible bug would make it fail, why no existing test already catches that bug, and whether it needs a hook in production code that no real caller uses.

## What counts as bloat

| Category | Example | Default action |
|---|---|---|
| Dead tests | Skipped, commented out, or testing a deleted source file | Delete |
| No real assertion | Calls the code and asserts nothing, or only "does not throw" | Delete, and report the real gap |
| Tautological | The expected value is computed by the code under test, or the test's own setup satisfies the assertion | Delete, or rewrite from the spec |
| Everything mocked | The module under test is mocked, or the mock implements the behaviour the test asserts | Delete, or move to an integration test |
| Duplicate contract | The same path, the same inputs and equivalent assertions | Keep the strongest owner, and delete the others |
| Near-duplicate examples | Ten tests that differ only in input values | Fold into one table-driven or property test |
| Coupled to implementation | Pins private call shapes, call counts or internal order that a public-boundary test already proves | Delete when the boundary test exists |
| Restated source | Greps for exact source strings, copied export lists, restated config flags | Delete, unless it guards a user-facing contract |
| Test-only seams in production code | Exports, globals or wrappers that only tests use | Delete the test and the seam |
| Snapshot bloat | Large snapshots of plain data or whole pages | Replace with targeted assertions, or delete |
| Fixture sprawl | The same setup copied across dozens of files | Consolidate into shared fixtures. No test is removed. |

## What never goes

- Never delete a test only because coverage stays the same without it.
- Keep every test that independently enforces a public API, protocol, config, migration, storage, security, access, platform-default or release contract.
- Keep guard tests that prove a check both passes and fails.
- A kept test that fails on the baseline may have found a product bug. Fix the code and leave the test.
- A slow test or a static test is not a candidate for that reason alone.

## Minimal-suite selection

Coverage alone is too weak a measure for pruning, because two tests can cover the same lines while only one checks the result. The campaign keeps the set of killed mutants constant.

1. **Build the evidence matrix.** For each test in scope, record the lines and branches it covers and the mutants it kills. Use per-test coverage contexts, such as `coverage run --contexts=test`, and a mutation tool that reports the killing tests per mutant.
2. **Find the tests with nothing unique.** A test with no uniquely covered branch and no uniquely killed mutant is a candidate.
3. **Choose the keepers.** Pick a small set of tests that together kill every mutant the full suite kills. A greedy set cover over the kill matrix does this. Break ties toward the test at the owning public boundary, then the deterministic one, then the fast one.
4. **Consolidate before you delete.** Fold near-duplicate examples into a table, and merge copied setup into shared fixtures.
5. **Apply "What never goes"** to every candidate before it enters the ledger.

## Evidence ledger

Write one row per candidate before any edit:

| Field | Content |
|---|---|
| Test | Name and location |
| Detects | The failure it can detect |
| Keeps alive | Non-test callers of anything it keeps alive |
| Covered by | The stronger test that still proves the same contract, by name |
| Unique | Unique coverage and unique mutant kills, which should both be zero |
| Risk | What could go wrong if this is a mistake |
| Validate | The command that shows the suite still passes |

## Campaign workflow

1. **Set a numeric target first.** An instruction to "clean up" ends too early without one. When the user gave none, propose this default: remove the least useful 20% of test declarations in scope, keep line and branch coverage within 2 points of the baseline, keep the mutation score on core modules at or above the baseline, and keep every retained test passing.
2. **Record the baseline**: test count, test LOC, suite runtime, line and branch coverage, and the mutation score on core modules.
3. **Discover read-only.** Build the evidence matrix and the ledger.
4. **Edit in batches**, one owner boundary per batch and one PR per batch. Each commit message lists what was removed and which retained test covers it.
5. **Measure again after each batch.** Revert a batch that breaks a tolerance.
6. **Preservation review.** A reviewer with fresh context, a person or a separate agent, checks that every security, contract and migration test survived.
7. **Report** tests and LOC removed, with test and production code counted separately, runtime saved, the coverage and mutation deltas, the candidates that were kept and why, and follow-ups.
8. **Prevent regrowth.** Propose additions to the repo's AGENTS.md or CLAUDE.md from the patterns this audit found.

## How this connects

- The deletion guard in `test-quality-review` blocks unexplained deletions and accepts deletions that come with this ledger.
- `test-mutation` supplies the kill matrix.
- Follow tests per killed mutant on core modules as the metric. A lean suite keeps it flat or falling as the codebase grows.
