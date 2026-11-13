# Words and technical terminology

## Core idea

Use a restricted common vocabulary, but keep necessary technical nouns and verbs.
Use each approved word only for its approved part of speech and meaning.

## Apply it

1. Identify domain terms, product names, APIs, identifiers, and defined legal
   terms.
2. Lock those terms before rewriting.
3. Pick one name for each remaining concept.
4. Prefer a short common word when it preserves meaning.
5. Use American spelling unless a governing directive requires another form.

For strict STE work, verify the word in the official dictionary. The bundled
word map covers common problems only.

## Technical-term rules

- Use terms accepted by the company, industry, or subject field.
- Prefer short terms that are easy to understand.
- Do not use slang, regional language, or unexplained team jargon.
- Do not use a technical noun as a verb.
- Do not use a technical verb as a noun.
- Do not rotate synonyms for the same item.

## Failure modes

- Replacing a defined term because it sounds complex.
- Changing `INSERT`, `commit`, `branch`, or another code-domain term mechanically.
- Using a simpler word that has broader or narrower scope.
- Replacing `should` with `must` and changing requirement force.

## Worked example

Source:

```text
The worker will leverage the configuration utility to facilitate the
initialization of the service.
```

Rewrite:

```text
Use the configuration utility to start the service.
```

The rewrite keeps `configuration utility` because it identifies a real tool. It
replaces three abstract actions with the primary action `start`.

## Connects to

- [ch11](ch11-dictionary.md): dictionary selection
- [references/word-choice.md](../references/word-choice.md): review map
