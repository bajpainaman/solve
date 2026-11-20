# Tamarin examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its declared outcomes and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/signed-challenge](good/signed-challenge/README.md) | good | OAuth / OIDC / session protocols; webhook signatures (E) | An `expect:` comment per lemma, a rejected design in its own theory, a replay attack as a found trace |
| [bad/dead-rule](bad/dead-rule/README.md) | bad | Any | A safety lemma about an action that can never fire holds vacuously; an executability lemma for that action exposes it |

## Anti-patterns without a reproduced example yet

`../references/anti-patterns.md` describes this one.

- A freshly generated value modeled as a public constant instead of `Fr(~n)`
