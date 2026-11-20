
## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues, managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout: one root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.

### Working in this repo

- The router is in `SKILL.md` and `references/router.md`. It picks decide, make, write, or answer.
- `html/` is html-artifact, fetched by `bin/html-sync`. It has no license file. Never commit it.
- `skills/` is what `npx skills add bajpainaman/solve` installs.
  - `skills/skill-router` is generated from `plugin/router/HEADER.md` and the vendored skills by `bin/build-plugin --tree`. Edit the header, not the output.
  - `skills/solve` is generated: run `bin/build-plugin --tree` after changing solve. A test fails when it is stale.
  - `skills/cdpi` is vendored from bajpainaman/cdpi at the pin in `sources.json`.
  - `skills/impeccable` (Apache-2.0) and `skills/{testing-toolkit,fv-toolkit,sdlc-toolkit,pr-review}` (MIT) are copied by `bin/vendor-sync <id>` at the pins in `sources.json`. Never edit them by hand. A toolkit's entry `SKILL.md` comes from `plugin/wrappers/<id>/`. `bin/vendor-sync` renames every nested upstream `SKILL.md` to `SKILL.upstream.md`, because Amp registers any nested `SKILL.md` as its own skill. Only the 8 entry skills may have a `SKILL.md`.
  - Before bumping a vendored pin, run `bin/vendor-sync <id> --review <ref>` and read every flagged file.
- `plugin/ROUTING.md` sends every plugin request to `skills/skill-router`.
- `sources.json` pins every upstream source. `bin/check-updates --force` compares them with upstream.
- Validate with `python3 -m unittest discover -s tests` and `tests/test_port.sh`.
- Decisions that change the architecture go in `docs/adr/`.
