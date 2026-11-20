# Document access

**Pattern:** ABAC / policy languages (catalog E).
**Teaches:** a forbid rule checked across several entities, a rejected
policy that widens access checked as a witness, and a mutations file that
plants a bug in each rule.

## The system

`policy.cedar` permits a user to view a document owned by their own
department, and forbids viewing a secret document without high clearance,
even inside the owning department. `schema.cedarschema` gives `User` a
`department` and a `clearance`, and `Document` an `owningDepartment` and a
`classification`.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| A low-clearance user is denied a secret document in their own department | safety | the `tests.json` cases for `alice`, `dave` |
| High clearance still grants the same document | safety | the `tests.json` case for `bob` |
| A different department is denied regardless of clearance | safety | the `tests.json` case for `carol` |
| Dropping the clearance check must be caught | witness | `DropClearanceCheck.cedar` run against the same tests |

## Checks

| Test case (entity) | Declared decision |
|---|---|
| `alice_allowed_normal_same_department` | allow |
| `alice_denied_secret_low_clearance` | deny |
| `bob_allowed_secret_high_clearance` | allow |
| `carol_denied_normal_different_department` | deny |
| `dave_denied_secret_medium_clearance` | deny |

`alice` and `dave` are two different entities that both get denied a secret
document by the same forbid rule, so the rule is checked on more than one
case, not just the one it was written against.

## Run

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/fv-cedar policy.cedar schema.cedarschema tests.json
${CLAUDE_PLUGIN_ROOT}/scripts/fv-cedar DropClearanceCheck.cedar schema.cedarschema tests.json   # the witness; must FAIL
${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate document-access.mutations
```

## Telling a counterexample

This is the real output of running the tests against `DropClearanceCheck.cedar`,
which has no forbid rule at all:

```text
PASS test alice_allowed_normal_same_department: ok
FAIL test alice_denied_secret_low_clearance: expected Deny, got Allow
PASS test bob_allowed_secret_high_clearance: ok
PASS test carol_denied_normal_different_department: ok
FAIL test dave_denied_secret_medium_clearance: expected Deny, got Allow
```

Read as steps:

```text
1. alice has low clearance in the eng department.
2. Document d2 is a secret document owned by the eng department.
3. The permit rule fires, because alice's department matches d2's.
4. No forbid rule exists to override it, so alice views a secret
   document she should not be able to see.
```

## Bounds and limits

The policy set checks one action over two attributes per entity. `cedar
validate` confirms the policy set parses against the schema; it does not
confirm the decisions in `tests.json` are the right ones, which is what the
test cases and the mutations file are for. A policy set with more actions
or more attributes needs its own test cases; these do not generalize past
the entities listed.
