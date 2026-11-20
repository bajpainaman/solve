---------------------------- MODULE WatermarkCursor ----------------------------
(* Source read at: 0000000
   Covers: etl/incremental_load.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   Two runs load rows by commit time against a cursor. Row r1 commits at 1,
   row r2 commits at 2, and row rl also commits at 2 but its transaction is
   slow: it can become visible at any point, including after the first run
   has already moved the cursor past 2.

   The knob Order chooses the design:
     "gt_no_dedup"    the query uses commit_time > cursor, and every match
                       is counted again
     "gte_no_dedup"   the query uses commit_time >= cursor, and every
                       match is counted again
     "gte_with_dedup" the query uses commit_time >= cursor, and a row
                       already loaded is never counted twice
   The fault switch SlowCommit lets rl's commit land after the first run.
   FALSE switches it off: rl is always visible from the start. *)
EXTENDS Naturals

CONSTANTS Order, SlowCommit

Rows == {"r1", "r2", "rl"}
CT == [r1 |-> 1, r2 |-> 2, rl |-> 2]

VARIABLES visible, cursor, loadedIds, loadedCount, ran1, ran2

vars == <<visible, cursor, loadedIds, loadedCount, ran1, ran2>>

Init ==
    /\ visible = [r1 |-> TRUE, r2 |-> TRUE, rl |-> ~SlowCommit]
    /\ cursor = 0
    /\ loadedIds = {}
    /\ loadedCount = [r \in Rows |-> 0]
    /\ ran1 = FALSE
    /\ ran2 = FALSE

TypeOK ==
    /\ visible \in [Rows -> BOOLEAN] /\ cursor \in Nat
    /\ loadedIds \subseteq Rows /\ loadedCount \in [Rows -> Nat]
    /\ ran1 \in BOOLEAN /\ ran2 \in BOOLEAN

UsesGte == Order \in {"gte_no_dedup", "gte_with_dedup"}
Matches(r) == IF UsesGte THEN CT[r] >= cursor ELSE CT[r] > cursor
MaxOf(T) == CHOOSE m \in T : \A x \in T : x <= m

\* Fault: rl's slow transaction commits and becomes visible, at any point
\* up to and including the second run.
CommitLate ==
    /\ SlowCommit /\ ~visible["rl"] /\ ~ran2
    /\ visible' = [visible EXCEPT !["rl"] = TRUE]
    /\ UNCHANGED <<cursor, loadedIds, loadedCount, ran1, ran2>>

\* Source: loader.run(), one pass of the incremental query and cursor move.
RunLoad ==
    LET matched == {r \in Rows : visible[r] /\ Matches(r)}
        toCount == {r \in matched : Order # "gte_with_dedup" \/ r \notin loadedIds}
    IN  /\ cursor' = IF matched = {} THEN cursor ELSE MaxOf({CT[r] : r \in matched})
        /\ loadedIds' = loadedIds \cup matched
        /\ loadedCount' = [r \in Rows |-> IF r \in toCount THEN loadedCount[r] + 1 ELSE loadedCount[r]]
        /\ UNCHANGED visible

Run1 ==
    /\ ~ran1
    /\ RunLoad
    /\ ran1' = TRUE /\ UNCHANGED ran2

Run2 ==
    /\ ran1 /\ ~ran2
    /\ RunLoad
    /\ ran2' = TRUE /\ UNCHANGED ran1

\* The end state gets its own action, so deadlock checking stays on.
Done == ran1 /\ ran2 /\ UNCHANGED vars

Work == CommitLate \/ Run1 \/ Run2
Next == Work \/ Done

Spec == Init /\ [][Next]_vars
\* The loader and the slow commit keep working while they can.
FairSpec == Spec /\ WF_vars(Work)

\* "A row that is visible by the end of the second run was loaded exactly once."
ExactlyOnce == (ran1 /\ ran2) => \A r \in Rows : visible[r] => loadedCount[r] = 1
\* "Both runs eventually happen."
EventuallyBothRan == <>(ran1 /\ ran2)
\* Witness: rl's late commit really can land after the first run.
NeverCommitsLate == ran1 /\ ~visible["rl"]
===================================================================================
