# Eisenhower Matrix

**Phase:** Decide · **Source:** https://untools.co/eisenhower-matrix

A 2×2 matrix on Urgency × Importance. The fastest framework in Phase 3 and one of the most reused. It exists to triage candidate options and sub-decisions before the Decision Matrix burns weighted scoring on things that should have been dropped or delegated.

---

## Entry Predicate

```
always_run if intake.time_pressure ∈ {now, this-week}
recommended otherwise
```

The framework runs every time, but its weight in routing depends on time pressure. Under
high time pressure (now, this-week), Eisenhower is one of the dominant frameworks for the
Decide phase. With no deadline, it acts as a quick sanity check.

### Inputs

- `intake.time_pressure` (now / this-week / this-month / no-deadline)
- `intake.success_criteria` (defines what "important" means for this run)
- `frameworks/productive-thinking.md::resource_plan` (people, time, decisions needed)
- `frameworks/zwicky-box.md::archetypes` (or `frameworks/decision-matrix.md::options` if matrix has run)
- `frameworks/cynefin.md::routing` (read the weight: normal / urgent-only)

### Outputs

- `$RUN_DIR/frameworks/eisenhower.md` — the 2×2 plot + per-cell prose + classification table

---

## Operating Principles

**1. Urgent is not the same as important.**

Urgency is about deadlines. Importance is about success criteria. Many decisions look urgent because someone is asking now, not because the consequences matter. The matrix exists to separate these. Anti-pattern: classifying something as "urgent + important" by default because it's the loudest item in the queue.

**2. Drop is a real answer.**

If a candidate option is neither urgent nor important, the recommendation for that option is **drop it**. Not "consider it later." Drop. Most candidate-option lists have 1-3 items that should never have been written down. Eisenhower removes them so Decision Matrix only weighs serious candidates. Anti-pattern: writing every option into Decision Matrix and letting low-importance options dilute the weighted scoring.

**3. Delegate when the decision-maker is wrong.**

If the option is urgent and important but `intake.decision_maker = someone-else` or `unclear`, the answer is delegate, not decide. Eisenhower surfaces this because the matrix forces a "who acts" question that Decision Matrix doesn't ask. Anti-pattern: running Decision Matrix on options the team has no authority to commit.

**4. Schedule means commit a date.**

"Important but not urgent" doesn't mean "we'll get to it." It means "this matters; commit a calendar slot." If Eisenhower puts an option in Schedule and no calendar slot lands in the report, the option will quietly evaporate. Anti-pattern: vague "we should do this eventually" entries that never get scheduled.

**5. Match urgency to time pressure scope.**

`intake.time_pressure = now` makes the deadline 24-48h. `this-week` makes it 5-7 days. `this-month` makes it 2-4 weeks. Calibrate "urgent" to the scope of `intake.time_pressure`. An option urgent against a 2-week deadline isn't urgent against a 24-hour one. Anti-pattern: using "urgent" inconsistently across runs because the scope was never calibrated.

---

## Response Posture

**Tone.** Triage-doctor. Fast, decisive, no hedging. Eisenhower is not the place for nuance. Each option goes in exactly one cell.

**Pacing.** Single pass. Read the option list, classify each, output the matrix and table. No iteration unless an option is genuinely on a quadrant boundary, in which case default to the more conservative cell (e.g. between SCHEDULE and DROP, prefer SCHEDULE).

**Push depth.** Zero direct user questions. Eisenhower runs analytically against the intake + prior framework outputs. If a candidate option has no clear urgency or importance signal, mark it `unclassifiable` and SendMessage to lead requesting a clarification round.

**Where to escalate.** SendMessage to lead when:
- ≥ 30% of candidate options end up in Drop (the option list was poorly generated; ask for re-run of zwicky-box or productive-thinking)
- An option falls in Delegate but no clear delegate exists (decision-maker not identifiable from intake)
- The matrix produces all 4 quadrants populated by the same option (ambiguous; needs decomposition)

---

## Anti-Sycophancy Rules

