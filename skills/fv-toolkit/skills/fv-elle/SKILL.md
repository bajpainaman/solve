---
name: fv-elle
description: "Checks a recorded transaction history for isolation anomalies with elle-cli: G0 through G2, write skew, lost update and the rest of Adya's taxonomy, in polynomial time in the size of the history. Covers list-append and rw-register histories, a header that declares the model and the expected outcome, and a mutations file that plants a known anomaly. Use when the question is whether a real datastore obeys the isolation level the application assumes, for a Jepsen-style history or elle-cli output, or when the formal-verification skill routes here. Not for designing a protocol before it exists (use fv-tlaplus) or for structural rules such as permissions or schemas (use fv-alloy)."
---

# Elle

`elle-cli` takes a recorded history of transaction operations and reports whether it is consistent with a named isolation level, or names the anomaly that breaks it. It checks a real system's behavior, never a design; there is nothing to simulate.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger that this skill encodes.

## Five rules

1. **The anomaly list decides what gets searched for, not the consistency-model label.** `-c` only names the result; declare every anomaly the assumed isolation level forbids, or the check never looks for most of them. See `examples/bad/weak-model/`.
2. **`list-append` and `rw-register` have no delete or update.** A bug that depends on a row leaving a predicate's matching set cannot be posed to either model. See `examples/bad/predicate-anomaly/`.
3. **Every history file declares its own expected outcome**, the way a TLA+ config declares `\* expect:`. A check with no declared outcome cannot fail.
4. **An operation's value is what a real transaction actually read or wrote.** A value chosen to force a cycle, instead of transcribed from a real run, checks the history you wanted, not the one the system produced.
5. **A check that has never failed on a planted anomaly proves nothing.** Ship a history with a known anomaly beside every clean one, and a mutations file that breaks the clean one on purpose.

## Files to write

| File | Holds |
|---|---|
| `<name>.edn` | The recorded operations. Leading `;;` comments carry `Source read at:` and `Covers:`, then the header: `expect`, `model`, `consistency-models`, `anomalies`. A comment above each transaction names what it represents |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the run commands, the bounds and the limits |

Copy `examples/good/list-append-serializable/` to start.

## Workflow

1. **Record the history**, one operation per `:invoke`/`:ok` pair, with real values from the system.
2. **Write the header.** `model` is `list-append`, `rw-register`, or another `elle-cli` model. `anomalies` is every anomaly the claimed `consistency-models` forbids, as a comma-separated list. `expect` is `valid` or `invalid <AnomalyType>`.
3. **Run it.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-elle <name>.edn
   ```

4. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

5. **Read a violation back into the code.** `fv-elle` names the anomaly `elle-cli` found. Follow part 2 of `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md` to connect the operations in the cycle to the transactions that recorded them.

## Reading the output

| Line | Meaning |
|---|---|
| `PASS X.edn: valid` | The declared outcome was `valid`, and `elle-cli` found no anomaly in the declared list |
| `PASS X.edn: invalid A` | The declared outcome named anomaly `A`, and `elle-cli` found it |
| `FAIL X.edn: expected valid, got invalid A` | A candidate bug in the real system, or an anomaly list that is wider than intended |
| `FAIL X.edn: expected invalid A, got valid` | The anomaly the history was built to show no longer reproduces, or the anomaly list no longer covers it |
| `ERROR X.edn: ...` | `elle-cli` could not check the history. This is never a violation |
| `UNAVAILABLE elle: ...` | The jar is missing. The history was not checked |

## Telling a counterexample

Number the operations in the cycle `elle-cli` reports, in the system's own words, one step per operation:

```text
1. Process 0 appends item 10 to cart 1.
2. Process 0 reads cart 2 as empty, which puts process 0 before process 1.
3. Process 1 appends item 20 to cart 2.
4. Process 1 reads cart 1 as empty, which puts process 1 before process 0: a cycle with step 2.
```

## Examples

`examples/INDEX.md` lists every example with its pattern and its lesson.

- `examples/good/list-append-serializable/` is the smallest complete history: a header, a mutations file, and a clean result.
- `examples/good/write-skew/` is the same shape with a real, declared anomaly.
- `examples/bad/` holds histories that pass while they prove nothing, each with the real output and the fix.

## References

| File | Read when |
|---|---|
| `references/anomalies.md` | You pick a model, a consistency level or an anomaly list |
| `references/anti-patterns.md` | You review a history, yours or someone else's |
