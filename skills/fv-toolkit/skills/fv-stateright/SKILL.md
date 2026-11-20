---
name: fv-stateright
description: "Checks a Rust actor or state-machine protocol by implementing Stateright's Model trait and exploring every reachable state with its checker: two-phase commit, leader election, quorum reads and writes, or any protocol where the model is meant to run as the real code later. Finds the shortest counterexample for a violated property and a witness that the interesting state is reachable at all. Use for a Rust protocol between a few actors, a linearizability or consensus question, or when the formal-verification skill routes here. Not for a design with no Rust code yet (use fv-tlaplus), or for a single-process data structure under a scheduler (use fv-shuttle)."
---

# Rust protocols with Stateright

Stateright explores every state a `Model` implementation can reach and
checks a property against each one, the same way TLC explores a TLA+
spec. Unlike TLA+, the model is Rust, so the same `Model` can later drive
the real networked actors. Use it for a protocol between a few actors:
two-phase commit, leader election, a replicated register.

If you came here directly, run steps 1 to 3 of the `formal-verification`
skill first. They produce the claims table and the confirmed property
ledger that this skill encodes.

## Five rules

1. **`actions()` must offer every action `next_state` handles.** An action
   variant that `actions()` never pushes is a state the checker can never
   reach, no matter how exhaustive its search otherwise is; see
   `examples/bad/narrow-actions/`.
2. **Every property needs a `Property::sometimes` witness** for the state
   it is meant to guard, so a model that cannot reach that state fails
   loudly instead of passing by accident.
3. **Check a rejected design too, with `#[should_panic(expected = "<name>")]`.**
   A property that no design in the crate could ever violate gives the
   same pass as a property that holds; `examples/good/two-phase-commit/`'s
   `rms_agree_unilateral` is the witness that `rms_agree` can fail.
4. **Bound the model until the checker finishes in seconds.** `spawn_bfs`
   is exhaustive within the actions and states it is given; widen the
   bound only after the small model is right.
5. **Every property must fail on a planted bug.** Write a `.mutations`
   file and run `fv-mutate`. A property that stays green on every planted
   bug checks nothing.

## Files to write

Put the files in one crate beside the code they describe, or in the crate
itself when the protocol under test is the crate.

| File | Holds |
|---|---|
| `Cargo.toml` | `stateright` as an exact-pinned dependency |
| `src/lib.rs` | One `Model` impl per design: the chosen one and at least one rejected one. Its header comment carries `Source read at:` and `Covers:`, and each `next_state` arm has a comment naming the step it transcribes |
| Tests, inline or under `tests/` | One test per design, named for the property; the chosen design's test calls `assert_properties()` directly, a rejected design's test wraps the same call in `#[should_panic(expected = "<property>")]` |
| `<Name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `Cargo.lock` | Committed, so the pinned crate version never drifts between runs |
| `README.md` | The property ledger, the checks table, the run commands, a counterexample, the bounds and limits |

Copy `examples/good/two-phase-commit/` to start.

## Workflow

1. **Write the state, the actions and `init_states` first**, shared by
   every design so they stay comparable.
2. **Write the chosen design's `next_state`** and one `Property::always`
   per safety claim, plus one `Property::sometimes` per state the design
   must be able to reach.
3. **Run it**, with the build output outside the crate so a later copy of
   it stays small:

   ```bash
   export CARGO_TARGET_DIR="${FV_HOME:-$HOME/.cache/fv}/stateright/target/<name>"
   cargo test --quiet --lib
   ```

4. **Write the rejected design's `next_state`**, reusing the same actions
   and the same `Property::always`, and check it with
   `#[should_panic(expected = "<property>")]`.
5. **Plant bugs in the chosen design.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <Name>.mutations
   ```

6. **Read each failure.** The panic names the property and prints the
   shortest path of actions that reaches the violating state.

## Reading the output

`cargo test`'s own output already has the shape `fv-mutate` and this
skill's tests need, with no wrapper script.

| Line | Meaning |
|---|---|
| `test result: ok. N passed; 0 failed...` | Every property held on every state the checker reached |
| `<module>::<test> --- FAILED` | A property was violated, or a `sometimes` witness was never satisfied; the panic above it names which |
| `Unexpected "<name>" counterexample Path[n]: ...` | The shortest sequence of actions that reaches a state violating property `<name>` |
| `Discovery for "<name>" not found.` | A `sometimes` witness never happened; the model is too narrow, not correct |
| a compile error, no `FAILED` line | The model or a trait bound is wrong; fix it before trusting any run |
| `UNAVAILABLE stateright: ...`, exit 3 | cargo is missing; nothing was checked |

## Telling a counterexample

Rewrite the counterexample path as numbered steps in the system's own
words, one step per action:

```text
1. Both RMs are Working.
2. RM 0 aborts on its own.                 AbortUnilaterally(0)
3. RM 1 prepares.                          Prepare(1)
4. RM 1 commits without checking RM 0.     Finish(1)
```

## What a pass means

A pass means the checker explored every state reachable from `init_states`
through `actions()`, within whatever bound the test gives `spawn_bfs` (or
`spawn_dfs`), and found no violation. It is exhaustive within that bound
and those actions, not a proof over an unbounded protocol, and a model
that never drives the real actors is still a design, not a code link.

## Examples

`examples/INDEX.md` lists every example. `examples/good/two-phase-commit/`
is the smallest complete one: two designs sharing one set of actions, a
`#[should_panic]` witness, and a mutations file that plants a bug in the
checked rule and a second one in its input.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a Stateright model, yours or someone else's, or need a fact measured on the pinned version |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
