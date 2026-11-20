# Two dbt-style rewrites: one equivalent, one NULL-sensitive

**Pattern:** SQL transform / dbt model rewrite equivalence (catalog C1).
**Teaches:** an `expect:` comment per check, a rejected rewrite that must produce a counterexample table, mutations on both.

## The approach

VeriEQL ([VeriEQL/VeriEQL](https://github.com/VeriEQL/VeriEQL)) is licensed under CC BY-NC-SA 4.0: NonCommercial and ShareAlike. That license does not permit vendoring or wrapping it into this MIT-licensed project. `fv-sqlequiv` is this project's own bounded checker instead: stdlib-only Python and SQLite, enumerating every table up to a small row and value bound, including NULL, and comparing two queries' results on each one.

## The system

One `.sql` file holds one or more `-- check: <Name>` sections, each with its own schema and two queries. `DistinctEqualsGroupBy` is a rewrite SQLite treats the same way. `NotInEqualsNotExists` is the rejected rewrite: `NOT IN` against a subquery that can hold a NULL disagrees with the `NOT EXISTS` form.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| `SELECT DISTINCT x FROM t` and `SELECT x FROM t GROUP BY x` return the same rows on every small table | oracle equivalence | `DistinctEqualsGroupBy` |
| The `NOT IN` and `NOT EXISTS` forms return the same rows on every small table | oracle equivalence | `NotInEqualsNotExists` |

## Commands

| Command | Rewrite | Expectation |
|---|---|---|
| `fv-sqlequiv rewrites.sql` (`DistinctEqualsGroupBy`) | equivalent | equivalent on every generated table |
| `fv-sqlequiv rewrites.sql` (`NotInEqualsNotExists`) | rejected | different; a counterexample table exists |

## Run

```bash
fv-sqlequiv rewrites.sql
fv-mutate rewrites.mutations
```

```text
PASS check DistinctEqualsGroupBy: equivalent on 13 tables
PASS check NotInEqualsNotExists: different
  table t1: ((1,),)
  table t2: ((None,),)
  query_a -> []
  query_b -> [(1,)]
```

```text
DETECTED the group-by rewrite drops the group, so duplicates are no longer collapsed: FAIL check DistinctEqualsGroupBy: expected equivalent, got different
DETECTED the not-in query is accidentally rewritten to the same query_b, hiding the witness: FAIL check NotInEqualsNotExists: expected different, got equivalent on 169 tables
GREEN a check comment is reworded
SUMMARY detected=2 missed=0 error=0 green=1 brittle=0 uncovered=0
```

## The counterexample, as fv-sqlequiv found it

```text
1. t1 holds one row, x = 1. t2 holds one row, y = NULL.
2. query_a asks `1 NOT IN (NULL)`. SQL's three-valued logic makes this UNKNOWN, never TRUE, so query_a excludes the row and returns nothing.
3. query_b asks `NOT EXISTS (SELECT 1 FROM t2 WHERE t2.y = 1)`. No row of t2 has y = 1, so the inner EXISTS is false and NOT EXISTS is true, and query_b returns the row.
```

A second, independent divergence exists even once `t2` cannot hold a NULL: a row of `t1` itself carrying `x = NULL` is excluded by the `NOT IN` form (`NULL NOT IN (...)` is UNKNOWN) and included by the `NOT EXISTS` form (the inner `t2.y = NULL` comparison is UNKNOWN for every row of `t2`, so `EXISTS` is false and `NOT EXISTS` is true). A rewrite that only filters NULLs out of the subquery does not fix this second case.

## Bounds and limits

Each check covers tables with 0 to 2 rows per table (`FV_SQLEQUIV_MAX_ROWS`), with values drawn from `[1, 2, NULL]` per integer column. A pass is exhaustive within that bound, not a proof over arbitrary tables: a larger table, a third distinct value, or a column type this script has no domain for is unchecked.
