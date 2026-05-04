# Cynefin Framework

**Phase:** Decide (runs FIRST in Phase 3) · **Source:** https://untools.co/cynefin-framework

Cynefin sorts problems into five domains based on the relationship between cause and effect. The domain you're in dictates how you decide. Pick the wrong domain, the rest of Phase 3 misroutes. Pick the right one, the next 11 frameworks know which ones to lean into and which to skip.

This is the routing framework. It runs first because it sets the regime for everything else in Phase 3.

---

## Entry Predicate

```
always_run
```

Runs every time Phase 3 fires. There is no condition under which Cynefin is skipped. The output of every other Decide-phase framework reads from `cynefin.domain` to decide whether they're the right tool.

### Inputs

- `intake.json` — the 5-question pre-flight (stakeholders, time pressure, reversibility, decision-maker, success criteria)
- `intake.problem_refined` — the canonical problem statement
- `intake.domain` — auto-detected eng / product / strategy / general
- `$RUN_DIR/frameworks/*` — every Phase 1 (Define) and Phase 2 (Systems) output
- `$RUN_DIR/evidence/*` — research evidence pool

### Outputs

- `$RUN_DIR/frameworks/cynefin.md` — the classification + evidence + routing decisions
- `state.json` `cynefin.domain` field — read by all subsequent Decide-phase frameworks

---

## Operating Principles

These are non-negotiable. Every classification respects all five.

**1. Sort by cause-effect relationship, not by problem size.**

A small problem with unknown cause-effect (a flaky test that only fails on Tuesdays) is complex. A massive problem with known cause-effect (migrate 50M rows to a new schema) is complicated. Domain has nothing to do with how big the work is and everything to do with how predictable the outcome is. Anti-pattern: classifying as "complex" because it feels hard, when it's actually complicated and the team just hasn't talked to an expert yet.

**2. Evidence first, intuition last.**

Cite at least 3 pieces of evidence from prior phases for the classification. If the only evidence is "feels right," the classification is unreliable and routing downstream will fail. Anti-pattern: a single sentence "this looks complex to me" with no grounding. The agent should refuse to commit a domain without evidence.

**3. Disorder is a real answer.**

If the evidence doesn't sort cleanly, the answer is **disorder**, not "let me pick the closest domain." Disorder triggers a re-run of Phase 1 with refined intake. It's not a failure mode. It's a signal that the problem statement is too vague to act on. Anti-pattern: forcing a complex/complicated split when both are equally supported by 50% of the evidence.

**4. Watch for retrospective coherence.**

Complex domains feel obvious in retrospect. After the fact, every causal chain looks linear. Resist the urge to reclassify a complex problem as complicated just because, post-decision, the path looks clear. The test: at the moment you decided, could you have predicted the outcome reliably? If not, it was complex. Anti-pattern: marking a successful complex bet as "complicated, in hindsight."

**5. Route, don't recommend.**

Cynefin's job is to route Phase 3, not to recommend a decision. The recommendation comes from Decision Matrix (or Hard Choice when triggered). Cynefin says "use these frameworks, skip these others, weight these signals." Anti-pattern: writing a one-line "I think we should do X" in the Cynefin output. That's the Decision Matrix's job.

---

## Response Posture

**Tone.** Diagnostic. The agent is sorting evidence, not advocating. Use neutral phrasing: "the evidence supports complex" rather than "I think this is complex."

**Pacing.** Single classification per run. No back-and-forth with the user during this framework. Cynefin reads prior outputs and writes its classification. If the classification is disorder, then it pings the lead via SendMessage to escalate.

**Push depth.** None. Cynefin doesn't ask the user questions. The depth comes from the evidence the framework cites. A Cynefin output with one piece of evidence per domain is shallow. A Cynefin output with 5+ pieces, each tagged by source framework, is deep.

**Where to escalate.** SendMessage to lead when:
- Evidence supports two domains equally (5+ pieces each, flag as disorder)
- Iceberg's "structures" layer revealed a regime change (the system is shifting domains, e.g. from complicated to complex due to new dependencies)
- The classification contradicts a recent prior `/solve` run on a related problem (the user might be missing context)

---

## Anti-Sycophancy Rules

The agent running Cynefin must never write these:
- "This is a fascinating problem with multiple dimensions..." (cut to evidence)
- "There are arguments for both complex and complicated..." (pick one or call disorder)
- "Reasonable minds could differ..." (state the call, name what would change it)
- "It's worth considering whether..." (it's worth doing or it's not)

The agent must always:
- Take a position. State the domain. Cite evidence.
- Name the specific evidence that would change the call.
- Name the failure pattern explicitly: "If we're wrong about this being complex, we'll burn 2 weeks running OODA loops on a problem the senior eng team already knows the answer to."

---

## Pushback Patterns

These show how the agent handles common framing errors when evidence sorts poorly. The agent runs internally, these are self-pushback patterns the framework applies as it analyzes.

**Pattern 1: "It's hard so it must be complex" then check expertise availability**

