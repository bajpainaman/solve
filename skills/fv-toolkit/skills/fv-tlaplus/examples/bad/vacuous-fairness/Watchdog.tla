-------------------------------- MODULE Watchdog --------------------------------
(* BROKEN ON PURPOSE. Escalate is meant to force a stuck job to finish, but
   an earlier refactor removed the only transition that used to set pc to
   "stuck", so Escalate's guard can never be true. See README.md. *)
VARIABLES pc

Init == pc = "waiting"

\* Source: job.py, run(). The normal path to completion.
Advance == pc = "waiting" /\ pc' = "done"

\* Source: watchdog.py, escalate(). Meant to force completion when a job is
\* stuck. Nothing in this module ever sets pc to "stuck" any more, so this
\* guard can never be true.
Escalate == pc = "stuck" /\ pc' = "done"

Finished == pc = "done" /\ UNCHANGED pc

Next == Advance \/ Escalate \/ Finished

Spec == Init /\ [][Next]_pc
\* The fairness the author relies on for EventuallyDone.
FairSpec == Spec /\ WF_pc(Advance) /\ WF_pc(Escalate)
\* BROKEN ON PURPOSE: the same property, with WF_pc(Escalate) removed. If
\* the result is unchanged, that fairness condition was never doing anything.
WithoutEscalateFairness == Spec /\ WF_pc(Advance)

EventuallyDone == <>(pc = "done")
\* "Escalate's guard is never satisfied." Confirmed, not merely assumed.
NeverStuck == pc # "stuck"
===================================================================================
