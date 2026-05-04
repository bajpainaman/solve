# Decision Matrix (Weighted Criteria)

**Phase:** Decide · **Source:** https://untools.co/decision-matrix

The Decision Matrix is the dominant Decide-phase framework when Cynefin classifies the problem as simple or complicated. It forces every option onto the same axes, every criterion to carry an explicit weight, every score to defend itself against the next option in the column. Picking up the matrix without defending the weights is the most common way teams ship a confident-wrong recommendation.

This framework is decisive in routing terms: the top option becomes the recommendation unless Hard Choice fires, the top-vs-second gap drives the confidence rubric, and the disqualified rows feed back to the inversion-define constraint check. Every other Decide-phase framework reads the matrix output to know what is being recommended and what was rejected.

---

## Entry Predicate

```
(|surviving_options| ≥ 2) ∧ cynefin.domain ∈ {simple, complicated, complex}
```

Skip when:
- Only one option survives the prior phases. Then there is nothing to weigh and the framework writes a one-line "trivial: only A survived intake + zwicky-box + inversion-define" with the surviving option promoted directly to recommendation.
- Cynefin classified as chaotic. In chaotic domains the recommendation is "act first to stabilize," and Decision Matrix is misuse of the team's time.
- Cynefin classified as disorder. Decision Matrix on a disordered problem produces confident-wrong scoring on weights nobody can justify.

Run with degraded weight when:
- Cynefin classified as complex. Matrix runs but its output is advisory, not decisive. The recommendation comes from OODA's first cycle, with the matrix offering a starting point. Mark the output `mode: advisory` and downgrade confidence rubric impact from +2 to 0.

### Inputs

- `frameworks/zwicky-box.md::archetypes` — the morphological combinations to score
- `frameworks/productive-thinking.md::forged_solutions` — synthesized options
- `frameworks/inversion-define.md::constraints` — failure paths that disqualify options entirely
- `frameworks/cynefin.md::routing.weight_overrides` — domain-specific weight floors (e.g. complicated + costly reversibility forces reversibility weight ≥ 7)
- `intake.success_criteria` — the canonical metric or qualitative signal options must satisfy
- `intake.reversibility` — drives the reversibility weight floor
- `intake.time_pressure` — drives the time-to-implement weight floor
- `evidence/decide-base-rates.md` — base rates for similar decisions, used to sanity-check scores
- `frameworks/iceberg.md::structures` — surfaces hidden constraints that adjust scoring

### Outputs

- `$RUN_DIR/frameworks/decision-matrix.md` — the score table + weight justifications + top option + runner-up gap
- `state.json` `decision_matrix.top_option`, `decision_matrix.top_two_within_5pct` — read by Hard Choice predicate

---

## Operating Principles

These five rules are non-negotiable. Skipping any of them produces a matrix that scores confidently in the wrong direction.

**1. Disqualify before you score.**

Any option that violates an inversion-define constraint receives total score 0 and a strikethrough row. Do not score disqualified options on individual criteria, even partially. Scoring a disqualified option on its strengths invites the team to rationalize its survival. The matrix is not a debate stage. Anti-pattern: scoring "big-bang single-cutover" on its speed criterion (high) when inversion-define said "must NOT freeze user funds during migration" and big-bang freezes funds. The 9 on speed seduces the room into reconsidering. Cross it out.

**2. Weights come from criteria, criteria come from success criteria.**

Do not invent criteria to justify a preferred option. The criterion list derives from `intake.success_criteria` plus `frameworks/inversion-define.md::failure_modes` plus `frameworks/iceberg.md::structures`. If a criterion appears that is not traceable to one of those three sources, delete it. Anti-pattern: the team prefers Option B, then adds "developer ergonomics" as a 7-weight criterion late in the run. Developer ergonomics was not in success criteria, was not a failure mode, was not an iceberg structure. It is rationalization. The matrix discards rationalized criteria.

**3. Weights are ordinal, not cardinal.**

A criterion weighted 8 is more important than a criterion weighted 5, but it is not "1.6 times" more important in any meaningful sense. The matrix produces a ranking, not a magnitude. Anti-pattern: the team obsesses over whether reversibility deserves 7 vs 8. They burn 30 min on the difference. The right move: ask "is reversibility more important than gas cost? Yes. More important than implementation time? Yes. Less important than fund safety? Yes." Position it by neighbors, not by absolute weight.

**4. Score with evidence, not vibes.**

Every cell in the matrix needs a one-line justification. "9 on safety because the dual-deploy approach has been used by 3 prior protocols (Stargate, Radiant, Ethena) without fund loss" is a defensible 9. "9 on safety because it feels safer" is not. Anti-pattern: filling in the matrix in a meeting from memory. The matrix is a research artifact, not a meeting tool. Pre-fill cells with evidence pointers from `evidence/`, then meet to challenge.

**5. The matrix routes the next framework, it does not decide.**

The matrix says "B leads A by 23%, run second-order on B, sanity-check via Six Hats, ship." The matrix does not say "we are doing B." That commitment comes from second-order plus Six Hats agreement plus adversary not breaking it plus Hard Choice not firing. Anti-pattern: the team treats the top score as the decision and skips the rest of Phase 3. The matrix is one input to a recommendation, not the recommendation itself. Anti-pattern in the other direction: the team disagrees with the top score and reweights criteria until their preferred option wins. That is bias laundering.

---

## Response Posture

**Tone.** Analytical and unflinching. The matrix is doing arithmetic on the team's stated values. The framework should sound like a good auditor: "The cells say B wins. Are the weights wrong, or is the team uncomfortable with what it just said it valued?"

**Pacing.** Single pass. The matrix is built once per run from the inputs, then challenged by adversary and revised once if necessary. Do not iterate the matrix into oblivion. If the third revision changes the top option, the problem is upstream (criteria are wrong, weights are unjustified). Surface that to the lead via SendMessage rather than re-scoring.

**Push depth.** Maximum on weights, moderate on scores. The team will fight harder over scores ("is the gas cost really a 6 for option B?") than over weights ("is gas cost weight 5 the right importance?"). Score arguments rarely change the ranking. Weight arguments often do. Push hardest on whether the criteria list is complete and the weights match the team's stated success criteria.

**Where to escalate.** SendMessage to lead when:
- A disqualifier surfaces during scoring that inversion-define did not catch (new failure mode discovered). Rerun inversion-define, regenerate the matrix.
- The top two options are within 5%. Trigger Hard Choice via state.decision_matrix.top_two_within_5pct = true.
- A criterion's weight is contested by ≥ 2 stakeholders and the swap would flip the top option. The team has not actually agreed on what success means.
- The matrix produces a top option that contradicts a strong adversary attack (adversary score ≥ 7 on the leading row). Pause for revision before declaring a winner.

