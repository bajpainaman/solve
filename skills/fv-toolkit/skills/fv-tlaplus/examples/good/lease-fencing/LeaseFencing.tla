---------------------------- MODULE LeaseFencing ----------------------------
(* Source read at: 0000000
   Covers: storage/lease.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   Holder h1 has the lease, carrying token 1. The lease times out without a
   renewal, which also covers a GC pause: h1 takes no steps for an unbounded
   period and resumes believing it still holds token 1. A second holder, h2,
   is then granted the lease with a higher token. h1 can still try to write
   with its old token after that.

   The knob Order chooses the design:
     "no_fencing"  storage accepts a write whatever token it carries
     "fencing"     storage keeps the highest token any grant has reached,
                   and rejects a write below that mark
   The fault switch AllowStaleWrite lets the paused holder try to write
   after its lease has already moved to someone else. FALSE switches it off:
   nothing ever uses the stale token, so there is nothing to reject. *)
EXTENDS Naturals

CONSTANTS Order, AllowStaleWrite

VARIABLES leaseToken, holder, h1Token, expired, storageToken, attempted, accepted

vars == <<leaseToken, holder, h1Token, expired, storageToken, attempted, accepted>>

Init ==
    /\ leaseToken = 1
    /\ holder = "h1"
    /\ h1Token = 1
    /\ expired = FALSE
    /\ storageToken = 0
    /\ attempted = FALSE
    /\ accepted = FALSE

TypeOK ==
    /\ leaseToken \in Nat /\ holder \in {"h1", "h2"} /\ h1Token \in Nat
    /\ expired \in BOOLEAN /\ storageToken \in Nat
    /\ attempted \in BOOLEAN /\ accepted \in BOOLEAN

\* Source: lease.on_timeout(). h1 fails to renew in time; the same action
\* covers a GC pause that keeps h1 from running at all until it is too late.
ExpireLease ==
    /\ holder = "h1" /\ ~expired
    /\ expired' = TRUE
    /\ UNCHANGED <<leaseToken, holder, h1Token, storageToken, attempted, accepted>>

\* Source: lease_service.grant(), handing the lease to h2 with a fresh,
\* higher token. The fencing design records that token as the high mark now,
\* not when h2 happens to write with it.
GrantToH2 ==
    /\ expired /\ holder = "h1"
    /\ leaseToken' = leaseToken + 1
    /\ holder' = "h2"
    /\ storageToken' = IF Order = "fencing" THEN leaseToken + 1 ELSE storageToken
    /\ UNCHANGED <<h1Token, expired, attempted, accepted>>

\* Source: storage.write(rm, token), h1's write with the token it was
\* granted, after it has lost the lease to h2.
WriteAsH1 ==
    /\ AllowStaleWrite /\ holder = "h2" /\ ~attempted
    /\ attempted' = TRUE
    /\ accepted' = IF Order = "fencing" THEN h1Token >= storageToken ELSE TRUE
    /\ UNCHANGED <<leaseToken, holder, h1Token, expired, storageToken>>

\* The end state gets its own action, so deadlock checking stays on.
Done == holder = "h2" /\ (attempted \/ ~AllowStaleWrite) /\ UNCHANGED vars

Work == ExpireLease \/ GrantToH2 \/ WriteAsH1
Next == Work \/ Done

Spec == Init /\ [][Next]_vars
\* The lease service and h1 keep working while they can.
FairSpec == Spec /\ WF_vars(Work)

\* "Storage rejects a write whose token is below the token the lease is on now."
StaleWriteRejected == accepted => h1Token >= leaseToken
\* "The lease is eventually granted to a new holder."
EventuallyGranted == <>(holder = "h2")
\* Witness: the lease really does move to a second holder.
NeverGranted == holder # "h2"
===============================================================================
