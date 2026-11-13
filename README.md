# solve

Strategic decisions with checkable evidence, independent refutation, and explicit uncertainty.

`solve "your decision"` launches the `$solve` Codex skill. It identifies the claims
that determine the choice, uses analysis only where needed, and checks the actual
result before declaring completion.

## Modes

solve routes each request before it does any work.

| Mode | For | Result |
|---|---|---|
| decide | Choices with stakes | A gated decision run and a verified decision-memo page |
| make | Pages people review or use | One of 32 templates: PR reviews, plans, postmortems, explainers, decks, prototypes, editors, blindspot passes |
| write | Rewrite, audit or lint prose | Built-in simplify-writing (ASD-STE100, Vale and Harper) |
| answer | Short questions | An inline reply |

The write layer applies to all prose in every mode. See the [router](references/router.md).
The make-mode exemplars come from [html-effectiveness](https://github.com/ThariqS/html-effectiveness)
(Apache-2.0). Component pages build with the built-in HTML mode in `html/`. The
installer fills it with `bin/html-sync`, which fetches
[html-artifact](https://github.com/aasimsani/html-artifact) at a pinned commit.
html-artifact has no license file, so this repository never commits that copy.

```bash
bin/check-updates                   # solve and pinned sources vs upstream
bin/html-sync                       # once, or after a pin bump
bin/templates match "write up the outage"
bin/prose-check --file docs/rfc.md
```

## What changed in 2.0

Quick, Standard, and Deep control time, external research spend, and evidence depth.
They no longer promise 8, 16, or 25 frameworks. The 25 methods remain available as
compact cards, with longer references opened only to answer a named question.

Each gate has exactly three legal states:

| State | Required evidence |
|---|---|
| FIRED | A hashed artifact and checks naming the surface, expected result, observed result, and outcome |
| N/A | The gate's exact written trigger, a supported false evaluation, and its evidence |
| BLOCKED | The obstruction and what remains unverified |

FIRED does not mean passed. A refuter disproving a claim has performed its check.
Missing or stale evidence becomes BLOCKED. A non-empty Markdown file cannot
establish completion.

## Workflow

1. Preserve the original request and user constraints.
2. Identify critical claims and their observable acceptance conditions.
3. Evaluate the small trigger catalog. Load only applicable method cards.
4. Check claims against evidence.
5. Run a fresh refuter that independently frames the problem before seeing the
   builder's claims and recommendation. It never receives builder rationale.
6. Render the report, with an optional HTML view, and give it to another fresh
   reviewer.
7. The consumer checks the actual report, follows evidence, exercises declared
   surfaces, and identifies material claims missing from the ledger.
8. Finalize only when current receipts justify completion.

For a page-removal claim, checking the filesystem is insufficient: the reviewer
must query the reader or serving interface. For a future outcome, verification
establishes the forecast's assumptions and limits, not that the future happened.

## Installation

Requirements: Codex CLI with fresh subagent support, Python 3, and Git for remote
installation. Parallel.ai and gstack integrations are optional.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/bajpainaman/solve/main/install)
```

From a clone:

```bash
./install
solve --status
```

The installer links the skill at `~/.agents/skills/solve` and installs the launcher
at `~/.local/bin/solve`. It preserves existing installations with backups and
does not modify Codex configuration. Restart Codex if a new skill is not yet listed.

```bash
solve "should we migrate the service?"
solve docs/decision-brief.md
solve --tier quick --budget time=15min spend=2 "a reversible decision"
solve --tier deep "a consequential decision"
solve progress --plain
solve --update
solve --uninstall
```

Inside Codex: `$solve should we migrate the service?`

## Tiers

| Tier | Default time | External spend | Evidence depth |
|---|---:|---:|---|
| Quick | 15 minutes | $2 | Focused |
| Standard | 30 minutes | $5 | Cross-check |
| Deep | 60 minutes | $15 | Replicate |

Every tier requires evidence, independent refutation, and consumer verification.
An applicable method cannot be waived to meet a budget. At 80%, stop starting
optional work. At 100%, preserve finished work and produce an unverified draft
with unfinished checks BLOCKED.

`time=unlimited spend=unlimited` removes solve's caps. The legacy `tokens=`
spelling means external API spend. It does not measure or cap Codex model usage.

## Files and commands

```text
.context/solve-<slug>.md                 delivered report
.context/solve-<slug>.html               optional decision-memo page (render --html)
.context/solve/<slug>/request.md        original request
.context/solve/<slug>/intake.json       user constraints
.context/solve/<slug>/claims.json       claims and consumer acceptance conditions
.context/solve/<slug>/facts.json        applicability observations
.context/solve/<slug>/gates/*.json      validated three-state receipts
.context/solve/<slug>/frameworks/*.md   applicable methods only
.context/solve/<slug>/evidence/*        captured observations
.context/solve/<slug>/reviews/*         fresh-review inputs and results
.context/solve/<slug>/completion.json   binding to the reviewed report
```

The renderer produces a draft. `bin/gates finalize` binds verified completion to
the report's exact path and bytes, the current decision, and the consumer receipt.
The report stays unchanged after review. Any later edit invalidates completion.

```bash
bin/gates catalog
bin/gates inspect --run-dir .context/solve/example --gate decision-matrix
bin/gates validate --run-dir .context/solve/example
bin/progress --run-dir .context/solve/example --plain
bin/prose-check --run-dir .context/solve/example --scope claims
bin/render-report --run-dir .context/solve/example --slug example \
  --output .context/solve-example.md --html
```

Two optional layers improve what the reader gets. They never replace a gate.
[simplify-writing](https://github.com/bajpainaman/simplify-writing) lints claims
and the decision before they are hashed. [html-artifact](https://github.com/aasimsani/html-artifact)
builds a verified decision-memo page, designed after
[html-effectiveness](https://github.com/ThariqS/html-effectiveness), whose hash
the consumer and completion receipts bind. See [output](references/output.md).

The full record schema and commands are in [runtime](references/runtime.md).
Fresh-context briefs and disclosure order are in [roles](references/roles.md).
[Confidence](references/confidence.md) explains how to report uncertainty without
framework votes. The accepted architecture is in [ADR-0001](docs/adr/0001-adaptive-verification.md).

## Research

Use current primary sources for facts that can change. A researcher handles named
evidence gaps rather than reading the entire framework library. Parallel.ai is an
optional breadth provider through bin/parallel-research; without it, use the host's
web tools. Configure it with bin/parallel-setup. Its rate is configurable through
SOLVE_PARALLEL_COST_PER_RUN; no claim is made that a historical default is today's price.

## Evaluation

[benchmarks/](benchmarks/README.md) contains synthetic cases, relevance judgments
(qrels), planted false claims, unknown evidence, and changed-premise pairs. The
scorer measures retrieval, gate decisions, refutation, abstention, and decision
changes. It reports usage only when supplied by an actual run.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_port.sh
bin/benchmark export --output /tmp/solve-cases.jsonl
bin/benchmark score --predictions /path/to/predictions.jsonl
```

Contract/scorer tests are not evidence of model decision quality. No live-model
accuracy, latency, token savings, or real-world success rate is claimed by this
release. Use the same cases and settings for baseline and candidate runs.

## Compatibility and limits

Pre-2.0 runs remain readable but unverified. They are never silently promoted from
file counts to gate receipts. Preserve the old directory and start a new run to
use the new contract. Historical calibration remains available; its old thresholds
do not determine current confidence.

The validator enforces receipts, coverage declarations, input freshness, and
review protocol metadata. It cannot prove an agent told the truth or enforce
filesystem secrecy. The orchestrator must use fresh non-inherited contexts and
reviewers must perform the recorded observations.

The full pre-2.0 explanations remain under [references/deep/](references/deep/README.md).
Their historical orchestration and confidence rules are superseded. Normal runs
use the compact [framework cards](frameworks/) and [trigger catalog](gates/catalog.json).

MIT. See [LICENSE](LICENSE), [CONTRIBUTING.md](CONTRIBUTING.md), and [CHANGELOG.md](CHANGELOG.md).
