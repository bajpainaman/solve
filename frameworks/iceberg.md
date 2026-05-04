# Iceberg Model

**Phase:** Systems · **Source:** https://untools.co/iceberg-model

The iceberg sorts what's visible from what's load-bearing. Above the waterline: events. Below: patterns, structures, mental models. Surface-level fixes treat events. Real leverage is at the structures and mental-models layer. The framework's job is to push the team past the events layer down to where decisions actually compound.

This is the routing-critical Systems framework. Its output drives **mid-run cross-skill handoffs**: if the structures layer reveals a named bug-shape, /solve auto-handoffs to /investigate. If the mental-models layer reveals pre-product or no-PMF uncertainty, /solve auto-handoffs to /office-hours. If the structures layer reveals an explicit architecture decision, the run flags `state.PLAN_ENG_REVIEW_AT_END = true`. Every Iceberg run evaluates these triggers explicitly, even when none fire.

---

## Entry Predicate

```
always_run
```

Iceberg runs every time. The framework's output is essential for Cynefin's emergence-dimension scoring and for Connection Circles' variable identification. Skipping Iceberg would degrade both downstream frameworks.

### Inputs

- All Phase 1 (Define) framework outputs
- `$RUN_DIR/evidence/define-*.md` (research evidence on prior art and failure modes)
- `$RUN_DIR/evidence/systems-*.md` (research on analogous systems if available)
- `intake.problem_refined`

### Outputs

- `$RUN_DIR/frameworks/iceberg.md` — 4-layer breakdown + cross-skill trigger evaluation + leverage points
- Possibly: `state.PLAN_ENG_REVIEW_AT_END = true` flag
- Possibly: SendMessage to lead triggering /investigate or /office-hours auto-handoff

---

## Operating Principles

**1. Each layer is concrete, not categorical.**

Events: specific incidents, specific dates. Patterns: recurring shapes with frequency. Structures: named system components with rules. Mental Models: explicit beliefs held by named actors. Anti-pattern: prose paragraphs that describe categories instead of concrete instances.

**2. Below the waterline is where leverage lives.**

Events get attention; structures and mental models get results. Solving at the events layer treats symptoms. Solving at structures and mental models is where decisions compound. The framework's value is forcing the team to push deeper than the events layer. Anti-pattern: writing 10 events and 1 sentence each for the deeper layers.

**3. Each layer feeds the next.**

Events imply patterns over time. Patterns are produced by structures. Structures are upheld by mental models. The output should make these causal links explicit. Anti-pattern: parallel layer dumps with no causal articulation.

**4. The cross-skill triggers run explicitly, every run.**

Every Iceberg output evaluates: bug-shape? pre-product? architecture decision? Even when none fire. This makes the routing decisions auditable and prevents silent skipping. Anti-pattern: only mentioning triggers when one fires, leaving the skip cases invisible.

**5. Mental models include the team's own.**

Don't just describe what users believe; describe what the team believes. The team's beliefs are the structures' enforcement mechanism. Surfacing them is how the iceberg becomes useful for self-aware decision-making. Anti-pattern: only documenting external actors' models.

---

## Response Posture

**Tone.** Anatomical. The framework is mapping a system's structure, not advocating for changes. Each layer entry is a specific observation, not a recommendation.

**Pacing.** Single pass through 4 layers, then a single pass through the 3 cross-skill triggers. Then a leverage-point summary.

**Push depth.** Zero direct user questions. Iceberg reads prior outputs + evidence and writes its analysis. If a layer is sparse (< 3 entries), SendMessage to lead requesting clarification or research expansion before completing.

