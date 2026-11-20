------------------------------ MODULE TokenPassing ------------------------------
(* BROKEN ON PURPOSE. A token moves between a symmetric set of processes.
   Pass hands the token to any other process, so two processes can pass it
   back and forth forever and starve a third. See README.md for what TLC
   1.7.4 does with SYMMETRY declared on a liveness check of this spec. *)
EXTENDS TLC

CONSTANTS Procs

VARIABLES holder

Init == holder \in Procs

Symm == Permutations(Procs)

\* Source: token.py, pass_to(). Hands the token to any other process.
Pass == \E q \in Procs \ {holder} : holder' = q

Next == Pass

Spec == Init /\ [][Next]_holder
FairSpec == Spec /\ WF_holder(Pass)

\* "Every process eventually holds the token."
EveryoneEventuallyHolds == \A p \in Procs : <>(holder = p)
===================================================================================
