# solve

One skill for decisions, clear writing, and reviewable HTML pages.

`solve` routes each request before it does any work. A decision gets checked
claims, a blind refuter, and a consumer review. A page gets one of 32 templates
and a headless-browser check. All prose follows controlled English. Run it as
`$solve` in Codex, `/solve` in Claude Code, or `solve "..."` from a shell.

## Modes

| Mode | For | Result |
|---|---|---|
| decide | Choices with stakes: "should we", build or buy, go or no-go | A gated decision run and a verified decision-memo page |
| make | Pages people review or use | One of 32 templates: PR reviews, plans, postmortems, explainers, decks, prototypes, editors, blindspot passes |
| write | Rewrite, audit, or lint prose | Built-in simplify-writing: ASD-STE100 rules with Vale and Harper |
| answer | Short questions | An inline reply |

Bugs go to an investigate skill, and unvalidated product ideas go to
office-hours. The [router](references/router.md) holds the full tables. It
chooses the mode, then Markdown or HTML, then the template. The write layer
applies to all prose in every mode.

```bash
solve "should we migrate the service to Postgres?"     # decide
bin/templates match "write up last night's outage"     # make: pick a template
bin/prose-check --file docs/rfc.md                     # write: lint any file
bin/check-updates                                      # compare pins with upstream
```