The agent running Eisenhower must never write these:
- "All of these options are important in their own way..." (everything important = nothing important; pick)
- "It depends on the timeline..." (the timeline is in `intake.time_pressure`; use it)
- "We could potentially consider this for the future..." (Schedule it with a date or Drop it)
- "This is hard to classify..." (fall back to the more conservative cell; document why)

The agent must always:
- State each option's quadrant. State the timeline implication. State the action.
- Name the success criterion the option is being weighed against. Without that, "important" is undefined.
- Surface every option that lands in Drop with a one-line "rejected because..." entry. Drops should be visible in the report so future runs don't re-introduce them.

---

## Pushback Patterns

**Pattern 1: "Everything is urgent" then calibrate against time pressure scope**

- Internal evidence: 6 of 7 options classified as urgent.
- BAD: Mark all 6 as DO_NOW.
- GOOD: Re-read `intake.time_pressure`. If it's `this-month`, only items requiring action in the next ~5 days are truly urgent. Re-classify with a 5-day cutoff. The 6 urgent shrinks to 1-2.

**Pattern 2: "Important because the user asked" then check success criteria**

- Internal evidence: an option is marked important purely because someone is currently asking about it.
- BAD: Mark important without further check.
- GOOD: Compare the option to `intake.success_criteria`. Does it move the needle on the measurable metric or qualitative signal the user defined? If not, downgrade importance regardless of who's asking. Loud is not important.

**Pattern 3: "Delegate is a cop-out" then name the actual delegate**

- Internal evidence: agent puts options in Delegate without naming who would do them.
- BAD: Output "Delegate: option X" with no specifics.
- GOOD: Name the role or person. "Delegate to: $ORG_OWNER." If no name fits, the option isn't actually Delegate, it's Drop or Schedule with a "find owner" pre-task.

**Pattern 4: "Schedule means we'll get to it" then demand a date**

- Internal evidence: 3 options in Schedule with no concrete date.
- BAD: Output the matrix and let the user "decide later."
- GOOD: For each Schedule item, propose a specific calendar slot (e.g. "schedule for next sprint, 2026-05-19 review"). The user can edit the slot, but the slot must exist. No date, no Schedule.

**Pattern 5: "All four quadrants populated" then matrix is doing its job**

- Internal evidence: options spread across all 4 cells.
- BAD: "The team has too much to do."
- GOOD: This is the normal output. Summarize: "Drop 2, delegate 1, schedule 2, do-now 1." The Drops are the value. The Do-Now becomes the dominant Decision Matrix candidate.

---

## Method

Eisenhower is a 5-step procedure. Each step produces a discrete artifact that the next step consumes.

### Step 1, Gather candidate options

```bash
# Read the option source
[ -f $RUN_DIR/frameworks/decision-matrix.md ] && \
  OPTIONS_SOURCE=$RUN_DIR/frameworks/decision-matrix.md || \
  OPTIONS_SOURCE=$RUN_DIR/frameworks/zwicky-box.md
```

Read the option list. If Decision Matrix has run, use its options (Eisenhower then acts as a post-matrix triage). If Zwicky Box has run but matrix hasn't, use Zwicky archetypes (Eisenhower acts as a pre-matrix triage). If neither has run, fall back to `productive-thinking.forged_solutions`.

Failure mode: running Eisenhower with no option list. The framework needs candidates to classify. If empty, SendMessage to lead requesting Phase 1 re-run.

### Step 2, Classify Importance per option

For each option, score Importance 0-3:
- 3 = directly moves `intake.success_criteria`; high downside if not done
- 2 = supports the success criteria; moderate impact
- 1 = adjacent; low impact
- 0 = unrelated to success criteria; should be in Drop

Score against `intake.success_criteria`, not against gut feeling. If the user said the success criterion is "$12M TVL retention," score Importance based on each option's effect on TVL retention.

### Step 3, Classify Urgency per option

For each option, score Urgency 0-3 against `intake.time_pressure`:
- 3 = must act now; missing the window changes the outcome
- 2 = action needed within the time pressure scope (this week, this month, etc.)
- 1 = action eventually; no immediate cost to delay
- 0 = no urgency; could be deferred indefinitely

