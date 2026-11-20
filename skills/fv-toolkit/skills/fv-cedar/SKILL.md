---
name: fv-cedar
description: "Checks Cedar authorization policies against a schema with the cedar CLI: validation that policies and schema agree, and run-tests cases that declare the allow or deny decision a request must get. Use for RBAC or ABAC policies written in Cedar, a forbid rule that must deny every listed entity, a rejected policy change that must be caught, or when the formal-verification skill routes here. Not for IAM-style policies outside Cedar or large rule tables (use Z3 by hand), or for a relational model with no decision per request (use fv-alloy)."
---

# Cedar policies with the cedar CLI

`cedar validate` checks that a policy set and a schema agree on entity
types and attributes. `cedar run-tests` checks that a policy set produces
the declared `allow` or `deny` decision for each of a list of requests.
Together they are this skill's check: validation catches a policy that
cannot type-check, and run-tests catches a policy that type-checks but
decides the wrong thing.

If you came here directly, run steps 1 to 3 of the `formal-verification`
skill first. They produce the claims table and the confirmed property
ledger that this skill encodes.

## Five rules

1. **An applicable `forbid` always wins over an applicable `permit`.**
   Give every `forbid` every attribute condition the cases it must not
   affect need, or it shadows a permit far wider than intended; see
   `examples/bad/shadowed-permit/`.
2. **Test every entity a rule's condition distinguishes, not only one.**
   A forbid rule checked against a single entity could be checking that
   entity's irrelevant attributes instead of the one the rule actually
   reads; `examples/good/document-access/` denies the same rule to two
   different entities.
3. **`cedar validate` is not a test.** It checks that the policy set
   type-checks against the schema, not that any decision is the right
   one. Use `run-tests` with a declared decision per request for that.
4. **Check a rejected policy too.** Run the same `tests.json` against a
   policy that widens access on purpose, and confirm at least one case
   fails. A policy set that passes under every rejected design would also
   pass under the chosen one for no reason that the test can see.
5. **Every rule must fail on a planted bug.** Write a `.mutations` file
   and run `fv-mutate`. A test suite that stays green on every planted
   bug checks nothing.

## Files to write

Put the files in one directory beside the code or config they describe.

| File | Holds |
|---|---|
| `Schema.cedarschema` | The entity types, attributes and actions. Its header comment carries `Source read at:` and `Covers:` |
| `Policy.cedar` | The chosen policy set, with one comment per rule naming the access rule it encodes |
| `<Mechanism>.cedar` | One per rejected policy change, named for what it does to access, never for a verdict |
| `tests.json` | One object per request: `name`, `request`, `entities`, `decision`, `reason`, and `num_errors` (always `0` unless a policy is expected to error) |
| `<Name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the checks table, the run commands, a counterexample, the bounds and limits |

Copy `examples/good/document-access/` to start.

## Workflow

1. **Write the schema**, then `cedar validate` an empty or near-empty
   policy set against it to confirm the entity types and actions parse.
2. **Write the chosen policy set**, one rule per access decision, each
   with a comment naming what it encodes.
3. **Write one test case per entity a rule distinguishes.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-cedar Policy.cedar Schema.cedarschema tests.json
   ```

4. **Write a rejected policy change** and confirm the same tests catch it:

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-cedar Widened.cedar Schema.cedarschema tests.json   # must FAIL
   ```

5. **Plant bugs in the chosen policy set.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <Name>.mutations
   ```

6. **Read each failure.** The decision cedar actually reached, and which
   test case named it, point at the rule that produced it.

## Reading the output

`${CLAUDE_PLUGIN_ROOT}/scripts/fv-cedar` reprints `run-tests`' own lines in
the shape `fv-mutate` needs.

| Line | Meaning |
|---|---|
| `PASS test <name>: ok` | The policy set produced the declared decision for this request |
| `FAIL test <name>: expected <Decision>, got <Decision>` | A rule is missing, too narrow or too wide for this request |
| `ERROR test <name>: <reason>` | This one test case could not be evaluated, for example a schema mismatch in its entities |
| `ERROR <tests file>: <reason>` | The policy set or the schema failed to parse; no test case ran at all |
| `UNAVAILABLE cedar: ...`, exit 3 | The cedar binary is missing; nothing was checked |

## Telling a counterexample

Rewrite a `FAIL` line as numbered steps in the system's own words:

```text
1. alice has low clearance in the eng department.
2. Document d2 is a secret document owned by the eng department.
3. The permit rule fires, because alice's department matches d2's.
4. No forbid rule exists to override it, so alice views a secret
   document she should not be able to see.
```

## What a pass means

A pass means every listed request produced its declared decision under
this policy set and this set of entities. It says nothing about a request
`tests.json` does not list, and nothing about a request outside the
schema's entity types and actions.

When the user needs the claim for every possible request, such as "the
rewrite allows nothing that the old policies denied", say that listed
cases cannot give it. Offer `fv-z3` for that claim. Its
`policy-containment` example encodes two policy sets and searches for a
request that only the new one allows.

## Examples

`examples/INDEX.md` lists every example. `examples/good/document-access/`
is the smallest complete one: a permit and a forbid, five test cases
across four entities, a rejected design, and a mutations file.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a Cedar policy set, yours or someone else's, or need a fact measured on the pinned version |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
