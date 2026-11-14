# Writing that preserves meaning

Use the bundled [writing guide](../write/WRITE.md). It adapts simplify-writing
for a portable plugin. Its references, original upstream guide, Vale rules,
Harper configuration, and MIT license are included under `write/`.

## Choose the work

For rewrite, return the revised text. For audit, report findings without editing.
For a file edit, preserve the original and inspect the diff. For new prose,
write only from the supplied brief and inspected evidence.

Match the user's audience and requested voice. Use direct technical prose for
claims and reports. Preserve distinctive voice in messages, essays, and marketing
copy while removing filler. Do not flatten all writing into a rigid manual.

## Preserve the invariants

Record the original facts, names, numbers, units, literals, URLs, code,
requirements, conditions, exceptions, sequence, uncertainty, and attribution.
Keep `must`, `should`, `may`, and `can` distinct. Never convert a promise into a
measured result, a correlation into a cause, or a guess into a fact.

Make at most two useful revision passes: clarity, then semantic comparison.
If a sentence is ambiguous in a way that changes meaning, retain the ambiguity
and flag it, or ask the one question needed to resolve it. Cosmetic choices
do not need another approval.

## Check available tools without downloads

Use the bundled helper in offline mode:

```bash
"$SOLVE_ROOT/bin/prose-check" --offline --file "$DRAFT"
```

The helper uses installed Vale and Harper only. It reports missing tools or
style packages as `SKIPPED`; skipped checks are not passed checks. Do not run
`vale sync`, a package manager, or the optional upstream review bridge during
ordinary plugin use. A manual edit remains useful when automation is absent.
The helper is advisory, never proof of ASD-STE100 compliance or factual accuracy.

In a decision run, lint claim text before gate digests and recommendation text
before refuter disclosure. Editing reviewed prose invalidates its hashes and
requires the affected review again. Do not polish a finalized file in place.

## Deliver

For a plain rewrite, return the text without an audit essay. For a report or
file edit, mention material uncertainty and actual verification limits once.
When host writing blocks are available, follow their skill for complete drafts.
When a downloadable document is requested, use the host's format-specific skill
and save the result. Do not claim a file exists based only on a rendered draft.
