# First Principles

**Phase:** Define (runs in Wave 1B, no dependencies on other frameworks but reads abstraction-ladder if available) · **Source:** https://untools.co/first-principles

First principles takes the problem framing and strips it down to the irreducible facts. The framework lists every assumption baked into the user's framing (and any prior framework's framing), tests each one against "is this physically/logically necessary, or just convention," keeps only the atomic truths, and rebuilds a solution from those atoms. The point is not novelty for its own sake. The point is to surface the conventional path's hidden costs so the team can see solutions the conventional frame makes invisible.

This is the assumption-stripper. Most decisions inherit framings that lock in 80% of the answer before any framework runs. First principles unlocks that 80% by naming what the framing took for granted, separating physics from convention, and rebuilding from the bottom.

---

## Entry Predicate

```
always_run
```

This framework runs on every /solve invocation. There is no condition under which it is skipped. Even when the team is confident in the conventional path, first-principles validates that the convention still applies. Skipping it on the assumption that "we know what we're doing" is the highest-cost shortcut available because conventions outlive their justification by years.

### Inputs

- `intake.problem_refined` — the user's canonical problem statement
- `intake.domain` — eng / product / strategy / general (changes which physical / regulatory / mathematical truths are relevant)
- `frameworks/abstraction-ladder.md::target_rung` — the rung the assumptions are stripped from (if abstraction-ladder ran first, which it should)
- `$RUN_DIR/evidence/define-prior-art.md` — research on conventional approaches in this domain (used to surface assumptions the user may not realize they hold)
- `$RUN_DIR/evidence/define-failure-modes.md` — historical failures (often signal which conventions broke)

### Outputs

- `$RUN_DIR/frameworks/first-principles.md` — the assumption inventory, the atomic truth list, the rebuilt framing
- `state.json` `atomic_truths` — array of truths read by zwicky-box (constrain dimensions), decision-matrix (filter options), inversion-define (validate failure paths)
- `state.json` `convention_breaks` — list of assumptions classified as convention; if any break-cost is low, this becomes a Hard Choice trigger downstream

---

## Operating Principles

These five rules govern every truth list and rebuilt framing this framework produces.

**1. Every assumption gets classified as physics, logic, regulation, or convention.**

Physics-bound assumptions cannot be challenged (the speed of light, gas costs at the EVM level, Solidity stack depth). Logic-bound assumptions are mathematically forced (a hash collision space is finite, a Merkle root is one bytes32). Regulation-bound assumptions are enforced by external rules (KYC requirements, audit thresholds). Convention-bound assumptions are choices made by other people that we inherited. Anti-pattern: lumping all assumptions as "given." Conventions look like physics until challenged.

**2. The atomic truth list must be exhaustive and minimal.**

Exhaustive: every claim downstream rests on an explicit truth, not an unstated one. Minimal: no truth is composed of other truths in the list. If truth A logically implies truth B, B is removed and A stays. Anti-pattern: writing 30 "truths" that are 15 truths and 15 paraphrases. The list is a foundation, not a brainstorm.

**3. Rebuilt framing must be different from the original or the framework was a waste.**

If the rebuilt framing reads identical to the original, the framework either failed to surface real conventions or the original was already first-principles-clean. Both are possible but rare. The default expectation is that rebuilding produces a framing that contains options the original made invisible. Anti-pattern: writing a rebuilt framing that is the original with synonyms.

**4. Convention-cost is named, not assumed.**

For every assumption classified as convention, the framework names the cost of the convention: what does following it cost in time, money, optionality, or risk? A convention with 0 cost is not worth challenging. A convention with high cost is the source of high-leverage moves. Anti-pattern: naming a convention without naming what it costs us. The cost is the entire reason to surface the convention.

**5. The framework does not break conventions, it surfaces their cost.**

The recommendation to break a convention belongs to decision-matrix, hard-choice, or the user. First-principles' job is to make the cost legible. The output should never read "we should not follow X" because that is a downstream call. The output should read "X is a convention, not a physical constraint; the cost of following it is Y; the cost of breaking it is Z." Anti-pattern: writing first-principles outputs that read as policy recommendations.

---

## Response Posture

**Tone.** Adversarial toward the framing, neutral toward the user. The framework treats the framing as something to be challenged, not adopted. Every assumption gets pushed back on. The agent does not assume the framing is good; it assumes the framing has 5-10 hidden conventions and goes hunting for them.

**Pacing.** Two-pass. First pass: list assumptions exhaustively (30-50 candidates). Second pass: classify and prune (down to 5-15 atomic truths). The two passes are not interleaved because pruning while listing causes the agent to skip assumptions it doesn't immediately recognize as convention.

**Push depth.** Maximum on assumption surfacing. The agent should produce 2-3x more candidate assumptions than will survive pruning. The discomfort of "this seems too obvious to write down" is the signal that you are surfacing a real convention. Write it down anyway, then classify.

**Where to escalate.** SendMessage to lead when:
- An assumption classified as physics turns out to have changed (e.g. "Solidity stack depth is 1024" but the team is on EOF which has different rules). This is a regime change that invalidates downstream framework outputs.
- An assumption classified as regulation turns out to be unverified (the team thinks something is required by regulation but no one has read the regulation). Spawn a research task.
- The rebuilt framing reads identical to the original after pruning. This signals the assumption surface was too narrow; expand and re-run.

---

## Anti-Sycophancy Rules

The agent running this framework must never write these:
- "It is important to note that some assumptions might be challengeable..." (cut to the assumptions, classify)
- "While the conventional approach is reasonable, alternatives exist..." (the framework does not advocate; surface conventions and their cost)
- "From a first-principles perspective, we could consider..." (drop the meta-framing; just produce the truths)
- "This framing makes sense given the constraints..." (the framing is a hypothesis; test it)

The agent must always:
- Produce ≥ 20 candidate assumptions in the first pass before pruning. Fewer indicates shallow surfacing.
- Classify every assumption explicitly as physics / logic / regulation / convention. No "depends" or "varies."
- Name the cost of every convention. A convention without a stated cost is incomplete.
- Compare rebuilt framing against original on at least 3 dimensions (problem statement, candidate solutions, constraints).
- State which conventions, if challenged successfully, would change the decision the most.