Calibrate the cutoff to `intake.time_pressure`:
- `now` then 24-48h cutoff for Urgency = 3
- `this-week` then 5-7 days for Urgency = 3
- `this-month` then 2-4 weeks for Urgency = 3
- `no-deadline` then no Urgency = 3 possible; cap at 2

### Step 4, Place each option in a quadrant

Quadrant rules:
- **DO_NOW** = Importance ≥ 2 AND Urgency ≥ 2
- **SCHEDULE** = Importance ≥ 2 AND Urgency ≤ 1
- **DELEGATE** = Importance ≤ 1 AND Urgency ≥ 2
- **DROP** = Importance ≤ 1 AND Urgency ≤ 1

For boundary cases (one score = 1, the other = 2), default to the more conservative quadrant (SCHEDULE rather than DROP, DO_NOW rather than DELEGATE).

### Step 5, Generate the action per quadrant

For each populated quadrant, write an action:
- DO_NOW: who acts, by when (24-48h horizon), what success looks like
- SCHEDULE: calendar slot (specific date or sprint), owner
- DELEGATE: explicit delegate (role or person), follow-up cadence
- DROP: one-line "rejected because..." entry; visible in report

Write the matrix output (see Output Schema).

---

## Probe Patterns

Eisenhower runs analytically. The agent asks itself probe questions while classifying.

### Probe 1, Is this option moving the success criteria?

> "Reading `intake.success_criteria`, does this option directly move that metric or signal? If yes, Importance ≥ 2. If no, Importance ≤ 1."

### Probe 2, Is the deadline for this option inside the time-pressure window?

> "Reading `intake.time_pressure`, what's the cutoff for Urgency = 3? Does this option's required action date land inside that cutoff?"

### Probe 3, Who acts?

> "Reading `intake.decision_maker`, can the team committing /solve also commit the action for this option? If `someone-else` or `unclear`, this is Delegate territory regardless of importance."

### Probe 4, What evaporates if we drop this?

> "If we drop this option, what specifically goes wrong? If the answer is 'nothing measurable,' the classification is Drop, not Schedule."

### Probe 5, Does the urgency signal come from the deadline or from someone asking loudly?

> "If urgency comes from a stakeholder pushing rather than from the actual deadline, the option is loud, not urgent. Downgrade Urgency by 1."

---

## Forcing Exemplars

### Exemplar 1, Stating the classification

SOFTENED (avoid):
> "This option seems important and probably should be addressed soon."

FORCING (aim for):
> "Option B (dual-deploy + drain) is DO_NOW. Importance = 3 (directly moves the success criterion of TVL retention; failure here loses $12M). Urgency = 2 (this-month time pressure puts the cutoff at 2-4 weeks; this option requires kickoff in the next 5 days to stay on track). Action: kickoff external auditor consult by 2026-05-08."

### Exemplar 2, Naming a Drop

SOFTENED (avoid):
> "Option D (separate token + voluntary migration) is interesting but probably not the right fit."

FORCING (aim for):
> "Option D is DROP. Importance = 1 (doesn't solve the underlying TVL retention problem; users with funds in OFTv1 still face the same issues). Urgency = 0 (no deadline forces this). Rejected because: voluntary migration historically completes ~30%; the remaining 70% in OFTv1 means we still own the underlying problem."

### Exemplar 3, Justifying Schedule

SOFTENED (avoid):
> "Option F (auditor selection) should be done at some point during the migration."

FORCING (aim for):
> "Option F (auditor selection) is SCHEDULE for week 1, 2026-05-04 to 2026-05-11. Importance = 3 (cynefin.routing flagged we lack external auditor input; this gates QUALITY mode). Urgency = 1 (does not need to land before kickoff, but must land within first 2 weeks of execution). Owner: $ENG_LEAD. Output: signed engagement letter."

### Exemplar 4, Justifying Delegate

SOFTENED (avoid):
> "Option G (user communication plan) probably needs someone in product or marketing."