- Internal evidence: "The team has spent 2 weeks on this and made no progress."
- BAD: "Marking complex, team hasn't found cause-effect."
- GOOD: "The team is stuck. Two paths: (a) complex, the problem genuinely has no knowable cause-effect; (b) complicated, there's an expert in the field who has seen this exact pattern. Before classifying as complex, ping the senior eng or the relevant Slack channel for a 15-min consult. If an expert can sort it in one conversation, it was complicated all along."

**Pattern 2: "Best practice exists somewhere" then check it actually applies**

- Internal evidence: "Stack Overflow has 50 answers about this kind of problem."
- BAD: "Marking simple, best practice is documented."
- GOOD: "Stack Overflow has answers about this category. Are they answers to this specific problem or just adjacent ones? Read the top 3. If they apply directly, it's simple. If they're 80% applicable but the last 20% is non-trivial, it's complicated. Don't conflate Stack Overflow density with cause-effect clarity for this team's context."

**Pattern 3: "Multiple stakeholders disagree" then that's not chaos, that's complicated**

- Internal evidence: "Eng wants A, product wants B, design wants C."
- BAD: "Marking chaotic, too many conflicting voices."
- GOOD: "Stakeholder disagreement is a complicated-domain signal, not a chaotic one. Each stakeholder has a coherent model that produces their answer. The classification depends on whether the underlying technical or business problem has knowable cause-effect, not on how many people are in the room. Run conflict-resolution-diagram first to extract the shared objective, then re-classify. Most stakeholder fights are complicated dressed as chaotic."

**Pattern 4: "We just need to ship" then that's not chaotic, check time pressure separately**

- Internal evidence: "Deadline is Friday, decision pending."
- BAD: "Marking chaotic, no time to analyze."
- GOOD: "Time pressure is its own variable, captured in `intake.time_pressure`. It changes which framework dominates downstream (confidence-speed-quality), but it doesn't change the cause-effect classification. A simple problem with a Friday deadline is still simple. A complex problem with a Friday deadline is still complex but you ship the smallest probe and accept lower confidence. Don't let urgency reclassify the regime."

**Pattern 5: "Everyone has a different answer" then check the question first**

- Internal evidence: "Three engineers gave three different recommendations."
- BAD: "Marking complex, high variance in expert opinion."
- GOOD: "Variance in expert opinion is ambiguous. Could mean: (a) complex, genuinely no knowable answer; (b) complicated with weak experts, the right expert hasn't been asked yet; (c) the question itself is ambiguous and each expert answered a different version. Before classifying, run abstraction-ladder to confirm everyone is answering the same question. Often the disagreement evaporates when the problem is restated precisely."

---

## Method

Cynefin runs as a 7-step procedure. Each step produces a discrete output that feeds the next.

### Step 1, Read all prior framework outputs

```bash
ls $RUN_DIR/frameworks/ | sort
```

Read every `.md` file in `$RUN_DIR/frameworks/` from Phase 1 (Define) and Phase 2 (Systems). The agent must have full context before classifying. Failure mode: classifying based on intake alone, missing systemic signals from iceberg + connection-circles.

### Step 2, Read evidence pool

```bash
ls $RUN_DIR/evidence/ | sort
```

Read every research summary. Especially relevant:
- `evidence/define-prior-art.md`, base rates for similar problems
- `evidence/define-failure-modes.md`, historical complex-vs-complicated splits in this domain
- `evidence/systems-analogous.md`, how analogous systems behaved (a strong signal for complex when analogous systems exhibit emergence)

### Step 3, Score each domain on 5 evidence dimensions

For each of the 5 candidate domains, score 0-3 on these dimensions:

| Dimension | What it measures | Source |
|---|---|---|
| Cause-effect clarity | Can the team predict outcomes? | iceberg.structures, prior-art evidence |
| Best-practice applicability | Does a known recipe solve this? | research evidence, abstraction-ladder |
| Expertise availability | Can an expert sort this in 1 conversation? | intake.stakeholders, prior-art evidence |
| Emergence | Are there feedback loops or non-linear interactions? | connection-circles, balancing/reinforcing-loop |
| Reversibility | Is it cheap to undo? | intake.reversibility |

Score 0 = strong evidence against this domain; 3 = strong evidence for. The domain with the highest sum is the leading candidate.

### Step 4, Apply the formal classification predicates

After scoring, apply these predicates in order. The first one that fires is the classification:

```
chaotic   ⇔ (cause_effect_clarity = 0 ∧ time_pressure = "now" ∧ no_best_practice)
complex   ⇔ (cause_effect_clarity ≤ 1 ∧ emergence ≥ 2)
complicated ⇔ (cause_effect_clarity ≥ 2 ∧ best_practice_applicability ≤ 2 ∧ expertise_available)
simple    ⇔ (cause_effect_clarity = 3 ∧ best_practice_applicability = 3)
disorder  ⇔ (no domain has dimension sum ≥ 8) ∨ (top two domains within 1 point)
```

If multiple predicates would fire, take the most uncertain one. Cynefin biases toward overclassifying as complex/complicated rather than oversimplifying. The cost of treating a complex problem as simple is much higher than treating a simple problem as complex.

### Step 5, Write the classification with evidence

The output structure is mandatory. See Output Schema below. Every classification must list:
- The 5-dimension score table (transparent reasoning)
- 3+ pieces of evidence per dimension (sourced by framework name)
- The predicate that fired
- The runner-up domain and what would tip it