---

## Pushback Patterns

These five patterns show how the agent resists soft framing during assumption surfacing.

**Pattern 1: User said "we have to use Foundry" → check why**

- Internal evidence: user stated a tooling choice as if it were a constraint.
- BAD: "Adding 'we use Foundry' as a constraint."
- GOOD: "'We have to use Foundry' is an assumption. Why? (a) Physics/logic: no, Foundry is not the only Solidity dev framework. (b) Regulation: no, no audit requires Foundry. (c) Convention: yes, the team learned on Foundry and switched in Q1. Cost of following: zero in the short run; some lock-in to Foundry's testing patterns. Cost of breaking: rewriting test suite (estimate 2-3 weeks). Likely conclusion: not worth challenging unless there is a compelling reason. But classify it as convention so downstream frameworks know it's not a physical truth."

**Pattern 2: "We need a token" → why?**

- User submitted a problem framing that assumes a token.
- BAD: "Atomic truth: a token is required."
- GOOD: "The framing assumes a token. Why? (a) Physics/logic: no, the underlying value-transfer mechanism does not require a token (it could use signed messages, NFTs, deposit receipts, or pure on-chain accounting). (b) Regulation: depends; some jurisdictions classify tokens as securities, which is a cost not a requirement. (c) Convention: yes, the team is in DeFi and tokens are the default unit. Cost of following: regulatory exposure, secondary-market dynamics, governance overhead. Cost of breaking: novel architecture, harder to compose with existing DeFi, weaker initial liquidity. The convention is high-cost and worth challenging. Add to convention_breaks list."

**Pattern 3: "Users expect a wallet flow" → check the user**

- Internal evidence: framing assumes the standard MetaMask-style wallet flow.
- BAD: "Atomic truth: users use wallets."
- GOOD: "The framing assumes wallets. Test the assumption. (a) Physics/logic: no, signing can be done without wallets via account abstraction, embedded wallets, or session keys. (b) Regulation: no specific requirement. (c) Convention: yes, but specifically a Web3-native convention; non-Web3-native users hate it. Cost of following: 90%+ drop-off for non-Web3-native users (per AA-wallet adoption research). Cost of breaking: more infra, key custody decisions. The convention is one of the highest-cost in the framing. Add to convention_breaks. Surface to decision-matrix as a criterion: 'wallet-flow choice' should be its own dimension."

**Pattern 4: "We can't do X because of gas" → check actual gas**

- Internal evidence: the team rejected a path on gas grounds.
- BAD: "Atomic truth: gas costs prevent X."
- GOOD: "The team's rejection of X cites gas. Test this. (a) Physics/logic: gas is bounded by block gas limit (30M on Ethereum mainnet, higher elsewhere). The actual gas cost of X is not a physical constant; it depends on implementation. (b) Convention: yes, the team is using a high-cost implementation. The atomic truth is 'X must fit in the block gas limit', not 'X costs Y gas in our current implementation.' Cost of following the convention: rejecting X based on stale benchmarks. Cost of breaking: re-benchmarking X with optimized implementation; estimate 1 day. Recommended action: re-benchmark before rejecting."

**Pattern 5: "We always do Y in production" → who is "we" and what is "always"**

- Internal evidence: framing references team practices as if they were rules.
- BAD: "Atomic truth: we deploy after audit."
- GOOD: "'We always do Y' is a convention statement disguised as a fact. Three sub-questions: (a) Is 'always' true (cite 3 prior cases where it was followed) or is the team romanticizing? (b) What is the cost of doing Y in this case? (c) What is the cost of skipping Y in this case? If the answer to (a) is unverified, mark as convention; spawn a research task to confirm precedent. If the cost in this case is high (e.g. audit takes 6 weeks, team has 4 weeks), the convention has a real cost that should be visible to decision-matrix."

---

## Method

The framework runs as a 7-step procedure. Each step has a discrete output.

### Step 1, Inventory all assumptions in the framing

Read `intake.problem_refined` and (if available) `frameworks/abstraction-ladder.md::target_rung`. List every claim the framing makes or implies. Aim for 20-50 candidate assumptions. The first pass is exhaustive; pruning happens later.

For each candidate assumption:
- Where it appears (intake / target rung / implied)
- The claim, stated as a complete sentence

Failure mode: producing fewer than 20 candidates. Indicates the agent is filtering as it goes; conventions are getting missed.

### Step 2, Classify each assumption

For each candidate, classify as one of:
- **Physics** — a physical or technical constraint that cannot be changed (gas costs nonzero, blocktime > 0, finite Solidity stack)
- **Logic** — a mathematical or logical constraint (hash collisions are inevitable in finite space, a Merkle proof is O(log n))
- **Regulation** — an external rule that has the force of law or contract (KYC for $10K+ transfers, audit before mainnet)
- **Convention** — a choice that other people made that we inherited; not physically forced

For convention, also note who set the convention (the team / the protocol / the industry / the user) and how recently.

Failure mode: lumping ambiguous assumptions as "depends" or "varies." Force a classification. If genuinely ambiguous, mark as convention because it is the conservative choice (convention-with-test-needed is safer than physics-when-actually-convention).

### Step 3, Name the cost of each convention

For every assumption classified as convention, name:
- **Cost of following** the convention (time, money, optionality, risk)
- **Cost of breaking** the convention (rebuild work, social cost, technical risk)
- **Net** (which is higher; do not commit to action, just measure)

Conventions with cost-of-following ≤ cost-of-breaking are not worth challenging in this run. Mark them as low-leverage. Conventions with cost-of-following > cost-of-breaking are high-leverage and surface to decision-matrix.

Failure mode: stating a cost as "high" or "low" without numbers, named risk, or named alternatives. Force concreteness.

### Step 4, Prune to atomic truths

