# Punctuation and word count

## Core idea

Punctuation must expose sentence structure. It must not carry relationships that
the words leave ambiguous.

## Punctuation rules

- Do not use semicolons.
- Use hyphens for words that function together.
- Use parentheses for defined purposes, such as references, IDs,
  abbreviations, explanations, or alternatives.
- The STE rules do not ban em dashes. This skill's AI-prose overlay removes them
  because they often hide sentence structure.

## STE word count

For strict checks:

- a colon before a vertical list ends the preceding sentence.
- parenthetical text counts as one word.
- each number, number-plus-unit, abbreviation, alphanumeric ID, quotation,
  heading/label, or proper name counts as one word.
- a hyphenated term counts as one word.

The bundled linter approximates these rules. It cannot identify every proper name
or technical token.

## Failure modes

- Replacing a semicolon with a comma and creating a run-on sentence.
- Removing an em dash without preserving contrast or explanation.
- Hyphenating a long noun cluster instead of clarifying it.
- Treating a linter's approximate count as certification.

## Worked example

Source:

```text
The check failed; restart the worker.
```

Rewrite:

> The check failed. Restart the worker.

The period separates a state from an instruction.

## Connects to

- [ch05](ch05-sentences.md): complete sentence structure
- [ch03](ch03-multi-word-nouns.md): hyphenated units
