# Second-Order Thinking

**Phase:** Decide · **Source:** https://untools.co/second-order-thinking

Second-order thinking forces the team to keep asking "and then what?" past the point where most decisions stop. First-order effects are visible. Second-order effects are usually overlooked. Third-order effects are where most blowups live: the medicine that became poison, the optimization that broke a system, the win that triggered the loss. This framework's job is to surface the chain before it surfaces in production.

The framework runs after Decision Matrix has produced its top 2 options and before Six Hats and the recommendation. Its output feeds the confidence rubric (catastrophic downside at any order = -2) and the Black Hat (which uses second-order's worst-case branches as ammunition).

---

## Entry Predicate

```
always_run
```

Second-order thinking runs every time Phase 3 fires. It applies to every option that survives Decision Matrix's disqualifier check. There is no Cynefin domain that exempts it; the question "and then what?" is universally useful.

The depth of the chain varies by domain:

```
depth = 3 if cynefin.domain ∈ {simple, complicated}
depth = 4 if cynefin.domain = complex ∨ connection-circles found reinforcing cycle
depth = 4 if intake.reversibility = one-way-door
depth = 2 if cynefin.domain = chaotic ∧ intake.time_pressure = "now" (act first, audit later)
```

The default is 3. Push to 4 when the system has reinforcing cycles (amplification compounds through orders) or when reversibility is one-way (the chain matters more because you can't reverse the head). Drop to 2 only when time pressure makes deeper analysis impractical.

### Inputs

- `frameworks/decision-matrix.md::top_2` — the two options to trace effects on
- `frameworks/connection-circles.md::cycles` — reinforcing/balancing cycles that amplify or dampen effects
- `frameworks/cynefin.md::domain` — drives chain depth
- `intake.reversibility` — drives chain depth
- `frameworks/iceberg.md::structures` — system structures that propagate effects
- `evidence/decide-prior-art.md` — base rates for similar decisions and their downstream effects

### Outputs

- `$RUN_DIR/frameworks/second-order.md` — the chain table per option, with effects tagged likely/possible/speculative
- `state.json` `second_order.catastrophic_downside` (boolean) — read by confidence rubric, Black Hat
- `state.json` `second_order.amplifying_cycle_hit` (boolean) — read by Black Hat for emphasis

---

## Operating Principles

These five rules are non-negotiable.

**1. Trace effects by chain, not by category.**

Second-order is not "list every possible thing that could happen." It is "given this first-order effect, what specifically follows from it as the next causal step?" Each effect at order N must be a direct consequence of an effect at order N-1. Anti-pattern: the team brainstorms a long list of "things to consider" and labels them all second-order. Second-order is a chain: A causes B causes C. If C does not follow from B specifically, C is not second-order with respect to B; it is a separate first-order effect of A.

**2. Tag every effect with confidence.**

Every effect gets one of three tags:
- **likely**: high-confidence prediction, supported by prior art or system structure
- **possible**: plausible but not assured, depends on conditions we don't fully control
- **speculative**: long chain or unfamiliar territory, named for completeness, not for action

The confidence tag matters more than the effect itself. A speculative third-order effect that would be catastrophic still warrants attention. A likely third-order effect that is mild is the operating reality. Anti-pattern: presenting all effects as equally weighted, with no confidence distinction. The team treats speculative as a tail and ignores it; it should be flagged for monitoring.

**3. Mark amplifications when cycles fire.**

If `connection-circles` found a reinforcing cycle, second-order's job is to trace whether the chosen option steps into that cycle. If yes, name the cycle, name the amplification, name the doubling time. Reinforcing cycles compound: a "2x worse than expected" first-order effect becomes "8x worse" by third-order if the cycle reinforces. Anti-pattern: ignoring cycles, treating effects as additive when the system is multiplicative.

**4. Look for the medicine-poison flip.**

The most valuable second-order outputs are effects that flip sign. The first-order effect is positive ("we shipped, users saw the new feature"). The second-order effect is negative ("the new feature changed the activation funnel and onboarding metrics dropped"). The third-order effect is the actual harm ("growth team rolled back the feature, eng team morale dropped, original engineer quit"). The flip is the warning. Anti-pattern: only tracing chains that confirm the option is good. The framework requires tracing both upside and downside chains for each option.

**5. Tie chains to actions, not to vibes.**

Each chain should end with a specific implication for the recommendation: a thing to monitor, a thing to mitigate, a thing to abort on. "Could be bad" is not actionable. "If user activation drops > 10% within 2 weeks, we abort and roll back" is actionable. Anti-pattern: writing chains that read like a thinkpiece. The framework is doing risk modeling, not commentary.

---

## Response Posture

**Tone.** Forensic. The agent is following causal chains, not editorializing. Use neutral phrasing: "the first-order effect of B is X, which causes Y at second order, which under conditions Z amplifies via the reinforcing cycle to W at third order."

**Pacing.** Per option, per order, in sequence. Build the chain for option B order 1, then B order 2, then B order 3. Then C order 1, etc. Do not batch all options at order 1. Chain coherence beats parallelism.

**Push depth.** Maximum on the medicine-poison flip. If a first-order effect is uniformly positive, push hard at second-order: what could go wrong specifically because we got the first-order win? At third-order: under what conditions does the second-order downside become catastrophic? The framework should sound paranoid about success.

**Where to escalate.** SendMessage to lead when:
- A speculative third-order effect would be catastrophic and the team cannot rule it out (would require evidence the team does not have). Mark for additional research.
- The reinforcing cycle from connection-circles is hit by the top option AND amplifies a downside. The recommendation may need a circuit breaker.
- All three top options have a similar third-order downside (same systemic risk). The problem is not "which option" but "the system itself." Surface to lead.
- A first-order effect that the team treated as a feature is actually the trigger of a second-order downside. Naming this requires reframing the recommendation.

---

## Anti-Sycophancy Rules

The agent running Second-Order must never write these:

- "Most likely the effects will be manageable." Tag specific effects with specific confidence; do not wave at "manageable."
- "There may be some unintended consequences worth monitoring." Name the consequences. Name the monitoring threshold.
- "Long-term effects are difficult to predict." If they are speculative, tag them speculative. Do not skip them.
- "On balance the chain looks favorable." Quote the specific positive and negative effects.
- "Worth keeping in mind that..." If it is worth keeping in mind, it is worth being a tagged effect with a monitor.

The agent must always:

- State each effect as a sentence: "Because of X, Y happens" with a confidence tag.
- Quote the cycle amplification specifically when one fires: "The reinforcing cycle (bridge volume → LP fees → liquidity) doubles the effect every 3 weeks."
- Name the medicine-poison flip explicitly: "First-order positive (X), second-order negative (Y) under condition Z."
- Tie the worst speculative effect to a monitoring or abort threshold.

---

## Pushback Patterns

These are common chain-tracing errors. The agent applies them as self-pushback.

**Pattern 1: "First-order effects only" → push for "and then what?"**

- Internal evidence: chain stops at first-order with "users get the new feature."
- BAD: Accept the first-order effect as the analysis. Mark complete.
- GOOD: Force the next link. "Users get the new feature. And then what? Some users find it confusing. And then what? Support load increases. And then what? Support team backlogs, response time degrades. And then what? Customer satisfaction dips, churn risk increases." Stop only at the depth specified by Cynefin/reversibility.

**Pattern 2: "All possible effects" → tighten to chained effects**

- Internal evidence: the chain at order 2 lists 8 effects.
- BAD: Treat all 8 as second-order effects of order 1.
- GOOD: For each of the 8, ask: does this directly follow from the order-1 effect? If yes, keep. If no, it is a separate first-order effect, move it to order 1. Second-order is a tree, not a swamp; each branch must connect to its parent.

**Pattern 3: "Long-term unknowable" → tag speculative, do not skip**

- Internal evidence: third-order chain feels too uncertain to write.
- BAD: Stop the chain at second-order, note "third-order effects are difficult to predict."
- GOOD: Write the chain anyway, tag every node speculative. Speculative effects with catastrophic outcomes still drive recommendations (e.g. monitor for early signal, build circuit breaker). The chain's value is in surfacing speculative tails, not in confirming likely paths.

**Pattern 4: "Only tracing favorable chains" → trace both directions**

- Internal evidence: option B's chain is "X (good), Y (good), Z (good)."
- BAD: Conclude B is favorable.
- GOOD: For each likely first-order effect, trace BOTH a positive and a negative second-order chain. The medicine-poison flip lives at the intersection: a positive first-order that creates conditions for a negative second-order. If the team cannot articulate a plausible negative chain, they have not pushed hard enough.

**Pattern 5: "Catastrophic but speculative" → still actionable**

- Internal evidence: third-order chain ends with a catastrophic but speculative effect.
- BAD: Discard because "speculative means we don't know."
- GOOD: Speculative does not mean ignorable. Convert to actionable: what early signal would tell us we are heading down this branch? What is the monitor? What is the abort threshold? A speculative catastrophic third-order effect triggers a recommendation to add a monitoring or circuit-breaker step to the implementation plan.

---

## Method

Second-Order runs as a 6-step procedure. Each step builds on the previous.

### Step 1, Read inputs

Prerequisites: Decision Matrix complete, connection-circles complete, Cynefin classification written.

```bash
ls $RUN_DIR/frameworks/ | grep -E "(decision-matrix|connection-circles|cynefin|iceberg)"
```

Extract:
- Top 2 options from `decision-matrix.top_2`
- Cycles from `connection-circles.cycles` (reinforcing and balancing)
- Domain from `cynefin.domain`
- Reversibility from `intake.reversibility`

Determine chain depth via the predicate (default 3, push to 4 if reinforcing cycle or one-way-door).

Output: depth value, list of options, list of cycles to watch.

Failure mode if skipped: chain depth is wrong, amplifications are missed.

### Step 2, Identify first-order effects per option

Prerequisites: Step 1 complete.

For each option in the top 2 (and optionally top 3), list the immediate first-order effects:

- What changes the moment this option ships?
- What is the immediate user-facing change?
- What is the immediate system change?
- What is the immediate team change?

Cap first-order at 4-5 per option. More than 5 means the team is conflating first-order with second-order.

Tag each first-order effect: likely / possible / speculative. Most should be likely (first-order effects are usually the most predictable).

Output: first-order list per option with tags.

Failure mode if skipped: chain has no roots; second-order has nothing to follow from.

### Step 3, Trace second-order effects per first-order

Prerequisites: Step 2 complete.

For each first-order effect, ask "and then what?" once. Generate 1-3 second-order effects per first-order. Each second-order must follow as a direct consequence of its parent first-order.

Tag each second-order effect:
- likely if the consequence is well-supported by prior art or system structure
- possible if the consequence depends on conditions partially in our control
- speculative if the consequence depends on user behavior, market dynamics, or system interactions we don't fully observe

Mark medicine-poison flips: where a positive first-order has a negative second-order, or vice versa. These are flagged in the output.

Output: second-order chain per option, organized as tree branches from first-order parents.

Failure mode if skipped: first-order effects are presented as the full picture, missing where success creates new failure surface.

### Step 4, Trace third-order effects (or fourth if depth = 4)

Prerequisites: Step 3 complete.

For each second-order effect, ask "and then what?" again. Generate 1-2 third-order effects per second-order.

Most third-order effects will be tagged possible or speculative. That is correct. The chain is moving away from direct causation into systems territory.

If `connection-circles` found a reinforcing cycle that any first-order effect steps into, explicitly trace the amplification through second and third order:

```
First-order: bridge volume increases by 30% (likely)
Reinforcing cycle: bridge volume → LP fees → liquidity → bridge volume
Second-order via cycle: LP fees increase 30% × LP-share = ~15% (possible)
Third-order via cycle: liquidity increases ~15%, attracting more bridge volume (speculative, doubling time ~3 weeks)
```

Mark amplification chains explicitly. Note the cycle's doubling time from connection-circles output.

Output: third-order chain per option.

Failure mode if skipped: long-tail risks are invisible, recommendation is brittle to compounding effects.

### Step 5, Identify catastrophic downsides

Prerequisites: Steps 1-4 complete.

Walk every chain from each option. Tag any effect that meets the catastrophic criterion:

- Loss of user funds (eng/product domain)
- Permanent reputation damage
- Forced shutdown of the product
- Regulatory or legal action
- Runaway loss not bounded by a circuit breaker

Catastrophic effects can be at any order and any confidence tag. A speculative third-order catastrophic effect still triggers the catastrophic-downside flag.

For each catastrophic effect:
- What is the early signal that we are heading toward it?
- What is the monitoring threshold?
- What is the circuit-breaker action?

Output: catastrophic downside list per option, with monitoring/abort thresholds.

Failure mode if skipped: confidence rubric does not get the -2 it should, recommendation is over-confident.

### Step 6, Write output and update state

Prerequisites: Steps 1-5 complete.

Write the chain table per option following the Output Schema. Update state.json:

- `state.second_order.catastrophic_downside = true` if any catastrophic effect was identified on any top-2 option
- `state.second_order.amplifying_cycle_hit = true` if any first-order effect of either top-2 option steps into a reinforcing cycle from connection-circles
- `state.second_order.medicine_poison_flips` = count of positive-to-negative or negative-to-positive transitions in the chains

SendMessage to decider: "second-order complete, catastrophic_downside=<bool>, amplifying_cycle_hit=<bool>, ready for Six Hats."

Output: `$RUN_DIR/frameworks/second-order.md` and updated state.

Failure mode if skipped: confidence rubric and Black Hat lack the inputs they need.

---

## Probe Patterns

The agent asks itself these probes while building each chain.

### Probe 1, chain coherence

> "For each second-order effect, can I write 'because of <first-order parent>, this happens'? If the connection is loose, the effect is misclassified."

Failure shape: the second-order effect is actually a separate first-order effect, or it depends on factors not present in the first-order. Reattach to the correct parent or move to a different order.

### Probe 2, confidence calibration

> "What evidence supports this 'likely' tag? If I cannot cite a source or a system structure, the tag should be 'possible' or 'speculative.'"

Calibration discipline:
- likely: cited evidence (prior art, system structure, base rates)
- possible: plausible mechanism, no specific evidence
- speculative: chain is long, evidence is thin, listed for completeness

Over-tagging "likely" is the most common bias. The framework should treat any unsupported "likely" as a default downgrade to "possible."

### Probe 3, cycle amplification check

> "Does any first-order effect of this option step into a reinforcing cycle from connection-circles? If yes, am I tracing the amplification through second and third order?"

If yes and the chain does not show amplification: rewrite the chain with the cycle's effect inline.

If no but a balancing cycle exists: trace the dampening. A balancing cycle suppresses second-order effects after a delay (use connection-circles' delay value).

### Probe 4, medicine-poison flip surfaced

> "For each option, is there at least one chain where a positive first-order effect leads to a negative second-order or third-order effect? If not, am I only tracing favorable chains?"

If no flip surfaced: re-run Step 3 with explicit attention to "what could go wrong because we got the first-order win?" The flip is the most valuable output of this framework.

### Probe 5, actionable threshold

> "For each catastrophic downside, do I have an early signal, a monitoring threshold, and an abort action? If not, the catastrophic flag is observation, not actionable risk."

Convert observations to thresholds. "Could be bad" becomes "if metric M drops > 10% in 2 weeks, abort and roll back." If a threshold cannot be specified, the catastrophic effect needs more research before recommendation.

---

## Forcing Exemplars

When writing chains, use the forcing-version (specific, evidence-tagged, actionable).

### Exemplar 1, Stating a chain

SOFTENED (avoid):
> "Migrating to OFTv2 might lead to some user confusion, which could affect retention over time."

FORCING (aim for):
> "First-order: dual-deploy plus drain ships, both v1 and v2 are live for 2-week drain window (likely). Second-order: a portion of users (estimated 8-15% based on Stargate post-migration data) transact on v1 after v2 launches because their UI cache is stale (likely). Third-order: those users see their v1 balance drain to zero as the contract migrates them; if no clear UX warning, they panic-message support (possible). Mitigation: front-end v1 check + warning banner during drain window."

### Exemplar 2, Marking amplification via cycle

SOFTENED (avoid):
> "Increased bridge volume could lead to more liquidity over time."

FORCING (aim for):
> "First-order: OFTv2 ships, bridge volume increases ~30% due to lower gas costs (likely). Reinforcing cycle from connection-circles: bridge volume → LP fees → liquidity → bridge volume, doubling time ~3 weeks. Second-order via cycle: LP fees increase ~15% as bridge volume grows (possible, depends on LP-share); active LPs see higher returns. Third-order via cycle: more LPs join, liquidity deepens ~15%, attracting larger bridge users (speculative). Compounding implication: if cycle holds, total liquidity doubles in ~9 weeks. Failure mode if cycle breaks: gas spike on a major chain disrupts the loop, liquidity stagnates."

### Exemplar 3, Surfacing medicine-poison flip

SOFTENED (avoid):
> "While dual-deploy reduces risk, there are some considerations to keep in mind."

FORCING (aim for):
> "Medicine-poison flip on B (dual-deploy + drain): First-order positive (likely): no freeze window, users keep transacting throughout migration. Second-order negative (possible): the long drain window (2 weeks) extends our exposure to any v2 vulnerability; if a v2 bug is discovered mid-drain, we have to halt drain with funds split across versions. Third-order negative (speculative): a halted drain leaves the system in a hybrid state where some users are on v1 and some on v2; reverting requires either re-draining or ad-hoc support, eroding user trust. Mitigation: pre-drain audit pass on v2; abort threshold = any v2 incident in first 48h triggers drain pause."

### Exemplar 4, Tagging speculative catastrophic

SOFTENED (avoid):
> "There are unlikely but possible severe scenarios we should be aware of."

FORCING (aim for):
> "Catastrophic speculative third-order on B: dual-deploy + drain ships during a high-gas period (e.g. ETH gas > 200 gwei). First-order: drain transactions are expensive and slow (likely under that condition). Second-order: users on v1 cannot afford to wait for v2 transition, abandon migration (possible). Third-order: v1 retains > 30% of TVL beyond drain window, requiring extended support; team incurs 6+ months of dual-runtime cost (speculative but catastrophic for ops). Early signal: ETH gas > 100 gwei on day 1 of drain. Monitoring threshold: hourly gas tracker during drain window. Abort: if gas remains > 150 gwei for 4 consecutive hours, pause drain, communicate delay, restart when gas normalizes."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/second-order.md` follows this exact structure.

### Section A, Header

```markdown
# Second-Order Thinking, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs:** decision-matrix.top_2, connection-circles.cycles, cynefin.domain, intake.reversibility
**Chain depth:** <2 | 3 | 4>
**Depth justification:** <reason from predicate>
```

### Section B, Per-option chain table

For each top-2 option:

```markdown
## Option B (Dual-deploy + drain)

| Order | Effect | Tag | Parent | Notes |
|---|---|---|---|---|
| 1 | Both v1 and v2 live during 2-week drain window | likely | (root) | |
| 1 | Bridge volume increases ~30% post-launch | likely | (root) | OFTv2 gas savings 22% per tx |
| 1 | Drain transactions add ~$50K total cost | likely | (root) | LZ relayer fees |
| 2 | 8-15% of users transact on v1 after v2 launches | likely | 1.1 | UI cache, education delay; Stargate base rate |
| 2 | LP fees increase ~15% as bridge volume grows | possible | 1.2 | Reinforcing cycle: bridge volume → LP fees |
| 2 | Drain extends exposure to any v2 vulnerability | possible | 1.1 | 2-week window vs single-cutover |
| 3 | If v2 bug emerges mid-drain, halt leaves hybrid state | speculative | 2.3 | Recovery cost: 6+ months ops |
| 3 | Liquidity deepens ~15%, attracting larger users | speculative | 2.2 | Reinforcing cycle, doubling time ~3wks |
| 3 | Users on stale v1 panic-message support if drained | possible | 2.1 | Front-end warning mitigates |
```

Tag legend:
- likely: cited evidence supports (prior art, system structure, base rate)
- possible: plausible mechanism, conditions partially controlled
- speculative: long chain, evidence thin, listed for completeness

### Section C, Amplification via cycles

```markdown
## Cycle Amplifications

**Reinforcing cycle from connection-circles:** bridge volume → LP fees → liquidity → bridge volume

| Option | Hits cycle? | First-order entry | Doubling time | Compound at order 3 |
|---|---|---|---|---|
| B | yes | bridge volume +30% (1st) | 3 weeks | +90-100% liquidity if cycle holds 9 weeks |
| C | partially | bridge volume +5% (smaller, wrapping adds hop) | 6 weeks | +20-30% liquidity if cycle holds 12 weeks |

**Balancing cycle from connection-circles:** gas → migration eagerness → cross-chain trades → gas

| Option | Hits cycle? | Dampening | Notes |
|---|---|---|---|
| B | yes | drain self-throttles if gas spikes | Already builds in via configurable drain rate |
| C | no | wrapping doesn't compete for chain bandwidth in same way | |
```

### Section D, Medicine-poison flips

```markdown
## Medicine-Poison Flips

| Option | Order | Positive (1st) | Negative (later) | Mitigation |
|---|---|---|---|---|
| B | 1→2 | No freeze, users keep transacting | Long drain window extends v2 vulnerability exposure | Pre-drain audit; abort if v2 incident in first 48h |
| B | 1→3 | Lower gas attracts more users | Larger bridge volume amplifies any v2 bug impact | Phased drain by chain (Avalanche first, then others) |
| C | 1→2 | UX continuity, same address | Wrapping adds extra cross-chain hop, slower for users | Pre-launch latency benchmark on testnet |
| C | 1→3 | Simpler implementation | Wrapper depends on v1 staying live indefinitely (no path to retire v1) | Long-term: separate decision on v1 EOL |
```

### Section E, Catastrophic downsides

```markdown
## Catastrophic Downsides

| Option | Effect | Order | Tag | Early signal | Monitor | Abort threshold |
|---|---|---|---|---|---|---|
| B | High gas during drain stalls migration; users on v1 stranded | 3 | speculative | ETH gas > 100 gwei day 1 | Hourly gas tracker | > 150 gwei × 4h → pause drain |
| B | v2 vulnerability emerges mid-drain | 2 | possible | Any user-reported v2 issue | LZ events monitoring | 1 critical incident → halt drain, audit |
| C | Wrapper introduces unaudited cross-chain hop | 2 | possible | Failed wrap test on any chain | Pre-launch testnet | 1 wrap failure → block deploy |
| C | Wrapping locks v1 in production indefinitely (no retirement path) | 3 | possible | None within this decision | Architectural review at 6mo | n/a (long-term concern) |
```

### Section F, State updates

```markdown
## Triggers and State

- catastrophic_downside_present: true (B has speculative-catastrophic at 3rd order, C has possible-catastrophic at 2nd order)
- amplifying_cycle_hit: true (B steps into reinforcing cycle at 1st order)
- medicine_poison_flips: 4 total (B: 2, C: 2)
- confidence rubric impact: -2 (catastrophic downside present, even though speculative; the rubric reflects systemic risk)

State updates:
- `state.second_order.catastrophic_downside = true`
- `state.second_order.amplifying_cycle_hit = true`
- `state.second_order.medicine_poison_flips = 4`
- Black Hat receives this as ammunition: "B's catastrophic third-order is speculative-but-real; emphasize gas-spike scenario."
```

### Section G, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 paragraphs synthesizing what the chains imply for the recommendation. Specific, decision-actionable.>

Example synthesis:
"Both B and C surface catastrophic downsides at 2nd-3rd order, but the downsides are different in shape. B's catastrophic risk is gas-spike during drain (speculative but not impossible during mainnet network volatility). C's catastrophic risk is wrapper failure (possible if any chain has unique wrap quirks).

The reinforcing cycle amplifies B more than C because B has a larger first-order entry (30% bridge volume increase vs C's 5%). This is good for the system if the cycle holds (compounding liquidity is a moat) and bad if it breaks (any disruption amplifies through the same channel).

Recommendation: proceed with B but build the gas-spike circuit-breaker into the implementation plan as a non-negotiable. The catastrophic downside is mitigated by the abort threshold (>150 gwei × 4h pauses drain). Without the circuit-breaker, B should not ship; with it, B's chain is favorable."
```

### Section H, Completeness Score

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- Chain depth matches predicate (3 or 4): +<N>
- Each top-2 option has ≥ 3 first-order effects: +<N>
- Each first-order has ≥ 1 second-order child, with parent links explicit: +<N>
- Reinforcing/balancing cycles traced when present: +<N>
- Medicine-poison flips identified explicitly: +<N>
- Catastrophic downsides have early signal + monitor + abort: +<N>
- All effects tagged likely/possible/speculative with discipline: +<N>
```

---

## Decision Hook

Second-Order's output drives the rest of Phase 3 in three ways.

### Confidence rubric impact

| Condition | Impact |
|---|---|
| No catastrophic downsides at any order | +2 |
| Catastrophic downsides exist but mitigations are specific (early signal + monitor + abort) | 0 |
| Catastrophic downsides exist with no mitigation path | -2 |
| Reinforcing cycle amplifies the recommendation favorably with no offsetting risk | +1 (above any other modifier) |
| Reinforcing cycle amplifies a downside | already counted in catastrophic if applicable |

### Downstream framework feeding

- **Black Hat (Six Hats)**: receives the catastrophic downside list. Black Hat uses these as the structural attack vectors in its analysis. The strongest second-order critique becomes a Black Hat finding.
- **Yellow Hat (Six Hats)**: receives the favorable chains (amplifications via reinforcing cycles, compounding wins). The strongest second-order positive becomes a Yellow Hat finding.
- **Hard Choice**: if it fires, second-order's flips inform the values comparison. A medicine-poison flip on the dominant criterion is a strong values-stake signal.
- **Confidence-Speed-Quality**: receives `amplifying_cycle_hit`. If true, QUALITY mode is preferred over SPEED (the cycle amplifies whatever you ship, so ship it right).
- **Recommendation prose**: the Minto framework reads second-order's catastrophic downsides + mitigations and includes them in the "Risks" section of the final report.

### Override conditions

Second-order does not override Decision Matrix. It modifies confidence and adds risk language. The only way second-order shifts the recommendation is if the catastrophic-downside trigger is so severe that the team adds "do not ship without mitigation" as a condition. In that case, the recommendation becomes "ship B with mitigation, or ship C without it; pick by tolerance for mitigation overhead."

---

## Cross-Framework Triggers

Conditions in second-order's output force changes elsewhere in /solve.

### Triggers fired by catastrophic_downside

- `catastrophic_downside = true`: confidence rubric -2, mark in Dissent. Black Hat focuses here.
- `catastrophic_downside = true` AND no mitigation specified: the recommendation becomes "do not ship until mitigation is designed." SendMessage to lead.
- `catastrophic_downside = true` AND `intake.reversibility = one-way-door`: trigger Hard Choice (catastrophic + irreversible = hard choice by definition).

### Triggers fired by amplifying_cycle_hit

- `amplifying_cycle_hit = true` AND amplification favors recommendation: confidence rubric +1, add to Yellow Hat ammunition.
- `amplifying_cycle_hit = true` AND amplification harms recommendation: confidence rubric -1, add to Black Hat. May trigger Hard Choice if the harm is catastrophic.
- `amplifying_cycle_hit = true` AND `intake.time_pressure = "now"`: warn that compounding effects accelerate any wrong call. Recommend OODA cycle ≤ doubling time / 2.

### Triggers fired by medicine-poison flip count

- `medicine_poison_flips ≥ 4`: the chain is highly non-monotonic. The decision benefits from explicit risk-management plan in Minto output.
- `medicine_poison_flips = 0` across all top options: suspicious. Either the chains are too short or only favorable paths were traced. Rerun Step 3 with explicit attention to flips.

---

## Failure Modes

Five ways second-order fails. The framework checks for each before completing.

### Failure Mode 1, chain shallowness

Trap: chains stop at second-order even though depth = 3 or 4. The team feels the chain "is getting too speculative" and stops.

Manifestation: third-order column in the output is empty for some options, especially the team's preferred option.

Check: every option must have ≥ 1 third-order effect (at depth 3) per first-order. Speculative tag is acceptable; missing entry is not.

Recovery: fill in third-order, tag speculative if uncertain. Speculative tags surface tail risks; missing entries hide them.

### Failure Mode 2, only-favorable bias

Trap: chains for the team's preferred option only trace positive consequences. Chains for less-preferred options have negative second/third-order effects highlighted.

Manifestation: medicine-poison flips are missing on the leading option but present on other options.

Check: each option must have at least one medicine-poison flip explicitly traced. If the team genuinely cannot find a flip on the leading option, push harder on Probe 4. If still nothing, note in output as "no flip identified despite explicit search" (rare but possible for genuinely robust options).

Recovery: rerun Step 3 with explicit prompt to trace negative chains from positive first-order effects on the preferred option.

### Failure Mode 3, cycle amplification ignored

Trap: connection-circles found a reinforcing cycle, but second-order's chain does not show amplification through orders.

Manifestation: chain treats effects as additive (linear) when system is multiplicative (compounding).

Check: scan first-order effects for any that match the cycle's entry point. If yes, the chain at second/third order should explicitly reference the cycle and quote the doubling time.

Recovery: rewrite the chain inline with cycle amplification. Update output to include the doubling time and the third-order compound number.

### Failure Mode 4, catastrophic-but-unactionable

Trap: a catastrophic downside is identified but no early signal, monitor, or abort threshold is specified. The team feels the risk is named so they have done due diligence.

Manifestation: catastrophic table has effects with empty cells in early-signal / monitor / abort columns.

Check: every catastrophic effect must have all three: early signal, monitor, abort threshold. If any are empty, the catastrophic flag is observation, not actionable risk.

Recovery: research what the early signal would be, propose a monitor (existing dashboard, new alert, manual check cadence), specify the threshold. If the team cannot specify any of these, the catastrophic effect requires more research before recommendation.

### Failure Mode 5, tag inflation

Trap: the team tags everything "likely" because they are confident. The output looks like a strong forecast but actually it is unfounded confidence.

Manifestation: > 70% of effects tagged likely, including third-order effects (which should mostly be possible or speculative).

Check: count tag distribution. Healthy distribution at depth 3:
- 1st-order: 70-90% likely, 10-30% possible
- 2nd-order: 30-50% likely, 40-50% possible, 10-20% speculative
- 3rd-order: 10-20% likely, 30-40% possible, 40-60% speculative

Recovery: rerun Step 3-4 with stricter calibration. Default unsupported "likely" to "possible." Default unsupported "possible" at third order to "speculative."

---

## Jargon Glossary

- first-order effect, the immediate consequence of an action; usually visible and predictable
- second-order effect, the consequence of the first-order effect; usually overlooked
- third-order effect, the consequence of the second-order effect; usually where compounding shows up
- chain depth, how many "and then what?" iterations the framework performs (default 3, push to 4 for cycles or one-way-door)
- medicine-poison flip, a chain where the sign of the effect flips between orders (positive then negative, or vice versa)
- reinforcing cycle, a feedback loop that amplifies through orders (output of connection-circles); doubles or triples second/third-order effects
- balancing cycle, a feedback loop that dampens through orders; suppresses second/third-order effects after a delay
- amplification, the multiplicative growth of an effect through a reinforcing cycle
- doubling time, how fast a reinforcing cycle compounds (from connection-circles); used to compute order-3 magnitude
- catastrophic downside, an effect at any order severe enough to warrant abort threshold (fund loss, shutdown, regulatory action, runaway loss)
- early signal, an observable metric that indicates we are heading toward a catastrophic downside
- monitor, the mechanism (dashboard, alert, manual check) that watches the early signal
- abort threshold, the value of the early signal that triggers a circuit-breaker action
- speculative tag, the lowest confidence tag; chain is long, evidence is thin, listed for completeness
- additive vs multiplicative, additive systems sum effects, multiplicative systems compound them through cycles
- chain coherence, every effect at order N is a direct consequence of an effect at order N-1

---

## Completeness Scoring

### 10/10, Decisive

- Chain depth matches predicate exactly (3 or 4 per Cynefin/reversibility)
- Each top-2 option has 3-5 first-order effects
- Each first-order has 1-3 second-order children with explicit parent links
- Each second-order has 1-2 third-order children (at depth 3)
- All cycles from connection-circles traced through orders with doubling time noted
- All medicine-poison flips explicitly listed per option
- All catastrophic downsides have early signal + monitor + abort threshold
- Tag distribution is calibrated (most 3rd-order is possible/speculative, not likely)
- State updates written

### 7/10, Confident

- Depth matches but one option has thin third-order
- Some chains missing parent links
- Cycles named but amplification not traced through all orders
- 1-2 medicine-poison flips identified (target ≥ 1 per option)
- Catastrophic downsides identified, mitigations partial
- Tag calibration loose (some unsupported "likely" tags)

### 4/10, Tentative

- Chain stops at second-order regardless of depth setting
- Cycles ignored or only mentioned in passing
- Medicine-poison flips missing
- Catastrophic downsides named without monitoring/abort
- Tags mostly "likely" without calibration

### 0/10, Unusable

- Chain has only first-order effects
- No cycle awareness
- No flips identified
- Catastrophic downsides not assessed
- No tagging

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This continues from Decision Matrix. Top 2: B (dual-deploy + drain, score 355) and C (wrapped legacy, score 303). Cynefin = complicated. Reversibility = costly. Connection-circles found 1 reinforcing cycle (bridge volume → LP fees → liquidity) with ~3-week doubling time, plus 1 balancing cycle (gas → migration eagerness → cross-chain trades → gas) with ~2-day delay.

Chain depth predicate evaluation:
- cynefin = complicated → default depth 3
- connection-circles has reinforcing cycle → push to depth 4
- intake.reversibility = costly (not one-way-door)
- Result: depth = 4 (because of reinforcing cycle)

### Step 1: Read inputs

Top 2 options: B, C
Cycles: reinforcing (bridge volume → LP fees → liquidity), balancing (gas → migration eagerness)
Domain: complicated
Reversibility: costly
Depth: 4

### Step 2: First-order effects per option

**Option B (Dual-deploy + drain):**

| First-order effect | Tag | Source |
|---|---|---|
| Both v1 and v2 live during 2-week drain window | likely | Migration mechanism |
| Bridge volume increases ~30% post-launch | likely | OFTv2 22% gas savings (evidence/decide-base-rates.md), Stargate base rate |
| Drain transactions add ~$50K total cost | likely | LZ relayer fees × ~5K v1 holders |
| User communications spike during week 1 (FAQ, support load) | likely | Stargate post-migration: 2-3x support tickets for 1 week |
| LP rebalancing as users migrate (some pull liquidity) | possible | Depends on LP behavior; mixed prior art |

**Option C (Wrapped legacy):**

| First-order effect | Tag | Source |
|---|---|---|
| New wrapper contract live; users opt-in to wrap | likely | Wrapper mechanism |
| Bridge volume increases ~5% (small, wrapping adds hop) | likely | Wrapping latency penalty offsets some demand |
| Wrap/unwrap fees add new gas line item | likely | Wrapper architecture |
| v1 stays live indefinitely; no retirement path | likely | By design |
| Auditor cost lower (~$30K vs B's ~$80K) | likely | Wrapping is simpler scope |

### Step 3: Second-order effects per first-order

**Option B, second-order:**

| 2nd-order effect | Tag | Parent | Notes |
|---|---|---|---|
| 8-15% of users transact on v1 after v2 launches | likely | "Both live during drain" | Stargate base rate; UI cache, education delay |
| LP fees increase ~15% as bridge volume grows | possible | "Volume +30%" | Reinforcing cycle entry; depends on LP-share rate |
| Drain extends exposure window for any v2 vulnerability | possible | "Both live during drain" | 2-week window vs single-cutover |
| Support team backlog accumulates as ticket volume rises | likely | "Communications spike" | 2-3x normal volume for 1 week |
| LPs pull liquidity opportunistically during transition | possible | "LP rebalancing" | Could exacerbate slippage |

**Option C, second-order:**

| 2nd-order effect | Tag | Parent | Notes |
|---|---|---|---|
| Wrapping adds extra cross-chain hop, slower for users | likely | "Wrap/unwrap fees" | iceberg.structures: amplifies mempool delays |
| Some users skip wrapping entirely, stay on v1 | likely | "Users opt-in" | Voluntary migration is slow |
| Wrapper bug class introduces new audit surface | possible | "Wrapper live" | Wrapping is well-understood pattern but not zero-risk |
| Long-term technical debt: dual-runtime indefinite | likely | "v1 stays live indefinitely" | 6+ months engineering effort to retire |
| Lower bridge volume bound limits cycle entry | possible | "Volume +5%" | Reinforcing cycle barely engages |

### Step 4: Third and fourth-order effects (depth = 4)

**Option B, third-order via reinforcing cycle:**

The reinforcing cycle (bridge volume → LP fees → liquidity → bridge volume) has doubling time ~3 weeks.

| 3rd-order effect | Tag | Parent | Cycle role |
|---|---|---|---|
| Liquidity deepens ~15-20% over 6 weeks as cycle compounds | speculative | LP fees +15% | Cycle midpoint |
| 8-15% lingering v1 users see balance drained (panic if no UI warning) | possible | Users on v1 after v2 launch | Front-end warning mitigates |
| If v2 bug emerges mid-drain, hybrid state requires complex recovery | speculative | Drain extends exposure | 6+ months ops overhead |
| Support team reaches breaking point if 3rd-week ticket volume not normalized | possible | Backlog accumulates | Possible team morale impact |

**Option B, fourth-order:**

| 4th-order effect | Tag | Parent | Notes |
|---|---|---|---|
| Compounding liquidity attracts larger bridge users; long-term moat | speculative | Liquidity deepens 15-20% | Cycle holds 9+ weeks |
| Recovery from hybrid state (if it occurs) erodes user trust | speculative | Hybrid state recovery | Trust impact lingers 6+ months |
| Burned-out support team triggers headcount discussion | speculative | Support breaking point | Hiring cycle is 2-3 months |

**Option C, third-order:**

| 3rd-order effect | Tag | Parent | Notes |
|---|---|---|---|
| User trust compounds over time as wrapping proves reliable (no fund loss) | possible | Lower volume, slower migration | Trust as a slow-build asset |
| v1 retirement deferred indefinitely; cost of dual-runtime grows monthly | likely | Long-term debt | $5-10K/month dual ops |
| Cycle barely engages, no compounding moat from migration | possible | Volume +5% bound | Misses out on B's amplification |
| Wrapper bug class, if discovered, requires audited patch | possible | New audit surface | Wrapping is safer pattern but not zero |

**Option C, fourth-order:**

| 4th-order effect | Tag | Parent | Notes |
|---|---|---|---|
| Long-term: separate decision required to retire v1 (deferred problem) | likely | v1 retirement deferred | 6-12mo from now |
| Competitive disadvantage if peer protocols migrate fully and benefit from compounding | speculative | Cycle barely engages | Peer protocols' choice unknown |
| Legacy wrapper itself becomes deprecated when LZ releases OFTv3 | speculative | Long-term debt | 12-24mo speculation |

### Step 5: Catastrophic downsides

**Option B catastrophic candidates:**

1. **High gas during drain stalls migration:**
   - Order: 3 (speculative)
   - Trigger: ETH gas > 100 gwei during drain window day 1
   - Path: drain transactions become expensive → users on v1 cannot afford to wait → abandon migration → v1 retains > 30% TVL beyond drain window → 6+ months of dual-runtime ops cost
   - Early signal: gas > 100 gwei at drain start
   - Monitor: hourly gas tracker (existing tooling)
   - Abort: gas > 150 gwei × 4 consecutive hours → pause drain, communicate, restart when normalized

2. **v2 vulnerability emerges mid-drain:**
   - Order: 2 (possible)
   - Trigger: any v2 critical incident during drain window
   - Path: bug → halt drain → hybrid state → recovery cost
   - Early signal: any LZ event reporting unexpected behavior on v2
   - Monitor: LZ event monitoring + community Discord/Telegram
   - Abort: 1 critical incident → halt drain, audit, communicate

**Option C catastrophic candidates:**

1. **Wrapper introduces unaudited cross-chain edge case:**
   - Order: 2 (possible)
   - Trigger: chain-specific wrap behavior that doesn't match testnet
   - Path: wrap fails on a chain → user funds stuck mid-wrap → support escalation
   - Early signal: any wrap failure on testnet
   - Monitor: pre-launch testnet on all 4 chains
   - Abort: 1 wrap failure on any chain → block deploy until fixed

2. **v1 retirement permanently deferred (architectural lock-in):**
   - Order: 3 (possible)
   - Trigger: 12 months elapse, no migration to retire v1
   - Path: dual-runtime cost grows → eventually exceeds full migration cost → team forced to do this decision again with worse position
   - Early signal: 6-month wrapping uptake < 30%
   - Monitor: wrap rate dashboard
   - Abort: at 12 months, mandatory architectural review for v1 retirement

### Step 6: State updates

```json
{
  "second_order": {
    "catastrophic_downside": true,
    "amplifying_cycle_hit": true,
    "medicine_poison_flips": 4,
    "depth": 4,
    "options_analyzed": ["B", "C"]
  }
}
```

Confidence rubric impact:
- catastrophic_downside present (B has speculative, C has possible) → -2 base
- amplifying_cycle_hit favors B's recommendation if cycle holds → +1
- Net: -1 from second-order

Black Hat ammunition: gas-spike scenario for B, wrapper edge case for C, long-term lock-in for C.
Yellow Hat ammunition: B's compounding liquidity moat from reinforcing cycle.

### Output written

```markdown
# Second-Order Thinking, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T18:10:00Z
**Inputs:** decision-matrix.top_2 (B, C), connection-circles.cycles (1 reinforcing, 1 balancing), cynefin.domain=complicated, intake.reversibility=costly
**Chain depth:** 4
**Depth justification:** reinforcing cycle (bridge volume → LP fees → liquidity) detected by connection-circles forces depth 4 over default 3

## Option B (Dual-deploy + drain)

[chain table as above with all 4 orders]

## Option C (Wrapped legacy)

[chain table as above with all 4 orders]

## Cycle Amplifications

[cycle table as in Output Schema]

## Medicine-Poison Flips

[flip table; 4 total flips, 2 per option]

## Catastrophic Downsides

[catastrophic table with monitor/abort thresholds]

## Triggers and State

- catastrophic_downside_present: true
- amplifying_cycle_hit: true (B steps into reinforcing cycle, doubling time 3 weeks)
- medicine_poison_flips: 4
- confidence rubric impact: -1 net

## What This Means For The Decision

Both B and C surface catastrophic downsides at 2nd-3rd order, but the shapes differ. B's catastrophic risk is gas-spike during drain (speculative but mainnet-volatility-real); C's is wrapper edge case (possible during testnet validation).

The reinforcing cycle amplifies B's recommendation favorably. Bridge volume +30% (1st-order) compounds via LP fees and liquidity, doubling in ~3 weeks. By order 4, B's compounding produces a structural liquidity moat. C's smaller first-order entry (volume +5%) means the cycle barely engages; C wins on simplicity but misses the moat.

Recommendation: proceed with B but build the gas-spike circuit-breaker and v2 incident abort threshold into the implementation plan as non-negotiables. Without these, B's catastrophic downside is unmitigated. With them, B's chain is favorable.

## Completeness: 9/10
- Chain depth matches predicate (4): +2
- Each option has 4-5 first-order effects: +2
- Parent links explicit on all 2nd/3rd/4th-order effects: +2
- Reinforcing cycle traced through orders with doubling time: +1
- Medicine-poison flips identified per option: +1
- Catastrophic downsides have monitor/abort: +1
- Tag distribution calibrated: 1st mostly likely, 4th mostly speculative
```

### What the next framework (Ladder of Inference) inherits

Ladder of Inference receives:
- Top recommendation: B (dual-deploy + drain)
- Second-order's catastrophic downsides (gas-spike, v2 mid-drain bug) become potential targets for "what assumption are we relying on?"
- Medicine-poison flips become candidates for "what data are we ignoring?"
- The team's "newer is better" mental model from iceberg.mental_models is the leading suspect for unjustified leap

Ladder will trace the team's reasoning back through 7 rungs and surface the leap that, if false, breaks the recommendation.

---

## What This Means For The Decision

Second-order thinking is rarely decisive on its own; it modifies confidence and surfaces risks. When run well, it produces three artifacts: the chain table (showing the team has thought past the first move), the catastrophic downside list (turning vague worry into actionable monitor/abort), and the cycle amplification analysis (quantifying compounding effects).

The framework's most valuable output is the medicine-poison flip. First-order effects rarely surprise; second/third-order flips are where decisions are won or lost. Teams that only trace favorable chains ship recommendations that work in the demo path and break in production. Teams that explicitly trace flips surface the abort thresholds that turn risk into manageable engineering work.

The cost of skipping second-order: confidence rubric +2 by default (no catastrophic downside surfaced), recommendation feels strong but is brittle to long-tail risks. The cost of running it badly (only-favorable bias, tag inflation): false confidence dressed as analysis. The benefit of running it right: a recommendation the team can defend in adversarial review, with explicit risks named and explicit thresholds set.

When a reinforcing cycle amplifies the recommendation, second-order should celebrate it openly (this is the source of compounding wins). When it amplifies a downside, second-order should specify the circuit-breaker. When the chain reveals a medicine-poison flip on the dominant criterion, second-order's job is to escalate to Hard Choice.
