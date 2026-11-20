# Running the rfc skill

`rfc` is a personal skill, not part of this plugin. It writes an engineering RFC as a reviewable HTML page. When the session lists it, invoke it with the Skill tool and give it these overrides:

- Write the source to `docs/sdlc/<slug>/rfc.src.html` and build `rfc.html` next to it. Its default location is the repo root.
- In its Gather step, read the concepts brief, `intent.md` and `spec.md` first.

## When the skill isn't available

Run `egm-draft`, as `egm.md` describes, to write `docs/sdlc/<slug>/rfc.md`. Then add any of these RFC sections the draft lacks: Constraints, an Options table with a verdict column, a Fallback with its triggers, Phases with a PR table, Proposed tickets, and Blast radius.
