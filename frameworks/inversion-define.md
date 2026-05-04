# Inversion (Define-Phase)

**Phase:** Define · **Source:** https://untools.co/inversion

Define-phase inversion: list every plausible failure path before a single solution is selected. The constraint set derived from those failure paths becomes a hard filter on the Decision Matrix. Inversion-define is cheap and disproportionately valuable. Ten minutes of "how could this fail?" prevents 80% of bad decisions made by only thinking about success.

This file describes the **define-phase** inversion. The continuous adversary (spawned in Step 4 of SKILL.md) handles ongoing critique throughout the run. The final inversion-as-dissent runs after Step 8 to challenge the recommendation. Three roles, one mental model: pre-commitment, in-flight, post-commitment.

---

## Entry Predicate

```
always_run
```

Every problem benefits. There is no condition under which the define-phase inversion is skipped. The output of this framework feeds the Decision Matrix as a disqualifier set: any option that violates an inversion-derived constraint scores 0 on that criterion.

### Inputs

- `intake.problem_refined`
- `intake.success_criteria` (defines what "failure" means concretely)
- `frameworks/abstraction-ladder.md::target_rung` (defines the level at which failure is being assessed)
- Research evidence at `$RUN_DIR/evidence/define-failure-modes.md` (historical failure patterns from analogous problems)

### Outputs

- `$RUN_DIR/frameworks/inversion-define.md`
- 5-10 named failure paths with conditions
- A constraint set derived from the conditions
- A "would-disqualify" predicate per constraint that Decision Matrix can apply

---

## Operating Principles

**1. Failure paths must be specific, not categorical.**

"User experience could be bad" is not a failure path. "Users transferring between chains during the migration window see a 30+ minute delay because the old contract is paused before the new one is fully indexed" is a failure path. Anti-pattern: vague categories that produce vague constraints.

**2. Each failure path produces at least one disqualifying constraint.**

If a failure path can't be converted to a constraint that Decision Matrix can evaluate, it isn't useful here. The constraint is the deliverable, not the prose. Anti-pattern: a list of bad things that never make it into the matrix scoring.

**3. Constraints disqualify; they don't penalize.**

If an option violates an inversion-derived constraint, that option scores 0 on the relevant criterion (often a separate "constraint compliance" criterion in Decision Matrix). It doesn't get partial credit. The constraint set is a binary filter applied before weighted scoring. Anti-pattern: treating constraints as soft preferences that can be averaged out.

**4. Failure paths come from research and prior art, not just imagination.**

Research evidence (`evidence/define-failure-modes.md`) provides historical base rates for similar problems. Prior protocol migrations, similar product launches, analogous strategic decisions: these supply the failure paths the team wouldn't have generated cold. Anti-pattern: brainstorming failure paths in a vacuum without historical grounding.

**5. The output is a checklist, not an essay.**

A teammate downstream should be able to apply each constraint in 10 seconds. Constraints must be: testable (can we tell whether an option violates this?), specific (no ambiguity in interpretation), and decidable (binary outcome). Anti-pattern: prose paragraphs the Decision Matrix scorer has to translate.

---

## Response Posture

**Tone.** Pre-mortem analyst. Cold, specific, evidence-anchored. Not anxious. Not encouraging. Just listing what could go wrong and what makes each go-wrong concrete.

**Pacing.** Single pass through the failure-path generation, then a single pass converting paths to constraints. No iteration unless evidence is incomplete (no `evidence/define-failure-modes.md` from research) — in that case, SendMessage to researcher requesting that evidence.

**Push depth.** Zero direct user questions. The framework reads intake + research evidence and writes the failure-path + constraint set. If the problem statement is too vague to generate specific failure paths, escalate.

**Where to escalate.** SendMessage to lead when:
- < 5 failure paths can be generated even with research evidence in hand (problem may be too vague; ask for re-run of intake)
- Failure paths cluster in one category (e.g. all are "audit didn't catch X") suggesting the problem framing is too narrow
- A failure path is high-impact but its conditions aren't observable from the team's vantage (e.g. "regulatory shift in jurisdiction Y") — flag in dissent rather than constraint

---

## Anti-Sycophancy Rules

