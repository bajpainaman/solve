-------------------------------- MODULE Lease --------------------------------
(* Source read at: 0000000
   Covers: locking/lease.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   The same lease slot as ../../good/lease-induction/. WeakInv is the
   invariant someone writes first: "the count is 0 or 1". It is true, and
   TLC confirms it by exploring every state reachable from Init. It is not
   inductive: an arbitrary state that satisfies WeakInv but was never
   reached, such as leases = 1 with phase = "idle", lets Acquire run again,
   because WeakInv says nothing about phase. *)
EXTENDS Integers

VARIABLES
    \* @type: Int;
    leases,
    \* @type: Str;
    phase

Acquire ==
    /\ phase = "idle"
    /\ leases' = leases + 1
    /\ phase' = "held"

Release ==
    /\ phase = "held"
    /\ leases' = leases - 1
    /\ phase' = "idle"

Init == leases = 0 /\ phase = "idle"
Next == Acquire \/ Release
Spec == Init /\ [][Next]_<<leases, phase>>

\* True of every reachable state. Not inductive on its own.
WeakInv == leases \in {0, 1} /\ phase \in {"idle", "held"}
===============================================================================