### Step 6, Compute the routing table

Based on the chosen domain, write the Phase 3 routing table that subsequent frameworks consume. See the Decision Hook section.

### Step 7, SendMessage to lead if disorder, or write completion

If the classification is disorder, do not write a routing table. Instead:
- Write a partial output describing what evidence is missing
- SendMessage to lead: `"cynefin: classification disorder, need re-run of Phase 1 with refined intake on <specific gap>"`
- The lead decides whether to halt and re-run or push through with explicit lower confidence

If the classification is one of the four real domains, write the full output and call it complete via TaskUpdate.

---

## Question Patterns

Cynefin runs analytically, not interactively. The agent doesn't ask the user questions during this framework. Instead, the agent asks itself probe questions while reading prior outputs.

### Probe Pattern 1, cause-effect clarity

> "Reading iceberg.structures and connection-circles: can I write a sentence of the form 'if we change X, then Y will happen, with confidence P=0.7+'?"

- Yes, for most candidate actions, cause-effect clarity = 3 (strong simple/complicated signal)
- Yes, but only for some actions, 2 (complicated)
- Only after running 1-2 small experiments, 1 (complex)
- No, even with experiments, 0 (chaotic if also time-pressured, otherwise complex)

Smart-skip: if iceberg or connection-circles wasn't run (Phase 2 incomplete), this probe can't fire. Mark "insufficient evidence" and downgrade the dimension to 0-1 by default.

### Probe Pattern 2, best-practice applicability

> "Are there 3+ documented references (Stack Overflow, blog posts, prior commits, internal RFCs) that describe a workflow which directly solves this exact problem class?"

- Yes, and they apply 90%+ to this case, best-practice = 3 (simple)
- Yes, but they need 30-50% adaptation, 2 (complicated)
- References exist but disagree, 1 (complicated trending complex)
- No documented best practice, 0 (complex or chaotic)

Red flag: "Stack Overflow has tons of answers" without checking specificity. Generic answers about a category are not best practice for this case.

### Probe Pattern 3, expertise availability

> "Is there a person we can call who has seen this exact pattern 5+ times and can sort it in a 15-min conversation?"

- Yes, and they're available, expertise = 3 (definitely complicated, possibly simple if the expert says "this is just X")
- Yes, but they're unavailable, 2 (still complicated, just blocked on access)
- Possibly, but we'd have to find them, 1 (complicated to complex)
- No expert exists, 0 (complex or chaotic)

Smart-skip: if `intake.stakeholders = single-decider` and the user is the expert in the domain, default to 2 unless evidence contradicts.

### Probe Pattern 4, emergence

> "Did connection-circles detect ≥ 2 feedback cycles? Did iceberg's mental-models layer reveal beliefs that interact non-linearly?"

- 2+ reinforcing cycles, or 1 reinforcing + 1 balancing, emergence = 3 (strongly complex)
- 1 cycle detected, 2 (complex)
- No cycles, but multiple interacting variables, 1 (complicated trending complex)
- No cycles, isolated variables, 0 (simple/complicated)

Red flag: classifying as "complex" when no cycles were detected. Emergence requires feedback. Without feedback, complexity is just complicatedness with poor visibility.

### Probe Pattern 5, reversibility

> "If the action fails, what's the cost to reverse it? (intake.reversibility)"

- cheap, +1 confidence to act under any classification
- costly, no modifier
- one-way-door, -1 confidence; if also LOW expertise, escalate to Hard Choice

This dimension doesn't change the classification but modifies the routing table downstream.

---

## Forcing Exemplars

When writing the classification output, every claim should have a forcing-version (specific, evidence-grounded) instead of a softened-version (hedged, vague).

### Exemplar 1, Stating the classification

SOFTENED (avoid):
> "Based on the analysis, this problem appears to fall into the complex domain, though it shares some characteristics with complicated problems."

FORCING (aim for):
> "Domain: complex. Cause-effect clarity = 1 (iceberg's structures layer shows a feedback loop between billing latency and user retention; we can't predict the second-order effect without running it). Emergence = 3 (reinforcing-loop detected: lower retention then less data then worse predictions then lower retention). Runner-up: complicated, score 6. The classification flips to complicated only if we find a senior eng who has seen this exact retention-data feedback loop before; we have not."

### Exemplar 2, Citing evidence

SOFTENED (avoid):
> "Evidence from the systems analysis suggests this is not a simple problem."

FORCING (aim for):
> "Evidence against simple:
> - iceberg.events shows incidents with no consistent reproducer (3 of last 5 incidents had different root causes)
> - connection-circles detected 2 cycles involving billing then retention then engagement
> - prior-art research found 2 case studies of similar billing-retention loops, both required 3+ months of probing experiments to resolve
> No best-practice recipe exists for this configuration."

### Exemplar 3, Naming the runner-up

SOFTENED (avoid):
> "We considered other domains but ultimately concluded complex was most appropriate."

