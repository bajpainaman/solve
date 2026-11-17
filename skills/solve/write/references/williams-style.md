# Williams and Bizup style

Apply the reader-centered principles in `Style: Lessons in Clarity and Grace`,
eleventh edition, alongside STE. Keep facts, requirement strength, safety wording,
and the user's purpose ahead of optional editorial choices.

## Diagnose before revising

Identify what the intended reader must infer. Choose the principle that addresses
that obstacle. Avoid changing a clear sentence merely to satisfy a style cue.

| Lesson | Review question | Printed pages |
|---|---|---|
| Understanding style | What makes this sentence difficult for its intended reader? | 2 to 8 |
| Correctness | Does a usage convention help this audience understand the text? | 9 to 26 |
| Actions | Can a verb express the main action more directly? | 28 to 45 |
| Characters | Can the reader identify the relevant actor? | 46 to 65 |
| Cohesion and coherence | Does each sentence connect to the reader's existing information? | 66 to 79 |
| Emphasis | Does the sentence give its important information suitable weight? | 80 to 96 |
| Motivation | Does this explanation identify a problem the reader needs to solve? | 98 to 112 |
| Global coherence | Do the sections connect to the document's purpose? | 113 to 124 |
| Concision | Can wording disappear without losing meaning or useful guidance? | 126 to 142 |
| Shape | Are the main subject and verb easy to find? | 143 to 166 |
| Elegance | Does parallel structure clarify related ideas? | 168 to 186 |
| The ethics of style | Does the wording preserve responsibility, evidence, and uncertainty? | 188 to 206 |
| Punctuation | Are grammatical relations and sentence boundaries clear? | 207 to 229 |
| Using sources | Can readers distinguish source claims from the writer's inference? | 230 to 238 |

Connect sentence openings to known information and maintain a useful topic thread.
Keep the main subject and verb accessible. Use endings to emphasize important
new information when the STE profile permits that structure.

Remove empty wording and repeated meaning. Retain qualifications and necessary
technical terms. A procedure, reference entry, or short answer can remain plain
and uniform without an essay introduction or literary variety.

## Vale checks

All three profiles load the `Williams` namespace:

| Check | Cue | Review needed |
|---|---|---|
| `ActionNouns` | Selected abstract action nouns | Decide whether the noun hides an action or names a useful technical concept. |
| `ActionPhrases` | Phrases that can use a direct verb | Preserve the actor, tense, and action. |
| `RedundantPairs` | Common wording with repeated meaning | Preserve distinctions and required emphasis. |

These rules return suggestions. They identify possible revision points and do
not determine meaning, coherence, evidence quality, or full book compliance.
They use original patterns derived from the principles. They do not reproduce
an exhaustive word list from the book.

## Jev and local source lookup

The optional bridge uses an installed `ste-writing` engine:

```bash
python3 scripts/review.py --jev --original original.md draft.md
python3 scripts/review.py --no-jev README.md
```

It loads this fork's Vale profile and combines the findings with Harper,
the global personal style, and configured Jev review.
Jev uses the existing local book index, source locations, prior decisions,
and feedback rankings. It preserves that shared history across both skills.

Use the installed `williams-style` skill to find exact book passages.
Its tools can review the complete index, reconsider decisions, and record
source feedback. Model scores remain provisional. Mark an agent's feedback
with `--reviewer agent` and keep earlier decisions in the history.

The bridge honors the engine's global Jev setting when you omit both Jev flags.
Hosted review sends the draft, an available original, summaries, and selected
excerpts to TypeSafe.

Use `--no-jev` for local checks or `--no-book` to omit
book context. No original means no comparison of meaning or requirement strength.

Revise at most twice. Review uncertain findings against the source and brief.
Preserve authorized factual additions. Ask for facts when the intended meaning
remains unclear.

Jev directs attention, and the writing agent makes justified edits.
