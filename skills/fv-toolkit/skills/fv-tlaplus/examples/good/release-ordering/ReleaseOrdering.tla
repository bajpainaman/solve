---------------------------- MODULE ReleaseOrdering ----------------------------
(* Source read at: 0000000
   Covers: deploy/schema_migration.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   Two instances serve traffic while a migration expands the schema, then
   migrates data, then contracts the old column. A rolling deploy upgrades
   one instance at a time, so both versions can run against the same
   schema at once. Old code needs the old column; the column is gone
   once the schema contracts.

   The knob Order chooses the design:
     "contract_too_early"  the schema contracts once migrated, whether or
                            not every instance has upgraded
     "wait_for_rollout"    the schema contracts only once every instance
                            reports running the new version
   The fault switch RollingDeploy lets instances upgrade one at a time.
   FALSE switches it off: every instance upgrades in one step, so there
   is never a moment with both versions running. *)
EXTENDS Naturals

CONSTANTS Instances, Order, RollingDeploy

VARIABLES version, phase

vars == <<version, phase>>

Init ==
    /\ version = [i \in Instances |-> "old"]
    /\ phase = "expand"

TypeOK ==
    /\ version \in [Instances -> {"old", "new"}]
    /\ phase \in {"expand", "migrate", "contract"}

AllUpgraded == \A i \in Instances : version[i] = "new"

\* Source: deploy.roll_one(), one instance restarting on the new version.
UpgradeOne(i) ==
    /\ RollingDeploy /\ version[i] = "old"
    /\ version' = [version EXCEPT ![i] = "new"]
    /\ UNCHANGED phase

\* Source: deploy.roll_all(), every instance restarting at once.
UpgradeAll ==
    /\ ~RollingDeploy /\ ~AllUpgraded
    /\ version' = [i \in Instances |-> "new"]
    /\ UNCHANGED phase

\* Source: migration.expand(), adding the new column.
AdvanceToMigrate ==
    /\ phase = "expand"
    /\ phase' = "migrate"
    /\ UNCHANGED version

\* Source: migration.contract(), dropping the old column once migrated,
\* without waiting to see whether every instance still needs it. With no
\* rolling window, the one deploy step always finishes first anyway.
ContractTooEarly ==
    /\ Order = "contract_too_early" /\ phase = "migrate" /\ (RollingDeploy \/ AllUpgraded)
    /\ phase' = "contract"
    /\ UNCHANGED version

\* Source: migration.contract(), dropping the old column only once every
\* instance reports it no longer needs it.
ContractAfterRollout ==
    /\ Order = "wait_for_rollout" /\ phase = "migrate" /\ AllUpgraded
    /\ phase' = "contract"
    /\ UNCHANGED version

\* The end state gets its own action, so deadlock checking stays on.
Done == phase = "contract" /\ AllUpgraded /\ UNCHANGED vars

Work == (\E i \in Instances : UpgradeOne(i)) \/ UpgradeAll \/ AdvanceToMigrate \/ ContractTooEarly \/ ContractAfterRollout
Next == Work \/ Done

Spec == Init /\ [][Next]_vars
\* The deploy and the migration keep working while they can.
FairSpec == Spec /\ WF_vars(Work)

\* "No instance still on the old version is left running once the old
\* column is gone."
NeverStrandsOldVersion == ~(\E i \in Instances : version[i] = "old" /\ phase = "contract")
\* "The rollout and the migration both finish."
EventuallyMigrated == <>(phase = "contract" /\ AllUpgraded)
\* Witness: the schema really does reach contract.
NeverContracts == phase # "contract"
===================================================================================
