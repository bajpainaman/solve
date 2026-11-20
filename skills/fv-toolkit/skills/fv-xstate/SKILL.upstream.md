---
name: fv-xstate
description: "Generates the shortest path to every reachable state of an XState v5 machine with @xstate/graph, then replays each path's events against a small plain-JS implementation and compares state after every step. Covers UI flows, multi-step forms and wizards, and other workflow state machines. Use for XState, getShortestPaths, getSimplePaths, path or conformance tests generated from a state machine, \"is every state reachable\", or when the formal-verification skill routes here. Not for a machine with no code behind it yet (write the model in fv-tlaplus or fv-alloy instead) or for properties over time across several processes (use fv-tlaplus)."
---

# Path generation from XState machines

`@xstate/graph`'s `getShortestPaths` walks an XState machine and returns the shortest path to every reachable combination of state and context. Replaying each path's events against the real implementation and comparing state at every step turns that walk into a conformance test, generated from the machine instead of hand-written one case at a time.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

## Five rules

1. **Compare the step's declared value, never its shape.** `step.state.value !== impl.state` catches a wrong transition. `typeof impl.state === "string"` does not. `examples/bad/asserts-nothing/` reproduces this.
2. **A state with no incoming transition has no path and raises no error.** After generating paths, check the state values the paths reach against the machine's own declared state names. `examples/bad/unreachable-state/` reproduces this.
3. **A correct, guarded machine cannot generate a path that violates its own guard.** To check that the implementation rejects what the design forbids, generate paths from a second machine that models the rejected design, and confirm the implementation refuses to follow them.
4. **Compare the full state the property cares about, not only the state node.** When a guard reads the context, compare the context fields the machine tracks at every step too, not only `state.value`.
5. **Every mutation must fail on a planted bug.** Write a `.mutations` file beside the driver script and run `fv-mutate`. A property that stays green on every planted bug checks nothing.

## Files to write

| File | Holds |
|---|---|
| `<name>.machine.cjs` | The XState machine, and a second machine for the rejected design when one exists. Its header carries `Source read at:` and `Covers:` |
| `<name>.cjs` | The real implementation the paths are tested against: a plain class or function, no XState at runtime |
| `run-paths.cjs` | Generates paths with `getShortestPaths`, replays each against the implementation, and prints the verdict lines |
| `run-paths.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the counterexample and the bounds |

Copy `examples/good/checkout/` to start.

## Workflow

1. **Write the machine first**, with its guards, and confirm by hand which states and context combinations should be reachable.
2. **Write the driver and run it before it asserts anything**, printing each path's events and the state it reaches, to confirm the generated paths are the ones you expect.

   ```bash
   node run-paths.cjs --machine guarded
   ```
3. **Add the comparison**: for each step, `impl.step !== step.state.value`, plus every context field the machine tracks, and print the verdict lines on top.
4. **If a rejected design exists, add its machine and run the same driver against it.** It must find a counterexample.
5. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate run-paths.mutations
   ```

## Reading the output

| Line | Meaning |
|---|---|
| `PASS path <Property>: <events> -> <state>` | The implementation matched every step of this path |
| `FAIL path <Property>: expected <state>, got <state> on <events>` | The implementation diverged from the path at the named step |

## What a pass means

A pass means the implementation matched the machine on every path `getShortestPaths` generated: one path per reachable (state, context) pair, up to whatever event parameters the machine was given. It says nothing about a state the machine cannot reach, and nothing about an event the machine never declares.

## Telling a counterexample

Read the path's events in order and name the step where the implementation and the machine part:

```text
1. The unguarded machine lets NEXT leave "shipping" with no address set, reaching "payment" in two events.
2. The real Checkout class, replayed on that same event sequence, refuses the second NEXT because hasAddress is still false.
3. It stays in "shipping" where the unguarded machine says "payment".
```

## Examples

`examples/INDEX.md` lists every example. `examples/good/checkout/` is the complete pattern: a chosen design checked beside its rejected design, with mutations. `examples/bad/` holds two drivers whose runs pass while they prove nothing.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a path test, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