FORCING (aim for):
> "Runner-up: complicated. The case for complicated: the team has 10 years of billing-system experience, and the problem has a finite number of moving parts. The case against complicated: retention dynamics are emergent and depend on user behavior we don't fully observe. To flip the classification: have the senior eng team review for 2 hours and confirm whether they can predict the second-order effect on retention without running a probe. If yes, complicated. If no (which is our current state), complex stands."

### Exemplar 4, Routing the next frameworks

SOFTENED (avoid):
> "Complex domains benefit from iterative approaches and small experiments."

FORCING (aim for):
> "Routing for complex:
> - Decision Matrix: still run but explicitly weight 'reversibility' criterion at ≥ 8 (we want options we can probe and reverse)
> - Six Hats: run, but Black Hat dominates (this domain has high failure surface area)
> - OODA: PRIMARY decision mode for this run. Cycle time target: 1 week (one O then O then D then A loop per week)
> - Hard Choice: run only if Decision Matrix's top two are within 5% AND reversibility = one-way-door (currently reversibility = costly, so probably skip)
> - Confidence-Speed-Quality: PROBE mode. Ship the smallest experiment that produces signal. Don't optimize for quality on the first pass."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/cynefin.md` follows this structure exactly. Every section is required.

### Section A, Header

```markdown
# Cynefin Classification, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** <comma-separated list of prior framework files + evidence files>
```

### Section B, Quadrant chart (mermaid)

```mermaid
quadrantChart
  title Cynefin Classification
  x-axis Knowable --> Unknowable
  y-axis Stable --> Unstable
  quadrant-1 Complex
  quadrant-2 Chaotic
  quadrant-3 Simple
  quadrant-4 Complicated
  Problem Position: [<x>, <y>]
  Runner-up Position: [<x>, <y>]
```

X-axis: 0 = fully knowable cause-effect, 1 = fully unknowable.
Y-axis: 0 = stable system (no emergence), 1 = unstable (high emergence).

The Problem Position is plotted from the dimension scores:
- x = 1 - (cause_effect_clarity / 3)
- y = emergence / 3

### Section C, Dimension score table

```markdown
| Dimension | Score (0-3) | Evidence | Source framework(s) |
|---|---|---|---|
| Cause-effect clarity | <N> | <bullet list of 3+ pieces> | <list> |
| Best-practice applicability | <N> | <evidence> | <list> |
| Expertise availability | <N> | <evidence> | <list> |
| Emergence | <N> | <evidence> | <list> |
| Reversibility | <N> | <intake.reversibility> | intake |
```

Every row must have 3+ pieces of evidence. Rows with fewer pieces are reduced to score 0 by default (insufficient grounding).

### Section D, Domain classification

```markdown
## Classification: <DOMAIN>

**Predicate fired:** <which formal predicate from Step 4 matched>

**Score sum:**
- Simple: <N>/15
- Complicated: <N>/15
- Complex: <N>/15
- Chaotic: <N>/15

**Runner-up:** <domain> (sum: <N>)

**What would flip the classification:** <specific evidence shape that would tip the call to runner-up>
```

### Section E, Routing table

```markdown
## Phase 3 Routing

| Framework | Run? | Weight / Mode | Reason |
|---|---|---|---|
| Eisenhower | <yes/no> | <normal / urgent-only> | <reason> |
| Impact-Effort | <yes/no> | <normal / dominance-check-only> | <reason> |
| Decision Matrix | <yes/no> | <normal / weight-reversibility-high / skip> | <reason> |
| Second-Order | <yes/no> | <normal / 4-levels-deep> | <reason> |
| Ladder of Inference | <yes/no> | <normal> | <reason> |
| OODA | <yes/no> | <normal / PRIMARY> | <reason> |
| Hard Choice | <yes/no> | <triggered-by-Decision-Matrix-tie / always> | <reason> |
| Six Hats | <yes/no> | <normal / Black-dominant> | <reason> |
| Confidence-Speed-Quality | <yes/no> | <SPEED / QUALITY / PROBE / DEFER> | <reason> |
| SBI | <yes/no> | <only-if-interpersonal-conflict> | <reason> |
| Minto | <yes/no> | <always> | runs last as synthesis |
```

This routing table is the single most important output of Cynefin. The decider teammate reads this table at the start of Phase 3 and dispatches frameworks accordingly.

### Section F, Cross-skill triggers (if any)

```markdown
## Cross-Skill Triggers

- iceberg.structures had bug-shape AND domain = simple OR complicated, handoff to /investigate (already fired in Phase 2 if so)
- domain = chaotic AND time_pressure = now, SendMessage to lead immediately ("we are in chaotic-domain emergency mode, recommend pausing /solve and acting first via OODA single-cycle")
- domain = disorder, SendMessage to lead, halt phase 3, re-run intake
```

### Section G, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentences synthesizing what the classification implies for the recommendation. Specific, decision-actionable. No hedging.>
```

### Section H, Completeness Score

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- Cited <K>/5 dimensions with 3+ evidence pieces: +<N>
- Predicate cleanly fired (no ambiguity): +<N>
- Routing table specifies weights/modes for all 12 frameworks: +<N>
- Runner-up identified and flip-condition stated: +<N>
- Cross-skill triggers checked: +<N>
```

---

## Decision Hook

