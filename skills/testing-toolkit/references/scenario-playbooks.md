# Scenario playbooks

The scenario decides the order of the skills and the definition of done. **Signal** is what to look for in the request or the diff. Run the skills in the order given, and stop only when the "Done when" column holds.

## Changing code

| Scenario | Signal | Playbook | Done when |
|---|---|---|---|
| **Bug fix** | An issue link, "fix", a stack trace | 1. `test-unit` or `test-integration`: write a test that reproduces the bug and fails on the current code. 2. Fix. 3. The test passes. 4. `test-mutation` on the diff. | The test failed before the fix and passes after it. No mutant survives on the changed lines. |
| **New feature in existing code** | A new endpoint, function or component | 1. `test-strategy`: pick the shape for this component. 2. Write tests from the spec at the right layer. 3. `test-quality-review` for diff coverage. 4. `test-mutation`, advisory. | Diff coverage meets the threshold. Every acceptance criterion has a test. |
| **Refactor with no behaviour change** | "refactor", "clean up", moved code | 1. Check that the current tests kill mutants in the area. If they don't, run `test-characterization` first. 2. Refactor. 3. Every pin still passes. 4. Optionally `test-property` with the old code as the oracle for the new code. | Pins or a differential test show the same observable behaviour. |
| **Legacy code with no tests** | Low coverage, no tests in the module | 1. Find seams. 2. `test-characterization` on untouched code. 3. `test-mutation` to show that the pins can fail. 4. Change the code. 5. Replace pins with real tests over time. | Pins are in place and have failed on mutants before any edit. |
| **Performance-sensitive change** | A hot path, a query change, caching | 1. Benchmark the baseline. 2. Change. 3. `test-load` smoke run with thresholds. 4. Scheduled stress or soak runs when the change is risky. | p95, p99 and throughput show no meaningful regression. |
| **Dependency or framework upgrade** | A lockfile change or a major version bump | 1. Full suite plus `test-contract` verification. 2. A differential test of key outputs, old against new. 3. Canary on deploy. | Contracts pass. Golden outputs show no difference. |
| **Security fix** | A CVE, auth, injection, input handling | 1. A regression test that exploits the bug. 2. Fix. 3. `test-fuzz` on the affected parser or handler. 4. A custom Semgrep rule that stops the bug from coming back. | The exploit test fails before the fix and passes after it. The rule runs in CI. |

## Building new things

| Scenario | Signal | Playbook | Done when |
|---|---|---|---|
| **Greenfield service** | A new repo or a service skeleton | 1. `test-strategy`: honeycomb for services, pyramid for libraries. 2. Install the CI stages. 3. `test-integration` with containers from the first day. 4. `test-contract` for every consumer. 5. `test-load` smoke run. 6. `release-safety` for canary and SLOs. | Every layer has at least one test, and CI runs every stage. |
| **New API endpoint** | A route or OpenAPI change | 1. Update the OpenAPI spec. 2. Run Schemathesis. 3. `test-integration` for business rules. 4. `test-contract` when consumers exist. 5. Schema-compatibility gate. | Fuzzing from the spec finds nothing. Contracts are verified. |
| **Service-to-service integration** | A new client of another service | 1. `test-contract`, consumer side. 2. Provider verification. 3. Fault tests with Toxiproxy: timeouts, 5xx, slow responses. 4. `can-i-deploy` gate. | The pact is verified. The failure modes have tests. |
| **Frontend feature** | A component or page change | 1. Component tests, trophy shape. 2. One `test-e2e` journey when the feature is critical. 3. Visual regression and accessibility checks. | Logic is covered by behaviour assertions and never by snapshots alone. |
| **Data pipeline or dbt model** | SQL, ETL, a schema change | 1. `test-data`: dbt unit tests on the transformation logic. 2. Schema and data tests. 3. A data diff against production. 4. Freshness and volume monitors. | Unit tests pass. Every row of the data diff has an explanation. |
| **LLM feature or prompt change** | A prompt, model or retrieval change | 1. `test-llm-evals`: golden set, deterministic checks, judge. 2. A red-team set for user-facing input. 3. Shadow or canary with eval sampling. | The regression pass rate is at or above the baseline. No new red-team failure. |
| **Database schema migration** | A migration file | 1. Run the migration on a snapshot of production size, and measure time and locks. 2. Old code against the new schema, and new code against the old schema. 3. Backfill test. 4. Rollback test. | Both version pairs pass. The migration time is measured. |

## Operating systems

| Scenario | Signal | Playbook | Done when |
|---|---|---|---|
| **Infrastructure or config change** | Terraform, Helm, k8s manifests | 1. IaC policy gate. 2. Plan review. 3. Canary or staged apply. 4. `chaos-experiment` when the change alters failure domains. | Policies pass. The staged rollout is healthy. |
| **Incident follow-up** | A postmortem action item | 1. A regression test that reproduces the trigger, at unit, integration or fault-injection level. 2. A `chaos-experiment` that recreates the failure. 3. SLO alert review. | The failure reproduces in CI or staging, and the system now handles it. |
| **Flaky-suite crisis** | Rising retry rates, people re-run CI until it passes | 1. `test-flaky-triage`. 2. Quarantine with an expiry date. 3. Fix the largest clusters first. | The flake rate is below the target the team agreed. |
| **Bootstrapping testing on a repo** | "Add tests to this repo" | 1. `test-strategy` audit of the current state. 2. CI stages. 3. `test-characterization` on the riskiest modules. 4. Diff-coverage gate for new code only. 5. Nightly mutation run. | New code is gated. Legacy debt is visible and does not block. |
| **Test-suite bloat** | A slow suite, test LOC that grows faster than production LOC, many tests added by agents | 1. `test-audit` campaign with a numeric target. The default removes 20% of tests, keeps coverage within 2 points, and keeps the mutation score. 2. Consolidate into table-driven or property tests. 3. One PR per batch, each with an evidence ledger. 4. Add the patterns found to AGENTS.md. | The target is met. Coverage and mutation score are within tolerance. The preservation review passed. |
