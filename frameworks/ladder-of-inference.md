# Ladder of Inference

**Phase:** Decide · **Source:** https://untools.co/ladder-of-inference

The Ladder of Inference traces a recommendation backward from action to raw data. Seven rungs, climbed unconsciously by every team. Skip a rung, the recommendation looks obvious but rests on borrowed confidence. Make the rungs explicit, the unjustified leap shows up. The adversary subagent attacks that leap.

This framework runs after Decision Matrix produces a top recommendation. It does not produce its own recommendation. It audits the reasoning chain that led to the matrix winner. The output is a 7-rung trace plus a list of flagged leaps plus the adversary's attack vector.

---

## Entry Predicate

```
always_run
```

Runs every Phase 3, after Decision Matrix completes. There is no skip condition. The point of the ladder is to expose unjustified confidence, and unjustified confidence shows up in every recommendation regardless of domain.

### Inputs

- `$RUN_DIR/frameworks/decision-matrix.md` — the top recommendation and its score breakdown
- `$RUN_DIR/frameworks/decision-matrix.md::evidence` — the evidence cells used to score each option
- `$RUN_DIR/intake.json` — the original problem framing and stakeholder context
- `$RUN_DIR/frameworks/iceberg.md::mental_models` — the team's beliefs about how the world works
- `$RUN_DIR/evidence/*` — the research evidence pool

### Outputs

- `$RUN_DIR/frameworks/ladder-of-inference.md` — the 7-rung trace, flagged leaps, attack vectors
- `state.json` `ladder.weakest_leap` — the rung-pair with the worst leap, consumed by the adversary
- `state.json` `ladder.attack_vector` — a one-sentence attack the adversary uses against the recommendation

---

## Operating Principles

These five rules govern every ladder run. Each one corrects a specific reasoning failure.

**1. Climb backward, not forward.**

Start at Rung 7 (the action) and trace down to Rung 1 (the raw data). If you climb forward from data to action, you naturalize the team's selection bias because you anchor on the data they already chose to look at. Climbing backward forces the question "where did this come from?" at every rung, which surfaces what got dropped on the way up. Anti-pattern: writing the rungs in 1 through 7 order and ending with a confident action that traces cleanly back to the cherry-picked data the team started with.

**2. Every rung gets explicit content.**

A rung labeled "the team interpreted this to mean X" is not enough. The rung needs the actual interpretation written out, in the team's voice, with the specific framing used. Vague rungs hide leaps. The leap from Rung 3 (Interpreted Meaning) to Rung 4 (Assumptions) only shows up when both rungs have specific text. Anti-pattern: skipping a rung because "it follows from the prior rung" — that's the leap you're trying to expose.

**3. Selected data is half the story; ignored data is the other half.**

Rung 2 (Selected Data) is two columns: what the team focused on, and what the team had access to but did not focus on. The ignored column is where the adversary lives. The most dangerous leap in any ladder is "we picked these 3 facts and ignored these 5 because they didn't fit." Anti-pattern: writing only the selected data and treating the ignored data as outside the framework's scope.

**4. Beliefs are not assumptions.**

Rung 4 (Assumptions) and Rung 6 (Beliefs) are different. Assumptions are the leaps made on this specific problem to reach this specific conclusion. Beliefs are the durable generalizations that this conclusion will reinforce going forward. Confusing them muddles the ladder and weakens the attack vector. Anti-pattern: writing "we believe X" at Rung 4 and "we assume Y" at Rung 6, swapping the layers and producing a meaningless trace.

**5. Flag the weakest leap, not all leaps.**

Every rung-to-rung transition involves some leap. The job is to find the worst one, not to flag every one as suspect. The adversary needs a single vector to attack. Listing 6 weak leaps gives the adversary nothing to grab. Listing 1 worst leap with the next 2 ranked behind it tells the adversary where to start the assault. Anti-pattern: marking every leap "needs more evidence" and producing a ladder where everything is equally weak (which means the framework is shallow, not the reasoning).

---

## Response Posture

**Tone.** Forensic. The agent is reconstructing reasoning, not advocating. Phrasing should be third-person observational: "the team's Rung 4 assumption is X" rather than "I think the assumption is X."

**Pacing.** Single trace per run. The ladder runs once on the Decision Matrix output. No back-and-forth with the user during the framework. If the trace surfaces a leap that needs user clarification (e.g. "is this assumption actually what the team believes?"), the agent flags it for the lead via SendMessage rather than asking directly.

**Push depth.** The ladder is shallow if any rung has fewer than 2 explicit pieces. Each rung must name specific evidence (Rung 1), specific items selected and ignored (Rung 2), specific interpretive language (Rung 3), specific assumptions stated as falsifiable claims (Rung 4), specific conclusions (Rung 5), specific beliefs (Rung 6), specific actions (Rung 7). A ladder where Rung 4 says "we assume the migration will work" without naming the cause-effect mechanism is a ladder that hasn't done the work.

**Where to escalate.** SendMessage to lead when:
- A rung has zero evidence after exhausting prior framework outputs (the framework upstream is broken, not the ladder)
- Rung 4 assumptions directly contradict Rung 6 beliefs (the team is unstable, recommendation is high-risk)
- The weakest leap is between Rung 1 and Rung 2 (the team selected data based on a prior conclusion, the entire reasoning chain is contaminated)

---

## Anti-Sycophancy Rules

The agent running Ladder of Inference must never write these:

- "The team's reasoning is generally sound, with some areas for improvement..." (state the leaps, name them)
- "There are some assumptions worth examining..." (which assumptions, on which rung, contradicting which evidence)
- "The conclusion seems reasonable given the data..." (does the conclusion follow from the data, yes or no, with the specific leap named)
- "Multiple paths could reach this recommendation..." (the team took one path, trace it; alternative paths are not relevant to this audit)
- "It's worth noting that some considerations may have been overlooked..." (name what got dropped at Rung 2 and why it matters)

