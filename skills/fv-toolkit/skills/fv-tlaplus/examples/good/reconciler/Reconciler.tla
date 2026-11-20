---------------------------- MODULE Reconciler ----------------------------
(* Source read at: 0000000
   Covers: controller/replica_controller.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A controller keeps a replica count at a fixed desired value. It reads
   the count from a local cache of the API server, which lags behind the
   true count: a create it already issued can take a while to show up
   there. The reconcile loop can run again before the cache has caught up.

   The knob Order chooses the design:
     "stale_read"              the loop computes the gap from the cache
                                alone, with no memory of its own creates
     "resource_version_check"  the loop keeps its own count of creates it
                                has issued but not yet seen in the cache,
                                and subtracts that from the gap, the way a
                                controller's expectations cache does
   The fault switch MaxReconciles bounds how many times the loop can run
   before the cache has synced. One switches it off: the loop runs once
   and has to wait for the cache to catch up before it can run again. *)
EXTENDS Naturals

CONSTANTS Order, MaxReconciles

Desired == 2

VARIABLES actual, cachedActual, expectedCreates, reconciles

vars == <<actual, cachedActual, expectedCreates, reconciles>>

Init ==
    /\ actual = 0
    /\ cachedActual = 0
    /\ expectedCreates = 0
    /\ reconciles = 0

TypeOK ==
    /\ actual \in Nat /\ cachedActual \in Nat
    /\ expectedCreates \in Nat /\ reconciles \in Nat

\* Source: controller.reconcile(), computing the gap from the cache alone
\* and creating that many replicas at once.
ReconcileStale ==
    /\ Order = "stale_read" /\ cachedActual < Desired /\ reconciles < MaxReconciles
    /\ actual' = actual + (Desired - cachedActual)
    /\ reconciles' = reconciles + 1
    /\ UNCHANGED <<cachedActual, expectedCreates>>

\* Source: controller.reconcile(), subtracting creates it already issued
\* but has not yet seen in the cache.
ReconcileChecked ==
    /\ Order = "resource_version_check"
    /\ cachedActual + expectedCreates < Desired /\ reconciles < MaxReconciles
    /\ LET gap == Desired - cachedActual - expectedCreates
       IN  /\ actual' = actual + gap
           /\ expectedCreates' = expectedCreates + gap
    /\ reconciles' = reconciles + 1
    /\ UNCHANGED cachedActual

\* Source: informer.on_watch_event(), the cache catching up one step. A
\* step the controller expected lowers its own outstanding count.
SyncCache ==
    /\ cachedActual < actual
    /\ cachedActual' = cachedActual + 1
    /\ expectedCreates' = IF expectedCreates > 0 THEN expectedCreates - 1 ELSE 0
    /\ UNCHANGED <<actual, reconciles>>

\* The end state gets its own action, so deadlock checking stays on.
Done == actual = Desired /\ cachedActual = Desired /\ UNCHANGED vars

Work == ReconcileStale \/ ReconcileChecked \/ SyncCache
Next == Work \/ Done

Spec == Init /\ [][Next]_vars
\* The controller and the cache keep working while they can.
FairSpec == Spec /\ WF_vars(Work)

\* "The controller never creates more replicas than desired."
NeverOvershoots == actual <= Desired
\* "The true count and the cache both converge on the desired count."
EventuallyConverges == <>(actual = Desired /\ cachedActual = Desired)
\* Witness: convergence really does happen.
NeverConverges == ~(actual = Desired /\ cachedActual = Desired)
=============================================================================
