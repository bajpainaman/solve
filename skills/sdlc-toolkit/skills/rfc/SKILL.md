---
name: rfc
description: SDLC stage 3. Writes the design RFC for an approved spec with the rfc skill, or with EGM's draft when the rfc skill isn't installed, then runs EGM's Goldfish design review and resolve. Also adopts or reviews an RFC someone else wrote. Use when the user runs /sdlc:rfc or the sdlc skill routes here.
argument-hint: "<slug> [--adopt <path|url>] [--review]"
---

# Stage 3 — RFC

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/egm.md`, `${CLAUDE_PLUGIN_ROOT}/references/rfc-skill.md` and `${CLAUDE_PLUGIN_ROOT}/references/fv-toolkit.md`.

The RFC decides how the system will meet the spec. It covers the options, the chosen design and its trade-offs, the fallback, the phases and PRs, the proposed tickets and the blast radius. The Plan stage turns its phases into work items, and after Ship the ADR stage copies it into a record of what was actually built.

Feature: `$ARGUMENTS`

## Author mode

1. **Read `intent.md`, `spec.md` and `egm/concepts_brief.md`.** Stop if the spec isn't approved. For a low-risk spec, ask the approver whether to skip this stage. A skip records its reason and also skips the ADR.

2. **Write the RFC** with the `rfc` skill, using the overrides in `rfc-skill.md`, so it lands at `docs/sdlc/<slug>/rfc.src.html` and `rfc.html`. If the `rfc` skill isn't available, use the `egm-draft` fallback in `rfc-skill.md`, which writes `rfc.md`.

3. **Check it against the spec.** Every requirement must be met by the chosen design, and every acceptance criterion must have a test planned somewhere in the phases. List any gap as an open question tagged "before approval".

4. **Check the design's claims.** Invoke `fv-toolkit:formal-verification` on each sentence in the spec and the RFC that says never, always, at most once or exactly once, with the inputs and overrides in `fv-toolkit.md`. Its triage says whether a claim earns a formal check, and most features have none. When one does, the approver confirms the properties, and the skill models the design and checks it before any code exists. A counterexample changes the design. Without the toolkit, name each such claim to the approver and record why the check didn't run.

5. **Gate.** The Goldfish review is `egm-review` with the `feature_spec` preset, and its Stage 7 resolves the findings with `egm-resolve`. Rebuild `rfc.html` after any fix. If the `rfc` skill offers its Notion mirror, pass that offer on to the user. Commit the RFC source, the built page, the `egm/` reports, the `fv/` folder if there is one, and `sdlc.yaml` together.

## Adopt and review modes

Follow `stage-rules.md`, using the same Goldfish review. An adopted RFC that's already HTML stays in its form. An adopted Notion page or Google Doc is fetched into `rfc.md`.
