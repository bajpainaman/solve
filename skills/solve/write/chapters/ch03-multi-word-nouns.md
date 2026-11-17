# Multi-word nouns

## Core idea

Long noun clusters force the reader to guess which word modifies which item.
Keep a multi-word noun to three words when possible.

## Apply it

- Identify consecutive nouns or modifiers that together name one item.
- Preserve the complete technical term at first use.
- If the official term has more than three words, define a short form after the
  full term.
- Use hyphens only when they make one unit clear.
- Repeat the selected form consistently.

## Failure modes

- Deleting part of an official term.
- Inventing an abbreviation that the organization does not use.
- Using different short forms in the same document.
- Adding many hyphens without resolving the underlying noun cluster.

## Worked example

Dense:

> Review the production database credential rotation failure recovery procedure.

Clear:

> Review the failure-recovery procedure for production database credential
> rotation.

If the document uses this term repeatedly, define a stable short form:

> Review the Production Database Credential Rotation Procedure (the rotation
> procedure).

Then use `rotation procedure` for later references.

## Decision rule

If shortening can change the identity of the item, keep the full term. Clarity
does not permit an inaccurate name.

## Connects to

- [ch02](ch02-words.md): stable terminology
- [ch09](ch09-punctuation.md): hyphenation and word count
