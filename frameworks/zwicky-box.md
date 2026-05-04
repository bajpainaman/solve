# Zwicky Box (Morphological Analysis)

**Phase:** Define · **Source:** https://untools.co/zwicky-box

Zwicky Box decomposes a problem into independent design dimensions, lists every plausible option per dimension, then explores the full Cartesian product to surface combinations the team would never have brainstormed unaided. The output is not a single recommendation. It is a structured solution space and a small set of named archetypes that the Decision Matrix later scores.

The framework matters because most teams converge on 2-3 obvious options early, lock in the framing, and never see the combination that would have been better. Zwicky forces breadth before convergence. When you skip it, your decision matrix has options A, B, C and the actual best answer was the unexplored A+C+modifier-Y combo.

---

## Entry Predicate

```
∃ ≥ 2 independent design dimensions in problem
∧ intake.problem_refined describes a system with multiple knobs (architecture, mechanism, scope, audience, timing)
```

The framework runs whenever the problem permits at least two orthogonal axes that can be varied independently. A single-axis question (do we deploy on Tuesday or Wednesday) does not warrant Zwicky. A multi-axis question (which migration mechanism, on which chains, with what user-facing transition) does.

If the predicate fails (true single-axis decision), skip Zwicky and feed `intake.problem_refined` directly to Decision Matrix as a binary or trinary option set.

### Inputs

- `intake.problem_refined` — the canonical problem statement. Dimensions must serve this question, not a related one.
- `intake.domain` — eng / product / strategy / general. Domain shapes which axes are typical.
- `intake.success_criteria` — measurable-metric / qualitative-signal. Drives which dimensions matter for archetype filtering.
- `frameworks/first-principles.md::atomic_truths` — atomic truths constrain which options on each dimension are physically plausible. Options that violate first-principles get pruned before clustering.
- `frameworks/issue-tree.md::leaves` — issue-tree leaves often map directly onto Zwicky dimensions. Use the tree's MECE structure to seed the axes.
- `frameworks/abstraction-ladder.md::target_rung` — the target rung sets the level at which dimensions live. Too high and dimensions become philosophical. Too low and they become implementation toggles.
- `frameworks/inversion-define.md::failure_modes` — failure modes constrain which combos survive filtering. A combo that triggers a known failure mode gets cut.
- `evidence/define-prior-art.md` — prior protocol or product migrations that already explored this space. If three teams chose the same archetype before, that archetype gets named after their pattern.

### Outputs

- `$RUN_DIR/frameworks/zwicky-box.md` — the matrix, the filter rules, the surviving combos, and 4-7 named archetypes
- `state.json` `zwicky.archetypes` field — array of archetype names consumed by Decision Matrix as the option set
- `$RUN_DIR/evidence/zwicky-axis-<n>.md` — one file per dimension produced by parallel research fan-out

---

## Operating Principles

These five rules are non-negotiable. Violating any of them produces a Zwicky output that looks complete but misroutes downstream.

**1. Dimensions must be orthogonal.**

Two dimensions are orthogonal when changing one does not constrain the other. If choosing "monolith" on the architecture axis forces "single-region" on the deployment axis, the axes are dependent and the matrix is misleading. Test orthogonality by asking: can I name a real-world system that mixes any cell on axis A with any cell on axis B? If no, the axes are entangled. Anti-pattern: listing "language" and "framework" as separate axes when the team has already decided Rust, in which case framework collapses to axum or actix and the axis is dependent.

**2. Options per dimension must be exhaustive within the abstraction rung.**

If your axis is "data store" and you list postgres, mongo, dynamodb, you have probably skipped sqlite, redis, cassandra, kafka-as-store, and fs-only. The Zwicky output is only as good as its option lists. The standard is 3-7 options per dimension, where 3 is the floor and 7 is the cap to avoid combinatorial explosion. If you find an option you forgot after clustering, redo the matrix. Anti-pattern: 3 options per axis that all cluster on the same vendor's ecosystem (postgres, supabase, neon all collapse to "managed postgres").

**3. Filter before clustering.**

The full Cartesian product of 5 axes with 4 options each is 1024 combinations. You cannot reason about 1024 combinations. Apply filter rules from inversion-define and first-principles to prune to a manageable set (typically 30-80) before clustering into archetypes. Filter rules must be explicit and source-cited. Anti-pattern: jumping directly from the matrix to 4 favorite combos without showing the filter step. The Decision Matrix downstream cannot trust the option set if the filter was implicit.

**4. Archetypes must be named, not numbered.**

An archetype called "Combo 3" is invisible to humans. An archetype called "dual-deploy + drain" lives in the team's vocabulary for years. Names should encode the strategic shape, not the components. Good name: "wrapped legacy" (encodes the strategy of preserving old contracts behind a new wrapper). Bad name: "option C" or "v2 with adapter." Anti-pattern: archetype names that are technical labels rather than strategic shapes.

**5. The output is a solution space, not a recommendation.**

Zwicky does not pick. Zwicky enumerates. The output goes to Decision Matrix, which scores. If your Zwicky output ends with "we recommend archetype X," you have collapsed two frameworks into one and the team will not see the trade-offs. Anti-pattern: writing a one-paragraph recommendation at the end of the Zwicky output. Save it for Decision Matrix.

---

## Response Posture

**Tone.** Generative, then converging. The first half (dimensions and options) is breadth-mode, ask "what else." The second half (filter and cluster) is rigor-mode, ask "why this combo, not that one."

