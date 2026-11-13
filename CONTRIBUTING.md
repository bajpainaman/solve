# Contributing to solve

solve has four modes: decide, make, write, and answer. The router in SKILL.md and
references/router.md chooses one. Keep each change inside the mode it serves.

The decide-mode guarantee is checkable evidence, appropriate restraint, and
independent verification. Framework count and report length are not success metrics.

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
under references/deep. Normal runs must not read them wholesale. A method needs
a test case showing when it fires and when it does not apply.

## Adding or changing a template

Add an entry to templates/catalog.json with an id, a family, a renderer
(`artifact`, `bespoke`, or `solve`), a one-line shape, and lowercase `use_when`
phrases. An `artifact` entry names an html-artifact type and components. A
`bespoke` entry needs an exemplar file. Add a routing case to
tests/test_solve_templates.py that shows a real request reaching the entry.
Do not edit files under templates/html-effectiveness/. They are upstream copies.

## Built-in sources

sources.json pins every upstream source to a full commit.

- write/ is simplify-writing (MIT). Change it upstream first, then copy the
  change in and update its ref.
- templates/html-effectiveness/ is html-effectiveness (Apache-2.0). Keep it
  unchanged and keep its LICENSE and NOTICE.md.
- html/ is html-artifact. It has no license file, so never commit it, never
  remove its .gitignore entries, and never copy its code into another directory.
  To take an update, set the new ref in sources.json and run `bin/html-sync`.

`bin/check-updates --force` shows which pins are behind upstream.

## Prose and pages

Docs and generated pages follow write/WRITE.md. Run `bin/prose-check --file`
on a doc you change, and fix true findings. Page changes must pass
`node html/scripts/build.mjs <page>.src.html --verify`.

## Validation

```bash
for f in solve install bin/* tests/test_port.sh; do bash -n "$f"; done
bin/html-sync
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_port.sh
git diff --check
```

Tests use temporary directories, isolated homes, local git remotes, and mocked
paid services. No test needs the network. Tests that need Node, Chrome, Vale, or
the fetched html/ directory skip when it is missing. Keep
contract tests adversarial: a readable report or a valid JSON shape alone should
not fool completion. Scorer tests may use artificial predictions, but label them
as scorer tests and never publish their scores as model results.

Use benchmark export/run/score for actual evaluation. Record adapter, model,
settings, case digest, and usage provenance. Evaluate against the same corpus and
compare changed-premise pairs. Do not score polished prose as correctness.

## Versioning and docs

Bump VERSION and add a changelog entry together. Changes to gate schemas, CLI
contracts, or freshness semantics require a major version. Keep the installer,
skill references, tests, metadata, and architecture decision records synchronized.

Issues live in GitHub. See docs/agents/issue-tracker.md. Domain conventions are in
docs/agents/domain.md. Do not publish issues, PRs, or releases without task authorization.
