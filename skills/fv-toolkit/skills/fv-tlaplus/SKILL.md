---
name: fv-tlaplus
description: "Writes and checks a TLA+ model of a protocol with TLC: orderings between actors, retries, crashes, message loss, leases and lifecycles. Covers the model, one config per design with a declared outcome, witnesses, mutations, and reading a counterexample back as numbered steps. Use when the question is whether a bad interleaving can happen, for .tla or .cfg files, TLC output or PlusCal, or when the formal-verification skill routes here. Not for questions about the shape of data (use fv-alloy) or for functions with no concurrency (use fv-hypothesis)."
---

# TLA+ with TLC

TLC tries every ordering of the steps in a small model and returns the shortest sequence that breaks a property. Use it when a bad ordering is the risk: two actors, a retry, a crash between two writes, a message that arrives twice or late.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger that this skill encodes.

## Five rules

1. **One action per atomic step in the code.** A read and a later write are two actions. A region under one lock, or one SQL statement, is one action. One action per function hides every interleaving inside the function.
2. **Every config declares its outcome, and every model has a witness.** The first line of a config is `\* expect: holds`, `\* expect: violated <Invariant>`, `\* expect: liveness` or `\* expect: deadlock`. A witness config checks an invariant that says the interesting state is never reached, and it must be violated.
3. **Design choices and faults are constants.** Write one config per design and per fault setting. Name each config for its mechanism, such as `CheckThenRefund`, and never for a verdict.
4. **Liveness needs the fairness that the code provides.** Give weak fairness to steps that the system keeps trying. Give none to a fault or to an optional user action.
5. **Run after every edit, with tiny constants.** Two or three actors and one or two faults find most design bugs. Widen only after the small model is right.

## Files to write

Put the files in one directory beside the code they describe.

| File | Holds |
|---|---|
| `<Name>.tla` | The model. Its header comment carries `Source read at:` and `Covers:`, the knobs and the assumptions. Each action has a comment that names the function it transcribes |
| `<Mechanism>.cfg` | One per design and per fault setting, with the `\* expect:` header on the first line |
| `Witness<State>.cfg` | One per interesting state, with `\* expect: violated <Never...>` |
| `<Name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the config table, the run commands, the bounds and the limits |

Copy `examples/good/refund-race/` to start. It has every file in this table.

## Workflow

1. **Write the header and the variables.** Keep only the state that a property mentions, plus one variable per fault switch. Follow `references/modeling.md`.
2. **Write `Init` and one action, then run.** Add one action at a time. Put `UNCHANGED` on every variable that the action leaves alone.

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-tlc <Name>.tla
   ```

3. **Give the end state a `Done` action.** `Done` is true only in a correct end state and changes nothing. Deadlock checking then stays on, and a real stall still shows up as a deadlock.
4. **Encode the ledger.** A safety property becomes an operator under `INVARIANT`. A liveness property becomes a temporal formula under `PROPERTY`, checked with a `SPECIFICATION` that includes fairness. Put one temporal property in a config when you must know which one failed, because TLC does not name it.
5. **Write the configs.** Add one for the design you chose, one for each design you rejected, and one witness for each interesting state.
6. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <Name>.mutations
   ```

7. **Read each violation back into the code.** `fv-tlc --trace` prints each counterexample as the variables each step changed. Follow part 2 of `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md`.
8. **Link the model to the code.** `fv-replay` writes a pytest file that drives the code through a counterexample. `fv-conform` checks a recorded run of the code against the spec. `examples/linking/` shows both.

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-replay <Name>.tla <Mechanism>.cfg -o test_replay_<mechanism>.py
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-conform <Name>.tla <Mechanism>.cfg run.jsonl
   ```

## Reading the output

| Line | Meaning |
|---|---|
| `PASS X.cfg: holds (n distinct states)` | TLC tried every ordering at this config's sizes and found no violation |
| `PASS X.cfg: violated P` | The config declared this violation, and TLC found it |
| `FAIL X.cfg: expected holds, got violated P` | A candidate bug, or a gap in the model. The reduced trace follows |
| `FAIL X.cfg: expected violated P, got holds` | A rejected design passes, or a witness state is unreachable. The model cannot produce the failure it should |
| `ERROR X.cfg: ...` | TLC could not check the spec. Fix the spec. This is never a violation |
| `UNAVAILABLE ...` | Java or the jar is missing. The spec was not checked |

When the config for the chosen design fails, investigate before you touch the model. That result is the most valuable one.

## Telling a counterexample

Rewrite the reduced trace as numbered steps in the system's own words, one step per action, and give each step its `file:line`:

```text
1. Both jobs are idle and nothing is refunded.
2. Job a reads 10 refundable.            refunds.py:41
3. Job b reads 10 refundable.            refunds.py:41
4. Job a refunds 10.                     refunds.py:47
5. Job b refunds 10. The customer has 20 back on a payment of 10.
```

The user asks one question of each step: can my system really do this?

When the `statechart` skill of the pstack plugin is installed, use it to draw the checked model as a chart in the user's words. Refer to it by name, and copy none of its commands into your files.

## Examples

`examples/INDEX.md` lists every example with its pattern and its lesson. Read the one closest to your case.

- `examples/good/refund-race/` is the smallest complete model: a knob, three configs, a witness and mutations.
- `examples/good/idempotent-receiver/` adds a crash fault with a switch, and liveness under a bounded fault.
- The other folders under `examples/good/` are templates, one per pattern: transactional outbox, orchestrated saga, two-phase commit, leader election, lease fencing, reconciler, cache invalidation, CDC snapshot handoff, DAG scheduler, watermark cursor and release ordering. Start from the template whose pattern matches the claim, and keep its knob, its configs and its witness.
- `examples/linking/` replays a counterexample against real code and validates a recorded run against the spec.
- `examples/bad/` holds models that pass while they prove nothing, each with the checker output and the fix. Read `bad/merged-atomicity/` before you write your first action.

## References

| File | Read when |
|---|---|
| `references/modeling.md` | You write or review a model |
| `references/gotchas.md` | TLC gives a result you did not expect |
| `references/refactors.md` | You split an action or add a variable |
| `references/anti-patterns.md` | You review a model, yours or someone else's |
| `references/apalache.md` | TLC cannot finish on the constants you need, or an invariant must be shown inductive. `fv-install apalache` installs the checker |