---

## Anti-Sycophancy Rules

The agent running Decision Matrix must never write these:

- "Both options have merit and the choice depends on..." Pick one. Cite the gap.
- "It's a close call between A and B." If it is close, say "top two within 5%, triggering Hard Choice." If it is not, name the winner.
- "Reasonable weights would also produce..." If alternative weights flip the answer, the criterion is unstable. Flag the weight, do not hedge the conclusion.
- "Some teams might prefer..." This team has stated success criteria. Score against those.
- "On balance..." Replace with the actual gap percentage.

The agent must always:

- State the top option and the runner-up by name with their total weighted scores.
- Quote the gap as a percentage of the runner-up.
- Name which 1-2 weights, if changed, would flip the result.
- Name the disqualified rows explicitly with the constraint that disqualified them.
- Cite the evidence source for every score ≥ 8 or ≤ 3 (the high-confidence cells).

---

## Pushback Patterns

These are the most common ways teams misuse the matrix. The agent applies them as self-pushback while building the matrix from prior framework outputs.

**Pattern 1: "All criteria matter equally" → check stated success criteria**

- Internal evidence: team has 6 criteria, all weighted 5-7.
- BAD: Run the matrix with flat weights. Top option wins by margin proportional to its strongest criterion, which the team did not consciously elevate.
- GOOD: Refuse to run flat weights. The team has not done the work of stating what matters. Read `intake.success_criteria` and `frameworks/inversion-define.md::failure_modes`. The success criteria is the highest weight (8-10). Failure modes are the disqualifiers. Implementation cost is below both. Force a 3-tier weight bucket: must-have (8-10), important (5-7), nice-to-have (1-4). Then revisit specific values.

**Pattern 2: "We need more criteria to be thorough" → check criterion-to-success-criteria traceability**

- Internal evidence: team adds "team morale," "code maintainability," "future flexibility" to a 4-criterion matrix.
- BAD: Add the criteria, score them, dilute the existing weights.
- GOOD: Check each new criterion against the source list. Does success_criteria mention team morale? Does inversion-define mention low maintainability? If no, the criterion is rationalization. The matrix does not get more accurate by adding criteria, it gets noisier. Cap the criterion list at 7. Each criterion must trace to a specific source in `intake.success_criteria` or `frameworks/inversion-define.md::failure_modes` or `frameworks/iceberg.md::structures`.

**Pattern 3: "Option C scored highest, but it feels wrong" → check whether bias is in the matrix or the gut**

- Internal evidence: matrix output is C top, B second, A third. Lead says "I think B is the right call."
- BAD: Reweight criteria until B wins. Rationalization disguised as analysis.
- GOOD: Two paths. Path 1: name the specific weight or score the lead disagrees with. If it is a weight, check whether the weight matches `intake.success_criteria`. If it is a score, ask for the evidence. Path 2: accept that gut may be tracking a constraint the matrix missed. Spawn a 5-min check: is there a failure mode in inversion-define that disqualifies C? Is there an iceberg.structures finding that affects C specifically? If yes, the gut is right and the inputs were incomplete. If no, the gut is the bias, and B winning is rationalization.

**Pattern 4: "The top two are very close" → trigger Hard Choice, do not iterate weights**

- Internal evidence: A scores 142, B scores 138, gap is 2.8%.
- BAD: Adjust criterion weights to widen the gap and "make the call clearer."
- GOOD: Stop. The matrix has produced its real signal: A and B are on a par. This is the trigger condition for Hard Choice. Set `state.decision_matrix.top_two_within_5pct = true`. Hard Choice will reframe the decision around values and identity, not weighted arithmetic. Mathematical closeness is information, not a defect to be eliminated.

**Pattern 5: "A criterion was missing and changes the order" → rerun, do not patch**

- Internal evidence: matrix is mid-build, team realizes "audit complexity" is a missing criterion.
- BAD: Add audit complexity as a new column, score 4 options, leave existing weights untouched.
- GOOD: Audit complexity affects the entire criterion taxonomy. The team should have caught this in inversion-define or success_criteria. Pause the matrix. Update inversion-define and success_criteria. Restate the canonical criterion list. Then rebuild the matrix from scratch. Patching the matrix mid-build produces a Frankenstein where some criteria are well-evidenced and others are afterthoughts.

---

## Method

Decision Matrix runs as an 8-step procedure. Each step has explicit prerequisites and produces a discrete output that feeds the next step. Skipping any step produces a matrix that the team cannot defend.

### Step 1, Read all upstream framework outputs

Prerequisites: Phases 1 and 2 complete, Cynefin classification written, intake JSON present.

```bash
ls $RUN_DIR/frameworks/ | sort
```

Read in this priority order: cynefin.md (for routing weights), zwicky-box.md (for archetypes), productive-thinking.md (for forged solutions), inversion-define.md (for constraints), iceberg.md (for hidden structures), evidence/decide-base-rates.md (for sanity-check ranges).

Output: a list of candidate options and a list of disqualifying constraints, written to scratchpad.

Failure mode if skipped: matrix scores options the team has already ruled out, wasting room time and confusing downstream frameworks.

### Step 2, Build the option list

Prerequisites: Step 1 complete.

Take the union of `zwicky-box.md::archetypes` ∪ `productive-thinking.md::forged_solutions`. Dedupe. Number the options A, B, C, D. Cap at 6 options. If more than 6 candidates exist, cluster the close ones (e.g. "wrapped legacy with ERC-20 wrapper" and "wrapped legacy with custom wrapper" collapse to "wrapped legacy") and pick the dominant variant per cluster.

Output: numbered option list with one-line description per option.

Failure mode if skipped: scoring proliferates, room loses focus, top option won by attention rather than evidence.

### Step 3, Apply disqualifiers from inversion-define

Prerequisites: Step 2 complete, inversion-define.md present.

For each option, walk through inversion-define.constraints. If any constraint applies and the option violates it, mark the option DISQUALIFIED with the specific constraint. Disqualified options keep their row in the table but get total score 0 with a strikethrough.

Output: option list with DISQUALIFIED markers. Surviving options proceed to Step 4.

Failure mode if skipped: a disqualified option might score highest by accident (because it is fast or cheap or simple), and the team rationalizes back to it.

### Step 4, Build the criterion list

