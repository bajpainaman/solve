# Policy containment: the new policy must allow nothing the old one denied

**Pattern:** IAM / access policies (catalog E).
**Teaches:** a policy diff as one formula, "no request the new policy allows was denied by the old one," and a rejected design that widens access by mistake.

## The system

A policy allows a request by its region and its action. Today's policy allows the `us` and `eu` regions, `read` and `write`. A rule change under review tightens this to `us`, `read` only. The question is whether the tightened policy could still allow something the old one denied, the way AWS's Zelkova asks "is policy B contained in policy A?" of IAM policies.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Nothing the tightened policy allows was denied by the old policy | containment | `check_TightenedPolicyAllowsNothingTheOldOneDenied`, `expect: unsat` |
| The rejected design can still be shown to widen access | witness | `check_RejectedDesignWidensAccessToGlobal`, `expect: sat` |

The rejected design adds a `global` region, a region the old policy never named, so it is denied by the old policy and allowed by the rejected one.

## Run

```bash
fv-z3 policy.py
fv-mutate policy.mutations
```

Real output, from the pinned z3-solver 5.4.1:

```text
PASS check TightenedPolicyAllowsNothingTheOldOneDenied: unsat
PASS check RejectedDesignWidensAccessToGlobal: sat
  action = 0, region = 2
```

## The counterexample, as the user reads it

```text
1. A request names region 2 (global) and action 0 (read).
2. The rejected design allows it: region is in {us, global} and action is read.
3. The old policy never named region 2, so it denies the same request.
4. The rejected design therefore allows a request the old policy denied.
```

## Bounds and limits

Regions and actions are modelled as small integers, not strings, so the formula stays in linear integer arithmetic and Z3 decides it exactly rather than searching a bounded scope. Adding a region or an action means adding a case to `old_allows`, not a new sort.