The agent must always:

- State the weakest leap with the rung pair (e.g. "Rung 4 to Rung 5: the assumption 'newer is better' is unverified and produces the conclusion 'migrate now' without independent grounding").
- Name the specific evidence that would close the leap (e.g. "a 2-week probe on testnet would convert this assumption into Rung 1 data").
- Name the failure pattern explicitly: "If the weakest leap is left unattacked, the recommendation lands with confidence the team has not actually earned, and post-decision review will produce hindsight regret."

---

## Pushback Patterns

These are self-pushback patterns the framework applies as it analyzes the recommendation. The agent is not talking to the user; it is interrogating its own draft trace.

**Pattern 1: "Rung 1 has lots of evidence" then check what got dropped at Rung 2**

- Internal evidence: "Rung 1 lists 12 facts."
- BAD: "Rung 1 is well-grounded, the recommendation is data-driven, ladder looks healthy."
- GOOD: "Rung 1 has 12 facts. Rung 2 selected 4 of them. List the 8 that got dropped. Were any of them dropped because they contradicted the emerging conclusion? If yes, the leap from Rung 1 to Rung 2 is a confirmation-bias gate, not a data-selection step. The adversary attacks this leap by re-introducing one of the dropped facts and showing the conclusion no longer follows."

**Pattern 2: "Rung 4 assumption sounds reasonable" then check if it's testable**

- Internal evidence: "Rung 4 says 'our team can execute a clean migration.'"
- BAD: "Reasonable assumption given the team's track record, mark validated, move on."
- GOOD: "Restate the assumption as a falsifiable claim with a probability estimate: 'the team can execute the migration without a rollback within 3 weeks at probability 0.8'. If the team won't commit to a number, the assumption is vibes, not reasoning. The leap from Rung 4 to Rung 5 is a vibes-to-conclusion jump. Adversary attacks: 'name the prior migration where this team hit the 3-week target on the first try.'"

**Pattern 3: "Rung 6 belief is implicit" then make it explicit**

- Internal evidence: "Rung 6 isn't filled in; the agent says 'no explicit belief change.'"
- BAD: "No belief change, ladder is complete at Rung 5."
- GOOD: "Every conclusion reinforces a belief, even if implicit. If the recommendation is 'migrate,' the belief reinforced is 'we should always upgrade when the vendor releases a new version.' If that belief is wrong, the next 5 vendor releases will trigger 5 more migrations under the same flawed reasoning. Make Rung 6 explicit. If the team disowns the belief, the conclusion at Rung 5 needs a different justification."

**Pattern 4: "Rung 5 conclusion matches Decision Matrix top score" then check the matrix evidence**

- Internal evidence: "Decision Matrix scored option A at 8.2, conclusion is 'do A,' ladder seems consistent."
- BAD: "Matrix and ladder agree, recommendation validated, complete."
- GOOD: "The matrix score is a quantitative summary; the ladder is a reasoning audit. They can agree on the answer and disagree on the why. Trace the matrix's evidence cells back through the ladder. Did the matrix score 'reversibility' as 7 because Rung 1 has data on reversibility, or because Rung 4 assumed the reversibility was acceptable? If the latter, the matrix's 8.2 score is borrowing confidence from an unverified assumption. The ladder should flag this and the adversary should attack it."

**Pattern 5: "All seven rungs are filled in" then check the leaps not the rungs**

- Internal evidence: "Every rung has content, ladder is complete."
- BAD: "Complete ladder, completeness 9/10."
- GOOD: "The ladder isn't 7 rungs, it's 6 transitions. Score each transition 0-3 for grounding. A ladder with 7 well-written rungs and 6 weakly-justified transitions is a ladder that documents the reasoning without auditing it. Mark the transitions, find the worst, and write the attack vector. Completeness scores the transitions, not the rungs."

---

## Method

Ladder of Inference runs as an 8-step procedure. Each step produces one rung of the trace plus a transition score.

### Step 1, Read the recommendation and its supporting evidence

```bash
cat $RUN_DIR/frameworks/decision-matrix.md
```

Extract:
- The top recommendation (Rung 7 source)
- The matrix score breakdown (Rung 5 source)
- The evidence cells per criterion (Rung 1 source)

If Decision Matrix didn't run, the ladder cannot run. SendMessage to lead and abort.

### Step 2, Read the systems-phase outputs for mental models

```bash
cat $RUN_DIR/frameworks/iceberg.md
```

Extract `iceberg.mental_models` — the team's stated and inferred beliefs about how the system works. These feed Rung 6 (Beliefs).

If iceberg didn't run, mental models default to an empty set. The Rung 6 entries are inferred from Rung 5 and flagged "inferred, not stated."

### Step 3, Trace Rung 7 (Action) backward to Rung 1 (Observable Data)

The trace runs in reverse. Start at the bottom of the table and fill upward.

| Rung | Question to answer |
|---|---|
| 7 (Action) | What does the recommendation actually do? |
| 6 (Beliefs) | What general belief does this conclusion reinforce? |
| 5 (Conclusions) | What did the team decide? |
| 4 (Assumptions) | What did the team need to assume to reach the conclusion? |
| 3 (Interpreted Meaning) | What did the team take the data to mean? |
| 2 (Selected Data) | Which facts did the team focus on? Which did they ignore? |
| 1 (Observable Data) | What raw facts and evidence exist? |

Each rung gets explicit text. No placeholders.

### Step 4, Score each transition 0-3 for grounding

For each rung pair (1→2, 2→3, 3→4, 4→5, 5→6, 6→7), score the transition:
- 3 = the next rung follows directly from the prior rung with cited evidence
- 2 = the next rung follows from the prior rung plus 1 named assumption
- 1 = the next rung follows from the prior rung plus 1 unverified assumption
- 0 = the next rung does not follow from the prior rung; a leap exists

