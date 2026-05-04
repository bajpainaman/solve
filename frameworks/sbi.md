# Situation-Behavior-Impact (SBI)

**Phase:** Decide (conditional) · **Source:** https://untools.co/situation-behavior-impact

SBI is a script-generator. When the recommendation requires a conversation that didn't happen yet (a teammate to push back to, a partner to align with, a user community to message), SBI produces the opening lines of that conversation. The format is specific: name the situation concretely, describe the behavior without judgment, name the impact specifically. Without scripts, "we'll talk to them about it" becomes a never-happens. With scripts, the conversation has a starting line.

This framework only fires when the predicate detects interpersonal-conflict signals or when the recommendation explicitly requires a behavior change someone has to be told about.

---

## Entry Predicate

```
intake.problem_refined contains interpersonal-conflict-signals
  ∨ intake.stakeholders ∈ {multi-stakeholder, org-wide}
  ∨ frameworks/conflict-resolution-diagram.md was triggered
  ∨ frameworks/decision-matrix.md::top_recommendation requires_behavior_change
  ∨ frameworks/six-hats.md surfaced inter-team disagreement
```

Conflict signals in `intake.problem_refined`:
- explicit: "team," "manager," "feedback," "report," "communication," "conflict," "disagree"
- implicit: "they keep doing X," "I don't know how to tell them," "the other team," "stakeholders"

Behavior-change signal in recommendation:
- the recommendation requires someone to do (or stop doing) something they're not currently doing
- the recommendation requires user-facing communication (a deprecation announcement, a deadline, a behavior change ask)

If none of these fire, SBI is **skipped** for this run. Skipping is documented in the cynefin routing table as `SBI: no, no interpersonal signals.`

### Inputs

- `intake.json` — stakeholders, problem text
- `intake.problem_refined` — canonical problem statement
- `frameworks/conflict-resolution-diagram.md` (if it ran in Phase 1) — the parties + shared objective
- `frameworks/decision-matrix.md::top_recommendation` — what's being decided
- `frameworks/six-hats-red.md` — Red Hat's gut sense of interpersonal friction
- `frameworks/six-hats-blue.md` — Blue Hat's process commentary on stakeholder dynamics

### Outputs

- `$RUN_DIR/frameworks/sbi.md` — the SBI scripts (one per required conversation)
- `state.SBI_SCRIPTS` field — the list of conversations the recommendation requires
- (Conditional) handoff to Minto: scripts must appear in the recommendation's execution plan

---

## Operating Principles

These are non-negotiable. Every SBI script respects all five.

**1. Situation is concrete or it's nothing.**

"In our last meeting" is not concrete. "In Tuesday's bridge-design review at 2pm" is concrete. The point of S is to anchor the conversation in a specific event the other party also remembers. Without a specific anchor, the conversation drifts into "you always do X" generalities, which trigger defensiveness. Anti-pattern: "When you sometimes don't communicate clearly..." That's not a situation, that's an accusation.

**2. Behavior is observable or it's a judgment.**

"You were dismissive" is a judgment. "You said 'no, that won't work' and changed topics within 15 seconds without asking what I meant" is a behavior. The other party can dispute a judgment forever. They can only dispute a behavior by claiming the observation is wrong, which is a much narrower fight. Anti-pattern: behavior described in adjectives ("rude," "unclear," "rushed"). Replace with verbs and observable actions.

**3. Impact is specific to the speaker, not generic.**

"It made the meeting unproductive" is generic. "I left the meeting without a decision on bridge architecture, which means I can't start the implementation Monday and we slip our launch by a week" is specific. The first sounds like a complaint. The second sounds like a problem to solve together. Anti-pattern: impact stated as "it affected morale" or "it created tension." Those are abstractions. Name the concrete consequence: who couldn't do what, by when, costing what.

**4. SBI is opening, not script-in-full.**

The script's job is to start the conversation in a productive frame. It's not the whole conversation. Don't write 10 paragraphs of speech for the user. Write 3 sentences (S, B, I) and stop. The other party then responds; the user adapts. Anti-pattern: writing a 500-word monologue including responses, rebuttals, and a call to action. That's a manifesto, not an opening.

**5. SBI is the speaker's perspective, not an arbitration verdict.**

The user is one party. The script is what they say. The other party will have a different SBI from their side. Don't pretend the SBI is "objective truth." It's the user's specific observation and consequence. Frame it as "from where I sit." Anti-pattern: writing the SBI as if it's the team's collective view; that pre-empts the other party's response and triggers defensiveness.

---

## Response Posture

**Tone.** Calibrated. SBI scripts succeed when they sound like the speaker on a clear-headed day, not the speaker in the heat of frustration. Write in the voice of someone who already cooled off and is trying to fix the working relationship.

**Pacing.** One script per required conversation. If the recommendation requires 3 conversations (eng, ops, partner), produce 3 scripts. Each script is independent.

**Push depth.** Heavy push on specificity. A script with "in our recent meeting" gets pushed to "in Tuesday's bridge-design review at 2pm." A script with "you were dismissive" gets pushed to a verb-and-observation sentence. The framework is only useful if the scripts are usable.

**Where to escalate.** SendMessage to lead when:
- The conflict is escalation-worthy (e.g. legal, HR, founder-to-founder); SBI alone is insufficient
- The relationship is too damaged for SBI to land (e.g. multi-month no-trust state); recommend mediator instead
- The behavior change requires an org-level intervention (e.g. process change, role re-org); SBI surfaces it but doesn't solve it

