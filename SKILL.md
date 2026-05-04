---
name: solve
version: 0.2.0
description: |
  Strategic problem solver. Orchestrates an agent team across 25 untools.co frameworks in
  3 phases (define, systems, decide). Lead spawns long-lived teammates (researcher, definer,
  systems-thinker, decider, adversary) plus 6 just-in-time Six-Hats teammates in Phase 3.
  Layered web research (Parallel.ai → WebSearch → gstack browse). Continuous adversary
  challenges every framework output. Produces .context/solve-<slug>.md with recommendation +
  0-10 rubric + Bayesian posterior + HIGH/MED/LOW bucket + dissent + Minto synthesis. Auto-
  handoffs mid-run to /investigate, /office-hours, /plan-eng-review when triggers fire.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebSearch
  - WebFetch
  - mcp__conductor__AskUserQuestion
  - Skill
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - TeamCreate
  - TeamDelete
  - SendMessage
triggers:
  - solve this problem
  - help me think through
  - work this out
  - strategic problem
  - decision framework
---

# /solve — Strategic Problem Solver (agent-teams edition)

This skill **must** run as an agent-teams orchestrator. The lead session does intake + synthesis
+ rendering. All framework execution and research is delegated to named teammates so phases run
in parallel, peers challenge each other, and Six Hats spawns 6 concurrent role-plays.

---

## Step 0 — Self-check (run first, fail fast)

```bash
_TEL_START=$(date +%s)
_SESSION_ID="$$-$_TEL_START"
mkdir -p ~/.gstack/sessions ~/.gstack/analytics .context/solve
touch ~/.gstack/sessions/"$PPID"

# Hard requirements
_FAILURES=()

# 1. Skill installed globally?
if [ ! -d "$HOME/.claude/skills/solve" ]; then
  _FAILURES+=("/solve not installed at ~/.claude/skills/solve — run the installer:")
  _FAILURES+=("    bash <THIS_DIR>/install")
fi

# 2. Agent teams flag enabled?
_AT_FLAG="${CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS:-}"
if [ -z "$_AT_FLAG" ] || [ "$_AT_FLAG" = "0" ]; then
  if [ -f "$HOME/.claude/settings.json" ] && \
     python3 -c "import json,sys;d=json.load(open('$HOME/.claude/settings.json'));sys.exit(0 if d.get('env',{}).get('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS')=='1' else 1)" 2>/dev/null; then
    echo "AGENT_TEAMS: enabled in settings.json (will apply on next claude restart if not yet active)"
  else
    _FAILURES+=("agent teams not enabled. Run the installer or add to ~/.claude/settings.json:")
    _FAILURES+=('    {"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}}')
  fi
fi

# 3. claude version >= 2.1.32
_CC_VER=$(claude --version 2>/dev/null | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
if [ -n "$_CC_VER" ]; then
  awk -v v="$_CC_VER" 'BEGIN{split(v,a,".");exit !(a[1]>2 || (a[1]==2 && a[2]>1) || (a[1]==2 && a[2]==1 && a[3]>=32))}' \
    || _FAILURES+=("claude $_CC_VER is too old, need >= 2.1.32 for agent teams")
fi

if [ ${#_FAILURES[@]} -gt 0 ]; then
  printf '\n/solve cannot start. Issues:\n'
  printf '  - %s\n' "${_FAILURES[@]}"
  exit 1
fi
echo "SELFCHECK: ok"
```

If self-check fails, **stop**. Do not proceed. Surface the install one-liner to the user.

---

## Step 1 — Preamble (gstack pattern)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
echo "SESSION_ID: $_SESSION_ID"

# Parallel.ai key
_PARALLEL_KEY="${PARALLEL_API_KEY:-}"
[ -z "$_PARALLEL_KEY" ] && [ -f ~/.gstack/parallel-api-key ] && \
  _PARALLEL_KEY=$(tr -d '[:space:]' < ~/.gstack/parallel-api-key 2>/dev/null)
if [ -n "$_PARALLEL_KEY" ]; then
  export PARALLEL_API_KEY="$_PARALLEL_KEY"
  echo "PARALLEL: ready"
else
  echo "PARALLEL: not configured (degrading to WebSearch + browse)"
fi

# gstack browse
_BROWSE_BIN="$HOME/.claude/skills/gstack/browse/dist/browse"
[ -x "$_BROWSE_BIN" ] && echo "BROWSE: ready" || echo "BROWSE: missing"

eval "$(~/.claude/skills/gstack/bin/gstack-slug 2>/dev/null)" 2>/dev/null || SLUG=unknown
~/.claude/skills/gstack/bin/gstack-timeline-log \
  '{"skill":"solve","event":"started","branch":"'"$_BRANCH"'","session":"'"$_SESSION_ID"'"}' \
  2>/dev/null &

