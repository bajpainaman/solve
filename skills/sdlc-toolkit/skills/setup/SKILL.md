---
name: setup
description: One-time setup that prepares a repo, and this machine, for the /sdlc loop. Installs sdlc-stack, which brings in the EGM, pr-review, ponytail, testing-toolkit and fv-toolkit plugins, and sets up CLAUDE.md, one verify command, REVIEW.md and docs/sdlc/. Use when the user runs /sdlc:setup, or when the sdlc skill reports that something is missing.
---

# SDLC setup (once per machine, once per repo)

## Machine

The stages call five other plugins. `sdlc-stack` is a plugin in this marketplace with no skills of its own. Its manifest declares those five as dependencies, so Claude Code installs them, keeps them enabled, and reports any that go missing.

| Plugin | Add its marketplace from | The loop uses it for |
|---|---|---|
| `egm@egm` | `google/elephant-goldfish-model` | The Goldfish review of each document |
| `pr-review@aasimsani-pr-review` | `aasimsani/pr-review` | Code review in a fresh session. The stack needs 1.3.0 or later. |
| `ponytail@ponytail` | `DietrichGebert/ponytail` | The smallest plan and the smallest code |
| `testing-toolkit@testing-toolkit` | `aasimsani/testing-toolkit` | Deciding, writing and auditing the tests. The stack needs 0.1.2 or later. |
| `fv-toolkit@formal-verification-toolkit` | `aasimsani/formal-verification-toolkit` | Formal checks of a design's claims |

1. **Check Claude Code.** Run `claude --version`. EGM needs 2.1.271 or later to isolate its Goldfish reviewers. If the version is older, tell the user to update before using the loop.

2. **Install the stack.** Ask first, then run `claude plugin install sdlc-stack@sdlc-toolkit`. It installs each dependency whose marketplace is already added, and it names the ones it couldn't find.

3. **Add each marketplace that's missing.** `claude plugin marketplace list --json` shows the ones already added. For each row of the table that isn't there, ask first, then run `claude plugin marketplace add <source>`. Adding a marketplace installs that row's plugin, because the stack depends on it.

4. **Confirm the stack.** Run:
   ```bash
   claude plugin list --json | jq -r '.[] | select(.id == "sdlc-stack@sdlc-toolkit") | .errors // [] | .[]'
   ```
   It prints nothing when every dependency is installed, enabled and new enough. Otherwise each line names one dependency and the command that fixes it.

5. **Offer updates.** A dependency installed long ago can be behind its marketplace. Offer `claude plugin update <plugin>` for each row. Another marketplace's plugin of the same name, such as a second `pr-review`, can stay enabled, because the loop finds each plugin by its full id.

6. **Check the tools.** Make sure `gh auth status` passes and `jq` is on `PATH`, because pr-review needs both. Run `java -version` too. The fv-toolkit's checkers need a JDK 17 or later, and without one a formal check reports "not checked".

7. **Restart.** If you installed anything, tell the user to start a new session so the plugins load.

## Repo

1. **CLAUDE.md.** If the repo has no `CLAUDE.md`, generate one with `/init` and trim it. Keep it light. Claude reads the repo itself, so the file holds what the code and the file tree don't show. Make sure it has these parts:
   - One or two lines on what the repo is for.
   - `## Commands` lists build, test, lint, the run command, and one **verify command**, such as `make verify`. It also says what healthy output looks like, for example "ends with `N passed, 0 failed`".
   - `## Things Claude gets wrong` holds the gotchas, which are conventions the code doesn't show and mistakes that keep coming back. It starts empty.
   - Pointers in place of copies. Architecture notes, long conventions and step-by-step procedures live in their own files, directory READMEs or skills. `CLAUDE.md` links to them, so Claude loads each one when a task needs it.

   Don't overwrite an existing `CLAUDE.md`, and don't delete the team's preferences from it. Add what's missing, offer to move long sections into linked files, and show the diff before you write it.

2. **Verify command.** Find an existing command that runs tests, lint and type checks together. If none exists, ask which checks it should run, and add one target, such as a Makefile target or a package script. Run it once and record the result.

3. **REVIEW.md.** pr-review appends this file to every review prompt. If the repo has none, write this template and ask the tech lead to adjust it:

   ```markdown
   # Review rules

   ## What counts as an issue
   1. Bugs: logic errors, unhandled edge cases, broken contracts with callers.
   2. Security: authentication, input validation, secrets, PII handling.
   3. Compliance: anything the team's policies or CLAUDE.md require.
   4. Tests: every new behavior has a test that fails without the change.

   ## What never counts
   - Style and naming taste the formatter or linter doesn't enforce.
   - Generated files and lockfiles.
   ```

4. **Verification skill (optional).** The Test stage's verifier checks a feature by running the app. Offer to write a project skill at `.claude/skills/verify-<app>/`, so the verifier doesn't work out how to launch and drive the app each time. Its `SKILL.md` holds the commands that start the app, check that it's healthy, drive it and clean up. Its `features/` folder holds one short file per feature area, and each file answers four questions: what exists, how a user reaches it, how to drive it with those commands, and what misleads. Start with `SKILL.md` alone. The Test stage adds a feature file as each feature ships.

5. **Directory READMEs (optional).** Offer to run `egm-bootstrap` on the repo root, or on the subtree the team owns, as `${CLAUDE_PLUGIN_ROOT}/references/egm.md` describes. It writes a `README.md` per directory. Goldfish reviewers read those as their baseline, and they're where architecture notes belong. It's a large run, so ask before starting.

6. **Artifact home.** Create `docs/sdlc/README.md` with one line saying that each subfolder holds one feature's artifacts and its `sdlc.yaml`.

7. **Gate hook (opt-in).** The loop has three rules that shouldn't depend on Claude following prose. Nothing commits on the default branch, a human approves and merges each PR, and a stage is approved only when its `tools` are on record. Ask whether the user wants a hook that enforces them. If they say yes:
   - Copy `${CLAUDE_PLUGIN_ROOT}/scripts/sdlc-gate.sh` to `.claude/hooks/sdlc-gate.sh` and make it executable. The copy lives in the repo because the plugin's install path changes with each version. The script needs `jq`.
   - Merge this entry into `.claude/settings.json`, and keep any hooks already there:
     ```json
     {"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/sdlc-gate.sh"}]}]}}
     ```
   - Tell the user what it does. It denies `git commit` on the default branch. It denies a commit that approves a stage while one of the stage's tools has no file and no skip reason in `sdlc.yaml`. It makes Claude Code ask the user before `gh pr merge` or an approving `gh pr review`. In a headless run nobody can answer, so the ask becomes a denial.

   Other guardrails are the team's choice, such as running the formatter after each edit or blocking edits to generated paths. Add them only if the user asks.

8. **Commit.** Show the full diff, get approval, and commit it on a branch as `chore(sdlc): set up repo for the sdlc loop`, or the repo's equivalent.
