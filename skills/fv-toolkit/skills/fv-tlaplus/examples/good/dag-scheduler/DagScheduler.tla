---------------------------- MODULE DagScheduler ----------------------------
(* Source read at: 0000000
   Covers: orchestration/scheduler.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   Task B depends on task A. The scheduler can crash after it marks A
   running but before it marks A done, so it does not know whether A's own
   work already happened.

   The knob Order chooses the design:
     "naive"    a restart always resumes A as running, and B starts once
                A has merely started
     "checked"  a restart checks whether A's work already happened before
                deciding, and B starts only once A is done
   The fault switch MaxCrashes bounds how many times the scheduler
   crashes. Zero switches it off, so a crash never happens. *)
EXTENDS Naturals

CONSTANTS Order, MaxCrashes

VARIABLES statusA, statusB, effectA, effectB, crashed, crashes

vars == <<statusA, statusB, effectA, effectB, crashed, crashes>>

Init ==
    /\ statusA = "pending"
    /\ statusB = "pending"
    /\ effectA = 0
    /\ effectB = 0
    /\ crashed = FALSE
    /\ crashes = 0

TypeOK ==
    /\ statusA \in {"pending", "running", "executed", "done"}
    /\ statusB \in {"pending", "done"}
    /\ effectA \in Nat /\ effectB \in Nat
    /\ crashed \in BOOLEAN /\ crashes \in Nat

\* Source: scheduler.dispatch(a), marking A running before it launches.
MarkRunningA ==
    /\ statusA = "pending"
    /\ statusA' = "running"
    /\ UNCHANGED <<statusB, effectA, effectB, crashed, crashes>>

\* Source: worker.run(a), the task's own side effect. It can happen even
\* while the scheduler shows crashed, because the worker is a separate
\* process the scheduler does not control once dispatched.
ExecuteA ==
    /\ statusA = "running"
    /\ statusA' = "executed" /\ effectA' = effectA + 1
    /\ UNCHANGED <<statusB, effectB, crashed, crashes>>

\* Source: scheduler.on_worker_done(a), the normal path once not crashed.
MarkDoneA ==
    /\ statusA = "executed" /\ ~crashed
    /\ statusA' = "done"
    /\ UNCHANGED <<statusB, effectA, effectB, crashed, crashes>>

\* Fault: the scheduler crashes before it learns whether A's work ran.
Crash ==
    /\ ~crashed /\ statusA \in {"running", "executed"} /\ crashes < MaxCrashes
    /\ crashed' = TRUE /\ crashes' = crashes + 1
    /\ UNCHANGED <<statusA, statusB, effectA, effectB>>

\* Source: scheduler.on_restart(a), which always assumes the worst.
RestartNaive ==
    /\ Order = "naive" /\ crashed
    /\ crashed' = FALSE /\ statusA' = "running"
    /\ UNCHANGED <<statusB, effectA, effectB, crashes>>

\* Source: scheduler.on_restart(a), which checks the durable effect count
\* before deciding whether the work still needs to run.
RestartChecked ==
    /\ Order = "checked" /\ crashed
    /\ crashed' = FALSE
    /\ statusA' = IF effectA > 0 THEN "executed" ELSE "running"
    /\ UNCHANGED <<statusB, effectA, effectB, crashes>>

\* "Naive" treats A as ready once it has merely started; "checked" waits
\* for it to be fully done.
ADependencyMet == IF Order = "checked" THEN statusA = "done" ELSE statusA # "pending"

\* Source: scheduler.dispatch(b), gated on A's dependency check.
RunB ==
    /\ statusB = "pending" /\ ADependencyMet
    /\ statusB' = "done" /\ effectB' = effectB + 1
    /\ UNCHANGED <<statusA, effectA, crashed, crashes>>

\* The end state gets its own action, so deadlock checking stays on.
Done == statusA = "done" /\ statusB = "done" /\ UNCHANGED vars

Work == MarkRunningA \/ ExecuteA \/ MarkDoneA \/ RestartNaive \/ RestartChecked \/ RunB
Next == Work \/ Crash \/ Done

Spec == Init /\ [][Next]_vars
\* The scheduler and the worker keep working while they can.
FairSpec == Spec /\ WF_vars(Work)

\* "A's side effect never runs more than once."
NeverRunsTwice == effectA <= 1
\* "B never runs while A is only partly done."
NeverRunsOnPartialUpstream == effectB > 0 => statusA = "done"
\* "Both tasks eventually finish."
EventuallyBothDone == <>(statusA = "done" /\ statusB = "done")
\* Witness: both tasks really do finish.
NeverBothDone == ~(statusA = "done" /\ statusB = "done")
===============================================================================
