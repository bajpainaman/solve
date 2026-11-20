# Anti-pattern: a property that holds because the state is unreachable

**Symptom:** the safety property passes, and the witness config fails.

The guard of `Commit` asks for more votes than there are participants, so `Commit` is never enabled. `CommitNeedsAllVotes` holds because `committed` is never true. The property proves nothing about commits.

```text
PASS Holds.cfg: holds (4 distinct states)
FAIL Witness.cfg: expected violated NeverCommitted, got holds
```

## The fix

Correct the guard to `votes = Participants`. Both configs then meet their declared outcomes.

## The check that catches it

The witness. For every state that a safety property talks about, add a config whose invariant says that the state is never reached, with the header `\* expect: violated <Name>`. `fv-tlc` fails that config when the state is unreachable. A typo in a guard, a constant that is too small, and a constraint that cuts the state space all show up this way.
