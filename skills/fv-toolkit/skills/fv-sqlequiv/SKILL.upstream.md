---
name: fv-sqlequiv
description: "Checks two SQL queries for equivalence on every small table up to a bound, with a stdlib-only Python and SQLite checker. Covers SQL rewrites and dbt model refactors: does the new query return the same rows as the old one, including on tables with NULLs and duplicate values. Not VeriEQL itself; that tool is CC BY-NC-SA licensed, so this skill is this project's own bounded checker. Use for SQL rewrite safety, dbt refactor PRs, \"is this query the same as that one\", or when the formal-verification skill routes here. Not for a query's performance, or for correctness beyond the row and value bound this skill states."
---

# Bounded SQL equivalence on SQLite

`fv-sqlequiv` builds every small table a schema allows, up to a row and value bound that always includes NULL and allows duplicate values, and compares what two queries return on each one. A pass means the queries agree on every table up to that bound; a divergence comes with the smallest table the generator found it on.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

## Which approach this skill uses

[VeriEQL](https://github.com/VeriEQL/VeriEQL) is a research tool for SQL query equivalence, licensed CC BY-NC-SA 4.0. That license's NonCommercial and ShareAlike terms do not permit vendoring or wrapping it into this MIT-licensed project, so this skill does not use it. `fv-sqlequiv` is this project's own stdlib-only checker: exhaustive enumeration of small tables against SQLite, not a decision procedure over symbolic tables. It cannot cover a table larger than the bound, a value outside the small domain it generates, or a SQL feature SQLite does not implement.

## Five rules

1. **The generated domain for every column must include NULL.** A rewrite that only disagrees once a column can hold NULL is reported equivalent otherwise. `examples/bad/domain-without-null/` reproduces this.
2. **Rows must be drawn independently from the domain, so a value can repeat.** A generator that gives each row a distinct value can never build the table a duplicate-sensitive rewrite disagrees on. `examples/bad/domain-without-duplicates/` reproduces this.
3. **Compare rows as a multiset, not an ordered list.** SQL without `ORDER BY` makes no promise about row order; comparing position by position reports a harmless reordering as a divergence.
4. **State the bound in the report.** A pass is exhaustive within the row count and value domain used, not a proof over every table; say both numbers.
5. **Every mutation must fail on a planted bug.** Write a `.mutations` file beside the SQL and run `fv-mutate`. A check that stays green on every planted bug checks nothing.

## Files to write

| File | Holds |
|---|---|
| `<name>.sql` | One or more `-- check: <Name>` sections, each with `-- expect:` (default `equivalent`), `-- schema`, `-- query_a`, `-- query_b`. Its header comment carries `Source read at:` and `Covers:` |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the counterexample and the bounds |

Copy `examples/good/rewrite-equivalence/` to start.

## Workflow

1. **Write the schema and both queries as one check**, with no `-- expect:` line if you expect them equivalent.
2. **Run it.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-sqlequiv <name>.sql
   ```
3. **If the rewrite is rejected on purpose, add `-- expect: different`** above that check, and confirm it finds a counterexample.
4. **Read the counterexample back into the real query**, following `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md`: does the real table ever hold the values the counterexample shows.
5. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

## Reading the output

| Line | Meaning |
|---|---|
| `PASS check <Name>: equivalent on N tables` | The two queries agreed on every one of the N generated tables |
| `PASS check <Name>: different` | The check declared `-- expect: different`, and a counterexample table was found |
| `FAIL check <Name>: expected <outcome>, got <outcome>` | The real outcome does not match the `-- expect:` line |

## What a pass means

A pass is exhaustive within the stated bound: every table with 0 to `FV_SQLEQUIV_MAX_ROWS` rows per table, built from each column's small domain (`[1, 2, NULL]` for an integer column, `['a', 'b', NULL]` for a text column). It is not a proof for a table outside that bound.

## Telling a counterexample

Name the table and the row each query produced, then the rule that explains the gap:

```text
1. t1 holds one row, x = 1. t2 holds one row, y = NULL.
2. query_a asks `1 NOT IN (NULL)`. Three-valued logic makes this UNKNOWN, never TRUE, so query_a returns nothing.
3. query_b asks whether any row of t2 has y = 1. None does, so query_b returns the row.
```

## Examples

`examples/INDEX.md` lists every example. `examples/good/rewrite-equivalence/` is the complete pattern: an equivalent rewrite checked beside a rejected one, with mutations for each. `examples/bad/` holds two generators whose checks pass while they prove nothing.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a check, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
