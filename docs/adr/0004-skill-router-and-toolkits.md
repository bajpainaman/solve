# One router over pinned skills and toolkits

Date: 2026-11-20
Status: Accepted.

## Problem

The user asked for solve, CDPI, html-artifact, impeccable and four aasimsani toolkits (testing, formal
verification, SDLC, PR review) to work as one collection: route each request to the right skill, know what every
subskill does, follow upstream changes, and suggest the next skill after each request. The toolkits hold 49
skills, and several overlap with each other and with solve, cdpi and impeccable.

## Decisions

- One generated `skill-router` skill is the entry point. Its fixed part, `plugin/router/HEADER.md`, holds the lead
  table, the overlap rules and the next-step table. Its catalog is generated from the vendored files, so a pin bump
  updates it in the same commit. A test keeps it under 20 KB, because it is meant to load in every session.
- Each toolkit installs as one skill. Our entry `SKILL.md` from `plugin/wrappers/<id>/` sits at the toolkit root,
  and the upstream skills stay under `skills/<id>/skills/`. The skills CLI stops at the shallower `SKILL.md`, so the
  49 subskills do not register as separate skills, collide with names already installed (`test-audit`, `review`,
  `ship`, `plan`) or load their descriptions in every session.
- The four toolkits are MIT, so they are vendored with their `LICENSE` and, for fv-toolkit, `NOTICE.md`. Evals,
  plugin manifests and hooks are not copied: they add size or run on session start without being read.
  html-artifact and CDPI's ai-skills have no license and stay fetched-only, as in ADR-0002 and the cdpi skill.
- Updates are pull-based and reviewed. `bin/check-updates` reports newer upstream commits. `bin/vendor-sync <id>
  --review <ref>` lists the changes and flags new skills, scripts, hooks and license changes. A person bumps the
  pin. `bin/vendor-sync` refuses a license whose hash differs from the pin and any symlink. Nothing fetches or runs
  upstream instructions on its own.
- Upstream workflows that install tools, start paid model runs or write hooks (fv-install, pr-review.sh, sdlc
  setup) need the user's approval before the first such step in a session. The router says so once.

## Limits

The upstream skills are written for Claude Code plugins (`${CLAUDE_PLUGIN_ROOT}`, the Skill tool, `claude plugin`).
The entry skills map those to paths, but sdlc-toolkit setup and pr-review still need the `claude` CLI. EGM and
ponytail, which sdlc-toolkit calls, are not bundled. Routing quality is not measured; an eval of the router on
real requests is pending and needs approval for model spend.
