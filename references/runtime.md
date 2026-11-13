# Adaptive run contract

## Tier profiles and budgets

| Tier | Time | External spend | Evidence depth |
|---|---:|---:|---|
| Quick | 15 minutes | $2 | Focused checks of deciding claims |
| Standard | 30 minutes | $5 | Cross-check sources and alternatives |
| Deep | 60 minutes | $15 | Replication, sensitivity, and counterexamples |

All three require evidence, independent refutation, and consumer verification.
There is no framework count. `bin/tier <tier> --json` returns the profile;
`bin/tier defaults <tier>` retains the two-value budget interface. Old count and
phase-list switches fail explicitly.

After gates init, write any launcher budget overrides through state-rw:
`{"time_seconds":1800,"tokens_usd":5}`. JSON null means unlimited. tokens_usd is
a compatibility name for external research spend, not model tokens. Export RUN_DIR,
SOLVE_RUN_DIR, SOLVE_COST_FILE="$RUN_DIR/cost-usd", SOLVE_EXTERNAL_SPEND_CAP, and
TEL_START from state.started_at when invoking the existing budget/research helpers.

At 80%, start no optional methods or new paid research. At 100%:

```bash
"$SOLVE_ROOT/bin/gates" halt --run-dir "$RUN_DIR" \
  --reason "Time cap exhausted; refutation and consumer checks remain unverified"
```

Then render a clearly unverified draft. Do not complete or downgrade an applicable
gate to N/A. On explicit budget renewal, update budget/start time, clear the prior
halted budget_status and partial flag, recheck receipts, and resume unfinished work.
The finalizer also checks the live run spend ledger and elapsed wall time.
A current completed run retains its original verification timestamp; idle time
does not expire it. Changing the decision or receipts requires current-time
budget checks again. Repeated finalization preserves the original completion.

## Data files

- request.md: the original user request, without builder rewriting.
- intake.json: user-provided constraints, success criteria, and consumer context.
- claims.json: the decision's assertions and acceptance conditions.
- facts.json: observed applicability facts keyed by the catalog's fact names.
- gates/<id>.json: the current receipt for each gate.
- gate-history.jsonl: replaced receipts, including failures.
- evidence/: source captures and expected/observed probe output.
- frameworks/: only methods whose triggers fired.
- reviews/: original-input bundles, independent framing, and review receipts.
- render.json: the report path/hash, any HTML view path/hash under subject.views,
  and the decision digest used to render it.
- prose/: advisory simplify-writing lint input and findings from bin/prose-check.
- completion.json: the final binding to the report and its consumer receipt.
- state.json: operational metadata, recommendation, next_action, budgets, and timestamps.

A material claim is one whose negation could change the choice, its conditions,
or the next action. Both independent reviewers must search for material claims
the builder did not list.

Example claims.json:

```json
[
  {
    "id": "reader-removal",
    "statement": "The reader no longer returns the removed page.",
    "kind": "fact",
    "critical": true,
    "acceptance": {
      "surface": "reader lookup for page example",
      "expected": "No page returned"
    }
  }
]
```

Use kind forecast for future outcomes and include string fields assumptions and
followup. A forecast is not a verified future fact. Use preference only for
user-owned values, with their stated source.

## Applicability evidence

The catalog owns the written trigger. Record a Boolean only when supported by
an observed fact; otherwise use null or leave it absent and record BLOCKED.

```json
{
  "stakeholder_conflict": {
    "value": false,
    "reason": "The user explicitly identified one decision-maker and no opposed requirements.",
    "evidence": [{"path": "evidence/intake-observation.md", "sha256": "<actual hash>"}]
  }
}
```

Obtain actual hashes with `bin/gates hash --run-dir "$RUN_DIR" evidence/file.md`.
Evidence must resolve inside the run; traversals and symlinks escaping it are
rejected. Capture an external response or observation in a run evidence file.
Never fill a hash from memory or call a missing response a successful check.

Evaluate with gates inspect. It returns the exact trigger, observed trigger_value
(true/false/null), affected claim IDs, and input_digest. Carry that digest into the
receipt. Optional `--claims c1 c2` scopes a method to named claims. Required gates
always bind the complete claim set.

