# Cedar examples

`tests/examples.d/cedar.sh` in the repository runs every example in this
table. A good example meets its declared outcomes and detects its
mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/document-access](good/document-access/README.md) | good | ABAC / policy languages (E) | A forbid rule checked across several entities, and a rejected design that drops it checked as a witness |
| [bad/shadowed-permit](bad/shadowed-permit/README.md) | bad | ABAC / policy languages (E) | A forbid narrower than it needs to be shadows the permit it was meant to leave alone, and a missing test case hides it |