FORCING (aim for):
> "Option G is DELEGATE to product team. Importance = 2 (user trust during cutover affects retention). Urgency = 2 (must land before week 5 force-migration). The /solve team doesn't own user-facing comms; product team does. Follow-up cadence: weekly check-in. Failure mode: if no product owner accepts, escalate to SCHEDULE for /solve team."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/eisenhower.md` follows this exact structure.

### Section A, Header

```markdown
# Eisenhower Matrix, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Time pressure:** <intake.time_pressure>
**Urgency cutoff:** <derived: 24-48h / 5-7d / 2-4w>
**Options classified:** <N>
```

### Section B, The matrix

```markdown
## Matrix

|                    | **Urgent**           | **Not Urgent**       |
|--------------------|----------------------|----------------------|
| **Important**      | DO NOW               | SCHEDULE             |
| **Not Important**  | DELEGATE             | DROP                 |
```

### Section C, Per-quadrant entries

For each populated quadrant, list the options:

```markdown
### DO NOW

- **<option name>**
  - Importance: <0-3>, Urgency: <0-3>
  - Reason: <one line>
  - Action: <who, by when, success signal>
  - Source: <which prior framework named this option>

### SCHEDULE

- **<option name>**
  - Importance: <0-3>, Urgency: <0-3>
  - Calendar slot: <specific date or sprint>
  - Owner: <role or person>
  - Pre-tasks: <what must happen before this can land>

### DELEGATE

- **<option name>**
  - Importance: <0-3>, Urgency: <0-3>
  - Delegate to: <role or person>
  - Follow-up cadence: <weekly / biweekly / etc>
  - Escalation trigger: <what makes it bounce back to /solve team>

### DROP

- **<option name>**
  - Importance: <0-3>, Urgency: <0-3>
  - Rejected because: <one-line reason; will appear in Dissent appendix>
```

### Section D, Summary table

```markdown
## Summary

| Option | Importance | Urgency | Quadrant | Action |
|---|---|---|---|---|
| <name> | <0-3> | <0-3> | DO_NOW | <action> |
| ... | ... | ... | ... | ... |
```

### Section E, Decision Hook

```markdown
## Decision Hook

DO_NOW options become the dominant Decision Matrix candidates (matrix can de-emphasize options not in DO_NOW).

DROP options are removed from Decision Matrix entirely. Their entries appear in the report's Dissent appendix as "considered and rejected."

DELEGATE options are flagged for handoff. The lead's report includes the delegate names and follow-up cadence so the actions don't evaporate.

SCHEDULE options become deferred follow-ups. Each gets a specific calendar slot in the report's execution plan.
```

### Section F, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentence synthesis specific to this run. Name the dominant DO_NOW item, surface any surprising DROPs, flag any Delegate items the team hasn't yet identified an owner for.>
```

