# inversion-define

Use only after `bin/gates inspect --gate inversion-define` returns `trigger_value: true`.

## Entry Predicate

A credible failure path has not been examined and could disqualify an option.

The authoritative text and fact key `failure_paths_unexamined` live in [the gate catalog](../gates/catalog.json).
Unknown or unsupported applicability is BLOCKED. N/A requires the exact trigger,
a false evaluation, its explanation, and hashed evidence. Tier never changes this rule.

## Method

1. Identify concrete ways the proposed choice could fail.
2. Name the conditions and observable signal for each deciding failure.
3. Turn supported failures into explicit constraints or disqualifiers.
4. Write only findings that affect a named claim. Request missing evidence instead of filling space.
5. Record expected and observed results with source receipts, then submit the gate record.

## Output Schema

Write `$RUN_DIR/frameworks/inversion-define.md` with the question, findings, evidence,
uncertainty, and **What This Means For The Decision**. Record a FIRED receipt through
`bin/gates record`: artifact hash, affected claim IDs, input digest, and checks.
The artifact alone cannot establish completion. A failed check is still FIRED.

## Decision Hook

Update affected claims or applicability facts when the evidence changes. This invalidates
stale receipts and may activate another method. Do not award confidence points or
require another framework merely because its name appears in an old worked example.

## Depth on demand

Only when a named question remains unresolved, read the relevant section of
[the deep reference](../references/deep/inversion-define.md). Its examples and historical
orchestration rules are not current facts or runtime instructions. Do not load the
whole reference by default. Independent refutation and consumer verification remain required.
