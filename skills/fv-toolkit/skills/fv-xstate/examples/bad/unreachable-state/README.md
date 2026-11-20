# A state with no incoming transition, never visited and never reported

**Symptom:** the run exits 0 and every line says `PASS`; the one state that matters is simply never mentioned.

## The bug

`broken.machine.cjs` declares a `cancelled` state, but no `on` map in any other state transitions to it:

```js
payment: { type: "final" },
cancelled: { type: "final" }, // BUG: nothing transitions here
```

The intent was a `CANCEL` event from `shipping`. It was never added, the same mistake as a `cancel()` method nothing calls.

## The real output

```text
$ node list-paths.cjs
PASS path reachable: xstate.init -> cart
PASS path reachable: xstate.init -> NEXT -> shipping
PASS path reachable: xstate.init -> NEXT -> SET_ADDRESS -> shipping
PASS path reachable: xstate.init -> NEXT -> SET_ADDRESS -> NEXT -> payment
4 states reached; the machine declares cart, shipping, payment, cancelled
```

`getShortestPaths` returns one path per state it can reach from the initial state. A state with no incoming transition has no path, so it has no line in this output, and nothing here says that one of the four declared states was skipped. The exit code is 0.

## The fix

Add the missing transition, for example `CANCEL: "cancelled"` on `shipping`'s `on` map, and confirm the path count rises to match the number of declared states (or that each excluded state is excluded for a reason the README names).

## The check that catches it

None of this project's checks catch it mechanically, because `fv-mutate` only detects a mutation that makes a declared property fail, and no property here claims that every declared state is reachable. Catching this needs a check written for the harness: compare the number of distinct state values in the generated paths against the machine's own declared state names, and fail when one is missing.