## Quick start

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/bajpainaman/solve/main/install)
solve --status
```

From a clone:

```bash
./install
```

The installer links the skill at `~/.agents/skills/solve`, installs the launcher
at `~/.local/bin/solve`, and runs `bin/html-sync` to fill the built-in HTML mode.
It keeps backups of existing installations and does not change Codex settings.
For Claude Code, link the clone: `ln -sfn "$PWD" ~/.claude/skills/solve`.

| Need | For |
|---|---|
| Python 3 and Git | Everything |
| Codex CLI with fresh subagents, or Claude Code | Decide mode's refuter and consumer reviewers |
| Node 22 or later | Building HTML pages |
| Google Chrome | The headless page check |
| `vale` and `harper-cli` (`brew install vale harper`) | Prose lint. Without them, the lint prints `SKIPPED` |
| Parallel.ai key | Optional paid research breadth |

## Decide mode

Quick, Standard, and Deep set time, external research spend, and evidence
depth. They never set a framework count.

| Tier | Default time | External spend | Evidence depth |
|---|---:|---:|---|
| Quick | 15 minutes | $2 | Focused |
| Standard | 30 minutes | $5 | Cross-check |
| Deep | 60 minutes | $15 | Replicate |

Every tier needs evidence, independent refutation, and consumer verification.
At 80% of a budget, solve starts no optional work. At 100%, it keeps finished
work and produces an unverified draft with unfinished checks BLOCKED.
`time=unlimited spend=unlimited` removes the caps. The legacy `tokens=` spelling
means external API spend, not model usage.

Each gate has exactly three legal states:

| State | Required evidence |
|---|---|
| FIRED | A hashed artifact and checks that name the surface, expected result, observed result, and outcome |
| N/A | The gate's exact written trigger, a supported false evaluation, and its evidence |
| BLOCKED | The obstruction and what remains unverified |

FIRED does not mean passed. Missing or stale evidence becomes BLOCKED. A
non-empty Markdown file cannot establish completion.

1. Keep the original request and user constraints.
2. Write the critical claims in plain language, with observable acceptance
   conditions. Lint them with `bin/prose-check --scope claims`.
3. Evaluate the trigger catalog. Load only the method cards that apply.
4. Check claims against evidence.
5. Record the recommendation and next action, and lint them. A fresh refuter
   frames the problem blind, then tries to disprove them.
6. Render the report and its decision-memo page with `render-report --html`.
7. A second fresh reviewer checks the report and the page, follows the evidence,
   and names material claims missing from the ledger.
8. `bin/gates finalize` binds completion to the exact bytes of both files.

An edit to the report or the page after review invalidates completion.

```bash
solve "should we migrate the service?"
solve docs/decision-brief.md
solve --tier quick --budget time=15min spend=2 "a reversible decision"
solve --tier deep "a consequential decision"
solve progress --plain
```

## Make mode

`bin/templates match "<request>"` ranks the catalog and prints the renderer,
the exemplar, and the type file for the best fits.

| Family | Templates |
|---|---|
| decide | decision-memo |
| explore | code-approaches, visual-directions, implementation-plan |
| code | pr-review, pr-writeup, module-map |
| design | design-system, component-variants |
| prototype | animation-sandbox, clickable-flow |
| diagram | flowchart, svg-figures |
| communicate | slide-deck, status-report, incident-report, pitch-doc |
| research | feature-explainer, concept-explainer, teach-unknowns, reference-port |
| editor | triage-board, feature-flags, prompt-tuner |
| unknowns | blindspot-pass, interview, tweakable-plan, brainstorm, design-directions, mock-first, implementation-notes, change-quiz |

There are two renderers:

- **artifact** pages use the built-in HTML components. Write `<name>.src.html`,
  then `node html/scripts/build.mjs <name>.src.html --verify` adds the theme,
  dark mode, phone layout, and a review kit with comments and Send to Claude.
- **bespoke** pages need interaction that the components do not have, such as
  a prompt tuner or a quiz. Write one self-contained page modeled on the
  exemplar, then run `node html/scripts/verify.mjs <page>.html`.

The check fails a page for console errors, external requests, no dark mode,
overflow at 400px, text under 12px, or credential-shaped strings. The exemplars
are for structure. Their names and data are fictional, and they lack dark mode.

## Write mode

[write/WRITE.md](write/WRITE.md) is a built-in copy of
[simplify-writing](https://github.com/bajpainaman/simplify-writing). It
rewrites, audits, or lints prose with ASD-STE100 rules, Williams style, and an
AI-prose overlay. It never changes code, identifiers, commands, URLs, numbers,
modal verbs, or uncertainty.

```bash
bin/prose-check --file README.md                        # any Markdown, text, or HTML file
bin/prose-check --run-dir .context/solve/x --scope all  # a decision's claims and recommendation
```

The first run downloads the pinned Vale packages. Findings are advisory.

## Built-in sources and updates

| Source | Directory | How it gets there | License |
|---|---|---|---|
| [simplify-writing](https://github.com/bajpainaman/simplify-writing) | `write/` | Committed | MIT |
| [html-effectiveness](https://github.com/ThariqS/html-effectiveness) | `templates/html-effectiveness/` | Committed, unchanged | Apache-2.0 |
| [html-artifact](https://github.com/aasimsani/html-artifact) | `html/` | Fetched by `bin/html-sync` at a pinned commit | None published |

html-artifact has no license file, so this repository never commits it.
`.gitignore` keeps `html/` out, and the installer fetches it on your machine.

`sources.json` pins each source to a full commit. `bin/check-updates` compares
solve and each pin with upstream and prints the action for each update. The
skill runs it once per session from a one-day cache. It reports and never
applies. An unreachable repository shows as UNKNOWN, never as current. Set
`SOLVE_NO_UPDATE_CHECK=1` to turn it off.

To take an update, review the printed compare link, set the new ref in
`sources.json`, and copy the change in. For html-artifact, run `bin/html-sync`.

## Files and commands

```text
SKILL.md                         router and decide-mode contract
references/router.md             mode, format, template, and write-layer tables
references/output.md             prose lint and decision-memo page binding
templates/catalog.json           32 templates with triggers and renderers
templates/html-effectiveness/    exemplar pages (Apache-2.0)
write/                           built-in simplify-writing (MIT)
html/                            built-in html-artifact, fetched and never committed
sources.json                     pinned upstream commits
gates/catalog.json               decide-mode gates and triggers
frameworks/                      25 compact method cards
```

A decision run writes:

```text
.context/solve-<slug>.md                 delivered report
.context/solve-<slug>.html               decision-memo page
.context/solve/<slug>/request.md         original request
.context/solve/<slug>/claims.json        claims and consumer acceptance conditions
.context/solve/<slug>/facts.json         applicability observations
.context/solve/<slug>/gates/*.json       validated three-state receipts
.context/solve/<slug>/evidence/*         captured observations
.context/solve/<slug>/reviews/*          fresh-review inputs and results
.context/solve/<slug>/prose/*            advisory prose-lint findings
.context/solve/<slug>/completion.json    binding to the reviewed report and page
```

| Command | Does |
|---|---|
| `bin/templates list\|show\|match` | Find a page template |
| `bin/prose-check` | Lint prose |
| `bin/html-sync` | Fetch html-artifact at the pinned commit |
| `bin/check-updates` | Compare solve and pins with upstream |
| `bin/gates catalog\|inspect\|record\|validate\|finalize` | Decide-mode gate contract |
| `bin/render-report --html` | Render a decision report and its page |
| `bin/progress --plain` | Show a decision run's gate counts |

The full record schema is in [runtime](references/runtime.md). Reviewer briefs
and disclosure order are in [roles](references/roles.md).
[Confidence](references/confidence.md) explains how to report uncertainty.
Architecture decisions are in [docs/adr/](docs/adr/).

## Research

Use current primary sources for facts that can change. A researcher handles
named evidence gaps, not the whole framework library. Parallel.ai is an optional
breadth provider through `bin/parallel-research`. Without it, solve uses the
host's web tools. Configure it with `bin/parallel-setup`. Set its rate with
`SOLVE_PARALLEL_COST_PER_RUN`.

## Evaluation

[benchmarks/](benchmarks/README.md) holds synthetic cases, relevance judgments,
planted false claims, unknown evidence, and changed-premise pairs. The scorer
measures retrieval, gate decisions, refutation, abstention, and decision
changes. It reports usage only when an actual run supplies it.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_port.sh
bin/benchmark export --output /tmp/solve-cases.jsonl
bin/benchmark score --predictions /path/to/predictions.jsonl
```

Contract and scorer tests are not evidence of model decision quality. This
release claims no live-model accuracy, latency, token savings, or real-world
success rate.

## Compatibility and limits

Pre-2.0 runs stay readable but unverified. solve never promotes them from file
counts to gate receipts. Start a new run to use the current contract.

The validator enforces receipts, coverage declarations, input freshness, and
review metadata. It cannot prove that an agent told the truth. The orchestrator
must use fresh contexts, and reviewers must make the observations they record.
The prose lint is pattern-based. It cannot certify ASD-STE100 compliance.

The full pre-2.0 framework explanations remain under
[references/deep/](references/deep/README.md). Normal runs use the compact
[framework cards](frameworks/) and the [trigger catalog](gates/catalog.json).

MIT. See [LICENSE](LICENSE), [CONTRIBUTING.md](CONTRIBUTING.md), and
[CHANGELOG.md](CHANGELOG.md). Built-in sources keep their own licenses.