export SOLVE_COST_FILE=".context/solve/.cost-$_SESSION_ID"
echo "0" > "$SOLVE_COST_FILE"
```

---

## Step 2 — Resolve Input

The user invokes one of:
- `/solve` (no args) → AskUserQuestion: open with "describe the problem in 1-3 sentences"
- `/solve "<one-liner>"` → use as-is
- `/solve <path>` → if `<path>` exists and is a file, read it as the problem brief

Then:

```bash
SOLVE_SLUG=$(echo "$PROBLEM_RAW" | head -c 60 | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]\+/-/g; s/^-\|-$//g')
RUN_DIR=".context/solve/$SOLVE_SLUG"
REPORT=".context/solve-$SOLVE_SLUG.md"
TEAM_NAME="solve-$SOLVE_SLUG"
mkdir -p "$RUN_DIR/evidence" "$RUN_DIR/frameworks" "$RUN_DIR/diagrams"
```

---

## Step 3 — Resume Detection

```bash
if [ -f "$RUN_DIR/state.json" ]; then echo "PARTIAL_RUN: yes"; else echo "PARTIAL_RUN: no"; fi
```

If `PARTIAL_RUN: yes`, AskUserQuestion: resume vs restart. On restart, archive prior to `$RUN_DIR.bak.<ts>`.

`bin/state-rw init "$RUN_DIR" "$SOLVE_SLUG" "$PROBLEM_RAW"` initializes state on fresh runs.

---

## Step 4 — Pre-flight Intake (5 questions)

AskUserQuestion (single batch where possible):

1. **Stakeholders** — single-decider / small-team / multi-stakeholder / org-wide
2. **Time pressure** — now / this-week / this-month / no-deadline
3. **Reversibility** — cheap / costly / one-way-door
4. **Decision-maker** — you-alone / you-with-input / someone-else / unclear
5. **Success criteria** — measurable-metric / qualitative-signal / can't-articulate / TBD

Then free-form: "Refine the problem statement in your own words (this becomes canonical)."

Persist to `$RUN_DIR/intake.json` via `bin/state-rw write "$RUN_DIR" intake '<json>'`.

**Domain auto-detect** from problem text:
- contains "contract|API|deploy|audit|gas" → DOMAIN=eng
- contains "users|feature|ship|MVP|PMF|GTM" → DOMAIN=product
- contains "career|company|should I" → DOMAIN=strategy
- else DOMAIN=general

---

## Step 5 — Output Format Pick

AskUserQuestion: pyramid / build-up / tldr. Persist to state.

---

## Step 6 — Create the Team

**Use TeamCreate to bootstrap the agent team.** This is the **exclusive** orchestration backbone.

```text
TeamCreate(team_name="$TEAM_NAME", description="Solve: $PROBLEM_REFINED")
```

The team file lives at `~/.claude/teams/$TEAM_NAME/config.json`. The shared task list lives at `~/.claude/tasks/$TEAM_NAME/`.

---

## Step 7 — Spawn Long-Lived Teammates (5)

Use the Agent tool with `team_name="$TEAM_NAME"` and a `name` (so peers can address them by name) for each role.

| Name             | subagent_type     | Role |
|------------------|-------------------|------|
| `researcher`     | `general-purpose` | Layered web research; populates `$RUN_DIR/evidence/` |
| `definer`        | `general-purpose` | Phase 1 — runs the 8 Define frameworks |
| `systems-thinker`| `architect`       | Phase 2 — runs the 5 Systems frameworks |
| `decider`        | `general-purpose` | Phase 3 — runs the 12 Decide frameworks (excluding Six Hats fan-out) |
| `adversary`      | `critic`          | Continuous devil's-advocate; reads every framework output, writes attacks to `$RUN_DIR/adversary.jsonl` |

**Spawn each with a self-contained brief.** Briefs include:
- The skill root (`~/.claude/skills/solve/`) so they can read framework specs
- The run directory (`$RUN_DIR`) so they know where to write
- The problem statement (`$PROBLEM_REFINED`) and intake JSON
- Their phase + framework list
- The communication protocol (see Step 8)

### Researcher brief (template)
```
You are `researcher` in team $TEAM_NAME for /solve.
Skill root: ~/.claude/skills/solve
Run dir: $RUN_DIR
Problem: $PROBLEM_REFINED
Intake: $RUN_DIR/intake.json

