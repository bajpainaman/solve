# RBAC with delegated administration

**Pattern:** RBAC (catalog E), permissions on shared content (catalog F3).
**Teaches:** a design rule as a predicate, one check per design with its expectation, a witness, a mutations file.

## The system

A user holds roles, and a role carries permissions. A user who administers a role can add other users to it. The question is whether a user can hand out a permission that they do not hold.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No user can grant a permission that they do not hold | safety | `NoEscalation` |
| Someone can still grant something | reachability | `run SomeoneCanGrant ... expect 1` |

## Commands

| Command | Design | Expectation |
|---|---|---|
| `run SomeoneCanGrant for 3` | A user administers only roles they hold | SAT: an instance exists |
| `check NoEscalationWhenAdminsHoldTheRole for 4` | A user administers only roles they hold | UNSAT: no counterexample |
| `check NoEscalationWhenAnyoneAdmins for 4` | Any user may administer any role | SAT: a counterexample exists |

The third command is the rejected design. It must find a counterexample. When it stops finding one, the model has lost the ability to show an escalation.

## Run

```bash
fv-alloy --show rbac.als
fv-mutate rbac.mutations
```

## The counterexample, as the user reads it

```text
1. Role R carries permission P.
2. User U holds no role, so U holds no permission.
3. U administers R.
4. U adds another user to R and has granted P without holding it.
```

## Bounds and limits

The checks cover every structure with up to four users, four roles and four permissions. The model has no role hierarchy and no revocation.
