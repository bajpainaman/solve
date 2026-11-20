---
name: adr
description: SDLC stage 8. After the PR merges, copies the approved RFC into an architectural decision record and updates the copy to match what actually shipped, using EGM's drift report to find where the code diverged. The RFC stays unchanged. Use when the user runs /sdlc:adr or the sdlc skill routes here.
argument-hint: "<slug>"
---

# Stage 8 — ADR

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. This stage also uses `${CLAUDE_PLUGIN_ROOT}/references/egm.md`.

The RFC records what we proposed. The ADR records what we decided and built. The ADR starts as a copy of the RFC, and the RFC itself never changes, so a reader can compare the two.

Feature: `$ARGUMENTS`

## Steps

1. **Check the inputs.** Stop if Ship isn't approved. If the RFC was skipped, skip this stage too and record why.

2. **Copy the RFC.** Copy `rfc.src.html` to `adr.src.html`, or `rfc.md` to `adr.md`. Commit nothing yet.

3. **Find what changed.** Run `egm-drift-report` on the RFC to list where the merged code diverges from it. Also read the departures recorded in `plan.md`, the won't-fix findings in `review.md`, and the gaps in `verify.md`.

4. **Turn the copy into an ADR:**
   - Change the masthead to `ADR: <decision as a sentence>`, with status Accepted, the merge date, the PR link and the approvers.
   - Keep Problem and goal, Constraints and Options as they were. Those sections are the decision's context.
   - Rename Chosen solution to Decision, and correct it to describe what shipped.
   - Replace Build plan, Phases and Proposed tickets with an "As built" section. It lists the merged PRs and every divergence from the RFC, with the reason for each.
   - Rename Blast radius to Consequences, and keep each row's detection and rollback.
   - Add "Supersedes" or "Superseded by" lines when the decision replaces an earlier ADR.

5. **Build it.** For the HTML form, build `adr.html` the way the `rfc` skill builds an RFC.

6. **Gate.** The approver checks the ADR against the drift report. Commit `adr.src.html`, `adr.html` (or `adr.md`), the drift report and `sdlc.yaml` together.
