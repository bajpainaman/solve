---
name: fv-dst
description: "Writes a small, hand-built deterministic simulator: one seeded scheduler that owns every nondeterministic choice (task order, message delay, loss, duplication, crash and restart), a system under test driven only through that scheduler, invariants checked after every step, and exact replay of any failing seed. Use when the question needs whole-system fault injection across a cluster or a protocol under crashes and message loss, for a hand-written simulation or a seed sweep, or when the formal-verification skill routes here. Not for one process's interleavings without faults (use fv-tlaplus) or for a single function's correctness (use fv-hypothesis)."
---

# Deterministic simulation testing

A deterministic simulator runs the real system logic inside a fake world whose only source of randomness is one seed. Sweeping seeds searches for a fault combination that breaks an invariant, and the seed that found it replays the exact same run on demand. This is a search over real code, not a proof, and it is the right tool when crashes, message loss and timing all have to interact to produce the bug.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

## Five rules

1. **One scheduler owns every nondeterministic choice.** Task order, message delay, loss, duplication, and crash and restart all come from one `random.Random(seed)`. Nothing else in the run reads the wall clock or calls the unseeded `random` module functions.
2. **Create a fresh `random.Random(seed)` inside each run, never one shared across a sweep.** A sweep that advances one RNG object across its iterations reports failing seeds that do not reproduce when replayed alone. `examples/bad/unseeded-rng/` reproduces this.
3. **Every declared fault must actually fire somewhere in the sweep.** A loss or crash probability that a typo wires to the wrong constant leaves the sweep exercising nothing. `examples/bad/fault-never-injected/` reproduces this.
4. **Crash and restart clear only volatile state.** Whatever the real system persists to disk must survive a simulated crash in the model too, or the simulator proves a durability property the real system does not have.
5. **Every mutation must fail on a planted bug.** Write a `.mutations` file beside the simulator and run `fv-mutate`. A property that stays green on every planted bug checks nothing.

## Files to write

| File | Holds |
|---|---|
| `<name>.py` | The scheduler, the system under test, the invariant check, and a CLI with `--sweep N`, `--replay SEED` and (when there is a rejected design) `--policy`. Its header carries `Source read at:` and `Covers:` |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the counterexample and the bounds |

Copy `examples/good/primary-backup/` to start.

## Workflow

1. **Write the scheduler's tick loop first**, with no invariant yet. Run it and read the trace to confirm the faults you intend actually happen.
2. **Write the invariant** and check it after the step where the interesting failure (a crash, a promotion, a handoff) occurs.
3. **Run a sweep**, starting small.

   ```bash
   python3 <name>.py --sweep 500
   ```
4. **If the pattern has a rejected design, run its sweep too**, and confirm it fails. This is the witness that the invariant can be violated at all.
5. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```
6. **Replay any failing seed** and confirm two runs of `--replay SEED` print identical traces.

## Reading the output

| Line | Meaning |
|---|---|
| `PASS sweep <Property>: holds for N seeds` | The invariant held on every one of the N seeds tried |
| `FAIL sweep <Property>: expected holds, got violated at seed S` | Seed S broke the invariant; the trace follows |
| `PASS replay <Property>: holds` | The single replayed seed did not violate the invariant |
| `FAIL replay <Property>: expected holds, got violated` | The single replayed seed reproduced a violation |

## What a pass means

A pass means the invariant held for every seed the sweep tried, within the step bound the run used. It is a search, not a proof: say the seed count and the step count, and say that a seed outside the sweep is unchecked.

## Telling a counterexample

Read the trace in order and name what each step does to the invariant, in the system's own words:

```text
1. At tick 11, the primary appends write 0 and tells the client it succeeded, without waiting for the backup.
2. The replicate message for write 0 reaches the backup only at tick 23, while it is dead, and is dropped.
3. At tick 40, the primary crashes permanently and the backup is promoted.
4. The backup's log has no entry for write 0, even though the client was already told it succeeded.
```

## Examples

`examples/INDEX.md` lists every example. `examples/good/primary-backup/` is the complete pattern: a chosen design checked beside its rejected design, with mutations. `examples/bad/` holds two simulators whose sweeps pass while they prove nothing.

## The hosted alternative

[Antithesis](https://antithesis.com/resources/deterministic_simulation_testing/) runs the unmodified system inside a deterministic hypervisor and injects faults below the application, instead of inside a hand-written scheduler. Reach for it when the system is too large, or spans too many processes and languages, to put behind the pattern in this skill.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a simulator, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
