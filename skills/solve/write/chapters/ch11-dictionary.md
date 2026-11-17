# Dictionary workflow

## Core idea

The dictionary controls word status, part of speech, meaning, permitted form, and
usage. A suggested alternative is not always a direct replacement.

## Dictionary facts

Issue 9 contains 875 approved words and 1,274 non-approved entries. It does not
list technical nouns or technical verbs as normal headwords.

An approved word can still be wrong when:

- the sentence uses a different part of speech.
- the sentence uses an unapproved meaning.
- the dictionary does not permit the form or tense.
- a help note restricts the word to a context.

## Lookup workflow

1. Find the candidate word.
2. Check uppercase approved status or lowercase non-approved status.
3. Check the part of speech.
4. Check the exact approved meaning.
5. Check permitted forms and help notes.
6. Review the STE example.
7. If an alternative changes grammar or meaning, reconstruct the sentence.

## Help categories

Dictionary help can:

- explain how to use an approved word.
- restrict an approved word to one meaning.
- restrict a word to one context, such as safety text.
- give other important usage information.

## Failure modes

- Treating the first suggested alternative as mandatory.
- Using an approved word with an unapproved meaning.
- Assuming the linter includes the full dictionary.
- Copying a dictionary example when its domain facts do not apply.

## Connects to

- [ch02](ch02-words.md): terminology
- [references/source-notes.md](../references/source-notes.md): source lookup
