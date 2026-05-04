# Changelog

All notable changes to `/solve` are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Pending
- Deepen remaining 11 framework files: ishikawa, inversion-define, iceberg, connection-circles, eisenhower, impact-effort, ladder-of-inference, ooda-loop, hard-choice, six-hats, minto. Agent fan-out in flight.
- Self-tag releases on GitHub for pinned-curl installs (`bash <(curl -fsSL https://raw.githubusercontent.com/bajpainaman/solve/v0.3.0/install)`).

## [0.3.0] — 2026-05-03

### Added
- **Deep gstack integration.** SKILL.md grew from 541 to 944 lines. Gstack touchpoints from 7 to 53.
- New skill-level sections: Plan Mode Safe Operations, Confusion Protocol, Continuous Checkpoint Mode, Context Health, Repo Ownership, Search Before Building (eureka pattern), Boil the Lake (completeness principle), Writing Style + jargon glosses.
- `gstack-update-check` in Step 0 surfaces `UPGRADE_AVAILABLE` and `JUST_UPGRADED`.
- `gstack-config` reads in Step 0: `proactive`, `explain_level`, `question_tuning`, `telemetry`, `cross_project_learnings`, `checkpoint_mode`, `checkpoint_push`.
- `gstack-repo-mode` integration (solo / collaborative / unknown) shapes how teammates flag anomalies.
- `gstack-learnings-search` in Step 1 surfaces prior insights for the slug. Prompts for `cross_project_learnings` opt-in on first run.
- Context Recovery: lists prior `/solve` runs for the slug, asks build-on-prior vs start-fresh.
- CLAUDE.md routing-rules check; suggests adding `/solve` route if missing.
- `gstack-question-preference --check` + `gstack-question-log` wraps every AskUserQuestion in Steps 4 + 5.
- Eureka logging pattern: definer logs contrarian first-principles findings to `~/.gstack/analytics/eureka.jsonl`.
- `gstack-review-log` writes after each cross-skill handoff completes.
- OPENCLAW_SESSION detection auto-modes the run for orchestrated invocations.
- Continuous Checkpoint Mode: WIP commits between framework files when `checkpoint_mode=continuous`.
- Adversary teammate now enforces the no-AI-vocab voice rule with line-number flags.

### Deepened
- 14 of 25 framework files expanded from ~30-60 lines to 600-1000 lines each, following the new `frameworks/_TEMPLATE.md` (17 required sections):
  - Define: abstraction-ladder, first-principles, issue-tree, zwicky-box, conflict-resolution-diagram, productive-thinking
  - Systems: balancing-loop, reinforcing-loop, concept-map
  - Decide: cynefin (canonical exemplar), decision-matrix, second-order, confidence-speed-quality, sbi
- All deepened frameworks share the canonical OFTv2 migration worked example for continuity.
- Total framework content jumped from ~1k to ~12k lines.

### Documentation
- README rewritten with the deconstruct → systems → rebuild metaphor.
- 8 mermaid diagrams: journey, full 25-framework DAG, Phase 1/2/3 zooms, agent team, OFTv2 walkthrough, layered research stack.
- New 25-frameworks-at-a-glance table with phase, run condition, and line counts.
- License finalized (MIT).

## [0.2.1] — 2026-05-03

### Added
- `solve` CLI shim now exports `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` itself before exec'ing claude. Every `solve "..."` invocation gets the flag guaranteed.
- Installer writes a single marked block to `~/.zshrc` / `~/.bashrc` / `~/.bash_profile` exporting both PATH and the experimental flag. Block is regenerated idempotently on every install.
- Triple-redundancy: env var in shell rc + settings.json env + shim self-export.

### Fixed
- `parallel-setup --help` previously leaked the `set -euo pipefail` line; sed range tightened to lines 2-14.

## [0.2.0] — 2026-05-03

### Added
- Standalone repo at `github.com/bajpainaman/solve`. Canonical source moves to `~/code/solve`; symlinked from `~/.claude/skills/solve` after install.
- `solve` CLI shim at `~/.local/bin/solve`. Type `solve "<problem>"` from any zsh/bash terminal.
- One-line installer with curl-bash one-liner: `bash <(curl -fsSL https://raw.githubusercontent.com/bajpainaman/solve/main/install)`.
- Installer features: claude version check, agent-teams flag setup, PATH edits to rc files, `parallel-setup` walkthrough, smoke tests, idempotent re-runs.
- `solve --update` (re-runs installer to refresh from upstream) and `solve --uninstall` (removes skill, shim, rc edits with backups; preserves Parallel.ai key).

### Changed
- SKILL.md fully rewritten for agent-teams orchestration (v0.2.0).
  - Step 0 self-check: skill installed + agent-teams flag + claude >= 2.1.32.
  - Step 6: `TeamCreate` bootstraps `solve-<slug>` team.
  - Step 7: spawns 5 long-lived teammates (researcher, definer, systems-thinker, decider, adversary) with self-contained briefs.
  - Step 8: communication protocol — TaskUpdate(owner) + SendMessage peer-to-peer.
  - Step 10: Six Hats burst spawns 6 fresh teammates mid-Phase-3 in a single parallel batch.
  - Step 14: graceful TeamDelete cleanup.

### Removed
- The orchestrator no longer uses one-off Agent subagent calls for Phase work. All execution goes through agent teams exclusively.

## [0.1.0] — 2026-05-03

### Added
- Initial release.
- 25 framework specs covering 3 phases (Define, Systems, Decide) sourced from [untools.co](https://untools.co/).
- 5 helper scripts: `parallel-research`, `parallel-setup`, `state-rw`, `cost-track`, `render-report`.
- Layered research stack: Parallel.ai breadth + WebSearch follow-ups + gstack browse deep extraction. Auto-degrades silently if no `PARALLEL_API_KEY`.
- Cross-skill mid-run auto-handoffs: `/investigate` (iceberg bug-shape), `/office-hours` (pre-product framing), `/plan-eng-review` (architecture decision at end).
- Confidence math: 0-10 rubric + Bayesian posterior + HIGH/MED/LOW bucket.
- Continuous adversary subagent flags every framework output.
- 5-question pre-flight intake (stakeholders, time pressure, reversibility, decision-maker, success criteria).
- Resume-safe state at `.context/solve/<slug>/state.json`.
- Output formats: pyramid (Minto top-down), build-up, tldr.
- Soft cost cap at $5 of API spend.

[Unreleased]: https://github.com/bajpainaman/solve/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/bajpainaman/solve/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/bajpainaman/solve/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/bajpainaman/solve/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bajpainaman/solve/releases/tag/v0.1.0
