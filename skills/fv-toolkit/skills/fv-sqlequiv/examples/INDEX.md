# SQL equivalence examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its declared outcomes and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/rewrite-equivalence](good/rewrite-equivalence/README.md) | good | SQL transform / dbt model rewrite equivalence (C1) | An `expect:` comment per check, a rejected rewrite that must produce a counterexample table |
| [bad/domain-without-null](bad/domain-without-null/README.md) | bad | Any | A domain with no NULL can never build the table a NULL-sensitive rewrite disagrees on |
| [bad/domain-without-duplicates](bad/domain-without-duplicates/README.md) | bad | Any | A generator that gives every row a distinct value can never build the table a duplicate-sensitive rewrite disagrees on |

## Anti-patterns without a reproduced example yet

`../references/anti-patterns.md` describes these two.

- Comparing two queries' rows as ordered lists instead of as a multiset
- Raising the row bound on one table of a schema and not the others