Prerequisites: Steps 1-3 complete.

Derive criteria from three sources, in this priority order:

1. `intake.success_criteria`. Each named success metric becomes a criterion. If success criteria is "qualitative-signal" rather than a metric, decompose into 2-3 sub-criteria the qualitative signal implies (e.g. "user trust during migration" decomposes into "fund safety," "UX clarity," "communication runbook").
2. `frameworks/inversion-define.md::failure_modes`. Each failure mode that wasn't already a disqualifier becomes a criterion measuring resilience to that failure mode.
3. `frameworks/iceberg.md::structures`. Each hidden structural constraint becomes a criterion (e.g. "handles cross-chain mempool dynamics gracefully").

Cap at 7 criteria. Apply Pattern 2 anti-bloat: every criterion must trace to one of the three sources. Reject ad-hoc criteria.

Output: numbered criterion list with one-line definition and source for each.

Failure mode if skipped: matrix scores on whatever the room thinks of in the moment, biases toward criteria that favor the speaker's preferred option.

### Step 5, Assign weights with justification

Prerequisites: Step 4 complete.

For each criterion, assign a weight 1-10 with a one-line justification grounded in the source. Apply Cynefin's routing weight overrides as floors:

- `cynefin.routing.weight_overrides` specifies floors per criterion (e.g. "reversibility ≥ 7" if reversibility is "costly" or worse).
- Time-pressure overrides: `intake.time_pressure = "now"` forces "time to implement" weight ≥ 7.
- Stakeholder overrides: `intake.stakeholders = "multi-stakeholder"` forces "alignment cost" weight ≥ 6.

Use the 3-tier bucket from Pattern 1: must-have (8-10), important (5-7), nice-to-have (1-4). Place each criterion in a bucket first, then refine to a specific number.

Output: criterion list with weight + one-line justification per criterion.

Failure mode if skipped: weights are flat or arbitrary, top option wins by accident of which criterion got scored most generously.

### Step 6, Score each surviving option × criterion cell

Prerequisites: Step 5 complete.

For each surviving option (non-disqualified) and each criterion, score 0-10 with evidence. Score interpretation:

- 10: best-in-class, evidence shows this option dominates on this criterion across all reference cases
- 7-9: strong performance, multiple evidence pieces support
- 5-6: middle of the pack
- 3-4: weak but acceptable, some evidence of difficulty
- 1-2: poor but not disqualifying
- 0: would be a disqualifier (move it to disqualifier list and rerun Step 3)

Every cell scoring ≥ 8 or ≤ 3 (the high-confidence cells) requires a citation to evidence in `$RUN_DIR/evidence/` or to a specific finding in another framework.

Output: filled score grid with one-line evidence note per high-confidence cell.

Failure mode if skipped: cells scored from memory and bias rather than from research, top option wins because the most charismatic team member talked loudest about its strengths.

### Step 7, Compute weighted totals and rank

Prerequisites: Step 6 complete.

For each surviving option:

```
total(option) = Σ (weight_criterion × score_option,criterion)
```

Rank options by total descending. Compute the gap percentage:

```
gap_pct = (top_total − second_total) / second_total × 100
```

Output: ranked list with totals + gap percentage.

Failure mode if skipped: the team eyeballs the matrix and picks the winner from impression rather than arithmetic.

### Step 8, Apply triggers and write output

Prerequisites: Step 7 complete.

Check trigger conditions:

- gap_pct < 5: set `state.decision_matrix.top_two_within_5pct = true`, Hard Choice fires
- top_total ≥ 1.5 × second_total: confidence rubric +2
- 1.0 × second_total < top_total < 1.5 × second_total: confidence rubric 0 (clear lead but not dominant)
- gap_pct ≥ 5 AND any disqualified option: note in output that disqualifier is binding, not arithmetic

Write the full output following the Output Schema. Update state.json. SendMessage to decider with completion.

Output: `$RUN_DIR/frameworks/decision-matrix.md` and updated state.

Failure mode if skipped: downstream frameworks (Hard Choice, second-order) do not know whether to fire, recommendation is built on incomplete signals.

---

## Probe Patterns

The agent asks itself these probes while building the matrix. They are sanity checks, not user questions.

### Probe 1, completeness of the criterion list

> "Does my criterion list cover (a) all of `intake.success_criteria`, (b) all `inversion-define.failure_modes` not already in disqualifiers, and (c) all `iceberg.structures` constraints?"

Coverage shape:
- Yes for all three: 3 (criterion list complete)
- 2 of 3: 2 (one source under-represented)
- 1 of 3: 1 (matrix is biased toward whatever was covered)
- 0 of 3: 0 (criteria are ad-hoc)

Smart-skip: if `intake.success_criteria = "TBD"`, the criterion list cannot derive from success criteria. Use only inversion-define and iceberg, mark completeness 2/3, and note in output that success criteria undefined.

Red flag: criteria appear that do not trace to any of the three sources. Delete them.

### Probe 2, defensibility of weights

> "If I removed this criterion's weight justification, would the team accept the weight? If not, the justification is post-hoc."

For each weight, check:
- Justification ties to a specific source quote (intake or framework). Strong defense.
- Justification ties to a general claim ("important for this kind of decision"). Weak. Find a specific source or drop the criterion.
- No justification. Cell is a guess. Either find a source or downgrade to weight 1-3 (nice-to-have).

### Probe 3, evidence density per cell

> "How many cells have evidence citations? Out of total cells (options × criteria)."

Density target:
- ≥ 60% of cells cited with specific evidence: matrix is well-grounded
- 30-60%: matrix is partially grounded, output flags low-evidence cells
- < 30%: matrix is mostly impressions, rerun Step 6 with deeper research first

### Probe 4, weight-flip stability

> "If I flipped the two highest-weight criteria's weights (swap weights), does the top option change?"

Stability shape:
- No change: top option is stable, recommendation is robust
- Top option swaps with runner-up: weights are decisive, name them in output
- Multiple options swap: matrix is unstable, criterion list may be incomplete or weights are not actually distinguishing

### Probe 5, dominance check

> "Does any option dominate another (≥ on every criterion)? If yes, the dominated option drops out before scoring."

Used in simple-domain runs where the matrix should produce an obvious answer. Cynefin = simple plus dominance check often shortcuts the rest.

---

## Forcing Exemplars

When writing the matrix output, use the forcing-version (specific) instead of the softened-version (hedged).

### Exemplar 1, Stating the recommendation

SOFTENED (avoid):
> "Based on the analysis, dual-deploy plus drain appears to be the leading option, scoring well across most criteria."

