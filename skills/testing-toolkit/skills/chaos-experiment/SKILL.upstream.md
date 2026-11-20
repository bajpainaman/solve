---
name: chaos-experiment
description: "Plans a chaos or fault-injection experiment: the steady-state metric, a falsifiable hypothesis with a threshold and a time window, limits on blast radius, stop conditions, a rollback plan and the experiment definition for Chaos Mesh, Litmus, AWS FIS or Toxiproxy. Also plans disaster-recovery drills and game days. Use for chaos engineering, a chaos experiment, fault injection in staging or production, a game day, a DR drill, recreating an incident's failure, or when the testing skill routes here. Not for fault-injection tests inside a test suite (use test-integration)."
---

# Chaos experiments

A chaos experiment injects a failure into a running system to learn whether the system handles it. Without a hypothesis and a stop condition, the experiment is an outage that someone caused on purpose. This skill produces the plan and the experiment definition. It does not run anything against a shared environment without the user's explicit agreement.

## It refuses to finish without

1. **A steady-state metric tied to a real user journey**, such as the success rate of checkout requests. CPU load is not a steady state.
2. **A falsifiable hypothesis** with a threshold and a time window: "When one of three API pods is killed, checkout success stays above 99.5% and p99 stays under 800 ms during the 5 minutes that follow."
3. **Limits on blast radius**: which environment, which share of traffic or instances, and which customers are excluded.
4. **Stop conditions set before the run**, such as error-budget burn above a set rate or the steady-state metric below its threshold for one minute. Name the person or the automation that stops it.
5. **A rollback plan**: how the fault is removed, and how long that takes.

When the user can't supply one of these, ask for it. Never fill it in with a guess, and never produce a definition that can run without it.

## Workflow

1. **Pick the failure.** Take it from an incident, a dependency map, or the fault list: crash, network delay, packet loss, partition, dependency error, disk full, clock skew, zone loss.
2. **Fill the five items above** with the user.
3. **Choose the stage.** Start with Toxiproxy on a developer machine or a game day in staging. Move to scheduled automated runs in staging once several runs have passed. Suggest production only when SLOs, alerting and rollback all exist.
4. **Write the experiment definition** for the tool the team has, with the duration, the selector and the stop conditions in the definition itself.
5. **Write the run log template**: the time, the people present, each observation against the hypothesis, the result, and the follow-up actions.
6. **State the learning question**: what the team will do differently for each outcome.

## Output

```text
Experiment:    kill one of three api pods
Steady state:  checkout success rate, from the load balancer's metrics
Hypothesis:    success >= 99.5% and p99 <= 800 ms for 5 minutes after the kill
Blast radius:  staging, one pod, synthetic traffic only
Stop when:     success < 99% for 60 s, or the on-call engineer says stop
Rollback:      the deployment restores the pod; manual `kubectl rollout restart` in under 2 minutes
Result:        (filled in after the run) held / broken, with the evidence
Follow-up:     (filled in after the run)
```

A hypothesis that breaks is the useful result. Record it as a finding, and turn it into a regression test at the lowest layer that can reproduce it, usually a fault-injection test in `test-integration`.

## Disaster-recovery drills

A DR drill is an experiment with the same five items. Its steady state is the recovery objective: the time to restore, and the data that may be lost. Run a restore from backup into a clean environment each quarter, measure both numbers, and record them against the targets.
