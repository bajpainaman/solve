# CrossHair anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| Reading `holds` as a proof | A function that is clearly wrong still reports `check X: holds`, because the contract is too weak or the search ran out of budget before finding the bug | State "none found within the budget," not "proved." Write the fuller contract. See `examples/bad/weak-contract-reads-as-proof/` |
| A contract that checks one property, not the whole promise | A function that satisfies the stated contract can still be wrong about everything the contract left out | Add a postcondition for each property the docstring or the callers actually rely on |
| Code that depends on real entropy, the clock or a thread | `check` reports `holds` by chance, because CrossHair executed the nondeterministic call for real once and never explored the other branch | Inject the value instead of reading it inside the function, so the input becomes a parameter CrossHair can make symbolic. See `examples/bad/nondeterministic-code-caps-the-result/` |
| `check` on two functions separately, instead of `diffbehavior` | Two functions each satisfy a loose shared contract and still disagree on a real input no `check` run ever tried | Run `diffbehavior old new` directly |
| Raising `--per_condition_timeout` to make a `FAIL` go away | The run takes longer and still fails, or passes only because it ran out of time first | Find what makes the postcondition false; a bigger budget does not change a real bug into a correct one |