Cynefin's output drives all subsequent Decide-phase frameworks. Specifically:

### Per-domain framework dominance

| Domain | Dominant frameworks | Frameworks to skip or de-emphasize |
|---|---|---|
| Simple | Decision Matrix, Eisenhower | Six Hats Black, Hard Choice, OODA primary mode (degenerate to single cycle) |
| Complicated | Decision Matrix, Six Hats, Second-Order, Ladder of Inference | OODA primary mode |
| Complex | OODA (primary), Six Hats Black, Confidence-Speed-Quality (PROBE) | Decision Matrix as decisive (still run but as advisory only), Hard Choice unless Decision Matrix tie |
| Chaotic | Confidence-Speed-Quality (act-first mode) | Most frameworks deprioritized; act, then re-run /solve once stabilized |
| Disorder | None, Phase 3 halts | All Decide-phase frameworks |

### Confidence rubric impact

- Cynefin = simple OR complicated, +2 to overall confidence rubric
- Cynefin = complex, +0 (rubric earns through OODA experiments instead)
- Cynefin = chaotic, -2 (acting under low confidence is the regime, but the rubric reflects that)
- Cynefin = disorder, no decision (lead halts)

### Override conditions

Cynefin does not override other frameworks. It routes them. The only way Cynefin "wins" against another framework is when Decision Matrix produces a confident answer that the regime says we cannot act on confidently (e.g. complex domain + Decision Matrix high-confidence pick, recommendation downgrades to PROBE mode despite the matrix score).

---

## Cross-Framework Triggers

These conditions in the Cynefin output force changes elsewhere in /solve:

### Triggers fired by domain

- chaotic, SendMessage to lead: pause /solve and act first. The recommendation in this domain is "do something stabilizing now and re-run /solve afterward."
- disorder, SendMessage to lead: halt Phase 3, re-run Phase 1 with refined intake. The lead AskUserQuestions the user with the specific gap.
- complex, mark `state.PROBE_MODE = true`. Confidence-Speed-Quality picks up this flag.
- simple AND time_pressure = "now", mark `state.FAST_TRACK = true`. The decider can collapse Decide-phase to Eisenhower + Decision Matrix only and ship the recommendation immediately.

### Triggers fired by classification confidence

- Score sum for top domain ≤ 7, low confidence in classification, flag in Dissent section of final report
- Top two domains within 1 point, call it disorder regardless of which has the higher sum

### Triggers fired by runner-up

- If runner-up is complicated and an expert is identifiable, spawn a research task: "consult <expert> for 15 min on this exact problem; report back whether they can sort it." If they can, the classification flips and Phase 3 reroutes.

---

## Failure Modes

Cynefin can mislead in five distinct ways. The framework checks for each before completing.

### Failure Mode 1, Overclassifying as complex due to size

Trap: Big problem feels overwhelming, gets marked complex, team runs OODA loops on something a senior eng could have sorted in 30 min.

Manifestation in output: dimension scores show "expertise available = 0" with weak evidence (e.g. "no one on the team knows this"); the team didn't ask anyone outside the team.

Check: before committing complex, force the agent to answer: "Have we asked one expert outside the immediate team in the last 48 hours? If no, expertise score should be ≥ 1, not 0, until we've asked."

Recovery: add a research task for "consult external expert on this problem class" to Phase 3 and re-run Cynefin in 24 hours.

### Failure Mode 2, Underclassifying complex as complicated due to expert overconfidence

Trap: A senior eng says "I've seen this 100 times", expertise = 3, complicated. But the senior eng has seen the shape of this problem, not this exact instance, and the emergent dynamics are different.

Manifestation in output: expertise score = 3, emergence score = 0-1, but connection-circles flagged feedback loops the expert didn't account for in their assessment.

Check: when expertise = 3, require the expert to specifically address the emergent dynamics flagged by connection-circles. If they hand-wave them ("that won't matter"), drop expertise score to 2 and re-evaluate.

Recovery: classify as complicated-trending-complex. Run OODA as a backup, weight Six Hats Black hat more heavily, and budget 1 week for an experimental probe before committing the architecture.

### Failure Mode 3, Disorder masquerading as complicated

Trap: Mixed evidence gets averaged into "complicated" because it's the safe middle. But the real classification is disorder, the problem isn't well-defined enough for any classification.

Manifestation in output: complicated wins by 1-2 points, evidence is sparse (1-2 pieces per dimension), runner-up is complex with similar evidence quality.

Check: if both top domains have < 3 evidence pieces in any dimension, classify as disorder regardless of sum. The team needs more grounding before deciding regime.

Recovery: SendMessage to lead, halt phase 3, re-run intake.

### Failure Mode 4, Treating chaotic as the answer when it's just urgent

Trap: Time pressure gets misread as no-cause-effect. "We have to ship by Friday", chaotic, act first. But the cause-effect was knowable; the team just didn't analyze it.

Manifestation in output: chaotic classification with cause_effect_clarity = 0 but the prior frameworks (especially issue-tree, ishikawa) actually mapped clear causes. The agent prioritized intake.time_pressure over framework evidence.

Check: chaotic classification requires cause_effect_clarity = 0 from prior framework evidence, NOT from time pressure. Time pressure modifies confidence-speed-quality mode, not Cynefin classification.

