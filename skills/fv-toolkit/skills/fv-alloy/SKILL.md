---
name: fv-alloy
description: "Writes and checks an Alloy 6 model of structure: which configurations of entities and relations can exist together. Covers ownership, cardinality, permissions and role grants, tenant isolation, schema and version compatibility, dependency rules and data lineage. Every check is paired with a satisfiable run, every command declares its expectation, and planted bugs must be detected. Use when the question is whether the data or the configuration can reach an invalid shape, for .als files or Alloy Analyzer output, or when the formal-verification skill routes here. Not for orderings over time (use fv-tlaplus) or for arithmetic over large numbers."
---

# Alloy

The Alloy Analyzer tries every small structure that satisfies a model and returns one that breaks an assertion. Use it when the risk is a bad shape: a user who can grant what they do not hold, a row that two tenants can read, two versions that cannot coexist, a dependency that points upward.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

Use Alloy for structure. For behaviour over time, use `fv-tlaplus`, because Alloy's temporal mode duplicates it. For arithmetic beyond small counts, see Z3 in `${CLAUDE_PLUGIN_ROOT}/references/tools.md`. Alloy's default integers run from -8 to 7.

## Five rules

1. **Every `check` has a satisfiable `run` beside it.** When the facts contradict each other, no instance exists and every check passes. A `run` that finds an instance rules that out. `fv-alloy` fails a model that has a check and no run.
2. **Every command declares its expectation on one line.** `expect 1` means that an instance or a counterexample must exist. `expect 0` means that none may exist. The check of a rejected design carries `expect 1`.
3. **A rule that the code must enforce is a predicate.** Keep a `fact` for what is true by construction, such as a foreign key that the database enforces. A design rule written as a fact removes the very structures you need to examine.
4. **Write `some x.f and x.f in S` when emptiness matters.** The empty set is a subset of every set, so `x.f in S` holds for an `x` with no `f`.
5. **State the scope.** A pass covers every structure up to the scope and nothing larger. Start at 3 or 4, and say the scope in the report.

## From the system to the model

| In the system | In the model |
|---|---|
| An entity or a table | A `sig` |
| A reference or a join table | A field: `owner: one Tenant`, `roles: set Role` |
| A subtype or a status | `sig Admin extends User`, or a subset `sig Approved in Role` |
| Something true by construction | A `fact` whose comment names the mechanism that enforces it |
| A rule the code must enforce | A `pred`, used as the premise of an assertion |
| A claim from the ledger | An `assert`, checked once under each design |
| A state that must be possible | A `pred` with a `run ... expect 1` |

Where the real system has the relation as data, such as an import graph, a role configuration or ORM metadata, generate the Alloy relation from it and do not retype it by hand.

## Files to write

| File | Holds |
|---|---|
| `<name>.als` | The model. Its header comment carries `Source read at:` and `Covers:`. Each `fun`, `pred` and `fact` has a comment that names the code it transcribes |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the scope and the limits |

Copy `examples/good/rbac/` to start.

## Workflow

1. **Write the signatures and one `run`, then run.** Confirm that the model has an instance before you write any assertion.

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-alloy --show <name>.als
   ```

2. **Write each design rule as a predicate** and each claim as an assertion with the rule as its premise.
3. **Add the commands.** Write one `check` per claim and design, one `check ... expect 1` for each rejected design, and one `run` per predicate you rely on.
4. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

5. **Read each counterexample back into the system.** Follow part 2 of `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md`. Ask of each tuple in the instance whether the real system can hold it.

## Reading the output

| Line | Meaning |
|---|---|
| `PASS check X: UNSAT` | No counterexample exists up to the scope |
| `PASS check X: SAT` | The command declared `expect 1`, and the analyzer found the counterexample |
| `PASS run X: SAT` | An instance exists, so the checks do not pass on an empty model |
| `FAIL check X: expected UNSAT, got SAT` | A candidate flaw in the design, or a gap in the model. The instance follows |
| `FAIL check X: expected SAT, got UNSAT` | A rejected design passes. The model can no longer show the failure |
| `FAIL run X: expected SAT, got UNSAT` | No instance satisfies the predicate. Look for contradicting facts |
| `ERROR ...` | The analyzer could not read the model. This is never a counterexample |
| `UNAVAILABLE ...` | Java or the jar is missing. The model was not checked |

## Telling a counterexample

`fv-alloy --show` prints the relations of the instance. Rewrite them as numbered sentences in the system's words:

```text
1. Role R carries permission P.
2. User U holds no role, so U holds no permission.
3. U administers R.
4. U adds another user to R and has granted P without holding it.
```

## Examples

`examples/INDEX.md` lists every example. `examples/good/rbac/` is the complete pattern, and the other folders under `examples/good/` are templates for relationship-based access, schema compatibility, slowly changing dimensions, PII lineage and tenant isolation. Start from the template whose pattern matches the claim. `examples/bad/` holds four models whose checks pass while they prove nothing. Read `bad/fact-forbids-the-bug/` before you write your first fact.

## References

| File | Read when |
|---|---|
| `references/syntax.md` | You need an operator, a multiplicity or a known pitfall of the analyzer |
| `references/anti-patterns.md` | You review a model, yours or someone else's |
