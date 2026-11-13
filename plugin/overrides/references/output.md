# Deliver the reviewed result

Write plain claims and recommendations before hashing them. Use
`bin/prose-check --offline` and preserve meaning when fixing true findings.
Missing lint engines remain explicitly skipped.

For a decision, render the Markdown report and portable HTML view together:

```bash
"$SOLVE_ROOT/bin/render-report" --run-dir "$RUN_DIR" --slug "$SLUG" \
  --output "$REPORT" --portable-html
```

The portable renderer uses bundled code and no external HTML dependency. It
embeds evidence summaries and recorded receipts so a standalone page retains
its support. It marks the page as pre-consumer or unverified. Rendering does
not create final completion. The subsequent consumer review and separate
completion receipt bind the exact report and view bytes.

Run `bin/artifact verify "$PAGE" --browser` when a browser is available.
Static HTML checks do not establish visual correctness. Browser success does
not establish factual truth. The independent consumer still reads the actual
report and view and exercises each declared acceptance surface.

Finish with `bin/gates validate` and `bin/gates finalize`. Leave reviewed files
unchanged. Save the delivered report and view through the host's durable file
workflow. For an auditable handoff, preserve the run's request, intake, claims,
facts, receipts, evidence, source, and completion receipt in a companion packet.
Exclude secrets and unrelated files. The local contract binds absolute paths;
an exported copy retains evidence but cannot independently prove the original
runtime state. Do not rewrite hashes to make a relocated copy look verified.

Include the recommendation and next action in chat, plus actual verification
status, important unknowns, and links. Do not make the reader open files to learn
whether the decision is blocked. Use the requested format and length.
