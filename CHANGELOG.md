# Changelog

All notable changes to `/solve` are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Pending
- Self-tag releases on GitHub for pinned-curl installs (`bash <(curl -fsSL https://raw.githubusercontent.com/bajpainaman/solve/v0.5.0/install)`).
- frameworks/minto.md: surface calibration drift warning in Dissent section (planned for v0.5.1).

## [0.6.0] — 2026-05-04

### Added — tier picker (Step 0.55)

A real-world run on a friend's machine took 45 min to reach 19/25 frameworks. Most strategic decisions don't need that depth. v0.6.0 adds three tiers:

| Tier | Frameworks | Approx wallclock | Default budget |
|---|---|---|---|
| Quick | 8 (load-bearing only) | ~15-20 min | time=15min, $2 |
| Standard | 16 (drops conditional + low-leverage) | ~30-40 min | time=30min, $5 |
| Deep | all 25 | ~50-70 min | time=1h, $15 |

**Standard is the default.** The skill asks at run start (Step 0.55, between regime classifier and budget intake). Skip the question with `solve --tier <name>` flag.

Tier maps to a specific framework subset:
- **Quick** — first-principles, issue-tree, inversion-define, iceberg, cynefin, decision-matrix, six-hats, minto
- **Standard** — Quick + abstraction-ladder, zwicky-box, productive-thinking, connection-circles, concept-map, eisenhower, second-order, confidence-speed-quality
- **Deep** — Standard + ishikawa, conflict-resolution-diagram, balancing-loop, reinforcing-loop, impact-effort, ladder-of-inference, ooda-loop, hard-choice, sbi

Frameworks not in the chosen tier are skipped silently. Confidence rubric max scales with tier (Quick caps at 6/10, Standard at 8/10, Deep at 10/10).

### Added — ETA estimator

Both `bin/progress` (in-conversation block) and `bin/statusline` (Claude Code bottom bar) now show estimated remaining time when ≥ 2 frameworks have completed:

- Progress block: `ETA: ~12m remaining (4/16)`
- Statusline: `... 3/16 framework • 9m/30m $0.80/$5 ~21m left`

ETA = avg per-framework time × frameworks remaining. Tier-aware (Quick = 8, Standard = 16, Deep = 25 in the divisor).

### Added — `bin/tier` helper

```
tier list                    show all 3 tiers + counts + default budgets
tier quick                   space-separated framework list
tier standard --json         JSON with phase breakdown
tier deep --in cynefin       exit 0 if framework is in the tier
tier defaults standard       prints "1800 5" (default time + tokens)
```

### Added — `solve --tier` flag

```bash
solve --tier quick "narrow problem"
solve --tier deep --budget time=2h "high-stakes one-way decision"
```

Pre-seeds Step 0.55 answer, skipping the prompt.

### Changed