FORCING (aim for):
> "Recommendation: dual-deploy plus drain (total 178). Runner-up: wrapped legacy (total 124). Gap: 43.5%. Confidence rubric: +2. The recommendation flips only if reversibility weight drops below 5 OR if dual-deploy plus drain's audit cost score drops to 3 (currently 7, evidence: 3 prior LZ migrations completed under similar audit budgets)."

### Exemplar 2, Justifying weights

SOFTENED (avoid):
> "Reversibility was weighted highly because it is important for this kind of migration."

FORCING (aim for):
> "Reversibility weight: 8. Source: `intake.reversibility = costly` triggers Cynefin's routing.weight_overrides floor of 7 for complicated domain. Source quote from cynefin.md: 'Decision Matrix runs but explicitly weight reversibility criterion at ≥ 8 because once we deploy OFTv2 and drain v1, reversing requires re-deploying v1 and convincing users to migrate back, which is multi-week.'"

### Exemplar 3, Citing scores

SOFTENED (avoid):
> "Dual-deploy scores high on safety because it has been validated by prior usage."

FORCING (aim for):
> "Dual-deploy plus drain, safety criterion, score 9. Evidence: Stargate (2023, $42M TVL), Radiant (2024, $18M TVL), Ethena (2024, $300M TVL) all completed dual-deploy + drain migrations without fund loss or reorg incidents. Source: `evidence/decide-prior-art.md`. The 9 (not 10) reserves space for edge cases none of those 3 prior cases hit (e.g. cross-chain mempool dynamics during gas spikes, flagged in iceberg.structures)."

### Exemplar 4, Marking disqualifiers

SOFTENED (avoid):
> "We did not score the big-bang option in detail given concerns about its approach."

FORCING (aim for):
> "Big-bang single-cutover: DISQUALIFIED. Inversion-define constraint: 'must NOT freeze user funds during migration.' Big-bang requires a freeze window of ≥ 4 hours during which v1 is paused before v2 launches. The freeze violates the constraint. Score: 0. Not scored on individual criteria. Even if it scored 10 on every other dimension (it does not), the constraint is binding."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/decision-matrix.md` follows this exact structure.

### Section A, Header

```markdown
# Decision Matrix, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** <comma-separated list of upstream frameworks + evidence>
**Cynefin domain (from cynefin.md):** <domain>
**Mode:** <decisive | advisory>
```

Mode = decisive when Cynefin = simple/complicated, advisory when Cynefin = complex.

### Section B, Option list with disqualifiers

```markdown
## Options

| Code | Option | Source | Status |
|---|---|---|---|
| A | Big-bang single-cutover | zwicky-box | DISQUALIFIED (inversion-define: freezes funds) |
| B | Dual-deploy + drain | zwicky-box, productive-thinking | active |
| C | Wrapped legacy | productive-thinking | active |
| D | Separate token + voluntary migration | zwicky-box | active |
```

Disqualified options remain in the table for audit trail but are excluded from scoring.

### Section C, Criterion list with weights

```markdown
## Criteria

| Code | Criterion | Weight | Source | Justification |
|---|---|---|---|---|
| C1 | Fund safety | 10 | success_criteria + inversion-define | "must NOT lose user funds" is the highest-priority constraint |
| C2 | Reversibility | 8 | intake.reversibility + cynefin.weight_override | costly reversibility forces floor 7, complicated domain raises to 8 |
| C3 | Implementation time | 7 | intake.time_pressure | this-month deadline forces floor 6, push to 7 due to dependency on audit |
| C4 | Audit cost | 6 | inversion-define.failure_modes | failed audit is a costly setback, but recoverable |
| C5 | UX continuity | 6 | iceberg.patterns | users expect < 30s settle; deviation causes support tickets |
| C6 | Gas efficiency | 5 | success_criteria | OFTv2's gas improvements are a stated benefit |
| C7 | Mempool resilience | 5 | iceberg.structures | non-trivial cross-chain dynamics flagged |
```

Weights total ≤ 50 (cap to keep ranking interpretable).

### Section D, Score matrix

```markdown
## Score Matrix (surviving options only)

| Option | C1 (w=10) | C2 (w=8) | C3 (w=7) | C4 (w=6) | C5 (w=6) | C6 (w=5) | C7 (w=5) | **Total** |
|---|---|---|---|---|---|---|---|---|
| ~~A~~ | DISQUALIFIED (inversion-define: freezes funds) | | | | | | | **0** |
| B | 9 (90) | 8 (64) | 6 (42) | 7 (42) | 7 (42) | 8 (40) | 7 (35) | **355** |
| C | 7 (70) | 6 (48) | 8 (56) | 5 (30) | 9 (54) | 5 (25) | 4 (20) | **303** |
| D | 6 (60) | 9 (72) | 5 (35) | 6 (36) | 5 (30) | 6 (30) | 6 (30) | **293** |
```

Cell format: `score (weighted_score)` where weighted_score = score × weight.

### Section E, Evidence per high-confidence cell

```markdown
## Evidence (cells scoring ≥ 8 or ≤ 3)

- B × C1 (9): Stargate, Radiant, Ethena dual-deploy + drain migrations without fund loss. Source: evidence/decide-prior-art.md
- B × C2 (8): drain mechanism allows pause and resume mid-migration; previous LZ deploys used this. Source: evidence/decide-prior-art.md, intake notes
- B × C6 (8): OFTv2 gas savings of ~22% on cross-chain transfers, measured on Stargate testnet. Source: evidence/decide-base-rates.md
- C × C5 (9): wrapped legacy preserves the existing token address; UX is unchanged for end users. Source: iceberg.patterns
- D × C2 (9): separate token approach is reversible (we can stop issuing OFTv2 and existing v1 holders are unaffected). Source: inversion-define
- C × C7 (4): wrapping introduces extra hop on cross-chain mempool, amplifying mempool delays. Source: iceberg.structures
```

### Section F, Ranking and gap

```markdown
## Ranking

1. **B (Dual-deploy + drain): 355**
2. C (Wrapped legacy): 303
3. D (Separate token): 293

**Top-vs-second gap:** (355 − 303) / 303 = 17.2%
**Disqualified:** A (big-bang single-cutover)

**Top-two-within-5pct:** false (gap = 17.2% > 5%)
**Top ≥ 1.5× second:** false (355 / 303 = 1.17, less than 1.5)

**Confidence rubric impact:** +0 (clear lead but not dominant; matrix-driven recommendation is reliable but does not earn the +2 multiplier)
```

### Section G, Sensitivity check

```markdown
## Sensitivity

