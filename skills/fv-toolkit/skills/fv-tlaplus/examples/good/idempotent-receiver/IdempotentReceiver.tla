--------------------------- MODULE IdempotentReceiver ---------------------------
(* Source read at: 0000000
   Covers: consumers/handler.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A broker delivers one message at least once. The consumer applies a
   business effect and records the message id, so that a redelivery is
   skipped. The consumer can crash at any step. A crash loses the program
   counter and keeps the durable state.

   The knob Order chooses the design:
     "effect_first"  the effect is written, then the dedup record
     "record_first"  the dedup record is written, then the effect
     "one_txn"       both writes commit in one database transaction
   The fault switch MaxCrashes bounds the crashes. Zero switches the fault off. *)
EXTENDS Naturals

CONSTANTS Order, MaxCrashes

VARIABLES inQueue, effects, seen, pc, crashes

vars == <<inQueue, effects, seen, pc, crashes>>

Init ==
    /\ inQueue = TRUE
    /\ effects = 0
    /\ seen = FALSE
    /\ pc = "idle"
    /\ crashes = 0

\* Source: consumer.poll(). The broker redelivers until the message is acked.
Receive ==
    /\ pc = "idle" /\ inQueue
    /\ pc' = IF seen THEN "ack" ELSE "first"
    /\ UNCHANGED <<inQueue, effects, seen, crashes>>

\* Source: handler.apply(), the write of the business effect.
ApplyEffect ==
    /\ \/ Order = "effect_first" /\ pc = "first" /\ pc' = "second"
       \/ Order = "record_first" /\ pc = "second" /\ pc' = "ack"
    /\ effects' = effects + 1
    /\ UNCHANGED <<inQueue, seen, crashes>>

\* Source: handler.mark_seen(), the write of the dedup record.
RecordSeen ==
    /\ \/ Order = "record_first" /\ pc = "first" /\ pc' = "second"
       \/ Order = "effect_first" /\ pc = "second" /\ pc' = "ack"
    /\ seen' = TRUE
    /\ UNCHANGED <<inQueue, effects, crashes>>

\* Source: handler.apply_and_mark(), both writes in one transaction.
ApplyAndRecord ==
    /\ Order = "one_txn" /\ pc = "first"
    /\ effects' = effects + 1 /\ seen' = TRUE /\ pc' = "ack"
    /\ UNCHANGED <<inQueue, crashes>>

\* Source: consumer.ack().
Ack ==
    /\ pc = "ack"
    /\ inQueue' = FALSE /\ pc' = "idle"
    /\ UNCHANGED <<effects, seen, crashes>>

\* Fault: the consumer crashes and restarts.
Crash ==
    /\ crashes < MaxCrashes /\ pc # "idle"
    /\ pc' = "idle" /\ crashes' = crashes + 1
    /\ UNCHANGED <<inQueue, effects, seen>>

\* The end state gets its own action, so deadlock checking stays on.
Done == ~inQueue /\ pc = "idle" /\ UNCHANGED vars

Work == Receive \/ ApplyEffect \/ RecordSeen \/ ApplyAndRecord \/ Ack
Next == Work \/ Crash \/ Done

Spec == Init /\ [][Next]_vars
\* The consumer keeps working while it can. A crash gets no fairness.
FairSpec == Spec /\ WF_vars(Work)

\* "The effect is applied at most once, despite redelivery."
AtMostOnce == effects <= 1
\* "A message that left the queue had its effect applied."
AckedImpliesApplied == ~inQueue => effects = 1
\* "The message is eventually acked."
EventuallyAcked == <>(~inQueue)
\* Witness: a run that crashes still reaches the ack.
NeverAckedAfterCrash == ~(~inQueue /\ crashes > 0)
=================================================================================