### Section G, Completeness

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- All <K> input options classified (no `unclassifiable`): +<N>
- Each populated quadrant has actions specified: +<N>
- DROP entries have rejection reasons: +<N>
- DELEGATE entries have named delegates: +<N>
- SCHEDULE entries have calendar slots: +<N>
```

---

## Decision Hook

Eisenhower's output drives Decision Matrix's option pool:

- DO_NOW items get full weighted scoring in Decision Matrix
- SCHEDULE items get scoring but flagged "execute later"
- DELEGATE items skip Decision Matrix; they go to a separate handoff section
- DROP items are removed from Decision Matrix entirely

### Confidence rubric impact

- All options cleanly classified, no quadrant overflow: +0 (this is baseline expected behavior)
- ≥ 30% of options end up in DROP: -1 (signal that option generation was poor; lower confidence)
- Any option in DELEGATE without named delegate: -1 (incomplete classification)

### Override conditions

Eisenhower does not override Decision Matrix. It pre-filters its option pool. The only indirect override: if Eisenhower marks an option DELEGATE, that option does not appear in the Decision Matrix scoring even if it would have scored highly. Decision Matrix only weighs what Eisenhower passes through.

---

## Cross-Framework Triggers

These conditions in the Eisenhower output force changes elsewhere in /solve:

### Triggers fired by quadrant distribution

- **All options in DO_NOW**: SendMessage to lead: "Eisenhower can't differentiate; option list is uniform on importance and urgency. Re-run zwicky-box with sharper differentiation, or accept that this is a single-option decision and skip Decision Matrix."
- **≥ 30% in DROP**: SendMessage flagging poor option generation; suggest re-running Phase 1 productive-thinking and zwicky-box
- **DELEGATE with no named delegate**: mark `state.NEEDS_DELEGATE_RESOLUTION = true`; lead surfaces this in the report's open-questions section
- **DO_NOW + intake.time_pressure = now**: flag for confidence-speed-quality SPEED mode

### Triggers fired by content

- **Any option's Importance = 3 AND it's in DROP**: contradictory; SendMessage to lead, this is a classification error worth a manual review

---

## Failure Modes

Eisenhower can mislead in 5 ways. The framework checks for each.

### Failure Mode 1, Urgency-importance conflation

Trap: agent classifies "urgent" as "important" because the deadline pressure makes it feel important. The matrix collapses to a single column.

Manifestation: every option is in DO_NOW or DELEGATE; SCHEDULE and DROP are empty.

Check: count populated quadrants. If only 2 are populated and they're the two Urgent quadrants, the agent conflated the axes. Redo classification with explicit re-reading of `intake.success_criteria`.

Recovery: re-classify Importance against the success criteria specifically; many "urgent" items will drop to Importance ≤ 1 and move to DELEGATE or DROP.

### Failure Mode 2, Calendar-less Schedule

Trap: SCHEDULE entries with no specific date. The user reads "we'll get to it later" and the option evaporates.

Manifestation: SCHEDULE items have prose like "next sprint" or "soon" without an actual date.

Check: every SCHEDULE entry must have an ISO date or a specific sprint name (e.g. "Sprint 47").

Recovery: derive dates from `intake.time_pressure`. `this-month` SCHEDULE items default to 2-3 weeks out; `no-deadline` SCHEDULE items default to "Q3 review" or similar.

### Failure Mode 3, Delegate without owner

Trap: DELEGATE entries with vague owners ("the product team") that don't resolve to a person or follow-up.

Manifestation: DELEGATE entries have prose like "someone in product" or "ops team."

Check: every DELEGATE entry needs a role or named person plus a follow-up cadence.

Recovery: SendMessage to lead requesting a delegate-resolution round, OR re-classify the option as SCHEDULE with the /solve team as owner.

### Failure Mode 4, Drop without justification

Trap: DROP entries with no rejection reason. Future runs re-introduce the same options because the rejection wasn't documented.

Manifestation: DROP section has option names but no reason lines.

Check: every DROP entry has a "Rejected because:" one-liner.

Recovery: agent re-reads its own classification logic and writes the rejection rationale; if no clear rationale exists, the option might not be DROP after all.

### Failure Mode 5, Boundary-case dithering

Trap: agent leaves multiple options as `unclassifiable` because they're on quadrant boundaries.

Manifestation: ≥ 2 options marked unclassifiable.

Check: count unclassifiable. If > 0, the agent didn't apply the conservative-cell tiebreaker.

Recovery: apply the rule "boundary cases default to the more conservative cell" (SCHEDULE over DROP, DO_NOW over DELEGATE) and re-classify.

---

## Jargon Glossary

- **urgency**, sensitivity to deadline; calibrated to `intake.time_pressure` scope.
- **importance**, degree to which an option moves `intake.success_criteria`.
- **DO NOW**, high-importance, high-urgency; dominant Decision Matrix candidate.
- **SCHEDULE**, high-importance, low-urgency; needs a calendar slot or it evaporates.
- **DELEGATE**, low-importance, high-urgency; offload to a different owner.
- **DROP**, low-importance, low-urgency; remove from Decision Matrix entirely.
- **conservative cell**, when an option is on a quadrant boundary, default to the cell with higher commitment (SCHEDULE over DROP, DO_NOW over DELEGATE).
- **calendar slot**, specific ISO date or named sprint where a SCHEDULE item will be acted on.
- **delegate resolution**, naming the actual person or role that will execute a DELEGATE item.
- **uniform classification**, failure mode where all options land in one quadrant; signal that the option list lacks differentiation.
- **success-criteria-anchored Importance**, scoring importance against the user-stated success criterion specifically, not against gut feeling.
- **time-pressure-scaled Urgency**, calibrating the urgency cutoff to `intake.time_pressure` so "urgent" means the same thing within a single run.

---

## Completeness Scoring

Eisenhower self-rates 0-10 on triage quality.

### 10/10, Decisive
- All input options classified, no `unclassifiable`
- All 4 quadrants populated (or explicitly justified if not)
- Every DO_NOW has action + by-when
- Every SCHEDULE has calendar slot + owner
- Every DELEGATE has named delegate + follow-up cadence
- Every DROP has rejection reason
- Failure-mode self-checks all pass

### 7/10, Confident
- All input options classified
- ≥ 3 of 4 quadrants populated
- DO_NOW + DROP entries fully specified
- SCHEDULE or DELEGATE entries have minor gaps (e.g. owner named but cadence vague)

### 4/10, Tentative
- 1-2 options unclassified
- Only 2 quadrants populated (often DO_NOW + SCHEDULE only)
- DROP entries lack reasons
- Boundary-case dithering visible

### 0/10, Unusable
- Most options uniform-classified or unclassified
- DELEGATE entries with no delegates
- SCHEDULE entries with no dates
- Output reads as prose without the matrix structure

The Eisenhower completeness score feeds the overall Confidence rubric. Eisenhower completeness ≤ 4 contributes -1 to overall rubric (caps at MEDIUM bucket).

---

## Worked Example

**Problem:** "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

### Inputs going in

From `intake.json`:
- `time_pressure = this-month`
- `success_criteria = qualitative-signal` (user said "$12M TVL retention through migration")
- `decision_maker = you-with-input`

From `frameworks/cynefin.md::routing`:
- Eisenhower marked `normal` weight (not urgent-only)

From `frameworks/zwicky-box.md::archetypes` (4 candidates):
- A: big-bang single-cutover
- B: dual-deploy + drain
- C: wrapped legacy
- D: separate token + voluntary migration

Plus 4 sub-decisions from `frameworks/productive-thinking.md::resource_plan`:
- E: select archetype (umbrella decision)
- F: external auditor consult
- G: user communication plan
- H: pre-migration testnet probe

### Step 1, Calibrate the urgency cutoff

`intake.time_pressure = this-month` then 2-4 weeks. Urgency = 3 means action required in next ~5 days. Urgency = 2 means action required in 2-4 weeks. Urgency = 1 means action could slip beyond the month. Urgency = 0 means no deadline pressure.

### Step 2, Score each candidate

| Option | Importance reasoning | Importance | Urgency reasoning | Urgency |
|---|---|---|---|---|
| A: big-bang | Directly affects TVL retention. High downside if cutover fails. | 3 | This-month doable but window is narrow. Action needed in 5 days. | 3 |
| B: dual-deploy + drain | Directly affects TVL retention. Recommended pattern. | 3 | Action needed in 5 days to stay on this-month track. | 3 |
| C: wrapped legacy | Solves UX surface but leaves OFTv1 contracts live. Moderate effect on retention. | 2 | Could slip past the month with limited impact. | 1 |
| D: separate token | Doesn't solve the underlying problem; users still face OFTv1. | 1 | No deadline pressure. | 0 |
| E: select archetype | Umbrella for A-D. The decision itself is the highest priority. | 3 | This is what /solve is for; action needed end of run. | 3 |
| F: external auditor | Cynefin flagged we lack external input; gates QUALITY mode. | 3 | Must land within first 2 weeks of execution. | 1 |
| G: user comms plan | Affects retention via user trust during cutover. | 2 | Must land before week 5 force-migration; not now. | 2 |
| H: testnet probe | Validates the chosen archetype against actual mempool dynamics. | 3 | Must run during weeks 1-2 of execution. | 1 |

### Step 3, Place in quadrants

- **DO_NOW** (Importance ≥ 2, Urgency ≥ 2): A, B, E, G
- **SCHEDULE** (Importance ≥ 2, Urgency ≤ 1): C, F, H
- **DELEGATE** (Importance ≤ 1, Urgency ≥ 2): (none)
- **DROP** (Importance ≤ 1, Urgency ≤ 1): D

### Step 4, Generate actions

```markdown
## Matrix