---

## Anti-Sycophancy Rules

The agent running SBI must never write these:
- "When you have a moment, perhaps we could discuss..." (cut to S, B, I)
- "I noticed that sometimes..." (sometimes = generic = useless)
- "I felt that..." (feelings without behavior is a judgment)
- "It would be great if you could..." (asks dressed as suggestions evade specificity)
- "I'm sure you didn't mean to..." (pre-empting their intent removes their agency to respond)

The agent must always:
- Anchor S in a specific moment.
- Describe B in observable verbs.
- Name I as a concrete consequence to the speaker.
- Stop after I; let the script breathe.
- Frame as "from where I sit," explicitly the speaker's perspective.

---

## Pushback Patterns

These show how the agent handles common framing errors when generating SBI scripts.

**Pattern 1: Situation too vague then anchor in a specific moment**

- User input (or prior framework output): "they often shut down ideas in meetings"
- BAD SBI: "S: In recent meetings... B: You shut down ideas... I: It's been frustrating."
- GOOD SBI: "S: In Tuesday's bridge-architecture review at 2pm. B: When I proposed the dual-deploy pattern, you said 'that's not how LayerZero works' and changed topics in under 30 seconds, before I could share the LZ docs link. I: I left the meeting without a decision and have spent the last two days reading the LZ docs to confirm my proposal works, which has delayed our migration timeline by three days from where I expected to be."

The push: "give me the specific meeting, the specific words, and the specific lost time. If you can't name them, the SBI isn't ready."

**Pattern 2: Behavior described as judgment then convert to verb-observation**

- Prior framework: "the partner team is uncooperative"
- BAD SBI: "B: You've been uncooperative on the migration timeline."
- GOOD SBI: "B: When we asked for a sign-off on the drain timeline by April 15, the response on April 22 was 'we'll get back to you,' and there has been no follow-up in the seven days since."

The push: "uncooperative is a label. What did they do, observably, with dates and quotes?"

**Pattern 3: Impact described abstractly then make it concrete**

- Prior framework: "the migration confusion has been bad for users"
- BAD SBI: "I: It's affecting our users negatively."
- GOOD SBI: "I: 47 support tickets in the last 5 days asking 'is OFTv1 deprecated yet?' Because we haven't published a clear deprecation date, support volume has increased 3x and our community manager is spending half their time on FAQ replies that a single announcement would resolve."

The push: "name the metric, the count, the cost to a specific role or budget. If you can't, the impact isn't specific enough to land."

**Pattern 4: SBI written as collective verdict then re-frame as speaker perspective**

- Prior framework: "the team feels eng has been moving too fast"
- BAD SBI: "We feel that you've been moving too fast on the migration."
- GOOD SBI: "From where I sit on the ops side: in last Wednesday's sprint review, when the OFTv2 deployment was added to next sprint with no time allocated for the runbook update, I said I needed two more days and the response was 'we can ship without the runbook ready.' The impact on me: I'm now planning to be on-call during the entire deploy window because the runbook gaps mean any incident during deploy will require ad-hoc decisions instead of documented procedures."

The push: "you is one person, not the team. Frame as 'from where I sit' and own the perspective."

**Pattern 5: SBI for a public announcement then adjust the format**

- Use case: the recommendation includes "announce OFTv1 deprecation to users"
- BAD SBI (treats as 1-on-1): "S: In our community Discord. B: When we announce, we'll say... I: Users will know."
- GOOD SBI (announcement format): "S: When announcing the migration on May 15 in the community Discord, blog post, and X thread. B: Clearly mark OFTv1 as deprecated by drain start date June 26, with a 30-day migration window, including a step-by-step guide and a 24/7 support channel for the first 2 weeks. I: This prevents the support-volume spike we saw in Stargate's OFTv1 → OFTv2 migration (where unclear deprecation timing produced 3-week support backlog) and reduces operational load during the highest-risk window."

The push: "announcements are SBI applied to a community, not a person. Adjust S to 'when announcing,' B to 'what we say,' I to 'what we prevent or enable.'"

---

## Method

SBI runs as a 5-step procedure. Each step produces a discrete output that feeds the next.

### Step 1, Detect that SBI should run

```bash
# Check predicate
echo "$INTAKE_PROBLEM_REFINED" | grep -iE "team|manager|feedback|report|communication|conflict|disagree|stakeholders" \
  || [ -f "$RUN_DIR/frameworks/conflict-resolution-diagram.md" ] \
  || [ "$INTAKE_STAKEHOLDERS" != "single-decider" ]
```

If the predicate doesn't fire, SBI writes a one-line skip note and exits:

```markdown
# SBI, <SLUG>

**Predicate:** not satisfied. No interpersonal-conflict signals in intake. Stakeholders = single-decider. No conflict-resolution-diagram in Phase 1. No inter-team disagreement in Six Hats.

**Skipped.** No scripts required for this recommendation.
```

This is a valid output. Don't force scripts when none are needed.

### Step 2, Enumerate the conversations the recommendation requires

For every required behavior change in the recommendation, identify:
- Who needs to act (or stop acting): the listener
- What they need to do (or stop doing): the requested behavior change
- Why they're not doing it now: the inferred friction

A conversation is required when:
- The behavior change is asked of a specific person or team
- The recommendation depends on the change (no change → recommendation fails)
- The change won't happen without an explicit ask

