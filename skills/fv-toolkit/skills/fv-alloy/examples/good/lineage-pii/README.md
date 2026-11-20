# Lineage and PII masking

**Pattern:** data lineage and PII propagation (catalog C4).
**Teaches:** a transitive `derivesFrom` relation, a masking rule as a predicate, the same claim checked against a rule that follows lineage and a rule that does not.

## The system

A column may derive from other columns through a transform, such as a column that copies or combines a PII column. A sink exposes some of its columns to readers and masks a subset of them. The question is whether a sink ever exposes, unmasked, a column that was computed from a PII column through any chain of transforms.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No sink exposes, unmasked, a column derived from PII | safety | `NoUnmaskedPIIAtASink_MaskingCoversLineage` |
| The lineage rule masks a column that is not itself tagged PII | reachability | `run ALineageOnlyColumnIsMasked ... expect 1` |

## Commands

| Command | Masking rule | Expectation |
|---|---|---|
| `run ALineageOnlyColumnIsMasked for 4` | `MaskingCoversLineage` | SAT: the rule reaches past a direct tag |
| `check NoUnmaskedPIIAtASink_MaskingCoversLineage for 4` | `MaskingCoversLineage` | UNSAT: no counterexample |
| `check NoUnmaskedPIIAtASink_MaskingCoversDirectPIIOnly for 4` | `MaskingCoversDirectPIIOnly` | SAT: a counterexample exists |

`MaskingCoversLineage` is the policy this project ships: mask a column whenever it is PII or was computed from PII through any chain of transforms. `MaskingCoversDirectPIIOnly` masks only the columns the catalog tags PII directly, the policy a masking rule written against a column name list ends up enforcing. The third command is that policy. It must find a sink that exposes, unmasked, a column that a transform computed from PII.

## Run

```bash
fv-alloy --show lineage-pii.als
fv-mutate lineage-pii.mutations
```

## The counterexample, as the user reads it

```text
this/Column<:derivesFrom={Column$0->Column$1}
this/Sink<:exposes={Sink$0->Column$0}
this/Sink<:masked={}
this/PIIColumn={Column$1}
```

1. Column 1 is tagged PII.
2. Column 0 is computed from Column 1 through a transform.
3. The sink exposes Column 0 and masks nothing.
4. The direct-only policy never looks at Column 0, because Column 0 itself carries no PII tag, so the transform's output leaves the sink in the clear.

## Bounds and limits

The checks cover four columns and four sinks. The model has one hop of masking per sink and no column that derives from more than one PII source at once.