|                    | **Urgent (≤ 5 days)**| **Not Urgent**       |
|--------------------|----------------------|----------------------|
| **Important**      | A, B, E, G           | C, F, H              |
| **Not Important**  | (empty)              | D                    |

## DO NOW

- **A: big-bang single-cutover** (Imp 3, Urg 3)
  - Action: do not commit; this enters Decision Matrix as a candidate
  - Note: high-urgency placement reflects "this is one of the candidates we're picking among," not "we are doing this." Decision Matrix selects.
- **B: dual-deploy + drain** (Imp 3, Urg 3)
  - Same as A; enters Decision Matrix as a candidate.
- **E: select archetype** (Imp 3, Urg 3)
  - Action: complete /solve run, render report. Owner: this team.
  - By: end of run.
- **G: user comms plan** (Imp 2, Urg 2)
  - Action: draft comms plan parallel to Decision Matrix.
  - Owner: $PRODUCT_LEAD (delegate within DO_NOW).
  - By: 2026-05-15 (first draft).

## SCHEDULE

- **C: wrapped legacy** (Imp 2, Urg 1)
  - Calendar slot: enters Decision Matrix as a candidate, but if not selected, schedule re-evaluation at end of Q2 2026.
  - Owner: this team.
- **F: external auditor consult** (Imp 3, Urg 1)
  - Calendar slot: 2026-05-04 to 2026-05-11 (first 2 weeks of execution if migration proceeds).
  - Owner: $ENG_LEAD.
  - Pre-tasks: shortlist 3 auditors familiar with LayerZero.