Your job: layered parallel web research. For each task you claim from the shared list:
  1. Read the task description (it names the framework or sub-question).
  2. Compose 3-7 parallel research queries.
  3. Use $HOME/.claude/skills/solve/bin/parallel-research to fan out.
     If PARALLEL_API_KEY is set, it uses Parallel.ai. Otherwise it returns
     fallback objects telling YOU to run WebSearch.
  4. For top-N candidate sources, run gstack browse for full-page extraction.
  5. Write evidence to $RUN_DIR/evidence/<task-id>.md (markdown summary +
     bullets + source URLs).
  6. SendMessage to the framework owner (definer / systems-thinker / decider)
     when their evidence is ready.
  7. TaskUpdate completed.

Cost discipline: increment $SOLVE_COST_FILE for each external API call.
If running total exceeds $5, SendMessage to lead asking for green-light.
```

### Definer brief
```
You are `definer` in team $TEAM_NAME.
Phase 1 (Define) frameworks — run these in this dependency-respecting order:

  Wave 1B (no deps): abstraction-ladder, first-principles, issue-tree,
                     ishikawa, inversion-define
  Wave 1C (deps on 1B): zwicky-box (request 1 sub-fan from researcher per axis),
                        conflict-resolution-diagram (only if intake.stakeholders
                        != "single-decider"),
                        productive-thinking

For each framework:
  1. Read $HOME/.claude/skills/solve/frameworks/<name>.md (spec + method).
  2. Apply the method to the problem. Use evidence from $RUN_DIR/evidence/.
  3. Write the framework output to $RUN_DIR/frameworks/<name>.md following
     that framework's Output Schema (mermaid diagrams, tables, prose).
  4. End with the "What This Means For The Decision" hook.
  5. TaskUpdate completed.

If you need research evidence: SendMessage to `researcher` describing the
sub-question. Wait for their reply before proceeding.

If `adversary` flags a weakness in your output: read $RUN_DIR/adversary.jsonl,
revise the framework file, and SendMessage to `adversary` for re-check.
```

### Systems-thinker brief
```
You are `systems-thinker` in team $TEAM_NAME.
Phase 2 (Systems) frameworks, in order:
  iceberg, connection-circles, concept-map,
  balancing-loop (only if connection-circles found a balancing cycle),
  reinforcing-loop (only if connection-circles found a reinforcing cycle).