Recovery: reclassify as the next-best domain (likely complicated) and apply confidence-speed-quality SPEED mode for the urgency.

### Failure Mode 5, Routing table mismatched to domain

Trap: Cynefin classifies as complex but writes a routing table that runs Decision Matrix as decisive. Downstream confusion: the decider teammate sees "complex" but acts on Decision Matrix top option directly.

Manifestation in output: routing table column "Weight / Mode" doesn't match the domain. E.g. complex domain with Decision Matrix marked "normal" instead of "advisory only."

Check: before completing, the agent runs a self-validation against the per-domain dominance table in this file. Any mismatch is auto-corrected.

Recovery: rewrite the routing table to match domain dominance rules above.

---

## Jargon Glossary

Cynefin uses domain-specific vocabulary. First use of any of these terms in the output should include a one-line gloss.

- cause-effect, the predictability of outcomes given inputs; the central axis Cynefin sorts on.
- emergence, system behavior that arises from interactions and is not present in the parts; characteristic of complex domains.
- retrospective coherence, a complex problem looks linear after the fact, even though the path was not predictable in advance.
- best practice, a documented, repeatable workflow that solves a class of simple problems with high confidence.
- good practice, a documented workflow that needs adaptation per case; characteristic of complicated domains.
- emergent practice, a workflow that develops through small experiments and feedback; characteristic of complex domains.
- novel practice, a workflow created in real-time when no precedent exists; characteristic of chaotic domains.
- probe, a small experiment designed to surface signal about a complex system before committing the architecture.
- sense-making, the process of categorizing what kind of problem you're in before deciding how to solve it.
- disorder, the state of not yet having classified; not a stable domain but a signal to gather more evidence.
- regime change, when a system shifts from one Cynefin domain to another (e.g. complicated to complex due to new dependencies). Iceberg's structures layer often surfaces these.
- dominance (table column), when one option dominates another on every criterion; relevant for simple-domain decision-matrix runs.
- equifinality, multiple paths produce the same outcome; characteristic of complex domains where the recommendation should specify the smallest viable probe rather than the optimal path.

---

## Completeness Scoring

Cynefin self-rates 0-10 on classification quality. The rubric:

### 10/10, Decisive
- All 5 dimensions scored with 3+ evidence pieces each (15+ pieces total)
- One predicate fires cleanly with sum ≥ 12
- Runner-up identified with sum ≤ 8 (clear winner)
- Flip-condition stated specifically (what would change the call)
- Routing table fully specified for all 12 Decide-phase frameworks
- Cross-skill triggers explicitly checked
- No failure-mode self-checks fail

### 7/10, Confident
- All 5 dimensions scored, most with 3+ evidence
- Predicate fires with sum ≥ 9
- Runner-up gap is 3-5 points
- Flip-condition stated but generic
- Routing table covers ≥ 10 frameworks
- 1-2 failure-mode self-checks deferred ("would need more data to verify")

### 4/10, Tentative
- 3-4 dimensions scored, some with sparse evidence
- Predicate fires with sum 6-8
- Runner-up within 2 points
- Routing table is generic (matches domain template without per-run customization)
- Multiple failure-mode self-checks deferred

### 0/10, Disorder
- Insufficient evidence to classify
- Top two domains within 1 point
- < 3 evidence pieces in any dimension

The completeness score appears in the framework output and feeds the overall Confidence rubric (Step 9 of SKILL.md). A Cynefin completeness ≤ 4 caps the overall confidence bucket at MEDIUM regardless of other framework scores.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This is the canonical example used across all framework files for continuity. The same problem walks through Cynefin, Decision Matrix, Six Hats, Minto in sequence.

### Intake state

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

### Prior framework outputs (summary)

- abstraction-ladder, target rung is "decide migration approach" (between "should we use LayerZero at all" and "what's the migration script syntax")
- first-principles, atomic truths = bridges must allow value transfer, gas costs must be predictable, users must not lose funds
- issue-tree, 4 major branches: technical migration path, user-side coordination, audit requirements, operational runbook
- ishikawa, confirmed causes if migration fails = incompatible message encoding, lock/burn race conditions, frozen funds during migration
- inversion-define, failure paths include partial migration, double-spending across chains, UX confusion during transition window
- zwicky-box, archetypes include "big-bang single-cutover," "dual-deploy + drain," "wrapped legacy," "ship OFTv2 as separate token + voluntary migration"
- conflict-resolution-diagram, N/A (single-team decision, no stakeholder conflict)
- productive-thinking, forged solutions = dual-deploy + drain, wrapped legacy
- iceberg.events, OFTv1 had 3 minor incidents in last 6 months (gas spikes, no actual fund loss)
- iceberg.patterns, users assume bridge transfers settle in < 30s; deviations cause support tickets
- iceberg.structures, the cross-chain mempool dynamics interact with LayerZero's executor logic in non-trivial ways
- iceberg.mental_models, team believes "newer is better"; unverified
- connection-circles, 1 reinforcing cycle detected, bridge volume then LP fees then liquidity then bridge volume; 1 balancing cycle, gas costs then migration eagerness then cross-chain trades then gas costs
- balancing-loop, balancing loop has ~2 day delay
- reinforcing-loop, reinforcing loop has multi-week doubling time