Apply Operating Principle 2 (exhaustive and minimal):
- Remove paraphrases (claim A and claim A' merge to one).
- Remove implications (if A logically implies B, drop B).
- Keep only the smallest set of claims that downstream frameworks can build on.

Target: 5-15 atomic truths (most problems land here). If the result is 25+ truths, the pruning was insufficient. If the result is 1-2 truths, the inventory was too narrow.

Failure mode: pruning too aggressively. The result is so generic ("things must work, gas must be low") that downstream frameworks cannot use it. Re-inventory.

### Step 5, Rebuild the framing from atoms only

Using only atomic truths (not the original framing's vocabulary), write a new problem statement. The rebuilt framing should:
- Use the verbs and nouns the atoms support
- Not reference any convention by its conventional name (e.g. don't say "wallet" if "wallet" is a convention; say "user signing mechanism")
- Be at the same abstraction level as the target rung
- Be a complete sentence with a verb

Failure mode: the rebuilt framing reads identical to the original. Either the inventory was too narrow (Operating Principle 3) or the conventions in the original were already minimal.

### Step 6, Compare rebuilt vs original on three dimensions

Diff the rebuilt framing against the original on:
- **Problem statement** — what changed? Did the verb change? Did the object change?
- **Candidate solutions** — what new candidates appear that the original made invisible?
- **Constraints** — what constraints went from "given" to "challengeable"?

If 0 of 3 dimensions show change, the rebuild produced no new value and the framework should re-run with a wider inventory.

Failure mode: skipping the comparison. The rebuilt framing sits in the output but downstream frameworks default to the original because the diff was not made explicit.

### Step 7, Write the output and update state.json

Write `$RUN_DIR/frameworks/first-principles.md` per the Output Schema. Write `atomic_truths` (array) and `convention_breaks` (list of high-leverage conventions with cost) to state.json. SendMessage to lead if (a) the rebuilt framing is materially different from the original (signals a re-confirmation may be needed before continuing), (b) any convention was reclassified from physics (signals a regime change).

---

## Probe Patterns

The framework runs analytically. The agent does not ask the user questions during the run. Instead, the agent runs these probes against the framing and prior frameworks.

### Probe Pattern 1, The "what if it were free" probe

> "If [assumption X] cost zero to break, would we still follow it?"

If the answer is no, the assumption is convention with non-trivial cost-of-following.

What good looks like: applies to every assumption, especially infrastructure choices. "If switching from Foundry to Hardhat were free, would we still use Foundry?" If yes, Foundry is genuinely the right tool. If no, Foundry is convention.

Red flags: applying the probe inconsistently. The probe should run on every assumption, not just the ones the agent already suspected were conventions.

Smart-skip: physics assumptions (the probe is incoherent for "if gravity cost zero to break").

### Probe Pattern 2, The "if the user weren't there" probe

> "If we were building this for ourselves with no users, which assumptions disappear?"

This surfaces user-driven conventions (UX patterns, naming, defaults) which are often the highest-cost.

What good looks like: distinguishes physics from user expectation. "If we were building for ourselves, would we still need a wallet flow?" If no, the wallet flow is convention driven by user expectation, not technical necessity.

Red flags: the probe surfaces nothing. Means user expectations are not in the inventory; re-list with user-side conventions.

### Probe Pattern 3, The "5 years ago" probe

> "Was this assumption true 5 years ago? Will it be true 5 years from now?"

Time-bounded assumptions are usually convention. Physics is time-invariant.

What good looks like: surfaces conventions that became dominant recently and will be challenged again. "Was 'use a smart contract for everything' true 5 years ago?" Yes. "Will it be true in 5 years?" Probably not, given account abstraction trends. Mark as convention.

Red flags: classifying recent conventions as physics because they feel established.

### Probe Pattern 4, The "in another industry" probe

> "How does [adjacent industry / domain] solve this same atom-level need? Is their solution available to us?"

Cross-domain comparison surfaces conventions that look universal but are domain-specific.

What good looks like: a Web2 team building Web3 might assume "users authenticate with wallet signatures." Cross-domain probe: how does Web2 solve user identity? Email + password, OAuth, biometrics. Could any of these apply to Web3? Maybe (account abstraction). Mark wallet-signature as convention.

Red flags: the comparison stays within the same domain ("how does another DeFi protocol solve this?"). That tests the convention against itself.

### Probe Pattern 5, The "regulator letter" probe

> "If a regulator sent us a letter asking why we built it this way, would the answer be 'because the law requires it' or 'because that's how it's done'?"

Distinguishes regulation from convention. Most "regulation" claims are conventions about regulation that nobody has actually verified.

What good looks like: "We have KYC because regulators require it." Apply the probe. Read the actual regulation. Often the requirement is "you must reasonably know your customer for transfers above $X for jurisdiction Y." That is a regulation. The convention is the specific implementation (KYC vendor Z, $X = $10K, blocking transfers below threshold).

Red flags: the team cites regulation but cannot name the specific rule, regulator, or jurisdiction. Spawn a research task.

---

## Forcing Exemplars

Every claim in the framework output should pick the forcing version over the softened version.

### Exemplar 1, Listing an assumption

SOFTENED (avoid):
> "The framing seems to assume that users will have wallets, which is a reasonable assumption in this domain."

FORCING (aim for):
> "Assumption: 'Users have a wallet.' Classification: convention (Web3-native default; not physics, not regulation, not logic). Cost of following: 90%+ drop-off rate for non-Web3-native users (per RainbowKit / Privy adoption research, 2024-2025). Cost of breaking: implementing account abstraction or embedded wallets, estimated at 4-6 weeks of frontend + smart-contract work. Net: cost of following is higher, surface to convention_breaks."

### Exemplar 2, Stating an atomic truth

SOFTENED (avoid):
> "Some kind of value transfer mechanism is needed."

FORCING (aim for):
> "Atomic truth: 'A user must be able to authorize a state change on chain.' This truth supports any signing mechanism (EOA, account abstraction, multi-sig, session key) without privileging the wallet convention. Downstream zwicky-box can generate dimensions including 'signer-shape' with values [EOA, AA, multi-sig, session-key, biometric-via-AA]."

### Exemplar 3, Classifying convention vs physics

SOFTENED (avoid):
> "Gas costs are an important consideration."

FORCING (aim for):
> "Atomic truth (physics): 'Operations have nonzero gas cost on the EVM, bounded by block gas limit.' Classification: physics. Block gas limit is 30M on Ethereum mainnet, higher elsewhere; the limit is a protocol parameter, not a constant of nature, but it changes on the order of months and is fixed for the run.

> Assumption (convention, not physics): 'Our operation Y costs N gas.' Classification: convention because N depends on implementation choices. The atomic truth is the upper bound (block limit), not the current implementation cost. Mark as convention; downstream zwicky-box may surface implementations that change N."

### Exemplar 4, Rebuilding the framing

SOFTENED (avoid):
> "Considering the problem from first principles, we want to enable cross-chain value transfer with low friction."

FORCING (aim for):
> "Original framing: 'Should we migrate our LayerZero OFTv1 deployment to OFTv2?'

> Assumption inventory: [LayerZero is the bridge, OFT is the standard, v2 is the next version, migration is the action, our deployment is the unit].

> Atomic truths after pruning: [(a) state changes on chain X must be replicable on chain Y for the system to function as a cross-chain token, (b) replication must be safe under adversarial conditions, (c) replication must complete within UX-acceptable latency].

> Rebuilt framing: 'Decide which mechanism replicates state across chains for our token, evaluating safety, latency, and cost across all available mechanisms (LayerZero v1, LayerZero v2, Wormhole, Axelar, IBC-via-Polymer, native bridges, custom).'

> Diff vs original: rebuilt framing surfaces non-LayerZero options (Wormhole, Axelar, etc.) that the original made invisible. The convention 'LayerZero is the bridge' is high-cost (locks in to one bridge ecosystem) but possibly worth following (LayerZero docs and prior art are deep). Surface to convention_breaks for decision-matrix."

---

## Output Schema

The framework writes to `$RUN_DIR/frameworks/first-principles.md` with this exact structure.

### Section A, Header

```markdown
# First Principles, <SLUG>

**Run:** <session-id>
**Generated:** <ISO timestamp>
**Inputs read:** intake.json, frameworks/abstraction-ladder.md (if present), evidence/define-prior-art.md, evidence/define-failure-modes.md
**Target rung:** <rung statement, copied from abstraction-ladder.md>
```

### Section B, Assumption inventory

```markdown
## Assumption Inventory

| # | Where | Claim | Classification | Subtype |
|---|---|---|---|---|
| 1 | intake | <claim> | <physics/logic/regulation/convention> | <subtype if convention> |
| 2 | abstraction-ladder rung +1 | <claim> | <classification> | <subtype> |
| ... | ... | ... | ... | ... |
```

Subtype for convention is one of: team / protocol / industry / user. Other classifications have no subtype.

Target inventory size: 20-50 candidates before pruning. Final inventory size: 20-50 (pruning happens at the truth list, not here).

### Section C, Convention cost table

```markdown
## Convention Cost Table

| Convention # | Claim | Set by | Cost of following | Cost of breaking | Net | Surface to convention_breaks? |
|---|---|---|---|---|---|---|
| C1 | <claim> | <team/protocol/industry/user> | <specific cost> | <specific cost> | <follow / break / neutral> | <yes/no> |
```

Every cost cell must be specific (time / dollars / risk named). "High" / "low" without specificity is invalid.

### Section D, Atomic truth list

```markdown
## Atomic Truths

After pruning <N> candidate assumptions to remove paraphrases and implications, the irreducible truth set is:

1. **<Truth 1>** — <one-line gloss>; classification: <physics/logic/regulation>
2. **<Truth 2>** — <gloss>; classification: <...>
...
```

Conventions are not in the truth list; they are in the convention table. The truth list contains only physics, logic, and regulation truths.

Target size: 5-15. Outside this range triggers a re-run (too few = inventory too narrow; too many = pruning insufficient).

### Section E, Rebuilt framing

```markdown
## Rebuilt Framing

**Original:** <copied verbatim from intake.problem_refined or target rung>

**Rebuilt:** <new framing using only atomic-truth vocabulary, complete sentence with verb, same abstraction level as target rung>

**Diff:**
| Dimension | Original | Rebuilt | Change? |
|---|---|---|---|
| Problem statement | <...> | <...> | <yes/no> |
| Candidate solutions implied | <...> | <...> | <yes/no> |
| Constraints from given to challengeable | <list> | <list> | <yes/no> |
```

If 0 of 3 dimensions changed, escalate to lead.

### Section F, High-leverage convention breaks

```markdown
## High-Leverage Convention Breaks

These conventions have cost-of-following > cost-of-breaking. Surface to decision-matrix as candidates for explicit evaluation.

1. **<Convention name>** — cost of following: <specific>; cost of breaking: <specific>; alternatives: <list of alternatives the break would unlock>
2. ...
```

If empty, the framework still ran successfully; the conventional path is fine. If 3+ items, the conventional path likely has a better alternative and decision-matrix should evaluate it explicitly.

### Section G, Downstream hooks

```markdown
## Downstream Hooks

- zwicky-box: dimensions are constrained by atomic truths. Specifically, dimensions <X, Y, Z> arise from truths <T1, T2, T3>.
- inversion-define: failure paths must violate at least one atomic truth or one regulation. Failures that "violate" a convention are not failures, they are convention breaks; surface separately.
- decision-matrix: criteria include atomic-truth compliance (always weighted highest) and (if any) high-leverage convention break evaluation.
- iceberg.mental_models: any assumption that contradicted the team's stated belief should surface here as a candidate mental model.
```

### Section H, What This Means For The Decision

```markdown
## What This Means For The Decision

<2 paragraph synthesis: which conventions, if challenged, would change the decision the most; whether the rebuilt framing changes the option set; what downstream phases must do differently because of this output.>
```

### Section I, Completeness Score

```markdown
**Completeness:** <N>/10

**Rubric for this run:**
- Inventory ≥ 20 candidate assumptions: +<N>
- Every assumption classified explicitly: +<N>
- Every convention has named cost: +<N>
- Atomic truth list 5-15 items: +<N>
- Rebuilt framing differs from original on ≥ 1 dimension: +<N>
- Downstream hooks specified: +<N>
```

---

## Decision Hook

This framework's output drives the following downstream frameworks.

### Frameworks that read atomic_truths and convention_breaks

- **zwicky-box** — dimensions of the matrix are constrained by atomic truths. A dimension that violates an atomic truth is invalid (e.g. if the atomic truth is "must support cross-chain replication," a dimension "single-chain only" is invalid). Convention breaks become candidate dimensions.
- **inversion-define** — failure paths are validated against atomic truths. A failure path that requires violating a regulation or physics truth is "real failure"; a failure path that requires violating a convention is a "convention break." First-principles separates these so inversion-define can rank failure paths by severity.
- **decision-matrix** — criteria include atomic-truth compliance (always present, always weighted high). Convention breaks may surface as their own criteria if the cost is high enough.
- **iceberg.mental_models** — any assumption that contradicts the team's stated mental model becomes a candidate mental-model entry.

### Confidence rubric impact

- Atomic truth list size in 5-15 range, +1 to overall confidence rubric.
- ≥ 3 high-leverage convention breaks surfaced, +0 (information, not confidence; the surfacing means the conventional path may be wrong, which lowers confidence in any convention-following recommendation).
- Rebuilt framing differs from original on all 3 dimensions, -1 (signals the original framing was significantly wrong; downstream phases inherit ambiguity that needs more evidence to resolve).
- Convention reclassified from physics, -2 (the team had a wrong mental model of what was forced; high uncertainty until the implications are traced).

### Override conditions

This framework does not override other frameworks. It supplies inputs they consume. The only override-like effect is that any framework using a convention-classified term (e.g. "wallet") must annotate the term as convention, not as a given.

---

## Cross-Framework Triggers

Conditions in the output that fire other frameworks or skill handoffs.

- ≥ 3 high-leverage convention breaks surfaced, mark `state.MULTI_CONVENTION_BREAK = true`. Decision-matrix gives explicit criteria for each.
- An assumption was reclassified from physics to convention, SendMessage to lead: "regime change detected; team's mental model of physical constraints was wrong on <topic>; recommend pausing /solve and confirming with team before continuing."
- Rebuilt framing differs from original on all 3 dimensions (problem, solutions, constraints), SendMessage to lead: "rebuilt framing is materially different from original; recommend confirming with user before /solve continues."
- An assumption claimed as regulation could not be verified, spawn research task `T-research-regulation-<topic>` for the researcher teammate. Block downstream framework progress on this leaf.
- The atomic truth list contains only 1-2 truths after pruning, the inventory was too narrow; restart Step 1 with a wider sweep.

---

## Failure Modes

Five distinct ways this framework misleads.

### Failure Mode 1, Insufficient inventory

Trap: The agent listed 5-10 assumptions and pruned to 3 truths. The framework looks done but most of the framing's conventions never surfaced.

Manifestation in output: assumption inventory has ≤ 10 items. Atomic truth list has 1-3 truths. Rebuilt framing reads identical to original.

Check: count the inventory. If < 20 items, the inventory is incomplete. Force re-run of Step 1 with explicit prompt: "List 20 more candidate assumptions, including obvious ones."

Recovery: re-inventory with the "if X cost zero to break" probe applied to every noun and verb in the framing.

### Failure Mode 2, "Depends" or "varies" classification

Trap: Agent classifies an assumption as "depends on context" or "varies." This is not a classification, it is a refusal to commit.

Manifestation in output: classification cells contain "depends," "varies," "context-dependent," or N/A.

Check: scan the inventory table for invalid classifications. Any cell that is not exactly one of {physics, logic, regulation, convention} is invalid.

Recovery: force a classification. If genuinely ambiguous, classify as convention because it is the conservative choice. Add a note that the classification is provisional pending evidence.

### Failure Mode 3, Convention without cost

Trap: Agent identifies a convention but the cost cells are empty, "high," or "low."

Manifestation in output: convention table has cost cells that are non-numeric and non-specific. Net column is missing or hand-waved.

Check: every cost cell must be specific (time / dollars / risk named) or contain "neutral" / "negligible" with reason.

Recovery: re-fill cost cells with concrete numbers. If the agent cannot estimate, spawn a research task.

### Failure Mode 4, Atomic truth list contains conventions

Trap: Agent let a convention slip into the atomic truth list because it felt obvious.

Manifestation in output: an atomic truth refers to a convention term (e.g. "users have wallets" instead of "users authorize state changes"). The truth list looks specific but is actually convention-laden.

Check: every atomic truth must be classified as physics, logic, or regulation. If the truth uses convention vocabulary, it is misclassified.

Recovery: rewrite the truth using only physics / logic / regulation vocabulary. The convention re-emerges in the convention table.

### Failure Mode 5, Rebuilt framing reads identical to original

Trap: After pruning, the rebuilt framing is the original with synonyms.

Manifestation in output: diff table shows 0 of 3 dimensions changed. Rebuilt framing uses the same nouns, verbs, and constraints as the original.

Check: the 3-dimension diff in Section E. If 0 of 3 changed, the framework provided no new value.

Recovery: re-inventory with cross-domain probe (Probe Pattern 4) and "if user weren't there" probe (Probe Pattern 2). These two probes typically surface conventions the agent missed.

---

## Jargon Glossary

These terms appear in the framework output. First use should include a one-line gloss.

- atomic truth — a claim that cannot be reduced further; classified as physics, logic, or regulation
- assumption — any claim baked into the framing, before classification
- physics — a physical or technical constraint that cannot be changed
- logic — a mathematical or logical constraint
- regulation — an external rule with the force of law or contract
- convention — a choice made by other people that we inherited; not physically forced
- convention break — an explicit choice to challenge a convention because the cost of following exceeds the cost of breaking
- cost of following — the cost the team pays in time, money, optionality, or risk by following a convention
- cost of breaking — the cost the team pays to challenge a convention (rebuild work, social cost, technical risk)
- net cost — the higher of (cost of following) vs (cost of breaking); determines whether the convention is worth challenging
- exhaustive (truth list) — every claim downstream rests on an explicit truth
- minimal (truth list) — no truth is composed of other truths in the list
- rebuilt framing — a new problem statement using only atomic-truth vocabulary
- regime change — a reclassification (e.g. an assumption thought to be physics turns out to be convention) that invalidates prior reasoning
- subtype (convention) — the source of the convention: team / protocol / industry / user

---

## Completeness Scoring

This framework self-rates 0-10. The rubric:

### 10/10, Decisive

- Assumption inventory has 30+ items
- Every assumption classified as exactly one of {physics, logic, regulation, convention}
- Every convention has specific cost cells (numbers or named risks)
- Atomic truth list has 5-15 items
- Rebuilt framing differs from original on all 3 dimensions (problem, solutions, constraints)
- ≥ 1 high-leverage convention break surfaced with named alternatives
- Downstream hooks specified for zwicky-box, inversion-define, decision-matrix, iceberg
- All 5 probe patterns applied

### 7/10, Confident

- Inventory has 20-29 items
- Most assumptions classified, 1-2 are "depends" (auto-corrected to convention)
- Convention costs are mostly specific, 1-2 are "high" / "low"
- Atomic truth list has 5-15 items
- Rebuilt framing differs from original on 1-2 dimensions
- 1 high-leverage convention break surfaced
- Downstream hooks specified for at least 3 of 4 frameworks

### 4/10, Tentative

- Inventory has 10-19 items
- Several assumptions misclassified or unclassified
- Convention costs are vague
- Atomic truth list has 3-4 items or 16-20 items
- Rebuilt framing reads similar to original
- No convention breaks surfaced
- Downstream hooks generic

### 0/10, Insufficient

- Inventory has < 10 items
- Most classifications missing or "depends"
- Convention costs missing
- Atomic truth list has 1-2 items or > 25 items
- Rebuilt framing identical to original
- No probe patterns applied

A completeness ≤ 4 forces a rebuild before downstream Define-phase frameworks run.

---

## Worked Example

Problem: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

This is the canonical example. Intake state and prior framework outputs are the same as cynefin.md and abstraction-ladder.md.

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

### Prior framework outputs

- abstraction-ladder.md: target rung = -1 ("choose the migration archetype"). Strategic why (rung +3) = "default OFT issuer on next 5 v2-only chains."

### Step 1, Inventory all assumptions

The framing assumes (in no particular order):

1. The token is a fungible token.
2. The token uses LayerZero as the bridge.
3. The bridge mechanism is OFT (Omnichain Fungible Token).
4. The token is deployed on exactly the 4 named chains.
5. TVL is currently $12M.
6. LayerZero v2 is "the next version" (single linear progression).
7. v2 is better on gas (the docs say so; we have not measured).
8. v2 is better on security (the docs say so).
9. v2 has a different message-encoding scheme.
10. Migration is the action being considered (vs no-op or sunset).
11. The team has authority to migrate.
12. Users will accept the migration.
13. Liquidity providers will accept the migration.
14. Audits will be available within the time pressure window.
15. The cost of migration is bounded.
16. The reversibility of migration is "costly" (intake-stated).
17. We need OFTv2 to deploy on v2-only chains (per abstraction-ladder rung +1).
18. Multi-chain LP volume is the strategic prize.
19. Competitor protocols (Stargate, Radiant, Ethena) used dual-deploy + drain successfully.
20. The team can run a migration without external help.
21. v2-only chains will have meaningful TVL.
22. v2 is the long-term LayerZero direction (vs a parallel experiment).
23. We will continue to be a stablecoin protocol through 2027 (per rung +2).
24. The current OFTv1 deployment is functioning correctly (no critical bugs blocking).
25. Gas costs on v2 are predictable.
26. Cross-chain settlement latency on v2 matches v1 within UX-acceptable range.
27. The encoding scheme change does not break composability with downstream contracts.
28. Wallets correctly handle v2 messages (most do; we have not verified).
29. Users can identify v2 vs v1 in their wallets.
30. The migration timing is independent of macro market conditions.
31. The team has Solidity expertise sufficient for the migration.
32. LayerZero will continue to support v1 during the migration period.
33. The audit firm we use audits OFTv2 patterns specifically.
34. Bridge volume is a leading indicator of LP fees (per connection-circles upcoming output).
35. Gas cost spikes during the migration window are tolerable.

### Step 2, Classify each assumption

| # | Claim | Classification | Subtype |
|---|---|---|---|
| 1 | Token is fungible | Convention | protocol |
| 2 | Uses LayerZero as bridge | Convention | team |
| 3 | Bridge is OFT | Convention | protocol |
| 4 | Deployed on 4 named chains | Convention | team (point-in-time) |
| 5 | TVL $12M | Physics (current state) | n/a |
| 6 | v2 is the next version | Convention | protocol (LayerZero's roadmap) |
| 7 | v2 better on gas | Convention | protocol (claim, not measured) |
| 8 | v2 better on security | Convention | protocol (claim, not measured) |
| 9 | v2 has different encoding | Logic (verifiable from spec) | n/a |
| 10 | Migration is the action | Convention | team |
| 11 | Team has authority | Convention | team |
| 12 | Users accept migration | Convention | user |
| 13 | LPs accept migration | Convention | user |
| 14 | Audits available in window | Convention | industry |
| 15 | Migration cost bounded | Convention | team (claim) |
| 16 | Reversibility costly | Logic (intake-stated, derived) | n/a |
| 17 | Need OFTv2 for v2-only chains | Logic (only v2 OFTs deploy on v2-only chains; verifiable) | n/a |
| 18 | Multi-chain LP volume is the prize | Convention | team |
| 19 | Competitor protocols used drain | Logic (verifiable from on-chain history) | n/a |
| 20 | Team can migrate without help | Convention | team |
| 21 | v2-only chains have meaningful TVL | Convention | industry (forecast) |
| 22 | v2 is long-term direction | Convention | protocol |
| 23 | We are stablecoin protocol through 2027 | Convention | team |
| 24 | OFTv1 functioning correctly | Convention | team (claim) |
| 25 | Gas on v2 predictable | Convention | protocol (claim) |
| 26 | Settlement latency matches v1 | Convention | protocol (claim) |
| 27 | Encoding does not break composability | Convention | protocol |
| 28 | Wallets handle v2 | Convention | user (most do) |
| 29 | Users distinguish v2 vs v1 | Convention | user |
| 30 | Migration timing independent of macro | Convention | team |
| 31 | Team has Solidity expertise | Convention | team |
| 32 | LZ supports v1 during migration | Convention | protocol |
| 33 | Auditor audits OFTv2 patterns | Convention | industry |
| 34 | Bridge volume leads LP fees | Convention | protocol (model) |
| 35 | Gas spikes tolerable | Convention | team |

Out of 35: physics 1, logic 4, regulation 0, convention 30.

### Step 3, Name the cost of each convention

For brevity, name costs for the top 8 highest-leverage conventions:

| # | Convention | Cost of following | Cost of breaking | Net | Surface? |
|---|---|---|---|---|---|
| 2 | Use LayerZero as bridge | Lock-in to LZ ecosystem; cost = future bridge optionality (~ $200K-$1M opportunity cost over 2 years if a competitor bridge becomes dominant) | Switch to Wormhole/Axelar/IBC; cost = 8-16 weeks rebuild + audit | Follow (break-cost too high for marginal benefit) | No |
| 7 | v2 better on gas | If false, migration ROI is lower than expected; cost = ~ 30% of expected ROI ($X) | Measure on testnet before committing; cost = 2 days | Break (cost of measurement is trivial) | Yes |
| 12 | Users accept migration | If false, churn during migration; cost = ~ 5-15% TVL churn ($600K-$1.8M) | Survey users / phase migration with opt-in; cost = 1 week + UX work | Break (high downside if false) | Yes |
| 13 | LPs accept migration | If false, LP withdrawal during migration; cost = ~ 10-30% LP churn | Coordinate with top 5 LPs in advance; cost = 1 week of comms | Break (high downside, low coordination cost) | Yes |
| 14 | Audits available in window | If false, deployment delay; cost = miss v2-only chain entry window (~ $3M-$8M opportunity cost per quarter delayed) | Pre-book audit slot; cost = financial commitment ($50K-$150K nonrefundable) | Break (the financial commitment is small vs delay cost) | Yes |
| 21 | v2-only chains have meaningful TVL | If false, the strategic why (rung +3) collapses; cost = 100% of expected migration upside | Validate with 1-2 partner protocols' deployment plans; cost = 1 week of conversations | Break (this is the rung +3 anchor; if false, do not migrate) | Yes |
| 24 | OFTv1 functioning correctly | If false, migration is hiding a bug; cost = bug surfaces in v2 with worse blast radius | Run a forensics pass on OFTv1 incidents (3 incidents per iceberg.events); cost = 2-3 days | Break (cheap and high-information) | Yes |
| 33 | Auditor audits OFTv2 patterns | If false, audit findings are surface-level; cost = security risk in production | Confirm auditor's OFTv2 experience before booking; cost = 1 hour | Break (trivially cheap) | Yes |

### Step 4, Prune to atomic truths

Remove physics+logic claims that are paraphrases or implications:

- Atom A: "State changes on chain X must be replicable on chain Y for cross-chain token semantics to hold." (subsumes claims 9, 17, 19)
- Atom B: "Replication must be safe under adversarial conditions (no double-spend, no fund-loss)." (subsumes claims 8, 16, 19)
- Atom C: "Replication must complete within UX-acceptable latency (current OFT v1 latency = 60-180s by chain)." (subsumes claim 26)
- Atom D: "Operations on chain have nonzero gas cost bounded by block gas limit." (physics; subsumes claims 7, 25, 35)
- Atom E: "Audits are available subject to scheduling, capacity, and auditor experience." (regulation-adjacent / industry; subsumes claims 14, 33)
- Atom F: "TVL at decision time is $12M (point-in-time, will change)." (physics, current state)
- Atom G: "Reversibility of any deployed bridge upgrade is costly (multi-week rollback effort)." (logic, intake-derived)

Atomic truth list: A, B, C, D, E, F, G (7 truths). In the 5-15 target range.

### Step 5, Rebuild the framing from atoms

Original: "Should we migrate our LayerZero OFTv1 deployment to OFTv2?"

Rebuilt: "Decide which mechanism replicates state across the 4 currently-deployed chains and the 5 expected v2-only chains for our token, with the constraint that replication is safe (Atom B), latency-bounded (Atom C), gas-bounded (Atom D), and reversibility-costly (Atom G); evaluate available mechanisms (LayerZero v1, LayerZero v2, alternative bridges) on cost-of-deployment, cost-of-audit (Atom E), and convention-following risks."

### Step 6, Compare rebuilt vs original

| Dimension | Original | Rebuilt | Change? |
|---|---|---|---|
| Problem statement | yes/no migration | which mechanism (no a-priori migration assumption) | Yes |
| Candidate solutions | OFTv1 vs OFTv2 | OFTv1, OFTv2, alternative bridges | Yes |
| Constraints | implied | explicit (Atoms A-G) | Yes |

Three of three dimensions changed. The framework produced new value. Specifically, the rebuilt framing surfaces alternative-bridge candidates (Wormhole, Axelar, IBC) that the original made invisible. However, per Convention 2's net cost analysis, the alternative-bridge path is high cost-of-breaking and not worth challenging in this run.

### Step 7, Write the output

```markdown
# First Principles, should-we-migrate-to-oftv2

**Run:** 13450-1777851341
**Generated:** 2026-05-03T17:35:00Z
**Inputs read:** intake.json, frameworks/abstraction-ladder.md, evidence/define-prior-art.md, evidence/define-failure-modes.md
**Target rung:** Choose the migration archetype (big-bang, dual-deploy+drain, wrapped legacy, separate token).

[Section B: Assumption Inventory — 35 items as listed above]

[Section C: Convention Cost Table — top 8 as above]

## Atomic Truths

After pruning 35 candidate assumptions to remove paraphrases and implications, the irreducible truth set is:

1. **Atom A** — State changes on chain X must be replicable on chain Y for cross-chain token semantics to hold; classification: logic.
2. **Atom B** — Replication must be safe under adversarial conditions; classification: logic.
3. **Atom C** — Replication must complete within UX-acceptable latency (60-180s baseline); classification: physics (network-bounded).
4. **Atom D** — Operations on chain have nonzero gas cost bounded by block gas limit; classification: physics.
5. **Atom E** — Audits are subject to scheduling, capacity, and auditor experience; classification: industry-regulation.
6. **Atom F** — TVL at decision time is $12M (point-in-time, may change); classification: physics (current state).
7. **Atom G** — Reversibility of any deployed bridge upgrade is costly; classification: logic (intake-derived).

## Rebuilt Framing

**Original:** Should we migrate our LayerZero OFTv1 deployment to OFTv2?

**Rebuilt:** Decide which mechanism replicates state across the 4 currently-deployed chains and the 5 expected v2-only chains for our token, with constraints: replication is safe (Atom B), latency-bounded (Atom C), gas-bounded (Atom D), reversibility-costly (Atom G). Evaluate available mechanisms (LayerZero v1, LayerZero v2, alternative bridges) on cost-of-deployment, cost-of-audit (Atom E), and convention-following risks.

**Diff:**
| Dimension | Original | Rebuilt | Change? |
|---|---|---|---|
| Problem statement | Yes/no migration | Which mechanism | Yes |
| Candidate solutions | OFTv1 vs OFTv2 | + alternative bridges | Yes |
| Constraints | Implied | Explicit Atoms A-G | Yes |

## High-Leverage Convention Breaks

These conventions have cost-of-following > cost-of-breaking. Surface to decision-matrix as candidates for explicit evaluation.

1. **v2 better on gas (#7)** — cost of following: ~30% of expected ROI if claim is false; cost of breaking: 2 days of testnet measurement. Alternative: measure before committing.

2. **Users accept migration (#12)** — cost of following: 5-15% TVL churn if false; cost of breaking: 1 week of UX + survey work. Alternative: opt-in phased migration with pre-announcement.

3. **LPs accept migration (#13)** — cost of following: 10-30% LP churn if false; cost of breaking: 1 week of LP coordination. Alternative: pre-coordinate with top 5 LPs.

4. **Audits available in window (#14)** — cost of following: $3M-$8M opportunity cost per delay quarter; cost of breaking: $50K-$150K audit booking commitment. Alternative: pre-book audit slot now.

5. **v2-only chains have meaningful TVL (#21)** — cost of following: 100% of expected upside if false (this is the rung +3 anchor); cost of breaking: 1 week of partner conversations. Alternative: validate with Hyperliquid + Sei + Mantle teams before committing.

6. **OFTv1 functioning correctly (#24)** — cost of following: bugs migrate forward with worse blast radius; cost of breaking: 2-3 days of forensics on the 3 historical incidents. Alternative: forensics pass before committing archetype.

7. **Auditor audits OFTv2 patterns (#33)** — cost of following: surface-level audit; cost of breaking: 1 hour conversation. Alternative: confirm auditor's OFTv2 experience before booking.

## Downstream Hooks

- zwicky-box: dimensions are constrained by Atoms A-G. Specifically, "cutover-shape" (Atom B forces no-double-spend), "audit-scope" (Atom E forces audit availability check), "reversibility-window" (Atom G forces designed rollback path).
- inversion-define: failure paths must violate one or more atoms. "Migration locks user funds" violates Atom B; "migration delivers gas costs above v1" violates Atom D; "migration cannot be reversed in N days" violates Atom G.
- decision-matrix: criteria include atomic-truth compliance (always weighted highest) plus the 7 high-leverage convention breaks as explicit criteria. Each convention break adds a "validate before commit" task.
- iceberg.mental_models: assumptions #6 (v2 is "next version"), #7 (v2 better on gas, unmeasured), #18 (multi-chain LP volume is the prize), #22 (v2 is long-term direction) are candidate mental models the team holds without explicit verification.

## What This Means For The Decision

The conventional path (migrate to OFTv2 because LayerZero says so and competitors did) is the right path, but only if 7 specific conventions hold. Surface them now or pay the cost later. The cheapest insurance is to validate (a) v2 gas claims on testnet, (b) audit availability, and (c) v2-only chain TVL forecasts before committing the archetype. Each validation costs days; the cost of skipping each is in the millions.

The rebuilt framing names alternative-bridge candidates (Wormhole, Axelar) that the original made invisible. The framework recommends NOT pursuing them in this run because the cost of breaking the LayerZero convention is high (Convention #2). But naming them keeps the option visible if the LayerZero v2 path encounters a deal-breaker mid-migration.

Downstream phases must operate on Atoms A-G as the constraint set, not on the original framing's implicit constraints. zwicky-box generates archetypes that respect these atoms. decision-matrix evaluates archetypes plus 7 convention-validation tasks.

## Completeness: 9/10

**Rubric:**
- Inventory has 35 items (target 20+): +2
- Every assumption classified: +2
- Every convention has specific cost cells: +2
- Atomic truth list has 7 items (target 5-15): +1
- Rebuilt framing differs on all 3 dimensions: +1
- 7 high-leverage convention breaks surfaced: +1
- Downstream hooks specified for 4 frameworks: +1
- 1 deferred check (no probe pattern formally applied to assumption 6 about LZ roadmap; could re-run with cross-domain probe): -1
```

This output then feeds:
- zwicky-box, which uses Atoms A-G to constrain the matrix dimensions and the convention breaks as candidate axes
- inversion-define, which uses atoms to validate failure paths
- decision-matrix, which inherits criteria including the 7 convention validations as pre-decision tasks
- iceberg.mental_models, which gets candidate mental models to verify

### What the next framework (zwicky-box) inherits

zwicky-box receives:
- Atoms A-G as constraints on every dimension
- Convention breaks #7, #12, #13, #14, #21, #24, #33 as candidate dimensions to test
- The rebuilt framing as the framing zwicky-box operates on (target rung -1)

zwicky-box then constructs the matrix using cutover-shape, liquidity-handling, naming, audit-scope, and audit-experience-validation as dimensions.

---

## What This Means For The Decision

This framework is the assumption auditor for /solve. Conventional paths inherit assumptions from years of accumulated industry choice; first-principles makes those assumptions visible and assigns cost to each one. When a convention is cheap to follow and expensive to break, the convention is fine. When it is the reverse, the convention is the source of high-leverage decisions everyone else missed.

The cost of skipping this framework: every downstream framework operates on the user's framing, including its hidden conventions, and the recommendation looks like every other team in the industry. The benefit of doing it right: the recommendation distinguishes the conventions worth following from the conventions worth challenging, and downstream frameworks evaluate the latter explicitly. This is the difference between confident-and-wrong (because everyone else is doing it this way) and confident-and-right (because we tested the conventions and they held, or we found the ones that didn't).
