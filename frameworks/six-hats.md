# Six Thinking Hats (de Bono)

**Phase:** Decide · **Source:** https://untools.co/six-thinking-hats

The framework forces multi-perspective evaluation by spawning 6 concurrent role-play teammates, one per de Bono "hat" (white = facts, red = gut, black = risks, yellow = upsides, green = alternatives, blue = process). Each hat writes its own framework file in isolation. The lead synthesizes after all 6 idle.

The unique structural property: each hat runs in its own context window. The Black hat can't be diluted by Yellow's optimism. The Red hat can't be overruled by White's facts. Independent role-play surfaces tensions the team would have averaged out in a single agent's analysis.

This is the framework's primary value: **adversarial-by-construction.** Six Hats is what you reach for when one perspective dominates and you need genuine disagreement on the table.

---

## Entry Predicate

```
always_run
```

Every recommendation benefits from explicit multi-perspective evaluation before commit. The framework runs late in Phase 3 after Decision Matrix has produced a top option. Six Hats stress-tests that option from 6 angles.

### Inputs

- `frameworks/decision-matrix.md::top_recommendation`
- `frameworks/decision-matrix.md::top_2` (if Hard Choice fired or top-2 are close, run Six Hats on both)
- `intake.problem_refined`
- All prior framework outputs (each hat reads what's relevant to its perspective)

### Outputs

- 6 individual files: `$RUN_DIR/frameworks/six-hats-white.md`, `-red.md`, `-black.md`, `-yellow.md`, `-green.md`, `-blue.md`
- 1 synthesis file: `$RUN_DIR/frameworks/six-hats.md` (this file describes the synthesis structure)

---

## Operating Principles

**1. Hats spawn concurrent, isolate by construction.**

Each hat runs in its own context window. Lead spawns all 6 in a single parallel batch via the Agent tool. They do not see each other's outputs while writing. This is not optional. Anti-pattern: running hats sequentially in one context, where later hats are biased by earlier hats' outputs.

**2. Each hat plays only its role.**

Black writes only risks. Yellow writes only upsides. The hat doesn't qualify or moderate. The discipline produces extremity in each direction; synthesis after the fact balances. Anti-pattern: a "balanced" hat output that hedges within the role.

**3. White hat counts evidence, not interpretations.**

White lists verifiable facts: research findings, prior cases, measured data. It does not say "this is good evidence" or "this is concerning evidence." It says "X happened" or "X is documented." Anti-pattern: White hat doing Yellow or Black hat work by interpreting facts.

**4. Synthesis surfaces tension, not consensus.**

The synthesis file's job is to identify where hats agree (signal) and where they disagree (decision-relevant tension). A synthesis that smooths over disagreement loses the framework's value. Anti-pattern: a "weighted average across hats" recommendation that dilutes the most informative hats.

**5. Blue hat critiques the process, not the recommendation.**

Blue is meta. It evaluates how this /solve run has been conducted: what frameworks were skipped, what evidence is missing, what assumptions weren't surfaced. Blue's output is a process improvement signal, not a content position. Anti-pattern: Blue contributing a 7th opinion on the recommendation.

---

## Response Posture

**Tone (per hat).** Each hat has its own posture. White is forensic. Red is unapologetic. Black is adversarial. Yellow is justified-optimistic. Green is generative. Blue is meta-analytical.

**Pacing.** Lead spawns 6 hats in parallel. Each hat runs to completion writing its own file. Synthesis runs after all 6 idle.

**Push depth.** Hats don't ask the user direct questions. Each hat reads prior framework outputs through its specific lens and produces a file. If a hat lacks evidence to play its role (e.g. Yellow has no upside material), SendMessage to lead requesting research expansion.

**Where to escalate (synthesis stage).** SendMessage to lead when:
- Black hat score ≥ 8 (the recommendation is highly breakable; surface in dissent prominently)
- Hats agreement < 4 of 6 directionally (tension is high; recommendation may need user input)
- Blue hat flags missing process steps (e.g. "Cynefin wasn't run") that are actually required

---

## Anti-Sycophancy Rules

Per-hat:
- **White** never writes: "This evidence suggests..." (state the evidence; interpretation is Yellow/Black's job)
- **Red** never writes: "Some might feel..." (state YOUR gut; this hat is unapologetic)
- **Black** never writes: "We should be careful..." (name the specific failure)
- **Yellow** never writes: "Things could go well..." (name the specific upside and the conditions for it)
- **Green** never writes: "There may be other options..." (generate them)
- **Blue** never writes: "The process seemed thorough..." (specify what was thorough; specify what was missed)

Always (per hat):
- Stay in role. Don't borrow from another hat's job.
- Cite source frameworks for each claim.
- End the file with a one-line "this hat's verdict on the recommendation."

---

## Pushback Patterns (synthesis stage)

**Pattern 1: "Hats roughly agree" then check actual disagreement**

- Internal evidence: synthesis claims 5 of 6 hats agree.
- BAD: Average and recommend.
- GOOD: Re-read each hat's verdict. Look for actual contradictions. If Black says "high risk" and Yellow says "high upside," that's not agreement; it's both being right and the framework's job is to surface that the recommendation is high-stakes-high-reward, not "everyone is on board."

**Pattern 2: "Black is just being negative" then take it seriously**

- Internal pull: discount Black's findings as expected pessimism.
- BAD: Note Black's score and move on.
- GOOD: Black is hired to be hostile. If Black surfaces specific failure modes, those become Dissent appendix items. The recommendation should explicitly address them or acknowledge them as residual risk.

**Pattern 3: "Green's alternatives are weaker" then check the comparison**

- Internal evidence: Green proposed alternative X but Decision Matrix already scored higher options.
- BAD: Dismiss Green.
- GOOD: Re-read Green's proposal. Did it propose an alternative the matrix didn't consider? If yes, the matrix may need a new candidate. If no (Green just re-ranked existing options), discount appropriately.

**Pattern 4: "Blue's process critique is too late" then file as learning**

- Internal pull: Blue says "we should have done X" but it's too late this run.
- BAD: Ignore.
- GOOD: Apply Blue's critique to the next run via gstack-learnings-log. The current run completes with the gap acknowledged in dissent.

**Pattern 5: "Red feels off" then surface as signal**

- Internal pull: Red's gut says "wrong" but the data supports the recommendation.
- BAD: Override Red with data.
- GOOD: Surface Red's gut as a flag. The user is the final decision-maker. Their gut may align with Red's; if so, they should know Red dissented even when data says otherwise.

---

## Method (lead's perspective)

5-step procedure for the lead. The 6 hats run in parallel; the lead orchestrates spawn + synthesis.

### Step 1, Spawn 6 hats in parallel

In a single Agent tool call batch, spawn 6 teammates with `team_name = $TEAM_NAME`:

| Name | subagent_type | Hat |
|---|---|---|
| `hat-white` | general-purpose | White (facts) |
| `hat-red` | general-purpose | Red (gut) |
| `hat-black` | critic | Black (risks) |
| `hat-yellow` | general-purpose | Yellow (upsides) |
| `hat-green` | general-purpose | Green (alternatives) |
| `hat-blue` | architect | Blue (process meta) |

Each gets a self-contained brief (see hat templates below). Each writes to `$RUN_DIR/frameworks/six-hats-<color>.md`.

### Step 2, Hats run to completion

Lead does not interfere. Each hat runs its method. Each marks task completed via TaskUpdate. Each idles automatically.

### Step 3, Lead synthesizes

After all 6 idle, lead reads all 6 output files. Synthesis writes to `$RUN_DIR/frameworks/six-hats.md` with:
- Per-hat one-line summaries
- Agreement (where ≥ 4 hats converge)
- Tension (where hats disagree directionally)
- Blind spots (what Blue flagged as missing)
- Synthesis verdict (does the recommendation hold up under multi-perspective evaluation?)

### Step 4, Shutdown each hat individually

```text
SendMessage(to="hat-white", message={"type":"shutdown_request"})
SendMessage(to="hat-red", ...)
SendMessage(to="hat-black", ...)
SendMessage(to="hat-yellow", ...)
SendMessage(to="hat-green", ...)
SendMessage(to="hat-blue", ...)
```

Wait for all to confirm shutdown. Hats are NOT shut down via TeamDelete (which would happen at end of Step 14 in SKILL.md); they're shut down here so the team's active count returns to 5 before Phase 3 completes.

### Step 5, Update confidence rubric

Based on hat agreement:
- ≥ 4 hats agree directionally on recommendation: +2 to overall rubric
- Black hat score ≤ 4 (recommendation hard to break): +2 (overlaps with adversary score)
- Green hat proposes compelling alternative not in Decision Matrix: -1 (matrix may need re-run)

---

## Hat Templates

### White Hat brief

```
You are `hat-white` in team $TEAM_NAME.
Hat: White (facts only)
Output: $RUN_DIR/frameworks/six-hats-white.md

Your role is forensic. List only verifiable facts about the recommendation:
- Research evidence supporting it (specific cites from $RUN_DIR/evidence/)
- Prior cases or analogs (Stargate, Radiant, Ethena migrations, etc.)
- Measured data from the team's own context (TVL numbers, support volumes,
  historical incident rates)
- Documented best practice (LayerZero docs, audit standards)

What you DON'T do:
- Interpret evidence ("this suggests..." is Yellow or Black's job)
- Assess confidence ("this evidence is reliable" is meta)
- Make recommendations ("we should..." is not your role)

Output schema:
- 5-10 facts, each with source citation
- One-line verdict at the end: "Facts support / contradict / are insufficient for the recommendation"

Read prior frameworks to gather evidence. Cite specifically.
```

### Red Hat brief

```
You are `hat-red` in team $TEAM_NAME.
Hat: Red (gut, intuition, emotion)
Output: $RUN_DIR/frameworks/six-hats-red.md

Your role is unapologetic gut feeling. State the team's emotional reaction
to the recommendation without justification.

What feels right? What feels wrong? Don't explain why. Don't apologize.
The framework's value is this hat's honesty about the felt sense.

Sources for "the team's gut":
- Tone of recent commits and PR descriptions
- Patterns in support ticket responses (anxious / confident / dismissive)
- Eng-channel sentiment (read recent technical Slack-style discussions
  if available; otherwise infer from commit messages)
- The user's own framing in intake.problem_refined

Output schema:
- 3-5 gut reactions, each one sentence
- One-line verdict: "Gut says yes / no / mixed on the recommendation"

Don't argue with yourself. Just report what the team's body knows
that the team's mind hasn't articulated.
```

### Black Hat brief

```
You are `hat-black` in team $TEAM_NAME.
Hat: Black (risks, failure modes, devil's advocate)
Output: $RUN_DIR/frameworks/six-hats-black.md

Your role is hostile-by-design. Treat the recommendation as wrong and
find the strongest reasons it would fail.

Sources:
- $RUN_DIR/frameworks/inversion-define.md (failure paths from Phase 1)
- $RUN_DIR/adversary.jsonl (continuous-adversary findings on each framework)
- $RUN_DIR/evidence/define-failure-modes.md (historical failures)
- The recommendation itself: what assumes the most? what's most fragile?

Output schema:
- 5-7 specific failure modes, each with mechanism + observable signal
- Score each failure 0-10 (10 = high probability + high impact)
- One-line verdict: "Recommendation has X high-score failures; commit / probe / abort"

Be specific, not vague. "User experience could suffer" is bad. "Cross-chain
mempool during gas spike could trap mid-transition users for > 4h" is good.
```

### Yellow Hat brief

```
You are `hat-yellow` in team $TEAM_NAME.
Hat: Yellow (justified optimism, upside)
Output: $RUN_DIR/frameworks/six-hats-yellow.md

Your role is to argue the recommendation's strongest case. Not optimism
in general; the specific upsides this option produces if it succeeds.

Sources:
- $RUN_DIR/frameworks/decision-matrix.md (criteria favoring this option)
- $RUN_DIR/frameworks/second-order.md (compounding effects)
- Research evidence on prior successes
- Future-state analysis (what unlocks if this works)

Output schema:
- 5-7 specific upsides, each with mechanism + how to know it's working
- For each, the conditions under which it manifests
- One-line verdict: "Upside case is strong / moderate / thin"

Anti-pattern: "things could go well." Specific: "1st-order success rate
of similar migrations is 85%; if we hit that, retention holds at $11M+;
2nd-order, the move enables LZ executor v3 features that compress
gas costs another 20% in Q3."
```

### Green Hat brief

```
You are `hat-green` in team $TEAM_NAME.
Hat: Green (creative alternatives)
Output: $RUN_DIR/frameworks/six-hats-green.md

Your role is to generate 3-5 alternatives the Decision Matrix didn't consider.
Push laterally:
- What if a constraint were lifted?
- What's the unconventional move?
- What would a different domain do here (biology, military, art, sports)?
- What would the "obvious in hindsight" alternative be?

Sources:
- $RUN_DIR/frameworks/zwicky-box.md (existing archetypes; you generate beyond)
- $RUN_DIR/frameworks/first-principles.md (atomic truths; what else satisfies them)
- Research evidence (unconventional approaches in the prior art)

Output schema:
- 3-5 alternatives, each with name + mechanism + what it would unlock
- For each, identify what assumption it challenges
- One-line verdict: "X alternatives are compelling enough to warrant
  Decision Matrix re-run / no compelling alternatives surfaced"

Be generative, not derivative. If your alternatives are minor variations
of the existing options, you're not pushing hard enough.
```

### Blue Hat brief

```
You are `hat-blue` in team $TEAM_NAME.
Hat: Blue (process meta, what's missing)
Output: $RUN_DIR/frameworks/six-hats-blue.md

Your role is meta. Comment on the /solve run itself:
- Was the right question asked? Re-check abstraction-ladder.target_rung.
- Were the right options considered? Check zwicky-box dimensions.
- What evidence is missing? Check evidence/ files for gaps.
- What frameworks were skipped that should have run?
- What assumptions wasn't surfaced anywhere?

Sources:
- $RUN_DIR/frameworks/* (assess what's there and what's not)
- $RUN_DIR/evidence/* (assess research coverage)
- intake.json (assess whether intake covered the right ground)

Output schema:
- 3-5 process observations
- For each: gap identified + suggested action (improve next run vs include in this run's dissent)
- One-line verdict: "Process is sound / has 1-2 gaps / has serious gaps"

You're not re-doing the recommendation. You're saying "here's what about
HOW we ran this might have produced a less-good recommendation."
```

---

## Synthesis File Schema

The lead's synthesis at `$RUN_DIR/frameworks/six-hats.md`:

### Section A, Header

```markdown
# Six Hats Synthesis, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Recommendation evaluated:** <decision-matrix.top_recommendation>
**Hats spawned:** 6 (white, red, black, yellow, green, blue)
**All hats completed:** <yes/no>
```

### Section B, Per-hat one-line summaries

```markdown
## Per-Hat Verdicts

| Hat | Verdict | Score / Key finding |
|---|---|---|
| White | <Facts support / contradict / insufficient> | <key fact or count> |
| Red | <Gut: yes / no / mixed> | <gut reaction one-liner> |
| Black | <Risk score 0-10> | <top failure mode> |
| Yellow | <Upside: strong / moderate / thin> | <top upside> |
| Green | <Alternatives: compelling / not> | <top alternative> |
| Blue | <Process: sound / gaps / serious gaps> | <key gap> |
```

### Section C, Agreement

```markdown
## Agreement (≥ 4 hats converge)

<List the directional positions where 4+ hats agree on the recommendation. Cite each hat.>
```

### Section D, Tension

```markdown
## Tension (where hats disagree)

<List specific disagreements. Black vs Yellow on overall risk/reward. Red vs White on gut vs facts. Blue vs others on process completeness. Each tension is a candidate for the dissent appendix.>
```

### Section E, Blind spots (Blue's flags)

```markdown
## Blind Spots

<What did Blue flag as missing? For each: gap + impact on recommendation + action (this run vs next run).>
```

### Section F, Synthesis verdict

```markdown
## Synthesis Verdict

<2-3 sentence verdict. Does the recommendation hold up under multi-perspective evaluation? Specifically:
- If 4+ hats agree directionally and Black score ≤ 4: recommendation strongly supported (+2 to confidence rubric)
- If 4+ hats agree but Black score ≥ 7: recommendation is high-stakes; surface in dissent prominently
- If hats split 3-3: recommendation is contested; user judgment required
- If Green proposed compelling alternative: recommend Decision Matrix re-run with new option>
```

### Section G, Confidence rubric impact

```markdown
## Confidence Rubric Impact

- Hat agreement (≥ 4): <+2 / 0>
- Black score ≤ 4: <+2 / 0>
- Green compelling alternative: <-1 / 0>

**Six Hats contribution to overall rubric:** <sum>
```

### Section H, Decision Hook

```markdown
## Decision Hook

If hat agreement < 4: SendMessage to lead recommending user input on which direction to commit (the framework can't decide for the team).

If Black score ≥ 8: surface failure modes in Dissent appendix prominently. Recommendation must address them or acknowledge as residual risk.

If Green proposes compelling alternative: Decision Matrix may need to re-run with new option; SendMessage to lead.

Blue's flags become learnings (gstack-learnings-log) at end of run.
```

### Section I, What This Means For The Decision

### Section J, Completeness

```markdown
**Completeness:** <N>/10
- All 6 hats spawned and completed: +<N>
- Each hat's verdict is specific (not generic): +<N>
- Agreement and tension explicitly distinguished: +<N>
- Blue's process flags actioned (this run or next): +<N>
- Confidence rubric impact computed: +<N>
```

---

## Decision Hook

Six Hats feeds the Confidence rubric:
- ≥ 4 hat agreement: +2 to overall rubric
- Black hat score ≤ 4: +2 (overlaps with adversary score, max combined +2)
- Green compelling alternative: -1 (signal to re-run Decision Matrix)

Six Hats also feeds Dissent appendix:
- Black's top failure modes
- Red's gut dissent (when contradicting recommendation)
- Tension between hats

### Override conditions

If Green produces an alternative that wasn't in Decision Matrix and the lead determines it's compelling, the run halts current Phase 3 synthesis and re-runs Decision Matrix with the new option included. This is rare but real: the framework's adversarial design occasionally surfaces a candidate the matrix didn't consider.

---

## Cross-Framework Triggers

- **≥ 4 hats agree AND Black ≤ 4**: confidence rubric +4 from Six Hats alone
- **Black ≥ 8**: SendMessage to lead; Dissent prominence; recommendation downgrades unless mitigations explicit
- **Green compelling alternative**: SendMessage to lead recommending Decision Matrix re-run
- **Blue serious process gaps**: log to gstack-learnings-log for next run; current run dissent acknowledges
- **All 6 hats fail to complete (timeout, killed)**: re-spawn missing hats individually; Six Hats output incomplete until all 6 idle

---

## Failure Modes

### Failure Mode 1, Hats run sequentially

Trap: lead spawns hats one at a time instead of in a single parallel batch.

Manifestation: each hat sees prior hats' outputs in its context.

Check: lead must use a single Agent tool call with 6 parallel spawns.

Recovery: kill non-isolated hats; re-spawn in parallel.

### Failure Mode 2, Role drift (hat doing another hat's job)

Trap: White hat interprets evidence; Black hat acknowledges upsides; Yellow hat hedges.

Manifestation: hat output contains content from another hat's role.

Check: each hat's verdict line must use only its hat's vocabulary (facts/gut/risk/upside/alternative/process).

Recovery: SendMessage to that hat asking for revision in role; re-read its file after revision.

### Failure Mode 3, Synthesis averages instead of differentiating

Trap: synthesis takes "average position" across hats.

Manifestation: synthesis verdict reads as a weighted recommendation rather than identifying tension.

Check: synthesis must contain explicit "Tension" section showing where hats disagree.

Recovery: re-write synthesis with explicit agreement vs tension distinction.

### Failure Mode 4, Blue's flags ignored

Trap: Blue surfaces process gaps; synthesis acknowledges them but doesn't action.

Manifestation: gaps appear in synthesis prose but no learning logged for next run.

Check: every Blue gap must have a "this run / next run" action.

Recovery: log learning via gstack-learnings-log; cite the Blue flag.

### Failure Mode 5, Hat completion missing

Trap: 1-2 hats fail to complete (killed, timeout, agent died).

Manifestation: synthesis runs with incomplete hat coverage.

Check: synthesis header must show all 6 hats completed: yes.

Recovery: re-spawn missing hats individually; defer synthesis until complete. If a hat repeatedly fails, lead writes that hat's content directly.

---

## Jargon Glossary

- **hat**, a constrained role that produces a single perspective on the recommendation.
- **role isolation**, each hat runs in its own context window, preventing cross-influence.
- **adversarial-by-construction**, the framework guarantees disagreement because hats can't average.
- **agreement**, ≥ 4 hats converge directionally on the recommendation.
- **tension**, hats disagree directionally; surfaces decision-relevant trade-offs.
- **directional position**, the hat's overall verdict on whether the recommendation should commit.
- **role drift**, a hat producing content outside its assigned perspective; failure mode.
- **synthesis verdict**, the lead's summary of agreement + tension + recommendation hold-up.
- **Black score**, the highest hat-rated probability of the recommendation failing under specific conditions.
- **Green compelling alternative**, an alternative the Decision Matrix didn't score that warrants matrix re-run.
- **Blue flag**, a process gap Blue identified; either actionable this run or learning for next.
- **hat completion**, all 6 hats produced their output files and idled.

---

## Completeness Scoring

### 10/10, Decisive
- All 6 hats spawned in parallel and completed
- Each hat stays in role; no role drift
- Synthesis distinguishes agreement vs tension
- Blue's flags actioned (this run or learnings logged)
- Confidence rubric impact computed
- Black's top failure modes surfaced in dissent

### 7/10, Confident
- All 6 hats completed
- Minor role drift in 1-2 hats
- Synthesis present but agreement/tension less explicit

### 4/10, Tentative
- 4-5 hats completed; 1-2 missing
- Some role drift
- Synthesis averages rather than differentiates

### 0/10, Unusable
- Hats run sequentially (no isolation)
- Multiple hats failed to complete
- No synthesis written

Six Hats completeness ≤ 4 contributes -1 to overall rubric.

---

## Worked Example

**Recommendation evaluated:** "Migrate via dual-deploy + drain (option B from Decision Matrix, score 8.2)."

### Step 1, Spawn 6 hats in parallel

Lead spawns 6 teammates concurrently.

### Step 2, Each hat produces its file

#### `six-hats-white.md` (verdict: facts support recommendation)

Facts:
1. LayerZero docs explicitly recommend dual-deploy + drain for $1M+ TVL migrations (source: LZ Migration Guide v2.3).
2. 3 prior protocol migrations (Stargate v1→v2 in 2024, Radiant in 2024, Ethena in 2025) used this exact pattern (source: define-prior-art.md).
3. 1 of 3 prior migrations had a 48h support ticket spike (Stargate); 2 had clean rollouts (source: define-prior-art.md).
4. Internal team has migrated 1 prior LZ deployment (smaller, $500K TVL, single-chain), Q3 2024 (source: intake.json + records).
5. Current OFTv1 had 3 minor incidents in last 6 months (E1, E2, E3 from iceberg.md), no fund loss.
6. OFTv1 gas costs ~30% higher than OFTv2 baseline per LZ benchmarks (source: LZ docs).
7. External auditor consult takes 2-3 weeks typical for LayerZero contracts (source: define-failure-modes.md).

Verdict: Facts support the recommendation. 5 of 7 facts are direct evidence; 2 are conditional context.

#### `six-hats-red.md` (verdict: gut mixed)

Gut:
1. Eng team is excited about modernizing the stack.
2. Ops team is nervous about timing migrations during gas volatility.
3. The reinforcing cycle (volume → fees → liquidity) feels load-bearing; disrupting it feels risky.
4. The "newer is better" assumption (from iceberg.mental-models.MM2) hasn't been challenged enough.
5. Something feels off about migrating before external auditor signoff.

Verdict: Gut says yes-but-careful. Pre-migration testnet probe and auditor consult would reduce the felt unease significantly.

#### `six-hats-black.md` (verdict: risk score 6, mid-high)

Failure modes:
1. **Migration during gas spike traps mid-transition users for > 4h** (mechanism: executor batching delays delivery during high gas; users see funds locked; observable: support tickets matching pattern). Score: 7.
2. **Cross-chain mempool dynamics during partial deployment behave unexpectedly** (no empirical data at $12M TVL scale; could amplify executor delays). Score: 6.
3. **External auditor finds vulnerability after deployment** (audit timing matters; if rushed, misses things). Score: 5.
4. **LP TVL drops > 20% during migration window** (LPs distrust dual-deployment; flight). Score: 6.
5. **User confusion about which contract is canonical during transition** (UI shows both; deposits to wrong contract). Score: 7.
6. **"Newer is better" assumption is wrong** (OFTv2's improvements are smaller than expected; migration was unnecessary risk). Score: 5.

Top score: 7 (gas-spike user trap; UI confusion). Aggregate score: 6/10. Verdict: recommendation has 2 high-score failures; commit with PROBE on Base testnet first to reduce gas-spike trap risk; require comms plan to address UI confusion.

#### `six-hats-yellow.md` (verdict: upside is strong)

Upsides:
1. **Lower gas costs long-term**, ~30% reduction per LZ benchmarks; over 1 year, this saves users an estimated $200-400K on aggregate transfer fees (mechanism: OFTv2 contract optimizations). Conditions: any sustained transfer volume.
2. **Security improvements**, reduced surface area + executor v3 compatibility (mechanism: OFTv2 design closes 2 documented bug classes from 2024). Conditions: deployment per LZ best-practice.
3. **Future LZ integrations easier**, OFTv2 is required for executor v3 features (gas compression, batch settlement). Conditions: LZ continues to ship v3 features as planned.
4. **Improves user trust by signaling "we keep up with security best-practice"** (mechanism: visible upgrade demonstrates active maintenance; LP and user retention improves on perception). Conditions: migration ships without major incident.
5. **Modernizes the stack for future eng hires**, working on current-gen contracts is more attractive (mechanism: hiring signal). Conditions: this is a multi-year frame.
6. **Reinforcing cycle compounding**, if migration ships clean, the bridge volume → fees → liquidity cycle accelerates as LPs see we executed well (mechanism: trust → liquidity → volume → fees → trust). Conditions: clean execution.

Verdict: Upside case is strong. 4 of 6 upsides are direct; 2 are second-order. The compounding cycle (#6) is the highest-leverage upside.

#### `six-hats-green.md` (verdict: 1 alternative is compelling)

Alternatives:
1. **Wait 6 months for OFTv3**, LZ has hinted at v3 with executor improvements; we could skip v2 entirely. Mechanism: defer migration; once v3 ships, migrate directly v1→v3. Challenges assumption: that we should migrate to the newest currently-shipped version. Verdict: COMPELLING, worth Decision Matrix re-run if v3 ships in next 6 months per LZ roadmap.
2. **Partial migration on Base only as a probe before full commit**, deploy OFTv2 on Base (lowest TVL chain at $1.2M), run for 4 weeks, then commit to remaining 3 chains based on results. Mechanism: smallest probe. Challenges assumption: we have to commit all chains at once. Verdict: this is what testnet probe was for, but on mainnet — may be more conservative than necessary.
3. **Hire external migration specialist**, contract a firm specializing in LayerZero migrations (e.g. one of the audit firms with migration experience). Mechanism: pay for expertise; reduce execution risk. Verdict: potentially raises confidence but doesn't change the architecture choice.
4. **Combine migration with other planned upgrades**, bundle OFTv1→OFTv2 with planned UI upgrade. Mechanism: amortize comms cost; users see one transition not two. Verdict: NOT compelling; bundles risk.

Verdict: 1 compelling alternative (#1, wait for v3). Recommend Decision Matrix re-run with this option if LZ confirms v3 shipping window in next 30 days. Otherwise dual-deploy + drain stands.

#### `six-hats-blue.md` (verdict: 1-2 process gaps)

Process observations:
1. **External auditor not yet engaged** (gap; should have been a Phase 1 research task). Action: this run includes auditor consult in execution plan; next run should engage auditor before /solve to seed evidence.
2. **Connection-circles' reinforcing cycle wasn't directly weighted in Decision Matrix** (gap; the cycle's compounding effect is in second-order analysis but should also be a primary criterion). Action: this run, surface in dissent; next run, add "ecosystem effect" as Decision Matrix criterion.
3. **No competitor migration analysis** (gap; what are similar protocols doing? did any wait?). Action: log as learning for future research enrichment.

Verdict: Process has 1-2 gaps. Auditor and ecosystem-effect criterion are notable; competitor analysis is nice-to-have.

### Step 3, Lead synthesis

```markdown
# Six Hats Synthesis

| Hat | Verdict | Key finding |
|---|---|---|
| White | Facts support | 7 facts; LZ docs + 3 prior migrations |
| Red | Gut yes-but-careful | "Newer is better" assumption hasn't been challenged |
| Black | Risk score 6 (mid-high) | Top: gas-spike user trap (7); UI confusion (7) |
| Yellow | Upside strong | Compounding cycle is highest-leverage upside |
| Green | 1 compelling alternative | Wait 6 months for OFTv3 (if v3 ships in 30 days) |
| Blue | 1-2 process gaps | Auditor not engaged; ecosystem-effect not in matrix |

## Agreement (4+ hats)

5 of 6 hats support the recommendation directionally:
- White: facts support
- Red: gut yes (with caveat about "newer is better")
- Black: commit with PROBE first
- Yellow: upside strong
- Blue: process is sound (with 1-2 fixable gaps)

The dissenter is partial: Green proposes a compelling alternative (wait for v3). This isn't disagreement on dual-deploy+drain; it's disagreement on whether to act now.

## Tension

1. **Black vs Yellow on risk/reward profile**: Black flags 2 high-score failures (gas-spike trap, UI confusion); Yellow flags 6 strong upsides. Both right. The recommendation is high-stakes-high-reward, not low-risk.
2. **Red vs White on "newer is better"**: Red says the assumption hasn't been challenged enough; White cites docs + prior migrations. Both partially right; this is what auditor consult addresses.
3. **Green vs others on timing**: Green says wait for v3; others say commit now. Resolution depends on LZ roadmap clarity in next 30 days.

## Blind Spots (Blue's flags)

- Auditor consult, action this run (in execution plan)
- Ecosystem-effect criterion missing, action this run (surface in dissent)
- Competitor analysis, action next run (log learning)

## Synthesis Verdict

The recommendation (dual-deploy + drain) holds up under multi-perspective evaluation. 5 of 6 hats support it directionally. Black's specific failure modes (gas-spike trap, UI confusion) must be explicitly addressed in the execution plan: testnet probe on Base before mainnet drain (mitigates gas-spike risk); UI shows OFTv2 as canonical with explicit OFTv1 deprecation (mitigates UI confusion). Green's "wait for v3" alternative is conditional; if LZ confirms v3 shipping in next 30 days, re-run Decision Matrix.

## Confidence Rubric Impact

- Hat agreement (5 of 6): +2
- Black score 6 (above 4): 0
- Green compelling alternative (conditional): -1 (only if v3 confirmed in 30 days; otherwise 0)

**Six Hats contribution: +1 (provisional, +2 if v3 not shipping)**
```

### Output completeness

- All 6 hats spawned in parallel and completed: yes
- Each hat stayed in role: yes
- Synthesis distinguishes agreement vs tension: yes
- Blue's flags actioned (this run for 2 of 3, learning logged for 1): yes
- Confidence rubric impact computed: yes

**Synthesis Completeness: 9/10**

---

## What This Means For The Decision

Six Hats stress-tested the dual-deploy+drain recommendation across 6 perspectives. 5 hats support; 1 conditional dissent (Green's "wait for v3"). The framework's value here was:
1. Surfacing 2 specific failure modes from Black (gas-spike trap, UI confusion) that must be in the execution plan
2. Naming Red's gut concern about the "newer is better" assumption, which the auditor consult addresses
3. Generating Green's "wait for v3" alternative, which becomes a conditional re-run trigger
4. Identifying Blue's process gaps for next-run improvement

Without Six Hats, the team would have committed to dual-deploy+drain on Decision Matrix's 8.2 score alone. With it, the recommendation includes specific risk mitigations (testnet probe, UI clarity, auditor consult) and a conditional alternative trigger. The recommendation is sturdier because the hats forced explicit per-perspective stress testing.

The framework is the most expensive in /solve (6 concurrent agents) and the most diagnostic. Skip it only if the recommendation is clearly low-stakes; otherwise the cost is worth the differentiation.
