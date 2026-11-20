---
name: intent
description: SDLC stage 1. Runs EGM's brainstorm with the originator, then distills its concepts brief into docs/sdlc/<slug>/intent.md. Also adopts or reviews an intent someone else wrote. Use when the user runs /sdlc:intent or the sdlc skill routes a new idea here.
argument-hint: "<slug or idea> [--adopt <path|url>] [--review]"
---

# Stage 1 — Intent

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/egm.md`.

The intent records what the originator wants and why, and never how. It replaces backlog entries, user stories and refinement meetings. Anyone can be the originator.

Input: `$ARGUMENTS`

## Author mode

1. **Set up the feature.** Create the feature branch and `sdlc.yaml`, and record the owner and approver for this stage. When the user names a ticket, record it as `ticket:`.

2. **Brainstorm.** Run `egm-brainstorm` with the originator's description. It asks clarifying questions, sends seven Goldfish reviewers to stress-test the idea, and writes `docs/sdlc/<slug>/egm/concepts_brief.md`. For a small, well-understood change, the approver may skip the swarm. In that case, interview the originator yourself until you can fill the template without guessing.

3. **Distill `intent.md`** from the brief, using the template below. Keep it in the originator's words. Implementation ideas from the brief stay in the brief, because the RFC stage reads it.

4. **Gate.** Show `intent.md` next to the brief. The originator corrects it, and the approver approves it. Commit `intent.md`, the `egm/` folder and `sdlc.yaml` together.

## Adopt and review modes

Follow `stage-rules.md`. The Goldfish review is `egm-review-loop` with the Heilmeier standard, using the inputs in `egm.md`.

## Template

```markdown
# <Feature title>

## Problem
<Who has the problem, what happens today, and what it costs.>

## Proposed outcome
<What is true once this ships, from the user's point of view.>

## Success criteria
- <A measurable signal, such as "export of 10k rows finishes in under 30 s">

## Affected users and systems
- <user group or system>

## Constraints
- <deadline, policy or must-not-change>

## Out of scope
- <thing we will not do>

## Open questions
- <question> — owner: <name>
```