**Where to escalate.** SendMessage to lead when:
- Events layer has fewer than 3 specific incidents (the team doesn't have observability or hasn't surfaced the data)
- Structures layer can't articulate the named system; Phase 1 frameworks didn't generate enough material
- A cross-skill trigger fires (bug-shape, pre-product, or architecture decision)
- Mental Models layer is empty (the team hasn't articulated its own assumptions; Ladder of Inference will struggle in Phase 3)

---

## Anti-Sycophancy Rules

Never write:
- "There are several events worth noting..." (list specific dated incidents)
- "Patterns suggest..." (state the pattern's name and frequency)
- "Various structural factors..." (name the structures with their rules)
- "Some mental models include..." (name them with the actor and the belief)

Always:
- Layer entries get bullet points with concrete content (date, actor, system name, rule).
- Causal links between layers are explicit (this event is part of this pattern, this pattern is produced by this structure).
- Cross-skill triggers are evaluated yes/no in a dedicated section.

---

## Pushback Patterns

**Pattern 1: "Events feel sufficient" then push to patterns**

- Internal evidence: 5 events listed, 1 pattern, 0 structures.
- BAD: Output as-is.
- GOOD: Patterns require 3+ events of the same shape. Re-read events. Group by shape. If shapes recur, name the pattern. If they don't recur, the events are independent (rare; usually team hasn't noticed the pattern yet).

**Pattern 2: "Structures are abstract" then name the components**

- Internal evidence: structures layer says "the org incentivizes X."
- BAD: Accept this.
- GOOD: "The org incentivizes X" is a mental model. The structure is the specific mechanism: which OKR, which compensation rule, which review process. Name the mechanism explicitly so the structure can be changed.

**Pattern 3: "Mental models are everyone's" then name actors**

- Internal evidence: "users believe X."
- BAD: Generic "users."
- GOOD: Name the segment. "Power users (≥ 5 transactions/week) believe X. New users (< 5) believe Y. The team itself believes Z." Different actors have different models; treating "users" as monolithic loses signal.

**Pattern 4: "No bug-shape, skip /investigate trigger" then verify**

- Internal evidence: agent assumes no bug-shape because the problem isn't a bug.
- BAD: Skip trigger evaluation.
- GOOD: Evaluate explicitly. "Bug-shape check: does any structure-layer entry name a system component that fails reliably under specific conditions? <yes/no>. If yes, auto-handoff to /investigate. For OFTv2: structures layer flags cross-chain mempool dynamics, but these are 'uncertainty' not 'reliable failure.' No bug-shape. Trigger does not fire."

**Pattern 5: "Architecture decision" then check whether it requires /plan-eng-review**

- Internal evidence: structures layer mentions "we need to redesign component X."
- BAD: Skip the trigger.
- GOOD: Evaluate. Does the decision involve creating new system components, changing how existing components interact, or making technology choices that constrain future work? If yes, mark `state.PLAN_ENG_REVIEW_AT_END = true`. The end-of-run handoff to /plan-eng-review surfaces the architecture review.

---

## Method

7-step procedure. Each layer + each trigger gets its own step.

### Step 1, Read all Phase 1 outputs

```bash
ls $RUN_DIR/frameworks/*.md | grep -v iceberg
```

Read every Phase 1 framework file. Iceberg's content comes from this aggregation; without it, the framework is generating from intake alone (insufficient).

### Step 2, Events layer

List specific incidents:
- Date or timeframe
- What happened (one sentence)
- Source (which prior framework or evidence file mentioned this)

Aim for 3-7 specific events. Prefer dated incidents from research evidence. If the team hasn't surfaced any specific events, that's signal: SendMessage to lead requesting an observability check.

### Step 3, Patterns layer

Group events by shape:
- Pattern name (descriptive)
- Frequency (how often)
- Affected segment (who experiences this)
- Source events (which Step 2 events fall under this pattern)

A pattern requires 3+ events of similar shape. If you can't group, the events are independent or the team hasn't noticed the pattern.

### Step 4, Structures layer

For each pattern, name the structure that produces it:
- Structure name (specific system component or organizational mechanism)
- Rule or behavior (what the structure does)
- How the structure produces the pattern (explicit causal link)

This is the leverage layer. Structures are nameable, ownable, and changeable. Anti-pattern: writing "the system" or "the way we work."

### Step 5, Mental Models layer

For each structure, identify the beliefs that uphold it:
- Actor (specific person, role, or segment)
- Belief (one sentence)
- Evidence (what observation supports this is the belief)
- Verification status (verified / unverified / contradicted)

Include the team's own mental models, not just external actors. Mark unverified beliefs explicitly; they're candidates for ladder-of-inference attack in Phase 3.

### Step 6, Cross-skill trigger evaluation

Three triggers, evaluated explicitly:

#### Trigger 1, Bug-shape (auto-handoff to /investigate)

Question: "Does any structure-layer entry name a system component that fails reliably under specific conditions?"

If yes: name the component, name the conditions, name the failure mode. SendMessage to lead: "iceberg.structures = bug-shape. Recommend mid-run handoff to /investigate. Component: <X>. Failure: <Y>. Conditions: <Z>."

If no: state explicitly. "Bug-shape check: NO. The structures we identified are uncertainty, not reliable failure modes. Trigger does not fire."

#### Trigger 2, Pre-product framing (auto-handoff to /office-hours)

Question: "Does the mental-models layer reveal that the team has a no-PMF or pre-product uncertainty (e.g. 'we believe users want X' without verification, OR no users yet)?"

If yes: SendMessage to lead: "iceberg.mental_models = pre-product. Recommend mid-run handoff to /office-hours. Unverified core belief: <belief>."

If no: state explicitly. "Pre-product check: NO. The team has users and verified core beliefs about value delivery. Trigger does not fire."

#### Trigger 3, Architecture decision (end-of-run handoff to /plan-eng-review)

Question: "Does the structures layer reveal an explicit architecture decision, requiring new components, changed interactions, or technology choices that constrain future work?"

If yes: mark `state.PLAN_ENG_REVIEW_AT_END = true`. The recommendation in the final report includes a /plan-eng-review handoff suggestion.

If no: state explicitly. "Architecture-decision check: NO. The decision is operational, not architectural. Trigger does not fire."

### Step 7, Leverage point summary

For each layer, identify 1-2 leverage points (places where intervention would have the largest effect):
- Events leverage: usually low (treats symptoms)
- Patterns leverage: medium (changes recurrence)
- Structures leverage: high (changes the source)
- Mental Models leverage: highest (changes who upholds the structure)

The recommendation in Phase 3 should preferentially target deeper-layer leverage when feasible.

---

## Probe Patterns

### Probe 1, Are events specific enough?

> "Each event entry has a date or timeframe + one-sentence description + source. If any are missing those fields, the events layer isn't usable for pattern detection."

### Probe 2, Are patterns load-bearing?

> "Each pattern groups 3+ events. If I have a pattern grouping 1-2 events, it's premature; downgrade to 'observation' rather than pattern."

### Probe 3, Are structures nameable and ownable?

> "Each structure entry names a specific component or mechanism that someone owns. If 'the system' or 'the org' is the named structure, push deeper."

### Probe 4, Are mental models verified?

> "Each mental model entry has a verification status. Unverified beliefs are candidates for ladder-of-inference attack in Phase 3; the more we have, the more likely Phase 3 surfaces unjustified leaps."

### Probe 5, Did I evaluate all 3 cross-skill triggers?

> "Bug-shape, pre-product, architecture decision: each evaluated explicitly with yes/no and reasoning. If any are missing, redo Step 6."

---

## Forcing Exemplars

### Exemplar 1, Stating an event

SOFTENED:
> "There have been some incidents recently."

FORCING:
> "Event E1: 2025-12-04, OFTv1 transfer between Avalanche and Arbitrum stuck for 2h 14m due to executor lag. Source: incident log + LayerZero scan. Affected ~12 users; no fund loss."

### Exemplar 2, Stating a pattern

SOFTENED:
> "There's a pattern of issues."

FORCING:
> "Pattern P1: Cross-chain delay during high-gas periods. Frequency: 3 incidents in last 6 months (E1, E2, E3 from events layer). Affected segment: Avalanche↔Arbitrum transfers > $5K. All occurred during gas-spike events on either chain."

### Exemplar 3, Stating a structure

SOFTENED:
> "The system has some issues."

FORCING:
> "Structure S1: LayerZero executor's gas-cost-aware batching. Rule: executor delays message delivery during gas spikes to optimize cost; user-facing latency increases as a result. Produces pattern P1 because the executor's optimization for cost ignores user-facing latency expectations."

### Exemplar 4, Stating a mental model

SOFTENED:
> "Users expect transfers to be fast."

FORCING:
> "Mental Model MM1: Power users (≥ 5 transfers/month) believe cross-chain transfers should settle within 30 seconds based on their experience with native-chain transfers. Evidence: 75% of support tickets mentioning latency cite '30 seconds' or 'instant' as the expected timing. Verification status: VERIFIED via support ticket sample of 200. This belief upholds Structure S1's user dissatisfaction; without re-anchoring user expectations, optimizing the executor alone won't change support volume."

### Exemplar 5, Stating a non-firing trigger

SOFTENED:
> "We don't think /investigate is needed."

FORCING:
> "Bug-shape trigger evaluation: NO. The structures layer flags S1 (executor batching) and S2 (cross-chain mempool dynamics). S1 is intentional behavior, not a failure mode. S2 is uncertainty under specific conditions, not reliable failure. Neither qualifies as a 'named system component failing reliably.' Trigger does not fire. /investigate handoff not recommended."

---

## Output Schema

### Section A, Header

```markdown
# Iceberg Model, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** <comma-separated Phase 1 framework files + evidence files>
**Cross-skill triggers fired:** <list or "none">
```

### Section B, Layer 1: Events

```markdown
## Events (visible incidents)

| ID | Date / Timeframe | Description | Source |
|---|---|---|---|
| E1 | <ISO or range> | <one sentence> | <framework or evidence file> |
| E2 | ... | ... | ... |
```

### Section C, Layer 2: Patterns

```markdown
## Patterns (over time)

### P1: <descriptive name>

- Frequency: <how often>
- Affected segment: <who>
- Source events: E<N>, E<N>, E<N>
- Causal link to structures: <which structure produces this>

### P2: ...
```

### Section D, Layer 3: Structures

```markdown
## Structures (systemic causes)

### S1: <specific named component or mechanism>

- Rule / behavior: <one sentence>
- Owner: <role or team>
- How this structure produces patterns: <causal explanation>
- Source patterns: P<N>

### S2: ...
```

### Section E, Layer 4: Mental Models

```markdown
## Mental Models (beliefs that uphold structures)

### MM1: <belief one-liner>

- Actor: <specific segment, role, or team — including own team>
- Evidence: <what observation supports this is the belief>
- Verification: <verified / unverified / contradicted>
- Upheld structures: S<N>

### MM2: ...
```

### Section F, Cross-skill triggers (always evaluated)

```markdown
## Cross-Skill Trigger Evaluation

### Bug-shape (auto-handoff to /investigate)

- Question: Does any structure name a system component failing reliably under specific conditions?
- Result: <YES / NO>
- Reasoning: <explicit>
- Action: <SendMessage to lead with handoff request / no action>

### Pre-product (auto-handoff to /office-hours)

- Question: Does mental-models layer reveal pre-product or no-PMF uncertainty?
- Result: <YES / NO>
- Reasoning: <explicit>
- Action: <SendMessage to lead / no action>

### Architecture decision (end-of-run handoff to /plan-eng-review)

- Question: Does structures layer reveal a decision requiring new components, changed interactions, or technology constraints?
- Result: <YES / NO>
- Reasoning: <explicit>
- Action: <state.PLAN_ENG_REVIEW_AT_END = true / no action>
```

### Section G, Leverage points

```markdown
## Leverage Points

| Layer | Leverage entry | Intervention scope |
|---|---|---|
| Events | <which event> | low (treats symptom) |
| Patterns | <which pattern> | medium |
| Structures | <which structure> | high |
| Mental Models | <which model> | highest |
```

### Section H, Decision Hook

```markdown
## Decision Hook

Phase 3 frameworks should preferentially target deeper-layer leverage points. Decision Matrix's "intervention level" criterion should weight structures and mental models higher than events.

If a cross-skill trigger fired, the recommendation in the final report includes the corresponding handoff (/investigate / /office-hours / /plan-eng-review).
```

### Section I, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentences. Name the deepest layer where leverage exists. Surface the highest-impact mental model. State which (if any) cross-skill trigger fired.>
```

### Section J, Completeness

```markdown
**Completeness:** <N>/10
- 3+ events with date + description + source: +<N>
- 2+ patterns each grouping 3+ events: +<N>
- 2+ structures with named components and rules: +<N>
- 2+ mental models with verification status: +<N>
- All 3 cross-skill triggers evaluated explicitly: +<N>
- Leverage points identified per layer: +<N>
```

---

## Decision Hook

Iceberg's output drives:

1. **Cynefin scoring**: emergence dimension reads `connection-circles.cycles` indirectly via Iceberg. Iceberg's structures layer is also the input to cynefin.cause_effect_clarity.

2. **Connection Circles input**: variables for Connection Circles often come from Iceberg's structures layer.

3. **Cross-skill auto-handoffs**: bug-shape → /investigate (mid-run); pre-product → /office-hours (mid-run); architecture → /plan-eng-review (end-of-run).

4. **Decision Matrix weighting**: options that target deeper-layer leverage (structures, mental models) get higher scores on the "intervention level" criterion.

5. **Confidence rubric impact**:
   - Mental Models layer has ≥ 1 unverified belief: +0 (this is normal; gives Phase 3 work)
   - Mental Models layer is empty: -1 (we don't know what we don't know)
   - All 3 cross-skill triggers explicitly evaluated: +0 (baseline)
   - Bug-shape fired AND /investigate completed: +1 (root cause known)

### Override conditions

If bug-shape trigger fires and /investigate produces evidence that changes the problem framing, /solve halts current Phase 3 and re-runs Phase 1 intake with the investigation findings. Iceberg's trigger evaluation is the gate for this override.

---

## Cross-Framework Triggers

(See Section F for the 3 cross-skill triggers Iceberg evaluates.)

Other downstream triggers Iceberg fires:
- **Mental Models layer empty** → SendMessage to lead recommending re-run of Phase 1 with focus on team's own assumptions
- **Structures layer fewer than 2 entries** → Connection Circles will struggle for variables; SendMessage to lead requesting research expansion
- **Events layer fewer than 3 entries** → suggests team lacks observability; flag for inclusion in execution plan ("add observability for X, Y, Z")

---

## Failure Modes

### Failure Mode 1, Events without dates

Trap: events listed as prose without specific dates or timeframes.

Manifestation: events table has descriptions but the "Date" column is "recent" or "frequently."

Check: every event has an ISO date or specific timeframe (e.g. "Q4 2025").

Recovery: SendMessage to lead requesting incident log review; don't proceed without dated events.

### Failure Mode 2, Patterns without minimum events

Trap: a pattern claimed with only 1-2 events backing it.

Manifestation: pattern's "Source events" column lists < 3 events.

Check: count source events per pattern.

Recovery: downgrade to "observation" or merge with another pattern; don't elevate sparse observations to pattern status.

### Failure Mode 3, Vague structures

Trap: structures layer has "the system" or "the way we work" entries.

Manifestation: structure entries don't name specific components.

Check: each structure entry names a specific component, mechanism, or rule.

Recovery: push deeper. Ask "what specifically does the system do?" until a concrete component is named.

### Failure Mode 4, Cross-skill triggers silently skipped

Trap: triggers evaluated implicitly or skipped because "obviously not."

Manifestation: Section F missing trigger entries.

Check: all 3 triggers must have explicit yes/no + reasoning.

Recovery: re-evaluate each, write reasoning even when skip is obvious.

### Failure Mode 5, Team's own mental models missing

Trap: Mental Models layer documents external actors (users, customers) but not the team itself.

Manifestation: no mental-model entries with "team" or "us" or "$ENG_LEAD" as actor.

Check: at least 1 mental-model entry has the team as actor.

Recovery: explicitly add team's beliefs (often: "we believe X", "our default is Y", "we assume Z").

---

## Jargon Glossary

- **events**, visible incidents above the waterline; the surface layer.
- **patterns**, recurring shapes across events; the second layer.
- **structures**, named system components or organizational mechanisms producing patterns; the third layer.
- **mental models**, beliefs held by named actors that uphold structures; the deepest layer.
- **leverage point**, a place where intervention has disproportionate effect on the system.
- **bug-shape**, a structure-layer entry naming a specific component that fails reliably under specific conditions; triggers /investigate handoff.
- **pre-product**, a mental-models-layer signal that the team has unverified core assumptions about user value; triggers /office-hours handoff.
- **architecture decision**, a structure-layer change requiring new components, changed interactions, or technology constraints; triggers /plan-eng-review handoff.
- **causal link**, the explicit "this layer produces that layer" connection that distinguishes Iceberg from a parallel layer dump.
- **verified belief**, a mental model with observation supporting it; resistant to ladder-of-inference attack.
- **unverified belief**, a mental model without supporting evidence; candidate for Phase 3 attack.
- **deeper-layer leverage**, intervention at structures or mental models rather than events; characteristic of high-leverage decisions.

---

## Completeness Scoring

### 10/10, Decisive
- 5+ events with dates and sources
- 3+ patterns each grouping 3+ events with explicit causal link to structures
- 3+ structures with named components and rules
- 3+ mental models with actors, evidence, and verification status (including team's own)
- All 3 cross-skill triggers evaluated explicitly with reasoning
- Leverage points identified per layer

### 7/10, Confident
- 3-4 events
- 2 patterns
- 2 structures
- 2 mental models (most external)
- All 3 triggers evaluated

### 4/10, Tentative
- < 3 events or events without dates
- 1 pattern
- Vague structures
- 1 mental model, generic actor
- 1-2 triggers evaluated

### 0/10, Unusable
- Prose paragraphs instead of layered entries
- No causal links between layers
- No trigger evaluation
- No leverage point summary

Iceberg completeness ≤ 4 contributes -1 to overall rubric AND blocks Connection Circles (insufficient variables).

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

### Step 1, Inputs read

Phase 1 frameworks (all 8) plus evidence files: define-prior-art.md, define-failure-modes.md.

### Step 2, Events

| ID | Date | Description | Source |
|---|---|---|---|
| E1 | 2025-12-04 | OFTv1 transfer between Avalanche and Arbitrum stuck for 2h 14m due to executor lag during gas spike | LayerZero scan + incident log |
| E2 | 2025-11-15 | Cross-chain transfer between Base and Ethereum delayed 45 min during Ethereum mempool congestion | LayerZero scan |
| E3 | 2025-10-22 | OFTv1 transfer Arbitrum→Avalanche delayed 1h 30m during Avalanche gas spike | incident log |
| E4 | 2025-09-08 | User-reported issue: transfer "feels slow" during normal-gas period; investigation found 12s settlement time | support tickets |
| E5 | 2025-08-12 | Edge case: multiple users initiated near-simultaneous transfers, 2 of 8 stuck for ~10 min | incident log |

### Step 3, Patterns

```markdown
### P1: Cross-chain delay during gas-spike periods

- Frequency: 3 incidents in last 6 months (E1, E2, E3)
- Affected segment: Avalanche↔Arbitrum + Base↔Ethereum transfers > $5K during gas events
- Causal link to structures: produced by Structure S1 (executor's gas-cost-aware batching)

### P2: User-perceived slowness during normal operation

- Frequency: ~2 support tickets/week with latency complaints (E4 sample)
- Affected segment: power users (≥ 5 transfers/month)
- Causal link to structures: produced by Structure S2 (cross-chain message ordering) interacting with Mental Model MM1
```

### Step 4, Structures

```markdown
### S1: LayerZero executor's gas-cost-aware batching

- Rule: executor delays message delivery during gas spikes to optimize cost
- Owner: LayerZero (third-party); we don't control directly
- How this produces pattern: cost optimization ignores user-facing latency expectations; pattern P1 emerges
- Source patterns: P1

### S2: Cross-chain message ordering and indexing

- Rule: messages are indexed asynchronously across chains; settlement time depends on chain finality + indexer lag
- Owner: combined LayerZero + chain validators
- How this produces pattern: even in normal operation, messages take 5-30 seconds; users expect <30s and 12s feels slow when expectation is 3s
- Source patterns: P2

### S3 (THIS IS THE ONE): Cross-chain mempool dynamics during partial deployment

- Rule: when OFTv1 and OFTv2 are deployed simultaneously on the same chain pairs, transfer messages can interact non-trivially with executor's batching logic
- Owner: us (we choose deployment topology) + LayerZero (executor logic)
- How this produces pattern: this is the key UNCERTAINTY for OFTv2 migration. We don't yet have empirical data on dual-deployed behavior at $12M TVL scale.
- Source patterns: not yet observed, but inferred from F2 in inversion-define
```

### Step 5, Mental Models

```markdown
### MM1: Power users believe cross-chain settles in <30 seconds

- Actor: power users (≥ 5 transfers/month, ~340 users)
- Evidence: 75% of latency-related support tickets cite "30 seconds" or "instant" expected timing
- Verification: VERIFIED via support ticket sample of 200
- Upheld structures: S2 (without re-anchoring expectations, optimizing the protocol won't change support volume)

### MM2: Team believes "newer is better"

- Actor: $ENG_TEAM (us)
- Evidence: prior conversations + commit messages reveal default preference for upgrading LayerZero versions
- Verification: UNVERIFIED (we have not done a rigorous OFTv1 vs OFTv2 audit comparison)
- Upheld structures: S3 (this belief is what drove us to consider migration; without verification, we're committing to migration on assumption)

### MM3: LP providers believe migration would disrupt liquidity

- Actor: LP providers on bridge pools (~6 large LPs)
- Evidence: prior LP communications during minor protocol upgrades; LP feedback in past surveys
- Verification: VERIFIED via prior LP interactions
- Upheld structures: feeds into the reinforcing cycle from connection-circles (LP behavior → bridge volume → fees → LP retention)
```

### Step 6, Cross-skill trigger evaluation

```markdown
### Bug-shape (auto-handoff to /investigate)

- Question: Does any structure name a system component failing reliably under specific conditions?
- Result: NO
- Reasoning: S1 (executor batching) is intentional behavior optimized for cost, not a failure mode. S2 (message ordering) is normal cross-chain behavior. S3 (mempool dynamics during partial deployment) is uncertainty about a future configuration, not reliable failure of an existing system. None qualify as bug-shape.
- Action: NO handoff to /investigate.

### Pre-product (auto-handoff to /office-hours)

- Question: Does mental-models layer reveal pre-product or no-PMF uncertainty?
- Result: NO
- Reasoning: MM1 (user latency expectations) is verified. MM3 (LP beliefs) is verified. MM2 (team's "newer is better") is UNVERIFIED but does not represent pre-product uncertainty about user value; it's an unverified internal preference about technology choice. /office-hours is for product/PMF questions; this is an engineering decision.
- Action: NO handoff to /office-hours.

### Architecture decision (end-of-run handoff to /plan-eng-review)

- Question: Does structures layer reveal a decision requiring new components, changed interactions, or technology constraints?
- Result: YES
- Reasoning: S3 explicitly identifies that the migration changes how OFTv1 and OFTv2 interact with executor's batching logic. The decision involves: (a) new component (OFTv2 contracts on 4 chains), (b) changed interactions (dual-deployment topology during drain window), (c) technology constraints (committing to OFTv2 for future LayerZero integrations). This is an architecture decision.
- Action: mark `state.PLAN_ENG_REVIEW_AT_END = true`. Recommendation in final report includes /plan-eng-review handoff.
```

### Step 7, Leverage points

| Layer | Leverage entry | Intervention scope |
|---|---|---|
| Events | E1-E5 | low (treats individual incidents) |
| Patterns | P1 (gas-spike delay) | medium (addressing this changes future incident shape) |
| Structures | S1 (executor batching) | medium (we don't directly control; can only work around) |
| Structures | S3 (mempool dynamics) | high (we control deployment topology; addressing this is what /solve is about) |
| Mental Models | MM2 (newer is better) | highest (this is the unverified belief driving our decision; verifying it via audit + testnet probe is the most leveraged action we can take during the run) |

### Output completeness

- 5 events with dates and sources: yes
- 2 patterns each grouping 3+ events: P1 has 3, P2 has multiple (sample of 1 cited): yes
- 3 structures with named components: yes (S1, S2, S3)
- 3 mental models with actors + verification status (including team's own MM2): yes
- All 3 cross-skill triggers explicitly evaluated: yes
- Leverage points identified per layer: yes

**Completeness: 9/10** (minus 1 for not naming specific support ticket counts in P2 source events).

---

## What This Means For The Decision

Iceberg surfaced 3 layers of useful structure for the OFTv2 decision. The structures layer revealed that the migration is fundamentally about S3 (cross-chain mempool dynamics during partial deployment), which is uncertainty rather than known failure. The mental-models layer flagged MM2 (team's unverified "newer is better" belief) as the highest-leverage point: a 2-week external audit + testnet probe directly addresses this belief and substantially raises confidence in the migration recommendation regardless of which archetype wins.

The architecture-decision trigger fired, marking `state.PLAN_ENG_REVIEW_AT_END = true`. The final recommendation includes /plan-eng-review as a follow-up handoff. Bug-shape and pre-product triggers did not fire; /investigate and /office-hours are not invoked mid-run.

The framework's value here was forcing the team past "OFTv2 is newer so we should upgrade" (events-layer thinking) down to "the central question is about an unverified mental model, and the pre-ship checklist must address it via auditor consult + testnet probe" (mental-models leverage). That shift is what turns the recommendation from "migrate" into "migrate with these specific verifications first."
