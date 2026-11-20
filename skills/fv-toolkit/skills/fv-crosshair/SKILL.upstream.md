---
name: fv-crosshair
description: "Checks a Python function's own contract (pre/post conditions in its docstring) by searching for a counterexample, and compares two functions with `diffbehavior` to find an input where they disagree. Good for a refactor that should preserve behaviour, and for small money, allocation or validation functions. Every check pairs a contract that must hold with one that must be refuted, and 'no counterexample found' is never read as a proof. Use for Python function contracts, comparing an old implementation with a new one, or when the formal-verification skill routes here. Not for HTTP APIs (use fv-schemathesis) or for input generation over the whole domain with no contract on the function (use fv-hypothesis)."
---

# CrossHair

CrossHair reads a function's type hints and its docstring's `pre:`/`post:` lines, then searches for an input that satisfies every precondition and breaks a postcondition. `diffbehavior` instead searches for an input on which two functions disagree. Both run the real code, under CrossHair's own patched interpreter, for a budget of time or iterations.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

## Five rules

1. **"No counterexample found" is a search result, not a proof.** Exit 0 from `crosshair check` means nothing turned up within the time or iteration budget given, never that the property holds for every input.
2. **Write the contract for what the function promises, not only for one property of it.** A contract that checks conservation alone lets a function that gets everything else wrong report `holds`.
3. **CrossHair can only search what it can make symbolic.** It patches `random`, so a bug behind `random.random()` is reachable. A real source of entropy, the system clock or a thread runs for real on each attempt, so a bug behind it is found or missed by chance, not by search.
4. **Compare with `diffbehavior`, not two separate `check` calls.** Two functions can each satisfy a loose contract and still disagree with each other on a real input; `diffbehavior` searches for that input directly.
5. **Pair every check that must hold with one that must be refuted.** A contract nothing can violate is not evidence the code is right. It may mean the contract is too weak, or that nothing has tried to break it yet.

## Files to write

| File | Holds |
|---|---|
| `<name>.py` | The code under check. A `check` target's docstring carries `pre:`/`post:` lines; a `diffbehavior` target needs only type hints. A module docstring carries `Source read at:` and `Covers:` |
| `<name>.crosshair` | The commands: `check <Name> <module.qualname> expect holds\|refuted` and `diff <Name> <module.qualname1> <module.qualname2> expect holds\|differs` |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the bounds and limits |

Copy `examples/good/split-evenly/` to start.

## Workflow

1. **Write the contract on the function itself**, from what it promises its callers, never from the implementation you are about to check.
2. **Run it directly first**, to read CrossHair's own counterexample line before anything wraps it.

   ```bash
   uv run --with crosshair-tool==0.0.113 crosshair check <module.qualname>
   ```

3. **Add the command to a `.crosshair` manifest**, with its declared expectation, and add a `diffbehavior` pair or a rejected design beside it.
4. **Run through the wrapper.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-crosshair <name>.crosshair
   ```

5. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

## Reading the output

| Line | Meaning |
|---|---|
| `PASS check X: holds` | No counterexample to X's contract turned up within the search budget |
| `PASS check X: refuted` | The command declared `expect: refuted`, and CrossHair found one |
| `FAIL check X: expected holds, got refuted` | A counterexample exists. It is printed below the line |
| `PASS diff X: holds` | The two functions agreed on every input CrossHair tried |
| `PASS diff X: differs` | The command declared `expect: differs`, and `diffbehavior` found a disagreement |
| `FAIL diff X: expected holds, got differs` | The refactor changed behaviour. The differing input is printed below the line |
| `ERROR check X: ...` | CrossHair could not import or run the target. This is never a pass |
| `UNAVAILABLE crosshair: ...` | `uv` or the pinned `crosshair-tool` is missing |

## Telling a counterexample

```text
money.py:25: error: false when calling split_evenly_full(2, 2) (which returns [2, 0])
```

Read as the system: splitting 2 cents into 2 shares returns `[2, 0]`. The highest share minus the lowest is 2, past the 1-cent bound the contract states, so this implementation does not split evenly.

## What a pass means

A pass from `check` means CrossHair tried inputs for the stated time or iteration budget and found none that broke the postcondition; it is a search, not an exhaustive check over the function's whole domain, and the budget belongs in the report the same way a TLC run states its scope. A pass from `diffbehavior` carries the same limit, over the smaller space of inputs where two functions might disagree.

## Examples

`examples/INDEX.md` lists every example. `examples/good/split-evenly/` pairs a contract check with a `diffbehavior` comparison between a function and its refactor, plus a rejected design. `examples/bad/weak-contract-reads-as-proof/` and `examples/bad/nondeterministic-code-caps-the-result/` reproduce rules 2 and 3 above.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a CrossHair check, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
