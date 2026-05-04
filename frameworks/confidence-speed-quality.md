# Confidence Determines Speed vs Quality

**Phase:** Decide (runs after rubric is computed) · **Source:** https://untools.co/confidence-determines-speed-vs-quality

This framework converts the confidence rubric into an execution mode. The rubric tells you how sure you are. Reversibility tells you what failure costs. The intersection picks one of four modes: SPEED, QUALITY, PROBE, or DEFER. The mode shapes the recommendation: how fast to ship, what to check before shipping, what signal to gather, when not to decide at all.

The most common decision-making mistake is treating a low-confidence one-way-door as a high-confidence MVP. This framework prevents that.

---

## Entry Predicate

```
always_run
```

Runs every time Phase 3 fires. Confidence-Speed-Quality reads the computed rubric (Step 11 of SKILL.md), the cynefin domain, and intake.reversibility. It writes the execution mode that the recommendation inherits.

### Inputs

- `state.confidence.rubric` — the 0-10 additive score computed in Step 11
- `state.confidence.posterior` — the Bayesian posterior 0-1
- `state.confidence.bucket` — HIGH / MEDIUM / LOW
- `frameworks/cynefin.md::domain` — simple / complicated / complex / chaotic / disorder
- `intake.reversibility` — cheap / costly / one-way-door
- `frameworks/decision-matrix.md::top_recommendation` — the option being evaluated
- `frameworks/second-order.md::compounding` — does the option compound (positive or negative)?
- `frameworks/six-hats.md::synthesis` — agreement count, Black Hat severity

### Outputs

- `$RUN_DIR/frameworks/confidence-speed-quality.md` — the 2x2 placement + mode + execution shape
- `state.execution_mode` field — read by Minto and the final report renderer
- (Conditional) `state.PRE_SHIP_CHECKLIST` — populated when mode = QUALITY
- (Conditional) `state.PROBE_DEFINITION` — populated when mode = PROBE
- (Conditional) `state.DEFER_LEARN_LIST` — populated when mode = DEFER

---

## Operating Principles

These are non-negotiable. Every mode placement respects all five.

**1. Confidence and reversibility are independent axes.**

Confidence asks "do we know what to do?" Reversibility asks "what does it cost to undo?" Both have to be evaluated separately. A high-confidence one-way-door is not the same as a high-confidence reversible decision. The first demands quality. The second demands speed. Anti-pattern: collapsing both axes into a single "should we ship?" gut call. The 2x2 only works when both axes are scored independently.

**2. The mode is a constraint on execution, not a description of it.**

The mode is what the recommendation must respect. SPEED means the recommendation must include a 24-hour first step. QUALITY means it must include a pre-ship checklist. PROBE means it must define success and failure signals upfront. DEFER means it must list what to learn before deciding. Anti-pattern: writing "ship the MVP" and calling it SPEED mode without naming the 24-hour first step. The mode without the artifact is just a label.

**3. Reversibility is intake-locked but can be challenged.**

The user gave you a reversibility answer in intake. Trust it as the prior. But if Second-Order analysis surfaced a compounding effect that makes a "costly" reversal actually one-way-door (because the compounding makes the original state unrecoverable), challenge the intake answer in the output and recommend re-running. Anti-pattern: blindly using intake.reversibility when prior frameworks contradict it. Compounding cycles often turn costly into one-way-door.

**4. Confidence is the rubric, not your gut.**

The 0-10 rubric is the input. Don't override it with "this feels confident." If the rubric says 5/10, the bucket is MEDIUM, regardless of how you feel about the recommendation. The whole point of the rubric is to discipline gut overconfidence. Anti-pattern: writing "rubric says 5 but I'm placing this on the high-confidence side because the team is excited." That's the bias the rubric exists to correct.

**5. The 2x2 is a routing function, not an opinion.**

Once you have confidence (HIGH/LOW thresholded at rubric ≥ 7) and reversibility (reversible/one-way thresholded at intake.reversibility = cheap), the 2x2 produces a deterministic mode. There's no judgment call inside the routing. The judgment happened upstream when computing the rubric and naming reversibility. Anti-pattern: re-litigating the rubric inside this framework. If you disagree with the rubric, fix the rubric in Step 11 and re-run, don't fudge the placement.

---

## Response Posture

**Tone.** Mechanical. The agent is computing a function: (confidence, reversibility) → mode. There is no creative work in the placement. The creative work is naming the artifact the mode requires (pre-ship checklist, probe signals, learn-list).

**Pacing.** Single placement per run. The framework reads the inputs, writes the 2x2, names the mode, produces the artifact. No back-and-forth with the user.

**Push depth.** None on the placement. Heavy push on the artifact. A pre-ship checklist with three vague items ("test it, review it, ship it") is shallow. A pre-ship checklist with twelve specific items, each tied to a frameworks output ("confirm second-order's reinforcing cycle is monitored via metric X with alert at threshold Y") is deep.

