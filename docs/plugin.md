# Solve plugin

The plugin bundles one router, the existing decision runtime, an original
portable HTML renderer, the 32 artifact patterns, and the writing layer.
It needs no server or separate model API key. It uses the host's model and
available execution, research, browser, and agent capabilities.

## Use

Select **Solve** in ChatGPT or invoke its skill in a compatible client.

- “Help me decide whether to build or buy this. Check the claims and tell me
  what evidence would change the recommendation.”
- “Choose the highest-signal experiment and turn it into a test plan.”
- “Make an incident report from these logs and notes.”
- “Rewrite this without changing the numbers, requirements, or uncertainty.”

Short questions stay short. Consequential decisions load the full evidence,
blind-refutation, and consumer-review workflow. Artifact and writing requests
do not create unnecessary decision ledgers.

## What is included

| Part | Behavior |
|---|---|
| Decisions | Existing 25 framework gates and 3 required gates, with evidence hashes and independent review |
| Artifacts | Self-contained HTML reports from inert JSON; dark mode, phone layout, print styles, tables, and expandable evidence |
| Artifact patterns | 32 catalog entries, including interactive design references; custom interaction requires authoring and host browser checks |
| Writing | Bundled MIT rules and references; optional offline Vale/Harper checks |
| Evaluation | Existing 14-case synthetic benchmark and scorer, plus package/renderer regression tests |
| Provenance | Source commit, runtime version, and SHA-256 for each packaged file |

The 593-word entry point loads mode-specific detail on demand. This measures
entry size, not total conversation tokens or decision performance. The gate
contract is preserved. Missing agents, sources, or execution leave affected
checks blocked rather than being silently treated as complete.

## Build

Build from a Git checkout with Python 3 and PyYAML available:

```bash
bin/build-plugin --output dist/solve-0.1.1.zip
```

The builder validates JSON/YAML and the final archive, checks internal links,
preserves notices, records file hashes, and refuses an existing output path.
It copies tracked shared reference files plus explicitly selected runtime files
and `plugin/overrides/`. Review the source before adding new tracked content.

The archive contains one portable `plugin.json` and one `skills/solve/` tree.
It has no `.app.json`, MCP server, hidden API-key requirement, or bundled
`html-artifact`. Upload it using the supported Plugin Creator account workflow.
Creation is private; workspace or public sharing is a separate action.

## Verify

```bash
python3 -m unittest discover -s tests
tests/test_port.sh
SOLVE_RUN_BROWSER_TESTS=1 python3 -m unittest discover -s tests -p test_portable_artifact.py
```

The last command needs a working Chromium and Playwright installation and must
actually launch the browser. Static checks do not replace it. Missing optional
linters and browsers are reported as skipped or blocked. The conservative
artifact verifier accepts generated report markup; use host browser tooling for
interactive HTML, SVG diagrams, or custom controls.

When the installed Codex cannot run in the test environment, record that failure
and run `env -u CODEX_HOME SOLVE_SKIP_LIVE_CODEX_TEST=1 tests/test_port.sh` for the isolated installer,
launcher, and helper checks. This switch explicitly skips live skill discovery;
it is not a passing live integration result.

Unit tests for receipts use synthetic fixtures. They test the software contract,
not actual independent agent behavior or strategic truth. Successful package
creation establishes installation, not higher decision quality.

## Measure optimization

Compare baseline and plugin with the same model and settings. Use fresh tasks
in addition to the small public corpus. Keep action accuracy, correct abstention,
false N/A, omitted claims, refutation quality, observed latency, and reported
token use separate. Record artifact usability and whether evidence survives
delivery. Do not combine regressions into a flattering aggregate score.

Ship improvements to decision quality only after that comparison supports them.
The package currently improves portability and conditional loading; it makes
no measured claim of superior strategic decisions or lower model cost.
