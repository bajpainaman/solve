#!/usr/bin/env python3
"""Broken on purpose: every generated row gets a value no other row in the
same table can have, so no generated table ever has a duplicate.

Source read at: 0000000
Covers: no real repository.

Checks plain `x` against `DISTINCT x`, a rewrite that only disagrees when a
table has two rows with the same x.
"""
import itertools
import sqlite3

MAX_ROWS = 2

SCHEMA = "CREATE TABLE t (x INTEGER);"
QUERY_A = "SELECT x FROM t;"
QUERY_B = "SELECT DISTINCT x FROM t;"


def instances():
    # BUG: row i always gets the value i, so two rows in the same table are
    # never equal. fv-sqlequiv instead draws every row from the same small
    # domain, so a value can repeat across rows.
    for count in range(MAX_ROWS + 1):
        yield tuple((i,) for i in range(count))


def main():
    total = 0
    for rows in instances():
        total += 1
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA)
        conn.executemany("INSERT INTO t VALUES (?)", rows)
        rows_a = sorted(conn.execute(QUERY_A))
        rows_b = sorted(conn.execute(QUERY_B))
        conn.close()
        if rows_a != rows_b:
            print(f"FAIL check XEqualsDistinctX: expected equivalent, got different on t={rows}")
            return 1
    print(f"PASS check XEqualsDistinctX: equivalent on {total} tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
