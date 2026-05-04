# OODA Loop (Boyd)

**Phase:** Decide · **Source:** https://untools.co/ooda-loop

OODA frames a decision as a cycle, not a one-shot. Observe what's happening. Orient how that updates your model. Decide the next branch. Act. Then observe again. Faster loops dominate slower loops at equal quality. In complex domains, OODA is the primary decision mode; Decision Matrix is advisory.

The framework's value isn't picking an option. It's picking a **cadence** at which you can re-decide. Slow loops on fast-moving problems lose. Fast loops on slow-moving problems waste capacity. Calibrate the cycle time to the problem.

---

## Entry Predicate

```
always_run if (intake.time_pressure = "now") ∨ (cynefin.domain ∈ {complex, chaotic})
recommended otherwise (run as secondary mode for complicated/simple domains)
```

OODA is **primary** for complex/chaotic domains and for any "now" time-pressure run. It's **secondary** for complicated/simple where Decision Matrix dominates and OODA acts as the execution-cadence framework.

### Inputs

- `intake.time_pressure`
- `frameworks/cynefin.md::domain` (drives whether OODA is primary or secondary)
- `frameworks/decision-matrix.md::top_recommendation` (the option to loop on)
- `frameworks/connection-circles.md::cycles` (cycle delays inform realistic loop timing)

### Outputs

- `$RUN_DIR/frameworks/ooda-loop.md` — 4-stage table + cycle-time estimate + decision branches per cycle

---

## Operating Principles

**1. Cycle time is the operating constraint.**

If your OODA cycle is 2 weeks and the problem moves on a 1-week cadence, you're permanently behind. The cycle-time estimate is the most important number in the framework output. Anti-pattern: writing the 4 stages without estimating how long one full cycle takes.

**2. Each Decide branch must be discrete.**

"Continue / pivot / abort" must mean specific actions, not vague directions. Continue = exact same path; pivot = named alternative; abort = explicit stop conditions. Anti-pattern: "we'll see how it goes" branches that don't commit to behavior.

**3. Observe is about signals, not data dumps.**

What specifically would tell us the chosen path is working? Not "all the metrics" but 2-3 leading indicators. Anti-pattern: a dashboard with 20 charts that never produces a Decide trigger.

**4. Orient is where the team's mental model gets updated.**

If signals contradict expectations, Orient is where you grapple with that. The framework requires explicit mental-model statements: "we expect X; if we see Y, our model was wrong about Z." Anti-pattern: skipping Orient and going straight from observed signal to a re-Decide.

**5. The loop never ends until the recommendation is shipped or aborted.**

OODA isn't run once. The framework output describes the cycle that will run for the duration of execution. Anti-pattern: treating the framework as a one-time analysis rather than a recurring cadence.

---

## Response Posture

**Tone.** Operational. The framework is about execution rhythm, not analysis. Each stage gets a specific action, not a meditation.

**Pacing.** Single design pass that produces the cycle template. The cycle then runs in the real world during execution; this framework's output is the template, not the runtime.

**Push depth.** Zero direct user questions during the framework run. The cycle parameters (signals to observe, branches to decide between) are derivable from prior framework outputs + intake.