Never write:
- "There are several risks worth considering..." (name them)
- "Failure could occur in many ways..." (list specific paths)
- "It's important to be careful about..." (state what specifically the constraint forbids)
- "Some options might face challenges..." (which options, what challenges, what's the constraint)

Always:
- Number each failure path. Cite the research evidence or analog that supports it.
- For every failure path, state the conditions under which it manifests.
- For every set of conditions, state the disqualifying constraint as a predicate Decision Matrix can evaluate.

---

## Pushback Patterns

**Pattern 1: "What about black swans?" then bound the failure space**

- Internal pull: list every conceivable bad outcome including 0.1% events.
- BAD: 30 failure paths including "earthquake destroys all Ethereum nodes."
- GOOD: 5-10 failure paths grounded in research evidence or domain priors. Black swans go in the dissent appendix, not the constraint set. The constraint set is for failures we can actively prevent.

**Pattern 2: "Vague worry" then convert to specific path**

- Internal evidence: agent writes "user trust could erode."
- BAD: Accept the prose as a failure path.
- GOOD: Convert. "User trust erodes if 5%+ of cross-chain transfers fail during migration window, observable via support ticket spike or social media volume." Now there's a measurable condition Decision Matrix can score.

**Pattern 3: "Catastrophic but unaddressable" then move to dissent**

- Internal evidence: failure path "regulatory ban on cross-chain transfers in 2026" identified.
- BAD: Add it as a constraint Decision Matrix must filter on.
- GOOD: Add it to dissent appendix as known unaddressable risk; do not add as constraint (no option can prevent it; it would disqualify all options uniformly, which is non-information).

**Pattern 4: "Failure path is actually a soft preference" then re-classify**

- Internal evidence: "ideally we don't lose any users."
- BAD: Constraint = "must not lose any users."
- GOOD: Re-read. "Lose any users" is a soft preference. The hard constraint is "must not lose user funds." Distinguish the two; only the hard ones become disqualifiers.

**Pattern 5: "Same failure path across all options" then check problem framing**

- Internal evidence: every option produces the same failure path.
- BAD: Add the path; let it disqualify nothing.
- GOOD: SendMessage to lead. If every option fails the same way, the problem is at a higher rung of abstraction-ladder; we're not differentiating on the right axis. Recommend re-running zwicky-box with different dimensions.

---

## Method

5-step procedure.

### Step 1, Read research evidence

```bash
[ -f $RUN_DIR/evidence/define-failure-modes.md ] && \
  cat $RUN_DIR/evidence/define-failure-modes.md
[ -f $RUN_DIR/evidence/define-prior-art.md ] && \
  cat $RUN_DIR/evidence/define-prior-art.md
```

If neither exists, SendMessage to researcher requesting "historical failure modes for problem class <X>" before proceeding. Inversion without research is imagination; inversion with research is risk modeling.

### Step 2, Generate 5-10 failure paths

For each path, write:
- A name (short, specific)
- The mechanism (what causes the failure)
- The observable signal (what would tell us this happened)
- The historical/analogous evidence (which prior case supports this being a real risk)

Aim for 5-10. More than 10 usually means the team is generating noise; fewer than 5 means the problem hasn't been thought about hard enough.

### Step 3, Derive conditions per path

For each failure path, write the conditions under which it manifests:
- Trigger (what initiates the failure sequence)
- Amplifiers (what makes it worse)
- Thresholds (at what scale does it become catastrophic vs minor)

Be specific. "If <trigger A> and <trigger B both happen within <window>>, then <amplifier> kicks in, and at <threshold> it becomes catastrophic."

### Step 4, Convert conditions to constraints

For each set of conditions, derive a constraint Decision Matrix can apply as a binary filter:
- Constraint: "an option must NOT [...]"
- Predicate: a sentence Decision Matrix scorer can evaluate yes/no per option
- Disqualification scope: all options or only a subset (e.g. "this constraint applies only to options involving cross-chain message replay")

### Step 5, Write the constraint set

Output the failure paths + constraints in the schema below. The set will be referenced by Decision Matrix Step 1 (disqualification check before scoring).

---

## Probe Patterns

### Probe 1, Specificity test

> "Reading this failure path, can a teammate downstream tell whether a specific candidate option triggers it? If not, the path is too vague; add specifics."

### Probe 2, Evidence anchor

> "What's the historical or analogous case that supports this being a real risk? If I can't name one, this might be imagination not analysis."

### Probe 3, Disqualification scope

> "Does this constraint disqualify ALL options uniformly? If yes, it's non-information; remove. The constraint set should differentiate options."

### Probe 4, Soft vs hard

> "Is this a 'we'd really not like X' (soft) or 'X cannot happen under any circumstance' (hard)? Only hard ones become Decision Matrix disqualifiers; soft ones become weighted criteria."

### Probe 5, Threshold articulation

> "At what scale does this failure become catastrophic vs minor? Without a threshold, the constraint can't be calibrated."

---

## Forcing Exemplars

### Exemplar 1, Stating a failure path

SOFTENED:
> "There's a risk that users could lose funds during the migration."

FORCING:
> "F1: Funds lost during cross-chain transfer in migration window. Mechanism: user initiates transfer on chain X while chain X's old contract is paused but chain Y's new contract is not yet drained, leading to a stuck message queue. Observable signal: support tickets matching pattern 'transfer X to Y, no balance arrived' over 30 minutes. Evidence: Ronin bridge 2022 incident, Wormhole 2022 incident — same class of stuck-message failures during partial-deployment windows."

### Exemplar 2, Deriving a constraint

SOFTENED:
> "We should make sure funds aren't lost."

FORCING:
> "Constraint C1 (derived from F1): Option must NOT pause the old contract on chain X before the new contract is verified-drained on chain Y. Predicate: the migration sequence has a verified-state checkpoint between old-pause and new-active. Disqualification: any option whose migration sequence lacks this checkpoint scores 0 on C1."

### Exemplar 3, Distinguishing hard from soft

SOFTENED:
> "It would be bad if users had to wait too long during the migration."

FORCING:
> "Soft preference: minimize user-perceived migration latency (this becomes a Decision Matrix criterion 'UX during migration', weighted normally). Hard constraint: NO user transfer can be stuck for more than 4 hours during the migration window (predicate: any option that doesn't bound transfer latency to 4h scores 0 on C2)."

### Exemplar 4, Bounding scope

SOFTENED:
> "Regulation could change."

FORCING:
> "Black-swan path Z1: Cross-chain transfers banned in jurisdiction Y in 2026. Conditions: regulatory rule R passes, our user base in Y is > 10%. Disqualification scope: this disqualifies all options uniformly. Therefore: NOT a Decision Matrix constraint. Move to dissent appendix as 'known unaddressable risk' so the recommendation acknowledges it without filtering."

---

## Output Schema

### Section A, Header

```markdown
# Inversion (Define-Phase), <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Failure paths identified:** <N>
**Constraints derived:** <M>
**Black-swan paths surfaced (dissent only):** <K>
```

### Section B, Failure paths

```markdown
## Failure Paths

### F1: <name>

- **Mechanism:** <what causes the failure sequence>
- **Observable signal:** <how we'd know this happened>
- **Conditions:**
  - Trigger: <initial event>
  - Amplifiers: <what makes it worse>
  - Threshold: <scale at which it becomes catastrophic>
- **Evidence:** <historical case or analog from research>

### F2: ...
```

### Section C, Constraints

```markdown
## Constraints (Decision Matrix disqualifiers)

| ID | Constraint | Predicate (yes/no per option) | Disqualification scope | Source |
|---|---|---|---|---|
| C1 | Option must NOT [...] | Does the option [...]? | all options / subset (which?) | F1 |
| C2 | ... | ... | ... | F2 |
```

### Section D, Black-swan paths

```markdown
## Black-Swan Paths (dissent only, NOT constraints)

- **Z1:** <name>
  - Mechanism: <one line>
  - Why it's not a constraint: disqualifies all options uniformly OR is unaddressable
  - Disposition: surface in dissent appendix; recommendation acknowledges
```

### Section E, Decision Hook

```markdown
## Decision Hook

Decision Matrix Step 1: apply each constraint as a binary filter. Any option violating any constraint scores 0 on that constraint's criterion. If an option violates ≥ 2 constraints, recommend removal from matrix entirely (option is non-viable).

Soft preferences (rejected as constraints) feed the Decision Matrix as weighted criteria.

Black-swan paths feed the dissent appendix.
```

### Section F, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentence synthesis. Name the most binding constraints. Surface any options already known to fail one. Flag the black-swan that most affects the recommendation.>
```

### Section G, Completeness

```markdown
**Completeness:** <N>/10

- 5-10 failure paths with mechanism + signal + conditions: +<N>
- Each failure path has historical evidence: +<N>
- Constraints derived with explicit predicates: +<N>
- Disqualification scope specified per constraint: +<N>
- Soft vs hard distinguished: +<N>
- Black-swan paths separated from constraints: +<N>
```

---

## Decision Hook

Inversion-define feeds Decision Matrix as a hard filter:

1. Decision Matrix Step 1 applies the constraint set BEFORE weighted scoring
2. Any option violating any constraint scores 0 on that constraint's criterion
3. Options violating ≥ 2 constraints are flagged for removal from matrix

Confidence rubric impact:
- All constraints have specific predicates: +0 (baseline)
- Constraints filter ≥ 1 candidate option: +1 (the constraint set is doing its job)
- Constraints filter 0 options across all candidates: -1 (constraints may be non-binding; re-check)

### Override conditions

If inversion-define produces > 15 constraints, the Decision Matrix becomes unscoreable (every option fails something). SendMessage to lead recommending re-prioritization: drop constraints that don't differentiate (apply uniformly across all options) or relax thresholds.

---

## Cross-Framework Triggers

- **All options violate same constraint** → SendMessage to lead recommending re-run of zwicky-box at a different abstraction level
- **No option violates any constraint** → constraints are non-binding; SendMessage flagging this as "constraint set is decoration, not filter"
- **Constraint count > 15** → matrix unscoreable; trigger constraint reduction
- **Black-swan path is highly likely (> 30%)** → SendMessage to lead; this might require re-framing the entire problem (Cynefin = chaotic re-classification)

---

## Failure Modes

### Failure Mode 1, Vague paths produce vague constraints

Trap: failure paths written as categories ("UX issues") rather than specific sequences.

Manifestation: constraints have predicates that cannot be evaluated yes/no per option.

Check: every constraint has a predicate that a downstream scorer can answer in 10 seconds.

Recovery: re-write failure paths with mechanism + signal + threshold; re-derive constraints.

### Failure Mode 2, Constraint inflation

Trap: 20+ constraints generated from 5 failure paths via over-decomposition.

Manifestation: many constraints with similar predicates; matrix becomes unscoreable.

Check: count constraints. If > 15, consolidate. If two predicates overlap > 80%, merge.

Recovery: collapse to canonical 5-10 constraints; the rest become "additional considerations" in dissent.

### Failure Mode 3, Soft preferences disguised as constraints

Trap: "we'd really like X" gets phrased as "must X" and becomes a disqualifier.

Manifestation: constraints disqualify options that the team would actually accept under the right circumstances.

Check: for each constraint, ask "would we ever accept an option that violates this?" If yes, it's soft, not hard.

Recovery: move soft preferences to Decision Matrix as weighted criteria; keep only hard constraints.

### Failure Mode 4, Missing evidence anchors

Trap: failure paths generated by imagination only.

Manifestation: paths cite no historical case; team confidence in the path is low.

Check: every path lists at least one prior case or analogous failure.

Recovery: SendMessage to researcher requesting failure-mode evidence; defer constraint derivation until evidence lands.

### Failure Mode 5, Black-swan creep into constraints

Trap: low-probability unaddressable events added as constraints, disqualifying all options.

Manifestation: a constraint disqualifies every candidate; matrix becomes unscoreable.

Check: scope check on every constraint. If `disqualification_scope = all` and probability is low, re-classify as black-swan.

Recovery: move to dissent appendix; recommendation acknowledges but doesn't filter.

---

## Jargon Glossary

- **failure path**, a specific sequence of events that produces a bad outcome.
- **mechanism**, what causes the failure sequence (the chain of cause-and-effect).
- **observable signal**, how we'd know the failure happened in production.
- **trigger**, the initiating event of a failure path.
- **amplifier**, a condition that makes the failure worse once triggered.
- **threshold**, the scale at which the failure shifts from minor to catastrophic.
- **constraint**, a "must NOT" predicate Decision Matrix uses as a binary disqualifier.
- **predicate**, the yes/no question a downstream scorer asks to test whether an option violates a constraint.
- **disqualification scope**, the subset of options to which a constraint applies.
- **black-swan path**, a low-probability unaddressable failure that goes to dissent, not constraints.
- **soft preference**, a "we'd prefer X" that becomes a Decision Matrix weighted criterion, not a constraint.
- **hard constraint**, a "X cannot happen" that becomes a Decision Matrix disqualifier.
- **pre-mortem**, the practice of imagining the project has already failed and listing why.
- **risk-anchored**, generated from research and prior cases rather than from imagination.

---

## Completeness Scoring

### 10/10, Decisive
- 5-10 failure paths with mechanism + signal + conditions + evidence
- Constraints derived with explicit predicates and scope
- Soft vs hard distinguished
- Black-swans separated to dissent
- Filter test passes (≥ 1 option disqualified by ≥ 1 constraint)

### 7/10, Confident
- 5+ failure paths with most fields populated
- Constraints have predicates but some scopes are implicit
- Soft preferences mostly distinguished

### 4/10, Tentative
- 3-4 failure paths
- Constraints lack predicates or scopes
- Soft preferences mixed with hard constraints
- Few or no evidence anchors

### 0/10, Unusable
- Prose list of "things that could go wrong" without conversion to constraints
- No predicates downstream can evaluate
- Black-swans treated as constraints

Inversion-define completeness ≤ 4 contributes -1 to overall confidence rubric AND flags the Decision Matrix as poorly filtered.

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

### Step 1, Read research evidence

`evidence/define-failure-modes.md` lists 4 historical analogs:
- Ronin bridge 2022 (stuck messages during partial deployment)
- Wormhole 2022 (key compromise during upgrade window)
- Stargate v1→v2 migration (smooth, but had 48h support spike from confused users)
- Radiant Capital (clean migration, but lost ~5% TVL to users who didn't migrate within window)

### Step 2, Generate failure paths

```markdown
### F1: Funds stuck mid-transfer
- Mechanism: user initiates cross-chain transfer while old contract is paused but new contract isn't fully drained; message gets stuck in queue.
- Observable signal: support tickets matching "transfer initiated, no balance" over 30+ minutes.
- Conditions:
  - Trigger: pause OFTv1 on chain X before OFTv2 indexed on chain Y
  - Amplifier: transfer initiated within 60s of pause
  - Threshold: ≥ 5 stuck transfers signals systemic problem
- Evidence: Ronin bridge 2022 (~$500K stuck for 14h)

### F2: Double-spending via replay
- Mechanism: a transfer message replayed on the new contract before the old contract's locked state is properly drained.
- Observable signal: total supply on chain Y exceeds total locked on chain X.
- Conditions:
  - Trigger: insufficient state-checkpoint between old-lock and new-mint
  - Amplifier: high transfer volume during migration window
  - Threshold: any double-spend is catastrophic regardless of scale
- Evidence: multiple bridge replays in 2022-2024; LayerZero docs explicitly warn

### F3: User confusion → wrong-network deposits
- Mechanism: users transfer OFTv1 tokens to OFTv2 deployment address (or vice versa) on a chain where one is paused.
- Observable signal: support tickets about "I sent tokens, they're missing"
- Conditions:
  - Trigger: visible OFTv1 contract still receiving tokens after OFTv2 deployment
  - Amplifier: poor user comms; UI shows both contracts active
  - Threshold: > 10 user reports = systemic comms failure
- Evidence: Stargate v1→v2 had ~150 user-confusion tickets in first 48h

### F4: Audit catches issue post-deployment
- Mechanism: external auditor finds vulnerability in OFTv2 contracts after they're live.
- Observable signal: auditor report flags issue requiring redeploy.
- Conditions:
  - Trigger: deployed OFTv2 to mainnet before auditor signoff
  - Amplifier: TVL ramp during audit window
  - Threshold: any flagged issue = redeploy required
- Evidence: 3+ recent protocol incidents from skipped or rushed audits

### F5: Liquidity dries during migration window
- Mechanism: LP providers withdraw because they don't trust the migration; bridge becomes thin; trades fail.
- Observable signal: LP TVL drops > 30% in 24h.
- Conditions:
  - Trigger: migration announced without clear LP communication
  - Amplifier: ongoing reinforcing cycle (bridge volume → fees → liquidity → bridge volume) flagged in connection-circles
  - Threshold: LP TVL < 60% of pre-migration baseline = trades fail
- Evidence: Curve's 3pool migration had similar LP-flight pattern

### F6: Force-migration deadline fails to engage long-tail
- Mechanism: at force-migration cutover, ~5-10% of users still on OFTv1 with no path to OFTv2.
- Observable signal: long-tail OFTv1 holders complain on social/support.
- Conditions:
  - Trigger: cutover proceeds without UX path for offline users
  - Threshold: ≥ 5% TVL stuck = significant retention failure
- Evidence: Radiant migration lost ~5% TVL to inactive users

### Z1 (black-swan): LayerZero deprecates v1 unexpectedly
- Conditions: LZ announces v1 sunset before our migration completes
- Disposition: black-swan; we don't control LZ roadmap
- Action: surface in dissent; not a constraint
```

### Step 3-4, Derive constraints

```markdown
| ID | Constraint | Predicate | Scope | Source |
|---|---|---|---|---|
| C1 | Option must NOT pause OFTv1 on chain X before OFTv2 verified-drained on chain Y | Does the migration sequence have a verified-state checkpoint between old-pause and new-active? | all options | F1 |
| C2 | Option must include replay protection (proof-of-burn before mint) | Does the migration ensure each token can mint on new only after burn confirmed on old? | all options | F2 |
| C3 | Option must include user-facing comms plan with deprecation date | Is there a documented comms timeline with explicit OFTv1 deprecation date? | all options | F3 |
| C4 | Option must NOT deploy to mainnet before external auditor signoff | Has external auditor signed off on the chosen migration mechanics? | all options | F4 |
| C5 | Option must include LP comms ≥ 2 weeks before migration kickoff | Is LP communication scheduled before bridge changes? | all options | F5 |
| C6 | Option must include force-migration UX for inactive users (e.g. OFTv1→OFTv2 unwrapper) | Is there a path for users who don't migrate during voluntary window? | all options | F6 |
```

### Step 5, Apply

Decision Matrix Step 1 applies these constraints to the 4 archetypes from Zwicky:
- A (big-bang): violates C1 (no checkpoint between old-pause and new-active by definition); scores 0 on C1.
- B (dual-deploy + drain): satisfies C1 by construction. Constraint compliance high.
- C (wrapped legacy): satisfies C1 (no pause); satisfies most others; complies broadly.
- D (separate token + voluntary): violates C6 by design (voluntary by nature, no force-migration UX).

Pre-matrix outcome:
- A: violates C1 → scores 0 on C1; can still score on other criteria but flagged as constraint-failing
- B: complies with all 6 constraints → enters matrix at full strength
- C: complies → enters matrix at full strength
- D: violates C6 → scores 0 on C6; moves toward elimination

### Output completeness

- 6 failure paths with mechanism + signal + conditions + evidence: yes
- 6 constraints derived with predicates: yes
- Disqualification scopes specified: yes
- 1 black-swan separated to dissent: yes
- Filter test passes (3 of 4 options disqualified by ≥ 1 constraint): yes

**Completeness: 9/10** (minus 1 for not explicitly testing whether C1 should be raised to "constraint that Decision Matrix removes from matrix entirely" rather than a 0-score on one criterion).

---

## What This Means For The Decision

Inversion-define produced 6 named failure paths, derived 6 hard constraints, surfaced 1 black-swan. The constraint set immediately disqualifies option A (big-bang violates C1 by design) and option D (separate token violates C6 by design). The matrix now scores B vs C with full constraint compliance, which previews B as the winner.

Without inversion-define, options A and D enter the Decision Matrix as full candidates and dilute the weighted scoring. With it, the matrix only weighs viable candidates and the recommendation is grounded in failure-aware filtering, not just upside-aware scoring.
