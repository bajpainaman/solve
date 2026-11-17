
## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues, managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout: one root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.

### Working in this repo

- The router is in `SKILL.md` and `references/router.md`. It picks decide, make, write, or answer.
- `html/` is html-artifact, fetched by `bin/html-sync`. It has no license file. Never commit it.
- `skills/` is what `npx skills add https://github.com/bajpainaman/solve/tree/main/skills` installs.
  - `skills/solve` is generated: run `bin/build-plugin --tree` after changing solve. A test fails when it is stale.
  - `skills/cdpi` is vendored from bajpainaman/cdpi at the pin in `sources.json`.
  - `skills/impeccable` (Apache-2.0) is fetched by `bin/impeccable-sync` at its pin. Never edit it by hand.
- `plugin/ROUTING.md` picks solve, cdpi or impeccable for every plugin request.
- `sources.json` pins every upstream source. `bin/check-updates --force` compares them with upstream.
- Validate with `python3 -m unittest discover -s tests` and `tests/test_port.sh`.
- Decisions that change the architecture go in `docs/adr/`.
