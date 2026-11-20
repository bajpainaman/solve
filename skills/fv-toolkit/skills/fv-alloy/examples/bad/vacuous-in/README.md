# Anti-pattern: `x.f in S` when `x.f` can be empty

**Symptom:** an assertion that was meant to say "every user holds an approved role" passes, and a user with no role satisfies it.

`u.roles in Approved` says that the set of roles is a subset of the approved roles. The empty set is a subset of every set, so a user with no role passes.

```text
PASS check EveryRoleHeldIsApproved: UNSAT
PASS check EveryUserHoldsAnApprovedRole: SAT
```

The second line is the stronger claim, and the analyzer finds its counterexample: a user who holds no role. The model declares that outcome with `expect 1`, because the design has no rule yet that gives every user a role.

## The fix

Write `some u.roles and u.roles in Approved` when emptiness matters. Then decide what the system should do about the user with no role, and encode that decision as a rule.

## The check that catches it

For each assertion of the form `x.f in S`, ask whether an empty `x.f` should satisfy the claim. When it should not, add `some x.f` and rerun.
