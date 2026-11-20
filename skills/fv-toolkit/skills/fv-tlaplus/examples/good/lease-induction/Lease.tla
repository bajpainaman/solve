-------------------------------- MODULE Lease --------------------------------
(* Source read at: 0000000
   Covers: locking/lease.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A single lease slot. One client at a time may hold it. The slot starts
   free and alternates between a held state and a free state.

   The first invariant anyone writes for this is usually the weak one:
   "leases is 0 or 1". That is true of every reachable state, and TLC
   confirms it on the bounded run in ../../bad/non-inductive-invariant/. It is
   not inductive on its own: an arbitrary state that merely satisfies it,
   such as leases = 1 with phase = "idle", is not reachable, but Apalache's
   inductive step is allowed to start there, and Acquire runs again from it.
   StrongInv below adds the fact that correlates leases with phase, which is
   what the induction actually needs. *)
EXTENDS Integers

VARIABLES
    \* @type: Int;
    leases,
    \* @type: Str;
    phase

\* Source: Lease.acquire(), which only runs when the slot is free.
Acquire ==
    /\ phase = "idle"
    /\ leases' = leases + 1
    /\ phase' = "held"

\* Source: Lease.release(), which only runs while the slot is held.
Release ==
    /\ phase = "held"
    /\ leases' = leases - 1
    /\ phase' = "idle"

Init == leases = 0 /\ phase = "idle"
Next == Acquire \/ Release
Spec == Init /\ [][Next]_<<leases, phase>>

\* "At most one lease is outstanding." The property the lock exists for.
Safety == leases <= 1

\* Not inductive: see bad/non-inductive-invariant/README.md.
WeakInv == leases \in {0, 1} /\ phase \in {"idle", "held"}

\* Inductive: the state of the slot and the count agree.
StrongInv == (phase = "idle" /\ leases = 0) \/ (phase = "held" /\ leases = 1)
===============================================================================
