----------------------------- MODULE MergedRefund -----------------------------
(* BROKEN ON PURPOSE. The code reads the refundable amount with a SELECT and
   issues the refund with a later INSERT. This model writes both statements as
   one action, so no other job can run between them. *)
EXTENDS Integers

CONSTANTS Paid, Jobs

VARIABLES refunded, pc

vars == <<refunded, pc>>

Init ==
    /\ refunded = 0
    /\ pc = [j \in Jobs |-> "start"]

\* Source: refund_job(), the whole function as one step. This is the error.
RefundJob(j) ==
    /\ pc[j] = "start"
    /\ refunded' = refunded + (Paid - refunded)
    /\ pc' = [pc EXCEPT ![j] = "done"]

Done == (\A j \in Jobs : pc[j] = "done") /\ UNCHANGED vars

Next == (\E j \in Jobs : RefundJob(j)) \/ Done

Spec == Init /\ [][Next]_vars

NeverOverRefund == refunded <= Paid
===============================================================================