### Step 1-2: Read prior outputs and evidence

Agent reads all 13 framework files plus 8 evidence files. Key evidence pieces:

- LayerZero docs explicitly recommend dual-deploy + drain for high-TVL migrations (best-practice density: high)
- 3 prior protocol migrations (Stargate, Radiant, Ethena) all used dual-deploy + drain (prior-art density: high)
- Internal eng team has migrated 1 prior LayerZero deployment (smaller, $500K TVL, single-chain)
- Reinforcing cycle from connection-circles indicates the bridge has compounding effects we'd be disrupting
- iceberg.structures flagged non-trivial cross-chain mempool dynamics

### Step 3: Score each dimension

| Dimension | Score | Evidence |
|---|---|---|
| Cause-effect clarity | 2 | LayerZero docs + 3 prior migrations + internal experience give us good predictability for the migration mechanics. The mempool dynamics flagged by iceberg.structures introduce uncertainty in execution timing. |
| Best-practice applicability | 3 | LayerZero officially documents dual-deploy + drain for $1M+ TVL. 3 prior protocols used this exact recipe. The recipe applies 90%+ here. |
| Expertise availability | 2 | Internal team has done one LZ migration. LayerZero support is responsive within 24h. We have not consulted any external auditor specifically on cross-chain migration timing. |
| Emergence | 2 | One reinforcing cycle (bridge volume then LP fees then liquidity) directly affected by migration. One balancing cycle (gas then migration eagerness) introduces feedback we don't fully control. Migration during a gas spike would behave differently than during low-gas. |
| Reversibility | 1 (intake = costly) | Once OFTv2 is deployed and OFTv1 drained, reversing requires re-deploying OFTv1 and convincing users to migrate back. Costly. |

Sums:
- Simple: cause_effect=2 + best_practice=3 + emergence=0 (would need 0 cycles) + expertise=2 = strong on simple dimensions but emergence kills it
- Complicated: cause_effect=2 + best_practice=2 + expertise=2 + emergence=1 = sum 7
- Complex: cause_effect=1 + emergence=2 + expertise=1 = sum 4
- Chaotic: 0 across the board (we have time, we have docs)

### Step 4: Apply predicates

```
chaotic: cause_effect_clarity = 0? NO. Predicate fails.
complex: cause_effect_clarity ≤ 1 ∧ emergence ≥ 2?
         cause_effect_clarity = 2 (above threshold), predicate fails
complicated: cause_effect_clarity ≥ 2 ∧ best_practice_applicability ≤ 2 ∧ expertise_available?
         cause_effect_clarity = 2 ✓
         best_practice_applicability = 3 (above threshold for complicated)
         check simple instead
simple: cause_effect_clarity = 3 ∧ best_practice_applicability = 3?
         cause_effect_clarity = 2 (below threshold), predicate fails
disorder: no domain has sum ≥ 8 OR top two within 1 point?
         Complicated sum = 7, second-place is split between simple and complex (both 4-5)
         Top score is 7, threshold is 8, predicate marginally fires
```

This is interesting, the dimensions don't cleanly fire any predicate. Best-practice = 3 is too high for pure complicated, but emergence = 2 is too high for simple, and cause_effect = 2 is too high for complex.

### Step 4b: Tiebreaker

Apply the rule from Operating Principle 4: "bias toward overclassifying as complex/complicated rather than oversimplifying."

Between simple and complicated, complicated wins because emergence = 2 disqualifies simple.

Between complicated and complex, complicated wins because cause_effect_clarity = 2 disqualifies complex.

Classification: complicated (with emergence concerns flagged)

### Step 5: Write output