Two stability checks:

1. **Weight-flip stability**: swap C1 (w=10) and C2 (w=8). Recompute. Top option:
   - Original: B (355)
   - Flipped: B (343), gap to C narrows to 13%. Top option stable.
2. **Score-floor stability**: drop B's lowest-scoring cell (C3 = 6) by 2 points. New B total = 343. Still leads C by 40 points. Stable.

**Decisive weight:** C1 (fund safety, w=10). If fund safety is wrong (e.g. a disqualifier we missed makes B unsafe), the entire recommendation flips. The dual-deploy + drain mechanism's safety record is the single most load-bearing assumption.
```

### Section H, Triggers fired

```markdown
## Triggers

- top_two_within_5pct: false → Hard Choice does NOT fire
- top ≥ 1.5× second: false → confidence rubric +0
- disqualifier present: true → A's disqualification is binding regardless of arithmetic
- complex domain (cynefin advisory mode): false → matrix is decisive

State updates:
- `state.decision_matrix.top_option = "B (dual-deploy + drain)"`
- `state.decision_matrix.gap_pct = 17.2`
- `state.decision_matrix.top_two_within_5pct = false`
- `state.decision_matrix.disqualified_count = 1`
```

### Section I, What This Means For The Decision

```markdown
## What This Means For The Decision

The recommendation is **dual-deploy + drain (Option B)** with a 17.2% lead over wrapped legacy (C). The lead is comfortable but not dominant; the matrix earns +0 to the confidence rubric (would have earned +2 if B had scored ≥ 1.5× C). The disqualified option (A, big-bang) is binding via inversion-define and is excluded from any further consideration.

The single most load-bearing assumption is fund safety (C1, w=10), where B scores 9 based on 3 prior protocol migrations. If a finding emerges that contradicts that safety record (e.g. a Stargate post-mortem reveals a near-miss the public did not see), the recommendation could shift toward C (wrapped legacy) which scores 7 on safety with a different mechanism.

Hard Choice does not fire (gap > 5%). Second-order will run on B + C (top 2). Six Hats will run with normal weighting (Cynefin = complicated, no Black-dominant override). Confidence-Speed-Quality runs in QUALITY mode (complicated + costly reversibility).
```

### Section J, Completeness Score

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- All criteria traceable to source (success_criteria / inversion-define / iceberg): +<N>
- All weights have one-line justification: +<N>
- ≥ 60% of cells have evidence citations: +<N>
- Disqualifiers explicitly listed with constraint reference: +<N>
- Sensitivity check (weight-flip + score-floor) performed: +<N>
- Triggers fired correctly (top_two_within_5pct, ≥1.5× check): +<N>
```

---

## Decision Hook

Decision Matrix's output drives the rest of Phase 3 in three ways.

### Per-domain decisiveness

| Domain | Matrix role | Confidence rubric impact |
|---|---|---|
| Simple | Decisive; if dominance check passes, the matrix is the recommendation, no further frameworks needed except Eisenhower triage | +2 if top ≥ 1.5× second |
| Complicated | Decisive; the matrix recommendation is the team's best call, validated by second-order, Six Hats, and adversary | +2 if top ≥ 1.5× second |
| Complex | Advisory only; OODA's first cycle becomes the decision, matrix gives a starting point for the probe | +0 (rubric earns through OODA experiments) |
| Chaotic | Skip entirely; act first via OODA single-cycle to stabilize, rerun /solve afterward | -2 (acting under low confidence) |
| Disorder | Phase 3 halts; matrix does not run | n/a |

### Downstream framework feeding

- **Second-order**: receives top 2 options (B and C), runs 3 levels of "and then what?" on each. If complex domain, runs 4 levels deep.
- **Ladder of Inference**: receives top recommendation (B). Traces the team's reasoning back through 7 rungs. Adversary attacks weakest leap.
- **Six Hats**: receives top recommendation (B). 6 hats roleplay; Black hat gets `state.decision_matrix.top_option` as the target of attack. Yellow hat gets the same as the target of upside.
- **Hard Choice**: receives `state.decision_matrix.top_two_within_5pct`. Fires only if true OR if `intake.reversibility = one-way-door`. When fires, Hard Choice's recommendation overrides Decision Matrix.
- **Impact-Effort**: receives surviving options + their weighted scores. Plots them on the 2x2; highest-weighted-score option that is also "high impact, low-medium effort" gets the green light.
- **Confidence rubric**: receives gap_pct. If top ≥ 1.5× second, +2. Otherwise +0. If complex domain, capped at +0.

### Override conditions

Decision Matrix is decisive in simple/complicated domains unless one of these overrides fires:

- **Hard Choice fires** (top 2 within 5% OR one-way-door reversibility): Hard Choice's recommendation overrides matrix. Matrix scores become supporting evidence.
- **Adversary breaks the recommendation** (adversary score ≥ 7 on the top row, plus a specific failure mode the team cannot rebut): the matrix recommendation is downgraded; if no recovery, recommendation becomes "no decision yet, gather X evidence."
- **Six Hats Black hat scores ≥ 8 against the top option** AND no other framework supports it: matrix recommendation is downgraded; rerun matrix with revised criteria/weights.
- **Cynefin = complex** (advisory mode): matrix never overrides, OODA does.

---

## Cross-Framework Triggers

Conditions in the Decision Matrix output force changes elsewhere in /solve.

### Triggers fired by gap_pct

- `gap_pct < 5`: trigger Hard Choice. Set `state.decision_matrix.top_two_within_5pct = true`. SendMessage to decider: "matrix top 2 within 5%, run Hard Choice."
- `gap_pct ≥ 50`: top option dominates by a margin that suggests one or more options should have been disqualified earlier. Sanity-check inversion-define for missed constraints.
- `gap_pct < 5` AND `cynefin = complex`: Hard Choice still fires. Complex domain narrows the recommendation to "smallest probe of B vs C," not the matrix's decisive framing.

### Triggers fired by disqualifier count

- `disqualified_count ≥ 50% of options`: too many options are getting disqualified. Either inversion-define is over-aggressive (rerun with a stricter "must NOT" check) or zwicky-box generated archetypes that all violate constraints (rerun with constraints-aware morphology). SendMessage to lead.
- `disqualified_count = 0` AND `inversion-define.constraints ≥ 3`: suspicious. Either no option violates any constraint (lucky) or the disqualifier check was lax. Rerun Step 3 with the explicit constraints list.

### Triggers fired by weight composition

