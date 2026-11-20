# Anti-pattern: an unbounded state space

**Symptom:** TLC never finishes, and prints nothing while it runs.

Nothing in `Next` stops `x` from growing. `Init` and `Next` admit the behaviour `x = 0, 1, 2, 3, ...` without end, so the set of reachable states is infinite. TLC explores states breadth-first and only reports a result after the search completes, so a search with no end never reports anything.

```text
$ fv-tlc UnboundedCounter.tla Unbounded.cfg > out.txt 2>&1 &
pid=$!
$ sleep 8 && kill -0 "$pid" && echo "still running after 8s"
still running after 8s
$ cat out.txt
```

Eight seconds in, the process is still running, and `out.txt` is empty. `fv-tlc` buffers the checker's output until it exits, and this one never does.

## The fix

Add a `CONSTRAINT` that keeps the search finite:

```tla
Bounded == x <= Max
```

```text
PASS Bounded.cfg: holds (6 distinct states)
```

`Bounded.cfg` sets `Max = 5` and adds `CONSTRAINT Bounded`, and the check finishes immediately, exploring the six states `x = 0` through `x = 5`. A `CONSTRAINT` removes behaviours from the search rather than describing the design, so the report that ships with a bounded check has to name what it excludes: here, any state with `x > Max`, which means this check says nothing about what happens once the real counter passes 5.

## The check that catches it

None of this model's own commands catch an unbounded state space, because the command never returns a wrong answer, it returns no answer. The catch is operational: run the check with a time budget, and treat "still running" past that budget the same way a `FAIL` is treated, as a check that cannot be trusted to finish. `tests/examples.d/tlaplus_bad.sh` runs the unbounded config in the background and confirms it is still alive after five seconds, rather than waiting on it.
