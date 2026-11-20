# CrossHair examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its expectations and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/split-evenly](good/split-evenly/README.md) | good | Money and rounding (F3), oracle equivalence (A3, C1) | A contract check beside a `diffbehavior` comparison, and a rejected design that the diff can still tell apart |
| [bad/weak-contract-reads-as-proof](bad/weak-contract-reads-as-proof/README.md) | bad | Any | A contract that checks one property lets `holds` stand in for "correct" |
| [bad/nondeterministic-code-caps-the-result](bad/nondeterministic-code-caps-the-result/README.md) | bad | Any | A real source of entropy runs once for real; `holds` can be luck |

## Anti-patterns without a reproduced example yet

`references/anti-patterns.md` describes these.

- `check` run on two functions separately, instead of `diffbehavior` on the pair, where each satisfies a loose shared contract and still disagrees with the other
- Raising `--per_condition_timeout` to make a real `FAIL` go away