- Any single criterion's weight contributes ≥ 50% of the top option's total: the matrix is effectively a single-criterion ranking. Surface in output: "the matrix is dominated by C1 (fund safety, w=10). The recommendation is essentially 'pick the safest option.' Confirm this matches stated success criteria."
- All weights within ±2 of each other: weights are not actually distinguishing. Rerun Step 5 with the 3-tier bucket approach.

### Triggers fired by evidence density

- < 30% of cells cited: matrix is mostly impressions. Pause, send researcher to fill evidence gaps, rerun Step 6.
- ≥ 80% of cells cited: matrix is strongly grounded; flag in output as "high evidence density."

---

## Failure Modes

Decision Matrix can mislead in five ways. The framework checks for each before completing.

### Failure Mode 1, weight bias laundering

Trap: the team has a preferred option going in. They tune weights until the preferred option wins. The matrix produces a recommendation that looks rigorous but is rationalization.

Manifestation in output: the team's previously-stated weights (in chat history or prior planning docs) differ from the weights in the matrix, with the differences favoring one option.

Check: compare current weights to weights in any prior planning artifact for this problem. If weights changed without a corresponding change in `intake.success_criteria` or `inversion-define.failure_modes`, the change is suspicious.

Recovery: revert to prior weights or require a justification tied to a source change. If neither, name the bias in output as a Dissent item.

### Failure Mode 2, criterion inflation

Trap: more criteria are added until every option has a criterion where it shines. The matrix becomes uninformative; every option has a strong column.

Manifestation in output: criterion list is 9+ entries. Most criteria have weights 4-6 (no clear hierarchy). Top option leads runner-up by < 10%.

Check: count criteria. If > 7, run Probe 1 (traceability) on each. Delete any criterion that does not trace to source.

Recovery: rebuild matrix with capped criterion list (≤ 7).

### Failure Mode 3, disqualifier amnesia

Trap: an option is scored despite being disqualified. The disqualifier is in inversion-define but the matrix builder did not check it. The option scores well, gets recommended, ships, fails on the disqualifying failure mode.

Manifestation in output: top option does not show DISQUALIFIED check; inversion-define has a failure mode that applies to the top option but is not referenced.

Check: for each surviving option, walk through every inversion-define.constraint. If any apply, the option should be disqualified.

Recovery: disqualify the option; rerun Steps 6-8 with the corrected list. If disqualifying changes the top option, the original recommendation was wrong.

### Failure Mode 4, evidence inflation through cell stuffing

Trap: every cell gets a citation, but the citations are weak ("see prior art research" without naming a specific case). Matrix appears well-grounded but evidence is thin.

Manifestation in output: 80%+ of cells cited, but the citations are generic. High-confidence cells (≥ 8 or ≤ 3) cite generic categories rather than specific cases.

Check: for each high-confidence cell, the citation must name a specific source (prior protocol name, specific evidence file path, specific framework finding). Generic citations downgrade the cell's contribution.

Recovery: require specific citations for high-confidence cells. Cells without specific evidence get downgraded toward the middle (5-6) until evidence improves.

### Failure Mode 5, top-two-within-5pct ignored

Trap: gap_pct is < 5 but the team treats the top option as the recommendation anyway, skipping Hard Choice. The decision is fragile and the team has not done the values work.

Manifestation in output: gap_pct < 5, `top_two_within_5pct = true`, but Hard Choice was not triggered or its output is missing.

Check: if `state.decision_matrix.top_two_within_5pct = true`, Hard Choice MUST fire before recommendation is finalized. The trigger is not optional.

Recovery: fire Hard Choice. Hard Choice's output overrides matrix's top option. If Hard Choice cannot resolve (commitment test fails on both), the recommendation is "no decision yet."

---

## Jargon Glossary

