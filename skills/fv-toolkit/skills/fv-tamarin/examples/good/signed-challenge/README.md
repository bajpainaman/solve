# Signed challenge-response against a Dolev-Yao attacker

**Pattern:** OAuth / OIDC / session protocols; webhook signatures and HMAC verification (catalog E).
**Teaches:** an `expect:` comment per lemma, a rejected design in its own theory, a replay attack as a found trace, mutations on both designs.

## The system

A server sends a client a fresh nonce. The client signs it with its private key; the server accepts once it verifies the signature against the client's public key. `challenge.spthy` is the chosen design: the client signs the nonce itself. `challenge-unbound.spthy` is the rejected design: the client signs a fixed value, never the nonce it was sent.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Every accepted response was a response to that specific challenge | authentication (safety) | `Authentication` |

## Commands

| Command | Design | Expectation |
|---|---|---|
| `fv-tamarin challenge.spthy` | signature covers the nonce | verified |
| `fv-tamarin challenge-unbound.spthy` | signature never covers the nonce (rejected) | falsified |

The second command is the rejected design's check. tamarin-prover finds a concrete replay trace, which is the witness that the authentication failure is reachable.

## Run

```bash
fv-tamarin challenge.spthy
fv-tamarin challenge-unbound.spthy
fv-mutate challenge.mutations
fv-mutate challenge-unbound.mutations
```

```text
PASS check Authentication: verified
```

```text
PASS check Authentication: falsified
```

```text
DETECTED the server stops checking that the signature covers the nonce: FAIL check Authentication: expected verified, got falsified
DETECTED the equality restriction is dropped, so Eq no longer constrains anything: FAIL check Authentication: expected verified, got falsified
GREEN a rule comment is reworded
SUMMARY detected=2 missed=0 error=0 green=1 brittle=0 uncovered=0
```

```text
DETECTED the server is accidentally fixed to check the nonce after all: FAIL check Authentication: expected falsified, got verified
GREEN a rule comment is reworded
SUMMARY detected=1 missed=0 error=0 green=1 brittle=0 uncovered=0
```

## The counterexample, as tamarin-prover found it

tamarin-prover's proof search for `challenge-unbound.spthy`'s `Authentication` ends in `SOLVED // trace found`, needing only one fact the client ever produces: `!KU( sign('ok', ~ltkA) )`, known to the intruder from the `Client_Respond` rule.

```text
1. The server issues a fresh challenge ~n to a claimed client A, and separately, A responds once to any challenge of its own.
2. Because A's reply never mentions which challenge it was answering, that one reply is the constant signature sign('ok', ltkA), the same value no matter which nonce triggered it.
3. The attacker, who already knows this signature from watching A reply once, sends it to the server's check for ~n.
4. The server accepts, because its check only asks whether the signature covers 'ok', which it does, so Accept(S, A, n) holds even though A never responded to this n.
```

## Bounds and limits

Tamarin-prover's search over `all-traces` lemmas is a proof, not a search bounded by a step count: `verified` means no trace violates the lemma under the given rules and the attacker's full Dolev-Yao capabilities, and `falsified` means it found one concrete counterexample, shown above. The model has one server and one client role, no key compromise, and no timestamps; a lemma about a property this theory does not state, such as secrecy of the nonce, is unchecked.
