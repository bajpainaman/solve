
## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues, managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout: one root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.

### Working in this repo

- The router is in `SKILL.md` and `references/router.md`. It picks decide, make, write, or answer.
- `html/` is html-artifact, fetched by `bin/html-sync`. It has no license file. Never commit it.
- `sources.json` pins every upstream source. `bin/check-updates --force` compares them with upstream.
- Validate with `python3 -m unittest discover -s tests` and `tests/test_port.sh`.
- Decisions that change the architecture go in `docs/adr/`.