**Where to escalate.** SendMessage to lead when:
- Mode is DEFER and intake.time_pressure = "now" (contradiction; lead must reconcile)
- Mode is PROBE but no probe-shape can be defined (e.g. "we can't ship anything smaller than the full thing"; this means PROBE is wrong, escalate to re-rubric)
- Mode is QUALITY but the team has hard-shipped a similar one-way-door with no checklist three times in the last quarter (cultural signal that QUALITY won't be respected; the recommendation must explicitly call this out)
- intake.reversibility says "costly" but Second-Order says compounding is unrecoverable (challenge to intake)

---

## Anti-Sycophancy Rules

The agent running Confidence-Speed-Quality must never write these:
- "Either approach could work depending on context..." (the 2x2 picks one; state it)
- "Speed and quality are both important..." (cut to the mode)
- "You'll want to balance moving quickly with getting it right..." (mode tells you how to balance)
- "Consider the trade-offs..." (the framework computed the trade-off; state the result)
- "It depends on your risk tolerance..." (risk tolerance was captured in intake.reversibility)

The agent must always:
- Place the case on the 2x2 with both coordinates stated.
- Name the mode (SPEED / QUALITY / PROBE / DEFER) in one word.
- Produce the artifact the mode requires (24-hour step, pre-ship checklist, probe signals, learn-list).
- Name what would change the mode: "if confidence drops below 7, this becomes PROBE."

---

## Pushback Patterns

These show how the agent self-corrects when prior frameworks or intake send mixed signals.

**Pattern 1: rubric says HIGH but team feels LOW then trust the rubric or fix the rubric**

- Internal evidence: "Rubric scored 8/10. Team retro mentioned multiple unresolved doubts."
- BAD: "Mark as MEDIUM since the team feels uncertain despite the rubric."
- GOOD: "Rubric is the input. If the team's doubts are real, they should be in the rubric. Re-examine: did Six Hats agreement count over-credit a hat that wasn't deeply considered? Did the adversary score under-credit a structural risk? Either fix the rubric component and re-compute (preferred) or override with explicit justification: 'rubric says 8 but team has uninspected doubt about X, downgrading bucket to MEDIUM with the dissent explicitly listing X.' Don't silently fudge the placement."

**Pattern 2: intake says reversible but Second-Order says compounding then re-evaluate reversibility**

- Internal evidence: "intake.reversibility = costly. Second-Order shows reinforcing cycle that, once triggered, has no symmetric reversal."
- BAD: "Use intake's costly placement. The 2x2 placement is QUALITY."
- GOOD: "Compounding cycles change reversibility. If we ship and the cycle starts, we can't get back to the pre-ship state in finite time, only to a different state with different dynamics. That's one-way-door, not costly. Challenge intake: 'the user marked this costly but Second-Order shows a reinforcing cycle that makes the post-ship state non-symmetric to the pre-ship state. Recommend treating as one-way-door.' Place on the QUALITY axis but raise the bar: pre-ship checklist must explicitly verify the cycle's monitoring is in place before launch."

**Pattern 3: confidence is HIGH but Black Hat scored 9 then HIGH confidence is wrong**

- Internal evidence: "Rubric = 8. Adversary attacks include one with severity 9 (not score 9; attack-severity 9)."
- BAD: "Place as HIGH. Note the Black Hat concern in dissent."
- GOOD: "Adversary severity 9 means the strongest attack would invalidate the recommendation. The rubric should have already absorbed this via the 'adversary max score ≤ 4' component (which adds +2 to the rubric). If adversary max is 9, that's -2 on the rubric component, so the rubric should not be 8. Either the rubric component was scored wrong (fix it) or the adversary attack-severity score was wrong (challenge and re-score). Don't ship with HIGH confidence and a 9-severity attack uncovered. SendMessage to lead and re-run rubric."

**Pattern 4: time_pressure = now but mode is DEFER then call the contradiction**

- Internal evidence: "Rubric = 4. Reversibility = one-way-door. Intake.time_pressure = now."
- BAD: "Mode is DEFER. Recommendation: do not decide yet."
- GOOD: "DEFER conflicts with time-pressure = now. Two real options: (a) accept the contradiction and tell the user 'we can't responsibly decide this in the time you have; either get more time or accept lower confidence on a forced decision'; (b) downgrade to PROBE if there's any reversible probe shape we can ship now to start gathering evidence. Don't silently write DEFER when intake says we have to act. Make the contradiction visible to the user. SendMessage to lead with the conflict explicit."

**Pattern 5: HIGH confidence on a complex domain then question the rubric**

- Internal evidence: "Cynefin = complex. Rubric = 9."
- BAD: "Place as HIGH + costly = QUALITY. Ship after pre-ship checklist."
- GOOD: "Complex domains have unknowable cause-effect by definition. A rubric of 9 in a complex domain means either (a) the domain was misclassified and is actually complicated, in which case re-run cynefin; or (b) the rubric over-credited some component, often Six Hats agreement on a path the system genuinely can't predict. Cap confidence in complex domains at MEDIUM regardless of rubric. Mode becomes PROBE not QUALITY: ship the smallest experiment that produces signal, not the full polished thing. The complex domain is the harder constraint."

---

## Method

Confidence-Speed-Quality runs as a 6-step procedure. Each step produces a discrete output that feeds the next.

### Step 1, Read the rubric and reversibility

```bash
cat $RUN_DIR/state.json | jq '.confidence'
cat $RUN_DIR/intake.json | jq '.reversibility'
cat $RUN_DIR/frameworks/cynefin.md | grep -E "^Domain:" | head -1
```

Get:
- rubric (0-10 integer)
- posterior (0-1 float)
- bucket (HIGH / MEDIUM / LOW)
- reversibility (cheap / costly / one-way-door)
- domain (simple / complicated / complex / chaotic / disorder)

Failure mode: framework runs before rubric is computed. Check: rubric must be a non-null integer in state.json. If null, SendMessage to lead: "rubric not yet computed, blocked."

### Step 2, Threshold both axes

The 2x2 needs binary inputs.

```
confidence_axis:
  HIGH if rubric ≥ 7
  LOW  otherwise

reversibility_axis:
  REVERSIBLE if intake.reversibility = cheap
  ONE-WAY    if intake.reversibility ∈ {costly, one-way-door}
```

Note: "costly" maps to ONE-WAY in this framework. The reasoning is asymmetric: a cheap reversal genuinely lets you ship-and-iterate; a costly reversal is functionally one-way for execution-mode purposes (you only get one good shot before reversal becomes prohibitive). The detailed shape of "costly vs one-way-door" lives in the artifact (pre-ship checklist depth varies).

### Step 3, Apply complex-domain cap

```
if cynefin.domain = complex:
  confidence_axis ← min(confidence_axis, LOW)  # complex caps at LOW

if cynefin.domain = chaotic:
  confidence_axis ← LOW  # by definition
  mode ← act-first (special case)

if cynefin.domain = disorder:
  halt; mode is undefined; SendMessage to lead
```

Complex domains have unknowable cause-effect, so HIGH confidence is structurally suspect. The cap forces PROBE or DEFER mode regardless of rubric. This is the most important guardrail in the framework.

### Step 4, Compute the mode

The 2x2:

```
                  REVERSIBLE          ONE-WAY
              ┌──────────────────┬──────────────────┐
       HIGH   │      SPEED       │     QUALITY      │
   confidence │  ship MVP fast   │  careful build   │
              │  iterate after   │  ship once       │
              ├──────────────────┼──────────────────┤
       LOW    │      PROBE       │      DEFER       │
   confidence │  smallest test   │  gather evidence │
              │  signal first    │  before deciding │
              └──────────────────┴──────────────────┘
```

Read off the mode from the cell. Edge cases:
- chaotic domain + reversible: mode = act-first-then-stabilize (special: skip the 2x2)
- disorder: no mode; halt
- HIGH confidence + reversible + intake.time_pressure = "no-deadline": still SPEED, but check that the user actually wants to ship; otherwise downgrade to QUALITY by user choice (rare)

### Step 5, Generate the mode artifact

Each mode requires a specific artifact in the framework output:

**SPEED mode artifact: 24-hour first step**

A single named action the user takes within 24 hours of reading the report. Must be:
- Specific (not "set up the project")
- Concrete (a command, a file write, a meeting booked)
- Producing observable output (so the user knows it's done)
- Reversible (consistent with the SPEED mode premise)

Example for OFTv1 → OFTv2 if it landed in SPEED (it doesn't, but for illustration): "Within 24h, deploy OFTv2 to Sepolia testnet via `forge script script/DeployOFTv2.s.sol --rpc-url $SEPOLIA_RPC --broadcast` and verify the contract resolves on Etherscan."

**QUALITY mode artifact: pre-ship checklist**

A list of 8-15 verification steps that must complete before shipping. Each item must be:
- Tied to a specific framework output (cite which framework surfaced this concern)
- Verifiable (someone can mark it done with confidence)
- Ordered (some items block others)
- Cost-budgeted (each item has an effort estimate)

Items typically draw from:
- Second-Order (compounding cycles need monitoring)
- Six Hats Black (top failure modes need mitigation)
- Adversary (top attacks need responses)
- Iceberg structures (architecture concerns need review)
- Reinforcing-loop (loops need observability before launch)

**PROBE mode artifact: probe definition**

A specification of:
- What the probe does (the smallest version of the action)
- What success looks like (specific signal, specific threshold)
- What failure looks like (specific signal, specific threshold)
- How long the probe runs (time-boxed, typically 1-4 weeks)
- What the probe costs (effort and money)
- What's the next step in each branch (success → scale up; failure → reroute)

The probe artifact is the single most important output of /solve in complex domains.

**DEFER mode artifact: learn-list**

A list of 3-7 evidence gaps the team must fill before deciding. Each item:
- Names the gap specifically (not "learn more about X" but "find out whether X behaves like Y under Z")
- Names how to learn (research, expert consult, small experiment, customer interview)
- Names the time-cost (hours / days)
- Names the budget cap (so DEFER doesn't become DEFER-FOREVER)

**act-first-then-stabilize mode artifact (chaotic only): stabilizing action**

A single action the user takes immediately. The action's only goal is to move the system out of chaotic into complex or complicated. After the action, /solve re-runs from intake.

### Step 6, Write output and update state

The output structure is mandatory. See Output Schema below.

State updates:
```json
{
  "execution_mode": "SPEED" | "QUALITY" | "PROBE" | "DEFER" | "act-first",
  "execution_artifact_path": "$RUN_DIR/frameworks/confidence-speed-quality.md#artifact"
}
```

Plus the mode-specific state field (PRE_SHIP_CHECKLIST, PROBE_DEFINITION, DEFER_LEARN_LIST).

---

## Probe Patterns

This framework runs analytically. The agent asks itself probes while reading prior outputs.

### Probe Pattern 1, rubric integrity

> "Did the rubric absorb the adversary score correctly? Adversary max ≤ 4 should have added +2 to the rubric. If adversary max is 9, the rubric component should be 0, not +2."

If the rubric component math doesn't reconcile, SendMessage to lead: rubric needs re-computation.

### Probe Pattern 2, reversibility challenge

> "Did Second-Order or Reinforcing-Loop surface a compounding effect that makes the post-ship state structurally different from the pre-ship state? If yes, intake's 'costly' may actually be one-way-door."

The check: read second-order.md for the words "irreversible," "compounds," "no symmetric reversal," "lock-in." If present, flag the reversibility challenge in the output.

### Probe Pattern 3, complex-domain cap

> "Cynefin says domain. If complex, am I about to write HIGH confidence? Stop. Cap to LOW."

Hard rule. No exceptions. Complex domain + HIGH confidence is a contradiction.

### Probe Pattern 4, mode-artifact alignment

> "Did I write a SPEED mode but no 24-hour step? Or QUALITY mode but no checklist? The artifact is the mode. Without it, the mode is a label, not a recommendation."

Self-validate: if mode = X, file must contain artifact section X.

### Probe Pattern 5, time-pressure conflict

> "If mode = DEFER and intake.time_pressure = now, this is a contradiction. The user can't both 'not decide yet' and 'decide now.' Surface the conflict."

The output must explicitly call this out. The user decides whether to extend the deadline or accept lower confidence on a forced decision.

---

## Forcing Exemplars

When writing the output, every claim should have a forcing version (specific, evidence-grounded) instead of a softened version (hedged, vague).

### Exemplar 1, stating the placement

SOFTENED (avoid):
> "Given the high level of confidence and the fact that this decision is somewhat difficult to reverse, we recommend a balanced approach that prioritizes quality."

FORCING (aim for):
> "Placement: HIGH confidence (rubric 9/10) × ONE-WAY (intake.reversibility = costly, upgraded to ONE-WAY by Second-Order's reinforcing cycle which makes post-ship state non-symmetric). Mode: QUALITY. Recommendation must include a pre-ship checklist before any code lands."

### Exemplar 2, naming the artifact

SOFTENED (avoid):
> "Before shipping, make sure to test thoroughly and consider the various concerns raised in the analysis."

FORCING (aim for):
> "Pre-ship checklist (12 items, ordered):
> 1. (Second-Order) Deploy bridge-volume metric with 24h SLO at $X TVL ± 10%; alert at deviation > 15% sustained 1h. Effort: 4h.
> 2. (Six Hats Black) Run mempool-stress simulation under 200 gwei equivalent on Sepolia + Avalanche; verify cross-chain settlement < 5 min. Effort: 1d.
> 3. (Adversary) Engage external auditor to review OFTv2 cross-chain message-encoding diff. Effort: 1 week, $X.
> 4. (Reinforcing-Loop) LP-fee dashboard live before deploy; confirm read-path unaffected by migration. Effort: 4h.
> ... [8 more items] ..."

### Exemplar 3, naming what would change the mode

SOFTENED (avoid):
> "If our level of confidence were to change significantly, we would reconsider the recommended approach."

FORCING (aim for):
> "What changes the mode:
> - Rubric drops below 7 (e.g. adversary surfaces a new structural attack): mode flips to PROBE; the pre-ship checklist becomes a probe definition.
> - Reversibility downgrades to one-way-door (e.g. legal team confirms the migration is unwind-blocked under regulation X): mode stays QUALITY but pre-ship checklist gains a 'kill switch' item.
> - Time-pressure changes to 'now' (e.g. a security disclosure forces emergency action): mode becomes act-first; QUALITY becomes infeasible; document and accept lower confidence."

### Exemplar 4, the contradiction-surfacing

SOFTENED (avoid):
> "There is some tension between the desire to defer the decision and the time pressure noted in the intake."

FORCING (aim for):
> "Conflict: mode computed as DEFER (rubric 4/10, reversibility one-way-door). Intake.time_pressure = 'now.' These contradict. Resolutions:
> - (preferred) Extend deadline by 2 weeks; use the time to fill the learn-list (3 items below).
> - (acceptable) Downgrade to PROBE if there's any reversible probe-shape; the team accepts that the probe may not finish before the deadline and will decide on partial signal.
> - (worst case) Force the decision under DEFER conditions; the rubric stays 4 and the recommendation explicitly notes 'this decision is being made under time pressure with insufficient evidence; expect a retraction or revision in 4-8 weeks.'
> Lead must pick one resolution before the report renders."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/confidence-speed-quality.md` follows this structure exactly. Every section is required.

### Section A, Header

```markdown
# Confidence vs Speed vs Quality, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** state.json (confidence), intake.json (reversibility), frameworks/cynefin.md, frameworks/decision-matrix.md, frameworks/second-order.md, frameworks/six-hats-*.md, frameworks/adversary.jsonl
```

### Section B, the 2x2 (mermaid quadrant)

```mermaid
quadrantChart
  title Confidence × Reversibility
  x-axis One-Way --> Reversible
  y-axis Low Confidence --> High Confidence
  quadrant-1 SPEED
  quadrant-2 QUALITY
  quadrant-3 PROBE
  quadrant-4 DEFER
  Problem Position: [<x>, <y>]
```

X-axis: 0 = one-way-door, 1 = cheap reversal.
Y-axis: 0 = LOW confidence (rubric ≤ 4), 1 = HIGH confidence (rubric = 10).

Position from inputs:
- x = (intake.reversibility == "cheap") ? 1.0 : (intake.reversibility == "costly" ? 0.4 : 0.0)
- y = rubric / 10

### Section C, axis values

```markdown
| Axis | Raw value | Threshold | Bucket |
|---|---|---|---|
| Confidence | rubric = <N>/10, posterior = <N> | rubric ≥ 7 = HIGH | <HIGH/LOW> |
| Reversibility | intake = <cheap/costly/one-way> | cheap = REVERSIBLE | <REVERSIBLE/ONE-WAY> |
```

If the complex-domain cap fires, add a row:

```markdown
| Cap | cynefin = complex | force LOW | LOW (capped) |
```

### Section D, mode

```markdown
## Mode: <SPEED | QUALITY | PROBE | DEFER | act-first>

**Justification:** <2-3 sentences citing the rubric components, the reversibility evidence, and any caps applied. Specific. No hedging.>

**Confidence trajectory:** <how the rubric got to this number; cite each +2 component>
```

### Section E, mode artifact (one of the four below)

#### SPEED artifact

```markdown
## 24-Hour First Step

**Action:** <single specific action>
**Command / artifact:** <command line or file path>
**Observable signal:** <what tells the user it's done>
**Reversibility check:** <what reversal looks like if it fails>
**Estimated effort:** <hours>

## Subsequent iteration cadence

| Cycle | Length | Goal | Exit condition |
|---|---|---|---|
| 1 | <N days> | <goal> | <signal> |
| 2 | <N days> | <goal> | <signal> |
| 3 | <N days> | <goal> | <signal> |
```

#### QUALITY artifact

```markdown
## Pre-Ship Checklist

| # | Item | Source framework | Effort | Blocks |
|---|---|---|---|---|
| 1 | <verification step> | <framework> | <hours/days> | <#s of items this blocks> |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

**Total effort estimate:** <hours/days>
**Critical path:** <ordered list of items on the longest dependency chain>
**Cost cap:** <$> (if external auditor / vendor work in checklist)

## Ship gate

Ship only when:
- All <N> checklist items marked complete by named owner
- <K> "must-pass" items have green signal (cite which items)
- No new adversary findings ≥ severity 7 introduced during checklist execution
```

#### PROBE artifact

```markdown
## Probe Definition

**Smallest version:** <description; what we ship>
**Time-box:** <N weeks>
**Effort cap:** <hours/days>
**Cost cap:** <$>

### Success signal

**Metric:** <named metric>
**Threshold:** <specific number>
**Window:** <time window over which to measure>
**If success:** <next action; typically "scale up to full version">

### Failure signal

**Metric:** <named metric, may be different from success metric>
**Threshold:** <specific number>
**Window:** <time window>
**If failure:** <next action; typically "reroute via OODA loop and re-run /solve">

### Ambiguity signal

**Definition:** <what "neither clear success nor clear failure" looks like>
**Default action:** <usually "extend probe by N weeks" or "split into two sub-probes">

## Re-decision trigger

After <time-box>, re-run /solve with the probe outcome as new evidence. Specifically update:
- intake.success_criteria (now measurable)
- evidence pool (probe data)
- frameworks/second-order.md (re-validate compounding)
```

#### DEFER artifact

```markdown
## Learn-List (do not decide yet)

| # | Gap | How to learn | Effort | Cost |
|---|---|---|---|---|
| 1 | <specific evidence gap> | <method> | <hours/days> | <$> |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

**Total time-to-decision estimate:** <weeks>
**Budget cap:** <$> (so DEFER doesn't become DEFER-FOREVER)

## Re-decision conditions

Re-run /solve when:
- All <N> learn-list items have evidence on file in $RUN_DIR/evidence/
- OR <M> weeks elapse without progress (force a decision under reduced confidence)
- OR external pressure changes (e.g. competitor ships first; market opens)
```

#### act-first artifact (chaotic domain only)

```markdown
## Stabilizing Action

**Action:** <single action>
**Goal:** move system from chaotic to complex (or complicated)
**Time:** within <N hours>
**Post-action:** re-run /solve from intake; the new domain classification dictates next steps
```

### Section F, mode-change conditions

```markdown
## What changes the mode

| Trigger | Current mode | New mode | Action |
|---|---|---|---|
| Rubric drops to <N> | SPEED | PROBE | redefine the smallest version |
| Reversibility downgrades to one-way | QUALITY | DEFER | populate learn-list |
| Adversary surfaces severity 9 | any | DEFER | re-run rubric |
| Time-pressure changes to "now" | DEFER | act-first or PROBE | resolve contradiction |
```

### Section G, contradictions and dissent

```markdown
## Open contradictions

<List any conflicts between mode, intake, prior frameworks. Each contradiction must have:>
- The conflict in 1 sentence
- The evidence on each side
- The proposed resolution
- The owner (lead / decider / user)
```

### Section H, what this means for the decision

```markdown
## What This Means For The Decision

<2-3 sentences synthesizing what the mode implies for the recommendation. Specific. Decision-actionable.>
```

### Section I, completeness score

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- Both axes thresholded with cited evidence: +<N>
- Complex-domain cap evaluated: +<N>
- Mode artifact populated with required depth: +<N>
- Mode-change conditions specified: +<N>
- Contradictions surfaced (or absence noted): +<N>
```

---

## Decision Hook

Confidence-Speed-Quality's output drives the shape of the final recommendation. Specifically:

### Recommendation shape per mode

| Mode | Recommendation must include | Recommendation must NOT |
|---|---|---|
| SPEED | 24-hour first step, iteration cadence, exit conditions | "exhaustive analysis," "comprehensive review" |
| QUALITY | pre-ship checklist with N items, owners, ship gate | "ship and iterate," "MVP first" |
| PROBE | probe definition with success/failure signals, time-box | "the recommendation," "the answer" |
| DEFER | learn-list, time-to-decision, budget cap | "we should X" (no decision yet) |
| act-first | stabilizing action, post-action /solve re-run | strategic recommendation |

The Minto pyramid synthesis at the end inherits the mode's recommendation shape.

### Confidence-rubric impact

Confidence-Speed-Quality does not modify the rubric. It consumes it. The framework's output cannot retroactively change the +2/0 components of Step 11.

### Override conditions

Confidence-Speed-Quality overrides Decision Matrix's recommendation timing. Decision Matrix says "do X." This framework says "do X but in mode Y." If Decision Matrix's top option assumes SPEED execution but the mode is QUALITY, the recommendation pace adjusts. Decision Matrix loses on timing; it does not lose on what to do.

---

## Cross-Framework Triggers

These conditions in the Confidence-Speed-Quality output force changes elsewhere in /solve.

### Triggers fired by mode

- mode = DEFER, populate `state.DEFER_LEARN_LIST`. The Minto pyramid's Answer changes from "do X" to "learn X1, X2, X3 then re-decide."
- mode = PROBE, populate `state.PROBE_DEFINITION`. Minto's Answer becomes "ship probe X with success signal Y."
- mode = QUALITY, populate `state.PRE_SHIP_CHECKLIST`. Minto's Why arguments must include checklist completion as a precondition.
- mode = act-first, halt /solve. The recommendation is "stabilize first, re-run /solve after." No Minto synthesis.

### Triggers fired by reversibility challenge

- intake.reversibility = "costly" but Second-Order shows compounding makes it functionally one-way, append a "Reversibility Challenge" section to the report. The user is asked to confirm the upgraded reversibility before report finalizes.

### Triggers fired by mode-domain conflict

- cynefin.domain = simple but mode = DEFER, structural inconsistency (simple problems shouldn't need deferral). Re-run rubric or re-run cynefin. SendMessage to lead.
- cynefin.domain = complex but mode = SPEED, the complex-domain cap should have prevented this. Bug in the framework execution. SendMessage to lead.

---

## Failure Modes

Confidence-Speed-Quality can mislead in five distinct ways. The framework checks for each before completing.

### Failure Mode 1, mode without artifact

Trap: the framework writes "Mode: QUALITY" and stops. The user sees a label but has no checklist. The recommendation is unactionable.

Manifestation: output file has Section D (mode) but Section E (artifact) is empty or has placeholder text.

Check: before completing, the agent verifies Section E contains the artifact corresponding to the mode named in Section D.

Recovery: populate the artifact. If the agent can't (e.g. PROBE mode but no probe-shape exists), SendMessage to lead and re-evaluate the mode.

### Failure Mode 2, complex domain with HIGH confidence

Trap: cynefin says complex, rubric says 8, agent places as HIGH × ONE-WAY = QUALITY. But complex domains have unknowable cause-effect; HIGH confidence is structurally suspect.

Manifestation: Section D mode = QUALITY despite Section B noting cynefin.domain = complex.

Check: hard rule, complex domain forces confidence_axis ← LOW.

Recovery: re-run with the cap; mode flips to PROBE or DEFER.

### Failure Mode 3, reversibility taken at face value

Trap: intake says "costly" so the framework treats it as ONE-WAY without checking Second-Order. But "costly" can mean two different things: literally expensive to reverse (still reversible, just painful) vs structurally non-reversible due to compounding.

Manifestation: reversibility axis = ONE-WAY with no reversibility-challenge section, and Second-Order shows a reinforcing cycle.

Check: when intake.reversibility = "costly," the agent must read second-order.md and explicitly state "compounding makes this functionally one-way" or "compounding does not change the costly classification, the reversal is expensive but tractable."

Recovery: add the challenge section. SendMessage to user if upgrading from costly to one-way-door.

### Failure Mode 4, time-pressure contradiction silently buried

Trap: mode = DEFER, intake.time_pressure = "now," the framework writes the DEFER artifact and moves on. The user gets a report that says "do not decide yet" when they explicitly need to decide today.

Manifestation: Section E has a learn-list with multi-week time-to-decision, but intake says now. No contradiction section.

Check: whenever mode = DEFER and time_pressure ∈ {now, this-week}, Section G must have a contradiction entry.

Recovery: write the contradiction. SendMessage to lead.

### Failure Mode 5, rubric drift between Step 11 and this framework

Trap: Step 11 wrote rubric = 7. Confidence-Speed-Quality reads "let's say 8 because the team feels good about it." Drift.

Manifestation: Section C shows rubric = 8 but state.json shows 7.

Check: the agent reads rubric from state.json, never re-derives it. If the rubric in Section C doesn't match state.json, fail and re-run.

Recovery: re-read state.json. If the rubric needs to change, change it in Step 11, not here.

---

## Jargon Glossary

Confidence-Speed-Quality uses domain-specific vocabulary. First use of any of these terms in the output should include a one-line gloss.

- confidence-rubric, the 0-10 additive score computed in Step 11 of SKILL.md.
- posterior, the Bayesian probability the decision is correct given evidence; range 0-1.
- bucket, the discrete confidence label (HIGH / MEDIUM / LOW) derived from rubric and posterior.
- reversibility, the cost to undo the action; from intake; cheap / costly / one-way-door.
- mode, the execution shape: SPEED / QUALITY / PROBE / DEFER / act-first.
- artifact, the named output the mode requires (24h step, checklist, probe def, learn-list, stabilizing action).
- complex-domain cap, the rule that complex cynefin domains force confidence_axis to LOW regardless of rubric.
- pre-ship checklist, the QUALITY-mode artifact, ordered verification steps with owners and effort.
- probe definition, the PROBE-mode artifact, smallest version + success/failure/ambiguity signals.
- learn-list, the DEFER-mode artifact, evidence gaps and how to fill them.
- ship gate, the binary "ship vs don't ship" criterion in QUALITY mode.
- 24-hour first step, the SPEED-mode artifact, the named action the user takes within 24h.
- reversibility challenge, the act of upgrading intake's "costly" to one-way-door based on Second-Order findings.
- time-pressure contradiction, the conflict between mode = DEFER and intake.time_pressure ∈ {now, this-week}.

---

## Completeness Scoring

Confidence-Speed-Quality self-rates 0-10 on placement quality. The rubric:

### 10/10, decisive

- Both axes thresholded with cited evidence (rubric components named, reversibility evidence cited)
- Complex-domain cap evaluated explicitly (even if not triggered)
- Mode named with single-word output
- Mode artifact fully populated:
  - SPEED: 24h step + iteration cadence + 3 exit conditions
  - QUALITY: 8+ checklist items with owners, effort, blocking dependencies, ship gate
  - PROBE: success + failure + ambiguity signals + time-box + cost cap
  - DEFER: 3+ learn-list items + time-to-decision + budget cap + re-decision conditions
- Mode-change conditions specified for at least 3 triggers
- Reversibility challenge explicit (yes / no, with evidence)
- Time-pressure contradiction explicit (yes / no, with resolution if yes)
- No failure-mode self-checks fail

### 7/10, confident

- Both axes thresholded
- Complex-domain cap evaluated
- Mode named
- Mode artifact populated (5+ items where applicable)
- 1-2 mode-change conditions specified
- Reversibility challenge addressed even if briefly

### 4/10, tentative

- Axes thresholded but evidence sparse
- Mode named
- Mode artifact has skeleton but lacks specificity (vague items, no effort estimates)
- No mode-change conditions
- Failure-mode self-checks deferred

### 0/10, broken

- Mode named without artifact, OR
- Mode contradicts inputs (e.g. complex domain + HIGH confidence), OR
- Rubric drift between state.json and this framework

A Confidence-Speed-Quality completeness ≤ 4 caps the overall confidence bucket at MEDIUM regardless of other framework scores.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

By the time Confidence-Speed-Quality runs, the Phase 3 chain has produced:

- cynefin: domain = complicated, rubric +2
- decision-matrix: dual-deploy + drain wins (score 8.2 vs runner-up wrapped legacy 6.7, gap > 5% so Hard Choice doesn't fire), rubric +2
- second-order (4 levels deep): dual-deploy + drain has compounding upside via reinforcing cycle (bridge volume → LP fees → liquidity → bridge volume); no catastrophic downside surfaced; rubric +2
- ladder-of-inference: identified "newer is better" as unjustified leap from iceberg.mental_models, but Decision Matrix has independent justification beyond it; rubric not modified
- ooda-loop: 6-week total cycle, weekly check-ins on success metrics
- hard-choice: skipped (predicate not satisfied; reversibility = costly, not one-way-door; gap > 5%)
- six-hats: not yet run in this chain order; assume run later. For this exercise, assume +2 if 4+ hats agree on directional call

Computed rubric components going into this framework:
- cynefin = complicated: +2
- decision-matrix top ≥ 1.5× second: 8.2 / 6.7 = 1.22, so NOT 1.5×; +0
- second-order no catastrophic downside: +2
- adversary max score ≤ 4: assume yes for this run, +2
- six-hats agreement (run later, included in rubric): +2 expected

Rubric: 2 + 0 + 2 + 2 + 2 = 8/10

Expected by problem statement to trend HIGH (rubric likely 8/10 by the time Confidence-Speed-Quality reads). Use 8 for the exercise.

Posterior: assume 0.78 (HIGH bucket).

Bucket: HIGH (rubric ≥ 8 AND posterior ≥ 0.75).

### Intake state (relevant fields)

```json
{
  "stakeholders": "small-team",
  "time_pressure": "this-month",
  "reversibility": "costly",
  "decision_maker": "you-with-input",
  "success_criteria": "qualitative-signal"
}
```

### Step 1, read inputs

```bash
$ cat $RUN_DIR/state.json | jq '.confidence'
{
  "rubric": 8,
  "posterior": 0.78,
  "bucket": "HIGH"
}

$ cat $RUN_DIR/intake.json | jq '.reversibility'
"costly"

$ grep "Domain:" $RUN_DIR/frameworks/cynefin.md
**Predicate fired:** complicated
```

Read second-order.md:
```
Compounding identified: reinforcing cycle (bridge volume → LP fees → liquidity → bridge volume)
Compounding direction: positive (the cycle amplifies success)
Catastrophic downside: none surfaced at level 4
Reversibility implication: post-ship state is structurally different from pre-ship state due to user behavior shifts after migration; technically reversible at high cost, but full reversal would require multi-month coordination + economic incentives
```

The Second-Order finding raises the reversibility-challenge question. "Costly" fits the technical reversal cost, but the user-behavior compounding makes a full restoration of pre-ship dynamics expensive in time and trust. We will treat as ONE-WAY for the 2x2 (consistent with our threshold rule mapping costly → ONE-WAY) and add a reversibility challenge note.

### Step 2, threshold both axes

```
confidence_axis: rubric = 8, threshold ≥ 7, → HIGH
reversibility_axis: intake = costly, threshold (cheap = REVERSIBLE), → ONE-WAY
```

### Step 3, complex-domain cap

```
cynefin.domain = complicated → no cap fires
```

### Step 4, compute mode

HIGH × ONE-WAY = QUALITY mode.

### Step 5, generate artifact (pre-ship checklist)

The pre-ship checklist for OFTv1 → OFTv2 dual-deploy + drain:

| # | Item | Source | Effort | Blocks |
|---|---|---|---|---|
| 1 | Engage external auditor (LayerZero-experienced) on cross-chain message-encoding diff between OFTv1 and OFTv2; scope includes: lock/burn race conditions, executor logic, cross-chain mempool dynamics. | Six Hats Black + Adversary + Iceberg structures | 1-2 weeks, $25K-$40K | 5, 6, 9, 10 |
| 2 | Deploy OFTv2 to all 4 chains (Ethereum, Avalanche, Arbitrum, Base) on testnet (Sepolia / Fuji / Arb Sepolia / Base Sepolia); run for 7 days under simulated cross-chain load. | Cynefin (complicated) + Reinforcing-Loop | 1 week, $0 | 3, 7 |
| 3 | Mempool-stress simulation: simulate 200 gwei equivalent gas spike on Ethereum simultaneously with cross-chain transfers from Avalanche → Arbitrum; verify settlement completes < 5 min in 95% of trials. | Iceberg structures + Cynefin emergence | 2 days | 7, 11 |
| 4 | Bridge-volume monitoring: deploy production-grade dashboard tracking $TVL across all 4 chains pre-migration baseline; alert at deviation > 15% sustained > 1h. | Reinforcing-Loop + Second-Order | 1 day | 11 |
| 5 | LP-fee monitoring: deploy dashboard tracking LP fees across all 4 chains; confirm read-path unchanged by migration. | Reinforcing-Loop | 4h | 11 |
| 6 | Update all internal documentation: protocol docs, integration guides, partner FAQ, support runbook. | Iceberg patterns (user expectations) | 2 days | 8 |
| 7 | Notify integrators (LPs, partners, indexers) 4 weeks before mainnet drain start; collect acknowledgment list. | Iceberg patterns + SBI (announcement script) | 4 weeks calendar (1 day work) | 11 |
| 8 | Update support team: brief them on migration timeline, common user issues to expect, escalation path if cross-chain transfers stall. | Six Hats Yellow + Iceberg patterns | 4h | 11 |
| 9 | Run external auditor's findings to closure: every finding ≥ severity Medium has either a fix in OFTv2 deployment or a documented rationale. | (item 1) | 1 week | 10 |
| 10 | Internal eng review of OFTv2 deployment scripts + drain mechanism; sign-off from senior eng + protocol lead. | Cynefin (expertise) + Six Hats Blue | 2 days | 11 |
| 11 | Mainnet dual-deploy of OFTv2 alongside OFTv1; OFTv2 in lock state until drain start. | (items 1-10) | 1 day | 12 |
| 12 | Drain start: announce 7-day grace window for users to migrate; LP incentives to accelerate; OFTv1 mint paused, burn allowed. | (item 11) | 7 days | (terminal) |

**Total effort:** approximately 5-6 weeks calendar time; 4-5 person-weeks of internal work; $25K-$40K external auditor budget.

**Critical path:** 1 → 9 → 10 → 11 → 12 (dominated by external audit, then mainnet deploy + drain window).

**Cost cap:** $50K external auditor + monitoring infrastructure.

**Ship gate:**
- All 12 items complete with named owner sign-off.
- Items 1, 9, 10 (audit + internal review) marked must-pass with green signal.
- No new adversary findings ≥ severity 7 introduced during checklist execution. If introduced, halt at the affected item and re-evaluate mode.
- Bridge-volume baseline (item 4) shows no anomalies in the 7 days preceding mainnet deploy.

### Step 6, write output

```markdown
# Confidence vs Speed vs Quality, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T18:45:00Z
**Inputs read:** state.json (confidence: rubric=8, posterior=0.78, bucket=HIGH), intake.json (reversibility=costly, time_pressure=this-month), frameworks/cynefin.md (domain=complicated), frameworks/decision-matrix.md (top: dual-deploy+drain, score 8.2), frameworks/second-order.md (reinforcing cycle compounds, no catastrophic downside), frameworks/six-hats-*.md (5 of 6 hats agree directionally), adversary.jsonl (max severity 6).

[mermaid 2x2 with Problem Position at (0.4, 0.8)]

## Axis values

| Axis | Raw | Threshold | Bucket |
|---|---|---|---|
| Confidence | rubric = 8/10, posterior = 0.78 | rubric ≥ 7 | HIGH |
| Reversibility | costly | cheap = REVERSIBLE | ONE-WAY |

(Complex-domain cap not triggered: cynefin = complicated.)

## Mode: QUALITY

**Justification:** Rubric is 8/10, driven by complicated-domain classification (+2), no catastrophic downside in 4-level Second-Order (+2), low adversary max severity (+2), and Six Hats agreement (+2). Confidence is HIGH. Reversibility is mapped to ONE-WAY: technically the migration can be reversed at high cost, but Second-Order's reinforcing cycle (bridge volume → LP fees → liquidity → bridge volume) means post-ship state is structurally different. Reversal cost is multi-month coordination + economic incentives. Mode is QUALITY: take the time to get it right, then ship.

**Confidence trajectory:** cynefin (+2) + decision-matrix gap < 1.5× (+0) + second-order safe (+2) + adversary safe (+2) + six-hats agreement (+2) = 8/10.

## Reversibility challenge

intake.reversibility = "costly." Second-Order shows compounding via reinforcing cycle. Pure technical reversal of contracts is tractable; restoration of pre-migration economic dynamics is not. Treating as ONE-WAY for execution-mode purposes. The pre-ship checklist explicitly includes monitoring infrastructure so that if the cycle goes wrong post-ship, we detect early enough to halt the drain.

## Pre-Ship Checklist

[12-item table from Step 5 above]

## Ship gate

[ship gate criteria from Step 5]

## What changes the mode

| Trigger | Current | New | Action |
|---|---|---|---|
| External auditor surfaces severity 8+ finding | QUALITY | DEFER or PROBE | Re-evaluate; may need to ship OFTv2 to single chain first as probe |
| Bridge-volume baseline shows pre-migration anomaly | QUALITY | DEFER | Investigate anomaly before adding migration as a variable |
| Rubric drops below 7 (e.g. new info changes a component) | QUALITY | PROBE | Redefine smallest version; ship to Base only first |
| Time-pressure changes to "now" (e.g. security disclosure) | QUALITY | act-first or SPEED | Pre-ship checklist becomes post-ship checklist; accept lower confidence explicitly in the report |

## Open contradictions

None. Time-pressure (this-month) is consistent with QUALITY mode's 5-6 week pre-ship timeline. The external audit is the gating item; if audit lead-time exceeds time-pressure budget, time-pressure must extend.

## What This Means For The Decision

QUALITY mode means the recommendation is "dual-deploy + drain executed against the 12-item pre-ship checklist over 5-6 weeks, gated on external audit and mainnet baseline confirmation." Ship is conditional on every checklist item green. If any item flips red mid-execution, halt and re-evaluate (possibly downgrading to PROBE on a single chain). The pre-ship checklist is the recommendation, not a supplement to it.

## Completeness: 9/10

**Rubric:**
- Both axes thresholded with cited evidence: +2
- Complex-domain cap evaluated explicitly (not triggered, noted): +1
- Mode artifact fully populated (12 items, owners implicit, effort estimates, ship gate): +2
- Mode-change conditions specified (4 triggers): +2
- Reversibility challenge explicit: +2
- Failure-mode self-checks: 1 deferred (we have not yet engaged auditor; effort estimate is a range pending auditor scope)
```

### What the next framework (Minto) inherits

Minto receives:
- mode = QUALITY
- pre-ship checklist (12 items)
- ship gate
- mode-change conditions
- reversibility challenge note
- the recommendation shape: "do X (dual-deploy+drain) but only after pre-ship checklist completes; halt at any red item."

Minto's pyramid will use QUALITY mode to shape:
- Answer: "Yes, via dual-deploy + drain over 6 weeks, with external audit consultation in the first 2 weeks."
- Why arguments: must include the pre-ship checklist as the executable plan, not just supporting evidence.
- Confidence: rubric 8 → posterior 0.78 → bucket HIGH consistent with QUALITY placement.

---

## What This Means For The Decision

Confidence-Speed-Quality is the framework that turns "we are confident" into "we ship in N days with checklist M." Without it, recommendations that read HIGH confidence end up shipping like SPEED (sloppy, fast, reversal-painful) and recommendations that read LOW confidence end up over-deferring (DEFER-FOREVER, no learn-list). The mode is the discipline.

For complicated domains with reinforcing cycles (like the OFTv1 → OFTv2 migration), QUALITY is the regime. The reinforcing cycle amplifies whatever we ship: a clean ship amplifies into compounding upside; a sloppy ship amplifies into systemic failure. The pre-ship checklist is the differentiator between the two outcomes.

The cost of skipping this framework: shipping with the right answer but the wrong execution mode. The benefit of doing it right: every word of the recommendation respects the mode's constraint, and the mode's constraint is grounded in the rubric and the reversibility, not gut.
