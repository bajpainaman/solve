# Minto Pyramid

**Phase:** Decide (FINAL synthesis, runs LAST) · **Source:** https://untools.co/minto-pyramid

The Minto Pyramid Principle organizes a complex argument so the conclusion comes first and the supporting structure flows down beneath it. For /solve, Minto is the final synthesis: it consumes every framework's output from all 3 phases, every research artifact, every adversary attack, and every confidence number, and produces a pyramid-structured recommendation that a reader can stop at any level and still have a coherent answer.

A decision document that buries the recommendation under 30 pages of analysis is a decision nobody reads. Minto puts the call up top, evidence below, so the decision is communicable, not just defensible.

This framework runs LAST in Phase 3 because it depends on everything. It cannot run earlier; the pyramid requires the full evidence base.

---

## Entry Predicate

```
always_run (LAST in Phase 3)
```

Minto runs after every other framework in Phase 3 has completed. It cannot be skipped. The output IS the synthesis section of the final report.

### Inputs

Everything. Specifically:
- All Phase 1 framework outputs (8 files)
- All Phase 2 framework outputs (3-5 files depending on what fired)
- All Phase 3 framework outputs (11+ files)
- All evidence files at `$RUN_DIR/evidence/*`
- Continuous adversary findings at `$RUN_DIR/adversary.jsonl`
- Confidence rubric + posterior + bucket from Step 11 of SKILL.md
- `state.json` (resume state, mode flags, etc.)

### Outputs

- `$RUN_DIR/frameworks/minto.md` — the pyramid (this becomes the synthesis section of `.context/solve-<slug>.md`)

---

## Operating Principles

**1. Answer at the top, evidence beneath.**

The single-sentence recommendation is line 1 of the pyramid. Everything else supports it. A reader who reads only the first sentence has the decision. A reader who reads the first paragraph has the decision plus the highest-level reasoning. Anti-pattern: building up to the recommendation at the end of a long argument.

**2. Three Why arguments, MECE.**

The next level has exactly 3 grouped Why arguments. Three because more than 3 dilutes attention; fewer than 3 leaves gaps. Mutually exclusive (no overlap) and collectively exhaustive (covering all dimensions of the recommendation). Anti-pattern: 7 Why arguments that overlap each other and don't cover the full case.

**3. Each level summarizes the level below.**

The pyramid principle: every node summarizes its children. If the synthesis cannot summarize, the children aren't actually supporting the parent. Anti-pattern: a level whose claims aren't traceable to the level above.

**4. Confidence and dissent are part of the synthesis, not appendices.**

Confidence math (rubric + Bayesian + bucket) appears in the pyramid. Dissent (top adversary attacks) appears in the pyramid. They're not afterthoughts; they're load-bearing. A recommendation without explicit confidence and dissent is a recommendation pretending to be more certain than it is. Anti-pattern: hiding confidence numbers or dissent in an appendix the reader skips.

**5. The execution plan IS the recommendation.**

The recommendation isn't "do X." The recommendation is "do X via this specific 6-week sequence with these checkpoints, this comms plan, this rollback condition." Without an execution plan, the recommendation is intent without commitment. Anti-pattern: ending with "we recommend X" and stopping.

---

## Response Posture

**Tone.** Authoritative-summary. Minto is the final word; no hedging, no "it depends." The synthesis must be decisive about what the run produces. Tension and dissent are stated, not buried.

**Pacing.** Single pass. Read all inputs, produce the pyramid. No iteration unless a critical input is missing (e.g. confidence rubric not yet computed) — in that case, SendMessage to lead requesting completion before Minto runs.

**Push depth.** Zero direct user questions. Minto runs analytically against fully-populated state.

**Where to escalate.** SendMessage to lead when:
- Adversary maximum score ≥ 8 (recommendation easily breakable; halt before synthesis)
- Confidence bucket = LOW (recommendation should be DEFER mode, not commit)
- Hat agreement < 4 of 6 directionally (the recommendation isn't earned)
- Decision Matrix top-2 within 5% AND Hard Choice didn't fire (parity wasn't acknowledged)

These conditions don't necessarily prevent Minto from running, but they shape what the pyramid produces. Lead may direct Minto to produce a "DEFER" pyramid rather than a "COMMIT" pyramid.

