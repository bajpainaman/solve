# A generated domain with no NULL misses the NULL-sensitive rewrite

**Symptom:** the check reports `equivalent`, on the same rewrite that `examples/good/rewrite-equivalence`'s `NotInEqualsNotExists` check finds a counterexample for.

## The bug

`check_without_null.py` draws every column's value from `[1, 2]`:

```python
DOMAIN = [1, 2]  # BUG: should be [1, 2, None], as fv-sqlequiv's DOMAINS use
```

`NOT IN` against a subquery and `NOT EXISTS` only disagree when the subquery's table can hold a `NULL`. A domain with no `NULL` can never build that table, so every table this script generates has both forms agreeing.

## The real output

```text
$ python3 check_without_null.py
PASS check NotInEqualsNotExists: equivalent on 49 tables
```

`examples/good/rewrite-equivalence/rewrites.sql`'s own `NotInEqualsNotExists` check, on the same two queries with `NULL` in its domain, reports the opposite:

```text
PASS check NotInEqualsNotExists: different
  table t1: ((1,),)
  table t2: ((None,),)
```

## The fix

Add `NULL` to every column's domain, as `fv-sqlequiv`'s `DOMAINS` does for every type it knows.

## The check that catches it

None of this project's checks catch it mechanically; nothing here asserts that a generator's domain includes `NULL`. Catching this needs a check written for the generator itself: confirm that at least one generated table, across the whole enumeration, has a `NULL` in each column the schema declares.
