# AI-prose overlay

This overlay adds writing checks for AI output. It is not part of
ASD-STE100.

## Remove em dashes

The standard does not prohibit em dashes. This overlay does. Replace an em dash
with a period, comma, colon, or parentheses only when the relationship stays
clear.

## Delete throat-clearing

Delete openings that delay the point:

- `It is important to note that...`
- `It is worth mentioning that...`
- `In today's rapidly evolving...`
- `When it comes to...`
- `At its core...`
- `As we have seen...`
- `In conclusion...`

Start with the fact, decision, action, or result.

## Replace hype with evidence

Do not use these words without a defined property or measurement:

`robust`, `seamless`, `powerful`, `innovative`, `cutting-edge`,
`game-changing`, `best-in-class`, `scalable`, `secure`, `fast`, `easy`,
`comprehensive`, `transformative`, `revolutionary`.

Examples:

- Weak: "The service provides a robust authentication solution."
- Better: "The service rejects expired tokens and rotates signing keys every 24 hours."

- Weak: `This seamless workflow improves productivity.`
- Better: "The workflow removes two manual approval steps."

## Remove model-favored filler

Review or delete:

`delve`, `leverage`, `utilize`, `facilitate`, `foster`, `empower`, `unlock`,
`navigate`, `underscore`, `showcase`, `pivotal`, `nuanced`, `multifaceted`,
`intricate`, `vibrant`, `realm`, `landscape`, `tapestry`, `journey`,
`ecosystem`, `testament`, `fundamental`, `significant`, `crucial`.

Use a direct verb or a concrete noun.

Prefer these common forms when meaning stays equal:

| Instead of | Prefer |
|---|---|
| begin, commence, initiate | start |
| utilize, leverage | use |
| facilitate | help |
| ensure | make sure |
| prior to | before |
| subsequent to | after |
| regarding, concerning | about |
| obtain, acquire | get |
| demonstrate | show |
| additionally, furthermore, moreover | also, or no connector |

## Do not rotate synonyms

AI often changes a term to sound less repetitive. Technical writing needs stable
terms.

- Pick `request`, not `request`, `call`, `operation`, and `interaction` for the
  same object.
- Pick `user`, not `user`, `customer`, `operator`, and `individual` unless these
  roles differ.
- Repeat the exact component name.

## Control transitions

Use a connector only when it states a real relationship:

- `because` for cause.
- `but` for contrast.
- `thus` or `as a result` for consequence.
- `then` for sequence.
- `for example` for an example.

Delete ornamental transitions such as `moreover`, `furthermore`, and
`additionally` when paragraph order already shows addition.

## Remove fake certainty and fake balance

Do not add:

- `clearly`, `obviously`, or `undoubtedly` without proof.
- "some may argue" without a real source.
- a benefits-and-challenges paragraph when the user asked for one decision.
- a generic caveat that does not change the answer.
- A claim that `experts agree` without attribution.

State the evidence, confidence, and unknowns.

## Compress repeated structure

Avoid:

- a preview paragraph, a detailed list, and a closing paragraph that repeat the
  same points.
- every bullet starting with a bold label followed by the same idea.
- "What this means" after a sentence that already states the meaning.
- a summary when the response is already short.

Say each fact once.

## Preserve useful voice

Direct does not mean robotic. Keep:

- concrete examples.
- domain-specific humor that does not hide meaning.
- a decisive recommendation with its reason.
- explicit uncertainty.
- brief empathy when the situation warrants it.

Do not force uppercase, aerospace terminology, or formal warning labels onto
ordinary chat.
