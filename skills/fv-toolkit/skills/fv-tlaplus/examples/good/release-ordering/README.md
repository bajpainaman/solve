# Release ordering

**Pattern:** rolling deploy across an expand-and-contract migration (catalog D).
**Teaches:** a fault switch scoped to the one action it actually affects, a non-rolling design that still needs an ordering guard against the step it races.

## The system

Two instances serve traffic while a migration expands the schema, then
migrates data, then contracts the old column. A rolling deploy upgrades
one instance at a time, so both versions can run against the same schema
at once. Old code needs the old column, which is gone once the schema
contracts.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No instance still on the old version is left running once the old column is gone | safety | `NeverStrandsOldVersion` |
| The rollout and the migration both finish | liveness | `EventuallyMigrated`, under weak fairness on the deploy and the migration |
| The schema really does reach contract | reachability | `WitnessContracts.cfg` must violate `NeverContracts` |

## Configs

| Config | Design | Rolling | Declared outcome |
|---|---|---|---|
| `WaitForRollout.cfg` | contracts only once every instance has upgraded | yes | holds |
| `ContractTooEarly.cfg` | contracts as soon as it is migrated | yes | violated `NeverStrandsOldVersion` |
| `ContractTooEarlyNotRolling.cfg` | contracts as soon as it is migrated | no | holds |
| `WitnessContracts.cfg` | contracts only once every instance has upgraded | yes | violated `NeverContracts` |

With no rolling window, every instance upgrades in a single step, so the
contract step itself still waits for that one step to land before it can
race ahead: there is no longer a moment with an old instance left behind
for it to catch.

## Run

```bash
fv-tlc --trace ReleaseOrdering.tla
fv-mutate ReleaseOrdering.mutations
```

## The counterexample, as the user reads it

```text
1. The deploy upgrades instance i1. i2 is still on the old version.
   deploy.py:9
2. The migration reaches "migrate": both columns exist, so both versions
   still work.                                            schema_migration.py:14
3. The migration contracts, dropping the old column, without checking
   whether every instance has upgraded.                   schema_migration.py:22
4. i2 is still on the old version and still needs the column that is
   now gone.
```

## Bounds and limits

The model has two instances and one migration. It does not model a
rollback, a second schema change layered on top, or an instance that
upgrades and then reverts.
