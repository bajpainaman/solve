# A timeout, fixed by raising the time limit

**Pattern:** pricing, fee, and discount calculation (catalog F3), the kind of concrete arithmetic proof this skill reaches for most often.
**Teaches:** raising `--verification-time-limit` until a check passes is not the same fix as giving the prover less to search for.

## The lemma

`FibConcrete` claims `Fib(36) == 14930352`. Nothing calls `FibConcrete` with a symbolic `n`, and the lemma has no induction; proving it means unfolding the recursive definition of `Fib` 36 levels deep and checking the resulting arithmetic. The `{:fuel Fib,60,61}` attribute lets Dafny unfold that far; without it, Dafny's default fuel stops unfolding before reaching `Fib(36)` and the proof fails for an unrelated reason.

## The real output

At the default time budget, cut to one second to make the point directly, the proof times out:

```text
Slow.dfy(11,24): Error: Verification of 'FibConcrete' timed out after 1 seconds. (the limit can be increased using --verification-time-limit)
   |
11 | lemma {:fuel Fib,60,61} FibConcrete()
   |                         ^^^^^^^^^^^


Dafny program verifier finished with 2 verified, 0 errors, 1 time out
```

```text
PASS Tight.dcfg: failed
```

Raising the limit to 20 seconds makes the same lemma verify, with no other change:

```text
PASS Relaxed.dcfg: verified
```

## Why the artifact is wrong

Nothing about the proof changed between the two runs. Z3 is still searching the same unfolded arithmetic; it simply finished before the clock ran out the second time. Dafny's own error message suggests exactly this fix (`the limit can be increased using --verification-time-limit`), which is reasonable advice for a proof that is merely slow, and a trap for a proof that is slow because of what it is asking Z3 to do: check an exponentially large arithmetic expression by brute force, instead of an inductive argument sized to `n`.

## The fix

Give Dafny the induction it needs instead of more time to search without it: a lemma `FibLowerBound(n: nat) requires n >= 6 ensures Fib(n) >= n`, proved by induction on `n`, replaces the need to unfold `Fib` to a specific literal at all.

## The check that catches the error

None, mechanically. `fv-dafny` with a tight time limit shows the proof is not robust, but nothing here tells you whether a passing run at the default limit (30 seconds) reflects a well-structured proof or one that happened to finish in time on this machine. Treat a proof that needs a raised `--verification-time-limit`, or a `{:fuel}` attribute, as a sign to look for the missing lemma before accepting the new limit.

## Run

```bash
fv-dafny Slow.dfy Tight.dcfg
fv-dafny Slow.dfy Relaxed.dcfg
```
