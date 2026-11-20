# A lemma that holds because the rule it is about can never fire

**Symptom:** `Authentication` reports `verified`, and the protocol is still broken.

## The bug

`Server_Accept`'s check asks for a signature over the fresh nonce `~n`, but `Client_Respond` only ever signs the constant `'ok'`:

```
rule Client_Respond:
  ...
  [ Out(<$A, sign('ok', ltkA)>) ]

rule Server_Accept:
  ...
  --[ Eq(verify(sig, ~n, pkA), true), Accept($S, $A, ~n) ]->
```

`verify(sig, ~n, pkA)` only reduces to `true` when `sig = sign(~n, ltkA)`, and nothing ever produces that term, because `~n` is a fresh name and `'ok'` is a fixed public constant; they are never equal. `Accept` can never fire.

## The real output

```text
$ fv-tamarin dead.spthy
PASS check Authentication: verified
PASS check Executability: falsified
```

The raw tamarin-prover summary this comes from:

```text
Authentication (all-traces): verified (5 steps)
Executability (exists-trace): falsified - no trace found (5 steps)
```

`Authentication` says `All ... Accept(...) ==> ...`, an implication whose premise is never true, so it holds for every trace by vacuous truth. `Executability`, `exists-trace "Ex ... #i. Accept(...) @ i"`, asks tamarin-prover to find even one trace where `Accept` happens at all, and it reports `falsified - no trace found`, which is tamarin-prover's own name for "no such trace exists."

## The fix

Make the server's check match what the client actually signs: `Eq(verify(sig, 'ok', pkA), true)`.

## The check that catches it

An executability lemma, `exists-trace "Ex S A n #i. Accept(S, A, n) @ i"`, beside every `all-traces` safety lemma that mentions the same action. Write one for `Accept` before trusting that `Authentication` verifying means anything.
