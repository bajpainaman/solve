#!/usr/bin/env python3
"""Broken on purpose: the generated domain never includes NULL.

Source read at: 0000000
Covers: no real repository.

The same NOT IN vs NOT EXISTS rewrite that
examples/good/rewrite-equivalence/rewrites.sql's NotInEqualsNotExists check
finds a counterexample for. Here the per-column domain is [1, 2], with no
NULL, so no generated t2 can ever expose the one case where the two
queries disagree.
"""
import itertools
import sqlite3

DOMAIN = [1, 2]  # BUG: should be [1, 2, None], as fv-sqlequiv's DOMAINS use
MAX_ROWS = 2

SCHEMA = "CREATE TABLE t1 (x INTEGER); CREATE TABLE t2 (y INTEGER);"
QUERY_A = "SELECT * FROM t1 WHERE x NOT IN (SELECT y FROM t2);"
QUERY_B = "SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t2.y = t1.x);"


def instances():
    rows = [(v,) for v in DOMAIN]
    for count in range(MAX_ROWS + 1):
        yield from itertools.product(rows, repeat=count)


def main():
    total = 0
    for t1_rows, t2_rows in itertools.product(instances(), instances()):
        total += 1
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA)
        conn.executemany("INSERT INTO t1 VALUES (?)", t1_rows)
        conn.executemany("INSERT INTO t2 VALUES (?)", t2_rows)
        rows_a = sorted(conn.execute(QUERY_A))
        rows_b = sorted(conn.execute(QUERY_B))
        conn.close()
        if rows_a != rows_b:
            print(f"FAIL check NotInEqualsNotExists: expected equivalent, got different "
                  f"on t1={t1_rows} t2={t2_rows}")
            return 1
    print(f"PASS check NotInEqualsNotExists: equivalent on {total} tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
