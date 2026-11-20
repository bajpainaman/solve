---------------------------- MODULE CdcSnapshotHandoff ----------------------------
(* Source read at: 0000000
   Covers: cdc/connector.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A source table takes three changes, c1 through c3, in order. A connector
   takes a snapshot that always reflects c1, then streams the rest of the
   log starting at the position it noted at snapshot time. The same
   redetermination happens again on any restart mid-stream, so the same
   race applies there too.

   The knob Order chooses the design:
     "wrong_offset"    the position is noted by a separate read that can
                        land early or late
     "correct_offset"  the position is noted in the same step as the
                        snapshot, so it always lands on c2
   The fault switch RaceWindow lets the noted position land anywhere in
   the race window. FALSE switches it off: even the wrong-offset design
   always happens to land on c2. *)
EXTENDS Naturals

CONSTANTS Order, RaceWindow

VARIABLES snapshotTaken, noted, streamed, applied

vars == <<snapshotTaken, noted, streamed, applied>>

Init ==
    /\ snapshotTaken = FALSE
    /\ noted = 0
    /\ streamed = 0
    /\ applied = [c \in 1..3 |-> 0]

TypeOK ==
    /\ snapshotTaken \in BOOLEAN /\ noted \in 0..3 /\ streamed \in 0..3
    /\ applied \in [1..3 -> Nat]

NotedChoices == IF RaceWindow THEN {1, 2, 3} ELSE {2}

\* Source: connector.snapshot(), applying c1 and noting where to stream from
\* in the same step as the snapshot itself.
TakeSnapshotCorrect ==
    /\ Order = "correct_offset" /\ ~snapshotTaken
    /\ snapshotTaken' = TRUE /\ noted' = 2
    /\ applied' = [applied EXCEPT ![1] = @ + 1]
    /\ UNCHANGED streamed

\* Source: connector.snapshot(), noting where to stream from with a
\* separate read that can land on either side of the true boundary.
TakeSnapshotWrong(n) ==
    /\ Order = "wrong_offset" /\ ~snapshotTaken /\ n \in NotedChoices
    /\ snapshotTaken' = TRUE /\ noted' = n
    /\ applied' = [applied EXCEPT ![1] = @ + 1]
    /\ UNCHANGED streamed

NextPos == IF streamed = 0 THEN noted ELSE streamed + 1

\* Source: connector.stream_next(), applying the next change in the log.
\* A restart mid-stream redetermines this same position the same way the
\* initial handoff did, so it is not modeled as a separate action.
StreamNext ==
    /\ snapshotTaken /\ NextPos <= 3
    /\ streamed' = NextPos
    /\ applied' = [applied EXCEPT ![NextPos] = @ + 1]
    /\ UNCHANGED <<snapshotTaken, noted>>

\* The end state gets its own action, so deadlock checking stays on.
Done == snapshotTaken /\ streamed = 3 /\ UNCHANGED vars

Work == TakeSnapshotCorrect \/ (\E n \in 1..3 : TakeSnapshotWrong(n)) \/ StreamNext
Next == Work \/ Done

Spec == Init /\ [][Next]_vars
\* The connector keeps working while it can.
FairSpec == Spec /\ WF_vars(Work)

\* "Once the stream finishes, every change has landed downstream exactly once."
ExactlyOnce == streamed = 3 => \A c \in 1..3 : applied[c] = 1
\* "Downstream eventually equals the source."
EventuallyCaughtUp == <>(streamed = 3)
\* Witness: the handoff really does finish.
NeverFinishes == ~(snapshotTaken /\ streamed = 3)
=====================================================================================
