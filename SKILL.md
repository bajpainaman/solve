---
name: solve
description: Strategic decisions with adaptive analysis and evidence-bound verification. Classify the request first. For a decision, identify critical claims, evaluate written gate triggers, use only applicable methods, run a fresh independent refuter, and verify the actual report through a fresh consumer reviewer. Quick, Standard, and Deep control budgets and evidence depth, never framework counts. Gate states are exactly FIRED, N/A, or BLOCKED. Produce a recommendation with checkable evidence and explicit uncertainty under .context/solve/.
---

# Solve

Help the user choose a path whose conditions and evidence they can inspect. The
user makes the decision. Completing analysis is not evidence that a claim is true.

## Scope first

Classify as decision, knowledge, bug, or idea. Answer knowledge requests directly.
Route a reproducible bug to an available investigate skill and an unvalidated
product idea to office-hours when appropriate. Do not start a decision workflow
for either. Honor a supplied brief by reading its contents.

For strategic decisions, read [runtime](references/runtime.md) and
[roles](references/roles.md). Read [confidence](references/confidence.md) before
summarizing certainty. Do not load the framework library.

## Non-negotiable contract

- Each gate has exactly one legal state: **FIRED**, **N/A**, or **BLOCKED**.
- FIRED names a hashed artifact and actual checks with expected and observed
  results. A check that disproves a claim is FIRED, with a failed outcome.
- N/A quotes the gate's exact written trigger and cites evidence that it is false.
  Unknown applicability is BLOCKED. Budget pressure never justifies N/A.
- BLOCKED names the obstruction and what is now unverified. Missing, malformed,
  or stale receipts are BLOCKED to the ledger's consumer.
- Evidence, independent refutation, and consumer verification are required in
  every decision run, including Quick. Neither roleplay nor a framework replaces them.
- Only `bin/gates finalize` establishes verified completion. File existence,
  an agent's completion message, or `state.phase=complete` is insufficient.
- Use fresh subagents for refutation and consumer review. This skill authorizes
  these bounded delegations. Explicitly set `fork_turns="none"`. No inherited
  conversation, reused builder, or shared reviewer identity.
- Never manufacture sources, observations, trigger facts, reviewer identities,
  test results, benchmark measurements, or the user's preferences.

## 1. Establish the run

Resolve SOLVE_ROOT from the installed skill path, then honor launcher preseeds:
SOLVE_PRESEED_TIER, SOLVE_PRESEED_TIME, SOLVE_PRESEED_SPEND (legacy TOKENS means
external research spend). Default to Standard. Tiers set time, spend, and evidence
depth. They never select a fixed number of methods.

Preserve the original request verbatim in a temporary brief. Initialize with:

```bash
"$SOLVE_ROOT/bin/gates" init --run-dir "$RUN_DIR" --request "$BRIEF" \
  --builder-id "$BUILDER_ID" --tier "$TIER" --slug "$SLUG"
```

Keep user-provided constraints and success criteria in intake.json. Do not put
builder reasoning in either intake.json or request.md. Ask only about missing
information that can change the decision or a necessary check.

Preserve existing runs. Resume verified 2.0 receipts after freshness checks.
Older runs remain unverified references; archive or choose a new directory before
starting the new contract. Never create migration receipts for work not checked.

## 2. Build claims and evaluate applicability

Write claims.json with the assertions on which the recommendation depends:
statement, fact/forecast/preference, critical Boolean, and a declared consumer
surface plus expected observation. Mark forecasts with assumptions and followup.
Do not omit a claim just because it is difficult to verify.

Read the cheap catalog with `bin/gates catalog`. For each trigger, record the
observed applicability fact, its explanation, and hashed source in facts.json.
Assess applicability in the scope of this decision. Do not infer absence from
silence, hide uncertainty, or ask the user 25 ritual questions.

Inspect each gate before work:

```bash
"$SOLVE_ROOT/bin/gates" inspect --run-dir "$RUN_DIR" --gate "$GATE"
```

Persist N/A for supported false triggers. Persist BLOCKED for unknown triggers,
with the deciding information missing. For true framework triggers, load only
the indicated compact method card. Open a specific deep-reference section only
when the card leaves a named question unanswered. Do not load all methods, fan
out 25 roles, or run frameworks to fill a quota.

## 3. Check the deciding claims

Use current primary evidence when facts can change. Research only named gaps.
A bounded researcher may own a source lane; give it no unrelated analysis. Keep
observations under evidence/. Optional Parallel.ai calls must respect spend caps.

Each applied method writes a short findings artifact and a gate receipt. Evidence
checks cover every critical claim. They name the actual surface, expected result,
observed result, Boolean outcome, and hashed observations. File creation is not a
consumer check when the claim concerns an API, page, application, or reader.

Record through `bin/gates record --run-dir "$RUN_DIR" --file "$RECEIPT"`.
Use the input digest obtained before the check. Changed inputs require another
check, not merely relabeling an old receipt with a new digest.

At each boundary, use budget-track and progress. At 80%, finish current necessary
checks and start no optional work or new paid research. At 100%, stop workers,
call `bin/gates halt` with the exhausted resource, render an unverified draft,
and provide resume instructions. Preserve completed checks.

## 4. Independently refute

Record nonempty recommendation and next_action strings in state through state-rw
before revealing claims. This snapshot is what the refuter will try to disprove.

Use the exact protocol in references/roles.md. The refuter first sees only the
original request and user constraints and finds its own evidence. It commits a
blind framing and list of material claims before `bin/gates reveal` exposes
claim statements, the recommendation and next action, and gate declarations.

The refuter checks both truth and coverage: which omitted assertion could change
the choice, conditions, or next action? It can challenge an unjustified N/A.
It does not receive builder rationale, framework outputs, confidence, or hat votes.

Revise refuted claims or the recommendation. Preserve failed receipts in history.
A changed recommendation, next action, or claim set requires a new refuter, starting blind.

Six Hats is optional when its own trigger fires. Any requested hats use fresh
original inputs and scoped perspectives. Their votes add no confidence and never
satisfy the independent-refutation gate.

## 5. Render, then verify through the consumer

Keep the reviewed recommendation and next action in state. Summarize
checked claims and uncertainty; do not compute confidence from votes or default
likelihood ratios.

Render with bin/render-report. This produces a draft and a render receipt. Spawn
a second fresh reviewer and prepare it with the exact delivered report path.
The consumer reads that report, checks claim coverage, follows evidence, and
exercises the declared acceptance surfaces. It must explicitly name missing
material claims or unsupported recommendations, even if every declared claim passed.

Record the consumer gate with the prepared report hash. Do not rewrite the report
after review. If anything changes, render again and obtain a fresh consumer review.

## 6. Finish

Run `bin/gates validate`, then `bin/gates finalize`. Return the report path,
recommendation, checked claims, unresolved uncertainty, and next action.
A failed or incomplete check prevents verified completion. A draft may still be
useful, but label it unverified and name the obstruction.

Use the host's messaging and wait tools; do not poll agents in shell loops.
Verify artifacts directly. Keep prose short, distinguish observations from
forecasts, and preserve dissent. No fabricated certainty, filler, or framework quotas.