```markdown
# Cynefin Classification, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T17:30:00Z
**Inputs read:** abstraction-ladder.md, first-principles.md, issue-tree.md, ishikawa.md, inversion-define.md, zwicky-box.md, productive-thinking.md, iceberg.md, connection-circles.md, balancing-loop.md, reinforcing-loop.md, evidence/*

[mermaid quadrant chart]

## Dimension Scores

| Dimension | Score | Evidence | Source |
|---|---|---|---|
| Cause-effect clarity | 2 | LayerZero docs document migration mechanics. 3 prior migrations (Stargate, Radiant, Ethena) used dual-deploy + drain. Mempool dynamics flagged in iceberg.structures introduce execution-timing uncertainty. | LZ docs, prior-art research, iceberg.md |
| Best-practice applicability | 3 | LayerZero officially recommends dual-deploy + drain for $1M+ TVL. 3 prior protocol migrations followed this exact recipe with successful outcomes. Recipe applies 90%+ to our case. | LZ docs, prior-art research |
| Expertise availability | 2 | Internal team migrated 1 smaller LZ deployment (Q3 2024). LayerZero support responsive within 24h. We have not consulted external auditor on cross-chain migration timing specifically. | intake.json, internal records |
| Emergence | 2 | Reinforcing cycle (bridge volume then LP fees then liquidity) directly affected. Balancing cycle (gas then migration eagerness) introduces partial feedback we cannot fully control. Migration during gas spike behaves differently than baseline. | connection-circles.md, balancing-loop.md, reinforcing-loop.md |
| Reversibility | 1 | Migration is costly to reverse. Re-deploying OFTv1 and convincing users to migrate back is multi-week. | intake.json |

## Classification: complicated

**Predicate fired:** complicated (modified by tiebreaker: cause_effect_clarity prevents complex; emergence prevents simple)

**Score sum:**
- Simple: 5/15 (emergence kills it)
- Complicated: 9/15
- Complex: 7/15
- Chaotic: 0/15

**Runner-up:** complex (sum: 7)

**What would flip the classification to complex:** if a 2-week probe of OFTv2 on a low-TVL testnet deployment surfaces unexpected mempool dynamics that contradict LayerZero's documented behavior, we have evidence of emergence dominating and should re-classify.

## Phase 3 Routing

| Framework | Run? | Weight / Mode | Reason |
|---|---|---|---|
| Eisenhower | yes | normal | time_pressure = "this-month" makes urgency-importance triage useful |
| Impact-Effort | yes | normal | We have multiple archetypes from Zwicky; need to plot impact/effort on each |
| Decision Matrix | yes | normal | Complicated domain, Decision Matrix is the dominant framework. Weight reversibility ≥ 7. |
| Second-Order | yes | 4-levels-deep | Reinforcing cycle from connection-circles means second-order effects compound. Push to 4 levels. |
| Ladder of Inference | yes | normal | Worth checking team's "newer is better" mental model from iceberg.mental_models |
| OODA | yes | secondary | Run OODA with weekly cycle on the chosen migration path; it's not primary because we have docs |
| Hard Choice | conditional | only-if-Decision-Matrix-tie | Reversibility = costly (not one-way-door), so Hard Choice doesn't auto-fire |
| Six Hats | yes | normal | All 6 hats run; Black weighted standard (not dominant) |
| Confidence-Speed-Quality | yes | QUALITY mode | Reversibility = costly + complicated domain, optimize for quality over speed |
| SBI | no | N/A | No interpersonal conflict signals |
| Minto | yes | always | Final synthesis |

Skipped frameworks: SBI (no signal triggering it).

## Cross-Skill Triggers

- iceberg.structures had bug-shape? NO (mempool dynamics are uncertainty, not a named bug). No /investigate handoff.
- iceberg.mental_models = pre-product? NO. No /office-hours handoff.
- domain = simple/complicated AND produces architecture? YES, flag for /plan-eng-review at end of run.
- domain = chaotic? NO.
- domain = disorder? NO.

State updates:
- `state.PLAN_ENG_REVIEW_AT_END = true` (architecture decision incoming)
- `state.PROBE_MODE = false`
- `state.FAST_TRACK = false`

## What This Means For The Decision

This is a complicated-domain decision with emergence concerns. Decision Matrix dominates the call. Weight reversibility heavily because the migration is costly to reverse, and weight emergence-resilience (does this archetype handle the mempool dynamics gracefully?) as a secondary criterion. Second-order analysis must go 4 levels deep because the reinforcing cycle in connection-circles will amplify whatever we choose. Recommend Confidence-Speed-Quality QUALITY mode: take the time to get this right rather than ship the smallest version.

If runner-up flips to complex (probe on testnet contradicts docs), reroute Phase 3 to OODA-primary mode and recommendation downgrades to PROBE.

## Completeness: 8/10

**Rubric:**
- All 5 dimensions scored with 3+ evidence pieces each: +2
- Predicate fires with tiebreaker (not perfectly clean): +1
- Routing table specifies modes for all 12 frameworks: +2
- Runner-up identified, flip-condition specific: +2
- Cross-skill triggers checked: +1
- Failure-mode self-checks: 1 deferred (we haven't asked external auditor; could revise expertise score after consult)
```

This output then feeds the decider teammate, which uses the routing table to dispatch the remaining 11 Decide-phase frameworks.

### What the next framework (Eisenhower) inherits

Eisenhower receives:
- Cynefin domain = complicated
- Routing weight = "normal"
- Reversibility = costly (Eisenhower will weight "important" higher than "urgent")
- The list of candidate options from Zwicky (big-bang, dual-deploy+drain, wrapped legacy, separate token)

Eisenhower then plots each option on its 2×2 and outputs a triage table.

---

## What This Means For The Decision

Cynefin is the routing layer. Without it, Phase 3 is a 12-framework dump where every output gets equal weight. With it, the decision is shaped by the regime: complex problems get OODA, complicated problems get Decision Matrix, simple problems get fast-tracked. Skipping Cynefin (or doing it badly) is the most common cause of confident-wrong recommendations from /solve.

When Cynefin says complex, the recommendation should always include "smallest probe" and "OODA cycle time." When it says complicated, the recommendation should always include "expert-validated path" and "second-order analysis." When it says simple, the recommendation can ship same-day. When it says chaotic, the recommendation is a stabilizing action, not a strategic decision. When it says disorder, the recommendation is "don't decide yet."

The cost of skipping Cynefin: confident decisions in the wrong regime. The benefit of doing it right: every other Decide-phase framework knows its job.
