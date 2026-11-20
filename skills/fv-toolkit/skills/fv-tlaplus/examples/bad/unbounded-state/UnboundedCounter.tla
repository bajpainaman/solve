-------------------------------- MODULE UnboundedCounter --------------------------------
(* BROKEN ON PURPOSE. Nothing bounds x, so the reachable state space is
   infinite and TLC never finishes checking it. See README.md. *)
EXTENDS Naturals

CONSTANTS Max

VARIABLES x

\* Source: counter.py, increment(). Called with no limit on how high x goes.
Init == x = 0
Next == x' = x + 1

Spec == Init /\ [][Next]_x

NeverNegative == x >= 0
\* A CONSTRAINT that keeps the search finite. It is not part of the design,
\* only of the search bound, so the report must name what it excludes.
Bounded == x <= Max
===========================================================================================