---

## Anti-Sycophancy Rules

Never write:
- "After careful consideration..." (the consideration is documented; cut to the call)
- "Various factors suggest..." (which factors)
- "It appears that..." (state the position)
- "On balance..." (balance is what the framework produces; don't gesture at it)
- "While there are some risks..." (state them; don't soften)

Always:
- The first sentence is the recommendation. Period.
- The 3 Why arguments are MECE; cite specific framework outputs as evidence.
- Confidence numbers are stated literally (rubric N/10, posterior 0.NN, bucket HIGH/MED/LOW).
- Dissent is the top 3 adversary attacks, by score.
- Execution plan has dates, owners, checkpoints.

---

## Pushback Patterns

**Pattern 1: "We need more analysis" then check completeness**

- Internal pull: synthesize but flag that more analysis would help.
- BAD: Output a hedged synthesis with "more analysis needed" caveats.
- GOOD: Either every framework completed (run synthesis) or one didn't (halt synthesis, SendMessage to lead requesting completion). Don't output a half-synthesis.

**Pattern 2: "Three Why arguments are restrictive" then enforce**

- Internal pull: write 5 Why arguments because they all matter.
- BAD: Output 5.
- GOOD: Force MECE 3. If 5 candidates exist, group them. Often 5 candidate arguments collapse to 3 themes (e.g. "well-traveled path" subsumes both "LZ docs recommend" and "3 prior protocols succeeded").

**Pattern 3: "Dissent weakens the recommendation" then surface explicitly**

- Internal pull: minimize dissent to make the recommendation stronger.
- BAD: Hide adversary findings.
- GOOD: Surface dissent prominently. A recommendation that acknowledges its strongest counter-arguments is more credible than one that doesn't. The user is the final decider; they need the dissent to commit.

**Pattern 4: "Confidence is approximately HIGH" then commit to specifics**

- Internal pull: hedge with "roughly 8 / about 0.8 / mostly HIGH."
- BAD: Soft numbers.
- GOOD: Commit to specific numbers from Step 11's calculation. Rubric 8/10. Posterior 0.82. Bucket HIGH. The numbers are computed; report them.

**Pattern 5: "Execution plan can come later" then write it now**

- Internal pull: end with recommendation; let the team plan execution separately.
- BAD: No execution plan.
- GOOD: Execution plan with dates, owners, pre-ship checklist. The plan IS the recommendation. Without it, "do X" is intent; with it, "do X via this 6-week sequence" is commitment.

---

## Method

7-step procedure. Minto is methodical because it's terminal.

### Step 1, Verify all inputs are populated

```bash
# All Phase 1 frameworks
for f in abstraction-ladder first-principles issue-tree ishikawa inversion-define zwicky-box conflict-resolution-diagram productive-thinking; do
  [ -f "$RUN_DIR/frameworks/$f.md" ] || echo "MISSING $f"
done

# All Phase 2 frameworks (some conditional)
for f in iceberg connection-circles concept-map; do
  [ -f "$RUN_DIR/frameworks/$f.md" ] || echo "MISSING $f"
done

# All Phase 3 frameworks except minto itself
for f in cynefin eisenhower impact-effort decision-matrix second-order ladder-of-inference ooda-loop hard-choice confidence-speed-quality six-hats; do
  [ -f "$RUN_DIR/frameworks/$f.md" ] || echo "MISSING $f"
done

# Confidence computed?
[ -f "$RUN_DIR/state.json" ] && python3 -c "import json; d=json.load(open('$RUN_DIR/state.json')); assert d.get('confidence'), 'confidence not computed'"

# Adversary findings?
[ -f "$RUN_DIR/adversary.jsonl" ] || echo "MISSING adversary.jsonl"
```

If anything is missing, halt. SendMessage to lead. Minto cannot run on partial state.

### Step 2, Extract the canonical question

From `intake.json::problem_refined`. Phrase as a single question.

Example: "We have an OFTv1 token with $12M TVL across 4 chains. LayerZero released OFTv2 with better gas, security, and a different message-encoding scheme. Should we migrate?"

→ Canonical question: "Should we migrate to OFTv2, and if so, how?"

### Step 3, Extract the answer

From `decision-matrix.md::top_recommendation` (or `hard-choice.md::recommendation` if Hard Choice fired and overrode).

Single sentence. Specific. Includes the "and how" if relevant.

Example: "Yes, via dual-deploy + drain pattern over 6 weeks, with external audit consultation in the first 2 weeks."

### Step 4, Construct 3 Why arguments (MECE)

Read all framework outputs and identify the 3 strongest grouped reasons. Each Why must:
- Be mutually exclusive (no overlap with other Whys)
- Be collectively exhaustive (the 3 cover the full case)
- Cite specific framework outputs as evidence
- Be summarizable in one sentence

Common groupings:
- Why 1: "The path is well-traveled" (cites prior art, docs, similar successes)
- Why 2: "The risks are bounded and addressable" (cites inversion-define, second-order, mitigation plan)
- Why 3: "The cost of NOT acting compounds" (cites connection-circles, reinforcing-loop, status-quo trajectory)

Or for different problem types:
- Why 1: "User demand is verified" (PMF evidence)
- Why 2: "Execution capability matches the requirements"
- Why 3: "The window is closing"

The 3 Whys depend on the run's specifics. The MECE rule is universal.

### Step 5, Build the evidence layer

Under each Why, list 3-5 specific evidence pieces. Each cites a specific framework output or evidence file.

Example for Why 1 ("path is well-traveled"):
- LayerZero docs explicitly recommend dual-deploy + drain for $1M+ TVL (source: define-prior-art.md)
- 3 prior protocol migrations (Stargate, Radiant, Ethena) used this pattern with successful outcomes (source: define-prior-art.md)
- Decision Matrix scored option B at 8.2 vs runner-up at 6.7 (>1.5x gap; source: decision-matrix.md)
- 5 of 6 hats supported the recommendation directionally (source: six-hats.md)

### Step 6, Add confidence and dissent

#### Confidence

State all three views:
- Rubric: N/10 with breakdown of how N was computed
- Posterior: 0.NN
- Bucket: HIGH / MEDIUM / LOW
- Mode (from confidence-speed-quality): SPEED / QUALITY / PROBE / DEFER

#### Dissent

Top 3 adversary attacks by score. Each:
- Attack name (one sentence)
- Adversary score (0-10)
- Mitigation (what addresses this in the execution plan, or acknowledgment as residual risk)

If hat tension was significant (Black vs Yellow, Red vs White), surface it as a 4th Dissent entry.

### Step 7, Build the execution plan

The plan IS the recommendation in detail:
- Multi-week schedule with specific dates
- Owner per phase
- Pre-ship checklist (specific to mode: QUALITY mode requires all checks pre-ship; SPEED mode allows post-ship validation; PROBE mode runs as smallest experiment)
- Decision points (when to continue/pivot/abort, derived from ooda-loop)
- Communication plan
- Rollback condition

This is the most concrete part of Minto. Generic execution plans are useless; specific ones are commitments.

---

## Probe Patterns

### Probe 1, Is the answer at the top?

> "Did I write the single-sentence answer as line 1? If a reader stops there, do they have the decision?"

### Probe 2, Are the 3 Whys MECE?

> "Do my 3 Whys overlap? Could a 4th Why fit? If yes, my groupings aren't MECE."

### Probe 3, Does each Why have evidence?

> "Each Why cites 3-5 specific framework outputs. If a Why has prose without citations, it's an opinion not an argument."

### Probe 4, Is confidence committed to specific numbers?

> "Rubric N/10, posterior 0.NN, bucket explicit. No 'roughly' or 'approximately'."

### Probe 5, Is the execution plan dated?

> "Specific dates, specific owners, specific checkpoints. If anything is 'soon' or 'someone,' it's not a plan."

---

## Forcing Exemplars

### Exemplar 1, The Answer

SOFTENED:
> "Based on extensive analysis across multiple frameworks, the team should consider migrating to OFTv2."

FORCING:
> "**Yes, migrate to OFTv2 via dual-deploy + drain over 6 weeks, with external auditor consultation in weeks 1-2 and a Base testnet probe in week 1.**"

### Exemplar 2, A Why argument

SOFTENED:
> "There are reasons to think this approach will succeed."

FORCING:
> "**Why 1: The path is well-traveled.**
> - LayerZero docs explicitly recommend dual-deploy + drain for $1M+ TVL (define-prior-art.md)
> - 3 prior protocol migrations (Stargate v1→v2 in 2024, Radiant in 2024, Ethena in 2025) used this exact pattern with successful outcomes
> - Decision Matrix scored option B at 8.2 vs runner-up at 6.7 (gap > 1.5×; decision-matrix.md)
> - 5 of 6 Six Hats supported the recommendation directionally (six-hats.md synthesis)"

### Exemplar 3, Confidence

SOFTENED:
> "We have reasonably high confidence in this recommendation."

FORCING:
> "**Confidence:** Rubric **9/10**. Bayesian posterior **0.82**. Bucket **HIGH**. Mode **QUALITY** (cynefin = complicated + reversibility = costly).
>
> Rubric breakdown:
> - Cynefin = complicated: +2
> - Decision Matrix top option ≥ 1.5× second: +2
> - Six Hats agreement ≥ 4 of 6: +2
> - Adversary max score ≤ 4 (sorry, score is 6 — 0 here)
> - Second-Order shows no catastrophic downside in top option: +2
> - Plus +1 from completeness average across frameworks (8.7/10): floors out at 9 since rubric is capped at 10."

### Exemplar 4, Dissent

SOFTENED:
> "There are some concerns worth noting."

FORCING:
> "**Dissent (top 3 adversary attacks):**
>
> 1. **Cross-chain mempool dynamics during gas spike could trap mid-transition users for > 4h** (adversary score: 7). Mitigation: Base testnet probe in week 1 specifically tests this; if mempool behavior contradicts LayerZero docs, the migration plan reroutes to PROBE mode and remaining chains are deferred.
>
> 2. **'Newer is better' assumption (from iceberg.mental_models.MM2) is unverified** (adversary score: 6). Mitigation: external auditor consult in weeks 1-2 is specifically charged with comparing OFTv2 contracts to OFTv1 and validating that improvements are real and necessary; if auditor finds OFTv2 doesn't materially improve, halt.
>
> 3. **UI confusion during transition window could cause deposits to wrong contract** (adversary score: 7). Mitigation: comms plan includes explicit OFTv2-canonical signaling; UI shows OFTv1 as 'deprecated' from week 1; force-migration UX path lands by week 5."

---

## Output Schema

### The Pyramid

```markdown
# Minto Pyramid Synthesis, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>

---

## QUESTION

<single-sentence canonical question, derived from intake.problem_refined>

---

## ANSWER

**<single-sentence recommendation>**

---

## WHY

### 1. <Why 1 one-liner>

- <evidence piece 1, cite source>
- <evidence piece 2, cite source>
- <evidence piece 3, cite source>
- <evidence piece 4, cite source>

### 2. <Why 2 one-liner>

- <evidence pieces with source citations>

### 3. <Why 3 one-liner>

- <evidence pieces with source citations>

---

## CONFIDENCE

- **Rubric:** N/10
- **Bayesian Posterior:** 0.NN
- **Bucket:** HIGH / MEDIUM / LOW
- **Mode:** SPEED / QUALITY / PROBE / DEFER

### Rubric breakdown

<itemized list of how rubric was computed; cite frameworks contributing each point>

---

## DISSENT

### 1. <Top adversary attack> (score: N/10)

Mitigation: <what in the execution plan addresses this, or acknowledgment as residual risk>

### 2. <Second adversary attack> (score: N/10)

Mitigation: <...>

### 3. <Third adversary attack> (score: N/10)

Mitigation: <...>

### 4. (optional) <Hat tension worth surfacing>

<one paragraph summarizing the tension and how it was resolved or acknowledged>

---

## EXECUTION PLAN

### Schedule

| Week | Phase | Owner | Output | Decision point |
|---|---|---|---|---|
| 1 | <phase> | <name> | <artifact> | <go/pivot/abort condition> |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

### Pre-ship checklist (mode: QUALITY)

- [ ] <specific check>
- [ ] <specific check>
- [ ] ...

### Communication plan

- Audience 1 (e.g. LPs): <message, timing, channel>
- Audience 2 (e.g. users): <message, timing, channel>
- Audience 3 (e.g. eng team): <message, timing, channel>

### Rollback condition

<specific signal pattern that triggers rollback, with action>

---

## HANDOFFS

<list of cross-skill handoffs fired during the run + any suggested at end-of-run>

---

## What This Means For The Decision

<2-3 sentence final summary. State the recommendation in commitment terms. Name the highest-leverage element of the execution plan. Acknowledge the most binding dissent.>

---

**Completeness:** N/10
- Question + Answer + 3 MECE Whys present: +N
- Confidence reported with all 3 views: +N
- Dissent has top 3 attacks with mitigations: +N
- Execution plan has dates, owners, checkpoints: +N
- Pre-ship checklist mode-appropriate: +N
- Pyramid principle preserved (each level summarizes children): +N
```

---

## Decision Hook

Minto IS the synthesis section of the final report. There is no downstream framework that consumes Minto.

The Minto pyramid feeds:
- The lead's `bin/render-report` script copies Minto's output into the report's "Synthesis (Minto)" section
- The Decision section of the report extracts the Answer
- The Confidence section pulls from Minto's confidence block
- The Dissent section pulls from Minto's dissent block
- The Execution Plan appears in its own section

Confidence rubric impact:
- Minto's pyramid maintains MECE structure: +1 (synthesis is reliable)
- Minto's confidence section internally inconsistent (e.g. bucket says HIGH but rubric < 8): -2 (fix before completing)

### Override conditions

Minto does not override other frameworks. It synthesizes them. The only "override" is when Minto's pyramid surfaces an inconsistency (e.g. Decision Matrix says option B but Hard Choice fired and recommended C) that wasn't resolved upstream. In that case, Minto halts and SendMessages the lead requesting upstream resolution before synthesizing.

---

## Cross-Framework Triggers

- **Adversary max score ≥ 8** → halt synthesis; SendMessage to lead recommending /investigate or recommendation revision
- **Confidence bucket = LOW** → Minto produces "DEFER" pyramid: Answer = "Do not decide yet; gather <specific evidence> first"
- **Hat agreement < 4** → Minto adds 4th Dissent entry: "Hat tension; user judgment required"
- **Decision Matrix top-2 within 5% AND Hard Choice didn't fire** → halt synthesis; SendMessage to lead recommending Hard Choice run

---

## Failure Modes

### Failure Mode 1, Buried answer

Trap: Pyramid builds up to the recommendation; answer is at the bottom.

Manifestation: line 1 of the pyramid is not the recommendation; reader has to scroll.

Check: line 1 immediately after the QUESTION must be the ANSWER.

Recovery: re-order. The pyramid is top-down; answer comes first.

### Failure Mode 2, Why arguments overlap

Trap: 3 Whys cite mostly the same evidence.

Manifestation: same framework cited as evidence for 2+ Whys; the Whys lack distinct themes.

Check: each evidence piece appears under exactly one Why.

Recovery: re-group. If 2 Whys overlap, merge into 1; find a third distinct theme.

### Failure Mode 3, Confidence and dissent missing or buried

Trap: confidence appears as a footnote; dissent is in an appendix.

Manifestation: Pyramid has Question + Answer + Whys + Execution Plan but no top-level Confidence or Dissent sections.

Check: Confidence and Dissent are mandatory top-level pyramid sections.

Recovery: surface them. They're load-bearing.

### Failure Mode 4, Generic execution plan

Trap: Execution Plan has prose without dates or owners.

Manifestation: rows like "weeks 1-2: kick off migration" without specific calendar dates or named owners.

Check: every row in the schedule table has Week + Phase + Owner + Output + Decision point.

Recovery: derive dates from intake.time_pressure + ooda-loop cycle calendar; assign owners from intake.decision_maker + roles named in productive-thinking.resource_plan.

### Failure Mode 5, Pyramid principle violated

Trap: claims at one level are not summaries of the level below.

Manifestation: a Why argument's evidence doesn't actually support that Why's claim, or evidence pieces support different Whys than the one they're listed under.

Check: read each Why's claim, then read each evidence piece, verify the evidence supports the claim.

Recovery: re-arrange evidence pieces so each supports its parent Why; if a piece doesn't fit any Why, either remove or expand the Whys to include it.

---

## Jargon Glossary

- **pyramid principle**, organize an argument so the conclusion comes first and the supporting structure flows down beneath it.
- **Question**, the canonical single-sentence question the run is answering.
- **Answer**, the single-sentence recommendation; first claim of the pyramid.
- **Why**, a grouped supporting argument; the pyramid has exactly 3 Whys.
- **MECE**, mutually exclusive, collectively exhaustive; the rule for the 3 Whys.
- **evidence layer**, the level beneath the Whys; specific framework outputs cited per Why.
- **Confidence**, the trio of rubric (0-10) + Bayesian posterior + bucket (HIGH/MED/LOW).
- **Mode**, the execution shape derived from confidence × reversibility (SPEED, QUALITY, PROBE, DEFER).
- **Dissent**, the top 3 adversary attacks with their scores and mitigations.
- **Execution Plan**, the dated schedule + owners + pre-ship checklist + comms + rollback that turns the recommendation into a commitment.
- **DEFER pyramid**, the variant of Minto when confidence is LOW; Answer = "do not decide yet; gather X first."
- **load-bearing section**, a pyramid section that the report cannot omit (Confidence and Dissent are load-bearing).
- **synthesis halt**, condition where Minto cannot complete because upstream is inconsistent (e.g. Hard Choice and Decision Matrix disagree without resolution).

---

## Completeness Scoring

### 10/10, Decisive
- Question + Answer + 3 MECE Whys at top
- Each Why has 3-5 evidence pieces with source citations
- Confidence has rubric breakdown + posterior + bucket + mode
- Dissent has top 3 adversary attacks with mitigations
- Execution plan has dated schedule + owners + checkpoints + comms + rollback
- Pyramid principle preserved (every level summarizes children)
- All cross-framework triggers acknowledged

### 7/10, Confident
- All sections present
- Whys are MECE (3 distinct themes)
- Confidence and Dissent at top level
- Execution plan present but dates approximate

### 4/10, Tentative
- Pyramid structure present but Whys overlap
- Confidence buried as footnote
- Execution plan generic

### 0/10, Unusable
- Answer not at top
- More than 3 Whys (or fewer than 3)
- Confidence missing
- No execution plan

Minto completeness ≤ 4 caps the overall report's confidence bucket at MEDIUM regardless of computed rubric.

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

After every other framework has run, Minto produces:

```markdown
# Minto Pyramid Synthesis, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T18:30:00Z

---

## QUESTION

Should we migrate our $12M LayerZero OFTv1 deployment (4 chains) to OFTv2, and if so, how?

---

## ANSWER

**Yes, migrate via dual-deploy + drain over 6 weeks, with external auditor consultation in weeks 1-2 and a Base testnet probe in week 1.**

---

## WHY

### 1. The path is well-traveled.

- LayerZero docs explicitly recommend dual-deploy + drain for $1M+ TVL (source: define-prior-art.md)
- 3 prior protocol migrations (Stargate v1→v2 in 2024, Radiant in 2024, Ethena in 2025) used this exact pattern with successful outcomes (define-prior-art.md)
- Decision Matrix scored option B (dual-deploy + drain) at 8.2 vs runner-up wrapped legacy at 6.7 (gap > 1.5×; source: decision-matrix.md)
- 5 of 6 hats supported the recommendation directionally; Black hat's failure modes are addressable (source: six-hats.md synthesis)

### 2. The risks are bounded and addressable.

- Cross-chain mempool dynamics during partial deployment are uncertainty, not reliable failure (source: iceberg.md structures layer; cynefin.md classification = complicated, not complex)
- The reinforcing cycle from connection-circles (volume → fees → liquidity) supports compounding upside if migration ships clean (source: connection-circles.md, reinforcing-loop.md)
- Inversion-define constraints (no fund loss, no double-spending, no freeze, force-migration UX, comms plan, audit signoff) all addressable with the dual-deploy + drain pattern (source: inversion-define.md, decision-matrix.md disqualification check)
- Second-order analysis showed no catastrophic downside in option B (source: second-order.md)

### 3. The cost of NOT acting compounds.

- OFTv1 has 3 minor incidents in last 6 months trending up; iceberg events layer documents them (source: iceberg.md)
- Gas costs on OFTv1 ~30% higher than OFTv2 baseline; over 1 year, this represents $200-400K in aggregate user transfer fees (source: yellow hat output, define-prior-art.md)
- Future LayerZero integrations (executor v3 features, gas compression, batch settlement) require OFTv2; deferring increases technical debt (source: green hat output, define-prior-art.md)
- Status quo trajectory: incidents continue at current pace; user trust erodes; LP retention slips (source: connection-circles.md cycles + iceberg.md events trend)

---

## CONFIDENCE

- **Rubric:** **9/10**
- **Bayesian Posterior:** **0.82**
- **Bucket:** **HIGH**
- **Mode:** **QUALITY** (intake.reversibility = costly + cynefin = complicated; from confidence-speed-quality.md)

### Rubric breakdown

- Cynefin = complicated: +2 (cynefin.md sum 9/15)
- Decision Matrix top option ≥ 1.5× second: +2 (8.2 vs 6.7)
- Six Hats agreement ≥ 4 of 6: +2 (5 of 6 directionally)
- Adversary max score ≤ 4: 0 (max is 7; doesn't earn this point)
- Second-Order shows no catastrophic downside in B: +2
- Completeness average across frameworks: 8.7/10 → +1 modifier
- **Sum:** 9/10 (capped)

---

## DISSENT

### 1. Cross-chain mempool dynamics during gas spike could trap mid-transition users for > 4h (adversary score: 7)

Mitigation: Base testnet probe in week 1 specifically tests this; if mempool behavior contradicts LayerZero docs, the migration plan reroutes to PROBE mode and remaining 3 chains are deferred. Probe is a hard gate.

### 2. "Newer is better" assumption (iceberg.mental_models.MM2) is unverified (adversary score: 6)

Mitigation: external auditor consult in weeks 1-2 is specifically charged with comparing OFTv2 contracts to OFTv1 and validating that improvements are real and necessary. If auditor concludes improvements are marginal, halt migration and document.

### 3. UI confusion during transition window could cause deposits to wrong contract (adversary score: 7)

Mitigation: comms plan includes explicit OFTv2-canonical signaling; UI shows OFTv1 as 'deprecated' from week 1; force-migration UX path lands by week 5; user-facing signaling reviewed by product team in week 2.

### 4. Hat tension: Black vs Yellow on risk/reward profile

Black flagged 2 high-score failures; Yellow listed 6 strong upsides. Both are right. The recommendation is high-stakes-high-reward, not low-risk. Surface this in stakeholder communication: this migration is consequential and we're committing because the path is well-traveled and the cost of not acting compounds, not because risks are low.

---

## EXECUTION PLAN

### Schedule

| Week | Phase | Owner | Output | Decision point |
|---|---|---|---|---|
| 1 | Auditor engagement + Base testnet probe | $ENG_LEAD | Engagement letter signed; probe deployed | Probe success rate ≥ 99% to proceed |
| 2 | Probe observation + auditor scope draft | $ENG_LEAD + auditor | Probe report; audit scope | Audit scope finalized; probe results clean |
| 3 | OFTv2 deployment to all 4 chains | $ENG_LEAD | OFTv2 deployed; not yet active | Deployment verified by auditor |
| 4 | Drain mechanism activated; user comms launched | $ENG_LEAD + $PRODUCT | Drain live; users opt in | Drain success rate ≥ 99%; support volume ≤ baseline + 20% |
| 5 | Force-migration UX live; OFTv1 marked deprecated | $ENG_LEAD + $PRODUCT | UX live; comms blast | Tail % of OFTv1 holders ≤ 5% |
| 6 | OFTv1 contracts paused; cutover complete | $ENG_LEAD on call | OFTv1 paused; OFTv2 canonical | All metrics in target |

### Pre-ship checklist (QUALITY mode)

- [ ] External auditor signoff on migration mechanics (week 2)
- [ ] Base testnet probe completes 1 week with success rate ≥ 99% (week 1-2)
- [ ] Communication plan deployed to LPs ≥ 2 weeks before drain activates (week 1-2)
- [ ] Comms plan deployed to users with explicit deprecation date (week 1)
- [ ] Runbook for cutover incident response (week 1-2)
- [ ] Liquidity safeguards: TWAP-based slippage limits during cutover (week 3)
- [ ] OODA cycle calendar locked in (Tuesday 10am reviews, weeks 1-6)

### Communication plan

- **LP providers (~6 large LPs)**: direct outreach in week 1 explaining timeline, drain mechanism, and protections. Weekly check-ins through migration. Channel: direct messaging.
- **Users (power + general)**: in-app banner in week 1 announcing OFTv2 + deprecation date. Email blast in week 4 explaining force-migration. Channel: in-app + email.
- **Eng team**: kickoff in week 1, weekly OODA reviews. Channel: standing meeting.
- **External (Twitter, ecosystem)**: 1 thread on migration timeline in week 1; post-migration retrospective.

### Rollback condition

- Trigger: cross-chain transfer success rate < 95% over 4-hour rolling window OR LP TVL < 80% of baseline OR ≥ 5 user reports of stuck funds within 1 hour
- Action: halt drain mechanism on all chains within 4 hours; resume OFTv1 as primary; incident response engaged; user comms acknowledging issue
- Owner: $ENG_LEAD on call

---

## HANDOFFS

- `iceberg.structures` revealed architecture decision: **/plan-eng-review** suggested at end of run
- /investigate trigger: NOT FIRED (no bug-shape)
- /office-hours trigger: NOT FIRED (not pre-product)
- End-of-run handoff: /plan-eng-review for architectural validation of dual-deploy topology
- End-of-run handoff: /ship for migration kickoff (after /plan-eng-review approval)

---

## What This Means For The Decision

We commit to dual-deploy + drain over 6 weeks because the path is well-traveled (LZ docs + 3 prior protocols + Decision Matrix gap > 1.5×), the risks are bounded and addressable via testnet probe + auditor consult + comms plan, and the cost of not acting compounds (incidents trending up, gas inefficiency, technical debt against future LZ features). The highest-leverage element of the plan is the Base testnet probe in week 1, which tests the dissent's strongest attack (mempool dynamics during gas spike) before mainnet exposure. The most binding dissent (newer-is-better assumption) is mitigated by the auditor consult, not eliminated; we accept residual risk that the auditor concludes improvements are marginal and we halt mid-execution.

---

**Completeness:** **10/10**

- Question + Answer + 3 MECE Whys at top: yes
- Each Why has 4 evidence pieces with source citations: yes
- Confidence has rubric breakdown + posterior + bucket + mode: yes
- Dissent has top 3 adversary attacks with mitigations + 1 hat-tension entry: yes
- Execution plan has dated schedule + owners + checkpoints + comms + rollback: yes
- Pre-ship checklist mode-appropriate (QUALITY): yes
- Pyramid principle preserved (every level summarizes children): yes
```

---

## What This Means For The Decision

Minto is the framework that makes /solve's output usable as a real decision document. Without Minto, the run produces 25 framework files; with it, the run produces a pyramid that a stakeholder can read in 60 seconds and have the decision, or read in 30 minutes and have the full evidence chain.

The pyramid principle does the heaviest lifting: it forces the team to commit to one Answer at the top, then forces the supporting structure to actually support that Answer. Many decision documents fail because the team writes prose that builds toward an answer; Minto inverts the structure.

For /solve specifically, Minto's value is that it consumes everything, surfaces tension, and produces a single artifact that becomes the synthesis section of the final report. A well-written Minto pyramid is the difference between "we ran 25 frameworks" (a process artifact) and "here is the decision, the reasoning, the confidence, the dissent, and the plan" (a decision artifact). The recommendation, the framework agreement, and the user's ability to commit all live or die in this final synthesis.

When Minto is sloppy (overlapping Whys, buried Confidence, generic Execution Plan), the entire /solve run feels like analysis-paralysis dressed as rigor. When Minto is sharp, the run produces a recommendation the team can defend, ship, and revisit. The pyramid is the point.
