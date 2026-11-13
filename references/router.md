# Router

Make three choices for every request, in this order: the mode, the format, then
the template. The write layer applies to all prose in every mode.

## 1. Mode

Pick the first row that matches.

| The request… | Mode | What runs |
|---|---|---|
| asks to choose between options with stakes: "should we", "which", build or buy, go or no-go, strategy | **decide** | The gated decision workflow in SKILL.md. It ends in the `decision-memo` page |
| reports a reproducible bug, a failing test or wrong output | **route** | An available investigate skill. Do not start a decision run |
| pitches an unvalidated product idea | **route** | office-hours when available. Do not start a decision run |
| asks to rewrite, simplify, de-slop, audit or lint prose | **write** | [write/WRITE.md](../write/WRITE.md) |
| asks for a page, report, review, plan, explainer, deck, prototype or small tool | **make** | Steps 2 and 3 below, then the template's renderer |
| asks a question with a short factual answer | **answer** | Reply inline. Use the write layer |

Signals that move a request between modes:

- A "make" request that contains an open choice with stakes ("plan the migration
  and tell me whether to use Kafka") is **decide** first. The plan follows the
  decision.
- A "decide" request with no real alternatives, or one whose answer is a known
  fact, is **answer**. Do not run gates to look rigorous.
- A "write" request about a whole document the reader will act on can also be
  **make**. Ask only if the user named neither format.

## 2. Format

Use HTML when any one of these is true. Otherwise use Markdown.

| Use HTML when | Example |
|---|---|
| The user asked for a page, artifact, deck or HTML | "make it a page" |
| The reader will act on the page: decide, tick, triage, comment, tune | test plan, triage board, decision memo |
| The information is spatial: diffs, flows, timelines, layouts, tokens | PR review, pipeline, postmortem |
| Options must sit side by side to compare | approaches, design directions |
| A behavior must be felt, not described: motion, interaction, a live model | animation sandbox, concept explainer |
| The result is more than one screen and others will review it | status report, RFC, plan |

Stay in Markdown when the answer fits in a few sentences, when it is code, a
command or a config block, when the reader reads it once and moves on, or when
the user asked for Markdown or a file format.

## 3. Template

Run `bin/templates match "<the request>"`. It ranks the catalog and prints the
renderer, the exemplar path, and the type file under `html/references/types/`. Take the top hit
unless a lower one plainly fits better. `bin/templates list` shows all 32.

| Family | Templates | For |
|---|---|---|
| decide | decision-memo | A gated recommendation. Only the decide mode uses it |
| explore | code-approaches, visual-directions, implementation-plan | Options before a choice, and the plan after it |
| code | pr-review, pr-writeup, module-map | Reviewing, explaining and mapping code |
| design | design-system, component-variants | Tokens and component states |
| prototype | animation-sandbox, clickable-flow | Feel motion or interaction |
| diagram | flowchart, svg-figures | Processes and figures |
| communicate | slide-deck, status-report, incident-report, pitch-doc | Updates, postmortems, talks and buy-in |
| research | feature-explainer, concept-explainer, teach-unknowns, reference-port | Explaining code, concepts and references |
| editor | triage-board, feature-flags, prompt-tuner | Throwaway tools that output a result |
| unknowns | blindspot-pass, interview, tweakable-plan, brainstorm, design-directions, mock-first, implementation-notes, change-quiz | Finding what you do not know before, during and after a build |

No hit means no template fits. Use the router in [html/HTML.md](../html/HTML.md) directly, or Markdown.

### Renderers

| Renderer | Steps |
|---|---|
| `solve` | Finish the decision workflow. `bin/render-report --html` writes and verifies the page. Never hand-write it |
| `artifact` | Read the exemplar for structure. Then read `html/references/components.md`, the type file and `html/references/rules/writing.md` in one command. Write `<name>.src.html` from components. Run `node $SOLVE_ROOT/html/scripts/build.mjs <name>.src.html --verify` |
| `bespoke` | Read the exemplar. Write one self-contained page with the same interaction. Add dark mode with `prefers-color-scheme` and keep text at 12px or more. The exemplars miss both, so do not copy those parts. Run `node $SOLVE_ROOT/html/scripts/verify.mjs <page>.html` |

When `html/` is missing, run `bin/html-sync`. Until it runs, `bin/templates`
reports `artifact` templates as `bespoke`. If `verify.mjs` is not available either, say in one line
that the page was not verified.

### Rules for every page

- The `h1` or lede states the answer, with its key number. Never the topic.
- If the reader must decide or do something, the first screen says what.
- Show the visual first, then the prose that explains it. Put detail in `<details>`.
- Every action item has an owner. Do not invent owners or dates. Use the role
  that the request names, or "Owner: to assign".
- Replace credentials with `<REDACTED:KIND>`. All exemplar names and data are
  fictional. Do not copy them into a real page.
- Name the file by kind, such as `postmortem_queue-backlog.src.html`. Put it in
  `.context/` unless the user names a place. On macOS, `open` the built page.

## 4. Write layer

Apply [write/WRITE.md](../write/WRITE.md) to all prose that this skill writes:
answers, claims, reports and page text. Never apply it to code, identifiers,
commands, URLs or quoted material.

| Text | Profile |
|---|---|
| Reports, explainers, claims, recommendations | Description, STE-flavored |
| Steps, runbooks, test plans, setup | Procedure |
| Warnings that involve injury or damage | Safety. Ask before you choose WARNING or CAUTION |
| Labels, buttons, error and status text | Interface |

Lint before delivery:

- Decide mode: `bin/prose-check --run-dir "$RUN_DIR" --scope claims` and
  `--scope decision`, at the points that SKILL.md names.
- Make and write modes: `bin/prose-check --file <page>.src.html` or the
  Markdown file. Lint the source, not the built page. The built page holds
  component text that is not yours.

Fix true findings. Keep every number, condition, modal verb and uncertainty
label. The lint is advisory. Report findings you left on purpose.