Make a list:

```
CONVERSATION 1: <speaker> → <listener>, about <topic>
CONVERSATION 2: ...
...
```

For an OFTv1 → OFTv2 migration with the dual-deploy + drain recommendation, typical conversations:

1. Eng → Ops, about runbook responsibility for the drain window
2. Eng → Partner integrators (LPs), about migration timeline
3. Eng/PM → Community, about deprecation announcement
4. Eng → External auditor (vendor relationship), about scope and lead time

Not every recommendation produces 4 conversations. Some produce 1. Some produce 0 (the skip case).

### Step 3, Generate the SBI for each conversation

Format per conversation:

```
CONVERSATION <N>: <speaker → listener>, <topic>

S: <specific situation>
B: <observable behavior>
I: <concrete impact>
```

Each line is one sentence (rarely two). The total length per conversation: 3-5 sentences. Anything longer is overshooting.

For the announcement / community case, the format adjusts:

```
ANNOUNCEMENT <N>: <topic>

S: When <event/timing>...
B: <what we say or do>
I: <what we prevent / enable>
```

### Step 4, Smell-test each script

For each script, the agent self-pushes:

- "If I were the listener, would I dispute S? If yes, S isn't anchored enough. Re-anchor."
- "If I were the listener, would I dispute B? If I'd say 'that's not what happened,' B isn't observable. Re-write."
- "If I were the listener, would I dispute I? If I'd say 'how was that my problem?' I isn't tied to a concrete consequence. Re-tie."

If any of the three fail the smell test, regenerate. The script is only valuable if it survives the listener's likely first response.

### Step 5, Write output and update state

The output structure is mandatory. See Output Schema below.

State update:

```json
{
  "SBI_SCRIPTS": [
    {
      "id": "conv-1",
      "speaker": "<who>",
      "listener": "<who>",
      "topic": "<short>",
      "script": "S: ... B: ... I: ..."
    },
    ...
  ]
}
```

The Minto pyramid synthesis at the end of Phase 3 must include SBI scripts in the recommendation's execution plan. If the user's recommendation requires conversations and the report doesn't include scripts, the user will skip the conversations and the recommendation will fail.

---

## Question Patterns

