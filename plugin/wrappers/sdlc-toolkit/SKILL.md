---
name: sdlc-toolkit
description: "Runs a feature through a gated lifecycle with one committed artifact per stage under docs/sdlc/<slug>/: intent, spec, RFC, plan, build, test and prove, ship, ADR and maintain, plus repo setup and demos. Use when asked to run the SDLC, start a feature the SDLC way, see which stage a feature is at, write or adopt a spec, RFC, plan or ADR in that loop, or feed an incident back as a new intent. Not for a one-off change outside the loop."
license: MIT
---

# SDLC toolkit

Vendored from [aasimsani/sdlc-toolkit](https://github.com/aasimsani/sdlc-toolkit) (MIT, see `LICENSE`) at the commit in `SOURCE`. Change it only through `bin/vendor-sync sdlc-toolkit` in the solve repository.

`TOOLKIT_ROOT` is the directory that contains this file. The upstream skills say `${CLAUDE_PLUGIN_ROOT}`; read that as `TOOLKIT_ROOT`. Its stage skills are not registered as separate skills: each one's instructions are in `TOOLKIT_ROOT/skills/<stage>/SKILL.upstream.md`. Where the upstream text says to invoke `sdlc:<stage>` with the Skill tool, read that file instead. Its companions map to sibling skills here: `testing-toolkit:<name>` is `../testing-toolkit/skills/<name>/SKILL.upstream.md`, the `formal-verification` skill is `../fv-toolkit/skills/formal-verification/SKILL.upstream.md`, and `pr-review` is the `pr-review` skill. EGM and ponytail are not bundled; when a stage needs them and they are missing, follow the stage's own fallback and record the tool as skipped.

## Route

Start with `skills/sdlc/SKILL.upstream.md`. It reads `sdlc.yaml`, reports the stage, and names the one stage skill to read next.

| Stage | Read | Leaves |
|---|---|---|
| Setup, once per repo | `skills/setup/SKILL.upstream.md` | verify command, `REVIEW.md`, `docs/sdlc/` |
| 1 Intent | `skills/intent/SKILL.upstream.md` | `intent.md` |
| 2 Spec | `skills/spec/SKILL.upstream.md` | `spec.md` |
| 3 RFC | `skills/rfc/SKILL.upstream.md` | `rfc.html` |
| 4 Plan | `skills/plan/SKILL.upstream.md` | `plan.md` with chosen tests |
| 5 Build | `skills/build/SKILL.upstream.md` | code and tests, test first |
| 6 Test & Prove | `skills/test/SKILL.upstream.md`, `skills/demo/SKILL.upstream.md` | `verify.md`, proof page |
| 7 Ship | `skills/ship/SKILL.upstream.md` | PR, `review.md` |
| 8 ADR | `skills/adr/SKILL.upstream.md` | `adr.html` |
| 9 Maintain | `skills/maintain/SKILL.upstream.md` | `lessons.md` |

Setup installs plugins and writes repo files. Ask before each install, hook and commit, as the setup skill says. The upstream setup targets Claude Code (`claude plugin ...`); on another host, say which steps do not apply.

## Boundaries with neighbours

- An open choice with stakes inside a stage (which queue, build or buy) goes to `solve` decide; its memo is an input to the RFC.
- The RFC's architecture review can add the `cdpi` lens. A frontend surface in Build can add `impeccable`.
- A repo that only needs ADRs in `docs/adr/` without the loop stays outside this toolkit.

## After the work

Each stage ends by offering the next stage, and stopping is normal because the next stage may belong to someone else. Name who it waits on.
