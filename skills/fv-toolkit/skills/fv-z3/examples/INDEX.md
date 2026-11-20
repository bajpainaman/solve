# Z3 examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its expectations and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/shipping-tiers](good/shipping-tiers/README.md) | good | Rule / decision table (A3, F3) | Completeness and uniqueness are two separate formulas, and a rejected design proves the model can still fail |
| [good/policy-containment](good/policy-containment/README.md) | good | IAM / access policies (E) | A policy diff is "no input the new policy allows was denied by the old one" |
| [bad/existence-not-universality](bad/existence-not-universality/README.md) | bad | Any | `expect: sat` on the claim itself proves existence, not the universal rule it was meant to check |
| [bad/unknown-read-as-pass](bad/unknown-read-as-pass/README.md) | bad | Any | Code that treats "not sat" as a pass also treats `unknown` as a pass |

## Anti-patterns without a reproduced example yet

`references/anti-patterns.md` describes these.

- Contradictory domain constraints, where every `check` is `unsat` because no input satisfies the setup at all
- Expecting Z3 to prove an inductive fact over an unbounded recursive structure