The transition scores are the framework's primary diagnostic. A ladder with one 0-score transition is healthier than a ladder with three 1-score transitions.

### Step 5, Identify the weakest leap

The weakest leap is the lowest-scored transition. If multiple transitions tie at 0 or 1, pick the one with the highest downstream amplification: a weak Rung 2→3 leap contaminates 4 downstream rungs, while a weak Rung 6→7 leap only affects 1.

Tie-breaker rule: lower-rung leaps win (more amplification). A 1-scored Rung 2→3 transition is the weakest leap even if Rung 5→6 is also 1-scored.

### Step 6, Name the dropped data at Rung 2

This is its own step because it's the most-frequently-skipped part of the framework. Open a list of facts the team had access to but did not select. Sources:
- Evidence files in `$RUN_DIR/evidence/` not cited by Decision Matrix
- Iceberg layers (events, patterns, structures, mental_models) not pulled into the matrix
- Inversion-define failure paths not addressed by the recommendation

Every dropped fact is a candidate for the adversary's attack. Rank the dropped facts by "would re-introducing this fact change the conclusion?" The top-ranked dropped fact pairs with the weakest leap to form the attack vector.

### Step 7, Write the attack vector

The attack vector is a single sentence the adversary will use to challenge the recommendation. Format:

> "The recommendation rests on the assumption [Rung 4 content], which is unverified because [name the missing evidence], and the team ignored [Rung 2 dropped data] which contradicts the assumption."

This sentence becomes `state.ladder.attack_vector`. The adversary reads it and writes a multi-paragraph dissent.

### Step 8, Write the output

Compose the full ladder output (see Output Schema). The output goes to `$RUN_DIR/frameworks/ladder-of-inference.md` and the state fields are updated.

---

## Probe Patterns

The ladder doesn't ask the user questions. It asks itself probe questions while reading prior outputs.

### Probe Pattern 1, Rung 1 Observable Data

> "Reading decision-matrix.md and evidence/*: list the raw facts that informed the matrix scores. Each fact must be falsifiable, sourced, and dateable."

- Strong Rung 1: 6+ facts, each with a source citation and a date
- Medium Rung 1: 3-5 facts, mostly sourced
- Weak Rung 1: 1-2 facts, or facts without sources

Smart-skip: never. If Rung 1 is weak, the ladder is fragile. Document the weakness and proceed; don't pad Rung 1 with inferred facts.

### Probe Pattern 2, Rung 2 Selected Data

> "Of the facts at Rung 1, which made it into the matrix's evidence cells? Of the facts at Rung 1, which did the matrix not cite? What's in the evidence pool that wasn't surfaced as a Rung 1 fact at all?"

- Strong Rung 2: explicit selected list + explicit ignored list, both with citations
- Medium Rung 2: selected list with citations, ignored list named but not cited
- Weak Rung 2: selected list only, ignored treated as out-of-scope

Red flag: Rung 2 with 0 ignored items. Either the team has perfect information (rare) or the agent didn't look hard enough.

### Probe Pattern 3, Rung 3 Interpreted Meaning

> "What did the team take the selected data to mean? Write the interpretation as a sentence the team would endorse."

- Strong Rung 3: a single sentence in the team's framing, with the interpretive verb visible (e.g. "the team interprets the LayerZero docs to indicate that dual-deploy + drain is the standard recipe for high-TVL migrations")
- Medium Rung 3: an interpretation, but the team's framing is replaced by neutral framing
- Weak Rung 3: no interpretive language; Rung 3 looks like a copy of Rung 2

Red flag: Rung 3 reads like an objective summary. Interpretation is subjective by design. If it's missing, the team is treating their interpretation as data.

### Probe Pattern 4, Rung 4 Assumptions

> "What does the team need to be true, on top of the interpreted meaning, to reach the conclusion? List as falsifiable claims."

- Strong Rung 4: 2-3 falsifiable claims, each with a probability estimate
- Medium Rung 4: 1-2 claims, no probabilities
- Weak Rung 4: vague language like "we assume things will work out"

Red flag: Rung 4 with implicit assumptions. Assumptions that aren't named are assumptions that can't be tested.

### Probe Pattern 5, Rung 5 Conclusions

> "What did the team conclude? Match the conclusion to the Decision Matrix top recommendation."

- Strong Rung 5: matches matrix top recommendation exactly, with the same option name and the same scope
- Medium Rung 5: matches the top recommendation but with a different scope (e.g. matrix says "migrate," ladder says "migrate next quarter")
- Weak Rung 5: doesn't match the matrix top; one of the framework outputs is wrong

Red flag: ladder Rung 5 differs from matrix top. The ladder is auditing the matrix, so they should agree on the conclusion. If they don't, one of the prior frameworks misread its source.

### Probe Pattern 6, Rung 6 Beliefs

> "What general belief does this conclusion reinforce? Will future similar decisions be made by reflex on this belief?"

- Strong Rung 6: a stated belief from iceberg.mental_models that the conclusion reinforces (e.g. "newer is better" reinforced by deciding to migrate)
- Medium Rung 6: an inferred belief, flagged as inferred
- Weak Rung 6: blank or "no belief change"

Red flag: Rung 6 left blank. Conclusions always reinforce something. The framework's job is to surface what.

### Probe Pattern 7, Rung 7 Action

> "What's the concrete action the recommendation produces? What's the first step?"

- Strong Rung 7: a specific action with a date, owner, and reversibility class
- Medium Rung 7: a specific action without a date or owner
- Weak Rung 7: a vague action ("plan the migration")

Smart-skip: never. Rung 7 is the easiest rung to fill but the one that exposes the most when filled badly.

---

## Forcing Exemplars

