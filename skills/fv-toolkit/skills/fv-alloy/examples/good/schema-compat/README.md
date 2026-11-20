# Schema compatibility across a rolling deploy

**Pattern:** data contracts and schema evolution (catalog C1), API versioning (catalog F1), blue-green and canary rollout (catalog B6).
**Teaches:** an ordering of versions with `util/ordering`, a compatibility rule between a producer version and a consumer version, a design rule checked under the registry's policy and under no policy at all.

## The system

Producers and consumers each pin to one schema version. A version carries a set of fields and declares which of them a reader must find. During a rolling deploy, the version one step older and the version one step newer run alongside the current one, so a producer on one version and a consumer on an adjacent version are live together.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Every producer version and consumer version that are live together are compatible | safety | `AllLivePairsCompatible_AdditiveWithGracePeriod` |
| A live pair exists where the consumer actually requires a field | reachability | `run SomeLivePairRequiresAField ... expect 1` |

## Commands

| Command | Registry policy | Expectation |
|---|---|---|
| `run SomeLivePairRequiresAField for 4 but 3 Version` | `AdditiveWithGracePeriod` | SAT: a live pair with a real requirement exists |
| `check AllLivePairsCompatible_AdditiveWithGracePeriod for 4 but 3 Version` | `AdditiveWithGracePeriod` | UNSAT: no counterexample |
| `check AllLivePairsCompatible_NoRule for 4 but 3 Version` | none | SAT: a counterexample exists |

`AdditiveWithGracePeriod` is the registry's two rules: fields are only ever added across versions, and a field becomes required only in a version after the one that added it, never the same version. The third command drops both rules. It must find an incompatible pair, because an unreviewed change can add a field and require it in the same release.

## Run

```bash
fv-alloy --show schema-compat.als
fv-mutate schema-compat.mutations
```

## The counterexample, as the user reads it

```text
this/Version<:fields={Version$0->Field$0, Version$0->Field$1, Version$0->Field$2}
this/Version<:required={Version$0->Field$0, Version$0->Field$1, Version$0->Field$2}
this/Producer<:ver={Producer$0->Version$1}
this/Consumer<:ver={Consumer$0->Version$0}
```

1. Version 0 carries three fields and requires all three.
2. Version 1 carries no fields at all, and the ordering puts it one step before Version 0.
3. A producer runs at Version 1, and a consumer runs at Version 0, so the rolling deploy has them live together.
4. The consumer requires three fields that the producer does not carry, with no registry rule in force to stop it.

## Bounds and limits

The checks cover three versions and up to four producers, four consumers and four fields. The model has one event type and no schema for the fields themselves, so a field rename is not distinguished from a field removal plus an addition.
