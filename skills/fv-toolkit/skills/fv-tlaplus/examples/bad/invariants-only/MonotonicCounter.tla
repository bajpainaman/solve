------------------------------ MODULE MonotonicCounter ------------------------------
(* BROKEN ON PURPOSE. The design says a view count only ever climbs, but
   Next also allows a step that lowers it, and the one invariant this model
   checks cannot see that. See README.md. *)
EXTENDS Naturals

CONSTANTS Max

VARIABLES x

Init == x = 0

\* Source: counter.py, increment(). Bounded here only to keep the search
\* finite; the design's own limit is unrelated to this check.
Increment == x < Max /\ x' = x + 1

\* Source: counter.py, decrement(). The design forbids calling this in
\* production, but a retried rollback can still reach it.
Decrement == x > 0 /\ x' = x - 1

Next == Increment \/ Decrement

Spec == Init /\ [][Next]_x

\* The invariant this model checks. It says nothing about which direction x
\* moves, so Decrement never breaks it.
NonNegative == x >= 0

\* "The view count only ever climbs." A relation between consecutive states,
\* which an INVARIANT cannot express.
Monotonic == [][x' >= x]_x
=======================================================================================