## Gate receipts

All receipts require gate, state, trigger, claims, input_digest, and reason.

FIRED adds artifact and checks:

```json
{
  "gate": "evidence",
  "state": "FIRED",
  "trigger": "Every strategic decision requires checks of its critical claims.",
  "claims": ["reader-removal"],
  "input_digest": "<digest returned by inspect before the check>",
  "reason": "The reader lookup was exercised and the response was captured.",
  "artifact": {"path": "evidence/reader-check.md", "sha256": "<actual hash>"},
  "checks": [{
    "claim": "reader-removal",
    "surface": "reader lookup for page example",
    "expected": "No page returned",
    "observed": "The reader returned the old page.",
    "passed": false,
    "evidence": [{"path": "evidence/reader-response.json", "sha256": "<actual hash>"}]
  }]
}
```

This check FIRED and found a failure. It cannot justify verified completion.
Every affected claim needs a check. Each required gate covers every critical claim.

N/A requires a supported false evaluation and the exact catalog trigger. It does
not require a framework artifact. BLOCKED requires a nonempty unverified list:
claim IDs or specific missing knowledge, plus a reason naming the obstruction.

`bin/gates record --run-dir "$RUN_DIR" --file receipt.json` validates before
writing. Invalid records fail rather than being saved as successes. Consumers
treat missing, malformed, or stale records as BLOCKED. Rendering and progress use
this same validator, never a count of Markdown files.

## Freshness and finalization

File references hash exact bytes with SHA-256. Structured digests use sorted,
compact UTF-8 JSON. Method receipts bind the catalog, request, intake, affected
claim definitions, and applicability fact. Required gates bind the entire claim
set. Refutation also binds recommendation, next_action, and their post-blind reveal.

The decision digest binds request, intake, all claims/facts, catalog, non-consumer
gate receipts, recommendation, next_action, TL;DR, format, tier, partial flag, and budget caps.
Source freshness is checked independently. Operational polling counters and
completion/reviewer receipts are excluded where needed to prevent hash cycles.

Before the refuter's reveal, write nonempty recommendation and next_action strings
through state-rw. Both appear in the report and the refuter's disclosed snapshot.
Changing either requires a new independent refutation and consumer review.

```bash
"$SOLVE_ROOT/bin/render-report" --slug "$SLUG" --format pyramid \
  --run-dir "$RUN_DIR" --output "$REPORT"
# Prepare and execute a fresh consumer review, then record its gate.
"$SOLVE_ROOT/bin/gates" validate --run-dir "$RUN_DIR"
"$SOLVE_ROOT/bin/gates" finalize --run-dir "$RUN_DIR"
```

The report remains unchanged after review. Its separate completion receipt must
match the actual path, bytes, current decision, and consumer record. Manually
setting state.phase cannot create verified completion. Changing a reviewed report
or its inputs makes the old completion invalid.

## Resume and compatibility

Do not overwrite existing runs. Init refuses existing state or run artifacts.
Resume a 2.0 run by validating receipts and redoing only stale or unfinished work.
A refuter revision uses a new context; old bundles are archived by prepare.

Pre-2.0 runs remain preserved and may be read as unverified references. New reports
for such runs say unverified; progress cannot promote their old file counts to
FIRED. Choose a new run directory or archive the old one before initialization.
Existing state, budget, research, and calibration commands remain available.
Legacy HIGH-score calibration is historical; it cannot set confidence for 2.0.

## Optional integrations

gstack handoffs, research providers, telemetry, and historical outcome logging
are optional. Their absence cannot skip a required verification gate. Use existing
skills for narrower tasks, log handoffs when performed, and never claim an
unavailable integration ran. Do not edit agent configuration to obtain slots.

The validator enforces structure, coverage declarations, and current evidence
bytes. It cannot prove that an agent told the truth or never opened another file.
Fresh contexts and narrow review bundles are required orchestration behavior,
not a filesystem sandbox or a guarantee that strategic outcomes will succeed.
