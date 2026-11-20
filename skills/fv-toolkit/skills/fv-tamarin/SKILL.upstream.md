---
name: fv-tamarin
description: "Writes and checks a Tamarin theory (.spthy) of a security protocol against an active Dolev-Yao attacker: authentication, secrecy and replay lemmas, each paired with an executability lemma and, for a rejected design, its own falsified lemma. Use for OAuth/OIDC flows, webhook signature verification, challenge-response and nonce-based auth, key exchange, or when the formal-verification skill routes here. Not for a protocol's timing or deadlines (use fv-tlaplus with a clock variable) or for the business rules of what the protocol unlocks (use fv-alloy or Z3)."
---

# Tamarin: security protocols against an active attacker

tamarin-prover proves or falsifies a first-order trace property over every protocol run an attacker can construct, including message interception, forgery from known material, and replay. It returns a proof of an `all-traces` lemma or a concrete attack trace that falsifies it.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

## Five rules

1. **Every safety lemma about an action needs an executability lemma for that action.** `All ... Accept(...) ==> ...` holds vacuously if nothing ever produces `Accept`. Write `exists-trace "Ex ... #i. Accept(...) @ i"` beside it, and expect it to find a trace. `examples/bad/dead-rule/` reproduces the vacuous case.
2. **Give a rejected design its own theory file**, not a second set of rules in the same file. The Dolev-Yao attacker has every rule in a theory to work with, so a mutation meant to fix one design's rules can be defeated, or can break the other design, through output the other design's rules still produce.
3. **Model every freshly generated value with `Fr(~n)`.** A nonce, key or timestamp written as a public constant is attacker-known from the start, and a lemma about it proves nothing.
4. **Bind what a signature or MAC covers to the exact term the check uses.** `sign(n, ltkA)` signed and `verify(sig, n, pkA)` checked must use the same bound variable; a check against a different term, or a fixed constant, lets any signature the attacker has already seen verify.
5. **Every mutation must fail on a planted bug.** Write a `.mutations` file beside the theory and run `fv-mutate`. A property that stays green on every planted bug checks nothing.

## Files to write

| File | Holds |
|---|---|
| `<name>.spthy` | The theory: roles as rules, lemmas with an `// expect: verified\|falsified` comment directly above each one. Its header comment carries `Source read at:` and `Covers:` |
| `<name>-<rejected>.spthy` | A rejected design, as its own theory, when one exists |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the counterexample and the bounds |

Copy `examples/good/signed-challenge/` to start.

## Workflow

1. **Write the roles as rules**, one rule per message a party sends or receives, with `Fr` for every value that must be unpredictable.
2. **Write the lemma in English first**, then as a guarded formula over the actions the rules already emit.
3. **Run it.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-tamarin <name>.spthy
   ```
4. **Add the executability lemma** for every action a safety lemma mentions, and confirm it finds a trace.
5. **If a rejected design exists, write its own theory file and confirm its lemma is falsified.**
6. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

## Reading the output

| Line | Meaning |
|---|---|
| `PASS check <Lemma>: verified` | tamarin-prover proved the `all-traces` lemma against every trace the rules allow |
| `PASS check <Lemma>: falsified` | The lemma was declared `// expect: falsified`, and tamarin-prover found the counterexample trace |
| `FAIL check <Lemma>: expected <outcome>, got <outcome>` | The lemma's real outcome does not match its `// expect:` comment |
| `UNAVAILABLE tamarin: ...` | tamarin-prover or maude is missing; nothing was checked |

## What a pass means

`verified` is a proof over every trace the rules and the Dolev-Yao attacker can construct, not a search bounded by a step count. `falsified` means tamarin-prover found one concrete trace; say what that trace needs (a specific replay, a specific key reuse) and whether the shipped protocol can produce it.

## Telling a counterexample

Read the rule names the proof search names, in order, and say what each one does in the system's own words:

```text
1. The server issues a fresh challenge to a claimed client, and separately, that client responds once to a challenge of its own.
2. The client's reply never mentions which challenge it answered, so it is the same term no matter which nonce triggered it.
3. The attacker, who already knows that reply, sends it to the server's check for a different challenge.
4. The server accepts, even though the client never responded to this one.
```

## Examples

`examples/INDEX.md` lists every example. `examples/good/signed-challenge/` is the complete pattern: a chosen design checked beside its rejected design, in separate files, with mutations for each. `examples/bad/dead-rule/` holds a theory whose safety lemma passes while it proves nothing.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a theory, yours or someone else's |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
