# Anti-pattern: a permit that a forbid shadows

**Symptom:** the check passes.

`policy.cedar` has a permit meant to let a high-clearance user view a
secret document in their own department, and a forbid meant to block a
low-clearance user from a secret document. The forbid's condition only
checks `resource.classification == "secret"`, with no clearance check, so
it fires for every secret document and overrides the high-clearance
permit too. `tests.json` has two cases, neither for a high-clearance user
on a secret document.

```text
PASS test alice_allowed_normal_same_department: ok
PASS test alice_denied_secret_low_clearance: ok
```

## Why it is wrong

Cedar's semantics make an applicable `forbid` always win over an
applicable `permit`, with no regard for which policy is more specific.
This forbid is less specific than the permit it is meant to coexist with,
so it blocks every case the permit was written for, not only the one it
was meant to replace. `tests.json` never asks a high-clearance user to
view a secret document, so nothing in the suite can see that the permit
for that case never actually applies.

Adding that case is what finds it:

```text
PASS test alice_allowed_normal_same_department: ok
PASS test alice_denied_secret_low_clearance: ok
FAIL test bob_allowed_secret_high_clearance: expected Allow, got Deny
```

## The fix

Add the same clearance condition to the forbid rule, as
`../../good/document-access/policy.cedar` does:
`resource.classification == "secret" && principal.clearance != "high"`.

## The check that catches it

No mechanical check inside `cedar validate` catches it, because the
policy set still parses and type-checks against the schema; shadowing is
a decision the schema says nothing about. `../../good/document-access/`'s
rule is the general one: a forbid rule needs a test case for every
principal attribute combination its condition does not mention, not only
the one case the author had in mind when writing it.
