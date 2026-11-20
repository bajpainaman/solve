---
name: maintain
description: SDLC stage 9. After a feature ships, checks real signals against intent.md's success criteria, runs EGM's drift report against the ADRs, writes docs/sdlc/<slug>/lessons.md, and turns any follow-up or incident into a new intent so the loop starts again. Use when the user runs /sdlc:maintain, reports an incident or regression to feed back into the SDLC, or asks to check docs against code across features.
argument-hint: "<slug> | <incident description> | drift"
---

# Stage 9 — Maintain

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/egm.md` and `${CLAUDE_PLUGIN_ROOT}/references/ponytail.md`. Its `drift` mode uses `${CLAUDE_PLUGIN_ROOT}/references/fv-toolkit.md` when the repo holds formal models.

Maintain closes the loop. Whatever goes wrong after release becomes a new intent and starts again at stage 1.

Input: `$ARGUMENTS`

## For a shipped feature

1. **Read the success criteria** in `intent.md`.

2. **Check the signals read-only.** Use the observability, error-tracking, analytics or CI tools in the session, such as MCP servers or CLIs. Compare each signal with the criterion it measures. If no tool can reach a signal, ask the user for the number and don't guess.

3. **Write `docs/sdlc/<slug>/lessons.md`** from the template.

4. **Turn the lessons into changes:**
   - Check the whole feature against the repeated-mistake rule in `stage-rules.md`.
   - When pr-review found a policy gap, propose an edit to the policy's skill or to `REVIEW.md`, and the policy owner signs it off.
   - When the repo has an agent eval suite, propose this feature's task as a new eval case.
   - Any follow-up work becomes a new feature. Run `sdlc:intent` for it, and record `from: <slug>` in its `sdlc.yaml`.

5. **Gate.** Get approval and commit `lessons.md` and `sdlc.yaml`. The feature is closed.

## For drift across features

When the input is `drift`, run these checks:

1. **Records against code.** Run `egm-drift-report` on `docs/sdlc/` to compare every ADR with the current code. Then let the user decide, divergence by divergence, whether the code or the record is wrong. A wrong record gets a superseding ADR through a new intent. Wrong code gets a new intent.
2. **Models against code.** When the repo holds a formal model with a sync record, invoke `fv-toolkit:fv-maintain`, as `fv-toolkit.md` describes. It says whether each model still describes the code, and whether a failure is drift in the model or a bug in the code. A bug gets a new intent.
3. **Over-engineering across features.** Run `ponytail:ponytail-audit` on the repo. It ranks what to delete or simplify across the whole tree, which catches complexity that built up feature by feature. Drop any cut that an ADR records as deliberate. The user picks the cuts worth making, and each one becomes a new intent, or one intent that groups them.

## For an incident or regression

1. **Diagnose read-only.** Read logs, metrics and recent deploys, but don't change code or infrastructure.
2. **Write a new intent** with `sdlc:intent`, using the diagnosis as the Problem. Link the incident and, if known, the feature whose ADR covers the broken behavior.
3. **Let the on-call engineer or service owner decide** whether to fix it now, schedule it or dismiss it. When it's fixed and the repo has an eval suite, the fix's test also becomes an eval case.

## Template

```markdown
# <Feature title> — lessons

## Outcome vs success criteria
| Criterion | Target | Observed | Met |
|---|---|---|---|

## What went wrong
- <stage> — <what happened>

## Changes proposed
- [ ] Check: <lint rule, test or hook>
- [ ] CLAUDE.md: <line>
- [ ] REVIEW.md or skill <name>: <edit>
- [ ] Eval: <case>

## Follow-ups
- <new intent slug>
```
