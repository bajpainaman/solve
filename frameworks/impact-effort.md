# Impact-Effort Matrix

**Phase:** Decide · **Source:** https://untools.co/impact-effort-matrix

A 2×2 matrix on Impact × Effort that classifies each candidate option into Quick Wins, Big Bets, Fill-Ins, or Thankless work. Where Decision Matrix asks "which option scores best on weighted criteria," Impact-Effort asks "is the cost worth it?" Both views matter. A high-criteria option that's also Thankless quadrant is rarely the right move.

Where Eisenhower triages on Urgency × Importance, Impact-Effort triages on Impact × Effort. They feed different downstream decisions: Eisenhower decides whether to act now or schedule, Impact-Effort decides whether the action is worth the spend.

---

## Entry Predicate

```
always_run if |options| ≥ 2
skip if Decision Matrix produced a single dominant option
```

The framework needs at least two candidates to compare. If only one option survives prior phases, skip and write a one-paragraph note pointing to the dominant option.

### Inputs

- `frameworks/decision-matrix.md::options` (preferred source, scored options)
- `frameworks/zwicky-box.md::archetypes` (fallback if Decision Matrix hasn't run)
- `frameworks/eisenhower.md::do_now` and `::schedule` (filter; only options not in DROP)
- `intake.reversibility` (modifies how harshly Big Bets are weighted)
- `frameworks/cynefin.md::routing` (complex domain raises Big Bet bar)

### Outputs

- `$RUN_DIR/frameworks/impact-effort.md` — 2×2 plot + per-quadrant entries + summary table

---

## Operating Principles

**1. Impact is decision-criteria-anchored, not gut-anchored.**

Impact = degree to which the option moves `intake.success_criteria`. Anti-pattern: scoring impact based on how exciting the option is, or how loud someone is advocating for it.

**2. Effort is total cost, not just engineering hours.**

Effort = engineering time + audit time + comms time + opportunity cost + ongoing maintenance burden. A "small code change" that requires a 4-week audit is High Effort. Anti-pattern: scoring effort as just the visible build time.

**3. Big Bets need the highest confidence to commit.**

Big Bets (high impact + high effort) consume the most resources and have the largest downside if wrong. Cynefin domain modifies the threshold: simple/complicated allows Big Bets at rubric ≥ 7; complex requires rubric ≥ 8 plus PROBE-mode validation. Anti-pattern: committing a Big Bet under medium confidence because the upside is large.

**4. Quick Wins ship even at medium confidence.**

Quick Wins (high impact + low effort) compound. Their low cost makes the downside cheap. Ship them at rubric ≥ 6 when they don't conflict with the larger Big Bet. Anti-pattern: holding Quick Wins for "after the big migration" when shipping them now is cheap.

**5. Thankless quadrant entries are surfaced in Dissent, not buried.**

If a candidate option lands in Thankless (low impact + high effort), it appears in the Dissent appendix with a "considered and rejected" entry. This prevents future runs from re-introducing the same dud. Anti-pattern: silently dropping Thankless entries; they'll come back next run.

---

## Response Posture

**Tone.** Cost-benefit triage. Each option gets a brief, decisive placement and a one-line implication. No prose padding.

**Pacing.** Single pass after Decision Matrix completes. The framework reads matrix scores + intake + cynefin domain, plots each option, generates per-quadrant entries.

**Push depth.** Zero direct user questions. If a candidate option's effort is unclear (e.g. an unknown audit duration), mark `effort_unknown` and SendMessage to lead requesting estimate or research task to scope.

**Where to escalate.** SendMessage to lead when:
- 3+ options land in Big Bet (the team is over-committing; pick at most 2)
- 0 options in Quick Win (option list lacks scrappy alternatives; suggest re-running zwicky-box looking for narrower wedges)
- Top Decision Matrix winner lands in Thankless (Decision Matrix and Impact-Effort disagree; surface the conflict)

---

## Anti-Sycophancy Rules

Never write:
- "All options have potential..." (potential is not impact)
- "It's hard to estimate effort accurately..." (estimate it; flag the uncertainty)
- "Big Bets can pay off..." (the question is whether THIS Big Bet pays off, not whether bets in general can)

Always:
- State each option's quadrant. Name the impact source. Name the effort cost.
- For every Big Bet, name the confidence threshold needed to commit.
- For every Thankless, name what was lost by considering it.

---

## Pushback Patterns

**Pattern 1: "It's high impact AND low effort" then check effort scope**

- Internal evidence: option marked Quick Win.
- BAD: Accept the placement.
- GOOD: Re-read effort. Does it include audit time? Comms time? Ongoing maintenance? If any of these are non-trivial, the option is not actually Low Effort. Most "Quick Wins" turn into Fill-Ins or Big Bets when total cost is honestly accounted.

**Pattern 2: "Big Bet but big upside" then check confidence**

- Internal evidence: option marked Big Bet, advocate is excited.
- BAD: Recommend committing because upside is high.
- GOOD: Pull confidence rubric (computed by Step 11 of SKILL.md, but provisional view available from running framework outputs). If rubric < threshold for cynefin domain, flag in Dissent that Big Bet exceeds confidence; recommendation must downgrade to PROBE mode.

**Pattern 3: "Thankless but someone wants it" then surface explicitly**

- Internal evidence: option lands in Thankless but a stakeholder advocated for it.
- BAD: Move to Fill-In to avoid surfacing the rejection.
- GOOD: Keep it in Thankless. Write the rejection reason explicitly. Adding the advocate's name (if known) to the dissent entry shows respect for the input while documenting why it didn't win.

**Pattern 4: "Quick Win but low impact" then re-check**

- Internal evidence: option marked Quick Win but barely moves success criteria.
- BAD: Ship as Quick Win on principle.
- GOOD: Re-classify. Quick Wins require high impact. If impact is low, this is Fill-In. Fill-Ins ship only when there's spare capacity and they don't compete with Big Bets.

**Pattern 5: "Two Big Bets, both compelling" then narrow**

- Internal evidence: 2 candidates in Big Bet.
- BAD: Recommend both.
- GOOD: Run Hard Choice if not already triggered. The team can rarely commit two Big Bets simultaneously. Force a choice or sequence them explicitly with a gate between (Big Bet A first, then re-evaluate Big Bet B based on Bet A outcomes).

---

## Method

5-step procedure.

### Step 1, Gather options

```bash
# Use Decision Matrix output if available
[ -f $RUN_DIR/frameworks/decision-matrix.md ] && \
  OPTIONS_SOURCE=$RUN_DIR/frameworks/decision-matrix.md || \
  OPTIONS_SOURCE=$RUN_DIR/frameworks/zwicky-box.md

# Filter out Eisenhower DROPs
[ -f $RUN_DIR/frameworks/eisenhower.md ] && \
  EXCLUDED=$(grep -A 100 "## DROP" $RUN_DIR/frameworks/eisenhower.md | grep -E "^- \*\*" | sed 's/- \*\*\(.*\)\*\*.*/\1/')
```

Read the option list. Apply Eisenhower's DROP filter (don't classify already-dropped options).

