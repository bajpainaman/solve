# Rewrite workflow

Use this workflow for every rewrite, audit, or authored response.

## 1. Capture semantic invariants

Make a private checklist before changing words:

| Invariant | Questions |
|---|---|
| Actor | Who or what does the action? Is the actor known? |
| Action | What actually happens? What is the primary verb? |
| Object | What receives the action? |
| Condition | What must be true first? |
| Sequence | Which action occurs first, next, or at the same time? |
| Modality | Is this required, advised, permitted, possible, or uncertain? |
| Result | What changes, fails, or becomes possible? |
| Evidence | Which source, measurement, or observation supports the claim? |
| Literals | Which names, numbers, units, code, flags, URLs, and quotations must stay exact? |

If the source does not identify one of these elements, do not invent it.

## 2. Classify the block

- **Procedure**: the reader must do something.
- **Description**: the reader must understand something.
- **Safety**: the reader must prevent injury, death, or object damage.
- **Interface**: the reader must understand a status or choose an action quickly.

Split mixed blocks. Put explanation before or after the steps, not inside every
step.

## 3. Build the sentence spine

Use these default shapes:

- Description: `Actor + active verb + object + condition/result.`
- Command: `Imperative verb + object + qualifier.`
- Conditional command: `When/If <condition>, <command>.`
- Cause: `<Cause>. As a result, <effect>.`
- Safety: `<WARNING|CAUTION>: <command or condition>. <risk or result>.`
- Status: `<Thing> <state>. <Next action>.`

Keep the primary action in the main verb. Do not hide it in nouns such as
`implementation`, `utilization`, `execution`, or `completion`.
Retain a noun when it names a necessary technical concept.

## 4. Split and order

Split a sentence when it has:

- two independent actions.
- more than one condition.
- a long interruption between actor and verb.
- a contrast and a result in the same sentence.
- more than the profile word limit.

For procedures, use one instruction per sentence. Keep simultaneous actions in
one sentence only when simultaneity is necessary.

Use a vertical list when three or more items share the same grammatical role.
Start every list item with the same part of speech.

For descriptions, connect sentence openings to known information.
Keep a useful topic thread across the paragraph. Give the important new point
appropriate weight at the end when the STE profile permits that structure.
Read [Williams and Bizup style](williams-style.md) for contextual guidance.

## 5. Control vocabulary

Use the same term for the same item. Prefer concrete words with one likely
meaning. Keep domain terms that identify real concepts. Define an unfamiliar
technical noun at first use.

Do not replace:

- product names, API names, flags, identifiers, or code tokens.
- a legal or standards term whose exact wording carries force.
- a technical term when the simpler word is less precise.
- modality without evidence that the requirement level is equal.

## 6. Apply the AI-prose overlay

Delete sentences that only announce importance, structure, or confidence. Replace
hype with an observable property. Replace vague benefit claims with the user
effect, measurement, or known mechanism.

Read `ai-prose-overlay.md` for the full list and examples.

## 7. Verify fidelity

Compare source and result:

1. Count facts, numbers, conditions, exceptions, and requirements.
2. Confirm that each one still exists.
3. Confirm that no new fact or causal claim appeared.
4. Confirm that `must`, `should`, `may`, and `can` kept their meanings.
5. Confirm that code and literals are byte-identical.
6. Read the rewrite as a first-time reader and resolve every ambiguous pronoun.

## 8. Decide the output

- Pasted text: return the rewrite first.
- Audit request: return numbered findings and proposed fixes.
- File edit: edit, lint, show the diff summary, and report exceptions.
- Safety ambiguity: stop and ask the user to confirm risk and consequence.
