# Running EGM skills

EGM is Google's Elephant-Goldfish Model plugin. Its Goldfish reviewers read a document with no memory of the conversation that produced it. `sdlc:setup` installs it.

## Find EGM

```bash
claude plugin list --json | jq -r '.[] | select(.enabled and .id == "egm@egm") | .installPath'
```

The command prints `EGM_ROOT`. If it prints nothing, EGM isn't installed or isn't enabled, so tell the user to run `sdlc:setup`. Never guess the path.

## Run a skill

EGM's skills set `disable-model-invocation`, so the Skill tool refuses them. EGM's own Claude Code guide says to read the skill's `SKILL.md` and follow it in the same thread. To run `egm-<name>`, take these steps:

1. Read `$EGM_ROOT/docs/claude.md`, then `$EGM_ROOT/skills/egm-<name>/SKILL.md`.
2. Follow that skill in this thread. When it names `${CLAUDE_PLUGIN_ROOT}` or a plugin-relative path such as `agents/`, `resources/` or `docs/`, read it under `EGM_ROOT`. Dispatch each Goldfish as the named subagent `egm:egm-<persona>`, such as `egm:egm-zoom-out`.
3. Treat `docs/sdlc/<slug>/egm/` as the EGM artifact directory. Every brief, draft and report EGM writes goes there and is committed with the stage.
4. Pass the inputs from the table below up front, so EGM doesn't stop to ask for them.
5. Follow EGM's rules while its skill runs, and only then. Its skill files are long and strict. They allow one question per turn with no "Recommended" labels, and they ban certain words. Those rules shape EGM's own questions and reports. They don't carry over to the rest of the stage. Return to the stage when the EGM skill reaches its terminal gate.

The **Goldfish context** for a feature is `CLAUDE.md`, the earlier approved artifacts in `docs/sdlc/<slug>/`, and the `README.md` of each directory the change touches.

## Which skill each stage runs

| Stage | EGM skill | Inputs |
|---|---|---|
| Setup | `egm-bootstrap` | `path`: the repo root, or the subtree the team owns |
| Intent | `egm-brainstorm` | The originator's description of the problem |
| Intent, adopt or review mode | `egm-review-loop` | `TargetFile: intent.md`, `SemanticTarget: full file`, `Reviewers: [egm-comprehension, egm-zoom-out]`, `Standards: {egm-comprehension: heilmeier-standard, egm-zoom-out: zoom-out-standard}`, the Goldfish context |
| Spec | `egm-review-loop` | `TargetFile: spec.md`, `SemanticTarget: full file`, `Reviewers: [egm-comprehension, egm-zoom-out]`, `Standards: {egm-comprehension: feature-spec-standard, egm-zoom-out: zoom-out-standard}`, the Goldfish context |
| RFC | `egm-draft`, only when the `rfc` skill isn't available | The concepts brief, `intent.md` and `spec.md` |
| RFC | `egm-review` | `TargetFile`: the RFC source, `Step: feature_spec`, the Goldfish context. Its Stage 7 runs `egm-resolve` on the findings. |
| Plan | `egm-review` | `TargetFile: plan.md`, `Step: implementation`, the Goldfish context plus the RFC |
| ADR | `egm-drift-report` | The RFC, to list where the code diverged from it |
| Maintain | `egm-drift-report` | `docs/sdlc/`, to check every ADR against the current code |
| Any review mode | `egm-resolve` | The report's findings, worked through with the artifact's owner |
