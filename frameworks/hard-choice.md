# Hard Choice Model (Ruth Chang)

**Phase:** Decide · **Source:** https://untools.co/hard-choice-model

Hard choices are not better/worse. They're **on a par**. Standard cost-benefit fails because no option dominates on all dimensions. Ruth Chang's framework recasts the question: not "which is better?" but "who do we become by choosing this?" Hard choices are self-defining. Trying to optimize them is the wrong frame.

This is a conditional framework. It only fires when the decision is genuinely hard, not just unfamiliar. Most decisions aren't on a par; one option does dominate the others on the criteria the team actually weights. Hard Choice exists for the small fraction of decisions where Decision Matrix legitimately can't break the tie.

---

## Entry Predicate

```
intake.reversibility = "one-way-door" 
∨ frameworks/decision-matrix.md::top_2_within_5pct
```

The framework fires when:
- The decision is hard to reverse (one-way-door) — even if Decision Matrix has a clear winner, reversibility raises the bar
- Decision Matrix's top two options scored within 5% of each other (genuine parity)

Otherwise: skip with explicit predicate evaluation in output.

### Inputs

- `intake.reversibility`
- `frameworks/decision-matrix.md::scores` (the top 2)
- `frameworks/zwicky-box.md::archetypes` (named values per option)
- `intake.success_criteria`

### Outputs

- `$RUN_DIR/frameworks/hard-choice.md` — predicate evaluation + (if fired) full method output

---

## Operating Principles

**1. Parity is real, not failure.**

When Decision Matrix's top two are within 5%, that's not a tie to break with a tiebreaker rule. It's a signal that the criteria don't capture the full decision. Standard tiebreakers (cost, time) often rank-shuffle without addressing the actual difference. Anti-pattern: applying a "secondary criterion" that pretends to break the tie but just hides the parity.

**2. Hard choices are about identity, not optimization.**

The framework asks: which option does the team commit to as their own? Which version of the team do we become by choosing? That's not a preference question; it's a commitment question. Anti-pattern: treating Hard Choice as a personality test ("which feels right") rather than a commitment test ("which can we defend").

**3. Commitment is two-sided, not pro/con.**

The framework doesn't ask "which has more upside." It asks: can we commit our reasons and our agency to A? Can we commit them to B? Often the answer is "yes to both" or "no to both." That's the actual finding. Anti-pattern: forcing a binary "we choose A" when the honest finding is "we can commit to either."

**4. Override Decision Matrix when triggered.**

When Hard Choice fires, its conclusion replaces Decision Matrix's recommendation. The matrix scores become supporting evidence, not the call. Anti-pattern: running Hard Choice but reverting to Decision Matrix's higher-scored option because "we have the data."

**5. Skip with predicate evaluation when not triggered.**

Most runs don't trigger Hard Choice. The framework still runs (writes a file) to document the predicate evaluation. This makes the skip auditable: "we considered Hard Choice, here's why it didn't fire." Anti-pattern: silently omitting the framework, leaving future runs unable to tell whether the skip was deliberate.

---

## Response Posture

**Tone.** Philosophical-practical. The framework draws on identity questions but anchors every claim to specific options and evidence.

**Pacing.** Two-stage. Stage 1: evaluate predicate. Stage 2 (only if fired): full method.

**Push depth.** If fired, may require user input via SendMessage to lead because the commitment test depends on what the team is willing to be defined by. The framework can write a recommendation but the lead may want to surface to user for confirmation.

