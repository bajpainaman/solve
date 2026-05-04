# Productive Thinking Model (Tim Hurson)

**Phase:** Define · **Source:** https://untools.co/productive-thinking-model

The Productive Thinking Model is a 6-step backbone that runs through every Define phase. It provides the spine that other Define frameworks plug into. Where Zwicky enumerates options and Issue Tree decomposes the problem, Productive Thinking forces the team to answer a complete question set: what is happening, what does success look like, what is the right question to ask, what are the candidate answers, which forged solutions survive, and what resources ship them. Skip any step and the decision pipeline is missing a load-bearing input.

This is not a generative framework in the same way Zwicky is. It is a checklist. Its value is catching the missing piece. Most teams handle steps 1-2 and 4-5 well. They skip step 3 (the question itself, often the hardest step) and step 6 (resources, often the most boring) and ship a confident wrong answer to the wrong question with no plan.

---

## Entry Predicate

```
always_run
```

Productive Thinking runs in every Phase 1 (Define) execution. There is no condition under which it is skipped. The 6-step output is the canonical Define-phase summary that all subsequent frameworks reference.

### Inputs

- `intake.problem_refined` — the canonical problem statement; feeds step 1 (what's going on) and validates step 3 (the question)
- `intake.success_criteria` — feeds step 2 (what does success look like)
- `frameworks/abstraction-ladder.md::target_rung` — sets the rung at which the question (step 3) lives
- `frameworks/zwicky-box.md::archetypes` — feeds step 4 (candidate answers, divergent)
- `frameworks/conflict-resolution-diagram.md::new_option_D_double_prime` — adds to candidate answers if CRD evaporated
- `frameworks/issue-tree.md::leaves` — provides decomposition that informs candidate answers
- `frameworks/first-principles.md::atomic_truths` — constrains forged solutions (step 5)
- `frameworks/inversion-define.md::failure_modes` — informs the resource plan (step 6) by surfacing dependencies that prevent failure
- `evidence/define-prior-art.md` — informs both candidate generation and resource estimation

### Outputs

- `$RUN_DIR/frameworks/productive-thinking.md` — the 6-step output
- `state.json` `productive_thinking.question` — the canonical question that downstream frameworks must answer
- `state.json` `productive_thinking.forged_solutions` — the 2-3 forged solutions consumed by Decision Matrix as the option-set anchor
- `state.json` `productive_thinking.resource_plan` — consumed by Eisenhower (urgency) and Impact-Effort (effort)

---

## Operating Principles

These five rules are non-negotiable. Each shapes a specific step of the 6-step process.

**1. Step 1 (what's going on) must be evidence-grounded, not a story.**

The "what's going on" answer must cite specific events, metrics, or observable phenomena. "We have a migration to consider" is a story. "OFTv1 is deployed on 4 chains with $12M TVL; LayerZero has shipped OFTv2 with documented gas savings and a different message-encoding scheme; we have not yet evaluated migration paths" is grounded. The grounding lets every subsequent step build on real signal. Anti-pattern: step 1 as narrative; downstream frameworks reproduce the narrative without testing it.

**2. Step 2 (success criteria) must be measurable or explicitly qualitative.**

If success is measurable, name the metric and the threshold. If success is qualitative, name the observable signal that would tell you it happened. "Successful migration" is neither; it is a label. "Migration completes within 8 weeks, < 0.1% TVL loss, no audit blowback, ops on-call load no greater than baseline" is measurable. "Team reports the migration as smooth and users report no confusion in the support channel" is qualitative-explicit. Anti-pattern: success criteria written as "we want it to go well," which provides no signal for the Decision Matrix to score against.

**3. Step 3 (the question) is the hardest and most under-invested step.**

Most teams skip step 3 because they assume the question is the original ask. It rarely is. The original ask is "should we migrate to OFTv2?" The right question, after step 1 evidence and step 2 success criteria, is often "which migration archetype best balances reversibility against gas-savings capture, given $12M TVL and quarter-end audit constraints?" The right question is more specific, names the trade-off, and excludes the meta-question (whether to migrate at all may have been answered yes by step 1 evidence). Anti-pattern: step 3 is the original ask copy-pasted; downstream frameworks answer the wrong question precisely.

**4. Step 4 (divergent answers) requires breadth before convergence.**

The framework requires ≥ 7 candidate answers. Fewer than 7 means the team converged early and missed the unexpected option. Sources for candidates: Zwicky archetypes (typically 4-7), CRD's evaporated option (if any), inversions of the obvious answer (the answer that does the opposite), the do-nothing answer (always include), the answer from analogous prior art. Anti-pattern: 3 obvious answers + 1 conservative variant; the divergence step did no work.

**5. Step 5 (forged solutions) names trade-offs explicitly.**

The forged solutions are the 2-3 candidates that survive convergent analysis. Each one names its strengths, its risks, and the specific atomic-truth or first-principle it relies on. Forging is not picking favorites; it is selecting candidates that pass first-principles tests and have non-overlapping strengths. Anti-pattern: 2 forged solutions that are minor variants of each other; the matrix later cannot distinguish them.

---

## Response Posture

**Tone.** Clinical. The framework is a checklist that catches missing pieces. The agent's job is to surface gaps, not to advocate.

**Pacing.** Sequential. Each step depends on the prior step's output. Do not parallelize across steps. Within a step, parallelize across candidate generation (step 4) by fanning out brief subagent calls.

**Push depth.** Push hard on step 3 (the question). Most teams answer the wrong question precisely; the agent's job is to catch that. Push moderately on step 2 (success criteria); accept qualitative-explicit but push back on label-only criteria. Push lightly on steps 1, 4, 5; the input from prior frameworks already makes them robust. Push hard again on step 6; resource plans are skipped almost universally.

**Where to escalate.** SendMessage to lead when:
- Step 1 evidence contradicts intake.problem_refined (the team's framing is at odds with the evidence; possibly re-route to abstraction-ladder)
- Step 3 question cannot be agreed upon (the team is solving multiple problems under one banner; recommend splitting the run into two /solve invocations)
- Step 6 resource plan reveals the decision is infeasible at any chosen archetype (trigger CSO-style review, or recommend reducing scope before continuing)

---

## Anti-Sycophancy Rules

The agent running Productive Thinking must never write these:
- "The current state involves a complex set of factors..." (cite the specific evidence)
- "Success could mean different things to different people..." (pin the criterion or mark it as qualitative-explicit with an observable signal)
- "The right question is an interesting consideration..." (state the question; if you cannot, escalate)
- "Many candidate answers come to mind..." (list them; ≥ 7)
- "Resource needs vary by approach..." (give the resource plan per forged solution)

The agent must always:
- Take a position on the canonical question (step 3) and require the team to confirm or restate.
- Cite the source for each candidate answer (Zwicky archetype N, CRD D'', inversion of obvious, etc.).
- Name the resource bottleneck (the limiting factor in step 6) if there is one.
- State which forged solution dominates which other on a specific criterion, and which trade-offs remain.

---

## Pushback Patterns

These are the most common errors when teams run Productive Thinking. The agent applies these self-checks.

**Pattern 1: step 1 as narrative**

- User input: "What's going on: we have a migration on our hands."
- BAD: "Captured."
- GOOD: "That is a label, not evidence. Step 1 needs the specific phenomena. Reading intake.problem_refined and prior-art evidence: OFTv1 is deployed on Ethereum, Avalanche, Arbitrum, Base with $12M TVL combined; OFTv2 was released with documented 30% gas savings and message-encoding changes; we have not yet evaluated migration paths. The phenomena are: existing deployment, new option from LayerZero, no internal evaluation. State this evidentially."

**Pattern 2: success as label**

- User input: "Success: migration goes well."
- BAD: "Success defined."
- GOOD: "That is a label. intake.success_criteria = qualitative-signal, so we cannot demand a metric, but we can demand an observable signal. What does 'goes well' look like in the support channel after week 1? In the on-call rotation during week 2-4? In the audit conversation at year-end? Pin three specific observable signals or this step does no work."

**Pattern 3: step 3 as the original ask**

- User input: "The question is: should we migrate to OFTv2?"
- BAD: "Question captured."
- GOOD: "That is the original ask. Step 1 evidence has likely already answered the meta-question (migration is on the table; the only question is how, not whether). The real question, given evidence and success criteria, is: 'which migration archetype best balances reversibility against gas-savings capture, given $12M TVL, quarter-end audit constraints, and the need to maintain bridge integrity across all 4 chains?' That is the question Decision Matrix will answer. Confirm or restate."

**Pattern 4: step 4 too narrow**

- User input: "Candidate answers: migrate now, defer to Q3, do nothing."
- BAD: "Three candidates noted."
- GOOD: "Three candidates is below the floor of 7. Add at least: (4) phased migration leader-chain-first; (5) wrapped legacy; (6) separate token + voluntary migration; (7) inversion of obvious (deploy OFTv1.5 with gas optimizations and never migrate to v2); (8) the CRD evaporation if applicable. The convergent step (5) cuts down to 2-3, but it cannot cut from 3 candidates and produce signal."

**Pattern 5: step 6 absent or vague**

- User input: "Resources: we have a small team."
- BAD: "Got it."
- GOOD: "Step 6 needs specifics per forged solution. For each forged solution: (a) people, name the roles needed and weeks of effort; (b) time, the calendar duration including dependencies; (c) decisions, who must approve at each milestone; (d) capital, dollars or audit cycles consumed. If you cannot complete step 6 for a forged solution, that solution is too vague to forge; re-run step 5."

---

## Method

Productive Thinking runs as a 6-step procedure. Each step has a defined output and a failure mode for skipping.

### Step 1, What's going on

Read `intake.problem_refined` and `evidence/define-prior-art.md`. Write 3-7 bullet points describing the current state: what is true now, what is changing, who feels the pain, what observable phenomena prove this is a real problem rather than a hypothetical concern.

Output type: bullet list with citations.

Failure mode of skipping: downstream frameworks reproduce the team's framing without grounding; if the framing is wrong, every framework after this is wrong.

### Step 2, What is success

Read `intake.success_criteria`. If measurable-metric: name the metric, the threshold, and the measurement window. If qualitative-signal: name the observable signal, where it appears (channel, dashboard, conversation), and the time horizon. If can't-articulate: halt and recommend re-running intake or running an abstraction-ladder pass before continuing.

Output type: 2-5 bullet points each with metric/threshold or signal/source.

Failure mode of skipping: Decision Matrix downstream cannot score against criteria; scores become arbitrary.

### Step 3, The question

Re-read step 1 evidence and step 2 success criteria. Identify the implicit meta-question already answered (often the should-we vs how-to). State the canonical question that, if answered, drives the decision. The question must be:
- Specific enough that two readers extract the same intent
- Trade-off-naming (the question references the dimension that splits the candidates)
- Bounded (excludes meta-questions already answered by step 1 evidence)

Output type: one-sentence canonical question.

Failure mode of skipping: subsequent frameworks answer the original ask, which is often the wrong question. Decision Matrix produces a confident answer to a wrong question.

### Step 4, Generate candidate answers (divergent)

Source candidates from:
- `frameworks/zwicky-box.md::archetypes` (typically 4-7 named archetypes)
- `frameworks/conflict-resolution-diagram.md::new_option_D_double_prime` (if CRD evaporated)
- Inversions of the obvious answer (what would doing the opposite look like?)
- The do-nothing answer (always include)
- Analogous prior art (what did similar teams do that we have not considered?)

Aim for ≥ 7 candidates. Fewer than 7 means the divergence step did insufficient work; re-run with broader sourcing.

Output type: numbered list with one-sentence description per candidate.

Failure mode of skipping: convergent step (5) operates on 2-3 obvious candidates and the unexpected option never enters the Decision Matrix.

### Step 5, Forge the solutions (convergent)

Apply the convergent filter to the candidate list:
- Cut candidates that violate first-principles atomic truths (cite which truth)
- Cut candidates that trigger inversion-define failure modes without mitigation (cite which mode)
- Cut candidates that have zero documented prior art and high novelty risk (unless intake.reversibility = cheap, which makes novelty acceptable)
- From the remaining candidates, select 2-3 that have non-overlapping strengths (a candidate that wins on speed, a candidate that wins on reversibility, etc.)

For each forged solution:
- Strengths: 2-3 bullet points
- Risks: 2-3 bullet points
- Atomic-truth alignment: which first-principles truth this solution leans on
- Prior-art reference: a real-world system that ran this solution

Output type: structured list of 2-3 forged solutions.

Failure mode of skipping: Decision Matrix has no clear option-set anchor; falls back on Zwicky archetypes raw without convergent filtering.

### Step 6, Align resources

For each forged solution, write a resource plan:

```markdown
**Forged solution N: <name>**
- People: <roles + weeks of effort + critical-path dependencies>
- Time: <calendar duration + key dependency milestones>
- Decisions: <decisions needed and decision-maker per milestone>
- Capital: <dollars + audit cycles + external services>
- Bottleneck: <the one thing that is most likely to slip>
```

Output type: structured resource plan per forged solution.

Failure mode of skipping: Eisenhower (urgency) and Impact-Effort (effort) frameworks downstream cannot score effort; scores become arbitrary or default to medium-medium.

### Step 7 (administrative), Write output and update state

Write `$RUN_DIR/frameworks/productive-thinking.md` per the Output Schema. Update `state.json`:

```json
{
  "productive_thinking": {
    "question": "<canonical question text>",
    "candidate_count": 8,
    "forged_solutions": ["dual-deploy+drain", "wrapped-legacy", "phased-cutover-leader-chain"],
    "forged_count": 3,
    "resource_bottleneck": "audit-team-availability-Q3",
    "completeness": 9
  }
}
```

Decision Matrix and Eisenhower read from this state.

---

## Question Patterns

Productive Thinking interacts with the user at three points (steps 2, 3, 6); the rest is analytical synthesis from prior frameworks.

### Question 1, Confirm success criteria specificity (step 2)

> "intake.success_criteria = <value>. I propose the following observable signals as the operational definition: <list>. Confirm, refine, or replace."

Good answer shape: confirmation or specific replacement. Red flag: "those look fine but let's keep it flexible"; flexibility kills downstream scoring.

Smart-skip: if intake.success_criteria = measurable-metric and the metric is named in `intake.problem_refined`, skip the question.

### Question 2, Confirm the canonical question (step 3)

> "The original ask was: <text>. Based on step 1 evidence, the meta-question (X) appears already answered. The canonical question that drives the decision is: <text>. Confirm, refine, or restate."

Good answer shape: confirmation, or a restatement that names a different trade-off. Red flag: "let's just answer the original question"; this often means the team has not internalized step 1 evidence.

### Question 3, Confirm resource bottleneck (step 6)

> "For each forged solution, the resource plan identifies a bottleneck: <list>. The dominant bottleneck across solutions is: <X>. Confirm or restate."

Good answer shape: confirmation. Red flag: "all the bottlenecks look manageable"; this often means the user has not run the resource plan against actual calendar dates.

Smart-skip: if `intake.time_pressure = no-deadline` and `decision_maker = you-alone`, the resource bottleneck rarely changes the recommendation; ask only if the team has multi-stakeholder commits.

---

## Forcing Exemplars

The four major Productive Thinking outputs each have softened and forcing versions.

### Exemplar 1, Stating step 1 (what's going on)

SOFTENED (avoid):
> "We are evaluating a potential migration."

FORCING (aim for):
> "OFTv1 is deployed on Ethereum, Avalanche, Arbitrum, Base. Combined TVL is $12M. LayerZero shipped OFTv2 in [date] with documented 30% gas savings on bridge transactions and a different message-encoding scheme that breaks backward compatibility at the wire level. We have not yet evaluated migration paths. Three competitor protocols (Stargate, Radiant, Ethena) have already migrated. Our internal team has migrated 1 prior LayerZero deployment ($500K TVL, single-chain). No incident on OFTv1 in the last 6 months."

### Exemplar 2, Stating step 3 (the question)

SOFTENED (avoid):
> "The question is whether to migrate."

FORCING (aim for):
> "Canonical question: which migration archetype best balances reversibility against gas-savings capture, given $12M TVL, quarter-end audit constraints, and the requirement to maintain bridge integrity across all 4 chains within an 8-week window? The meta-question (whether to migrate at all) is answered yes by step 1 evidence: OFTv1 will increasingly diverge from competitor protocols on message-encoding compatibility, and the gas-savings opportunity is large. The remaining question is the how, not the whether."

### Exemplar 3, Forging a solution (step 5)

SOFTENED (avoid):
> "Dual-deploy + drain seems strong."

FORCING (aim for):
> "Forged solution 1: dual-deploy + drain.
> Strengths: matches established LayerZero migration pattern (Stargate USDC, Radiant v1-to-v2, Ethena USDe); rollback envelope is the dual-rail period (4-8 weeks); zero forced cutover for users; gas-savings begin immediately upon deployment.
> Risks: ops complexity during dual-rail (ops needs to monitor 2 contracts per chain × 4 chains = 8 monitoring surfaces); drain incentive design must be calibrated (too high incentive overspends; too low extends the dual-rail period and increases ops cost).
> Atomic-truth alignment: relies on first-principles atomic-truth-3 (users must not lose funds), which dual-deploy explicitly preserves.
> Prior art: Stargate USDC migration ran 6 weeks dual-rail with successful 99%+ migration; Radiant v1-to-v2 ran 8 weeks; Ethena USDe similar."

### Exemplar 4, Resource plan (step 6)

SOFTENED (avoid):
> "Resources: standard team, a few weeks."

FORCING (aim for):
> "Resource plan for forged solution 1 (dual-deploy + drain):
> People: 1 lead engineer (4 weeks development + 8 weeks dual-rail oversight), 1 ops engineer (1 week setup + 8 weeks dual-rail monitoring), 1 auditor (2 weeks delta-audit on OFTv2 contracts before deployment), 0.25 PM (8 weeks coordination).
> Time: 14 calendar weeks total (2 weeks audit, 4 weeks development overlap with audit, 8 weeks dual-rail and drain). Cutover window: weeks 12-14.
> Decisions: lead engineer signs off on deployment readiness (week 4); auditor signs off on contract security (week 6); PM signs off on user-comms plan (week 6); CTO signs off on cutover (week 12).
> Capital: $30K audit cost, $40K estimated drain incentive, $15K ops monitoring tools, total ~$85K hard cost.
> Bottleneck: audit-team availability in Q4. The auditor is booked for year-end audits and can only allocate 2 weeks delta-audit time. If we miss the Q4 slot, the next available slot is Q1 (delays migration by 8 weeks). This is the limiting factor."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/productive-thinking.md` follows this exact structure.

### Section A, Header

```markdown
# Productive Thinking, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** intake.json, abstraction-ladder.md, zwicky-box.md, conflict-resolution-diagram.md, issue-tree.md, first-principles.md, inversion-define.md, evidence/*
**Status:** complete | partial-pending-question-confirmation | partial-pending-resource-plan
```

### Section B, Step 1: What's going on

```markdown
## 1. What's going on

- <bullet 1 with citation>
- <bullet 2 with citation>
- <bullet 3 with citation>
- <bullet 4 with citation>
- <bullet 5 with citation>

**Source:** intake.problem_refined, evidence/define-prior-art.md, frameworks/issue-tree.md
```

### Section C, Step 2: What is success

```markdown
## 2. What is success

| Criterion | Type | Threshold/Signal | Measurement window |
|---|---|---|---|
| <name> | metric | <threshold> | <window> |
| <name> | signal | <observable> | <window> |
| <name> | metric | <threshold> | <window> |
```

### Section D, Step 3: The question

```markdown
## 3. The question

**Canonical question:** <text>

**Why this and not the original ask:** <rationale referencing step 1 evidence and step 2 success criteria>

**Trade-off named in the question:** <which dimension splits the candidates>
```

### Section E, Step 4: Candidate answers (divergent)

```markdown
## 4. Candidate answers

| ID | Candidate | Source |
|---|---|---|
| 1 | <name> | zwicky-box archetype 1 |
| 2 | <name> | zwicky-box archetype 2 |
| 3 | <name> | zwicky-box archetype 3 |
| 4 | <name> | zwicky-box archetype 4 |
| 5 | <name> | CRD evaporated D'' |
| 6 | <name> | inversion (do the opposite of obvious) |
| 7 | <name> | do-nothing baseline |
| 8 | <name> | analogous prior art (e.g. Compound v3 pattern) |
```

Minimum 7 candidates.

### Section F, Step 5: Forged solutions (convergent)

```markdown
## 5. Forged solutions

### Forged 1: <name>
- **Strengths:** <bullets>
- **Risks:** <bullets>
- **Atomic-truth alignment:** <which first-principle this leans on>
- **Prior art:** <reference>

### Forged 2: <name>
- ...

### Forged 3: <name>
- ...

**Cuts (candidates not forged):**
| Candidate | Cut reason |
|---|---|
| <id, name> | <which atomic-truth or failure-mode caused the cut> |
```

### Section G, Step 6: Align resources

```markdown
## 6. Resource plan

| Forged solution | People | Time | Decisions | Capital | Bottleneck |
|---|---|---|---|---|---|
| <name 1> | <roles + weeks> | <weeks> | <list> | <$> | <text> |
| <name 2> | <roles + weeks> | <weeks> | <list> | <$> | <text> |
| <name 3> | <roles + weeks> | <weeks> | <list> | <$> | <text> |

**Dominant bottleneck across all forged solutions:** <text>
```

### Section H, Decision Matrix handoff

```markdown
## Decision Matrix Handoff

The forged solutions become the option-set anchor for Decision Matrix. The candidate list (step 4) is preserved as a fallback for re-scoring if Decision Matrix's forged-only run produces a tie.

Suggested criteria for Decision Matrix derived from forged-solution trade-offs:
- <criterion 1>
- <criterion 2>
- <criterion 3>

Resource bottleneck flag for Eisenhower: <text>
```

### Section I, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentences on what the 6-step output implies for the recommendation. Specific, decision-actionable.>
```

### Section J, Completeness Score

```markdown
**Completeness:** <N>/10
```

---

## Decision Hook

Productive Thinking's output drives every subsequent framework. Specifically:

### Per-step downstream consumption

| Step | Output | Downstream consumer |
|---|---|---|
| 1 | What's going on | All frameworks reference for grounding |
| 2 | Success criteria | Decision Matrix as criteria; Confidence-Speed-Quality as quality definition |
| 3 | The question | Every framework answers this question; if framework's output does not bear on this question, framework is misaligned |
| 4 | Candidate answers | Decision Matrix as the option-set superset (forged solutions are the anchor; candidates are the fallback) |
| 5 | Forged solutions | Decision Matrix as the option-set anchor (2-3 options) |
| 6 | Resource plan | Eisenhower (urgency from time column); Impact-Effort (effort from people + capital columns) |

### Confidence rubric impact

- Productive Thinking complete with all 6 steps grounded in evidence: +1 to overall confidence
- Step 3 question explicitly differs from original ask and is justified by step 1 evidence: +1 to overall confidence
- Step 6 resource plan identifies a bottleneck that the lead acknowledges: 0 to confidence (the bottleneck does not change confidence in the decision; it changes scheduling)
- Step 6 missing or generic: -1 to overall confidence (the team has not internalized the cost)

### Override conditions

Productive Thinking does not override other frameworks; it provides the spine. The spine can suppress a framework's output:
- If step 5 forged solutions cut a Zwicky archetype, that archetype is removed from Decision Matrix (the forging step is authoritative)
- If step 6 resource plan reveals a forged solution is infeasible (resource bottleneck has zero slack), the solution is downgraded in Decision Matrix even if it scores high on other criteria

---

## Cross-Framework Triggers

Specific Productive Thinking outputs trigger downstream actions or skill handoffs.

- Step 3 canonical question explicitly differs from original ask AND the difference suggests pre-product uncertainty (the team is asking "should we exist" rather than "how to ship"), trigger `/office-hours` handoff at end of run
- Step 6 resource bottleneck is "audit-team-availability" or "external-vendor-availability" (capacity outside team control), flag for Eisenhower as urgent-important and recommend pre-booking
- Step 5 forges a solution with no documented prior art (novel architecture), flag for `/plan-eng-review` at end of run
- Step 1 evidence reveals the team is conflating two problems under one banner, halt and recommend splitting into two /solve invocations
- Step 5 forged solutions are 2 minor variants of a single archetype, halt and recommend re-running step 4 with broader sourcing

---

## Failure Modes

Productive Thinking misleads in five distinct ways. The framework runs each self-check.

### Failure Mode 1, Step 1 narrative not evidence

Trap: Step 1 reads like a story rather than a list of grounded phenomena. Subsequent steps reproduce the narrative without testing it.

Manifestation: step 1 contains adjectives ("complex," "challenging") and emotive verbs but no specific metrics, dates, or events.

Check: each bullet in step 1 must cite a source (intake field, evidence file, prior framework). Bullets without sources are removed.

Recovery: re-run step 1 with explicit sourcing requirement. Often the sources exist but were not cited; this is a 10-minute fix.

### Failure Mode 2, Step 3 is the original ask

Trap: The team writes the canonical question as the original ask, missing the meta-question already answered by step 1 evidence.

Manifestation: question contains "should we" or "is it worth"; the answer would change Phase 3's framing fundamentally if the meta-question were re-opened.

Check: the canonical question must reference a specific trade-off dimension and exclude meta-questions. If step 1 evidence answers a meta-question, the canonical question must build on that answer, not re-litigate it.

Recovery: re-run step 3 with the explicit instruction to identify the meta-question and exclude it. The lead must confirm.

### Failure Mode 3, Step 4 too narrow

Trap: The candidate list is 3-4 obvious answers without divergent breadth. Convergent step (5) cannot do work because there is nothing to filter.

Manifestation: step 4 has fewer than 7 candidates, or all candidates are minor variants of one archetype.

Check: candidate count ≥ 7 AND candidates span ≥ 3 distinct archetypes. If both fail, re-run.

Recovery: re-run step 4 with explicit broader sourcing (Zwicky + CRD + inversion + do-nothing + analogous prior art).

### Failure Mode 4, Step 5 forges variants of one solution

Trap: The 2-3 forged solutions are minor variants (e.g. dual-deploy with 4-week drain, dual-deploy with 6-week drain, dual-deploy with 8-week drain). Decision Matrix cannot distinguish them; scores collapse.

Manifestation: forged solutions share an archetype root and differ only in parameters.

Check: each forged solution must come from a distinct archetype (or distinct strategic shape). Variants of one archetype merge into a single forged solution.

Recovery: re-run step 5 with the constraint that each forged solution must represent a distinct archetype. If the team can only forge 2 distinct archetypes, that is fine; do not pad with variants.

### Failure Mode 5, Step 6 absent or boilerplate

Trap: Resource plan is "1-2 weeks, small team" for every forged solution. Eisenhower and Impact-Effort downstream score arbitrary.

Manifestation: step 6 cells have no specifics; bottleneck cell is empty or "depends."

Check: each forged solution's resource plan must have specific numbers (weeks, dollars, named roles) and a named bottleneck. Generic resource plans are rejected.

Recovery: re-run step 6 with the explicit requirement to write per-solution resource plans. If the team genuinely cannot estimate, that is itself a finding (the decision is premature) and should escalate to the lead.

---

## Jargon Glossary

- step 1, the "what's going on" diagnosis; the evidence-grounded current state.
- step 2, the success definition; metric or qualitative-explicit signal.
- step 3, the canonical question; the question whose answer drives the decision.
- step 4, divergent answer generation; ≥ 7 candidates.
- step 5, convergent forging; 2-3 forged solutions with non-overlapping strengths.
- step 6, resource alignment; per-solution resource plan and dominant bottleneck.
- meta-question, a question that step 1 evidence already answers; should be excluded from the canonical question.
- forged solution, a candidate that survived convergent filtering and has explicit strengths, risks, atomic-truth alignment, and prior art.
- divergent step, the breadth phase of generating candidates.
- convergent step, the rigor phase of cutting candidates.
- canonical question, the single sentence that step 3 produces; the question every downstream framework answers.
- candidate, a possible answer surfaced in step 4; not all candidates become forged solutions.
- bottleneck, the resource constraint that is most likely to slip; named per forged solution.
- Hurson, Tim Hurson, the originator of the Productive Thinking model; alternate name for the framework.
- spine, the role Productive Thinking plays in Phase 1; the structural backbone other Define frameworks plug into.

---

## Completeness Scoring

The Productive Thinking output self-rates 0-10 based on this rubric.

### 10/10, Decisive spine

- Step 1: 5+ bullets, every bullet sourced
- Step 2: 3+ criteria, each with metric/threshold or signal/source/window
- Step 3: canonical question explicitly different from original ask, meta-question identified and excluded, trade-off dimension named
- Step 4: ≥ 7 candidates, span ≥ 3 distinct archetypes, each candidate sourced
- Step 5: 2-3 forged solutions, each from a distinct archetype, each with strengths/risks/atomic-truth/prior-art filled
- Step 6: per-solution resource plan with specific numbers, dominant bottleneck named
- Cross-framework triggers checked
- No failure-mode self-checks fail

### 7/10, Useful spine

- All 6 steps complete, most with cited sources
- Step 3 question differs from original ask but trade-off dimension is implicit
- Step 4 has 7-8 candidates spanning 2-3 archetypes
- Step 5 forges 2-3 solutions, mostly distinct (1 may be a variant)
- Step 6 has resource plans, bottleneck named for 2 of 3 solutions

### 4/10, Tentative spine

- Steps 1-2 grounded; step 3 question is the original ask
- Step 4 has 5-6 candidates, mostly minor variants
- Step 5 forges 2 solutions of similar archetype
- Step 6 generic ("small team, 4 weeks") without per-solution differentiation

### 0/10, Untrustworthy

- Step 1 narrative without sources
- Step 2 label-only success criteria
- Step 3 missing or copy of original ask
- Step 4 has < 5 candidates
- Step 5 forges 1 solution (no convergent filter visible)
- Step 6 absent or boilerplate

The completeness score appears in the Productive Thinking output. A completeness ≤ 4 caps overall confidence at MEDIUM and triggers a re-run recommendation.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This is the canonical example. Productive Thinking runs the 6-step backbone for this problem.

### Intake state going in

```json
{
  "problem_refined": "We have an OFTv1 token deployed on 4 chains (Ethereum, Avalanche, Arbitrum, Base) with $12M TVL. LayerZero released OFTv2 with better gas, security improvements, and a different message-encoding scheme. Should we migrate?",
  "stakeholders": "small-team",
  "time_pressure": "this-month",
  "reversibility": "costly",
  "decision_maker": "you-with-input",
  "success_criteria": "qualitative-signal",
  "domain": "eng"
}
```

### Prior framework outputs consumed

- abstraction-ladder, target rung is "decide migration approach"
- first-principles, atomic truths: bridges must allow value transfer, gas costs must be predictable, users must not lose funds, message encoding must be backward-compatible during dual-rail period
- issue-tree, branches: technical migration mechanism, user-side coordination, audit requirements, operational runbook
- inversion-define, failure modes: partial migration with frozen funds, double-spending across chains during transition window, UX confusion at the cutover moment, audit timeline slip blocking deploy
- zwicky-box, archetypes: dual-deploy + drain, wrapped legacy, phased cutover with leader chain, separate token + voluntary migration
- conflict-resolution-diagram, evaporated D'': deploy this month, dual-rail through year-end, cutover Q3

### Step 1, What's going on

- OFTv1 is deployed on Ethereum, Avalanche, Arbitrum, Base; combined TVL is $12M. (intake)
- LayerZero shipped OFTv2 with documented 30% gas savings on bridge transactions and a different message-encoding scheme that breaks backward compatibility at the wire level. (LZ docs)
- 3 competitor protocols (Stargate, Radiant, Ethena) have already migrated; their migration approaches are public. (evidence/define-prior-art.md)
- Internal team has migrated 1 prior LayerZero deployment ($500K TVL, single-chain) to OFTv2; the experience is partial but real. (intake)
- No incident on OFTv1 in the last 6 months; system is stable but increasingly diverging from the LayerZero ecosystem direction. (iceberg.events)
- Audit team is booked for year-end audits in Q4 and can allocate 2 weeks delta-audit time before that block. (intake step + evidence)
- Quarter-end (year-end) audit window closes in week 8 from now; ops bandwidth is reduced during this window. (intake)

### Step 2, What is success

intake.success_criteria = qualitative-signal. The framework demands observable signals.

| Criterion | Type | Threshold/Signal | Measurement window |
|---|---|---|---|
| Bridge integrity preserved | signal | Zero customer-reported fund-loss tickets in support channel during migration | Migration window + 4 weeks |
| TVL preserved | metric | TVL maintains > 95% of pre-migration baseline through migration window | Migration window + 4 weeks |
| Audit-clean state | signal | Auditor confirms no audit blowback during year-end review | Q4 audit conversation |
| Ops on-call load manageable | signal | On-call ticket volume during dual-rail period stays within 1.5x baseline | Dual-rail weeks |
| Gas savings captured | metric | New bridge transactions show ~30% gas reduction post-deployment | Post-deployment weeks |

### Step 3, The question

The original ask is "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

Step 1 evidence answers the meta-question (whether to migrate at all). The evidence: competitors have migrated, message-encoding is diverging, gas-savings are real, no fundamental blocker exists. Migration is on the table; the question is the how, not the whether.

**Canonical question:** "Which migration archetype best balances reversibility against gas-savings capture, given $12M TVL, quarter-end audit constraints, ops capacity reduction during year-end, and the requirement to maintain bridge integrity across all 4 chains within an 8-week ops-friendly window?"

**Why this and not the original ask:** the meta-question (should we migrate?) is answered yes by step 1 evidence; the original ask would re-litigate that answered question and fail to surface the trade-off Decision Matrix needs to score.

**Trade-off named in the question:** reversibility vs gas-savings-capture, modulated by audit constraints and ops capacity.

### Step 4, Candidate answers

| ID | Candidate | Source |
|---|---|---|
| 1 | dual-deploy + drain | zwicky-box archetype 1 |
| 2 | wrapped legacy | zwicky-box archetype 2 |
| 3 | phased cutover with leader chain | zwicky-box archetype 3 |
| 4 | separate token + voluntary migration | zwicky-box archetype 4 |
| 5 | deploy this month, dual-rail through year-end, cutover Q3 (CRD evaporated) | conflict-resolution-diagram D'' |
| 6 | deploy OFTv1.5 with gas optimizations, never migrate to v2 (inversion) | inversion of obvious |
| 7 | do nothing, accept gas-cost drift and message-encoding divergence | do-nothing baseline |
| 8 | wait 6 months and observe how Stargate, Radiant, Ethena's migrations age (analogous prior art delay) | analogous prior art |

8 candidates. Spans dual-deploy, wrap, phase, separate-token, hybrid, inversion, do-nothing, observe-then-act.

### Step 5, Forged solutions

Apply convergent filter:

**Cuts:**
- Candidate 6 (deploy OFTv1.5): violates first-principles atomic-truth-4 (message-encoding backward-compat with the LayerZero ecosystem direction). The OFTv1.5 fork would diverge from LZ standards and create long-term drift. Also, no documented prior art for forking OFTv1 with patches.
- Candidate 7 (do nothing): violates intake.success_criteria.gas-savings clause (do-nothing captures zero gas savings) and ignores the message-encoding divergence pressure. Cut because it does not answer the canonical question.
- Candidate 8 (wait 6 months): conflicts with intake.time_pressure = this-month. The team has explicitly said this is a this-month decision. Cut.
- Candidate 4 (separate token + voluntary): triggers inversion-define failure-mode (liquidity fragmentation) without strong mitigation; intake suggests the team values $12M TVL consolidation, so fragmentation is high cost. Cut at the convergent step.
- Candidate 2 (wrapped legacy): viable but trades long-term tech debt for migration safety. The team's intake suggests the migration is wanted (eng wants OFTv2 features); wrapped-legacy abandons the feature capture. Cut at convergent step but flagged as fallback if forged solutions slip.

**Forged solutions (3):**

### Forged 1: dual-deploy + drain (immediate cutover)

- **Strengths:** matches established LZ migration pattern (Stargate USDC, Radiant v1-to-v2, Ethena USDe); rollback envelope is the dual-rail period (4-8 weeks); zero forced cutover for users; gas-savings begin immediately upon deployment; high prior-art density.
- **Risks:** ops complexity during dual-rail (8 monitoring surfaces: 2 contracts × 4 chains); drain incentive design must be calibrated; immediate cutover during quarter-end audit conflicts with audit-clean-state criterion if not coordinated.
- **Atomic-truth alignment:** atomic-truth-3 (users must not lose funds), preserved by dual-deploy architecture; atomic-truth-4 (encoding compat during dual-rail), preserved by maintaining OFTv1 active.
- **Prior art:** Stargate USDC 6-week dual-rail with 99%+ migration; Radiant v1-to-v2 8-week; Ethena similar.

### Forged 2: phased cutover with leader chain

- **Strengths:** per-chain controlled blast radius; learning between phases; reversibility within each phase; suits team's prior single-chain migration experience; lower simultaneous ops load.
- **Risks:** total migration timeline 4-8 weeks per chain × 4 chains = up to 32 weeks if fully sequential, conflicts with this-month time pressure unless aggressive overlap; cross-chain message-encoding incompatibility during multi-chain phase windows.
- **Atomic-truth alignment:** atomic-truth-1 (value transfer), preserved per chain at the cost of cross-chain transfer being limited during phase windows.
- **Prior art:** Compound v2-to-v3 (Ethereum first); Uniswap v2-to-v3 (Ethereum first); both succeeded but at much smaller TVL on the leader chain.

### Forged 3: dual-deploy + delayed cutover (CRD evaporated)

- **Strengths:** captures gas-savings from week 1 (deployment captures); preserves audit-clean-state through year-end (cutover deferred to Q3); satisfies both eng (deploy now) and ops (cutover later) needs explicitly; matches CRD evaporation outcome.
- **Risks:** longer dual-rail period (16+ weeks if cutover is Q3); operational fatigue during dual-rail; drain mechanics must be re-designed for delayed cutover (incentive structure differs from immediate-cutover dual-deploy).
- **Atomic-truth alignment:** atomic-truth-3 (no fund loss), preserved by dual-deploy; atomic-truth-2 (gas predictable), maintained because both contracts run in parallel without unexpected interactions.
- **Prior art:** less direct prior art for delayed cutover; Lido stETH-wstETH cohabitation is similar but is permanent rather than time-bound. CRD evaporation produced this option fresh.

**Cuts table:**

| Candidate | Cut reason |
|---|---|
| 6 (OFTv1.5) | violates atomic-truth-4 (encoding compat with LZ ecosystem) |
| 7 (do nothing) | violates success-criterion gas-savings; ignores encoding divergence |
| 8 (wait 6 months) | conflicts with intake.time_pressure |
| 4 (separate token) | high liquidity fragmentation cost; cut at convergent step |
| 2 (wrapped legacy) | abandons OFTv2 feature capture; flagged as fallback |

### Step 6, Resource plan

| Forged solution | People | Time | Decisions | Capital | Bottleneck |
|---|---|---|---|---|---|
| dual-deploy + drain (immediate cutover) | 1 lead eng (4 dev + 8 dual-rail = 12 wks); 1 ops eng (1 setup + 8 dual-rail = 9 wks); 1 auditor (2 wks delta); 0.25 PM (8 wks coord) | 14 calendar weeks total | week 4 deploy sign-off, week 6 audit sign-off, week 12 cutover sign-off | $30K audit + $40K drain incentive + $15K ops tools = $85K | audit-team Q4 availability (2-week slot before year-end block) |
| phased cutover with leader chain | 1 lead eng (4 dev + 16 phased oversight = 20 wks); 1 ops eng (4 phased monitoring); 1 auditor (3 wks delta-audit per chain × 4 = 12 wks); 0.5 PM (16 wks) | 20 calendar weeks if aggressive overlap; 32 if fully sequential | per-chain deploy/cutover sign-offs (8 decisions across 4 chains × 2 phases) | $80K audit (per-chain) + $20K ops + $30K tooling = $130K | audit team multi-week commitment across 4 chains; cannot overlap with year-end |
| dual-deploy + delayed cutover | 1 lead eng (4 dev + 16 dual-rail oversight = 20 wks); 1 ops eng (16 wks dual-rail); 1 auditor (2 wks delta); 0.25 PM (16 wks) | 22 calendar weeks (4 dev, 16 dual-rail, 2 cutover) | week 4 deploy, week 6 audit, week 18-20 cutover | $30K audit + $30K drain (lower than immediate because slower) + $25K ops monitoring (extended) = $85K | ops bandwidth across the longer dual-rail period; team fatigue risk |

**Dominant bottleneck across all forged solutions:** auditor availability before year-end. Solutions 1 and 3 fit the 2-week delta-audit window; solution 2 (phased) cannot fit because it needs 12 weeks of audit work that conflicts with year-end audit block.

### Decision Matrix Handoff

The forged solutions become Decision Matrix's option-set anchor:
1. dual-deploy + drain (immediate cutover)
2. phased cutover with leader chain
3. dual-deploy + delayed cutover

Suggested criteria from forged-solution trade-off analysis:
- Reversibility (rollback envelope)
- Gas-savings capture timing
- Ops complexity during transition
- Audit fit (per-window auditor availability)
- Prior-art density
- Stakeholder satisfaction (CRD-derived; only solution 3 explicitly satisfies both sides)

Resource bottleneck flag for Eisenhower: **auditor availability before year-end is the binding constraint**. Solutions that fit the 2-week pre-Q4 window become urgent-important; solution 2 (phased) is feasible but slips past year-end.

### State update

```json
{
  "productive_thinking": {
    "question": "Which migration archetype best balances reversibility against gas-savings capture, given $12M TVL, quarter-end audit constraints, ops capacity reduction during year-end, and the requirement to maintain bridge integrity across all 4 chains within an 8-week ops-friendly window?",
    "candidate_count": 8,
    "forged_solutions": ["dual-deploy+drain-immediate", "phased-cutover-leader-chain", "dual-deploy+delayed-cutover"],
    "forged_count": 3,
    "resource_bottleneck": "auditor-availability-pre-Q4",
    "completeness": 9
  }
}
```

### What the next framework (Decision Matrix) inherits

Decision Matrix gets:
- 3 forged solutions as the option-set anchor
- 5 candidate solutions cut at the convergent step (preserved as fallback if forged solutions tie in scoring)
- 6 suggested criteria with weights informed by forged-solution trade-offs
- The auditor-availability bottleneck as a hard constraint that affects scoring on the time-fit and audit criteria
- A note that solution 3 (dual-deploy + delayed cutover) is the CRD-evaporated option and is the only solution that explicitly satisfies both eng and ops stakeholders

---

## What This Means For The Decision

Productive Thinking is the spine. When all 6 steps run cleanly, Decision Matrix downstream operates on a known canonical question, an option-set anchor of 2-3 distinct forged solutions, and a resource plan that surfaces the binding constraint. The recommendation produced by Decision Matrix becomes credible because every input is grounded.

The cost of skipping any step: skipping step 1 (no evidence) yields a recommendation that the team cannot defend; skipping step 3 (wrong question) yields a confident answer to the wrong question; skipping step 4 (narrow candidates) yields a Decision Matrix that picks among the obvious without exploring alternatives; skipping step 5 (no convergent forging) yields Decision Matrix scoring noise; skipping step 6 (no resource plan) yields a recommendation that ignores binding constraints and fails at execution.

For this OFTv2 migration: the canonical question explicitly names the reversibility-vs-gas-savings trade-off. The 3 forged solutions are strategically distinct (immediate cutover vs phased vs delayed). The auditor availability bottleneck rules in solutions 1 and 3 and rules out solution 2 unless the team accepts a delay past year-end. Decision Matrix should weight reversibility, audit fit, and stakeholder satisfaction high, and is likely to recommend solution 3 (the CRD-evaporated option) because it matches both eng and ops needs and fits the auditor window.
