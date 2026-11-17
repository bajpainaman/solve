# impact-effort

Use only after `bin/gates inspect --gate impact-effort` returns `trigger_value: true`.

## Entry Predicate

Material differences in expected impact and effort could change option priority.

The authoritative text and fact key `effort_tradeoff` live in [the gate catalog](../gates/catalog.json).
Unknown or unsupported applicability is BLOCKED. N/A requires the exact trigger,
a false evaluation, its explanation, and hashed evidence. Tier never changes this rule.

## Method

1. Estimate impact and effort in explicit units or bounded ranges.
2. Cite assumptions and account for dependencies and uncertainty.
3. Test whether the priority survives plausible changes in the estimates.
4. Write only findings that affect a named claim. Request missing evidence instead of filling space.
5. Record expected and observed results with source receipts, then submit the gate record.

## Output Schema

Write `$RUN_DIR/frameworks/impact-effort.md` with the question, findings, evidence,
uncertainty, and **What This Means For The Decision**. Record a FIRED receipt through
`bin/gates record`: artifact hash, affected claim IDs, input digest, and checks.
The artifact alone cannot establish completion. A failed check is still FIRED.

## Decision Hook

Update affected claims or applicability facts when the evidence changes. This invalidates
stale receipts and may activate another method. Do not award confidence points or
require another framework merely because its name appears in an old worked example.

## Depth on demand

Only when a named question remains unresolved, read the relevant section of
[the deep reference](../references/deep/impact-effort.md). Its examples and historical
orchestration rules are not current facts or runtime instructions. Do not load the
whole reference by default. Independent refutation and consumer verification remain required.
