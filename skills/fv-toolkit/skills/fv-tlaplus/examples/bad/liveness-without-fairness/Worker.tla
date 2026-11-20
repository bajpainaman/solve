-------------------------------- MODULE Worker --------------------------------
(* A worker takes a queued job and finishes it. The liveness property says
   that a queued job is eventually finished. *)
VARIABLE state

Init == state = "queued"

Take == state = "queued" /\ state' = "running"
Finish == state = "running" /\ state' = "finished"
Done == state = "finished" /\ UNCHANGED state

Next == Take \/ Finish \/ Done

\* BROKEN ON PURPOSE: no fairness. The worker may stop at any state for ever.
Spec == Init /\ [][Next]_state
\* The fix: a step that stays possible is eventually taken.
FairSpec == Spec /\ WF_state(Take) /\ WF_state(Finish)

QueuedLeadsToFinished == (state = "queued") ~> (state = "finished")
===============================================================================