**Where to escalate.** SendMessage to lead when:
- Predicate fires AND Decision Matrix has clear winner (intake.reversibility = one-way-door but Decision Matrix top-2 gap > 5%; flag the conflict)
- Commitment test produces "yes to both" or "no to both" (true parity; recommendation may need to come from user, not framework)
- Both options have equally compelling values stories (the framework can't differentiate; user judgment required)

---

## Anti-Sycophancy Rules

Never write:
- "Both options have merit..." (state the parity explicitly)
- "It depends on what we value..." (name the values; force the team to articulate them)
- "The right answer depends on context..." (the context is intake; use it)
- "There's no perfect choice..." (Hard Choice exists precisely because there's no perfect choice; that's not an excuse)

Always:
- State the predicate evaluation up front. Did it fire? Why?
- If fired, name the values at stake on each side specifically.
- If fired, name who the team becomes by choosing each option.
- State the framework's recommendation as commitment, not optimization.

---

## Pushback Patterns

**Pattern 1: "Just pick the higher-scored option" then check reversibility**

- Internal evidence: Decision Matrix top is 8.2, runner-up is 7.9 (gap < 5%), reversibility = costly.
- BAD: Recommend higher-scored option.
- GOOD: This is exactly when Hard Choice fires. The 5% gap means Decision Matrix can't differentiate confidently; reversibility = costly raises the bar. Run the full method.

**Pattern 2: "We need more criteria to break the tie" then surface the real question**

- Internal pull: add weighted criteria until one option pulls ahead.
- BAD: Add tiebreaker criteria.
- GOOD: Recognize that adding criteria to force a winner is hiding the parity. Run Hard Choice. The parity itself is information about how the team thinks.

**Pattern 3: "Personal preference" then anchor in commitment**

- Internal evidence: agent reduces Hard Choice to "which feels right."
- BAD: Frame as preference question.
- GOOD: Reframe as commitment question. "Do we commit our reasons + agency to A? Do we commit them to B?" The commitment test is reproducible; preference isn't.

**Pattern 4: "Hard Choice means we can't decide" then anchor in self-definition**

- Internal pull: report the parity and stop.
- BAD: "We can't differentiate between A and B."
- GOOD: Apply the self-definition test. "Choosing A makes us a team that values <X>. Choosing B makes us a team that values <Y>. Which identity do we commit to?" That produces a recommendation; pure cost-benefit doesn't.

**Pattern 5: "Override Decision Matrix" then verify framework actually fired**

- Internal pull: assume Hard Choice always overrides matrix.
- BAD: Override even when predicate didn't fire.
- GOOD: Override only when predicate fires (one-way-door OR top-2 within 5%). Otherwise Decision Matrix dominates and Hard Choice is a documented skip.

---

## Method

Two-stage procedure: predicate then full method.

### Stage 1, Predicate evaluation (always run)

Read the inputs and evaluate:

```python
predicate_fires = (
    intake.reversibility == "one-way-door"
    or
    abs(decision_matrix.top_score - decision_matrix.runner_up_score) / decision_matrix.top_score < 0.05
)
```

Document the evaluation:
- `intake.reversibility` value
- Decision Matrix top score and runner-up score
- Gap percentage
- Predicate result (fired / skipped)

If skipped, write the output document with predicate evaluation only and stop.

### Stage 2, Full method (only if fired)

#### Step 2.1, Acknowledge parity

State: "These options are on a par. Neither dominates on all the dimensions we care about." Cite the matrix scores and gap.

#### Step 2.2, Identify values per option

For each of the top 2 options, write 3-5 values it embodies:
- What does choosing this option say about our priorities?
- What capabilities does this option preserve or build?
- What kind of team does it require us to be?

#### Step 2.3, Commitment test per option

For each option, ask:
- Can we commit our reasons to this option (i.e. defend it publicly to stakeholders)?
- Can we commit our agency to this option (i.e. do the work it requires without resentment)?
- If yes to both: option is committable.
- If no to either: option is not committable.

#### Step 2.4, Self-definition statement

For each committable option, write:
- "Choosing this makes us a team that <identity statement>"
- "We commit to becoming <identity> by choosing this."

#### Step 2.5, Recommendation

If exactly one option is committable: recommend it.
If both are committable: recommend the one whose self-definition the team most wants to commit to (this may require SendMessage to lead for user input).
If neither: recommend "do not decide yet; gather more evidence" (rare but real).

---

## Probe Patterns

### Probe 1, Is the predicate firing?

> "What's `intake.reversibility`? What's the Decision Matrix gap? Run the formula. Does it fire?"

### Probe 2, Are these options actually on a par?

> "If I added more criteria, would one option pull ahead naturally? If yes, this isn't true parity; it's a measurement gap. Don't run full method; ask Decision Matrix to expand criteria."

### Probe 3, What does each option commit us to?

> "If I imagine the team 6 months after choosing A, what do they look like? Same for B. The two pictures should be different. If they're the same, I'm not naming the actual differences."

### Probe 4, Can we defend each publicly?

> "If I had to write a 1-page memo to stakeholders justifying choice A, could I do it? Same for B. If one option's memo is hard to write, that's commitment failure, not preference failure."

### Probe 5, Is the recommendation a commitment or an optimization?

> "Did I produce 'A is better than B by metric X' (optimization, wrong frame) or 'we commit to becoming the team that chose A' (commitment, right frame)?"

---

## Forcing Exemplars

### Exemplar 1, Stating predicate evaluation

SOFTENED:
> "Hard Choice may apply here."

FORCING:
> "Predicate evaluation: intake.reversibility = costly (NOT one-way-door, fails first half). Decision Matrix top score 8.2 (B: dual-deploy+drain), runner-up 6.7 (C: wrapped legacy), gap = 18% (>> 5% threshold, fails second half). Predicate does NOT fire. Hard Choice skipped for this run."

### Exemplar 2, Stating a values story

SOFTENED:
> "Option A reflects our values."

FORCING:
> "Choosing big-bang single-cutover commits us to:
> - speed and clarity over caution (single transition, no dual-contract overhead)
> - high-confidence engineering culture (we trust our deploy mechanics)
> - operational simplicity (one contract path, fewer maintenance modes)
> Choosing dual-deploy + drain commits us to:
> - safety over speed (drain mechanism gives users control)
> - documented-best-practice alignment (we follow LayerZero's recommendation)
> - higher operational complexity (4 weeks of dual-contract maintenance) with lower headline risk"

### Exemplar 3, Commitment test

SOFTENED:
> "Both options seem viable."

FORCING:
> "Commitment test for option A: can we publicly defend big-bang to LP investors after seeing Wormhole 2022? Marginal — we'd need to point to our specific risk-mitigation differentiator. Can we commit our agency? Yes; eng team is excited.
>
> Commitment test for option B: can we publicly defend dual-deploy to LPs? Easily — we're following the published best-practice. Can we commit agency? Yes; ops team prefers this; eng accepts it.
>
> A is marginally committable. B is fully committable. Recommendation: B."

### Exemplar 4, Self-definition statement

SOFTENED:
> "Choosing dual-deploy means we're being cautious."

FORCING:
> "Choosing dual-deploy + drain means we commit to becoming a team that ships migrations the boring documented way, that values reproducible-LP-trust over engineering-prestige, and that accepts 4 weeks of dual-contract complexity as a tax on lower headline risk. We commit to becoming that team because the alternative (the prestige team that pulls off a big-bang) is the version that exists right up until the moment a stuck transaction makes the local 7am Slack thread."

---

## Output Schema

### Section A, Header

```markdown
# Hard Choice, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Predicate evaluation:** <FIRED / SKIPPED>
**Reversibility:** <intake.reversibility>
**Decision Matrix top-2 gap:** <N%>
```

### Section B, Predicate evaluation

```markdown
## Predicate Evaluation

| Test | Value | Threshold | Result |
|---|---|---|---|
| intake.reversibility = "one-way-door" | <value> | one-way-door | <yes/no> |
| Decision Matrix top-2 within 5% | <gap%> | < 5% | <yes/no> |

**Predicate result:** <FIRED if either yes / SKIPPED if both no>
```

### Section C (only if fired), Full method output

```markdown
## Parity Acknowledgment

The two top options are on a par:
- A (<name>): Decision Matrix score <N>
- B (<name>): Decision Matrix score <N>
- Gap: <%>

Standard cost-benefit cannot differentiate confidently. Hard Choice applies.

## Values Per Option

### A: <name>
- Value 1: <one line>
- Value 2: <one line>
- Value 3: <one line>

### B: <name>
- Value 1: <one line>
- Value 2: <one line>
- Value 3: <one line>

## Commitment Test

| Option | Can defend publicly? | Can commit agency? | Committable? |
|---|---|---|---|
| A | <yes / marginal / no> | <yes / no> | <yes / no> |
| B | <yes / marginal / no> | <yes / no> | <yes / no> |

## Self-Definition

### Choosing A
We commit to becoming a team that <identity statement>.

### Choosing B
We commit to becoming a team that <identity statement>.

## Recommendation

<Recommendation: A / B / neither (gather evidence first)>

Reason: <commitment-anchored, not optimization-anchored>
```

### Section D, Decision Hook (always)

```markdown
## Decision Hook

If FIRED, this framework's recommendation overrides Decision Matrix's. Decision Matrix scores become supporting evidence.

If SKIPPED, Decision Matrix's recommendation stands.

In either case, the recommendation feeds Minto's pyramid synthesis as the Answer.
```

### Section E, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentence synthesis. State whether predicate fired, what the recommendation is, and why this framework's commitment frame produced a different/aligned answer than pure optimization.>
```

### Section F, Completeness

```markdown
**Completeness:** <N>/10
- Predicate evaluated explicitly: +<N>
- If fired: parity acknowledged with score gap: +<N>
- If fired: 3+ values per option: +<N>
- If fired: commitment test answered for both options: +<N>
- If fired: self-definition statements written: +<N>
- If fired: recommendation is commitment-anchored: +<N>
```

---

## Decision Hook

When triggered, Hard Choice replaces Decision Matrix's recommendation as the canonical recommendation. Decision Matrix scores become supporting evidence.

When skipped, Decision Matrix's recommendation stands and Hard Choice's output is just the predicate-evaluation paragraph.

Confidence rubric impact:
- Predicate evaluated cleanly (fired or skipped): +0 (baseline)
- Fired AND recommendation aligns with Decision Matrix top: +1 (commitment confirms scoring)
- Fired AND recommendation differs from Decision Matrix top: -1 (frameworks disagree; surface in dissent)
- Fired AND result is "neither" (no committable option): -2 (run is in DEFER mode regardless)

### Override conditions

When Hard Choice fires AND produces a recommendation, that recommendation is the Decision Matrix-overriding canonical answer. Minto reads from Hard Choice, not Decision Matrix.

---

## Cross-Framework Triggers

- **Predicate fires AND result is "neither committable"** → mark `state.DEFER_MODE = true`; recommendation downgrades to "gather evidence first"
- **Predicate fires AND recommendation differs from Decision Matrix top** → SendMessage to lead flagging the framework disagreement; surface in Dissent
- **Predicate skipped AND intake.reversibility = costly AND top-2 gap < 10%** → mark `state.MARGINAL_GAP = true`; Confidence-Speed-Quality reads this as a flag for QUALITY mode

---

## Failure Modes

### Failure Mode 1, Forced firing

Trap: predicate doesn't actually fire but agent runs full method anyway because the decision "feels hard."

Manifestation: Stage 1 evaluation shows skip, but Stage 2 ran.

Check: Stage 2 should not execute if predicate fails.

Recovery: revert to Stage 1 only; document why the decision feels hard but doesn't meet predicate (e.g. "novel territory" — that's not parity, that's unfamiliarity).

### Failure Mode 2, Optimization disguised as commitment

Trap: framework writes "we commit to A because it scores higher on X."

Manifestation: recommendation cites quantitative scoring rather than identity/commitment.

Check: recommendation must be a commitment statement, not a comparison statement.

Recovery: re-write recommendation. "We commit to becoming the team that values <Y>" not "A is better on metric X."

### Failure Mode 3, Personality mistaken for commitment

Trap: agent recommends based on which feels right.

Manifestation: justification has no public-defensibility test.

Check: every recommendation answers "could we defend this publicly?" If not addressed, redo.

Recovery: run the public-defensibility test explicitly; if option fails, downgrade committability.

### Failure Mode 4, Both committable, no recommendation

Trap: Stage 2 ends with "both are committable" and stops.

Manifestation: no recommendation in output.

Check: framework must produce recommendation OR "neither (DEFER)" verdict.

Recovery: SendMessage to lead requesting user input on which identity to commit to.

### Failure Mode 5, Skipped without predicate evaluation

Trap: Stage 1 omitted in output; framework just labeled "skipped."

Manifestation: no predicate values shown.

Check: even when skipped, output must show inputs + threshold + result.

Recovery: write Stage 1 properly so future runs can audit the skip.

---

## Jargon Glossary

- **on a par**, two options that are neither better nor worse on the dimensions used to evaluate them; characteristic of hard choices.
- **commitment test**, can we (a) publicly defend this choice to stakeholders, (b) commit our agency to executing it without resentment.
- **self-definition**, the identity the team adopts by choosing this option.
- **one-way-door**, decision that is costly or impossible to reverse; raises the Hard Choice bar.
- **predicate**, the formal condition that determines whether Hard Choice runs.
- **parity gap**, the percentage difference between Decision Matrix top and runner-up scores; < 5% triggers the framework.
- **optimization frame**, treating the decision as "which is better"; the wrong frame for hard choices.
- **commitment frame**, treating the decision as "who do we become"; the right frame for hard choices.
- **public-defensibility**, can we write a 1-page memo justifying this choice to stakeholders without hand-waving.
- **agency commitment**, willingness to do the work the option requires without internal resistance.
- **DEFER**, when neither option passes the commitment test; recommendation becomes "gather evidence first."

---

## Completeness Scoring

### 10/10, Decisive
- Stage 1 predicate evaluation shown with all inputs + threshold + result
- If fired: parity acknowledged
- If fired: 3+ values per option
- If fired: commitment test for both options
- If fired: self-definition statements
- If fired: recommendation is commitment-anchored

### 7/10, Confident
- Stage 1 evaluation present
- If fired: most fields filled, some abbreviated

### 4/10, Tentative
- Predicate evaluated implicitly
- If fired: values listed but commitment test missing

### 0/10, Unusable
- No predicate evaluation
- If fired: optimization-style recommendation rather than commitment

Hard Choice completeness ≤ 4 contributes -1 to overall rubric IF predicate fired.

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

### Stage 1, Predicate evaluation

| Test | Value | Threshold | Result |
|---|---|---|---|
| intake.reversibility = "one-way-door" | costly | one-way-door | NO |
| Decision Matrix top-2 within 5% | gap = 18% (B: 8.2, C: 6.7) | < 5% | NO |

**Predicate result:** SKIPPED. Both halves of the predicate fail.

For OFTv2, reversibility is costly (re-deploying OFTv1 + convincing users to migrate back is multi-week work) but not one-way-door (it's expensive, not impossible). The Decision Matrix gap between B (dual-deploy+drain, 8.2) and C (wrapped legacy, 6.7) is 18%, well above the 5% parity threshold. Decision Matrix's pick stands.

### Stage 2, Full method (NOT RUN for OFTv2)

For demonstration of the framework's mechanics on a different problem where the predicate WOULD fire, here is a secondary worked example.

#### Secondary problem: "Should I take the new job?"

Predicate evaluation:
- intake.reversibility = "one-way-door" (declining the offer means losing it; accepting means leaving current team)
- Decision Matrix top-2 gap: stay 7.4, accept 7.6 (gap = 3%, BELOW 5%)
- **Predicate FIRES on both halves.**

Full method output:

##### Parity acknowledgment
Stay at current job (DM 7.4) and accept new job (DM 7.6) are on a par. The 3% gap is noise relative to the criteria's resolution.

##### Values per option

**Stay (current job):**
- Value 1: continuity with team I helped build over 3 years
- Value 2: deep domain expertise that compounds annually
- Value 3: known unknowns about org direction

**Accept (new job):**
- Value 1: faster compensation curve and equity
- Value 2: novel domain (web3 from web2 background) that resets compounding clock
- Value 3: unknown team dynamics

##### Commitment test

| Option | Can defend publicly? | Can commit agency? | Committable? |
|---|---|---|---|
| Stay | yes (continuity argument is clear) | yes (no resentment about doing this work) | yes |
| Accept | marginal (compensation argument feels small in 5-year frame) | yes (excitement is genuine) | marginal |

##### Self-definition

**Choosing stay:** we commit to becoming the engineer who builds compounding expertise over time and trusts that depth produces opportunities.

**Choosing accept:** we commit to becoming the engineer who resets the clock to chase a domain shift, betting that the new domain compounds faster than the old one.

##### Recommendation

**Stay.** The commitment test favors staying because:
- Public defensibility is stronger (continuity story is harder to argue against than compensation story)
- Self-definition is more compatible with the team's stated values around depth
- Decision Matrix's marginal preference for accept doesn't override the commitment test

This recommendation differs from Decision Matrix's. The commitment frame produced a clearer answer than the optimization frame.

### Step 5, Output for OFTv2 specifically

For the OFTv2 problem, the framework output is short:

```markdown
# Hard Choice, should-we-migrate-to-oftv2

**Predicate evaluation:** SKIPPED.

| Test | Value | Threshold | Result |
|---|---|---|---|
| intake.reversibility = "one-way-door" | costly | one-way-door | NO |
| Decision Matrix top-2 within 5% | 18% | < 5% | NO |

Decision Matrix recommendation (B: dual-deploy + drain, score 8.2) stands. Hard Choice does not override.

## What This Means For The Decision

This run does not need a Hard Choice. The Decision Matrix produced a clear winner with sufficient gap. The framework's predicate evaluation is documented for audit purposes; future runs on similar problems can confirm Hard Choice was considered and rejected.

**Completeness: 9/10** (full predicate evaluation, full reasoning, secondary worked example for framework mechanics).
```

---

## What This Means For The Decision

Hard Choice for OFTv2 is a documented skip. The predicate doesn't fire because the decision is costly (not one-way-door) and Decision Matrix produced an 18% gap (well above the 5% parity threshold). Decision Matrix's recommendation (dual-deploy + drain) stands.

The framework's value across runs is in the dual demonstration. By writing the predicate evaluation in every run, /solve produces an audit trail that says "we considered Hard Choice and here's why it didn't apply." When the predicate does fire (on a different problem), the framework produces a recommendation that overrides Decision Matrix because the commitment frame is more honest than the optimization frame for genuinely hard choices.

The cost of skipping the framework: confident recommendations on parity-class decisions where the team commits to the wrong identity. The value of running it (even when it skips): every run can defend why the decision wasn't a hard choice, and the rare runs where it fires get the right frame from the start.