Inputs: all of $RUN_DIR/frameworks/* from Phase 1 and $RUN_DIR/evidence/*.
Output: write each to $RUN_DIR/frameworks/<name>.md with mermaid diagrams.

CRITICAL TRIGGERS (SendMessage to lead immediately if these fire):
  - iceberg's "structures" layer reveals a bug-shape (named system component
    failing reliably) → tell lead to invoke /investigate
  - iceberg's "mental models" layer reveals pre-product / no-PMF uncertainty
    → tell lead to invoke /office-hours
  - structures layer reveals an explicit architecture decision → mark
    "PLAN_ENG_REVIEW_AT_END=true" in $RUN_DIR/state.json
```

### Decider brief
```
You are `decider` in team $TEAM_NAME.
Phase 3 (Decide) frameworks, in this order:
  cynefin (FIRST — its result routes the rest),
  eisenhower, impact-effort, decision-matrix, second-order,
  ladder-of-inference, ooda-loop,
  hard-choice (only if intake.reversibility = one-way-door OR
               top 2 decision-matrix options within 5%),
  confidence-speed-quality, sbi (only if interpersonal signals).

Six Hats is handled separately: when you reach that step, SendMessage to
lead to spawn the 6 hat-teammates. They write their files. You synthesize
after they idle.

Minto runs LAST and consumes everything. Output schema is strict — see
$HOME/.claude/skills/solve/frameworks/minto.md.

When all 12 frameworks complete, SendMessage to lead with a single line:
  "decider: phase 3 complete, ready for synthesis"
```

### Adversary brief
```
You are `adversary` in team $TEAM_NAME.
Long-lived watcher. Your job is continuous devil's-advocate.

Watch $RUN_DIR/frameworks/. For every new file:
  1. Read it.
  2. List the strongest 3 ways its conclusion could be wrong.
  3. Identify hidden assumptions that, if false, invalidate it.
  4. Score adversarial confidence 0-10 (10 = "I can break this easily").
  5. Append one JSON line per framework to $RUN_DIR/adversary.jsonl:
       {"framework":"<name>","attacks":[...],"assumptions":[...],"score":N,"ts":"..."}
  6. If score >= 7: SendMessage to the framework owner asking for revision.

Do not interrupt other teammates' work. React when files appear.
Continue until lead sends `{"type":"shutdown_request"}`.
```

---

## Step 8 — Communication Protocol

The team uses these patterns:

- **Lead → teammate**: TaskUpdate with `owner: <name>` to assign work. Then SendMessage with the briefing details.
- **Teammate → lead**: idle notifications are automatic. SendMessage with `to: "<lead-name>"` only for blockers, trigger fires, or cost-cap requests.
- **Peer → peer**: SendMessage by name (e.g. `definer` → `researcher` for a sub-question).
- **Adversary → owner**: SendMessage when a framework's adversarial score ≥ 7.

All teammates **must** mark tasks `completed` via TaskUpdate when done. Otherwise dependent tasks can't unblock.

---

## Step 9 — Populate the Shared Task List

Use TaskCreate to seed the work. One task per framework, plus per-axis tasks for Zwicky and per-hat tasks for Six Hats (created in Phase 3). Use `addBlockedBy` to express dependencies.

Create in groups (lead does this once teammates are spawned):

```text
Phase 1 tasks (assign owner=definer):
  T-define-abstraction-ladder, T-define-first-principles, T-define-issue-tree,
  T-define-ishikawa, T-define-inversion, T-define-zwicky-box,
  T-define-conflict-res, T-define-productive-thinking

Phase 1 research tasks (assign owner=researcher, blocks the framework tasks
that need its evidence):
  T-research-define-prior-art, T-research-define-failure-modes
  (extra T-research-zwicky-axis-N spawned as definer requests)

Phase 2 tasks (assign owner=systems-thinker, blockedBy phase-1 group):
  T-systems-iceberg, T-systems-connection-circles, T-systems-concept-map
  (T-systems-balancing-loop and T-systems-reinforcing-loop are conditional
  and created mid-run by systems-thinker if cycles surface)

Phase 2 research tasks (assign owner=researcher):
  T-research-systems-analogous, T-research-systems-failure-modes-prior

Phase 3 tasks (assign owner=decider, blockedBy phase-2 group):
  T-decide-cynefin (must complete first within phase 3), T-decide-eisenhower,
  T-decide-impact-effort, T-decide-decision-matrix, T-decide-second-order,
  T-decide-ladder-of-inference, T-decide-ooda, T-decide-hard-choice,
  T-decide-confidence-speed-quality, T-decide-sbi, T-decide-minto

Phase 3 research tasks (assign owner=researcher):
  T-research-decide-base-rates, T-research-decide-prior-art

Continuous task (no owner — adversary self-claims):
  T-adversary-monitor (no completion target; lead marks it complete on
  shutdown)
```

---

## Step 10 — Six Hats Spawn (Phase 3 mid-flight)

When `decider` reaches the Six Hats step it sends the lead a message. The lead spawns 6 fresh teammates **in parallel** (one Agent call per hat in a single message, all with the same `team_name`):

| Name              | subagent_type   | Hat & focus |
|-------------------|-----------------|-------------|
| `hat-white`       | general-purpose | Facts only, verifiable evidence |
| `hat-red`         | general-purpose | Gut, intuition, emotion |
| `hat-black`       | critic          | Risks, failure modes, devil's advocate |
| `hat-yellow`      | general-purpose | Justified optimism, upside |
| `hat-green`       | general-purpose | Lateral, alternative recommendations |
| `hat-blue`        | architect       | Process meta, what's missing |

Each gets the same brief plus their hat role from `frameworks/six-hats.md`. They each write `$RUN_DIR/frameworks/six-hats-<color>.md` and idle.

Once all 6 idle, the lead synthesizes (or asks `decider` to). Then SendMessage shutdown to each hat teammate, individually.

---

## Step 11 — Confidence Synthesis (lead, no team needed)

Compute three confidence views. Inputs come from the framework files written by teammates.

1. **Rubric (0-10)** — additive scoring:
   - +2 if Cynefin domain ∈ {simple, complicated}
   - +2 if decision-matrix top option ≥ 1.5× second
   - +2 if Six Hats ≥ 4 hats agree
   - +2 if adversary max score ≤ 4 (hard-to-break)
   - +2 if second-order surfaces no catastrophic downside

2. **Bayesian posterior** — `P(decision correct | evidence)`:
   - Prior from research base rates
   - Likelihood from framework agreement
   - Posterior = Prior × Likelihood / Normalize

3. **Bucket**:
   - HIGH = rubric ≥ 8 AND posterior ≥ 0.75
   - MEDIUM = rubric 5-7 OR posterior 0.55-0.75
   - LOW = otherwise

Persist via `bin/state-rw write "$RUN_DIR" confidence '<json>'`.

---

## Step 12 — Render Report

```bash
~/.claude/skills/solve/bin/render-report \
  --slug "$SOLVE_SLUG" \
  --format "$FORMAT" \
  --run-dir "$RUN_DIR" \
  --output "$REPORT"
open "$REPORT" 2>/dev/null || true
```

Sections (per format):
- Header (problem, slug, date, intake)
- Decision (one-paragraph recommendation)
- Confidence (rubric breakdown + Bayesian + bucket)
- Dissent (top adversary attacks)
- Synthesis (Minto pyramid)
- Phase 1: Define
- Phase 2: Systems
- Phase 3: Decide
- Handoffs Performed (if any mid-run)
- Appendix (raw evidence, queries fired, costs, learnings)

---

## Step 13 — Cross-Skill Handoffs

If any of these triggers fired during the run, the lead invokes the corresponding skill via the Skill tool **after** report renders, with the report path as context:

- `iceberg.structures = bug-shape` → `Skill(skill="investigate", args=...)`
- `iceberg.mental_models = pre-product` → `Skill(skill="office-hours", args=...)`
- `state.PLAN_ENG_REVIEW_AT_END = true` → `Skill(skill="plan-eng-review", args=...)`

Log every handoff to `$RUN_DIR/handoffs.jsonl`.

---

## Step 14 — Shutdown Team

```text
SendMessage(to="researcher", message={"type":"shutdown_request"})
SendMessage(to="definer", ...)
SendMessage(to="systems-thinker", ...)
SendMessage(to="decider", ...)
SendMessage(to="adversary", ...)
# any leftover hat teammates if not already shut down
```

After all idle, **TeamDelete** to clean up team config + task list. The lead must do this, never a teammate.

---

## Step 15 — Learnings Extraction

```bash
~/.claude/skills/gstack/bin/gstack-learnings-log '{
  "skill":"solve","type":"insight","key":"<short>",
  "insight":"<observed>","confidence":N,"source":"observed","slug":"'"$SOLVE_SLUG"'"
}'
```

0-5 learnings per run. Look for: under-weighted dimensions, recurring Cynefin classifications, frameworks that consistently surface tension.

---

## Step 16 — Cost + Telemetry (run last)

```bash
_COST=$(cat "$SOLVE_COST_FILE" 2>/dev/null || echo "0")
echo "Total API spend this run: \$$_COST"

_TEL_END=$(date +%s)
_TEL_DUR=$(( _TEL_END - _TEL_START ))
~/.claude/skills/gstack/bin/gstack-timeline-log '{
  "skill":"solve","event":"completed",
  "branch":"'$(git branch --show-current 2>/dev/null || echo unknown)'",
  "outcome":"success","duration_s":"'"$_TEL_DUR"'",
  "session":"'"$_SESSION_ID"'","slug":"'"$SOLVE_SLUG"'","cost_usd":"'"$_COST"'"
}' 2>/dev/null || true
echo '{"skill":"solve","duration_s":"'"$_TEL_DUR"'","outcome":"success","session":"'"$_SESSION_ID"'","cost_usd":"'"$_COST"'","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true
```

---

## Voice

Builder-to-builder. No filler. Name files, frameworks, commands explicitly.
No em dashes. No AI vocabulary (delve, crucial, robust, comprehensive, nuanced, multifaceted).
Every framework section ends with "What This Means For The Decision."

## Completion Status Protocol

- **DONE** — all 25 frameworks ran, report rendered, team cleaned up.
- **DONE_WITH_CONCERNS** — completed but adversary max score ≥ 7.
- **BLOCKED** — research stack failed AND no fallback worked.
- **NEEDS_CONTEXT** — pre-flight intake revealed problem isn't well-defined.

## Limitations of agent-teams mode

- Experimental. Session resumption (`/resume`, `/rewind`) does NOT restore in-process teammates. After resume, lead must re-spawn fresh teammates (state on disk survives).
- One team per session. If a previous /solve team is still alive, ask user before TeamDelete.
- Token cost scales linearly with active teammates. The 5+6 = 11 teammates during Six Hats burst is intentional but expensive.
- No nested teams: teammates cannot spawn their own teammates. Only the lead spawns hat-* during Phase 3.

## Helpers

- `bin/parallel-research <queries.json> <out-dir>` — Parallel.ai fan-out, falls back to WebSearch instructions
- `bin/parallel-setup` — interactive paste-friendly Parallel.ai key setup
- `bin/state-rw read|write|init <run-dir> <key> [value]` — JSON state for resume safety
- `bin/cost-track <usd>` — increments `$SOLVE_COST_FILE`
- `bin/render-report` — assembles final markdown
- `install` — one-shot installer (run once per machine)