**Pacing.** Asynchronous. The framework spawns a parallel research subtask per axis. Definer collates after all axis researchers report. Do not block on a slow axis; run filtering on the surviving axes and add the slow one when it lands.

**Push depth.** Push hard on dimension orthogonality. If the user names two axes that depend on each other, refuse to proceed until they collapse to a single axis or restructure. Push moderately on option exhaustiveness; the team often forgets one or two and accepts the prompt to add them. Push lightly on archetype naming; teams have taste here, accept reasonable names.

**Where to escalate.** SendMessage to lead when:
- The full Cartesian product exceeds 2000 combos (axes too granular or too many)
- After filtering, fewer than 6 combos survive (filter rules too aggressive, or the problem is genuinely binary)
- An axis cannot be researched (no prior art, no expert) and three other axes already produced 5+ options each (the missing axis suggests a different framework, possibly first-principles second pass)

---

## Anti-Sycophancy Rules

The agent running Zwicky must never write these:
- "Great list of options, here are some additional ones to consider..." (generate them, do not announce them)
- "These archetypes seem reasonable, though we could explore more..." (commit to the set or expand it; do not hedge)
- "Combo 7 is interesting because it combines several elements..." (state what strategic shape it represents and why that shape matters)
- "There are many ways to approach this problem..." (cut to dimensions)

