-- Source read at: 0000000
-- Covers: no real repository; this models catalog C1's SQL rewrite
-- equivalence on two well-known dbt-style rewrites.

-- check: DistinctEqualsGroupBy
-- Equivalent rewrite: DISTINCT and a GROUP BY on the same column collapse
-- NULL into one group the same way SQLite's own DISTINCT does.
-- schema
CREATE TABLE t (x INTEGER);
-- query_a
SELECT DISTINCT x FROM t;
-- query_b
SELECT x FROM t GROUP BY x;

-- check: NotInEqualsNotExists
-- expect: different
-- Rejected rewrite: NOT IN and NOT EXISTS disagree once the subquery's
-- table can hold a NULL, because `x NOT IN (SELECT y FROM t2)` is
-- UNKNOWN, never TRUE, for every row once any y is NULL.
-- schema
CREATE TABLE t1 (x INTEGER);
CREATE TABLE t2 (y INTEGER);
-- query_a
SELECT * FROM t1 WHERE x NOT IN (SELECT y FROM t2);
-- query_b
SELECT * FROM t1 WHERE NOT EXISTS (SELECT 1 FROM t2 WHERE t2.y = t1.x);
