# Contributing to solve

The product guarantee is checkable evidence, appropriate restraint, and independent
verification. Framework count and report length are not success metrics.

## Changing the contract

- Keep the gate-state vocabulary exactly FIRED, N/A, BLOCKED.
- FIRED means executed, not passed. Preserve failed outcomes and replaced receipts.
- N/A must cite the catalog's exact trigger and supported false applicability.
- Unknown facts, unavailable consumers, stale inputs, and missing evidence remain BLOCKED.
- Refutation starts blind. Consumer review binds the actual delivered report.
- Cover omitted material claims as well as claims the builder listed.
- Do not add confidence points for votes, framework completion, or tier choice.

Use lib/solve_contract.py as the shared validator for every consumer. Do not add a
parallel completion check based on filenames or status flags.

## Adding a method

Add an observable trigger to gates/catalog.json and a compact framework card using
frameworks/_TEMPLATE.md. Keep the card below 4 KB. Put optional long explanations
under references/deep; normal runs must not read them wholesale. A method needs
a test case showing when it fires and when it does not apply.

## Validation

```bash
for f in solve install bin/* tests/test_port.sh; do bash -n "$f"; done
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_port.sh
git diff --check
```

Tests use temporary directories, isolated homes, and mocked paid services. Keep
contract tests adversarial: a readable report or a valid JSON shape alone should
not fool completion. Scorer tests may use artificial predictions, but label them
as scorer tests and never publish their scores as model results.

Use benchmark export/run/score for actual evaluation. Record adapter, model,
settings, case digest, and usage provenance. Evaluate against the same corpus and
compare changed-premise pairs; don't score polished prose as correctness.

## Versioning and docs

Bump VERSION and add a changelog entry together. Changes to gate schemas, CLI
contracts, or freshness semantics require a major version. Keep the installer,
skill references, tests, metadata, and architecture decision records synchronized.

Issues live in GitHub; see docs/agents/issue-tracker.md. Domain conventions are in
docs/agents/domain.md. Do not publish issues, PRs, or releases without task authorization.