The agent must always:
- Take a position on which combos survive the filter, with the explicit rule cited.
- Name the archetype with a strategic-shape phrase, not a label.
- Name the dimension that is most likely missing (the team's blind spot), even if the user has not asked.
- Name the cell that has zero documented prior art (highest novelty risk for the Decision Matrix).

---

## Pushback Patterns

These are the most common failure shapes when teams run Zwicky for the first time. The agent applies these self-checks during execution.

**Pattern 1: dependent axes posing as independent**

- User input: "Axes are language, framework, deployment platform."
- BAD: "Got it, listing options for each."
- GOOD: "Language and framework are dependent. Choosing Rust collapses framework to axum-or-actix. Choosing TypeScript opens it to next-or-remix-or-nest. Either merge into a single 'stack-pick' axis with named bundles (rust+axum, ts+next, ts+nest, etc.) or keep language as the axis and drop framework. Pick one."

**Pattern 2: too few options per axis**

- User input: "Storage axis: postgres, mongo."
- BAD: "Two options for storage, that works."
- GOOD: "Two options is below the floor of 3. Storage candidates you have not listed: sqlite (single-node, embedded), dynamodb (managed kv), kafka-as-store (event sourcing), redis-as-primary (in-memory durable). For your TVL profile, sqlite and redis-as-primary fail the durability test, but dynamodb and kafka-as-store should be on the matrix. Add at least one more or justify why the answer is binary."

**Pattern 3: archetypes named after components, not shapes**

- User input: "Archetype 1 is postgres + monolith + JWT. Archetype 2 is mongo + microservices + sessions."
- BAD: "Two archetypes captured."
- GOOD: "These are component lists, not archetypes. The strategic shape of archetype 1 is 'tight-coupled relational stack with stateless auth,' which I would call 'rails-style canonical.' Archetype 2 is 'document-store with stateful auth across services,' which I would call 'session-aware federation.' Names matter because Decision Matrix downstream needs to weight criteria against the shape, not against an arbitrary label."

**Pattern 4: filtering implicit**

- User input: "Out of 256 combos, here are the 4 we picked."
- BAD: "Solid shortlist."
- GOOD: "256 to 4 is a 64x cut with no rule shown. State the filter explicitly. Inversion-define listed 7 failure modes; show which combos got cut by which failure mode. First-principles named 3 atomic truths; show which combos violate one. If 252 cuts cannot be traced to a rule, the option set is taste, not analysis, and the Decision Matrix cannot trust it."

**Pattern 5: missing axis covered by the abstraction-ladder**

- User input: "Five axes: architecture, language, deployment, storage, auth."
- BAD: "Five axes, looks complete."
- GOOD: "abstraction-ladder.md target rung is 'decide migration approach.' At that rung, two axes are missing: 'user-side coordination' (forced cutover, voluntary, dual-rail) and 'rollback envelope' (instant, costly, irreversible). The five technical axes you listed are below the target rung. Pull them up or add the missing two. Decision Matrix needs the user-side axis to weigh against engineering cost."

---

## Method

Zwicky runs as an 8-step procedure. Steps 4-5 fan out to parallel research subagents.

### Step 1, Read prior framework outputs and intake

```bash
ls $RUN_DIR/frameworks/ | grep -E '(abstraction-ladder|first-principles|issue-tree|inversion-define)'
cat $RUN_DIR/intake.json
```

The agent reads the abstraction-ladder target rung, the first-principles atomic truths, the issue-tree MECE leaves, and the inversion-define failure modes. Without these, dimensions are guesses. Failure mode of skipping: dimensions live at the wrong rung.

### Step 2, Identify candidate dimensions

Brainstorm 6-10 candidate dimensions. The candidate list is later filtered to 3-5 final axes. Source candidates from:
- Issue-tree branches (each top-level branch is often a dimension)
- Domain conventions (eng problems usually include architecture, storage, auth; product problems usually include audience, mechanism, channel)
- The user's own framing (axes the user named in the problem statement)
- Inversion (axes whose absence created prior failure modes)

Output type: bullet list of candidate dimensions with one-line gloss each. Failure mode: brainstorming axes too late or too narrow, missing the strategic ones.

### Step 3, Filter to 3-5 orthogonal dimensions

Apply orthogonality test to each pair. If two dimensions are dependent, either merge them into a bundle axis or drop the more derivative one. Cap the final count at 5 (more axes inflate the Cartesian product without producing better archetypes). Floor is 3 (fewer than 3 collapses Zwicky into a 1D or 2D analysis better served by issue-tree or impact-effort).

Output type: numbered list of 3-5 final dimensions with definition. Failure mode: keeping 6+ axes, blowing the Cartesian product to thousands of combos.

### Step 4, Fan out to parallel axis research

```text
For each dimension D:
  TaskCreate(id="T-research-zwicky-axis-<D>", owner="researcher",
             description="enumerate options for axis <D> on problem <SLUG>")
  SendMessage(to="researcher", brief={
    "axis": "<D>",
    "scope": "list 3-7 options that fit at the abstraction rung defined by intake.target_rung",
    "constraints": "<atomic-truths from first-principles>",
    "deliverable": "$RUN_DIR/evidence/zwicky-axis-<D>.md"
  })
```

Each axis researcher returns a markdown file with options, prior art per option, and known constraints. Failure mode: researchers return options at different abstraction rungs, making the matrix incoherent.

### Step 5, Collate the matrix

Once all axis files are written, build the matrix as a markdown table:

| Dimension | Option 1 | Option 2 | Option 3 | Option 4 |
|---|---|---|---|---|
| Architecture | <a1> | <a2> | <a3> | <a4> |
| Storage | <s1> | <s2> | <s3> | <s4> |

Total combinations equal product of option counts. Capture this number explicitly in the output. Failure mode: building the matrix without showing the combinatorial total, hiding the scope of the filter that follows.

### Step 6, Apply filter rules

Read inversion-define.md and first-principles.md. Extract filter rules in the form `combo violates rule R if <condition>`. Apply each rule to the full Cartesian product, marking surviving combos. Track cut counts per rule for transparency.

Output type: filter table.

| Rule source | Rule | Combos cut | Combos remaining |
|---|---|---|---|
| first-principles atomic-truth-1 | option <X> on axis A breaks invariant <Y> | <N> | <N> |
| inversion-define failure-mode-3 | option <P> on axis B and option <Q> on axis C jointly trigger <FM> | <N> | <N> |

Surviving combos must remain ≥ 8 to support meaningful clustering. If fewer survive, the filter is too aggressive or the problem is genuinely narrower than Zwicky-shaped. Failure mode: filtering too aggressively then declaring the problem is binary, when the matrix would have shown 5+ archetypes if rules were applied as stated.

### Step 7, Cluster surviving combos into archetypes

Group surviving combos by strategic shape. Two combos belong to the same archetype if they answer the canonical question the same way at the level of intent, even if they differ on lower-level details. Aim for 4-7 archetypes. Fewer than 4 means clustering is too coarse; more than 7 makes Decision Matrix downstream unwieldy.

Each archetype gets:
- A strategic-shape name (2-4 words)
- A one-paragraph definition of what the archetype does
- The list of constituent surviving combos
- The dominant trade-off the archetype accepts
- Prior art reference (a real-world system following this archetype)

Failure mode: clustering by superficial similarity instead of by strategic intent. "All combos with postgres" is not an archetype; it is a coincidence.

### Step 8, Write output and feed Decision Matrix

Write `$RUN_DIR/frameworks/zwicky-box.md` per the Output Schema. Update `state.json` with:

```json
{
  "zwicky": {
    "axes_count": 4,
    "options_total": 256,
    "options_after_filter": 38,
    "archetypes": ["big-bang", "dual-deploy+drain", "wrapped-legacy", "separate-token-voluntary"],
    "archetype_count": 4
  }
}
```

The Decision Matrix reads `state.zwicky.archetypes` as its option set.

Failure mode: writing archetypes to the markdown but not updating state.json, causing Decision Matrix to fall back on issue-tree leaves as options, which are at the wrong rung.

---

## Question Patterns

Zwicky asks the user few direct questions; most work is analytical. The user-facing questions appear in three places.

### Question 1, dimension confirmation

> "I have identified 5 candidate dimensions for this problem: <list>. The first three (X, Y, Z) appear orthogonal. The last two (W, V) appear dependent on X. I propose merging W into a bundle axis with X. Confirm or restate."

Good answer shape: user confirms or restates with a specific reason ("V is not actually dependent on X because <case>"). Red flag: user accepts without engaging; this often means the dimensions do not match the user's actual decision.

Smart-skip: if `intake.domain = eng` and dimensions match the canonical eng pattern (architecture, storage, auth, deployment), skip the question and proceed.

### Question 2, missing axis check

> "Reading abstraction-ladder.md, the target rung is <X>. The dimensions I have are below the rung. Should I pull them up or add a higher-rung dimension (typical candidates: <list>)?"

Good answer shape: user names the higher-rung dimension or accepts the current set with rationale. Red flag: "let's keep it simple"; the simple version often misses the dimension that matters most.

### Question 3, archetype naming

> "I have clustered surviving combos into 4 archetypes. I propose names: A1, A2, A3, A4. Each name encodes the strategic shape (not the components). Reword any name that does not fit your team's vocabulary."

Good answer shape: user accepts or substitutes with team-specific names. Red flag: user proposes names that are component lists (postgres+monolith); push back.

---

## Forcing Exemplars

Each of the four major Zwicky outputs has a softened version (avoid) and a forcing version (aim for).

### Exemplar 1, Naming a dimension

SOFTENED (avoid):
> "Architecture is a possible dimension."

FORCING (aim for):
> "Architecture is dimension 1. It splits along: monolith (single deployable, all-in-process), modular monolith (single deployable, hard module boundaries), microservices (many deployables, network boundaries), serverless (event-driven, no long-lived process). The axis is orthogonal to storage because each architecture supports each storage option without modification. The axis is at the target rung from abstraction-ladder.md (decide migration approach) and not at the lower rung (which framework)."

### Exemplar 2, Filtering a combo

SOFTENED (avoid):
> "We removed combos that did not seem viable."

FORCING (aim for):
> "Filter rule R3 from inversion-define.md::failure-mode-2 ('partial migration with two-phase commit causes frozen funds during outage'): any combo with architecture=microservices and migration-mechanism=phased-cutover violates R3 because the network partition between services creates the frozen-funds window. Combos cut by R3: 16 (4 storage options × 4 auth options × 1 architecture × 1 mechanism). Combos remaining after R3: 240."

### Exemplar 3, Naming an archetype

SOFTENED (avoid):
> "Archetype 2 uses dual-deploy with a draining mechanism."

FORCING (aim for):
> "Archetype 2: dual-deploy + drain. Strategic shape: ship the new system alongside the old, route new traffic to new, drain old at a controlled rate, decommission old after drain completes. Trade-off accepted: extended dual-rail period (typically 4-8 weeks) in exchange for clean rollback envelope and zero forced cutover. Prior art: Stargate's OFTv1-to-OFTv2 migration ran dual-deploy for 6 weeks. Constituent surviving combos: 12, all share architecture ∈ {monolith, modular monolith}, mechanism = phased, user-coordination = optional."

### Exemplar 4, Handing off to Decision Matrix

SOFTENED (avoid):
> "These archetypes can be evaluated in the Decision Matrix step."

FORCING (aim for):
> "Decision Matrix receives 4 archetypes as the option set: big-bang, dual-deploy + drain, wrapped legacy, separate-token + voluntary. Each archetype's dominant trade-off is captured in zwicky-box.md and the Decision Matrix should weight 'reversibility' as the criterion that splits big-bang (one-way-door) from the other three (rollback envelope ranges from days to weeks). Skip the Hard Choice fallback unless big-bang scores within 5% of the top alternative; the irreversibility makes that gap meaningful."

---

## Output Schema

The framework output at `$RUN_DIR/frameworks/zwicky-box.md` follows this exact structure.

### Section A, Header

```markdown
# Zwicky Box, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** abstraction-ladder.md, first-principles.md, issue-tree.md, inversion-define.md, evidence/zwicky-axis-*.md
**Combinatorial total:** <N options>
**After filter:** <M combos>
**Archetypes:** <K names>
```

### Section B, Dimensions table

```markdown
| Axis | Definition | Options | Source for options |
|---|---|---|---|
| <axis 1> | <one-line> | <opt1, opt2, opt3, opt4> | <evidence file> |
```

Every option must trace to a source. Options without sources get a TODO line and a research task is created.

### Section C, Matrix grid

```markdown
| Dimension | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Architecture | monolith | modular-monolith | microservices | serverless |
| Storage | postgres | mongo | dynamodb | sqlite |
| Auth | session | jwt | oauth | passkeys |
```

Column types: every option is a string. Allowed values: any string at the abstraction rung defined by abstraction-ladder.

### Section D, Filter rules and cuts

```markdown
| Rule ID | Source | Rule | Combos cut | Remaining |
|---|---|---|---|---|
| R1 | first-principles.atomic-truth-1 | <rule> | <N> | <N> |
| R2 | inversion-define.failure-mode-3 | <rule> | <N> | <N> |
```

Rules must be deterministic (a script could replay them). The total cut must reconcile to (combinatorial total minus survivors).

### Section E, Surviving combos (sample)

```markdown
| Combo ID | Architecture | Storage | Auth | Migration | Cluster archetype |
|---|---|---|---|---|---|
| C014 | monolith | postgres | session | dual-deploy | dual-deploy+drain |
| C027 | monolith | postgres | session | phased | dual-deploy+drain |
| C081 | modular-monolith | postgres | jwt | dual-deploy | dual-deploy+drain |
```

Show all surviving combos if there are fewer than 30. If more than 30, show 10 sample rows from each archetype cluster and link to a full table appendix.

### Section F, Archetype definitions

```markdown
## Archetype 1: <name>

**Strategic shape:** <2-3 sentences on what the archetype does at the level of intent>
**Trade-off accepted:** <the one trade the archetype makes consciously>
**Prior art:** <real-world system that ran this archetype>
**Constituent combos:** C014, C027, C081, ...
**Dominant cell pattern:** architecture ∈ {monolith, modular-monolith}, mechanism = phased

**When this archetype wins:** <conditions under which Decision Matrix should score this high>
**When this archetype loses:** <conditions under which it scores low>
```

Repeat for each archetype.

### Section G, Decision Matrix handoff

```markdown
## Decision Matrix Option Set

The following archetypes are passed to Decision Matrix as the option set:

1. <archetype-1-name>
2. <archetype-2-name>
3. <archetype-3-name>
4. <archetype-4-name>

Suggested criteria the Decision Matrix should include (these came up in archetype trade-off analysis):
- Reversibility (split big-bang from drain-style)
- Engineering effort
- User-side coordination cost
- Time-to-cutover
- Rollback envelope
```

### Section H, What This Means For The Decision

```markdown
## What This Means For The Decision

<2-3 sentences on what the archetype set tells the team. Specific, decision-actionable.>
```

### Section I, Completeness Score

```markdown
**Completeness:** <N>/10
```

---

## Decision Hook

Zwicky's output is a solution space, not a decision. It feeds Decision Matrix as the option set.

### Per-archetype framework feed

| Receiving framework | What it consumes |
|---|---|
| Decision Matrix | archetype list as options; trade-off summary as suggested criteria |
| Impact-Effort | archetype list to plot 2x2 |
| Eisenhower | archetype list, urgency-importance triage per archetype |
| Second-Order | archetype list to walk 2-3 levels of consequence per archetype |
| Hard Choice | the two top-scoring archetypes from Decision Matrix, if their scores are within 5% |
| Six Hats | each archetype gets evaluated by all 6 hats |

### Confidence rubric impact

- Zwicky archetype count between 4 and 6 with one clearly dominant trade-off, +1 to overall confidence
- Zwicky archetype count of 1-2 (genuinely binary problem after rigorous filter), +1 to confidence (but flag as Zwicky-not-applicable in retrospect)
- Zwicky archetype count > 7 (overcrowded, Decision Matrix will struggle), 0 to confidence; recommend re-clustering
- Filter rules cut < 30% of combos (too permissive, surviving set may include unrealizable combos), -1 to confidence

### Override conditions

Zwicky does not override other frameworks. It populates the option set. The override that matters: if Decision Matrix scores all archetypes within 10% of each other, the framework signals that Zwicky's clustering was insufficient (the archetypes are not strategically distinct) and recommends re-running Zwicky with finer cluster definitions.

---

## Cross-Framework Triggers

Specific Zwicky outputs trigger downstream actions or hand off to other skills.

- `zwicky.archetype_count = 1` after filter, the problem is genuinely a single solution; SendMessage to lead, recommend skipping Decision Matrix and going directly to Second-Order on the single archetype
- `zwicky.archetype_count > 7`, signal Decision Matrix to not run and instead re-cluster. Often this happens when filter rules were too lax; re-run with a stricter cut
- `zwicky.surviving_combos = 0`, hard halt. Filter rules over-cut, the problem may be infeasible as stated. SendMessage to lead recommending re-run of Phase 1 with relaxed first-principles or revised inversion-define
- An archetype with no documented prior art (novel combination), flag for `/plan-eng-review` at end of run because architecture is novel and warrants pre-implementation review
- An archetype that contradicts a stated atomic-truth from first-principles, push back to first-principles step; one of them is wrong

---

## Failure Modes

Zwicky misleads in five distinct ways. The framework runs each self-check before completing.

### Failure Mode 1, Dimensions at the wrong rung

Trap: Axes are at a rung below abstraction-ladder.md::target_rung. The matrix produces archetypes that are implementation-detail bundles rather than strategic options.

Manifestation: archetype names are technology stacks ("postgres+next+vercel") rather than strategic shapes ("managed-stack canonical").

Check: each axis must be representable in 1-3 words at the abstraction-ladder rung. If you cannot describe the axis without naming a vendor, the axis is too low.

Recovery: pull each axis up one rung. Re-list options at the new rung. Re-cluster.

### Failure Mode 2, Dependent axes treated as independent

Trap: Two axes secretly depend on each other; the Cartesian product includes combos that are physically impossible.

Manifestation: surviving combos after filter include cells that nobody in prior art has ever shipped, because they cannot ship.

Check: the orthogonality test in Operating Principle 1. Can you name a real system that combines axis-A:opt2 with axis-B:opt3? If no real system has, that combo is suspect.

Recovery: merge the dependent axes into a bundle axis with named bundles. Re-run the matrix.

### Failure Mode 3, Filter rules implicit, archetype set is taste

Trap: The team jumps from the matrix to a favorite shortlist without showing how the filter rules cut the rest.

Manifestation: filter table missing or sparse; surviving combos appear without a rule trace.

Check: every cut combo must trace to a rule. If filter table cuts < 90% of the cut combos with explicit rules, the rest is implicit and the archetype set is taste, not analysis.

Recovery: re-run filter step with explicit rules. If a rule cannot be articulated, that is a Zwicky-skill failure (filter is intuition rather than logic) and the surviving set is unreliable.

### Failure Mode 4, Archetypes named by component, not strategic shape

Trap: Each archetype is named after its dominant components ("postgres-monolith") rather than its strategic shape ("rails-style canonical").

Manifestation: archetype names contain technology nouns; Decision Matrix downstream cannot weight against shape because the name does not encode shape.

Check: every archetype name must pass the "5-year test." Read the name in 5 years. Does it tell you what the archetype does, or only which technologies were in fashion when it was written?

Recovery: re-name. Use 2-4 word phrases that encode strategic intent.

### Failure Mode 5, Skipping Zwicky for "obvious" 2-option problems

Trap: The problem is framed as binary (do it / do not do it). Zwicky predicate fails superficially. But the problem actually has 3-5 dimensions hidden under the binary framing.

Manifestation: Decision Matrix downstream runs on 2 options that are at the highest rung, missing the 4-5 strategic shapes a Zwicky would have surfaced.

Check: any time intake.problem_refined contains "should we do X" without naming the alternatives, run Zwicky anyway with X as one cell on a "scope" axis.

Recovery: re-run Phase 1 step 6 (Zwicky) with the binary expanded into 3-5 axes.

---

## Jargon Glossary

- dimension, an axis of the solution space along which options vary independently. Synonym for axis.
- axis, see dimension.
- option, one valid value on a dimension; e.g. monolith on the architecture axis.
- combo, a tuple selecting one option per axis; one row in the Cartesian product.
- Cartesian product, the full set of combos formed by picking one option from each axis; size is the product of option counts per axis.
- orthogonal, two axes are orthogonal when changing one does not constrain the other.
- bundle axis, an axis whose options are pre-bundled groups of correlated picks; used when two natural axes are dependent.
- filter rule, a deterministic rule that cuts combos based on a constraint from first-principles or inversion-define.
- archetype, a named cluster of surviving combos that share a strategic shape.
- strategic shape, the level of intent at which two combos are "the same idea" even if their lower-level details differ.
- target rung, the abstraction level at which dimensions live, set by abstraction-ladder.md.
- novelty risk, an archetype with no documented prior art; high uncertainty for Decision Matrix to score.
- combinatorial explosion, the failure mode where too many axes or options produce a Cartesian product too large to reason about (typically > 1000 combos).
- prune, to remove combos via filter rules.
- cluster, to group surviving combos by strategic shape into archetypes.
- option set, the final list of archetypes passed to Decision Matrix.

---

## Completeness Scoring

The Zwicky output self-rates 0-10 based on this rubric.

### 10/10, Decisive option set

- 4-5 dimensions, each orthogonal to the others (orthogonality test passes for every pair)
- 3-7 options per axis, each option traced to a source (evidence file or prior art)
- Combinatorial total stated; filter rules cut 70-95% of combos with each cut traced to an explicit rule
- 4-7 archetypes, each named with a strategic-shape phrase, each with prior art reference, each with dominant trade-off named
- Decision Matrix option set is the archetype list with no leakage of unfiltered combos
- Cross-framework triggers checked; novel-archetype flag set if applicable

### 7/10, Useful

- 3-5 dimensions, mostly orthogonal (one pair partially dependent, flagged but not merged)
- 3-5 options per axis, most traced to a source (1-2 axes have options without explicit prior art)
- Filter rules cut 50-70% of combos with most cuts traced to rules (a few implicit cuts noted)
- 4-7 archetypes, mostly named with strategic-shape phrases (1-2 named partially by component)
- Decision Matrix option set is usable; Decision Matrix scores will be reliable

### 4/10, Tentative

- 3-4 dimensions, orthogonality not validated rigorously
- 3 options per axis on average, fewer than half traced to sources
- Filter rules cut < 50% of combos or rules are partially implicit
- 3-7 archetypes, naming inconsistent (mix of shapes and components)
- Decision Matrix can run but scores will reflect Zwicky's noise

### 0/10, Untrustworthy

- < 3 dimensions, or all dimensions dependent on one master axis
- 1-2 options per axis (matrix collapses)
- Filter rules absent or fully implicit
- Archetype names are numeric labels or arbitrary
- Decision Matrix cannot trust the option set; recommend re-running Zwicky

The completeness score appears in the Zwicky output. A Zwicky completeness ≤ 4 caps Decision Matrix's confidence at MEDIUM until Zwicky is re-run.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This is the canonical example used across all framework files. The Zwicky output here feeds Decision Matrix in Phase 3.

### Intake state going in

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

### Prior framework outputs consumed

- abstraction-ladder, target rung is "decide migration approach"
- first-principles, atomic truths: bridges must allow value transfer, gas costs must be predictable, users must not lose funds, message encoding must be backward-compatible during dual-rail period
- issue-tree, branches: technical migration mechanism, user-side coordination, audit requirements, operational runbook
- inversion-define, failure modes: partial migration with frozen funds, double-spending across chains during transition window, UX confusion at the cutover moment, audit timeline slip blocking deploy

### Step 1-2: identify candidate dimensions

Reading prior outputs, candidate dimensions:

1. Migration mechanism (how the new contract receives state from the old)
2. User-side coordination (how users move from old to new)
3. Rollback envelope (how reversible the migration is at each phase)
4. Audit scope (how the new code path is verified)
5. Cutover timing (instant, phased, indefinite dual-rail)
6. Token identity (same name/symbol on new contract, or new identity)
7. Chain coverage (all 4 chains together, or one chain at a time)

### Step 3: filter to 4 orthogonal dimensions

- Migration mechanism and Rollback envelope are dependent (mechanism determines envelope). Merge into a bundle axis.
- Audit scope is partially dependent on mechanism but offers an independent variation (full re-audit vs. delta-audit). Keep as separate axis.
- Cutover timing and User-side coordination are partially dependent. Merge into bundle axis "Coordination strategy."
- Token identity is independent of the rest. Keep.
- Chain coverage is independent. Keep.

Final 4 axes:
1. **Migration mechanism + rollback** (bundle): big-bang-cutover (no rollback), phased-cutover (rollback within phase), dual-deploy-with-drain (full rollback during dual period), wrapped-legacy (no migration, just front)
2. **Coordination strategy**: forced (users must migrate), incentivized (users get rewards to migrate), voluntary (users choose, no incentive), invisible (UX hides the migration)
3. **Token identity**: same-name-and-symbol, new-name-and-symbol-with-rebrand, dual-identity-during-period
4. **Chain coverage**: simultaneous-all-chains, leader-chain-first-then-others, per-chain-independent

### Step 4: fan out to research

Researcher subagent receives 4 tasks, one per axis. Each returns evidence file with options and prior art:

`evidence/zwicky-axis-1-migration.md`:
- big-bang-cutover, prior art: small testnet migrations, no large-TVL examples
- phased-cutover, prior art: Compound v2 to v3, Uniswap v2 to v3
- dual-deploy-with-drain, prior art: Stargate USDC migration, Radiant v1 to v2, Ethena USDe rebase
- wrapped-legacy, prior art: WBTC wrapping pattern, Aave aTokens

`evidence/zwicky-axis-2-coordination.md`:
- forced, prior art: Curve crvUSD migration (forced after deadline)
- incentivized, prior art: Aave v2 to v3 (incentivized via emissions)
- voluntary, prior art: Maker DSR migrations
- invisible, prior art: 1inch limit-order migrations (router upgrade transparent to user)

`evidence/zwicky-axis-3-identity.md`:
- same-name-and-symbol, prior art: most v2-to-v3 migrations
- new-name-and-symbol, prior art: rebrands (FTT to FTT2 was abandoned, MKR to TKN, etc.)
- dual-identity, prior art: Lido stETH and wstETH coexistence

`evidence/zwicky-axis-4-chain.md`:
- simultaneous-all-chains, prior art: most LayerZero-native migrations attempted simultaneously
- leader-chain-first, prior art: Stargate launched on Ethereum then expanded
- per-chain-independent, prior art: most LayerZero v1 deployments started this way

### Step 5: collate matrix

| Dimension | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Migration mechanism + rollback | big-bang-cutover | phased-cutover | dual-deploy-with-drain | wrapped-legacy |
| Coordination strategy | forced | incentivized | voluntary | invisible |
| Token identity | same-name-and-symbol | new-name-and-symbol | dual-identity-during-period | (n/a) |
| Chain coverage | simultaneous-all-chains | leader-chain-first | per-chain-independent | (n/a) |

Combinatorial total: 4 × 4 × 3 × 3 = 144 combos.

### Step 6: apply filter rules

| Rule ID | Source | Rule | Combos cut | Remaining |
|---|---|---|---|---|
| R1 | first-principles atomic-truth-3 (users must not lose funds) | mechanism = big-bang-cutover and coordination = voluntary or invisible (users do not know cutover happened) | 8 | 136 |
| R2 | first-principles atomic-truth-4 (message encoding backward-compat during dual-rail) | mechanism = big-bang-cutover (no dual-rail at all) requires identity = same-name-and-symbol (user balance preservation). Cuts big-bang × new-name and big-bang × dual-identity | 6 | 130 |
| R3 | inversion-define failure-mode-1 (partial migration frozen funds) | mechanism = phased-cutover and chain = simultaneous-all-chains (all-chain phase concurrently is a single failure point) | 12 | 118 |
| R4 | inversion-define failure-mode-2 (double-spend during transition) | mechanism = wrapped-legacy and identity = same-name-and-symbol (wrapping the same identity creates double-spend window) | 4 | 114 |
| R5 | inversion-define failure-mode-3 (UX confusion at cutover) | mechanism = big-bang-cutover and coordination = forced (deadline cliff with no incentive creates UX cliff) | 3 | 111 |
| R6 | atomic-truth-2 (gas predictable) | chain = per-chain-independent and mechanism = dual-deploy (running parallel drains on all 4 chains independently spikes gas during overlap) | 12 | 99 |
| R7 | issue-tree audit branch (audit scope must complete pre-deploy) | identity = new-name-and-symbol and audit timeline already constrained to this-month, time pressure rule cuts | 18 | 81 |
| R8 | inversion-define failure-mode-4 (audit slip blocks deploy) | mechanism = big-bang-cutover requires full re-audit, time-pressure = this-month means full re-audit infeasible, cut all big-bang | 16 | 65 |

After filter, 65 combos remain. (Note: rule R8 supersedes some earlier R1-R5 cuts; the count reconciliation is 144 - 79 unique cuts = 65.)

### Step 7: cluster surviving combos into archetypes

Reading the 65 surviving combos by strategic shape:

**Archetype 1: dual-deploy + drain**
- Strategic shape: ship OFTv2 alongside OFTv1, route new bridge volume to OFTv2, drain OFTv1 over 4-8 weeks via incentivized migration, decommission OFTv1 after drain.
- Trade-off accepted: dual-rail period of 4-8 weeks with operational complexity, in exchange for clean rollback and zero forced cutover.
- Prior art: Stargate USDC migration ran 6 weeks, Radiant v1-to-v2 ran 8 weeks, Ethena USDe similar pattern.
- Constituent combos: ~24 combos (mechanism = dual-deploy-with-drain, coordination ∈ {incentivized, invisible}, identity ∈ {same-name, dual-identity}, chain ∈ {leader-chain-first, simultaneous-all-chains})
- Dominant cell pattern: mechanism = dual-deploy-with-drain across all 24
- When this archetype wins: when reversibility is costly and TVL is high enough that forced cutover risks fund loss
- When this archetype loses: when ops bandwidth cannot sustain a 6+ week dual-rail

**Archetype 2: wrapped legacy**
- Strategic shape: do not migrate. Deploy a wrapper contract that exposes OFTv2 interface but routes underlying calls to OFTv1. Existing users see no change. New integrations get OFTv2 surface.
- Trade-off accepted: long-term tech debt (two interface layers forever, gas overhead per call) in exchange for zero migration risk and zero user-side action.
- Prior art: WBTC wrapping pattern. Aave aTokens are conceptually similar.
- Constituent combos: ~16 combos (mechanism = wrapped-legacy, all coordination styles compatible because wrapping is invisible)
- Dominant cell pattern: mechanism = wrapped-legacy
- When this archetype wins: when the team has high confidence OFTv1 will not deprecate and gas overhead is tolerable
- When this archetype loses: when OFTv1 deprecation is announced or gas overhead degrades user experience materially

**Archetype 3: phased cutover with leader chain**
- Strategic shape: cutover one chain at a time starting with the lowest-TVL chain (Base, $1M TVL) as the leader, then Arbitrum, Avalanche, Ethereum in TVL order. Each chain's cutover is a controlled blast radius.
- Trade-off accepted: total migration timeline of 4-8 weeks (not parallel) in exchange for per-chain controlled rollback and learning between phases.
- Prior art: Compound v2-to-v3 (deployed Ethereum first, then expanded). Uniswap v2-to-v3 (Ethereum first).
- Constituent combos: ~15 combos (mechanism = phased-cutover, chain = leader-chain-first)
- Dominant cell pattern: mechanism = phased-cutover, chain = leader-chain-first
- When this archetype wins: when the team has high confidence in execution per chain but wants to reserve the option to halt mid-migration
- When this archetype loses: when message-encoding incompatibility forces all chains to migrate simultaneously to maintain bridge integrity

**Archetype 4: separate token + voluntary migration**
- Strategic shape: deploy OFTv2 as a separately-named token (e.g., FOO2 alongside FOO). Set up a 1:1 swap contract. Let users migrate at will. Old token remains live.
- Trade-off accepted: liquidity fragmentation across two tokens for a long period (months to years) in exchange for zero forced action and full user agency.
- Prior art: Lido stETH and wstETH coexist permanently. ENS migration kept old contracts live.
- Constituent combos: ~10 combos (mechanism = dual-deploy, coordination = voluntary, identity = new-name-and-symbol or dual-identity)
- Dominant cell pattern: identity = new-name-and-symbol or dual-identity
- When this archetype wins: when the team is comfortable with permanent fragmentation and the new features only benefit a subset of users
- When this archetype loses: when liquidity needs to consolidate (LP fees, market depth) or when the team needs to decommission OFTv1 by a deadline

### Step 8: write output and feed Decision Matrix

`state.json` updated:

```json
{
  "zwicky": {
    "axes_count": 4,
    "options_total": 144,
    "options_after_filter": 65,
    "archetypes": ["dual-deploy+drain", "wrapped-legacy", "phased-cutover-leader-chain", "separate-token-voluntary"],
    "archetype_count": 4,
    "completeness": 9
  }
}
```

Decision Matrix downstream receives 4 archetypes. Suggested criteria from Zwicky's trade-off analysis:

- Reversibility (rollback envelope per archetype)
- Engineering effort (dev-weeks to ship)
- Operational complexity during transition (ops-weeks to maintain)
- Audit scope (full re-audit, delta-audit, or wrapping-only audit)
- User-side coordination cost (forced, incentivized, voluntary, invisible)
- Gas overhead (steady-state, transient during transition)
- Bridge integrity risk (worst-case failure mode per archetype)

### What the next framework (Decision Matrix) inherits

Decision Matrix gets:
- 4 archetypes as the option set (not 144 raw combos)
- 7 suggested criteria from Zwicky's trade-off analysis
- A novel-archetype flag set to false (all 4 archetypes have prior art)
- Reversibility weight suggestion: ≥ 7 (because intake.reversibility = costly and the archetypes split sharply on this axis)
- A handoff hint: "if Decision Matrix top two are within 5%, fire Hard Choice; the 4 archetypes are strategically distinct enough that a near-tie suggests something missing."

---

## What This Means For The Decision

Zwicky is the breadth phase of Define. It is the framework that forces the team to consider combinations they would not have brainstormed under time pressure. When Zwicky runs cleanly with 4-5 orthogonal axes, explicit filter rules, and 4-7 named archetypes, the Decision Matrix downstream operates on a strategically-distinct option set and the recommendation becomes credible.

The cost of skipping Zwicky: Decision Matrix runs on 2-3 obvious options, the team locks in early framing, and the better combo (the unexplored cell) never reaches the matrix. The cost of running Zwicky badly (no orthogonality, no filter, archetype names that are component lists): Decision Matrix scores noise instead of signal, and the team gets a confident-wrong recommendation. The benefit of running Zwicky well: the Decision Matrix top option is meaningfully better than the runner-up because the option set is wide.

For this OFTv2 migration: dual-deploy + drain has the most prior art and tightest rollback envelope, but Decision Matrix should weight reversibility, ops complexity, and bridge integrity to determine whether wrapped-legacy or phased-cutover-leader-chain might score higher under specific weightings. Separate-token-voluntary should not win unless liquidity fragmentation is acceptable, which intake suggests it is not (the team values $12M TVL consolidation).