Every rung has a softened version (vague, hedged) and a forcing version (specific, falsifiable, evidence-grounded).

### Exemplar 1, Stating Rung 1 (Observable Data)

SOFTENED (avoid):
> "Rung 1: The team has access to LayerZero documentation and prior migration case studies."

FORCING (aim for):
> "Rung 1, Observable Data:
> - LayerZero v2 docs at https://docs.layerzero.network/v2 describe dual-deploy + drain for $1M+ TVL migrations (accessed 2026-04-15)
> - Stargate migration retrospective (Q2 2024) describes a 3-week dual-deploy phase with 0 fund loss
> - Radiant migration retrospective (Q3 2024) describes a 2-week dual-deploy phase with 1 incident (gas spike during drain, 4h support spike)
> - Ethena migration retrospective (Q4 2024) describes a 4-week phase, 0 incidents
> - Internal records: team migrated $500K TVL OFTv1 deployment in Q3 2024, single chain, took 1 week
> - LayerZero support response time average 18h (sample of 12 tickets, Q1 2026)"

### Exemplar 2, Stating Rung 2 (Selected Data and Ignored Data)

SOFTENED (avoid):
> "Rung 2: The team focused on documentation and prior migrations."

FORCING (aim for):
> "Rung 2, Selected Data:
> SELECTED (cited in matrix):
> - LayerZero docs (Rung 1 item 1)
> - 3 prior protocol migrations (Rung 1 items 2-4)
> - Internal $500K migration experience (Rung 1 item 5)
>
> IGNORED (in evidence pool, not cited in matrix):
> - Radiant migration had a 48h support-ticket spike during the drain phase. The matrix scored 'user impact' as 6 without referencing this. Re-introducing this drops user-impact score to 4 and changes the matrix top option.
> - LayerZero v2 docs explicitly warn against migration during high-gas periods. Current gas conditions on Ethereum are 60+ gwei. Matrix did not score 'timing risk.'
> - Internal $500K migration was single-chain. Current case is 4-chain. The 4-chain dimension is a category change the matrix scored as a quantity change."

### Exemplar 3, Stating Rung 4 (Assumptions)

SOFTENED (avoid):
> "Rung 4: The team assumes the migration will go smoothly and the docs are accurate."

FORCING (aim for):
> "Rung 4, Assumptions (each as a falsifiable claim with probability):
> - A1: 'LayerZero v2 docs accurately describe the dual-deploy + drain workflow for our 4-chain configuration.' (P=0.85, source: docs density + 3 prior protocols)
> - A2: 'Our team can execute a 4-chain migration in 3 weeks based on the 1-chain $500K experience.' (P=0.5, source: internal records, but 4-chain is unverified)
> - A3: 'The mempool dynamics flagged by iceberg.structures are within the variance covered by the prior 3 protocol migrations.' (P=0.6, source: inferred, no direct evidence)
> - A4: 'Gas conditions during the migration window will not spike to >100 gwei.' (P=0.7, source: 30-day gas trend)
>
> Weakest assumption: A2 (P=0.5). The 1-chain experience does not transfer cleanly to 4 chains because each chain has independent mempool, executor, and validator dynamics."

### Exemplar 4, Stating the Weakest Leap

SOFTENED (avoid):
> "There may be some weakness in the assumption layer that should be examined further."

FORCING (aim for):
> "Weakest leap: Rung 4 → Rung 5.
> - Rung 4 contains assumption A2: 'Our team can execute a 4-chain migration in 3 weeks based on the 1-chain $500K experience.' P=0.5.
> - Rung 5 conclusion: 'Migrate now using dual-deploy + drain.'
> - The leap is treating a 0.5-probability assumption as load-bearing. The Decision Matrix scored 'execution risk' at 6, which implicitly priced in P=0.7+. The matrix is over-confident by 0.2 probability units on this dimension.
> - Transition score: 1 (the conclusion follows from the assumption + 1 unverified probability inflation).
> - The adversary attacks this leap with: 'Name the prior 4-chain migration this team has executed. There is none. The 1-chain experience is a category-distinct case. The 3-week estimate is a guess, not a forecast.'"

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/ladder-of-inference.md` follows this structure exactly.

### Section A, Header

```markdown
# Ladder of Inference, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** decision-matrix.md, iceberg.md, intake.json, evidence/*
**Top recommendation audited:** <option name from Decision Matrix>
**Matrix score:** <N>/10
```

### Section B, The 7-Rung Trace

```markdown
## Trace (top to bottom, action to data)

### Rung 7, Action
<concrete action, owner, date, reversibility class>

### Rung 6, Beliefs
<general belief reinforced by this conclusion; sourced from iceberg.mental_models or inferred>

### Rung 5, Conclusions
<the team's conclusion; matches Decision Matrix top recommendation>

### Rung 4, Assumptions
<2-3 falsifiable claims with probability estimates>

### Rung 3, Interpreted Meaning
<the team's interpretation in their own framing>

### Rung 2, Selected Data
**Selected:**
- <fact>
- <fact>

**Ignored:**
- <fact>, [why it matters]
- <fact>, [why it matters]

### Rung 1, Observable Data
- <fact with source>
- <fact with source>
- <fact with source>
```

### Section C, Transition Scores

```markdown
## Transitions

| From | To | Score (0-3) | Justification |
|---|---|---|---|
| Rung 1 (Data) | Rung 2 (Selected) | <N> | <which facts dropped, why> |
| Rung 2 (Selected) | Rung 3 (Meaning) | <N> | <interpretive language used> |
| Rung 3 (Meaning) | Rung 4 (Assumptions) | <N> | <what beliefs added to make meaning coherent> |
| Rung 4 (Assumptions) | Rung 5 (Conclusion) | <N> | <how assumptions produced the conclusion> |
| Rung 5 (Conclusion) | Rung 6 (Beliefs) | <N> | <which belief the conclusion reinforces> |
| Rung 6 (Beliefs) | Rung 7 (Action) | <N> | <how the belief produced the action> |

