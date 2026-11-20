# Example: a team setup

This example shows how one team runs pr-review. The org, repos, team and PR are made up. "Acme" stands in for your GitHub org.

## Config

First, copy the [data-integration lens](data-integration-lens.md) next to the config. The lens adds a fourth reviewer and a DATA category, which suit a team that owns many connectors that must behave alike. The plugin's install path changes with each version, so copy the file rather than pointing at it.

```bash
mkdir -p ~/.config/pr-review
cp "$(claude plugin list --json | jq -r '.[] | select(.enabled and (.id|startswith("pr-review@"))) | .installPath')/examples/data-integration-lens.md" \
   ~/.config/pr-review/extra.md
```

Then save this as `~/.config/pr-review/config.sh`:

```bash
# PRs requesting MY review in these two repos
MINE_REPOS=(acme/acme-api acme/acme-web)

# PRs requesting my TEAM's review, only in the API repo
TEAM_REPOS=(acme/acme-api)

# Add the data-integration lens to every review
EXTRA_PROMPT_FILE="$HOME/.config/pr-review/extra.md"
```

To scope a whole org instead of listed repos, use a bare owner, such as `MINE_REPOS=(acme)`.

## Runs

```bash
pr-review.sh --repo acme/acme-api --pr 1234   # one PR, whoever it's assigned to
pr-review.sh --local                          # your branch, before you push
pr-review.sh                                  # everything waiting on you or your team
```

This cron entry runs batch mode at 9am and noon on weekdays:

```cron
0 9,12 * * 1-5 $HOME/bin/pr-review.sh
```

## Sample review

This review is what `--repo acme/acme-api --pr 1234` writes to `~/pr-reviews/2026-11-11/acme_acme-api_PR1234.md` when the data-integration lens is on. The PR, code and findings are invented.

~~~markdown
# Review: acme/acme-api PR #1234

- Source: https://github.com/acme/acme-api/pull/1234 — Add incremental sync for the billing connector
- Branch: `feat/billing-incremental-sync` vs `main`
- Head: `3f2c9a1e7b4d5c6a8e9f0b1c2d3e4f5a6b7c8d9e`
- Reviewed: Wed Nov 11 09:00:12 PST 2026
- Session cost: $1.84
- Tokens: in 412 · out 9,318 · cache-read 1,204,551 · cache-write 88,120

## Ask Claude follow-up questions about this review
The clone below is shared and may have moved to another PR since this
review — the checkout line restores this PR's exact code first.
```bash
cd "/Users/you/pr-reviews/repos/acme_acme-api"
git fetch --quiet origin && gh pr checkout 1234 --force
claude --resume 0b6e1d52-7c3a-4f19-9a2e-5d8c4b7f1e30
```

---

# Code Review — acme/acme-api `feat/billing-incremental-sync` @ 3f2c9a1e

## Summary
- Base: `main`
- Totals: Critical 0, High 1, Medium 1, Low 1 (Total 3)
- Verdict: needs-work

## Issues
| ID | Sev | Cat | Location | Issue |
|----|-----|-----|----------|-------|
| DATA-1 | High | DATA | `connectors/billing/sync.py:88` `fetch_since()` | The cursor advances before the page is written, so a failed write drops rows |
| PERF-1 | Medium | PERF | `connectors/billing/client.py:41` `list_invoices()` | The client requests 10 rows per page, unlike the 500 its sibling connectors use |
| DESIGN-1 | Low | DESIGN | `connectors/billing/models.py:17` `Invoice` | The model stores `amount` as a float, which the CLAUDE.md money rule forbids |

## Details
### DATA-1 — The cursor advances before the page is written, so a failed write drops rows
- Severity: High
- Confidence Score: 90
- Verification method: We read `fetch_since()` at head and traced the order of `save_cursor()` and `write_rows()`. The sibling connector in `connectors/crm/sync.py:102` writes rows first.
- Category: DATA — Integration platform consistency and reliability
- Location: `connectors/billing/sync.py:88` in `fetch_since()`
- Permalink: https://github.com/acme/acme-api/blob/3f2c9a1e7b4d5c6a8e9f0b1c2d3e4f5a6b7c8d9e/connectors/billing/sync.py#L88
- Code: `save_cursor(page.next_cursor)`
- Fingerprint: `DATA|connectors/billing/sync.py|fetch_since|cursor-saved-before-write`
- Problem: The sync saves the next cursor before it writes the page's rows. If `write_rows()` raises, the next run starts after rows that were never stored.
- Fix: Move `save_cursor()` after `write_rows()` succeeds. Wrap both in the transaction the CRM connector already uses.
~~~
