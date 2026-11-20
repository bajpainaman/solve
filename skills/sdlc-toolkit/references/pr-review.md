# Running pr-review

pr-review runs a headless code review in a fresh session, so the reviewer has none of the build session's context. `sdlc:setup` installs it.

## Find the script

```bash
claude plugin list --json | jq -r '.[] | select(.enabled and .id == "pr-review@aasimsani-pr-review") | .installPath'
```

The command prints `PR_REVIEW_ROOT`, and the script is `$PR_REVIEW_ROOT/skills/pr-review/pr-review.sh`. If it prints nothing, pr-review isn't installed or isn't enabled, so tell the user to run `sdlc:setup`. Never guess the path.

## Run it

Every run takes several minutes and costs real money, so run it in the background and record the cost line from the report.

- **Local** (Build and Test). Commit first, because the script reviews committed `HEAD` only. Then run `"$SCRIPT" --local` from the repo root. It prints the review file's path on stdout.
- **PR** (Ship). Run `"$SCRIPT" --repo <owner/name> --pr <n>`. It writes `~/pr-reviews/<date>/<owner>_<repo>_PR<n>.md`.

## Perspectives

pr-review takes one `--panel FILE` and any number of `--lens FILE` flags. The panel says who reviews, and each lens adds a reviewer or rules. Build every run's flags in this order:

1. **The stage's default lens.** Build and Test runs add `--lens "$PR_REVIEW_ROOT/examples/ponytail-lens.md"`. It adds an over-engineering reviewer whose SIMPLE findings never block, so it suggests cuts without holding up the stage. Ship adds no default lens, so the human reviewer sees correctness findings without simplification nits.
2. **The feature's perspectives.** When `sdlc.yaml` has a `pr_review` block, pass its panel and lenses to every run. A stage key overrides the feature default for that stage.

   ```yaml
   pr_review:
     panel: .pr-review/panels/red-team.md        # optional, for every stage
     lenses: [.pr-review/lenses/migrations.md]   # added to every stage
     ship: {panel: .pr-review/panels/default-plus-lead.md}
   ```

3. **The repo's own perspectives.** pr-review reads `REVIEW.md`, `.pr-review/panel.md` and `.pr-review/lenses/*.md` from the base branch by itself, so don't pass them.

When the spec is high-risk, ask the approver at Build whether to add a specialist panel or lens for the risky area, such as the red-team panel in `$PR_REVIEW_ROOT/examples/` for an auth change. Record the answer in `sdlc.yaml`.

## After each run

1. Copy the review to `docs/sdlc/<slug>/pr-review/<stage>-<n>.md`, numbering runs from 1.
2. Read its `## Summary` totals and `## Issues` table.
3. Compare its fingerprints with the previous run's. A fingerprint that disappeared is **fixed**, one that appeared is **new**, and one in both runs is **open**.
4. Deal with the **blocking findings**, which are the Critical and High ones. A stage can't finish while one is open. Fix each one, or record a won't-fix reason that the approver accepts. Medium and Low findings are the owner's call.
5. Stop after two runs in a row that close no blocking finding. Show the approver what's still open, and run it again only if they say to.