- Default budget now derives from tier (was always unlimited if user didn't specify).
- Statusline now shows the correct `N/<tier_total>` rather than always `N/25`.
- Progress block ETA + completion percentage scale with tier.
- install smoke tests verify all 10 bins.

### Why

The 45-min real-world run hit the natural ceiling of /solve's depth. Adding a tier picker lets users pick the trade-off intentionally:

- "Quick decision, low stakes" → Quick tier, ~15 min, gets the load-bearing frameworks only
- "Standard decision, normal stakes" → Standard tier (default), ~30 min, drops the conditional + redundant frameworks
- "One-way-door, high stakes" → Deep tier, full 25 frameworks with all the dissent-surfacing depth

Previous behavior (always Deep, no cap) is preserved by passing `--tier deep --budget time=unlimited`.


## [0.5.2] — 2026-05-04

### Added

- **`bin/statusline` helper** — Claude Code bottom status bar renderer. Shows `● solve <slug> [████░░░░░░] 8/25 framework-name • 4m/15m $1.20/$5` while a /solve run is active. Reads cwd from Claude Code's JSON stdin context, finds the most-recent `.context/solve/<slug>/`, computes per-phase completion + budget burn. Stays under 50ms per call.

- **Auto-config in install** (Step 4.5/7). Installer detects existing `statusLine` config in `~/.claude/settings.json`:
  - **None**: prompts (or auto-enables in non-interactive curl-bash flow) to wire `/solve` statusline.
  - **Already ours**: confirms it's set up.
  - **Custom**: warns and shows the config to set manually rather than overwriting.

### Changed

- install smoke tests now verify all 9 bins.
- SKILL.md version 0.5.1 → 0.5.2.

### Why

Real-world feedback: the v0.5.1 progress block (printed as a tool-call result in the conversation) is informative but only visible when you scroll. Claude Code's bottom status bar is always visible. Wiring our progress into that bar means the user sees /solve state at a glance, alongside the token count and permissions indicator.


## [0.5.1] — 2026-05-04

### Added

- **`bin/progress` helper** — multi-phase Unicode progress bar for /solve runs. Shows Phase 1/2/3 completion (`[████████████░░░░░░░░] 8/12`), adversary max score with low/moderate/high label, budget burn (time + cost vs caps), latest framework written. Modes: default rich block, `--plain` single-line, `--watch` repaint every 2s.

- **`solve progress`** subcommand. Reads the most-recent run dir under `.context/solve/` and shows the snapshot. Useful for checking a long-running session from a separate terminal.

- **SKILL.md Step 8 now invokes `bin/progress`** between framework boundaries so the user sees live progress as a tool-call result. Print rules: at start of each phase, after each framework, on HALT, before report rendering.

### Changed

- install smoke tests now verify all 8 bins (added `progress`).
- SKILL.md version bumped to 0.5.1.


## [0.5.0] — 2026-05-04

### Added

- **Step 0.6 — Budget intake** (after regime classifier, before preamble; runs only if `regime = decision`).
  AskUserQuestion for time + tokens budget. Time options: 5min / 15min / 30min / 1hr / unlimited. Token options: $1 / $5 / $20 / unlimited. User picks one or both. Both null = unlimited (backward compat).
  `bin/budget-track` enforces both axes between framework boundaries: warns at 80%, halts entire run at 100%.

- **Step 0.7 — Calibration check + audit** (after budget; runs only if `regime = decision`).
  Reads `~/.gstack/calibration.jsonl` ledger. If most-recent HIGH-bucket entry is 3-30 days old and outcome is TBD, asks the user "did it ship?" and updates the ledger. Auto-detects shipped recommendation via git log scan as a hint (user always confirms).
  Drift audit: if HIGH success rate < 70% over ≥ 10 settled HIGH runs, raise rubric requirement from 8 to 9 automatically. Warning surfaced at next run start AND in next run's Dissent section. User can revert with `solve --calibrate reset`.

- **Step 8.5 — Tool-call cap enforcement** (non-negotiable guardrail).
  Each teammate has a counter file at `$RUN_DIR/teammate-counters/<name>.json` tracking calls per tool (Bash/Read/Write/Edit/Glob/Grep/WebSearch/WebFetch). Hit 6 of any single tool = halt entire run. Adversary is exempt from the Read cap (it watches every framework file, legitimately needs many reads). Hat teammates get fresh counters per spawn.
  Rationale: catches loop bugs (a teammate retrying the same Bash command) without penalizing legitimate work (a definer reading 8 framework specs).

- **AskUserQuestion auto-conversion** (in adversary brief).
  Adversary scans framework outputs for prose questions ending in `?`. Writes `$RUN_DIR/pending-questions/<framework>-<n>.json` for each non-rhetorical question. Lead polls between framework boundaries, invokes AskUserQuestion, relays answer to originating teammate via SendMessage, deletes the pending file.
  Rhetorical filter: questions containing "this means" / "obviously" / "of course" are skipped. Framework templates can opt out with `<!-- skip-question-scan -->`.

- **`solve --calibrate <subcommand>`** routes to the new bin/calibration helper. Subcommands: status, audit, reset, log, log-outcome, detect-shipped, pending-followup.

- **`solve --budget`** flag pre-seeds Step 0.6 answers, skipping the AskUserQuestion. Format: `solve --budget time=15min tokens=$5 "<problem>"`. Either or both axes optional.

- **`solve status`** (already in 0.4.0) now prints v0.5.0.

- **`bin/budget-track`** new helper — wallclock + token spend tracker with per-tool, per-teammate caps. Output: JSON status with verdict (under_cap / warned_time / warned_tokens / halted_time / halted_tokens / unlimited).

- **`bin/calibration`** new helper — append-only ledger + drift audit. ~150 lines covering log/log-outcome/status/audit/reset/detect-shipped/pending-followup.

### Changed

- **SKILL.md** grew from 944 to 1332 lines.
- **Adversary brief** now includes the question auto-conversion protocol AND a Read-exempt cap-tracking note.
- **All 4 non-adversary teammate briefs** now end with the TOOL CALL CAP instruction block.
- **Step 8 (Communication Protocol)** now describes the lead's pending-questions polling loop and budget-track polling loop between framework boundaries.
- **Step 16 (Cost + Telemetry)** now appends a calibration ledger row at end of each completed run with `outcome: TBD`.
- **install** smoke tests now verify all 7 bins (added budget-track + calibration to the loop).

### Fixed (carried forward from v0.4.0 patches)

- Framework count smoke test correctly excludes `_TEMPLATE.md` (was warning "framework count != 25").
- `solve update` typo (without `--`) now triggers the updater, not the skill on the word.
- `parallel-setup` removed the wrong sk-/pk- prefix warning; added length sanity check; "Store anyway?" prompt now masks the buffer and explicitly tells the user not to paste the key again.

### Architecture rationale

The v0.5.0 changes close 3 loops the v0.4.0 install run exposed:
1. **No budget guardrails** → runs could spiral on edge cases. Now: hard halt with clear restart instructions.
2. **No tool-call caps** → a stuck teammate could burn the budget alone. Now: 6 of any tool = halt.
3. **Calibration drift was invisible** → HIGH bucket could silently mean "matrix winner but world disagreed." Now: ledger + 70% threshold + auto-shift + dissent surface.

The fourth piece (AskUserQuestion auto-conversion) is preventive: teammates occasionally write inline prose questions that get lost. Now the adversary catches them and the lead routes through proper UI.


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

[Unreleased]: https://github.com/bajpainaman/solve/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/bajpainaman/solve/compare/v0.5.2...v0.6.0
[0.5.2]: https://github.com/bajpainaman/solve/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/bajpainaman/solve/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/bajpainaman/solve/compare/v0.3.0...v0.5.0
[0.3.0]: https://github.com/bajpainaman/solve/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/bajpainaman/solve/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/bajpainaman/solve/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bajpainaman/solve/releases/tag/v0.1.0