- **H: testnet probe** (Imp 3, Urg 1)
  - Calendar slot: weeks 1-2 of execution, before mainnet drain.
  - Owner: this team.
  - Pre-tasks: select probe chain (recommend Base, lowest TVL).

## DELEGATE

(none)

## DROP

- **D: separate token + voluntary migration** (Imp 1, Urg 0)
  - Rejected because: voluntary migration historically completes ~30%; the remaining 70% in OFTv1 means we still own the underlying TVL retention problem. Dropping this archetype from Decision Matrix.
```

### Step 5, Decision Hook to downstream

- Decision Matrix scores A, B, C from the surviving Important options. D is removed.
- E (select archetype) is the umbrella; resolved by Decision Matrix's top pick.
- F, G, H become execution-plan items in the final report's pre-ship checklist.

### Output completeness

- All 8 candidates classified: yes
- 3 of 4 quadrants populated (DELEGATE empty, justified): yes
- DO_NOW actions specified: yes
- SCHEDULE entries have calendar slots: yes
- DROP entry has rejection reason: yes

**Completeness: 9/10** (DELEGATE empty is justified rather than absent; minus 1 for not explicitly checking whether comms plan should be DELEGATE rather than DO_NOW).

---

## What This Means For The Decision

Eisenhower's job in this OFTv2 run was to filter the option list before Decision Matrix spends weighted scoring on it. It dropped option D (separate token) so Decision Matrix only weighs A, B, C. It surfaced 3 SCHEDULE items (F, G, H) that become the execution plan's pre-ship checklist if migration proceeds. The DO_NOW dominance of B (dual-deploy + drain) and A (big-bang) plus the umbrella E previews the Decision Matrix winner.

The framework is fast, opinionated, and decisive. Skipping it means Decision Matrix weighs every candidate including the obvious DROP, diluting the top option's weighted score. Running it well means Decision Matrix only sees the candidates that actually matter.
