# Dafny anti-patterns

Each row is a way a proof passes while it proves nothing, with the symptom and the fix.

| Anti-pattern | Symptom | Fix / check | Source |
| --- | --- | --- | --- |
| `assume false`, or any `assume` with no `{:axiom}`, inside a method body | `N verified, 0 errors`, with a warning the exit code does not reflect | Delete the `assume`; prove the real postcondition, or correct it to what the method does | `examples/bad/unsound-proof/AssumeFalse.dfy` in this plugin |
| A `requires` clause no input can satisfy | `N verified, 0 errors`, with no warning at all | Narrow or correct the precondition to the inputs the caller actually passes | `examples/bad/unsound-proof/ContradictoryPrecondition.dfy` in this plugin |
| Raising `--verification-time-limit`, or a function's `{:fuel}`, until a proof passes | The proof still depends on brute-force search finishing in time, on this machine, with this Z3 version | Find the lemma or induction the proof is missing; a well-structured proof does not get slower as unrelated code changes | `examples/bad/masked-timeout/` in this plugin, and [Dafny's own suggestion in the timeout message](https://github.com/dafny-lang/dafny), which names the limit, not the proof, as the thing to change |
| A differential reference derived from the Dafny source, by copying it into another language | The reference cannot disagree with the proof, so the test checks that a translation is syntactically faithful, not that the specification is right | Write the reference from the same informal description the Dafny model was written from, independently | [Cedar's Lean-vs-Rust differential testing](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development), which keeps the two implementations in separate languages for the same reason |
| Any proof shipped without a mutations file | No evidence the proof, or the differential test built on it, would have caught a real regression | Plant the bug in the hand-written reference, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes | `${CLAUDE_PLUGIN_ROOT}/references/bite.md` |

## A symptom and where to look first

| Symptom | Look at |
|---|---|
| A method verifies and you expected a failure | An `assume` first, then whether the precondition is satisfiable |
| A method fails to verify and you did not expect it | The loop invariants, then whether a lemma is missing for a step Z3 cannot see on its own |
| A method verifies only above a certain `--verification-time-limit` or `{:fuel}` | The proof strategy, not the limit. Look for an inductive lemma that replaces the search |
| The compiled core and the reference disagree on a specific `(total, n)` | Which one matches the informal description, not which one is "the proof" |
