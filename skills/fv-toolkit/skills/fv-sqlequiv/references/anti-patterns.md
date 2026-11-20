# Anti-patterns in bounded SQL equivalence checks

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| The generated domain for a column has no `NULL` | A rewrite that only disagrees once a column can hold `NULL` is reported equivalent | Include `NULL` in every column's domain. Reproduced in `examples/bad/domain-without-null/` |
| Each row's value comes from its position (row 0 gets 0, row 1 gets 1, ...) instead of an independent draw from the domain | A rewrite that only disagrees on a table with a repeated value is reported equivalent, because no generated table ever has one | Draw every row from the same small domain independently, so a value can repeat across rows. Reproduced in `examples/bad/domain-without-duplicates/` |
| Comparing two queries' rows as ordered lists instead of as a multiset | A harmless difference in row order, which SQL without `ORDER BY` never promises, is reported as a divergence | Sort both result sets with the same key before comparing, as `fv-sqlequiv`'s `run_query` does |
| The row bound is raised only on the table that already found a counterexample, not on every table the schema declares | A rewrite that needs two tables both to grow past the bound to disagree is never checked at a bound where it would fail | Raise `FV_SQLEQUIV_MAX_ROWS` for every table in the schema, not one at a time |
