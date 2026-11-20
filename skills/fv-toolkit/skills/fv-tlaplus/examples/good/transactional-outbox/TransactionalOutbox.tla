---------------------------- MODULE TransactionalOutbox ----------------------------
(* Source read at: 0000000
   Covers: orders/outbox.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   One business change must reach a consumer as one event. The process can
   crash at any step and resumes from whatever it wrote durably. A relay
   reads unmarked outbox rows and publishes them, and it does not remember a
   publish it made before a crash, so it can publish the same row twice.

   The knob Order chooses the design:
     "no_outbox"     the handler publishes to the broker, then commits
     "separate_txn"  the business write commits, then a later write adds the
                      outbox row
     "one_txn"       both writes commit in one database transaction
   ConsumerDedup chooses whether the consumer skips a key it already applied.
   The fault switch MaxCrashes bounds the crashes. Zero switches it off. *)
EXTENDS Naturals

CONSTANTS Order, ConsumerDedup, MaxCrashes

VARIABLES pc, committed, outboxWritten, outboxMarked, delivered, consumed, applied, crashes

vars == <<pc, committed, outboxWritten, outboxMarked, delivered, consumed, applied, crashes>>

Init ==
    /\ pc = "start"
    /\ committed = FALSE
    /\ outboxWritten = FALSE
    /\ outboxMarked = FALSE
    /\ delivered = 0
    /\ consumed = 0
    /\ applied = 0
    /\ crashes = 0

TypeOK ==
    /\ pc \in {"start", "published_pending_commit", "committed_pending_outbox",
               "outbox_written_pending_relay", "published_pending_mark", "done"}
    /\ committed \in BOOLEAN /\ outboxWritten \in BOOLEAN /\ outboxMarked \in BOOLEAN
    /\ delivered \in Nat /\ consumed \in Nat /\ applied \in Nat /\ crashes \in Nat

\* Source: publish_then_commit(), sends to the broker before the local commit.
DirectPublish ==
    /\ Order = "no_outbox" /\ pc = "start" /\ delivered = 0
    /\ delivered' = delivered + 1
    /\ pc' = "published_pending_commit"
    /\ UNCHANGED <<committed, outboxWritten, outboxMarked, consumed, applied, crashes>>

\* Source: publish_then_commit(), the commit after the broker already has it.
CommitAfterPublish ==
    /\ Order = "no_outbox" /\ pc = "published_pending_commit"
    /\ committed' = TRUE
    /\ pc' = "done"
    /\ UNCHANGED <<outboxWritten, outboxMarked, delivered, consumed, applied, crashes>>

\* Source: save_order(), the commit of the business row alone.
CommitBusiness ==
    /\ Order = "separate_txn" /\ pc = "start" /\ ~committed
    /\ committed' = TRUE
    /\ pc' = "committed_pending_outbox"
    /\ UNCHANGED <<outboxWritten, outboxMarked, delivered, consumed, applied, crashes>>

\* Source: write_outbox_row(), a later transaction that adds the outbox row.
WriteOutbox ==
    /\ Order = "separate_txn" /\ pc = "committed_pending_outbox" /\ ~outboxWritten
    /\ outboxWritten' = TRUE
    /\ pc' = "outbox_written_pending_relay"
    /\ UNCHANGED <<committed, outboxMarked, delivered, consumed, applied, crashes>>

\* Source: save_order_with_outbox(), one transaction for both rows.
CommitWithOutbox ==
    /\ Order = "one_txn" /\ pc = "start" /\ ~committed
    /\ committed' = TRUE /\ outboxWritten' = TRUE
    /\ pc' = "outbox_written_pending_relay"
    /\ UNCHANGED <<outboxMarked, delivered, consumed, applied, crashes>>

\* Source: relay.publish(), sends an unmarked row to the broker.
RelayPublish ==
    /\ outboxWritten /\ pc = "outbox_written_pending_relay"
    /\ delivered' = delivered + 1
    /\ pc' = "published_pending_mark"
    /\ UNCHANGED <<committed, outboxWritten, outboxMarked, consumed, applied, crashes>>

\* Source: relay.mark_published(), the write after a successful send.
RelayMark ==
    /\ pc = "published_pending_mark"
    /\ outboxMarked' = TRUE
    /\ pc' = "done"
    /\ UNCHANGED <<committed, outboxWritten, delivered, consumed, applied, crashes>>

\* Source: consumer.handle(), applies the effect unless the key was seen.
Apply ==
    /\ delivered > consumed
    /\ consumed' = consumed + 1
    /\ applied' = IF ConsumerDedup /\ applied >= 1 THEN applied ELSE applied + 1
    /\ UNCHANGED <<pc, committed, outboxWritten, outboxMarked, delivered, crashes>>

\* The point the process resumes at, decided by what it wrote durably.
ResumePoint ==
    IF ~committed THEN "start"
    ELSE IF Order = "no_outbox" THEN "done"
    ELSE IF ~outboxWritten THEN "start"
    ELSE IF ~outboxMarked THEN "outbox_written_pending_relay"
    ELSE "done"

\* Fault: the process crashes and restarts, keeping only durable state.
Crash ==
    /\ crashes < MaxCrashes /\ pc \notin {"start", "done"}
    /\ pc' = ResumePoint
    /\ crashes' = crashes + 1
    /\ UNCHANGED <<committed, outboxWritten, outboxMarked, delivered, consumed, applied>>

\* The end state gets its own action, so deadlock checking stays on.
Done == pc = "done" /\ UNCHANGED vars

Work == DirectPublish \/ CommitAfterPublish \/ CommitBusiness \/ WriteOutbox
         \/ CommitWithOutbox \/ RelayPublish \/ RelayMark \/ Apply
Next == Work \/ Crash \/ Done

Spec == Init /\ [][Next]_vars
\* The process and the consumer keep working while they can. A crash gets no fairness.
FairSpec == Spec /\ WF_vars(Work)

\* "An event never reaches the broker for a change that never committed."
NoEventWithoutCommit == delivered > 0 => committed
\* "The consumer applies the business effect at most once."
AtMostOnceApplied == applied <= 1
\* "A committed change is eventually delivered to the consumer."
EventuallyApplied == committed ~> (applied >= 1)
\* Witness: the relay really can deliver the same row twice.
NeverDuplicateDelivery == delivered <= 1
======================================================================================
