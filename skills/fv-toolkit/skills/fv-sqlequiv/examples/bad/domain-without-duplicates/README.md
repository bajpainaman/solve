# A generator that never repeats a value misses a duplicate-sensitive rewrite

**Symptom:** the check reports `equivalent` on `SELECT x FROM t` versus `SELECT DISTINCT x FROM t`, a pair that disagrees on any table with a repeated value.

## The bug

`check_without_duplicates.py` gives each row in a table its own position as the value:

```python
def instances():
    # BUG: row i always gets the value i, so two rows in the same table are
    # never equal. fv-sqlequiv instead draws every row from the same small
    # domain, so a value can repeat across rows.
    for count in range(MAX_ROWS + 1):
        yield tuple((i,) for i in range(count))
```

A two-row table is always `((0,), (1,))`, never `((1,), (1,))`. `x` and `DISTINCT x` only disagree when a table holds two rows with the same value, and this generator can never build one.

## The real output

```text
$ python3 check_without_duplicates.py
PASS check XEqualsDistinctX: equivalent on 3 tables
```

The same pair, checked with `fv-sqlequiv`'s own generator (which draws every row from the same small domain, so a value can repeat), finds the counterexample:

```text
$ fv-sqlequiv /tmp/dup_check.sql
PASS check XEqualsDistinctX: different
  table t: ((1,), (1,))
  query_a -> [(1,), (1,)]
  query_b -> [(1,)]
```

## The fix

Draw every row from the same small domain independently, as `fv-sqlequiv`'s `table_instances` does with `itertools.product(possible_rows, repeat=row_count)`, instead of deriving each row's value from its position.

## The check that catches it

None of this project's checks catch it mechanically; nothing here asserts that a generator can produce a duplicate. Catching this needs a check written for the generator itself: confirm that at least one generated table, across the whole enumeration, has two rows with the same value in every column the schema declares.
