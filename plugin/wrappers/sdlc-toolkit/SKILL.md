---
name: sdlc-toolkit
description: "Runs a feature through a gated lifecycle with one committed artifact per stage under docs/sdlc/<slug>/: intent, spec, RFC, plan, build, test and prove, ship, ADR and maintain, plus repo setup and demos. Use when asked to run the SDLC, start a feature the SDLC way, see which stage a feature is at, write or adopt a spec, RFC, plan or ADR in that loop, or feed an incident back as a new intent. Not for a one-off change outside the loop."
license: MIT
---

# SDLC toolkit

Vendored from [aasimsani/sdlc-toolkit](https://github.com/aasimsani/sdlc-toolkit) (MIT, see `LICENSE`) at the commit in `SOURCE`. Change it only through `bin/vendor-sync sdlc-toolkit` in the solve repository.

`TOOLKIT_ROOT` is the directory that contains this file. The upstream skills say `${CLAUDE_PLUGIN_ROOT}`; read that as `TOOLKIT_ROOT`. Where one says to invoke `sdlc:<stage>` with the Skill tool, read `TOOLKIT_ROOT/skills/<stage>/SKILL.md`. Its companions map to sibling skills here: `testing-toolkit:*` is `../testing-toolkit`, `fv-toolkit` is `../fv-toolkit`, and `pr-review` is `../pr-review`. EGM and ponytail are not bundled; when a stage needs them and they are missing, follow the stage's own fallback and record the tool as skipped.

## Route

Start with `skills/sdlc/SKILL.md`. It reads `sdlc.yaml`, reports the stage, and names the one stage skill to read next.

| Stage | Read | Leaves |
|---|---|---|
| Setup, once per repo | `skills/setup/SKILL.md` | verify command, `REVIEW.md`, `docs/sdlc/` |
| 1 Intent | `skills/intent/SKILL.md` | `intent.md` |
| 2 Spec | `skills/spec/SKILL.md` | `spec.md` |
| 3 RFC | `skills/rfc/SKILL.md` | `rfc.html` |
| 4 Plan | `skills/plan/SKILL.md` | `plan.md` with chosen tests |
| 5 Build | `skills/build/SKILL.md` | code and tests, test first |
| 6 Test & Prove | `skills/test/SKILL.md`, `skills/demo/SKILL.md` | `verify.md`, proof page |
| 7 Ship | `skills/ship/SKILL.md` | PR, `review.md` |
| 8 ADR | `skills/adr/SKILL.md` | `adr.html` |
| 9 Maintain | `skills/maintain/SKILL.md` | `lessons.md` |

Setup installs plugins and writes repo files. Ask before each install, hook and commit, as the setup skill says. The upstream setup targets Claude Code (`claude plugin ...`); on another host, say which steps do not apply.

## Boundaries with neighbours

- An open choice with stakes inside a stage (which queue, build or buy) goes to `solve` decide; its memo is an input to the RFC.
- The RFC's architecture review can add the `cdpi` lens. A frontend surface in Build can add `impeccable`.
- A repo that only needs ADRs in `docs/adr/` without the loop stays outside this toolkit.

## After the work

Each stage ends by offering the next stage, and stopping is normal because the next stage may belong to someone else. Name who it waits on.
