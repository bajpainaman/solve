---------------------------- MODULE SagaOrchestrated ----------------------------
(* Source read at: 0000000
   Covers: orders/saga.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   An orchestrator runs one saga step at a participant: hold inventory for an
   order. The request can be retried once before any answer comes back, and
   the request can sit in flight past the orchestrator's own timeout, because
   the participant or the network is slow. On a timeout the orchestrator
   decides whether to compensate.

   The knob Order chooses the design:
     "blind_compensate"     always compensates on timeout, and never stops a
                             request that is still in flight
     "confirmed_compensate" compensates only when the effect already landed,
                             and fences out any request still in flight at
                             that moment, so it can never land afterward
   The fault switch AllowLateApply lets the timeout fire while the request is
   still in flight. FALSE switches it off: the orchestrator only times out
   once the request has already resolved, one way or the other. *)
EXTENDS Naturals

CONSTANTS Order, AllowLateApply

VARIABLES pc, inFlight, attempts, effectB, fenced, compensated, effectAtSettle

vars == <<pc, inFlight, attempts, effectB, fenced, compensated, effectAtSettle>>

Init ==
    /\ pc = "begin"
    /\ inFlight = 0
    /\ attempts = 0
    /\ effectB = FALSE
    /\ fenced = FALSE
    /\ compensated = FALSE
    /\ effectAtSettle = FALSE

TypeOK ==
    /\ pc \in {"begin", "b_inflight", "timed_out", "committed", "aborted"}
    /\ inFlight \in 0..2 /\ attempts \in 0..2
    /\ effectB \in BOOLEAN /\ fenced \in BOOLEAN
    /\ compensated \in BOOLEAN /\ effectAtSettle \in BOOLEAN

\* Source: orchestrator.hold_inventory(), the first send of the request.
IssueB ==
    /\ pc = "begin"
    /\ inFlight' = 1 /\ attempts' = 1
    /\ pc' = "b_inflight"
    /\ UNCHANGED <<effectB, fenced, compensated, effectAtSettle>>

\* Source: orchestrator.retry_once(), one retried send of the same request,
\* while the orchestrator is still waiting on the first answer.
Retry ==
    /\ attempts < 2 /\ pc = "b_inflight"
    /\ inFlight' = inFlight + 1 /\ attempts' = attempts + 1
    /\ UNCHANGED <<pc, effectB, fenced, compensated, effectAtSettle>>

\* Source: participant.hold(), the effect lands unless the request is fenced.
ApplyOne ==
    /\ inFlight > 0 /\ ~fenced
    /\ inFlight' = inFlight - 1 /\ effectB' = TRUE
    /\ UNCHANGED <<pc, attempts, fenced, compensated, effectAtSettle>>

\* Source: a dropped or a fenced-and-rejected delivery of one attempt.
LoseOne ==
    /\ inFlight > 0
    /\ inFlight' = inFlight - 1
    /\ UNCHANGED <<pc, attempts, effectB, fenced, compensated, effectAtSettle>>

\* Source: orchestrator.on_hold_ack(), the request answered before any timeout.
Ack ==
    /\ pc = "b_inflight" /\ effectB
    /\ pc' = "committed"
    /\ UNCHANGED <<inFlight, attempts, effectB, fenced, compensated, effectAtSettle>>

\* Source: orchestrator.on_timeout(). The fault lets this fire while a
\* request is still in flight; off, it waits for every attempt to resolve.
Timeout ==
    /\ pc = "b_inflight" /\ (AllowLateApply \/ inFlight = 0)
    /\ pc' = "timed_out"
    /\ UNCHANGED <<inFlight, attempts, effectB, fenced, compensated, effectAtSettle>>

\* Source: orchestrator.compensate(), fires on every timeout, fences nothing.
Compensate ==
    /\ Order = "blind_compensate" /\ pc = "timed_out"
    /\ compensated' = TRUE /\ effectAtSettle' = effectB
    /\ pc' = "aborted"
    /\ UNCHANGED <<inFlight, attempts, effectB, fenced>>

\* Source: orchestrator.confirm_and_settle(), checks the effect and fences
\* the step before deciding, so no later attempt can still land.
ConfirmAndSettle ==
    /\ Order = "confirmed_compensate" /\ pc = "timed_out"
    /\ fenced' = TRUE
    /\ compensated' = effectB
    /\ effectAtSettle' = effectB
    /\ pc' = "aborted"
    /\ UNCHANGED <<inFlight, attempts, effectB>>

\* The end states get their own action, so deadlock checking stays on.
Done == pc \in {"committed", "aborted"} /\ UNCHANGED vars

Work == IssueB \/ Retry \/ ApplyOne \/ LoseOne \/ Ack \/ Timeout \/ Compensate \/ ConfirmAndSettle
Next == Work \/ Done

Spec == Init /\ [][Next]_vars
\* The orchestrator and the participant keep working while they can.
FairSpec == Spec /\ WF_vars(Work)

\* "Compensation never runs for a step whose effect never landed."
CompensateImpliesRan == compensated => effectB
\* "Once the saga settles, nothing it already decided changes underneath it."
SettledEffectIsFinal == pc = "aborted" => effectB = effectAtSettle
\* "Every saga ends committed or aborted."
EventuallyDone == <>(pc \in {"committed", "aborted"})
\* Witness: an abort can skip compensation, because the step never ran.
NeverSkipsCompensation == ~(pc = "aborted" /\ ~compensated)
===================================================================================
