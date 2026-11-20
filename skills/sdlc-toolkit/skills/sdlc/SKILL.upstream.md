---
name: sdlc
description: Entry point for the AI-native SDLC loop. Use when the user types /sdlc, asks to "run the SDLC", start a feature the SDLC way, see the status of features in flight, or find out which stage a feature is at. Reads docs/sdlc/<slug>/sdlc.yaml, reports the stage, and runs the next stage skill.
argument-hint: "[slug | new idea in plain words] [--adopt <path|url>] [--review]"
---

# /sdlc — show status or run the next stage

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first. It defines `sdlc.yaml`, the three modes, and the gate every stage ends with.

Each stage ends by committing one artifact, and that commit starts the next stage. Everything lives in `docs/sdlc/<slug>/`, so the folder's git history records who asked for what, what was produced, and who approved it.

| # | Stage | Skill | Artifact | Fresh-context review |
|---|---|---|---|---|
| 1 | Intent | `sdlc:intent` | `intent.md` (from EGM's concepts brief) | `egm-brainstorm` swarm |
| 2 | Spec | `sdlc:spec` | `spec.md` | `egm-review-loop` |
| 3 | RFC | `sdlc:rfc` | `rfc.src.html` + `rfc.html` | the fv-toolkit's check of the design's claims, `egm-review`, then `egm-resolve` |
| 4 | Plan | `sdlc:plan` | `plan.md`, with the tests the testing toolkit chose | `egm-review` implementation stage |
| 5 | Build | `sdlc:build` | code + tests, each test written first | ponytail mode while coding, then `pr-review --local` with the ponytail lens after each phase |
| 6 | Test & Prove | `sdlc:test` | `verify.md` + `proof/proof.html` | the testing toolkit's final tests, check and audit, final `pr-review --local` with the ponytail lens, the `verifier` subagent, the `fv-verifier` subagent when the design was modelled + a demo from `sdlc:demo` when the approver wants one |
| 7 | Ship | `sdlc:ship` | PR + `review.md` | `pr-review --repo --pr`, then a human |
| 8 | ADR | `sdlc:adr` | `adr.src.html` + `adr.html` (a copy of the RFC, updated to what shipped) | `egm-drift-report` |
| 9 | Maintain | `sdlc:maintain` | `lessons.md` | `egm-drift-report`, `ponytail-audit`, live signals |

Arguments: `$ARGUMENTS`

## Steps

1. **Check the repo is set up.** The repo is ready when `CLAUDE.md` names one verify command, `REVIEW.md` exists at the root, and the plugins the stages call are installed. Check with `claude plugin list --json`: the `sdlc-stack@sdlc-toolkit` entry is enabled and has no `errors`. If anything is missing, say what's missing and offer to run `sdlc:setup` first.

2. **With no argument, show the status board.** Read every `docs/sdlc/*/sdlc.yaml`, fetching first so teammates' branches are included. Then print one row per feature that isn't closed.

   | Feature | Stage | Owner | Waiting on | Branch | Last change |
   |---|---|---|---|---|---|

   "Waiting on" is the approver when the current stage is a draft that's ready for review. Otherwise it's the owner. Then ask which feature to continue, or offer to start a new one.

3. **Resolve the feature.**
   - If the argument matches a folder in `docs/sdlc/`, use that feature.
   - If the argument is a sentence, treat it as a new idea. Derive a short kebab-case slug, confirm it, and create `sdlc.yaml`.

4. **Find the stage.** It's the first stage in the table whose status isn't `approved` or `skipped`. A feature with every stage done is closed, so say so and stop. For a feature at Build, count the phases in `plan.md` that are `done`, so the report can say how far along it is.

5. **Report and run.** Tell the user in one line where the feature is and who it's waiting on, for example "`bulk-export` is at Plan. The plan is a draft owned by Priya and needs Aasim's approval." Then invoke the stage skill with the Skill tool, passing the slug and any `--adopt` or `--review` flag.

6. **Offer the next stage.** When the stage commits, ask whether to continue to the next stage now or stop. Stopping is normal, because the next stage may belong to someone else.