**Where to escalate.** SendMessage to lead when:
- Cycle time exceeds `intake.time_pressure` deadline / 3 (loop is too slow; flag in dissent)
- Observe signals overlap heavily (the framework can't differentiate from noise; signals need refinement)
- Decide branches collapse to a single option (no actual decision being made; framework is decoration)

---

## Anti-Sycophancy Rules

Never write:
- "We'll iterate as we learn..." (specify the iteration cadence and branches)
- "We'll keep an eye on things..." (name the signals)
- "Pivot if needed..." (name the pivot conditions and the pivot target)
- "Adapt as the situation evolves..." (specify the adaptation triggers)

Always:
- State the cycle time in concrete units (days, weeks).
- For each Observe signal, state the threshold that triggers a Decide.
- For each Decide branch, state the action (continue / pivot to X / abort).

---

## Pushback Patterns

**Pattern 1: "We'll watch the metrics" then name the metrics**

- Internal evidence: Observe stage written as "monitor performance."
- BAD: Accept this.
- GOOD: Specify. "Observe: (1) cross-chain transfer success rate (target ≥ 99%, alert at < 95%), (2) support ticket volume (target ≤ baseline + 20%, alert at + 50%), (3) LP TVL change (target ≥ 90% of baseline, alert at < 80%)."

**Pattern 2: "Pivot if it's not working" then name the pivot**

- Internal evidence: Decide branch is "pivot if needed."
- BAD: Accept.
- GOOD: Specify. "Decide branches: (continue) proceed to next migration phase if all 3 signals green; (pivot to dual-track) hold OFTv1 active longer than planned if signal 1 < 99%; (abort) halt migration and rollback if signal 1 < 95% AND signal 2 > +50%."

**Pattern 3: "Cycle time is roughly..." then commit**

- Internal evidence: cycle time written as "roughly weekly."
- BAD: Accept.
- GOOD: Commit to a specific day and ritual. "Cycle time: 7 days, Tuesday review at 10am, signals reviewed in standing meeting, Decide branch chosen by end of day Wednesday."

**Pattern 4: "Orient is implicit" then make it explicit**

- Internal evidence: Orient stage is empty or just says "interpret the data."
- BAD: Accept.
- GOOD: Force explicit mental-model statements. "Expected model: dual-deploy migration causes a 2-day support spike then normalizes. Surprise indicator: spike persists > 3 days, suggesting comms failure rather than UX friction. Surprise model update: re-evaluate user-facing materials, not contract behavior."

**Pattern 5: "OODA is just iteration" then differentiate**

- Internal pull: treat OODA as a generic "iterate" framework.
- BAD: 4 stages of vague "do, see, learn, repeat."
- GOOD: OODA's value is specifically Orient. Without explicit model-update logic, you have a poll loop, not OODA. Make Orient load-bearing.

---

## Method

5-step procedure to design the cycle template.

### Step 1, Estimate the natural problem cadence

How fast does the problem state change?
- Hourly (incident response): cycle time 1-4 hours
- Daily (active deployment, product launch): cycle time 1-2 days
- Weekly (multi-week project, strategic shift): cycle time 5-7 days
- Monthly (org change, market shift): cycle time 2-4 weeks

Read `intake.time_pressure` and `connection-circles.cycles` for delays. The OODA cycle should be ≤ deadline / 3 and ≤ shortest connection-cycle delay / 2.

### Step 2, Specify Observe signals

Pick 2-4 leading indicators (not lagging metrics). Each signal needs:
- Definition (what's being measured)
- Target (the expected value)
- Alert threshold (what triggers a Decide branch)
- Source (where the data comes from, who collects it)

### Step 3, Specify Orient mental model

Write the expected model in one paragraph:
- "We expect [signal trajectory] because [reason from cynefin or research]"
- "If [unexpected pattern], the model was wrong about [specific assumption]"
- "Surprise indicator: [specific deviation that triggers model update]"

### Step 4, Specify Decide branches

For each Decide branch, write:
- Trigger (which signal pattern fires this branch)
- Action (continue / pivot to X / abort)
- Owner (who commits the action)
- Communication (who needs to know)

### Step 5, Specify Act first step

For each Decide branch, the first concrete Act:
- Within hours of the Decide trigger
- Specific (commit to deploy contract X / send comms Y / halt drain mechanism Z)
- Reversible if possible

---

## Probe Patterns

### Probe 1, Cycle time vs deadline

> "What's `intake.time_pressure` deadline / 3? Is my cycle time ≤ that? If not, the loop is too slow."

### Probe 2, Signal independence

> "Are my Observe signals correlated? If signals 1 and 2 always move together, they're one signal. Find an independent third."

### Probe 3, Mental model articulation

> "Can I write the Orient mental model in one sentence? If not, it's vague; refine."

### Probe 4, Branch differentiation

> "Are my Decide branches actually different actions, or rephrasings of 'continue'? If they collapse to one, I'm not making a decision."

### Probe 5, Connection-cycle delay check

> "What's the shortest delay in connection-circles.cycles? Is my OODA cycle < that delay / 2? If not, the loop won't catch the cycle's effect in time."

---

## Forcing Exemplars

### Exemplar 1, Stating cycle time

SOFTENED:
> "We'll review progress regularly."

FORCING:
> "Cycle time: 7 days. Tuesday 10am standing meeting reviews signals from prior week. Decide branch chosen by end of day Wednesday. Act commits by end of week. Total cycle: Tuesday → Tuesday."

### Exemplar 2, Stating signals

SOFTENED:
> "We'll monitor cross-chain transfer health."

FORCING:
> "Observe signals (3):
> 1. Cross-chain transfer success rate; target ≥ 99% over rolling 24h; alert at < 95%; source: contract event logs aggregated daily.
> 2. Support ticket volume; target ≤ 50/day baseline; alert at > 75/day; source: support tool dashboard.
> 3. LP TVL on bridge pools; target ≥ 90% of pre-migration baseline; alert at < 80%; source: on-chain TVL aggregator."

### Exemplar 3, Stating Decide branches

SOFTENED:
> "We'll continue if things look good and pivot if not."

FORCING:
> "Decide branches:
> - **Continue**: signals 1, 2, 3 all in target range. Action: proceed to next migration phase per schedule.
> - **Pivot to dual-track**: signal 1 < 99% but ≥ 95% OR signal 2 > +20% but ≤ +50%. Action: extend OFTv1 active window by 1 cycle; investigate root cause; comms update to users.
> - **Abort and rollback**: signal 1 < 95% OR signal 3 < 80%. Action: halt new-contract operations within 4 hours; resume OFTv1 as primary; incident response engaged."

### Exemplar 4, Stating Orient model

SOFTENED:
> "We'll interpret what we see."

FORCING:
> "Expected mental model: based on Stargate v1→v2 migration analog, expect a 24-48h support-ticket spike (~+30%) that normalizes by day 4. LP TVL expected to dip 5-10% then recover. Cross-chain success rate stays ≥ 99%. Surprise indicator: support spike persists > 4 days OR LP TVL drops > 20%, suggesting our model is wrong about user trust dynamics or LP-comms coverage. Model update on surprise: this is closer to Curve 3pool (where comms gap caused LP flight) than to Stargate."

---

## Output Schema

### Section A, Header

```markdown
# OODA Loop, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Cynefin domain:** <from cynefin.md>
**Time pressure:** <from intake>
**Cycle time:** <N days/weeks>
**Total expected cycles:** <K cycles to complete recommendation>
**Mode:** <PRIMARY (complex/chaotic/now) / SECONDARY (complicated/simple)>
```

### Section B, OODA stages

```markdown
## Stages

### Observe (signals to monitor)

| # | Signal | Target | Alert | Source | Cadence |
|---|---|---|---|---|---|
| 1 | <name> | <value> | <threshold> | <where> | <when> |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

### Orient (mental model)

**Expected:** <one paragraph>

**Surprise indicators:**
- <pattern> → model was wrong about <assumption>
- <pattern> → model update: <new framing>

### Decide (branches)

- **Continue**: <trigger> → <action> → <owner>
- **Pivot to <named alt>**: <trigger> → <action> → <owner>
- **Abort/rollback**: <trigger> → <action> → <owner>

### Act (first step per branch)

| Branch | First Act | Owner | Within | Reversible? |
|---|---|---|---|---|
| Continue | <action> | <name/role> | <time> | <yes/no> |
| Pivot | <action> | <name/role> | <time> | <yes/no> |
| Abort | <action> | <name/role> | <time> | <yes/no> |
```

### Section C, Cycle calendar

```markdown
## Cycle Calendar

| Cycle | Date | Observe due | Orient meeting | Decide deadline | Act commit |
|---|---|---|---|---|---|
| 1 | <ISO> | <day> | <day> | <day> | <day> |
| 2 | <ISO> | <day> | <day> | <day> | <day> |
| ... | ... | ... | ... | ... | ... |
```

### Section D, Decision Hook

```markdown
## Decision Hook

OODA's cycle time is the operating constraint. If cycle time > `intake.time_pressure / 3`, flag in dissent.

For PRIMARY mode (complex/chaotic): recommendation must include "smallest probe" + cycle cadence.

For SECONDARY mode (complicated/simple): cycle is an execution-cadence backup; recommendation primary path follows Decision Matrix.
```

### Section E, What This Means For The Decision

### Section F, Completeness

```markdown
**Completeness:** <N>/10
- Cycle time committed in concrete units: +<N>
- 2-4 independent Observe signals with thresholds: +<N>
- Orient mental model + surprise indicators stated: +<N>
- 3 differentiated Decide branches with triggers and owners: +<N>
- First Act per branch specified: +<N>
- Cycle calendar with dates: +<N>
```

---

## Decision Hook

OODA feeds Confidence-Speed-Quality and the recommendation:
- PRIMARY mode → recommendation is "smallest probe + cycle cadence"
- SECONDARY mode → recommendation is Decision Matrix top option + OODA execution cadence

Confidence rubric impact:
- Cycle time ≤ deadline / 3: +0 (baseline)
- Cycle time > deadline / 3: -1 (loop too slow; high risk)

### Override conditions

If OODA cycle time exceeds `intake.time_pressure` deadline, the recommendation must downgrade execution mode (Confidence-Speed-Quality switches to PROBE or DEFER regardless of confidence rubric).

---

## Cross-Framework Triggers

- **Cycle time > deadline / 3** → mark `state.LOOP_TOO_SLOW = true`; Confidence-Speed-Quality reads this
- **Cynefin = complex AND OODA primary** → mark `state.PROBE_MODE = true`
- **Cynefin = chaotic** → cycle time should be ≤ 24h; if not, escalate
- **Cycle calendar lacks named owners** → SendMessage to lead requesting owner assignment

---

## Failure Modes

### Failure Mode 1, Cycle too slow for problem cadence

Trap: weekly cycle on a daily-cadence problem.

Manifestation: cycle time > deadline / 3 OR cycle time > shortest connection-cycle delay / 2.

Check: ratio test. If failing, shorten cycle.

Recovery: shorten cycle (often by reducing scope per cycle: review 3 signals weekly instead of 10 signals weekly with batched analysis).

### Failure Mode 2, Vague signals

Trap: Observe signals lack thresholds; can't trigger a Decide.

Manifestation: signal entries have name + source but no target/alert numbers.

Check: every signal has 5 fields populated.

Recovery: derive thresholds from baseline + research evidence; if no baseline exists, run one cycle to establish it before activating the OODA framework.

### Failure Mode 3, Single-branch Decide

Trap: only "continue" branch present; pivot and abort are placeholder.

Manifestation: Decide table has 1 differentiated row, 2 collapsed.

Check: pivot and abort branches must specify different actions, not "continue with caveat."

Recovery: specify the actual pivot target (named alternative from zwicky-box archetypes) and the abort rollback action.

### Failure Mode 4, Orient skipped

Trap: signals trigger Decide branches without an explicit mental-model update.

Manifestation: Orient stage is empty or generic ("interpret data").

Check: Orient must contain expected model + surprise indicators.

Recovery: write the model. The framework is OODA, not OdA.

### Failure Mode 5, No cycle calendar

Trap: cycle described in abstract, no specific dates committed.

Manifestation: cycle calendar section empty.

Check: at least the first 2 cycle dates committed.

Recovery: derive dates from intake.time_pressure + cycle time; commit to ISO dates.

---

## Jargon Glossary

- **OODA**, Observe-Orient-Decide-Act; Boyd's decision cycle.
- **cycle time**, the duration of one full O→O→D→A iteration.
- **leading indicator**, a signal that changes BEFORE the outcome you care about; what Observe should monitor.
- **lagging metric**, a signal that changes AFTER the outcome; useful for postmortems but not for OODA.
- **Decide branch**, a specific action triggered by a specific signal pattern (continue / pivot / abort).
- **Act first step**, the immediate concrete action within hours of a Decide branch firing.
- **mental model**, the team's expected trajectory of the system; explicit in Orient.
- **surprise indicator**, a deviation pattern that signals the mental model is wrong; triggers a model update.
- **PRIMARY mode**, OODA is the dominant decision framework (complex/chaotic domains, urgent runs).
- **SECONDARY mode**, OODA is the execution cadence; Decision Matrix is the dominant decision framework.
- **probe**, a smallest-scale experiment to gather signal under PROBE mode (used in PRIMARY OODA for complex domains).

---

## Completeness Scoring

### 10/10, Decisive
- Cycle time in concrete units, ≤ deadline / 3
- 2-4 independent Observe signals with all 5 fields
- Orient model + surprise indicators
- 3 differentiated Decide branches with triggers, actions, owners
- First Act per branch specified, with reversibility
- Cycle calendar with at least 2-3 cycles dated

### 7/10, Confident
- All sections present
- Cycle time committed but cycle calendar partial
- Some Observe signals lack alert thresholds
- Decide branches differentiated but owners missing

### 4/10, Tentative
- Cycle time vague ("weekly")
- Signals lack thresholds
- Decide branches collapse to 1-2
- No Orient model

### 0/10, Unusable
- Generic "iterate" without OODA structure
- No cycle time
- No signals
- No Decide branches

OODA completeness ≤ 4 contributes -1 to overall rubric AND triggers `state.LOOP_TOO_SLOW = true`.

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

### Inputs

- Cynefin: complicated → OODA SECONDARY mode
- Time pressure: this-month (2-4 weeks deadline)
- Decision Matrix top: B (dual-deploy + drain), score 8.2
- Connection-cycles delays: balancing cycle ~2 days, reinforcing cycle multi-week

### Step 1, Cycle time

- Deadline / 3: this-month → ~7-10 days
- Shortest cycle delay / 2: balancing 2 days / 2 = 1 day
- Cycle time chosen: 7 days (weekly)
- Justification: balancing-cycle effects (gas → migration eagerness) play out over days; we don't need daily cycles. Reinforcing cycle (multi-week) means weekly cadence catches early signals before compounding.

### Step 2, Observe signals

| # | Signal | Target | Alert | Source | Cadence |
|---|---|---|---|---|---|
| 1 | Cross-chain transfer success rate | ≥ 99% rolling 24h | < 95% | Contract event logs aggregated daily | Daily check, weekly review |
| 2 | Support ticket volume on migration | ≤ baseline 50/day, max +20% during cutover | > +50% from baseline | Support tool dashboard | Daily check, weekly review |
| 3 | LP TVL on bridge pools | ≥ 90% of pre-migration | < 80% | On-chain TVL aggregator (DeFiLlama API) | Daily check, weekly review |

### Step 3, Orient

**Expected:** dual-deploy + drain pattern follows Stargate analog. 24-48h support spike around contract activation, normalizes by day 4. LP TVL dips 5-10% then recovers as drain mechanism activates. Cross-chain success rate stays ≥ 99% throughout.

**Surprise indicators:**
- Support spike persists > 4 days → comms failure, not UX (model update: this is Curve 3pool not Stargate; LP comms gap is the issue)
- LP TVL > 20% drop → trust failure rather than dip-and-recover (model update: re-engage LPs with direct outreach; pause force-migration)
- Success rate < 99% → mempool dynamics worse than expected (model update: testnet probe didn't surface this; mainnet has different conditions)

### Step 4, Decide branches

- **Continue (proceed to next phase)**: signals 1, 2, 3 all in target range OR transient deviation < 24h. Action: proceed per schedule. Owner: $ENG_LEAD.
- **Pivot to extended dual-track**: signal 1 < 99% but ≥ 95% OR signal 2 > +20% but ≤ +50%. Action: extend OFTv1 active window by 1 cycle; investigate root cause; user comms update; do NOT advance to next phase. Owner: $ENG_LEAD + $PRODUCT.
- **Abort and rollback**: signal 1 < 95% OR signal 3 < 80% OR signal 2 > +50%. Action: halt new-contract operations within 4 hours; resume OFTv1 as primary; incident response engaged. Owner: $ENG_LEAD on call.

### Step 5, Act first steps

| Branch | First Act | Owner | Within | Reversible? |
|---|---|---|---|---|
| Continue | Deploy next-phase migration steps per runbook | $ENG_LEAD | 24h after Decide | Yes (rollback runbook exists) |
| Pivot | Comms update + investigate root cause | $ENG_LEAD + $PRODUCT | 4h | Yes |
| Abort | Halt drain mechanism on all chains | $ENG_LEAD on call | 4h | Yes (resume OFTv1) |

### Cycle calendar

| Cycle | Date | Observe due | Orient meeting | Decide deadline | Act commit |
|---|---|---|---|---|---|
| 1 | 2026-05-04 | Mon AM | Tue 10am | Tue EOD | Wed |
| 2 | 2026-05-11 | Mon AM | Tue 10am | Tue EOD | Wed |
| 3 | 2026-05-18 | Mon AM | Tue 10am | Tue EOD | Wed |
| 4 | 2026-05-25 | Mon AM | Tue 10am | Tue EOD | Wed |
| 5 | 2026-06-01 | Mon AM | Tue 10am | Tue EOD | Wed |
| 6 | 2026-06-08 | Mon AM | Tue 10am | Tue EOD | Wed (final) |

Total expected cycles: 6 (matches 6-week migration plan from execution outline).

### Output completeness

- Cycle time committed (7 days): yes
- 3 independent signals with all 5 fields: yes
- Orient model + 3 surprise indicators: yes
- 3 differentiated Decide branches with triggers + owners: yes
- First Act per branch specified with reversibility: yes
- Cycle calendar with all 6 cycles dated: yes

**Completeness: 10/10**

---

## What This Means For The Decision

OODA in this OFTv2 run sets the execution cadence at 7 days for 6 cycles. The framework's value is committing the team to a Tuesday 10am check-in with 3 specific signals and 3 differentiated Decide branches. Without OODA, the dual-deploy+drain rollout would happen on a "we'll see" cadence; with it, Tuesday becomes a decision point with specific go/pivot/abort triggers.

The framework is SECONDARY mode here (cynefin = complicated, Decision Matrix dominates). If the testnet probe surfaces unexpected mempool dynamics and we re-classify to complex, OODA flips to PRIMARY and the recommendation downgrades to PROBE mode. The cycle template is robust to that flip; only the cadence might tighten (3-4 day cycles instead of 7).
