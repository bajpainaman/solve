# Anti-patterns in XState path testing

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| A state with no incoming transition | `getShortestPaths` never generates a path to it, and the run reports nothing wrong | Compare the state values the generated paths reach against the machine's declared state names. Reproduced in `examples/bad/unreachable-state/` |
| A path test asserts that a step's value has a shape, not that it equals the path's own expected value | Every mutation in the implementation is `MISSED` | Compare `step.state.value` (and the context fields the machine tracks) against the implementation at every step. Reproduced in `examples/bad/asserts-nothing/` |
| Generating paths only from the correct, guarded machine | A missing or inverted guard in the implementation has no path that would expose it, because the model itself never takes the illegal transition | Also generate paths from a second machine that models the rejected design (the guard removed or inverted), and check that the real implementation refuses to follow them. `examples/good/checkout/` does this with `checkoutMachineUnguarded` |
