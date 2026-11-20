---------------------------- MODULE TwoPhaseCommit ----------------------------
(* Source read at: 0000000
   Covers: txn/coordinator.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A coordinator runs two-phase commit over a fixed set of resource managers.
   Every manager prepares, and the coordinator remembers each prepare vote
   even if that manager later changes its mind on its own. The coordinator
   can crash after it has started collecting votes but before it decides.

   The knob Order chooses the design:
     "block_on_crash"  a prepared manager with no decision just waits
     "timeout_abort"   a prepared manager aborts on its own once the
                        coordinator has been down for a while
   The fault switch MaxCrashes bounds how many times the coordinator
   crashes, and Recovers says whether a crashed coordinator ever comes
   back. FALSE means a crash before a decision blocks the protocol for
   good: that is the blocking two-phase commit is named for. *)
EXTENDS Naturals

CONSTANTS RM, Order, MaxCrashes, Recovers

VARIABLES rmState, tmPrepared, tmState, crashed, crashes

vars == <<rmState, tmPrepared, tmState, crashed, crashes>>

Init ==
    /\ rmState = [rm \in RM |-> "working"]
    /\ tmPrepared = {}
    /\ tmState = "init"
    /\ crashed = FALSE
    /\ crashes = 0

TypeOK ==
    /\ rmState \in [RM -> {"working", "prepared", "committed", "aborted"}]
    /\ tmPrepared \subseteq RM
    /\ tmState \in {"init", "committed", "aborted"}
    /\ crashed \in BOOLEAN /\ crashes \in Nat

\* Source: resource_manager.prepare(). The vote is recorded at once; the
\* coordinator's record of it never changes once a manager has voted.
Prepare(rm) ==
    /\ rmState[rm] = "working"
    /\ rmState' = [rmState EXCEPT ![rm] = "prepared"]
    /\ tmPrepared' = tmPrepared \cup {rm}
    /\ UNCHANGED <<tmState, crashed, crashes>>

\* Source: coordinator.commit(), once every manager has voted to prepare.
TMCommit ==
    /\ ~crashed /\ tmState = "init" /\ tmPrepared = RM
    /\ tmState' = "committed"
    /\ UNCHANGED <<rmState, tmPrepared, crashed, crashes>>

\* Source: coordinator.abort(), which the coordinator can choose at any
\* point before it has decided.
TMAbort ==
    /\ ~crashed /\ tmState = "init"
    /\ tmState' = "aborted"
    /\ UNCHANGED <<rmState, tmPrepared, crashed, crashes>>

\* Source: resource_manager.on_decision(), learning the coordinator's commit.
RMLearnCommit(rm) ==
    /\ tmState = "committed" /\ rmState[rm] = "prepared"
    /\ rmState' = [rmState EXCEPT ![rm] = "committed"]
    /\ UNCHANGED <<tmPrepared, tmState, crashed, crashes>>

\* Source: resource_manager.on_decision(), learning the coordinator's abort.
RMLearnAbort(rm) ==
    /\ tmState = "aborted" /\ rmState[rm] \in {"working", "prepared"}
    /\ rmState' = [rmState EXCEPT ![rm] = "aborted"]
    /\ UNCHANGED <<tmPrepared, tmState, crashed, crashes>>

\* Source: resource_manager.on_timeout(), unilaterally giving up on a
\* coordinator that has been down since this manager prepared.
RMTimeoutAbort(rm) ==
    /\ Order = "timeout_abort"
    /\ crashed /\ tmState = "init" /\ rmState[rm] = "prepared"
    /\ rmState' = [rmState EXCEPT ![rm] = "aborted"]
    /\ UNCHANGED <<tmPrepared, tmState, crashed, crashes>>

\* Fault: the coordinator crashes before it has decided. MaxCrashes bounds
\* how many times this can happen, so a recovery is never followed by a
\* crash the model has not budgeted for.
Crash ==
    /\ ~crashed /\ tmState = "init" /\ crashes < MaxCrashes
    /\ crashed' = TRUE
    /\ crashes' = crashes + 1
    /\ UNCHANGED <<rmState, tmPrepared, tmState>>

\* Fault: the coordinator restarts, keeping its durable prepare votes.
Recover ==
    /\ crashed /\ Recovers
    /\ crashed' = FALSE
    /\ UNCHANGED <<rmState, tmPrepared, tmState, crashes>>

\* The end state gets its own action, so deadlock checking stays on, and a
\* coordinator crash with no recovery still shows up as a real deadlock.
Done == tmState \in {"committed", "aborted"} /\ \A rm \in RM: rmState[rm] \in {"committed", "aborted"} /\ UNCHANGED vars

Work == (\E rm \in RM : Prepare(rm) \/ RMLearnCommit(rm) \/ RMLearnAbort(rm) \/ RMTimeoutAbort(rm))
         \/ TMCommit \/ TMAbort \/ Recover
Next == Work \/ Crash \/ Done

Spec == Init /\ [][Next]_vars
\* Every manager and the coordinator keep working while they can. A crash
\* gets no fairness; a recovery is part of the work the coordinator does.
FairSpec == Spec /\ WF_vars(Work)

\* "No manager commits while another aborts."
AllOrNothing == ~(\E rm1, rm2 \in RM : rmState[rm1] = "committed" /\ rmState[rm2] = "aborted")
\* "Every manager eventually reaches a decision."
EventuallyDecided == <>(\A rm \in RM : rmState[rm] \in {"committed", "aborted"})
\* Witness: every manager committing is reachable.
NeverAllCommitted == ~(\A rm \in RM : rmState[rm] = "committed")
=================================================================================
