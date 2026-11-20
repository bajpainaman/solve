# Anti-patterns in Tamarin theories

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| A safety lemma's action never fires, because a rule's precondition can never be satisfied (a typo'd constant, a check against the wrong variable) | The lemma reports `verified`, vacuously, and the protocol is still broken | Write an `exists-trace` executability lemma for the same action, and confirm it is `falsified` (found trace), not `verified`. Reproduced in `examples/bad/dead-rule/` |
| A rejected design's rules share a theory with the chosen design's rules | A mutation that only touches one design's rules can still change the other design's lemma, because the Dolev-Yao attacker has both designs' outputs to work with at once | Give the rejected design its own theory file, with its own copy of the shared rules, as `examples/good/signed-challenge/challenge-unbound.spthy` does |
| The nonce or timestamp a lemma depends on is modeled as a public constant instead of `Fr(~n)` | Every "fresh" value is guessable, so a replay lemma can be falsified by a trivial trace that teaches nothing about the real design | Model every freshly generated value with `Fr`, and bind the lemma to the specific fresh term an action carries |
