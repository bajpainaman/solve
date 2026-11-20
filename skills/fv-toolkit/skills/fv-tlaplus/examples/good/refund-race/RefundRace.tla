------------------------------ MODULE RefundRace ------------------------------
(* Source read at: 0000000
   Covers: billing/refunds.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A customer paid Paid. Several refund jobs run at once: an agent clicks
   refund while a webhook delivers the same refund, or a retried job runs
   twice. Each job reads how much is still refundable and then refunds that
   amount.

   The knob Atomic chooses the design. FALSE is a read followed by a separate
   write. TRUE is one conditional UPDATE, which is one indivisible step. *)
EXTENDS Integers

CONSTANTS Paid, Jobs, Atomic

VARIABLES refunded, snap, pc

vars == <<refunded, snap, pc>>

Init ==
    /\ refunded = 0
    /\ snap = [j \in Jobs |-> 0]
    /\ pc = [j \in Jobs |-> "check"]

\* Source: refund_job(), the SELECT that reads the refundable amount.
Check(j) ==
    /\ ~Atomic /\ pc[j] = "check"
    /\ snap' = [snap EXCEPT ![j] = Paid - refunded]
    /\ pc' = [pc EXCEPT ![j] = "refund"]
    /\ UNCHANGED refunded

\* Source: refund_job(), the INSERT that issues the refund it read earlier.
Refund(j) ==
    /\ ~Atomic /\ pc[j] = "refund"
    /\ refunded' = refunded + snap[j]
    /\ pc' = [pc EXCEPT ![j] = "done"]
    /\ UNCHANGED snap

\* Source: refund_job_atomic(), one UPDATE ... SET refunded = paid.
AtomicRefund(j) ==
    /\ Atomic /\ pc[j] = "check"
    /\ refunded' = refunded + (Paid - refunded)
    /\ pc' = [pc EXCEPT ![j] = "done"]
    /\ UNCHANGED snap

AllDone == \A j \in Jobs : pc[j] = "done"

\* The end state gets its own action, so deadlock checking stays on and a
\* real stall still shows up as a deadlock.
Done == AllDone /\ UNCHANGED vars

Step(j) == Check(j) \/ Refund(j) \/ AtomicRefund(j)
Next == (\E j \in Jobs : Step(j)) \/ Done

Spec == Init /\ [][Next]_vars
\* A job that can take a step eventually takes it.
FairSpec == Spec /\ \A j \in Jobs : WF_vars(Step(j))

\* "Never refund more than was paid."
NeverOverRefund == refunded <= Paid
\* "Every refund job finishes."
EventuallyDone == <>AllDone
\* Witness: the full refund is reachable. A config that checks this as an
\* invariant must be violated.
NeverFullyRefunded == ~(AllDone /\ refunded = Paid)
===============================================================================
