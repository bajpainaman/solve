# Companion skills from other workflow plugins

Superpowers and agent-skills are often installed next to this plugin. Each one defines its own lifecycle, and its session-start text tells Claude to invoke its skills before anything else. Inside an sdlc stage, the stage is the workflow. A companion skill is know-how for one step of it.

## Decide in three questions

1. **Does the stage already produce this artifact or run this review?** Then skip the companion. Running both does the work twice and leaves two artifacts that can disagree. The "Repeats the stage" column lists these.
2. **Does the companion add know-how for the step you're on?** Then load it for that step. Take its guidance and leave its workflow. The "Adds something" column lists these.
3. **Do two companions cover the same ground?** Load one. The two `test-driven-development` skills overlap, and so do `superpowers:systematic-debugging` and `agent-skills:debugging-and-error-recovery`.

A companion never replaces a stage's artifact, its gate or its fresh-context review. When a companion's text conflicts with the stage, the stage wins. When the user's instructions conflict with either, the user's instructions win.

Outside a stage, such as a quick fix that doesn't go through the loop, use these plugins the way they describe themselves.

## By stage

| Stage | Adds something | Repeats the stage |
|---|---|---|
| Intent | Nothing by default. When the approver skips the EGM swarm, `superpowers:brainstorming` or `agent-skills:idea-refine` can run the interview. | `superpowers:brainstorming` and `agent-skills:idea-refine`, because `egm-brainstorm` already questions the originator and stress-tests the idea. |
| Spec | `agent-skills:api-and-interface-design` when the change adds or changes an interface. `agent-skills:security-and-hardening` as a checklist for a high-risk spec. | `agent-skills:spec-driven-development`, because the stage owns `spec.md`. |
| RFC | `agent-skills:api-and-interface-design`. `agent-skills:deprecation-and-migration` when the design retires something. | `agent-skills:documentation-and-adrs`, because the RFC and ADR stages own those records. |
| Plan | Nothing by default. | `superpowers:writing-plans` and `agent-skills:planning-and-task-breakdown`, because the stage owns `plan.md` and a second plan file would split the todo list. |
| Build | `superpowers:systematic-debugging` when a test fails for a reason you didn't expect. `superpowers:receiving-code-review` before acting on a pr-review finding you doubt. `agent-skills:source-driven-development` when the code calls a library API you haven't checked. `agent-skills:frontend-ui-engineering` for UI work. `superpowers:using-git-worktrees` for the mechanics of parallel phases. | Both `test-driven-development` skills, `agent-skills:incremental-implementation`, `superpowers:executing-plans` and `superpowers:subagent-driven-development`, because Build already runs the plan phase by phase, test first. `superpowers:verification-before-completion`, because the verify command and the Test stage cover it. |
| Test | `agent-skills:browser-testing-with-devtools` for a UI. `agent-skills:performance-optimization` when the spec sets a performance number. The `agent-skills:security-auditor` agent for a high-risk spec. The `agent-skills:test-engineer` agent when `verify.md` lists gaps and the testing toolkit isn't installed. | `superpowers:requesting-code-review`, `agent-skills:code-review-and-quality` and its `code-reviewer` agent, because pr-review is the stage's code review. Add a second reviewer only as a different perspective the approver asks for. |
| Ship | `agent-skills:shipping-and-launch` for the deploy and rollback steps in `review.md`. `agent-skills:ci-cd-and-automation` when the deploy needs a pipeline change. `superpowers:receiving-code-review` for the human reviewer's comments. | `superpowers:finishing-a-development-branch`, because it offers to merge the branch itself, and in this loop a human merges. |
| ADR | Nothing by default. | `agent-skills:documentation-and-adrs`, because the ADR here is a copy of the RFC and a second format would compete with it. |
| Maintain | `superpowers:systematic-debugging` for an incident's diagnosis. `agent-skills:deprecation-and-migration` when a follow-up removes something. | `agent-skills:code-simplification`, because `ponytail-audit` already ranks what to cut. |
