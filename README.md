# solve — Strategic Problem Solver

Adaptive 25-framework problem-solving skill built from [untools.co](https://untools.co/).
Orchestrates a Claude Code [agent team](https://code.claude.com/docs/en/agent-teams) (5 long-lived
teammates + 6 just-in-time Six-Hats roleplays) across Define → Systems → Decide phases with
layered parallel web research, continuous devil's-advocate, and Minto-pyramid synthesis.

## Install (one line)

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/bajpainaman/solve/main/install)
```

Or after cloning:

```bash
git clone https://github.com/bajpainaman/solve.git && cd solve && ./install
```

The installer:
1. Verifies `claude --version` ≥ 2.1.32 (agent teams requirement)
2. Symlinks the skill to `~/.claude/skills/solve` so it loads in every project
3. Drops a `solve` CLI shim at `~/.local/bin/solve` and ensures `~/.local/bin` is on PATH (edits `~/.zshrc` / `~/.bashrc` if needed)
4. Adds `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to `~/.claude/settings.json` (merge, not overwrite)
5. Walks through Parallel.ai API key setup interactively (skippable — `/solve` degrades to WebSearch + browse if no key)
6. Smoke-tests every helper script

Re-run any time (idempotent): `solve --update`. Remove cleanly: `solve --uninstall`.

## Usage

After install, `solve` is a real shell command:

```bash
solve                              # interactive intake
solve "should we migrate to OFTv2" # one-line problem
solve docs/problem.md              # path to written brief
```

Inside an already-running Claude Code session, the slash form works too:

```text
/solve "should we migrate to OFTv2"
```

## How it works

**Step 0 — Self-check.** Verifies install + agent-teams flag + claude version. Bails with the install one-liner if anything's missing.

**Step 1-5 — Lead-only setup.** Preamble, input resolve, resume detect, 5-question intake, output format pick.

**Step 6 — TeamCreate.** Spins up `solve-<slug>` team. Shared task list at `~/.claude/tasks/solve-<slug>/`.

**Step 7 — Spawn 5 long-lived teammates:**
| Name | Role |
|---|---|
| `researcher` | Layered web research (Parallel.ai → WebSearch → gstack browse) |
| `definer` | Phase 1: 8 Define frameworks |
| `systems-thinker` | Phase 2: 5 Systems frameworks |
| `decider` | Phase 3: 12 Decide frameworks (excluding Six Hats fan-out) |
| `adversary` | Continuous devil's-advocate — flags weakness in every framework output |

**Step 8 — Communication protocol.** Lead assigns work via TaskUpdate(owner=...). Teammates self-claim from the shared list. Peers SendMessage when they need each other (e.g. `definer` → `researcher` for a sub-question; `adversary` → `definer` when adversary score ≥ 7).

**Step 9 — Seed the task list.** One TaskCreate per framework, with `addBlockedBy` to express phase dependencies.

**Step 10 — Six Hats burst.** Mid-Phase-3, lead spawns 6 fresh teammates (`hat-white`, `hat-red`, `hat-black`, `hat-yellow`, `hat-green`, `hat-blue`) in a single parallel batch. They each write `frameworks/six-hats-<color>.md`. Shut down individually after.

**Step 11 — Confidence synthesis.** Lead computes 0-10 rubric + Bayesian posterior + HIGH/MED/LOW bucket from the framework outputs.

**Step 12 — Render.** `bin/render-report` assembles `.context/solve-<slug>.md` (pyramid / build-up / tldr — your pick at start).

**Step 13 — Cross-skill handoffs.** If iceberg surfaces a bug-shape, lead auto-invokes `/investigate`. If pre-product, auto-invokes `/office-hours`. End-of-run hand-off to `/plan-eng-review` if architecture decision was produced.

**Step 14 — TeamDelete.** Lead shuts down each teammate via `SendMessage(message={"type":"shutdown_request"})`, then `TeamDelete` cleans up.

**Step 15-16 — Learnings + telemetry.**

## Frameworks

**Phase 1 — Define (8):** abstraction-ladder, first-principles, issue-tree, ishikawa, inversion-define, zwicky-box, conflict-resolution-diagram, productive-thinking.

**Phase 2 — Systems (5):** iceberg, connection-circles, concept-map, balancing-loop, reinforcing-loop.

**Phase 3 — Decide (12):** cynefin, eisenhower, impact-effort, decision-matrix, second-order, ladder-of-inference, ooda-loop, hard-choice, confidence-speed-quality, sbi, six-hats (6 roleplays), minto.

Each framework spec lives in `frameworks/<name>.md` with: entry predicate (formal logic), method, output schema (mermaid / table / prose), and a "What This Means For The Decision" hook.

## Parallel.ai key

The installer walks you through this. After install, manage manually:

```bash
# Interactive (recommended) — silent paste prompt
~/.claude/skills/solve/bin/parallel-setup

# One-liner
~/.claude/skills/solve/bin/parallel-setup --key "sk-YOUR_KEY"

# Pipe from a password manager / clipboard
pbpaste | ~/.claude/skills/solve/bin/parallel-setup --stdin
op item get parallel-ai --field credential | ~/.claude/skills/solve/bin/parallel-setup --stdin

# Inspect / validate / remove
~/.claude/skills/solve/bin/parallel-setup --status   # masked preview
~/.claude/skills/solve/bin/parallel-setup --check    # probes the API
~/.claude/skills/solve/bin/parallel-setup --remove
```

Stored at `~/.gstack/parallel-api-key` (mode 0600). The setup script probes the API before storing — if validation fails it asks before saving an unverified key. `/solve` reads `$PARALLEL_API_KEY` first, then falls back to the file.

If no key is configured, `/solve` degrades silently to WebSearch + gstack browse only.

## Resume

If interrupted, re-invoke `/solve` with the same problem; lead asks resume-or-restart. State at `.context/solve/<slug>/state.json`.

> ⚠️ Agent-teams limitation: Claude Code `/resume` and `/rewind` do **not** restore in-process teammates. After Claude session resume, the lead re-spawns teammates from scratch — the on-disk state and partially-written framework files survive, so work is not lost.

## Files

```
.claude/skills/solve/
├── SKILL.md                # main entry, agent-teams orchestrator
├── README.md               # this file
├── install                 # one-shot installer (run once per machine)
├── frameworks/             # 25 framework specs
│   ├── abstraction-ladder.md
│   ├── ...
│   └── minto.md
├── bin/
│   ├── parallel-research   # Parallel.ai fan-out + WebSearch fallback
│   ├── parallel-setup      # interactive Parallel.ai key setup
│   ├── state-rw            # JSON state read/write for resume safety
│   ├── cost-track          # running spend ledger
│   └── render-report       # assembles final markdown
└── templates/
    └── report.md           # base template
```

## Voice

Builder-to-builder. No filler. Names files, frameworks, and commands explicitly.

## Why agent teams (not subagents)

`/solve` does adversarial reasoning: framework outputs need to challenge each other, the adversary needs to flag weakness in real time, and Six Hats roleplays need to disagree. [Subagents](https://code.claude.com/docs/en/sub-agents) only report back to the lead — they can't argue with each other. [Agent teams](https://code.claude.com/docs/en/agent-teams) share a task list and message peers directly, which is the right primitive for "investigate with competing hypotheses." That's why this skill uses teams exclusively.
