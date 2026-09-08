# Bounded roles and independent verification

## Shared ownership contract

Every agent brief names the original task, allowed inputs, owned output paths,
and required observations. Tell it other agents share the workspace and it must
not overwrite or revert their work. No nested agents. Missing information goes
to the lead. A completion message is only a notification.

The lead is the builder: it owns intake, claims, facts, framework artifacts, state,
and report assembly. A researcher is optional and owns only a named evidence lane.
Do not create a standing phase team. Read compact method cards only when triggered.

## Refuter: first establish an independent view

Spawn a new agent with `fork_turns="none"`. Its initial bounded task is independent
refutation; tell it to wait for its prepared manifest before reading workspace
files. Use the returned agent identity to prepare the bundle:

```bash
"$SOLVE_ROOT/bin/gates" prepare --run-dir "$RUN_DIR" \
  --role refuter --agent-id "$REFUTER_ID"
```

Give it only the manifest path, the allowed input paths, and this brief:

> You are an independent refuter. Read only your prepared original request and
> user constraints at first. Do not read the parent conversation, claims.json,
> facts.json, state.json, frameworks, hats, or builder evidence. Formulate the
> decision and the assertions that would have to hold. Find your own primary
> evidence, using original user sources when relevant. Save observations under
> reviews/refuter/evidence/. Write reviews/refuter/blind.json, then notify the
> lead and stop until the lead supplies the reveal receipt.

blind.json requires framing (string), material_claims (nonempty list), and evidence
(nonempty list of hashed run files). Commit this before disclosure, not afterward.

When builder claims, recommendation, next action, and applicability facts are stable, call:

```bash
"$SOLVE_ROOT/bin/gates" reveal --run-dir "$RUN_DIR"
```

The helper refuses disclosure without the independent framing. It binds those
bytes and writes a claim/recommendation/next-action snapshot. Give the same refuter the reveal
and claims snapshot. Its follow-up task:

> Compare the disclosed claims, recommendation, and next action against your independent view.
> Do not read builder rationale, framework outputs, confidence, or roleplay files.
> Check every critical claim through sources you inspect yourself. Audit gate
> declarations: unsupported absence cannot justify N/A. Identify material claims
> missing from the ledger and unsupported parts of the recommendation. A claim
> is material if negating it could change the choice, conditions, or next action.
> Record observations, checks, and coverage. Preserve dissent; do not optimize for
> agreement. Return a candidate refutation gate receipt.

The receipt follows runtime.md and adds:

```json
{
  "review": {
    "agent_id": "<actual refuter identity>",
    "manifest": {"path": "reviews/refuter/manifest.json", "sha256": "<actual hash>"},
    "reveal": {"path": "reviews/refuter/reveal.json", "sha256": "<actual hash>"}
  },
  "coverage": {
    "complete": true,
    "missing_claims": [],
    "unsupported_recommendations": [],
    "reason": "<actual comparison of independent claims against the ledger>",
    "evidence": [{"path": "reviews/refuter/evidence/coverage.md", "sha256": "<actual hash>"}]
  }
}
```

Coverage is a substantive check, not a boilerplate declaration. Missing claims,
unsupported conclusions, and failed checks block finalization. A changed
recommendation, next action, or claim set requires a new refuter and another blind/reveal cycle.
Do not merely rehash an old review. Old bundles and receipts remain preserved.

The lead may record the reviewer's receipt with bin/gates; it must not author the
reviewer's observations or substitute its own favorable verdict.

## Consumer: verify the actual delivered result

After pre-consumer checks pass, render the report. Spawn another fresh agent with
`fork_turns="none"`, initially waiting for its manifest. Prepare it:

```bash
"$SOLVE_ROOT/bin/gates" prepare --run-dir "$RUN_DIR" --role consumer \
  --agent-id "$CONSUMER_ID" --report "$REPORT"
```

Give it this brief and the manifest:

> You are the cold reader and consumer verifier. Read the actual report at the
> prepared subject path, then follow its cited evidence. Do not read private
> builder notes or the parent conversation. Can you identify the recommendation,
> its conditions, what remains uncertain, and what would change the choice?
> Independently identify material claims omitted from the ledger. Exercise every
> critical claim's declared acceptance surface and record expected and observed
> results. If a claim concerns a page, query its reader or serving interface;
> filesystem deletion is insufficient. For a forecast, check its assumptions,
> uncertainty label, and follow-up condition rather than asserting future truth.
> Save observations under reviews/consumer/evidence/ and return a consumer gate
> receipt. Do not edit the report. An inaccessible surface leaves work BLOCKED.

The consumer receipt includes review.agent_id, the hashed consumer manifest, the
same coverage object as refutation, and subject copied exactly from the manifest
(actual absolute report path and hash). Each check's surface and expected result
must match its claim's acceptance condition. Evidence contains actual observations,
not statements that the evidence file exists.

Changing the report or decision requires fresh consumer review. A separate
completion receipt avoids rewriting the report after its hash has been checked.

## Optional Six Hats

Only when the six-hats trigger fires, use the compact card. If the user requests
all hats, each receives original frozen inputs in a fresh context and owns one
output file. Otherwise address only the named missing perspectives. Do not give
later hats earlier outputs. Use waves under the host limit; no configuration edits.

Hat agreement is qualitative context. It contributes no numerical confidence,
does not count as replication, and never satisfies refutation or consumer gates.

## Operational boundaries

The validator checks declared fresh identities, manifests, reveal order, evidence
hashes, coverage, and the report binding. A shared workspace does not enforce
input secrecy. Never claim OS-level isolation. The orchestrator must actually
use fresh non-inherited contexts and the reviewer must obey its input contract.
If the host cannot supply fresh agents, record required review gates BLOCKED.

Reuse an agent only for the two stages of the same unchanged refutation. Revisions
and consumer reviews need new identities. Stop obsolete work using the host's
controls, and use message/wait facilities rather than shell polling.