- weighted score, the product of weight and score for a single cell; sum across criteria gives an option's total
- dominance, when one option is ≥ another option on every criterion; the dominated option drops out
- orthogonality, criteria are independent; orthogonal criteria measure different things and don't double-count the same property
- disqualifier, a constraint from inversion-define that, if violated, sets the option's total to 0 regardless of other scores
- weight floor, a minimum weight forced by upstream framework outputs (e.g. Cynefin's routing weight overrides)
- weight-flip stability, whether the top option remains the top after swapping the two highest weights; high stability means the recommendation is robust
- gap_pct, percentage gap between top and second-place totals, used to trigger Hard Choice and confidence rubric
- decisive mode, Decision Matrix output is the recommendation (Cynefin = simple/complicated)
- advisory mode, Decision Matrix output is a starting point for OODA (Cynefin = complex)
- 3-tier weight bucket, the must-have / important / nice-to-have hierarchy used in Step 5
- evidence density, fraction of cells with specific evidence citations; high density correlates with reliable recommendations
- bias laundering, rationalizing weights to make a preferred option win; the most common matrix failure mode
- top_two_within_5pct, the trigger condition for Hard Choice; matrix arithmetic cannot distinguish the top 2

---

## Completeness Scoring

Decision Matrix self-rates 0-10 on quality. The rubric:

### 10/10, Decisive

- All options listed with sources from zwicky-box + productive-thinking
- Disqualifiers applied with explicit inversion-define constraint references
- Criterion list (≤ 7) traces 100% to source (success_criteria / inversion-define / iceberg)
- Every weight has a one-line justification grounded in source
- Cynefin routing weight overrides applied as floors
- ≥ 60% of cells have specific evidence citations
- Every high-confidence cell (≥ 8 or ≤ 3) cites specific case
- Sensitivity check performed (weight-flip + score-floor)
- Gap percentage stated, triggers fired correctly (top_two_within_5pct, ≥1.5× check)
- State updates written

### 7/10, Confident

- All options listed
- Disqualifiers applied but not all constraints checked (1-2 deferred)
- Criterion list mostly traceable; 1-2 criteria added by team without source
- Weights justified for top 4-5 criteria, generic for the rest
- 30-60% of cells cited
- Sensitivity check skipped or partial
- Gap percentage stated, triggers fired

### 4/10, Tentative

- Options listed but without source attribution
- Disqualifier check skipped (relies on memory)
- Criterion list ad-hoc, < 50% traceable
- Weights flat or arbitrary
- < 30% of cells cited
- No sensitivity check
- Gap percentage stated but triggers not all fired

### 0/10, Unusable

- < 2 surviving options
- No disqualifier check
- No criterion list (just options vs single "score")
- No weights
- No evidence
- Gap percentage cannot be computed

The completeness score appears in the framework output and feeds the overall Confidence rubric (Step 11 of SKILL.md). A Decision Matrix completeness ≤ 4 caps overall confidence at MEDIUM regardless of other framework scores.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This continues the canonical example from cynefin.md. Cynefin classified the problem as complicated (sum 9), with complex as runner-up (sum 7). The routing table specified:

- Decision Matrix: yes, normal mode, weight reversibility ≥ 7, Six Hats normal weight, OODA secondary, Hard Choice conditional on top-two-within-5pct
- Mode: decisive (complicated domain)

### Intake state (carried forward)

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

### Upstream framework outputs (carried forward)

- zwicky-box archetypes: A = big-bang, B = dual-deploy + drain, C = wrapped legacy, D = separate token
- productive-thinking forged solutions: B = dual-deploy + drain, C = wrapped legacy
- inversion-define constraints: must NOT lose user funds, must NOT freeze funds during migration, must NOT cause double-spending
- cynefin domain: complicated, weight overrides force reversibility ≥ 7
- iceberg.structures: cross-chain mempool dynamics non-trivial
- iceberg.patterns: users expect < 30s settle
- iceberg.mental_models: team believes "newer is better" (unverified)
- connection-circles: 1 reinforcing cycle (bridge volume → LP fees → liquidity), 1 balancing cycle (gas → migration eagerness)

### Step 1: Read upstream

Agent reads cynefin.md, zwicky-box.md, productive-thinking.md, inversion-define.md, iceberg.md, evidence/decide-prior-art.md.

Key extracted:
- Options: A, B, C, D
- Constraints: 3 disqualifiers from inversion-define
- Cynefin weights: reversibility floor 7
- Time pressure: this-month forces implementation-time floor 6
- Prior art: Stargate, Radiant, Ethena dual-deploy + drain (3 cases)

### Step 2: Build option list

```
A: Big-bang single-cutover (zwicky-box)
B: Dual-deploy + drain (zwicky-box, productive-thinking)
C: Wrapped legacy (productive-thinking)
D: Separate token + voluntary migration (zwicky-box)
```

4 options, well within cap of 6.

### Step 3: Apply disqualifiers

Walk through inversion-define.constraints:

1. "must NOT lose user funds":
   - A: high risk during freeze window. Borderline disqualifier (can be mitigated with multi-sig + tested rollback). Mark "active with caveat."
   - B: drain mechanism is gradual, no fund loss in prior cases. Active.
   - C: wrapping preserves underlying assets. Active.
   - D: voluntary migration leaves v1 holders intact. Active.

2. "must NOT freeze funds during migration":
   - A: REQUIRES a freeze window of ≥ 4 hours during cutover. **DISQUALIFIED.**
   - B: no freeze; both v1 and v2 active during drain. Active.
   - C: no freeze; wrapping happens at user request. Active.
   - D: no freeze; v1 stays live indefinitely. Active.

3. "must NOT cause double-spending":
   - All options have replay protection in LZ message encoding. Active.

Result: A is DISQUALIFIED on constraint 2.

### Step 4: Build criterion list

Source priorities:

From `intake.success_criteria = "qualitative-signal"`, decompose into:
- C1: fund safety (must-have)
- C5: UX continuity (important; users expect < 30s settle, deviations cause tickets)
- C6: gas efficiency (success criterion: "OFTv2 has better gas")

From `inversion-define.failure_modes` (not already disqualifiers):
- C4: audit cost (failed audit is recoverable but costly)

From `intake.reversibility + cynefin weight overrides`:
- C2: reversibility (forced floor 7)

From `intake.time_pressure = this-month`:
- C3: implementation time (forced floor 6)

From `iceberg.structures`:
- C7: mempool resilience (cross-chain mempool dynamics flagged)

Total: 7 criteria, at the cap.

### Step 5: Assign weights

Apply 3-tier bucket:

Must-have (8-10):
- C1 fund safety: 10 (top priority constraint)
- C2 reversibility: 8 (floor 7 from cynefin, raised to 8 for complicated domain + costly reversibility)

Important (5-7):
- C3 implementation time: 7 (floor 6, raised to 7 because audit dependency lengthens timeline)
- C4 audit cost: 6
- C5 UX continuity: 6 (iceberg.patterns flagged this)
- C6 gas efficiency: 5 (named success criterion but not load-bearing)
- C7 mempool resilience: 5 (iceberg.structures flagged but mitigation paths exist)

Sum of weights: 47 (under 50 cap).

### Step 6: Score cells

Surviving options: B, C, D.

| Option | C1 fund (10) | C2 rev (8) | C3 time (7) | C4 audit (6) | C5 ux (6) | C6 gas (5) | C7 mempool (5) |
|---|---|---|---|---|---|---|---|
| B | 9 (90) | 8 (64) | 6 (42) | 7 (42) | 7 (42) | 8 (40) | 7 (35) |
| C | 7 (70) | 6 (48) | 8 (56) | 5 (30) | 9 (54) | 5 (25) | 4 (20) |
| D | 6 (60) | 9 (72) | 5 (35) | 6 (36) | 5 (30) | 6 (30) | 6 (30) |

Evidence for high-confidence cells:

- B × C1 (9): Stargate ($42M), Radiant ($18M), Ethena ($300M) used dual-deploy + drain without fund loss. evidence/decide-prior-art.md.
- B × C2 (8): drain is pausable; if v2 has issue, halt drain and users continue on v1. Source: LZ docs.
- B × C6 (8): OFTv2 measured 22% gas savings on cross-chain transfers. evidence/decide-base-rates.md.
- C × C5 (9): wrapping preserves the v1 address; UX is unchanged. Source: iceberg.patterns.
- C × C3 (8): wrapping is the simplest implementation, ~2 weeks vs B's ~5 weeks. Source: prior team estimates.
- D × C2 (9): separate token leaves v1 fully intact; v2 can be paused without affecting v1 holders. Source: inversion-define.
- C × C7 (4): wrapping adds an extra cross-chain hop, amplifying mempool delays. Source: iceberg.structures.
- D × C5 (5): users hold both v1 and v2 confusingly; UX is split. Source: iceberg.patterns.

### Step 7: Compute totals

```
B = 90 + 64 + 42 + 42 + 42 + 40 + 35 = 355
C = 70 + 48 + 56 + 30 + 54 + 25 + 20 = 303
D = 60 + 72 + 35 + 36 + 30 + 30 + 30 = 293
A = 0 (disqualified)
```

Ranking:
1. B (355)
2. C (303)
3. D (293)

Gap_pct (top vs second): (355 − 303) / 303 = 17.2%

Top vs 1.5× second: 355 / 303 = 1.17 (less than 1.5)

### Step 8: Apply triggers

- top_two_within_5pct: false (gap = 17.2%) → Hard Choice does NOT fire
- top ≥ 1.5× second: false (1.17 < 1.5) → confidence rubric +0
- disqualifier present: true (A) → noted in output
- complex domain advisory mode: false (cynefin = complicated)

State updates:
```json
{
  "decision_matrix": {
    "top_option": "B (dual-deploy + drain)",
    "runner_up": "C (wrapped legacy)",
    "gap_pct": 17.2,
    "top_two_within_5pct": false,
    "top_ge_1_5x_second": false,
    "disqualified": ["A (big-bang single-cutover)"],
    "mode": "decisive"
  }
}
```

### Output written

```markdown
# Decision Matrix, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T17:55:00Z
**Inputs read:** cynefin.md, zwicky-box.md, productive-thinking.md, inversion-define.md, iceberg.md, intake.json, evidence/decide-prior-art.md, evidence/decide-base-rates.md
**Cynefin domain:** complicated
**Mode:** decisive

## Options

| Code | Option | Source | Status |
|---|---|---|---|
| A | Big-bang single-cutover | zwicky-box | DISQUALIFIED (inversion-define: freezes funds during cutover) |
| B | Dual-deploy + drain | zwicky-box, productive-thinking | active |
| C | Wrapped legacy | productive-thinking | active |
| D | Separate token + voluntary migration | zwicky-box | active |

## Criteria

| Code | Criterion | Weight | Source | Justification |
|---|---|---|---|---|
| C1 | Fund safety | 10 | success_criteria + inversion-define | "must NOT lose funds" is the highest constraint |
| C2 | Reversibility | 8 | intake.reversibility + cynefin weight override | costly + complicated raises floor 7 to 8 |
| C3 | Implementation time | 7 | intake.time_pressure | this-month deadline + audit dependency |
| C4 | Audit cost | 6 | inversion-define | failed audit is recoverable but costly |
| C5 | UX continuity | 6 | iceberg.patterns | users expect < 30s settle |
| C6 | Gas efficiency | 5 | success_criteria | named success criterion |
| C7 | Mempool resilience | 5 | iceberg.structures | cross-chain mempool dynamics flagged |

## Score Matrix

| Option | C1 (10) | C2 (8) | C3 (7) | C4 (6) | C5 (6) | C6 (5) | C7 (5) | Total |
|---|---|---|---|---|---|---|---|---|
| ~~A~~ | DISQUALIFIED | | | | | | | 0 |
| B | 9 (90) | 8 (64) | 6 (42) | 7 (42) | 7 (42) | 8 (40) | 7 (35) | 355 |
| C | 7 (70) | 6 (48) | 8 (56) | 5 (30) | 9 (54) | 5 (25) | 4 (20) | 303 |
| D | 6 (60) | 9 (72) | 5 (35) | 6 (36) | 5 (30) | 6 (30) | 6 (30) | 293 |

## Ranking

1. B (Dual-deploy + drain): 355
2. C (Wrapped legacy): 303
3. D (Separate token): 293

Gap: 17.2% (B leads C)
Top ≥ 1.5× second: false

## Sensitivity

Weight-flip stability: swap C1 (10) and C2 (8). New B = 343, new C = 297. Gap narrows to 15.5%. B remains top. Stable.

Score-floor stability: drop B's lowest cell (C3 = 6) by 2 points. New B = 343. Still leads C by 40. Stable.

Decisive weight: C1 (fund safety, w=10). If B's safety score drops below 7, recommendation flips to C.

## Triggers

- top_two_within_5pct: false → Hard Choice does NOT fire
- top ≥ 1.5× second: false → confidence rubric +0
- disqualifier present: true → A's disqualification is binding
- complex advisory mode: false

## What This Means For The Decision

Recommendation: **B (Dual-deploy + drain)** with 17.2% lead over C (wrapped legacy). Confidence rubric +0 (clear lead but not dominant).

Most load-bearing assumption: B's fund safety score (9) based on 3 prior protocol migrations. If a counter-example surfaces, recommendation could shift to C (safety score 7).

Hard Choice does NOT fire. Second-order will run on B + C (top 2). Six Hats normal weighting. Confidence-Speed-Quality QUALITY mode (complicated + costly reversibility).

## Completeness: 9/10

- All criteria traced to source: +2
- Weights justified: +2
- Evidence cited on 8 of 21 cells (38%): +1 (target ≥ 60%)
- Disqualifier explicit: +2
- Sensitivity check performed: +2
```

### What the next framework (Second-Order) inherits

Second-Order receives:
- Top 2 options: B (dual-deploy + drain) and C (wrapped legacy)
- Cynefin domain: complicated → 3 levels of "and then what?" (complex would have forced 4 levels)
- Note from cynefin: connection-circles found a reinforcing cycle (bridge volume → LP fees → liquidity), so second-order should explicitly trace amplification through that cycle
- The runner-up gap (17.2%) is comfortable, so second-order serves as confirmation rather than tiebreaker

Second-Order then traces 1st/2nd/3rd-order effects of B and C and outputs a table the recommendation references.

---

## What This Means For The Decision

Decision Matrix is the workhorse of Phase 3 in simple and complicated domains. When it works, the team has a defensible recommendation with a clear gap, traceable criteria, and weight-flip stability. The matrix's job is to make the team's stated values arithmetic, then compare options against those values without negotiation.

When the matrix is built well, the rest of Phase 3 confirms or challenges its top option. When it is built badly (criterion inflation, weight bias laundering, disqualifier amnesia), the rest of Phase 3 papers over the rot. The forcing function in this framework is the per-cell evidence requirement: cells without specific citations are downgraded; high-confidence cells without source are reduced to the middle.

The cost of skipping Decision Matrix in a complicated-domain run: the team makes a decision from impression and momentum, with no audit trail and no defensible gap. The cost of running it badly: the team makes a confident-wrong decision dressed up as analysis, with the matrix's apparent rigor laundering the bias. The benefit of running it right: a recommendation the team can defend in an after-action review six months later, with the cells and weights showing exactly why this option won.

When the matrix's top two are within 5%, the framework's job is to surrender to Hard Choice. When the gap is dominant (≥ 1.5×), the framework's job is to earn the rubric +2 and let downstream frameworks confirm. Either way, the matrix is one input to the recommendation, not the recommendation itself.
