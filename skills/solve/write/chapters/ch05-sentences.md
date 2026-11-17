# Sentences and cohesion

## Core idea

Write complete sentences with one clear relationship. Use lists and connectors
only when they expose structure.

## Apply it

- Keep sentences short enough for the content profile.
- Do not omit articles or required words to save space.
- Do not use contractions in strict mode.
- Use a vertical list for three or more parallel items or complex conditions.
- Use `because`, `but`, `then`, `thus`, or `as a result` only for the
  relationship each word names.
- Use `a`, `an`, `the`, `this`, or `these` when it identifies the noun correctly.

## Failure modes

- Splitting a sentence but losing the causal or conditional relationship.
- Adding connectors as decoration.
- Mixing verbs, nouns, and full sentences in one list.
- Using `this` without naming what `this` means.
- Compressing a sentence until articles disappear and noun clusters grow.

## Worked example

Dense:

> The client retries the request when the server returns 503, which can happen
> during maintenance, but it stops after three attempts to avoid duplicate work.

Clear:

> The server can return 503 during maintenance. When this occurs, the client
> retries the request. The client stops after three attempts. This limit
> prevents duplicate work.

Verify that the final claim is true. Do not invent the reason for the limit.

## Connects to

- [ch07](ch07-descriptions.md): paragraph structure
- [ch09](ch09-punctuation.md): permitted punctuation
