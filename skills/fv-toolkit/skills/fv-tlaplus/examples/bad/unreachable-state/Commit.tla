-------------------------------- MODULE Commit --------------------------------
(* A coordinator commits when every participant has voted yes. *)
EXTENDS Naturals, FiniteSets

CONSTANT Participants

VARIABLES votes, committed

vars == <<votes, committed>>

Init == votes = {} /\ committed = FALSE

Vote(p) == p \notin votes /\ votes' = votes \cup {p} /\ UNCHANGED committed

\* BROKEN ON PURPOSE: the guard asks for more votes than there are participants.
Commit ==
    /\ ~committed
    /\ Cardinality(votes) > Cardinality(Participants)
    /\ committed' = TRUE
    /\ UNCHANGED votes

Done == Cardinality(votes) = Cardinality(Participants) /\ UNCHANGED vars

Next == (\E p \in Participants : Vote(p)) \/ Commit \/ Done

Spec == Init /\ [][Next]_vars

\* "A commit happens only after every participant voted."
CommitNeedsAllVotes == committed => votes = Participants
\* Witness: a commit is reachable. A config that checks this must be violated.
NeverCommitted == ~committed
===============================================================================
