# Pipeline: what runs where

Each stage has a time budget. A check moves to a later stage once it costs more than its stage allows. Mutation, fuzz and load steps run on the diff early and in full on a schedule. Unit, integration and E2E tests run on every change, and impact analysis trims them when the suite grows large.

This version of the plugin ships no workflow files. Write each stage for the repo's own stack and CI system from the table below, and add only the stages the repo is missing.

| Stage | Budget | Runs | Blocks merge or deploy? |
|---|---|---|---|
| **Pre-commit** hook | Under 30 s | Formatters, linters, type checks, secret scan, unit tests for touched files | Locally only |
| **PR, fast** | Under 10 min | Unit and integration tests, diff coverage, schema-compatibility checks, SAST, dependency scan, contract consumer tests, Schemathesis on changed endpoints, the small LLM eval set on prompt changes | Yes |
| **PR, extended**, in parallel | Under 30 min | Mutation testing on the diff, fuzzing of changed targets for about 10 minutes, E2E on critical paths, k6 smoke run, visual regression | Advisory first. Blocking on critical paths once the team trusts it. |
| **Main** | Under 30 min | Full unit and integration, the full E2E set, provider contract verification, benchmark comparison against the baseline | Blocks the deploy pipeline |
| **Nightly** | Hours | Full mutation run on core modules, batch fuzzing, load, stress and spike tests, flaky-test detection over history, the full LLM eval set and red-team set, DAST on staging, full dependency audit | Opens issues |
| **Weekly or scheduled** | Hours | Soak tests, chaos experiments in staging, DR restore drill, mutation score trend, `test-audit` campaign each quarter | Opens issues |
| **Pre-deploy** | Under 5 min | `can-i-deploy`, migration dry run, SLO error-budget check | Yes |
| **Deploy, canary** | 10 to 60 min | Progressive traffic with automated analysis, synthetic probes against the canary | Rolls back automatically |
| **Production** | Always on | Synthetic monitoring, SLO burn-rate alerts, invariant monitors, sampled LLM evals on live traffic | Pages a person |

## Gates that need no skill

These checks need no judgement once they are installed, so they are CI configuration.

| Gate | Tools | Notes |
|---|---|---|
| Test-impact selection | Bazel, Nx, pytest-testmon, Launchable | Always keep a periodic full run |
| Performance regression | Benchmarks compared with a stored baseline, k6 thresholds | Fail only on a slowdown that is statistically meaningful |
| Contract gate | `can-i-deploy` | Runs before every deploy |
| Schema compatibility | `buf breaking`, an OpenAPI diff, a migration linter | On the PR |
| SAST, secrets, dependencies, IaC | Semgrep, CodeQL, gitleaks, OSV-Scanner, Checkov | Judgement is needed only to write a custom Semgrep rule |

## Order of adoption

1. PR-fast with diff coverage.
2. Characterization tests on risky modules.
3. Nightly mutation run, advisory.
4. Contract gate.
5. Canary analysis.
6. Mutation on the PR as a blocking check on critical paths.
7. Chaos experiments and DR drills.

## Metrics

Follow the trend of each metric. Do not gate on an absolute value. Start with the first five.

| Metric | Measures | Healthy direction |
|---|---|---|
| Mutation score on changed code | Whether tests catch real behaviour changes | Up |
| Diff coverage | Whether new code carries its own tests | Stable at or above the team's threshold |
| Flake rate | Trust in the suite | Down |
| PR feedback time, p50 and p90 | Developer experience | Under the stage budget |
| Escaped defects, tagged by the layer that should have caught each one | What the tests missed | Down. Each one drives a new test and a playbook review. |
| Quarantine size and age | Hidden loss of coverage | Small, with nothing past its expiry |
| Time from postmortem to merged regression test | The learning loop | Short |
| Change failure rate | Release safety | Down |
| Canary rollback rate | Whether earlier stages catch problems | Low and above zero. Zero can mean that the canary analysis is too lax. |
| Eval regression pass rate | Stability of LLM features | At or above the baseline |
| Tests per killed mutant | How lean the suite is | Flat or down as the codebase grows |
