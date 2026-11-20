# Triage: the claims table

A formal tool checks a claim. Collect the claims first, and then pick a check for each claim by its shape.

## Read before you list

- **Read the design as well as the diff.** Read the documents and the tickets that the change cites, because a design bug usually sits there. When a source cannot be reached, say which source stood in for it.
- **Read the house rules.** Each rule in `CLAUDE.md`, `AGENTS.md` or a rules document that the change touches is a claim to assert. Assert a wiring rule, such as "X must not depend on Y", on the call graph or the dependency graph. Today's behaviour can look right while the wiring is wrong.
- **Audit the evidence that the change brings.** Check whether a fixture overrides the function under review, whether a fake behaves like the real thing, and whether a test asserts the outcome that the claim needs. A green suite that cannot see the bug is a finding.
- **Read outward.** List the callers of every changed function, guard and dependency, transitively. A narrowed guard breaks its callers. For anything shared, such as a counter, a lock, a cache or a queue, compare its key with the scope of the claim. A lock per row does not serialise two jobs that work on different rows.

## Write the claims down

Quote every "never", "always", "only when", "guaranteed", "unchanged", "at most", "exactly once" and "safe to" from the description, the ticket, the docstrings and the request. Add the unwritten claims that the design plainly needs, and mark them as yours. Three to six claims is the usual size.

Sort each claim into one kind:

- **Safety** says that a bad thing never happens. It becomes an invariant or an assertion.
- **Liveness** says that a good thing eventually happens. It needs an explicit fairness assumption.
- **Reachability** says that a thing can happen. It needs a witness.

A fix can trade safety for liveness, so check both after a fix.

## Pick the check by the shape of the claim

| Claim shape | Check | Why a weaker check fails | Skill |
|---|---|---|---|
| Orderings: two actors, retries, crashes, lifecycles, rolling deploys | A TLA+ model | A test samples orderings, and the checker tries all of them | `fv-tlaplus` |
| Which configurations can exist together: ownership, cardinality, permissions | An Alloy model | A test samples structures, and the analyzer tries every small one | `fv-alloy` |
| A finite decision function whose inputs can all be listed | Every input, through the real entry point | A model of the function copies the bug or misses it | `fv-hypothesis` |
| A function over unbounded inputs: dates, amounts, histories, windows | Properties on generated inputs, or a reference written from the rule and compared with the real code | Hand-picked cases miss the boundaries | `fv-hypothesis` |
| Two paths that must agree: old and new, batch and streaming, two callers of one calculation | A differential test with the same inputs on both paths and every output compared | One path cannot disagree with itself | `fv-hypothesis` |
| Arithmetic, rounding, precision | Property tests on the real code | There is nothing to model | `fv-hypothesis` |
| Data that acts as the program: rule tables, rate rows, reference data | Checks on the shipped data through the real lookup code | The rows are the change | `tools.md`, under Z3 |

Write this table before you build anything. Each row ends as an assertion that can fail. A claim that was only printed or read by eye is unchecked, and the report never says that it holds.

## When the answer is no

A model checker earns its cost when four things are true:

1. The invariant fits in one sentence.
2. The system has concurrency, retries or distributed state.
3. A violation is expensive.
4. The protocol is small enough to model.

When no claim meets that bar, say so in one paragraph and stop. Ordinary logic gets unit tests and property tests.