SBI runs partly interactively (when the user has direct context the framework doesn't) and partly analytically. The question patterns drive the interactive parts.

### Question Pattern 1, anchoring the situation

> "What was the specific moment? Tell me the date, the meeting name, the timestamp if you remember it. If you can't name a specific moment, name the meeting type and rough timeframe ('last Tuesday's standup,' 'the bridge review the week of April 15')."

Good answer: "The bridge-architecture review on Tuesday April 22, around 2pm in the eng-design Zoom."

Red flag: "Lately in our meetings..." Push: "name one specific meeting. If you can't, the SBI won't anchor."

Smart-skip: if `intake.problem_refined` already specifies the moment ("in last Tuesday's stand-up I said X"), use that.

### Question Pattern 2, observing the behavior

> "What did they do? Use verbs. What did they say (use quotes if you remember)? What was the immediate observable effect (someone changed topics, a decision was made, the meeting ended)? Avoid adjectives like 'dismissive,' 'rude,' 'unclear.' Stick to verbs and quotes."

Good answer: "When I shared the dual-deploy proposal, they said 'that's not how LayerZero works' and changed topics within 30 seconds before I could share the LZ docs link."

Red flag: "They were dismissive." Push: "what does dismissive look like in this case? Quotes if you have them, otherwise verbs."

### Question Pattern 3, naming the impact

> "What concrete thing didn't happen, or happened badly, because of the behavior? Quantify if possible: hours lost, decisions deferred, support tickets generated, ship dates slipped. Tie it to your work or your role specifically; not 'the team's morale,' but 'I had to do X' or 'I couldn't do Y.'"

Good answer: "I left the meeting without a decision and have spent the last two days re-reading LZ docs and writing a 5-page memo to demonstrate the dual-deploy approach is correct, when a 5-minute response in the meeting would have been enough."

Red flag: "It hurt morale." Push: "morale is generic. What specifically didn't happen for you?"

### Question Pattern 4, multi-stakeholder mapping

> "Are there other stakeholders affected by this same situation? If yes, do they need their own SBI script (different listener, different behavior change, different impact), or are they aligned with you (then they should hear yours, not write their own)?"

Good answer: "Ops also affected. They need their own SBI to the partner team about the runbook timeline; the listener is different, the impact is different."

Red flag: "Everyone is affected." Push: "name the specific roles and impacts. If everyone is affected the same way, write one SBI. If they're affected differently, write separate scripts."

### Question Pattern 5, announcement format

> "Is this conversation 1-on-1 or a public announcement (community, blog, partners)? If public, the format is: 'When announcing X, clearly state Y, this prevents Z.' Use this when the listener is a group, not a person."

Good answer: "Public, this is the OFTv1 deprecation announcement to the community."

Red flag: trying to write a 1-on-1 SBI for a community announcement. Push: "switch format to 'when announcing.'"

---

## Forcing Exemplars

When writing SBI scripts, every script should have a forcing version (specific, observable, concrete) instead of a softened version (vague, judgmental, abstract).

### Exemplar 1, peer-to-peer eng conversation

SOFTENED (avoid):
> "S: I've noticed in our recent meetings... B: You sometimes shut down ideas without fully considering them... I: It's been frustrating and I think it's affecting team dynamics."

FORCING (aim for):
> "S: In Tuesday's bridge-architecture review on April 22 at 2pm. B: When I proposed dual-deploy + drain for OFTv2, you said 'that's not how LayerZero works' and moved to the next agenda item within 30 seconds, before I could share the LZ docs link supporting the approach. I: I left the meeting without a decision and have spent the next two days writing a 5-page memo to validate the proposal, which has delayed the start of OFTv2 implementation by three days from where I planned to be this week."

### Exemplar 2, eng-to-ops conversation

SOFTENED (avoid):
> "S: As we plan the migration... B: It seems like the runbook isn't getting enough attention... I: This could cause issues during deploy."

FORCING (aim for):
> "S: In last Wednesday's sprint review on April 24, when we added the OFTv2 deployment to the next sprint without an explicit runbook-update task. B: I said the runbook needed two more days of work to cover cross-chain failure cases, and the response was 'we can ship without the runbook fully updated.' I: From where I sit on ops, this means I'm planning to be on-call for the entire 7-day drain window because incidents that hit during deploy will require ad-hoc decisions instead of documented procedures, which adds 40+ hours of on-call to my next two weeks and increases incident-response time during the highest-risk migration phase."

### Exemplar 3, public deprecation announcement

SOFTENED (avoid):
> "S: When we announce the migration... B: We'll let users know... I: Users will be informed."

FORCING (aim for):
> "S: When announcing the OFTv2 migration on May 15 at 9am UTC across the community Discord, blog, X thread, and partner integrator email list. B: Clearly mark OFTv1 as deprecated effective drain start date June 26, with a 30-day migration window, a step-by-step migration guide linked in the announcement, and a dedicated 24/7 support channel for the first 14 days post-announcement. I: This prevents the support-volume spike we saw during Stargate's OFTv1 to OFTv2 migration (3-week support backlog due to unclear deprecation timing), reduces ops load during the highest-risk window, and gives partner integrators the lead time their compliance + integration cycles require to update their codepaths."

### Exemplar 4, vendor (external auditor) conversation

SOFTENED (avoid):
> "S: As we plan the audit... B: We'd like to engage you for the OFTv2 review... I: It would be great to get this scheduled."

FORCING (aim for):
> "S: In our project intake call on May 6, when we discussed scope and timeline. B: We've defined the OFTv2 audit scope as cross-chain message-encoding diff between OFTv1 and OFTv2, lock/burn race conditions, executor logic, and cross-chain mempool dynamics, and we're requesting a 1-2 week engagement starting May 9 with a final report by May 23. I: We need the report by May 23 because our pre-ship checklist gates mainnet deploy on audit closure (item 9 of 12); a delay of more than 5 business days on the report shifts our drain start from June 26 to early July, which conflicts with our community-announced timeline and triggers a re-announcement to integrators."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/sbi.md` follows this structure exactly. Every section is required.

### Section A, Header

```markdown
# Situation-Behavior-Impact, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Predicate:** <fired / not fired, with the specific signal>
**Inputs read:** intake.json, frameworks/conflict-resolution-diagram.md (if exists), frameworks/decision-matrix.md, frameworks/six-hats-red.md, frameworks/six-hats-blue.md
```

If predicate did not fire, the rest of the output is a single skip note and the file ends. See Step 1.

### Section B, Conversations enumerated

```markdown
## Conversations Required

| # | Speaker → Listener | Topic | Why required | Driver framework |
|---|---|---|---|---|
| 1 | <who> → <who> | <topic> | <why this conversation must happen> | <framework that surfaced the need> |
| 2 | ... | ... | ... | ... |
```

### Section C, Scripts (one per conversation)

```markdown
## Script 1: <Speaker> → <Listener>, <Topic>

**S:** <specific situation, one sentence>
**B:** <observable behavior, one sentence>
**I:** <concrete impact, one sentence>

**Smell test:**
- Could listener dispute S? <yes/no, with reasoning>
- Could listener dispute B? <yes/no, with reasoning>
- Could listener dispute I? <yes/no, with reasoning>
- Survives first response? <yes/no>

**Anticipated reply:** <one sentence; what the listener likely says next>
**Speaker's follow-up move:** <how the speaker should respond to that likely reply, in one sentence>
```

For announcement-format scripts (when listener is a group):

```markdown
## Announcement N: <Topic>

**S:** When <event/timing>, in <channel(s)>.
**B:** <what we say / do, one sentence with specific dates and links>.
**I:** This prevents <specific failure mode> and enables <specific outcome>.
```

### Section D, Cross-script dependencies

```markdown
## Dependencies between scripts

<If script 2 depends on script 1 happening first (e.g. internal alignment before public announcement), state explicitly.>

| Script | Blocks | Blocked by | Sequence |
|---|---|---|---|
| 1 | <#s> | <#s> | <ordered position> |
| ... | ... | ... | ... |
```

### Section E, Escalation conditions

```markdown
## When SBI is not enough

For each script, name the condition under which SBI is insufficient and the conversation needs a different intervention (mediator, manager involvement, formal process):

| Script | Escalation condition | Next intervention |
|---|---|---|
| 1 | <e.g. listener has consistently shut down 3 prior conversations> | <e.g. manager involvement> |
| 2 | <e.g. partner refuses to commit timeline> | <e.g. legal review of contract terms> |
```

### Section F, What this means for the decision

```markdown
## What This Means For The Decision

<2-3 sentences. The recommendation requires N conversations. Without these conversations, the recommendation does not execute. The scripts above are the opening lines of those conversations.>
```

### Section G, Completeness score

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- All required conversations enumerated: +<N>
- Each script has S/B/I with specificity: +<N>
- Smell test applied per script: +<N>
- Anticipated reply named per script: +<N>
- Cross-script dependencies + escalation conditions specified: +<N>
```

---

## Decision Hook

SBI's output drives the recommendation's execution plan. Specifically:

### Recommendation must include scripts when SBI fires

The Minto pyramid's Why arguments include "this requires conversations X, Y, Z" with the SBI scripts in an appendix or inline. Without scripts, the recommendation has a behavior-change ask without an opening line.

### Confidence-rubric impact

SBI does not directly modify the rubric. Indirectly:
- If SBI reveals that the recommendation requires N conversations and N is large (≥ 4), the execution risk is higher; this is captured by adversary scoring on coordination risk, not by SBI directly.
- If SBI reveals that one of the required conversations is escalation-worthy (mediator, legal, HR), the recommendation may need to pause and resolve the inter-personal layer before executing the technical decision; this triggers a SendMessage to lead.

### Override conditions

SBI does not override other frameworks. It supplements. The recommendation stays the same; SBI provides the conversation scripts the recommendation already requires.

---

## Cross-Framework Triggers

These conditions in the SBI output force changes elsewhere in /solve.

### Triggers fired by escalation conditions

- Any script's escalation condition lists "manager involvement" or "legal review", flag in the report's "Open Risks" section. The recommendation is conditional on the inter-personal layer holding.
- All scripts' escalation conditions are "trivial / first conversation likely succeeds", no flag.

### Triggers fired by conversation count

- ≥ 5 conversations required, the recommendation has high coordination overhead. Add a "coordination risk" note to the dissent section.
- 0 conversations (predicate didn't fire), single-line skip note. No further triggers.

### Triggers fired by mismatched stakeholder count

- intake.stakeholders = "single-decider" but SBI surfaced ≥ 1 conversation, contradiction. The user marked it single-decider but the recommendation requires conversations. SendMessage to lead: confirm whether intake should be updated to "small-team" or whether the conversations are skippable.

---

## Failure Modes

SBI can mislead in five distinct ways. The framework checks for each before completing.

### Failure Mode 1, generating SBI when none is needed

Trap: predicate didn't fire (single-decider, no conflict signals) but the agent generates 3 scripts because it can.

Manifestation: output has scripts for "yourself," "your future self," "the project plan." These are not real listeners.

Check: Step 1 explicitly checks the predicate. If predicate is false, write the skip note and exit.

Recovery: delete the generated scripts; write the skip note.

### Failure Mode 2, situation too vague

Trap: S says "in our meetings" or "lately." The script doesn't anchor.

Manifestation: S contains the words "often," "sometimes," "lately," "recently," "usually" without a specific date or event.

Check: regex pattern on S, fail if any of those words appear without a specific anchor (date, meeting name, named event).

Recovery: ask for the specific moment via Question Pattern 1; regenerate S.

### Failure Mode 3, behavior described as judgment

Trap: B contains adjectives ("dismissive," "unclear," "rude") instead of verbs.

Manifestation: B is grammatically a description of someone, not a description of an action.

Check: B must contain at least one observable verb (said, did, wrote, sent, changed, moved, paused). If only adjectives, fail.

Recovery: ask for the specific action via Question Pattern 2; regenerate B.

### Failure Mode 4, impact stated abstractly

Trap: I says "it affected the team" or "it created tension." Generic.

Manifestation: I lacks a quantified or specific consequence. No number, no role, no missed deadline.

Check: I must contain at least one of: a number, a named role, a specific deliverable, a date.

Recovery: ask for the specific consequence via Question Pattern 3; regenerate I.

### Failure Mode 5, single conversation written as collective verdict

Trap: SBI written in "we" voice, pretending it's the team's collective view. Triggers defensiveness in listener.

Manifestation: B uses "we feel," "the team thinks," "all of us have noticed."

Check: B must be in first-person singular ("I observed," "from where I sit"). Or, for announcement format, B is in plural ("we will say").

Recovery: re-frame to first-person singular; regenerate B.

---

## Jargon Glossary

SBI uses domain-specific vocabulary. First use of any of these terms in the output should include a one-line gloss.

- SBI, the Situation-Behavior-Impact framework for structuring difficult conversations.
- script, a 3-sentence opening (S, B, I) for a conversation, not the whole conversation.
- listener, the person (or group) the speaker addresses; the recipient of the script.
- speaker, the person delivering the SBI; one specific perspective, not the team's.
- anchor, the specific moment in S that both parties can recall; without it, the conversation drifts.
- observable, a behavior described in verbs and quotes, not adjectives or judgments.
- impact-specificity, the rule that I must name a concrete consequence: a number, a role, a deliverable.
- announcement format, the SBI variant for public communications (community, blog, partners).
- smell-test, the self-pushback applied to S, B, I by asking "would the listener dispute this?"
- cross-script dependency, when one conversation must happen before another (e.g. internal alignment before public announcement).
- escalation condition, the threshold at which SBI alone is insufficient; mediator or formal process required.
- skip note, the valid output when the predicate doesn't fire; SBI is not always required.

---

## Completeness Scoring

SBI self-rates 0-10 on script quality. The rubric:

### 10/10, decisive

- Predicate fired and all required conversations enumerated
- Each script has:
  - S anchored to a specific moment (date or named event)
  - B in observable verbs (with quotes if available)
  - I with concrete consequence (number, role, deliverable, or date)
  - Smell test applied with all three lines passing
  - Anticipated reply + speaker follow-up move
- Cross-script dependencies named
- Escalation conditions per script
- 0-1 conversations could be added but were judged unnecessary; rationale documented

### 7/10, confident

- All conversations enumerated
- Each script has S/B/I with specificity but anticipated-reply field is generic or missing
- Smell test applied
- Cross-script dependencies named for ≥ 50% of scripts

### 4/10, tentative

- Conversations enumerated
- Scripts written but lack specificity in 1+ of S/B/I
- No anticipated-reply field
- Cross-script dependencies absent
- Escalation conditions absent

### 0/10, broken

- Scripts generated when predicate didn't fire, OR
- Multiple scripts with judgmental B (adjectives instead of verbs), OR
- I is generic across all scripts ("affected the team," "created tension")

A SBI completeness ≤ 4 caps the recommendation's execution-plan completeness at MEDIUM.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

By the time SBI runs, the chain has produced:
- cynefin: complicated, +2
- decision-matrix: dual-deploy + drain wins (8.2 vs 6.7)
- second-order: positive compounding via reinforcing cycle
- ladder-of-inference: identified "newer is better" leap, but Decision Matrix has independent justification
- ooda: 6-week cycle, weekly check-ins
- hard-choice: skipped
- confidence-speed-quality: QUALITY mode, pre-ship checklist with 12 items

### Step 1, predicate evaluation

Check signals in `intake.problem_refined`:

> "We have an OFTv1 token deployed on 4 chains (Ethereum, Avalanche, Arbitrum, Base) with $12M TVL. LayerZero released OFTv2 with better gas, security improvements, and a different message-encoding scheme. Should we migrate?"

Signals to check:
- "team" → not present
- "manager" → not present
- "feedback" → not present
- "communication" → not present
- "conflict" → not present
- "disagree" → not present
- "stakeholders" → implicit, but `intake.stakeholders = small-team`, not multi-stakeholder

Other predicate paths:
- conflict-resolution-diagram in Phase 1: NOT triggered (no inter-team conflict signaled)
- decision-matrix.top_recommendation requires_behavior_change: YES, the recommendation "dual-deploy + drain" requires:
  - eng team to implement dual-deploy
  - ops team to update runbook
  - users to migrate from OFTv1 to OFTv2
  - integrators to update their codepaths
  - external auditor (vendor relationship) to engage

So while the intake.problem_refined doesn't have explicit conflict signals, the recommendation's execution requires conversations.

**Predicate evaluation:** PARTIAL FIRE. The intake-level conflict signals are absent (this run does NOT have an inter-team disagreement that needed conflict-resolution-diagram). But the recommendation requires user-facing communication and vendor coordination, which is the secondary use case for SBI.

For the worked example, we treat this as the secondary case: SBI fires because the recommendation requires announcements and vendor conversations, not because there's interpersonal conflict to resolve.

### Hypothetical: what would have fired the framework on the conflict path?

For documentation, here is what would have fired SBI on the primary path:

> Suppose during Phase 1, the conflict-resolution-diagram framework had been triggered because eng (proposed dual-deploy + drain) and ops (proposed big-bang single-cutover with downtime) disagreed on the migration approach. Conflict-resolution-diagram would have surfaced:
>
> - Eng's want: dual-deploy + drain (lower user disruption, no downtime, longer total timeline)
> - Ops's want: big-bang single-cutover (shorter total timeline, planned 4h downtime, simpler runbook)
> - Shared objective: successful migration with minimal user fund loss and minimal post-migration support load
>
> SBI would then fire on the primary path with this script:

> **Script (primary path, hypothetical): Eng → Ops, about migration approach**
>
> S: In the migration-planning meeting on April 24 at 11am, when we discussed the OFTv1 → OFTv2 approach.
> B: When I proposed dual-deploy + drain, you said "we should just do a big-bang with 4h downtime, the dual-deploy will take 6 weeks and that's too long" and we moved to other agenda items without resolving the choice.
> I: From where I sit on the eng side, the dual-deploy + drain approach is what LayerZero officially recommends for $1M+ TVL migrations and what 3 prior protocols (Stargate, Radiant, Ethena) used successfully; without an explicit decision on approach, I can't start implementation, and a 4-h downtime big-bang would expose users to mempool dynamics during the cutover that the dual-deploy avoids. I'd like to walk through the LZ docs together this week to align on approach before next sprint planning.

> Anticipated reply: "I'm not against dual-deploy in principle, my concern is the 6-week timeline and ops load."
> Follow-up move: agree to dedicate 30 min to walking through LZ docs together; if their concern is timeline, address with the pre-ship checklist and shared on-call plan; if their concern is ops load specifically, surface to manager for resourcing.

Back to the actual worked example, where the conflict path did NOT fire.

### Step 2, enumerate conversations the recommendation requires (secondary use case)

The dual-deploy + drain recommendation requires:

| # | Speaker → Listener | Topic | Why | Driver |
|---|---|---|---|---|
| 1 | Eng (PM) → Community (Discord, blog, X) | OFTv1 deprecation announcement + migration guide | The pre-ship checklist (item 7) requires user-facing announcement 4 weeks before drain start; without clear deprecation messaging, support volume spikes (per Stargate's prior experience). | confidence-speed-quality.pre_ship_checklist[7] |
| 2 | Eng (PM) → Partner integrators (LP teams, indexers) | Migration timeline + technical details | Pre-ship checklist (item 7) requires integrator notification 4 weeks before drain start; integrators have their own update cycles and need lead time. | confidence-speed-quality.pre_ship_checklist[7] |
| 3 | Eng → External auditor | Audit scope + timeline + budget | Pre-ship checklist (item 1) gates mainnet deploy on audit closure; the auditor relationship is vendor-style and needs explicit scope-and-timeline conversation. | confidence-speed-quality.pre_ship_checklist[1] |

(No internal eng → ops script needed for this run because intake.stakeholders = small-team and no disagreement was surfaced. If a disagreement had been surfaced in Phase 1 conflict-resolution-diagram, we would add an internal script per the hypothetical above.)

### Step 3, generate scripts

#### Announcement 1: OFTv1 deprecation to community

**S:** When announcing the OFTv2 migration on May 28 at 9am UTC across the community Discord (#announcements), the protocol blog, the @protocol X account (with thread), and the partner integrator email list.

**B:** Clearly mark OFTv1 as deprecated effective drain start date June 26 (4 weeks lead time), with a 30-day migration window through July 26, including: a step-by-step migration guide, a recorded video walkthrough, a dedicated #oft-migration support channel staffed 24/7 for the first 14 days, and an FAQ covering the top 10 anticipated questions (drawn from Stargate's migration FAQ as base).

**I:** This prevents the support-volume spike Stargate experienced during their OFTv1 → OFTv2 migration (3-week support backlog due to unclear deprecation timing and no dedicated support channel), reduces ops load during the highest-risk drain window from approximately 100 tickets/day projected to under 30 tickets/day projected, and gives partner integrators 4 weeks of lead time to update their codepaths and documentation.

**Smell test:**
- Could community dispute S? Probably not; specific date and channels.
- Could community dispute B? Possibly on FAQ completeness; but the structure (step-by-step + video + dedicated channel) is unambiguous.
- Could community dispute I? They could ask for evidence of the Stargate baseline; we have it from prior-art research.
- Survives first response? Yes.

#### Announcement 2: Partner integrator notification

**S:** When sending the OFTv2 migration notice on May 28 at 9am UTC via direct email to the LP team contacts (Curve, Balancer, Velodrome, Aerodrome) and indexer teams (Goldsky, Ponder), with calendar invites for two technical office-hours sessions (June 4 at 2pm UTC, June 11 at 2pm UTC).

**B:** Provide: drain start date June 26, drain window 30 days, full OFTv2 contract addresses across all 4 chains, the message-encoding diff document, the integrator-side code update guide (with diff samples for common SDK integrations), the test-bench setup instructions for partner verification, and the dedicated integrator Slack channel for technical questions during migration.

**I:** This gives integrators the 4-week lead time their compliance + integration cycles require to update their codepaths, prevents the integrator-side liquidity disruption that occurred during Radiant's OFTv2 migration when 2 LPs missed the migration window and had to do emergency post-cutover updates, and surfaces any integrator-side blockers (compliance, audit cycle, codepath complexity) early enough to either accommodate or coordinate workarounds.

**Smell test:**
- Could integrators dispute S? No; specific channel and timing.
- Could integrators dispute B? Possibly on test-bench completeness; we'll iterate based on first office-hours feedback.
- Could integrators dispute I? They might have different lead-time needs; we surface that as a sub-conversation if it comes up.
- Survives first response? Yes.

#### Script 3: Eng → External auditor

**S:** In the auditor intake call on May 6 at 10am UTC, when we discussed scope, timeline, and budget for the OFTv2 migration audit.

**B:** We propose: scope = cross-chain message-encoding diff between OFTv1 and OFTv2, lock/burn race conditions in the drain mechanism, executor logic verification across all 4 chains, and cross-chain mempool dynamics under simulated gas-spike conditions. Timeline = 1-2 week engagement starting May 9, with preliminary findings by May 16 and final report by May 23. Budget = $25K-$40K depending on scope refinement after preliminary findings.

**I:** We need the report by May 23 because our pre-ship checklist gates mainnet deploy on audit closure (item 9 of 12); a delay of more than 5 business days on the report shifts our drain start from June 26 to early July, which conflicts with our community-announced timeline (announcement is locked to May 28) and would trigger a re-announcement to integrators. From our side, we'll provide: complete OFTv2 contract codebase tagged at commit X, the migration runbook draft, the test-bench setup, and 1 hour of context-setting time for the lead auditor.

**Smell test:**
- Could auditor dispute S? No; specific call and time.
- Could auditor dispute B? Possibly on scope (they may want to expand or narrow); the conversation should resolve this in the intake call itself.
- Could auditor dispute I? Possibly on timeline if their engagement queue is full; we hear back, and if their timeline doesn't fit, we either extend the migration window or seek a backup auditor.
- Survives first response? Yes.

### Step 4, smell-test summary

All three scripts pass the smell test. Anticipated replies:

- Community: most likely a flood of clarifying questions in the dedicated channel; staff for it.
- Integrators: most likely scheduling conflicts on office-hours; offer 1-on-1 backup slots.
- Auditor: most likely scope expansion request (they want to include economic-attack vectors); agree if budget permits, else scope as primary with a follow-up engagement for the rest.

### Step 5, write output

```markdown
# Situation-Behavior-Impact, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T19:30:00Z
**Predicate:** PARTIAL FIRE. Intake-level conflict signals absent (no team disagreement, no conflict-resolution-diagram in Phase 1). Recommendation-driven fire: dual-deploy + drain requires public announcement (community, integrators) and vendor coordination (auditor). SBI runs on the secondary use case path.
**Inputs read:** intake.json (stakeholders=small-team, no conflict signals), frameworks/decision-matrix.md (top: dual-deploy + drain), frameworks/confidence-speed-quality.md (mode: QUALITY, checklist 12 items), frameworks/six-hats-red.md (no inter-team friction signals), frameworks/six-hats-blue.md (flagged auditor consultation as missing).

## Conversations Required

| # | Speaker → Listener | Topic | Why required | Driver |
|---|---|---|---|---|
| 1 | Eng (PM) → Community | OFTv1 deprecation announcement | Pre-ship checklist item 7: integrator and user notification 4 weeks before drain start | confidence-speed-quality.checklist[7] |
| 2 | Eng (PM) → Partner integrators | Migration timeline + technical handoff | Pre-ship checklist item 7: integrator notification with technical detail | confidence-speed-quality.checklist[7] |
| 3 | Eng → External auditor | Audit scope, timeline, budget | Pre-ship checklist item 1: external audit gates mainnet deploy | confidence-speed-quality.checklist[1] |

## Announcement 1: OFTv1 deprecation to community

[full S, B, I from Step 3]

[smell test, anticipated reply, follow-up move]

## Announcement 2: Partner integrator notification

[full S, B, I from Step 3]

[smell test, anticipated reply, follow-up move]

## Script 3: Eng → External auditor

[full S, B, I from Step 3]

[smell test, anticipated reply, follow-up move]

## Dependencies between scripts

| Script | Blocks | Blocked by | Sequence |
|---|---|---|---|
| 3 (auditor) | 1, 2 | none | first; auditor engagement starts May 9 |
| 1 (community) | none | 3 (need audit closure status known before locking date) | second; announcement on May 28 |
| 2 (integrators) | none | 3 (same reason); paired with 1 | second; same date as 1 |

## When SBI is not enough

| Script | Escalation condition | Next intervention |
|---|---|---|
| 1 (community) | Community pushes back on timeline (e.g. "30 days isn't enough"); 2+ days of escalating sentiment in #oft-migration | Extend migration window to 45 days; communicate via secondary announcement |
| 2 (integrators) | One or more integrators cannot meet the 4-week timeline | Negotiate per-integrator extensions; if blocking integrator is structural to liquidity, escalate to founder for partner relationship management |
| 3 (auditor) | Auditor declines or cannot meet May 23 deadline | Engage backup auditor (Trail of Bits, Spearbit) immediately; if no auditor can fit timeline, downgrade confidence-speed-quality mode to PROBE on a single chain (Base) first, then re-run /solve |

## What This Means For The Decision

The dual-deploy + drain recommendation requires 3 conversations to execute: 1 vendor (auditor), 2 announcements (community, integrators). Without these conversations, the pre-ship checklist (which gates the recommendation in QUALITY mode) cannot complete. The scripts above are the opening lines of those conversations. Schedule them in order: auditor intake May 6, then announcements scripted for May 28 once audit timeline is confirmed.

If conflict-resolution-diagram had fired in Phase 1 (eng vs ops on big-bang vs dual-deploy), an additional internal script would be required and would block all three external scripts above. It did not fire in this run, so internal alignment is assumed.

## Completeness: 9/10

**Rubric:**
- Predicate evaluated correctly (partial fire on secondary path, primary path documented for completeness): +2
- All 3 required conversations enumerated with driver framework: +2
- Each script has S/B/I with specificity: +2
- Smell test applied per script: +1
- Anticipated reply + follow-up move per script: +1
- Cross-script dependencies + escalation conditions specified: +1
- Failure-mode self-checks: 0 deferred
```

### What the next framework (Minto) inherits

Minto receives:
- 3 SBI scripts (1 vendor, 2 announcements)
- Cross-script dependencies (auditor must engage before announcements lock)
- Escalation conditions per script
- The fact that the recommendation's execution plan must include these scripts inline or in an appendix

Minto's pyramid will incorporate SBI scripts in the recommendation's execution plan, ensuring the user has the opening lines for every required conversation.

---

## What This Means For The Decision

SBI is the framework that turns "we'll talk to them about it" into a real opening line. Without scripts, hard conversations don't happen, partner notifications get vague, vendor relationships get sloppy, and the recommendation's execution stalls at the inter-personal layer.

For the OFTv1 → OFTv2 migration, the conflict path didn't fire (no team disagreement) but the secondary path did (public announcements + vendor coordination). The 3 scripts above are the difference between a recommendation that ships clean and one that ships with confusion, support backlog, and integrator surprise.

The cost of skipping SBI when it should fire: the recommendation's behavior-change asks become hopes. The benefit of doing it right: every required conversation has a starting line, a smell-test, an anticipated reply, and an escalation plan.
