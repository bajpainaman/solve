------------------------------ MODULE TurnBasedWorker ------------------------------
(* BROKEN ON PURPOSE. A task runs only on "its" turn. An external scheduler
   flips the turn at any time. The task's turn recurs infinitely often but is
   never held continuously, which is exactly the gap between weak and strong
   fairness. See README.md. *)
VARIABLES turn, done

vars == <<turn, done>>

Init == turn \in {"self", "other"} /\ done = FALSE

\* An external scheduler, such as another higher-priority task, that may
\* take the turn away at any point.
Tick == turn' = (IF turn = "self" THEN "other" ELSE "self") /\ UNCHANGED done

\* Source: worker.run_my_turn(). Only runs while it holds the turn.
Act == turn = "self" /\ done' = TRUE /\ UNCHANGED turn

Done == done /\ UNCHANGED vars

Next == Tick \/ Act \/ Done

Spec == Init /\ [][Next]_vars
\* BROKEN ON PURPOSE: weak fairness never forces Act, because Act's enabled
\* window never becomes continuous. It flickers on and off forever as Tick
\* keeps taking the turn away right after it returns.
WeaklyFairSpec == Spec /\ WF_vars(Tick) /\ WF_vars(Act)
\* The fix: strong fairness forces an action that recurs infinitely often,
\* even without ever holding a continuous window.
StronglyFairSpec == Spec /\ WF_vars(Tick) /\ SF_vars(Act)

EventuallyDone == <>done
=====================================================================================
