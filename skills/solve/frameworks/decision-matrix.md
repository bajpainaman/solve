# decision-matrix

Use only after `bin/gates inspect --gate decision-matrix` returns `trigger_value: true`.

## Entry Predicate

Two or more feasible options can be compared on explicit decision criteria.

The authoritative text and fact key `comparable_options` live in [the gate catalog](../gates/catalog.json).
Unknown or unsupported applicability is BLOCKED. N/A requires the exact trigger,
a false evaluation, its explanation, and hashed evidence. Tier never changes this rule.

## Method

1. Derive criteria from success conditions and binding constraints.
2. Disqualify infeasible options before scoring; cite scores and weights.
3. Calculate totals and sensitivity; expose ties instead of inventing precision.
4. Write only findings that affect a named claim. Request missing evidence instead of filling space.
5. Record expected and observed results with source receipts, then submit the gate record.

## Output Schema

Write `$RUN_DIR/frameworks/decision-matrix.md` with the question, findings, evidence,
uncertainty, and **What This Means For The Decision**. Record a FIRED receipt through
`bin/gates record`: artifact hash, affected claim IDs, input digest, and checks.
The artifact alone cannot establish completion. A failed check is still FIRED.

## Decision Hook

Update affected claims or applicability facts when the evidence changes. This invalidates
stale receipts and may activate another method. Do not award confidence points or
require another framework merely because its name appears in an old worked example.

## Depth on demand

Only when a named question remains unresolved, read the relevant section of
[the deep reference](../references/deep/decision-matrix.md). Its examples and historical
orchestration rules are not current facts or runtime instructions. Do not load the
whole reference by default. Independent refutation and consumer verification remain required.
