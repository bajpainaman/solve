---
name: release-safety
description: "Plans how a release is checked in production: canary steps with automated analysis and rollback, SLO definitions with burn-rate alerts, synthetic probes, feature-flag rollouts, shadow traffic and a rollback runbook. Use for canary analysis, Argo Rollouts, progressive delivery, SLOs and error budgets, burn-rate alerts, synthetic monitoring, shadow or dark traffic, a rollback plan, \"how do we ship this safely\", or when the testing skill routes here. Not for tests that run before deploy."
---

# Release safety

A test suite can't see production data shapes or production load. Release safety is the set of checks that run on real traffic: a small share of users gets the new version, metrics decide whether it continues, and a bad version rolls back without a person in the loop.

This skill produces configs and runbooks. It changes no running system without the user's explicit agreement.

## It refuses to finish without

1. **Metrics that compare the canary with the stable version.** A fixed number passes or fails with the time of day. A comparison between two versions under the same traffic shows the effect of the release.
2. **At least one business KPI** beside error rate and latency, such as completed checkouts per minute. A version can return fast 200 responses and still break the product.
3. **A rollback that has been tried.** Name the command, the time it takes, and what happens to data the new version wrote.

When the user can't supply one of these, ask for it. Never fill it in with a guess.

## What it produces

| Artifact | Content |
|---|---|
| **Rollout config** | Canary steps with a traffic share and a pause for each, and analysis templates with success and failure conditions |
| **SLO definitions** | The indicator, the target and the window for each user journey, with alerts on fast and slow burn of the error budget |
| **Synthetic probes** | The journeys to probe every minute. Reuse the specs from `test-e2e`. |
| **Rollback runbook** | The trigger, the command, the verification, and how to handle data |

## Workflow

1. **Check the preconditions.** Progressive delivery needs metrics per version, a way to split traffic, and a rollback. When one is missing, plan that first and say that a canary without it ships bugs to a share of users.
2. **Define the SLOs** for the journeys that matter: the indicator, the target, the window.
3. **Write the rollout**: small first steps, such as 5%, 25%, 50% and 100%, with an analysis run at each pause.
4. **Write the analysis**: canary against stable for error rate, latency percentiles and the business KPI, with the number of failed measurements that triggers a rollback.
5. **Add the pre-deploy gates**: `can-i-deploy`, a migration dry run, and a check that enough error budget is left to ship.
6. **List the synthetic probes** and where they run.
7. **Write the rollback runbook**, and schedule a rehearsal.

## Choosing a technique

| Situation | Technique |
|---|---|
| Every deploy of a service with real traffic | Canary with automated analysis |
| A risky feature that must be easy to switch off | A feature flag with a progressive rollout |
| A rewrite whose output must match the old system | Shadow traffic with a diff of the responses |
| A journey that must work at 3 a.m. with no users | Synthetic probes |
| A decision on whether to ship at all today | An error-budget gate |

A canary rollback rate of zero over a long time can mean that the analysis is too lax. Review the conditions when no deploy has rolled back for months.

`${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` places these checks in the pre-deploy, canary and production stages.