**Total transition score:** <sum>/18
```

### Section D, Weakest Leap

```markdown
## Weakest Leap

**Leap:** Rung <N> → Rung <M>
**Score:** <0 or 1>
**Content:** <the rung pair text>
**Why this is the weakest:** <amplification factor + grounding deficit>
```

### Section E, Attack Vector

```markdown
## Attack Vector (consumed by adversary)

> <single sentence of the form: "The recommendation rests on the assumption [Rung 4 content], which is unverified because [missing evidence], and the team ignored [Rung 2 dropped data] which contradicts the assumption.">

**State updates:**
- `ladder.weakest_leap` = "Rung <N> → Rung <M>"
- `ladder.attack_vector` = "<sentence>"
- `ladder.attack_target` = "<Rung 4 assumption being attacked>"
```

### Section F, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentences synthesizing the ladder's diagnostic. State whether the recommendation should land as-is, land with the assumption flagged in Dissent, or be downgraded pending evidence on the weakest leap.>
```

### Section G, Completeness

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- All 7 rungs filled with explicit text: +<N>
- All 6 transitions scored with justification: +<N>
- Weakest leap identified with rung pair + content: +<N>
- Attack vector written as a single sentence: +<N>
- Rung 2 ignored list has 2+ items with "why it matters" notes: +<N>
- Rung 4 assumptions written as falsifiable claims with probability estimates: +<N>
```

---

## Decision Hook

The ladder feeds two downstream consumers.

### Consumer 1, the adversary subagent

The adversary reads `state.ladder.attack_vector` and writes a multi-paragraph dissent in the final report. The dissent attacks the weakest leap by:
1. Restating the unverified assumption
2. Citing the dropped data from Rung 2
3. Showing how re-introducing the dropped data flips the conclusion
4. Naming the specific experiment or evidence that would resolve the leap

If the dissent is compelling (adversary scores ≥ 7 on Black Hat severity), the recommendation downgrades from HIGH to MEDIUM confidence in the final synthesis.

### Consumer 2, the Six Hats Blue Hat (process critique)

Six Hats Blue Hat consumes the ladder's transition scores. A ladder with average transition score < 2 indicates the recommendation's reasoning chain is shallow, and Blue Hat flags this in the process critique. Blue Hat is the only hat that consumes ladder output directly.

### Confidence rubric impact

- All transitions scored 2 or 3: +1 to overall confidence rubric
- One transition scored 0 or 1: 0 modifier (recommendation lands with attack vector flagged)
- Multiple transitions scored 0 or 1: -1 to confidence rubric
- Rung 1 has < 3 facts: -1 to confidence rubric (the data layer is too thin to support a recommendation)

### Override conditions

The ladder does not override the recommendation. It audits it. The recommendation only changes if:
- The adversary's dissent is adopted by the lead during synthesis (lead-controlled)
- The weakest leap reveals a Rung 1 evidence gap that, when filled, changes the matrix scores

---

## Cross-Framework Triggers

Conditions in the ladder output that force changes elsewhere in /solve.

### Trigger 1, Adversary escalation

If the weakest leap is between Rungs 1 and 2 (the team selected data based on a prior conclusion), escalate the adversary from "challenge weakest leap" to "challenge entire reasoning chain." The dissent doubles in scope and the recommendation defaults to MEDIUM confidence regardless of matrix score.

### Trigger 2, Iceberg re-run

If Rung 6 reveals a belief that contradicts iceberg.mental_models (the team's stated belief is X, but the conclusion reinforces belief Y), trigger an iceberg re-run with the contradiction flagged. The systems-thinker re-evaluates the mental_models layer. This is rare but high-value when it fires.

### Trigger 3, Decision Matrix re-score

If Rung 2 dropped data includes evidence that would change a matrix criterion score by 2+ points, trigger a Decision Matrix re-score. The matrix re-runs with the dropped evidence included and the ladder re-runs on the new top recommendation.

### Trigger 4, Confidence-Speed-Quality downgrade

If the ladder's total transition score is < 10/18, trigger Confidence-Speed-Quality to PROBE mode. The recommendation downgrades from "ship" to "probe and re-evaluate."

---

## Failure Modes

The ladder can mislead in five distinct ways.

### Failure Mode 1, Rung 4 stuffed with hindsight rationalizations

Trap: After Rung 5 is filled, the agent walks back to Rung 4 and writes assumptions that perfectly support the conclusion. This produces a clean ladder that audits nothing.

Manifestation: every assumption at Rung 4 has P ≥ 0.8 and they all flow neatly to the conclusion. No assumption fails. No leap exists.

Check: before completing, the agent flags any Rung 4 assumption with P ≥ 0.85 and asks "what evidence supports this probability?" If the answer is "the conclusion," the assumption is hindsight-rationalization. Drop the probability to 0.5 and re-trace.

Recovery: rewrite Rung 4 from Rung 3 forward, not from Rung 5 backward. Rung 3 is the team's interpretation; Rung 4 should be assumptions added on top of that interpretation, not assumptions retro-fitted to support a conclusion.

### Failure Mode 2, Rung 2 ignored data is empty

Trap: The agent writes Rung 2's "selected" list but skips the "ignored" list because "the team didn't drop anything important." This is the most common ladder failure.

Manifestation: Rung 2 has a selected list with 3-5 items and an empty or single-item ignored list.

Check: compare the count of items in Rung 1 (data) to the count in Rung 2 (selected). If the counts match, the agent treated Rung 1 = Rung 2, which means Rung 2 didn't do its work. The ignored list must contain at least (Rung 1 count - Rung 2 selected count) items.

Recovery: revisit `evidence/*` and iceberg layers. List every fact the team had access to. Subtract the selected list. The remainder is the ignored list. If the remainder is empty, the team had perfect information (rare) or the evidence pool is shallow (common). In the latter case, flag the framework upstream.

### Failure Mode 3, Weakest leap is mis-identified

Trap: The agent identifies a leap that's clearly weak (e.g. a Rung 5 → Rung 6 leap with 0 grounding) but ignores a more amplifying leap upstream (e.g. a Rung 2 → Rung 3 leap with 1 grounding).

Manifestation: the weakest leap is at the top of the ladder (closer to Rung 7) but the lower-rung leaps have similar or worse scores.

Check: when scoring the weakest leap, apply the tie-breaker rule: lower-rung leaps win. A 1-scored Rung 2→3 transition is the weakest leap even if Rung 5→6 is also 1-scored, because Rung 2→3 amplifies through 4 more rungs.

Recovery: re-rank by amplification. The weakest leap is the lowest-rung leap with a score ≤ 1.

### Failure Mode 4, Attack vector is too generic

Trap: The agent writes an attack vector like "the team's reasoning has assumptions that should be tested." This is a non-attack. The adversary cannot use it.

Manifestation: the attack vector lacks specifics. Doesn't name the assumption (Rung 4 content). Doesn't name the dropped data (Rung 2 ignored). Doesn't show how re-introducing the data flips the conclusion.

Check: read the attack vector aloud. Does it contain a specific assumption? A specific dropped fact? A specific consequence? If not, it's generic.

Recovery: rewrite using the template: "The recommendation rests on the assumption [name it], which is unverified because [name the missing evidence], and the team ignored [name the dropped fact] which contradicts the assumption." Force the names.

### Failure Mode 5, Ladder duplicates the Decision Matrix instead of auditing it

Trap: The ladder's Rung 5 conclusion matches the matrix top, the Rung 4 assumptions match the matrix's criterion-weighting rationale, and the Rung 1 data matches the matrix's evidence cells. The ladder isn't auditing; it's restating.

Manifestation: the transition scores are all 2 or 3 because the ladder rebuilt the matrix's reasoning without questioning it. No leap is flagged.

Check: a healthy ladder finds at least one transition with a score of 0 or 1. If every transition is 2+, the ladder didn't probe hard enough. The agent must answer: "what would convince me one of these transitions is weak?" If the answer is "nothing," the ladder is a mirror, not an audit.

Recovery: re-score Rung 4 assumptions with adversarial probability estimates. Re-list Rung 2 ignored data with adversarial dropped facts. Re-evaluate transitions.

---

## Jargon Glossary

- rung — one of the 7 layers in the ladder, from Observable Data (1) to Action (7)
- leap — the transition between two adjacent rungs; the place where unjustified confidence is added
- weakest leap — the rung-pair with the lowest grounding score; the adversary's primary attack target
- attack vector — a single-sentence challenge the adversary uses against the recommendation, derived from the weakest leap
- selected data — the subset of observable data the team focused on in their reasoning
- ignored data — the subset of observable data the team had access to but did not focus on; the most-frequently-skipped part of the framework
- interpreted meaning — what the team took the selected data to mean, in the team's framing
- assumption — a belief added on top of the interpretation to make it coherent with the conclusion
- conclusion — the recommendation produced by the chain of reasoning
- belief — a durable generalization that the conclusion reinforces and that will affect future similar decisions
- action — the concrete first step that implements the recommendation
- transition score — a 0-3 grounding rating for a rung pair
- amplification — the number of downstream rungs affected by a leap; lower-rung leaps amplify more
- hindsight rationalization — assumptions written backward from the conclusion, producing a clean ladder that audits nothing
- adversarial probability — a probability estimate written from the perspective of "what would defeat this assumption?" rather than "what supports it?"

---

## Completeness Scoring

The ladder self-rates 0-10 on audit quality.

### 10/10, Decisive

- All 7 rungs filled with explicit text (no placeholders, no vague language)
- All 6 transitions scored with justification
- Weakest leap identified with rung pair + content + amplification justification
- Attack vector written as a single sentence with named assumption + named dropped fact + named consequence
- Rung 2 ignored list has 3+ items with "why it matters" notes
- Rung 4 assumptions written as falsifiable claims with probability estimates between 0.3 and 0.9
- Rung 1 has 6+ facts with sources
- One transition is scored 0 or 1 (the ladder found a real leap, not a mirror)

### 7/10, Confident

- All 7 rungs filled, most with explicit text
- All 6 transitions scored
- Weakest leap identified with rung pair
- Attack vector written but lacks one of (named assumption, named dropped fact, named consequence)
- Rung 2 ignored list has 1-2 items
- Rung 4 has 1-2 assumptions with probability estimates
- Rung 1 has 4-5 facts

### 4/10, Tentative

- 5-6 rungs filled, 1-2 with vague language
- 3-4 transitions scored
- Weakest leap identified by rung name only
- Attack vector is generic
- Rung 2 ignored list is empty or has 1 item without justification
- Rung 4 has assumptions without probabilities
- Rung 1 has 2-3 facts

### 0/10, Mirror

- The ladder restates the Decision Matrix without auditing
- All transitions scored 2 or 3 (no leap flagged)
- Rung 2 selected list = Rung 1 data list (no dropped data)
- Rung 4 assumptions all P ≥ 0.85 (hindsight rationalization)

A ladder completeness ≤ 4 caps the overall confidence bucket at MEDIUM regardless of other framework scores. The ladder is a load-bearing audit; if it can't audit, the recommendation can't claim HIGH.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This continues the canonical OFTv2 example from cynefin.md. Cynefin classified this as complicated. Decision Matrix produced top recommendation: dual-deploy + drain (score 8.2), runner-up: wrapped legacy (score 6.7).

### Inputs read

- `decision-matrix.md` — top: dual-deploy + drain, score 8.2
- `decision-matrix.md::evidence` — criterion scores for reversibility (7), execution-risk (6), user-impact (6), gas-cost (8), audit-cost (7)
- `iceberg.md::mental_models` — "newer is better" (unverified)
- `intake.json` — reversibility = costly, time_pressure = this-month
- `evidence/*` — LayerZero docs, 3 prior protocol migrations, internal $500K migration record

### Step 1-2, Read recommendation and mental models

Top recommendation: dual-deploy + drain. Score 8.2.

Iceberg mental_models entry: "newer is better" — flagged unverified by systems-thinker.

### Step 3, Trace backward from Rung 7 to Rung 1

**Rung 7, Action:**
> Start the migration. Deploy OFTv2 contracts on all 4 chains in parallel (Ethereum, Avalanche, Arbitrum, Base). Open the drain phase 1 week after dual-deploy. Owner: eng team lead. Date: 2026-05-15. Reversibility class: costly (re-deploying OFTv1 would take 2 weeks and require user re-migration).

**Rung 6, Beliefs:**
> "We should always upgrade to newer LayerZero versions on a 6-month cadence." Reinforced by deciding to migrate now. Sourced from iceberg.mental_models "newer is better," extended by the agent to a release-cadence belief.

**Rung 5, Conclusions:**
> Migrate now using dual-deploy + drain. Matches Decision Matrix top recommendation exactly.

**Rung 4, Assumptions:**
> A1: "LayerZero v2 docs accurately describe the dual-deploy + drain workflow for our 4-chain configuration." (P=0.85, source: docs density + 3 prior protocols)
> A2: "Our team can execute a 4-chain migration in 3 weeks based on the 1-chain $500K experience." (P=0.5, source: internal records, but 4-chain is unverified)
> A3: "The mempool dynamics flagged by iceberg.structures are within the variance covered by the prior 3 protocol migrations." (P=0.6, source: inferred, no direct evidence)
> A4: "Newer is better." (P=unverified, source: iceberg.mental_models, never tested)

**Rung 3, Interpreted Meaning:**
> The team interprets the LayerZero docs and 3 prior migrations to mean that "this is well-traveled territory; the recipe is documented and battle-tested." The team treats the documentation density as evidence of low execution risk.

**Rung 2, Selected Data:**
> SELECTED:
> - LayerZero v2 docs (docs density signal)
> - 3 prior protocol migrations (Stargate, Radiant, Ethena, all dual-deploy + drain)
> - Internal $500K migration experience
>
> IGNORED:
> - Radiant migration had a 48h support spike during the drain phase. The matrix scored "user impact" at 6 without referencing this spike. Re-introducing this fact drops user-impact to 4 and changes the matrix top option.
> - Internal $500K migration was single-chain, current case is 4-chain. The 4-chain dimension is a category change the matrix scored as a quantity change.
> - LayerZero v2 docs explicitly warn against migration during high-gas periods. Current Ethereum gas conditions are 60+ gwei (above the doc's recommended threshold of 40 gwei).

**Rung 1, Observable Data:**
> - LayerZero v2 docs at https://docs.layerzero.network/v2 describe dual-deploy + drain for $1M+ TVL migrations (accessed 2026-04-15)
> - Stargate migration retrospective (Q2 2024): 3-week dual-deploy phase, 0 fund loss, 0 support spike
> - Radiant migration retrospective (Q3 2024): 2-week dual-deploy phase, 1 incident (gas spike during drain, 48h support spike, 0 fund loss)
> - Ethena migration retrospective (Q4 2024): 4-week phase, 0 incidents
> - Internal records: team migrated $500K TVL OFTv1 deployment in Q3 2024, single chain, took 1 week
> - LayerZero support response time average 18h (sample of 12 tickets, Q1 2026)
> - Current Ethereum gas: 60+ gwei (sample of last 7 days)
> - Iceberg.structures flagged non-trivial cross-chain mempool dynamics

### Step 4, Score transitions

| From | To | Score | Justification |
|---|---|---|---|
| Rung 1 (Data) | Rung 2 (Selected) | 1 | The team dropped 3 important facts at Rung 2: Radiant's 48h support spike, the 1-chain to 4-chain category change, the high-gas warning. The selection bias gate is partially closed. |
| Rung 2 (Selected) | Rung 3 (Meaning) | 2 | Given the selected data, the interpretation "well-traveled territory" follows. But the interpretation ignores the variance in prior migrations (Radiant's spike, Ethena's 4-week duration). |
| Rung 3 (Meaning) | Rung 4 (Assumptions) | 1 | Assumption A2 (P=0.5) doesn't follow from the meaning. The 1-chain experience is a category-distinct base rate. The leap is treating 1-chain history as 4-chain forecast. |
| Rung 4 (Assumptions) | Rung 5 (Conclusion) | 1 | The conclusion "migrate now" follows from A1+A3 cleanly but borrows confidence from A2 (P=0.5) and A4 (unverified). The matrix scored execution-risk at 6, implying P=0.7+, which is over-confident by 0.2 probability units. |
| Rung 5 (Conclusion) | Rung 6 (Beliefs) | 0 | The belief "newer is better, always upgrade on 6-month cadence" is an unverified generalization that the conclusion will reinforce. No grounding for the belief; it's the unverified mental_model from iceberg, never tested. |
| Rung 6 (Beliefs) | Rung 7 (Action) | 2 | Given the belief, the action follows. The action's reversibility class is correctly noted as costly. |

**Total transition score: 7/18**

### Step 5, Identify the weakest leap

Tied at score 0: Rung 5 → Rung 6.
Tied at score 1: Rung 1 → Rung 2, Rung 3 → Rung 4, Rung 4 → Rung 5.

Apply tie-breaker (lower-rung leaps win on amplification): the weakest leap is Rung 1 → Rung 2 (lowest rung at score 1) over Rung 5 → Rung 6 (high rung at score 0).

Re-evaluate: a 0-scored leap is technically worse than a 1-scored leap regardless of amplification. The rule "lower-rung leaps win" applies to ties at the same score. Rung 5 → Rung 6 at 0 is the weakest leap by absolute score.

But the Rung 5 → Rung 6 leap is downstream of Rung 4 → Rung 5, which sets up the conclusion. The adversary attacks the conclusion's grounding, not the belief's reinforcement. Re-rank: prioritize the leap that drives the conclusion. That's Rung 4 → Rung 5.

**Weakest leap: Rung 4 → Rung 5 (score 1).** The conclusion borrows confidence from A2 (P=0.5, 1-chain to 4-chain category change) and A4 (unverified "newer is better").

Note: Rung 1 → Rung 2 is the second-weakest (score 1, dropped 3 important facts). The adversary's secondary attack vector goes there.

### Step 6, Name the dropped data

Already named at Rung 2:
1. Radiant 48h support spike (would drop user-impact score from 6 to 4)
2. 1-chain to 4-chain category change (would drop execution-risk score from 6 to 4)
3. Current high-gas conditions (would add a new criterion: timing-risk, scored at 3 — bad)

Re-introducing all 3 dropped facts to the matrix:
- User-impact: 6 → 4
- Execution-risk: 6 → 4
- New criterion timing-risk: 3 (weight 0.15)
- New top recommendation score: 8.2 → 6.4
- Wrapped legacy score (current runner-up): 6.7 (unchanged)
- New matrix top: wrapped legacy

Re-introducing dropped data flips the recommendation. This is the adversary's primary attack.

### Step 7, Write the attack vector

> "The recommendation to do dual-deploy + drain rests on assumption A2 ('our team can execute a 4-chain migration in 3 weeks based on the 1-chain $500K experience,' P=0.5), which is unverified because the 1-chain experience is a category-distinct base rate, and the team ignored 3 facts at Rung 2 (Radiant's 48h support spike, the 1-chain to 4-chain category change, the current high-gas conditions) which collectively flip the matrix top from dual-deploy + drain to wrapped legacy."

State updates:
- `ladder.weakest_leap = "Rung 4 → Rung 5"`
- `ladder.attack_vector = "<sentence above>"`
- `ladder.attack_target = "A2: 4-chain execution risk based on 1-chain experience"`

### Step 8, Write the output

Output file at `$RUN_DIR/frameworks/ladder-of-inference.md` contains all sections. Highlights:

**What This Means For The Decision:**
The Decision Matrix top recommendation (dual-deploy + drain, score 8.2) borrows confidence from a 0.5-probability assumption (A2) and 3 ignored facts at Rung 2. The adversary will attack on these grounds. If the adversary's dissent is adopted, the recommendation downgrades to MEDIUM confidence and the lead may pivot to wrapped legacy. The lead should weight the adversary's attack heavily because re-introducing the dropped data flips the matrix top.

**Completeness: 8/10**
- All 7 rungs filled with explicit text: +2
- All 6 transitions scored with justification: +2
- Weakest leap identified with rung pair + amplification: +1
- Attack vector written as single sentence with named assumption + dropped fact + consequence: +2
- Rung 2 ignored list has 3 items with "why it matters" notes: +1
- Rung 4 has 4 assumptions with probability estimates: +0 (one assumption A4 has unverified probability rather than estimate)

### What the next consumer (adversary) inherits

The adversary subagent reads `state.ladder.attack_vector` and writes a 4-paragraph dissent in the final report:

> The team recommends dual-deploy + drain at matrix score 8.2. The ladder reveals this score borrows 0.2 probability units of confidence from assumption A2, which assumes a 4-chain migration follows the same execution-risk profile as a 1-chain migration. This is a category error. Each chain has independent mempool, executor, and validator dynamics. The 1-chain experience cannot forecast 4-chain timing.
>
> Three facts at Rung 2 were dropped that, if re-introduced, flip the recommendation: Radiant's 48h support spike during their drain phase, the 1-chain to 4-chain category change, and the current high-gas conditions on Ethereum (60+ gwei against LayerZero's 40 gwei threshold). Each fact independently degrades the dual-deploy + drain score. Together they drop it from 8.2 to 6.4, putting wrapped legacy (6.7) as the new top.
>
> The team's belief at Rung 6 ("newer is better") is unverified and will reinforce a 6-month migration cadence going forward. This is a long-term cost: every LayerZero release will trigger a migration debate. The team should test the belief before reinforcing it.
>
> Recommendation downgrade: MEDIUM confidence on dual-deploy + drain. Alternative: wrapped legacy at MEDIUM confidence. Lead's call which to ship.

This dissent reaches the final synthesis and the lead decides whether to adopt it.

---

## What This Means For The Decision

The Ladder of Inference is the audit layer between Decision Matrix (the recommender) and the adversary (the challenger). Without it, the adversary attacks blind. With it, the adversary has a named target: the weakest leap, the dropped data, the unverified assumption. The ladder doesn't change the recommendation. It changes the confidence with which the recommendation lands.

When the ladder finds a clean trace (all transitions ≥ 2), the recommendation lands at HIGH confidence with a one-line note "no significant leaps detected." When the ladder finds one weak transition, the recommendation lands at HIGH-with-flag and the dissent names the assumption. When the ladder finds multiple weak transitions or a 0-scored leap, the recommendation downgrades to MEDIUM and the lead decides whether to ship anyway, probe further, or pivot to the runner-up.

The cost of skipping the ladder: confident recommendations that look obvious in retrospect and produce hindsight regret. The benefit of running it well: every leap the team made unconsciously becomes visible, and the adversary attacks the weakest one before it ships.