### Step 2, Score Impact 0-3 per option

Score against `intake.success_criteria`:
- 3 = directly moves the success criterion; primary effect
- 2 = supports the success criterion; secondary effect
- 1 = adjacent; tertiary effect
- 0 = unrelated (consider whether option should be in the list at all)

Cite the success criterion explicitly: "Impact = 3 because option B directly drives TVL retention via Y mechanism."

### Step 3, Score Effort 0-3 per option

Total effort across all dimensions:
- 0 = trivial (< 1 day total work, no external dependencies)
- 1 = small (1-5 days, minimal dependencies)
- 2 = medium (1-3 weeks, some external coordination)
- 3 = large (1+ months, multiple teams or audits, significant maintenance burden)

Include in the estimate:
- Engineering time
- Audit / review time
- Communications / coordination
- Onboarding / documentation
- Ongoing maintenance burden
- Opportunity cost (what doesn't ship because of this)

### Step 4, Place in quadrant

```
              EFFORT
              Low (0-1)             High (2-3)
   ┌───────────────────────┬───────────────────────┐
H  │   QUICK WIN           │   BIG BET             │
i  │   ship at rubric ≥ 6  │   ship at rubric ≥ 7  │
g  │                       │   (≥ 8 if cynefin =   │
h  │                       │    complex)           │
   ├───────────────────────┼───────────────────────┤
L  │   FILL-IN             │   THANKLESS           │
o  │   ship if spare       │   reject; document    │
w  │   capacity            │   in Dissent          │
   └───────────────────────┴───────────────────────┘
        IMPACT
```

Rules:
- **Quick Win** = Impact ≥ 2, Effort ≤ 1
- **Big Bet** = Impact ≥ 2, Effort ≥ 2
- **Fill-In** = Impact ≤ 1, Effort ≤ 1
- **Thankless** = Impact ≤ 1, Effort ≥ 2

### Step 5, Write per-quadrant entries

For each populated quadrant, document the implication:
- Quick Wins: "ship now at rubric ≥ 6"
- Big Bets: "commit at rubric ≥ 7 for simple/complicated; ≥ 8 for complex; downgrade to PROBE if below"
- Fill-Ins: "queue if spare capacity; otherwise defer"
- Thankless: "reject; appears in Dissent appendix"

---

## Probe Patterns

### Probe 1, Total cost honesty

> "Is my Effort score covering audit + comms + ongoing maintenance, or just build time? If just build time, raise Effort by 1."

### Probe 2, Impact decay over time

> "Does this option's impact persist after shipping, or does it depreciate? If depreciation is fast (e.g. cosmetic UX fix), downgrade Impact by 1 unless the option is part of a chain."

### Probe 3, Cynefin-domain calibration

> "Reading `cynefin.domain`, is the Big Bet threshold here ≥ 7 (simple/complicated) or ≥ 8 (complex)? Use the right threshold."

### Probe 4, Effort uncertainty

> "What's the 90% confidence interval on the effort estimate? If wide, mark `effort_uncertain` and recommend a research task to scope."

### Probe 5, Reversibility check

> "If `intake.reversibility = one-way-door`, raise the Big Bet threshold by 1. One-way-door Big Bets need rubric ≥ 8 to commit even in simple domain."

---

## Forcing Exemplars

### Exemplar 1, Stating quadrant placement

SOFTENED:
> "Option B looks like it could be a high-impact option that would require significant effort."

FORCING:
> "Option B (dual-deploy + drain) is BIG BET. Impact = 3 (directly drives TVL retention; the central success criterion). Effort = 3 (4-6 weeks of eng + 2-week external audit + user comms + ongoing dual-contract maintenance for ~4 weeks). Threshold to commit: rubric ≥ 7 (cynefin = complicated). Currently rubric ~9, exceeds threshold."

### Exemplar 2, Surfacing a Thankless

SOFTENED:
> "Option D (separate token) might not be the most efficient path."

FORCING:
> "Option D (separate token + voluntary migration) is THANKLESS. Impact = 1 (only ~30% of users migrate voluntarily; remaining 70% in OFTv1 means we still own the original problem). Effort = 2 (deploy new token contracts + comms infrastructure for migration). Rejected because: solves nothing for the bulk of users; creates a long-tail support burden for the remaining 70% indefinitely. Documented in Dissent."

### Exemplar 3, Quick Win callout

SOFTENED:
> "Option G (user comms plan) is something we could do."

FORCING:
> "Option G (user comms plan) is QUICK WIN. Impact = 2 (improves user trust during cutover; supports retention indirectly). Effort = 1 (1-week product team draft). Threshold to ship: rubric ≥ 6. Currently rubric provisional 7, ship in parallel with Big Bet."

### Exemplar 4, Big Bet downgrade to PROBE

SOFTENED:
> "Option A (big-bang single-cutover) has high upside but might be risky."

FORCING:
> "Option A (big-bang single-cutover) is BIG BET. Impact = 3 (single transition, no dual-contract overhead). Effort = 2 (2-week eng + 1-week audit). Threshold for commit: rubric ≥ 7 because cynefin = complicated. BUT inversion-define flagged big-bang as failure-amplifying (any incident becomes catastrophic). Confidence-Speed-Quality must downgrade to PROBE for big-bang specifically: validate on Base testnet first; only commit after probe succeeds. Decision Matrix accounts for this with weight on reversibility."

---

## Output Schema

### Section A, Header

```markdown
# Impact-Effort Matrix, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Cynefin domain:** <from cynefin.md>
**Big Bet threshold:** <≥ 7 / ≥ 8 / + 1 if reversibility=one-way-door>
**Options classified:** <N>
```

### Section B, Visual matrix

```
              EFFORT
              Low (0-1)             High (2-3)
   ┌───────────────────────┬───────────────────────┐
H  │   QUICK WIN           │   BIG BET             │
i  │   <option list>       │   <option list>       │
g  │                       │                       │
h  │                       │                       │
   ├───────────────────────┼───────────────────────┤
L  │   FILL-IN             │   THANKLESS           │
o  │   <option list>       │   <option list>       │
w  │                       │                       │
   └───────────────────────┴───────────────────────┘
        IMPACT
```

### Section C, Per-quadrant entries

```markdown
### QUICK WINS

- **<option>**
  - Impact: <0-3>, Effort: <0-3>
  - Reason: <one-line>
  - Ship threshold: rubric ≥ 6
  - Implication: <ship now / queue alongside Big Bet / etc>

### BIG BETS

- **<option>**
  - Impact: <0-3>, Effort: <0-3>
  - Reason: <one-line>
  - Ship threshold: rubric ≥ <7 or 8>
  - Cynefin gate: <simple/complicated → 7; complex → 8; +1 if one-way-door>
  - Currently provisional rubric: <N>
  - Mode if below threshold: <PROBE / DEFER>

### FILL-INS

- **<option>**
  - Impact: <0-3>, Effort: <0-3>
  - Implication: queue if spare capacity; defer otherwise

### THANKLESS

- **<option>**
  - Impact: <0-3>, Effort: <0-3>
  - Rejected because: <one-line>
  - Advocate (if known): <name or role>
```

### Section D, Summary table

```markdown
| Option | Impact | Effort | Quadrant | Ship/Defer/Reject | Notes |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |
```

### Section E, Decision Hook

```markdown
## Decision Hook

QUICK WINS ship at rubric ≥ 6; can run in parallel with Big Bets.
BIG BETS commit at the cynefin-adjusted threshold; downgrade to PROBE if below.
FILL-INS queue conditionally on spare capacity.
THANKLESS entries appear in Dissent appendix as "considered and rejected."

If multiple BIG BETS exist, trigger Hard Choice unless they can be sequenced cleanly.
```

### Section F, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentence synthesis. Name the dominant Big Bet, the Quick Wins to ship in parallel, surface any Thankless entries that surprised the analysis.>
```

### Section G, Completeness

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- All input options classified: +<N>
- Effort scores include audit + comms + maintenance: +<N>
- Big Bet threshold matched to cynefin domain + reversibility: +<N>
- Thankless entries have rejection reasons: +<N>
- Provisional rubric checked against thresholds: +<N>
```

---

## Decision Hook

Impact-Effort feeds Confidence-Speed-Quality and the final recommendation:

- **Quick Wins** ship at rubric ≥ 6; if rubric < 6, defer to next /solve cycle
- **Big Bets** commit at cynefin-adjusted threshold; downgrade to PROBE if below; downgrade to DEFER if much below
- **Fill-Ins** appear in execution plan as "if spare capacity" optional items
- **Thankless** entries become Dissent appendix; never enter the recommendation

Confidence rubric impact:
- Top option in Quick Win: +1 to overall confidence rubric (the cost of being wrong is small)
- Top option in Big Bet AND rubric ≥ threshold: +0 (baseline; threshold met)
- Top option in Big Bet AND rubric < threshold: -2 (over-committing; degrades to PROBE recommendation)
- Top option in Thankless: contradiction with Decision Matrix; flag in Dissent and SendMessage

### Override conditions

If Decision Matrix top option lands in Thankless, Impact-Effort overrides Decision Matrix. The recommendation downgrades to "do not commit; rerun with refined criteria." This is rare but real: it means Decision Matrix's weights didn't capture cost adequately.

---

## Cross-Framework Triggers

- **3+ options in Big Bet** → SendMessage to lead recommending narrowing via Hard Choice or sequencing
- **0 options in Quick Win** → SendMessage suggesting zwicky-box re-run looking for narrower wedges
- **Top Decision Matrix option in Thankless** → SendMessage flagging contradiction; surface in Dissent
- **Big Bet + cynefin = complex + rubric < 8** → mark `state.PROBE_MODE = true` for Confidence-Speed-Quality
- **Big Bet + intake.reversibility = one-way-door + rubric < 8** → trigger Hard Choice if not already triggered

---

## Failure Modes

### Failure Mode 1, Effort myopia (only counting build time)

Trap: Effort scores ignore audit, comms, ongoing maintenance.

Manifestation: Big Bets misclassified as Quick Wins; team commits to "small" change that has 4-week tail.

Check: every Effort score has 3+ cost dimensions cited (eng + audit + comms + ...). If only one cost cited, raise Effort by 1.

Recovery: re-score with full cost accounting.

### Failure Mode 2, Impact inflation from advocacy

Trap: option scored high impact because someone is advocating loudly.

Manifestation: Impact = 3 with weak link to `intake.success_criteria`.

Check: every Impact = 3 has explicit citation of `intake.success_criteria` and the mechanism by which the option moves it.

Recovery: downgrade options that fail the citation test to Impact = 1-2.

### Failure Mode 3, Big Bet without confidence threshold check

Trap: agent classifies Big Bet but doesn't check whether confidence rubric meets the cynefin-adjusted threshold.

Manifestation: Big Bet entry without "currently rubric: N" line.

Check: every Big Bet has provisional rubric vs threshold comparison.

Recovery: read confidence state from `state.json` (or compute provisional from framework outputs); add comparison; downgrade to PROBE if below.

### Failure Mode 4, Thankless silently dropped

Trap: low-impact-high-effort options removed from output without rejection reason.

Manifestation: Thankless quadrant empty in output, but option list shrunk between input and output.

Check: count input options vs output classified options. If shrunk, missing options must appear in Thankless with reasons.

Recovery: add the missing options back with explicit rejection reasons.

### Failure Mode 5, Reversibility ignored

Trap: Big Bet threshold doesn't account for `intake.reversibility = one-way-door`.

Manifestation: one-way-door Big Bets evaluated at standard threshold (≥ 7) instead of raised threshold (≥ 8).

Check: if `intake.reversibility = one-way-door`, header must show "Big Bet threshold: ≥ 8" (raised).

Recovery: re-evaluate all Big Bets at raised threshold.

---

## Jargon Glossary

- **impact**, degree to which an option moves `intake.success_criteria`.
- **effort**, total cost: build + audit + comms + maintenance + opportunity cost.
- **Quick Win**, high impact + low effort; ship at rubric ≥ 6.
- **Big Bet**, high impact + high effort; commit at cynefin-adjusted threshold.
- **Fill-In**, low impact + low effort; queue if spare capacity.
- **Thankless**, low impact + high effort; reject and document.
- **threshold**, minimum confidence rubric required to commit a Big Bet; varies by cynefin domain and reversibility.
- **PROBE downgrade**, Big Bet below threshold becomes a smallest-experiment recommendation rather than a commit.
- **DEFER downgrade**, Big Bet much below threshold becomes "gather evidence first" rather than committing or probing.
- **provisional rubric**, the confidence rubric computed from framework outputs available at this point in the run (Step 9 of SKILL.md formalizes the final rubric).
- **opportunity cost**, what doesn't ship because resources are spent on this option.
- **maintenance burden**, ongoing eng / ops cost after the option ships; often the largest hidden effort component.

---

## Completeness Scoring

### 10/10, Decisive
- Every option classified with Impact and Effort scores
- Effort scores include 3+ cost dimensions (build, audit, comms, maintenance, opportunity)
- Big Bet thresholds adjusted for cynefin + reversibility
- Each Big Bet has provisional rubric comparison
- Thankless entries have rejection reasons
- Quick Win shipping plan articulated

### 7/10, Confident
- All options classified
- Effort scores include 2 cost dimensions (most common: build + audit)
- Big Bet thresholds correctly adjusted
- Some entries have minor gaps (e.g. Fill-In implication unclear)

### 4/10, Tentative
- 1-2 options unclassified or `effort_unknown`
- Effort scores only count build time
- Big Bet thresholds use defaults (not cynefin-adjusted)
- Thankless entries silently dropped or lacking reasons

### 0/10, Unusable
- Most options uniform-classified
- No Effort breakdown
- No threshold comparison for Big Bets
- Output reads as recommendation list without quadrant structure

Impact-Effort completeness ≤ 4 contributes -1 to overall rubric.

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

### Inputs going in

From `frameworks/cynefin.md`:
- Domain: complicated
- Big Bet threshold: ≥ 7 (cynefin-adjusted)

From `intake.json`:
- `reversibility = costly` (NOT one-way-door, so threshold stays at 7)

From `frameworks/eisenhower.md`:
- DROPs: D (separate token) → excluded
- DO_NOW + SCHEDULE: A (big-bang), B (dual-deploy+drain), C (wrapped legacy), plus sub-decisions E/F/G/H

From `frameworks/decision-matrix.md` (provisional from concurrent run):
- B (dual-deploy+drain) score: 8.2
- A (big-bang) score: 6.4
- C (wrapped legacy) score: 6.7

Sub-decisions (F, G, H) classified separately.

### Step 1, Filter dropped

- Removed: D
- Surviving for matrix: A, B, C
- Sub-decisions to classify: E, F, G, H

### Step 2-3, Score Impact and Effort

| Option | Impact reasoning | Imp | Effort reasoning | Eff |
|---|---|---|---|---|
| A: big-bang | Directly drives TVL retention if cutover succeeds; high downside if it fails | 3 | 2 weeks eng + 1 week audit + comms + 0 ongoing maintenance (single contract path) | 2 |
| B: dual-deploy+drain | Directly drives TVL retention; documented best-practice pattern | 3 | 4-6 weeks eng + 2 weeks external audit + comms + 4 weeks ongoing dual-contract maintenance | 3 |
| C: wrapped legacy | Solves UX without migrating; partial impact on retention | 2 | 3 weeks eng + 1 week audit + comms + indefinite ongoing maintenance of 2 contracts | 3 |
| E: select archetype | Umbrella decision; resolved by Decision Matrix | n/a | n/a | n/a |
| F: external auditor consult | Indirectly improves all paths via audit signoff | 2 | 1 week setup + auditor budget; ongoing comms during 2-week audit | 1 |
| G: user comms plan | Improves user trust during cutover; supports retention | 2 | 1 week product team draft + ongoing weekly updates during migration | 1 |
| H: testnet probe | Validates chosen archetype; lowers Big Bet risk | 3 | 1 week setup + 1 week observation on Base testnet | 1 |

### Step 4, Place in quadrants

- **QUICK WINS** (Imp ≥ 2, Eff ≤ 1): F, G, H
- **BIG BETS** (Imp ≥ 2, Eff ≥ 2): A, B, C
- **FILL-INS**: (none)
- **THANKLESS**: (none, since D was already dropped by Eisenhower)

### Step 5, Write per-quadrant

```markdown
## Visual

              EFFORT
              Low (0-1)             High (2-3)
   ┌───────────────────────┬───────────────────────┐
H  │   QUICK WIN           │   BIG BET             │
i  │   F: auditor consult  │   A: big-bang         │
g  │   G: comms plan       │   B: dual-deploy+drain│
h  │   H: testnet probe    │   C: wrapped legacy   │
   ├───────────────────────┼───────────────────────┤
L  │   FILL-IN             │   THANKLESS           │
o  │   (none)              │   (none)              │
w  │                       │                       │
   └───────────────────────┴───────────────────────┘

## QUICK WINS

- **F: external auditor consult** (Imp 2, Eff 1)
  - Reason: indirectly raises confidence on whatever archetype wins
  - Ship threshold: rubric ≥ 6 (currently provisional 7+)
  - Implication: ship in parallel with Big Bet kickoff (week 1)

- **G: user comms plan** (Imp 2, Eff 1)
  - Reason: user trust during cutover; partial retention upside
  - Ship threshold: rubric ≥ 6
  - Implication: ship in parallel; product team owns

- **H: testnet probe** (Imp 3, Eff 1)
  - Reason: validates chosen archetype against actual mempool dynamics
  - Ship threshold: rubric ≥ 6 (currently exceeded)
  - Implication: critical Quick Win; ship before Big Bet commits

## BIG BETS

- **A: big-bang single-cutover** (Imp 3, Eff 2)
  - Reason: simpler operational model than dual-deploy
  - Ship threshold: rubric ≥ 7 (cynefin = complicated)
  - Currently provisional rubric for A: 6 (Decision Matrix score 6.4)
  - Mode if below threshold: PROBE on Base testnet first
  - Note: inversion-define flagged big-bang as failure-amplifying; even at threshold, downgrade to PROBE for safety

- **B: dual-deploy + drain** (Imp 3, Eff 3)
  - Reason: documented LayerZero best-practice for $1M+ TVL; 3 prior protocol successes
  - Ship threshold: rubric ≥ 7 (cynefin = complicated)
  - Currently provisional rubric for B: 9 (Decision Matrix score 8.2)
  - Mode: COMMIT (rubric exceeds threshold)

- **C: wrapped legacy** (Imp 2, Eff 3)
  - Reason: avoids deprecation but has indefinite maintenance
  - Ship threshold: rubric ≥ 7
  - Currently provisional rubric for C: 5 (Decision Matrix score 6.7)
  - Mode if below threshold: DEFER (do not commit; this archetype isn't winning)

## FILL-INS, THANKLESS

(none)
```

### Step 5, Summary table

```markdown
| Option | Imp | Eff | Quadrant | Ship/Defer/Reject |
|---|---|---|---|---|
| A | 3 | 2 | BIG BET | PROBE on Base first |
| B | 3 | 3 | BIG BET | COMMIT (threshold met) |
| C | 2 | 3 | BIG BET | DEFER (below threshold) |
| F | 2 | 1 | QUICK WIN | SHIP parallel |
| G | 2 | 1 | QUICK WIN | SHIP parallel |
| H | 3 | 1 | QUICK WIN | SHIP before Big Bet commits |
```

### Output completeness

- All 6 candidates classified: yes
- Effort scores include build + audit + comms + maintenance: yes
- Big Bet threshold matched to cynefin (complicated → ≥ 7): yes
- Reversibility check (costly, not one-way-door): no threshold raise needed
- Provisional rubric compared per Big Bet: yes
- All Quick Win and Big Bet entries have ship/defer recommendations: yes

**Completeness: 9/10** (minus 1 for not citing maintenance-cost dimension explicitly per option; only summarized in prose).

---

## What This Means For The Decision

Impact-Effort told us three Quick Wins to ship in parallel (F, G, H). It told us only one Big Bet (B: dual-deploy+drain) meets the cynefin-adjusted commit threshold; the other two Big Bets (A, C) are below threshold and must downgrade to PROBE or DEFER. The Decision Matrix top option (B) and Impact-Effort agree: B commits.

The framework's value here isn't picking the winner (Decision Matrix did that). It's surfacing that A and C are not affordable Big Bets, and that F+G+H must ship in parallel rather than after the Big Bet. Without Impact-Effort, those Quick Wins would queue behind B and the migration would hit the field without auditor signoff or user comms in place.
