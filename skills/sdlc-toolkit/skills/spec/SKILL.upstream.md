---
name: spec
description: SDLC stage 2. Turns an approved intent into testable requirements and acceptance criteria at docs/sdlc/<slug>/spec.md, applying the session's policy skills, then runs an EGM Goldfish review. Also adopts or reviews a spec someone else wrote. Use when the user runs /sdlc:spec or the sdlc skill routes here.
argument-hint: "<slug> [--adopt <path|url>] [--review]"
---

# Stage 2 — Spec

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/egm.md`.

The spec says *what* the system must do, in testable terms. The RFC decides *how*. Claude writes the spec, and the product owner reviews it but doesn't write it. Policies apply while Claude writes the spec, so nobody finds them later in review.

Feature: `$ARGUMENTS`

## Author mode

1. **Read `intent.md` and `egm/concepts_brief.md`.** Stop if the intent isn't approved.

2. **Load the policies.** Check which skills in this session encode security, compliance, brand, UX or API policy, and apply each relevant one. List their names under Policies applied.

3. **Read the code the change touches,** so the requirements name real systems and real limits.

4. **Write `docs/sdlc/<slug>/spec.md`** from the template. Every requirement must be testable. Answer the intent's open questions where the code or a policy settles them, and keep the rest open.

5. **Route the concerns.** List each risk or policy concern with the person who owns that policy. Resolve every concern with its owner before approval, and record the outcome.

6. **Set the risk level.** A change is high-risk when it touches auth, money, PII, data migrations or a public API. A high-risk spec needs the tech lead as an approver, and it never skips the RFC. A spec also keeps the RFC when a requirement says never, always, at most once or exactly once about ordering, retries, permissions or a rule table, because the RFC stage checks that claim against the design.

7. **Gate.** The Goldfish review is `egm-review-loop` with the feature-spec standard, using the inputs in `egm.md`. Commit `spec.md`, its report and `sdlc.yaml` together.

## Adopt and review modes

Follow `stage-rules.md`, using the same Goldfish review.

## Template

```markdown
# <Feature title> — spec

Risk: low | high
Policies applied: <skill names>

## Summary
<Two or three sentences on what the system will do.>

## Requirements
- **R1** <The system does X when Y.>

## Non-functional requirements
- <performance, security, availability, accessibility, with numbers>

## Acceptance criteria
| Id | Criterion | Covers |
|---|---|---|
| AC1 | <observable behavior> | R1 |

## Risks and policy concerns
| Concern | Policy owner | Resolution |
|---|---|---|

## Open questions
- <question> — owner: <name>
```
