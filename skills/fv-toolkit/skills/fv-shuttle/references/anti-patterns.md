# Anti-patterns and facts measured on Shuttle 0.9.10 / Loom 0.7.3

## Anti-patterns

| Anti-pattern | Symptom | Fix / check | Example |
|---|---|---|---|
| A plain `#[test]` with real OS threads on racy code | The test passes, because thread creation costs far more than the race window it is trying to hit | Run the same code under `--cfg shuttle` or `--cfg loom` instead of leaving scheduling to the OS | `examples/bad/plain-threads/` |
| Joining a thread before spawning the next one | Loom's search is exhaustive over a state space that no longer contains any overlap | Spawn every thread first, then join every handle | `examples/bad/narrow-loom/` |
| Only one iteration of `shuttle::check_random` | A random search over one schedule is not a search | Call `check_random` with enough iterations that the state space is actually sampled; this skill's example uses 200 for a two-thread race | — |
| Testing under only one of the two schedulers | Shuttle can miss a rare interleaving that Loom's exhaustive search would find, and Loom checks nothing that Shuttle's model does not also admit | Run both; `examples/good/counter/` does | — |

## Facts measured on this pin

- `shuttle = "0.9.10"` and `loom = "0.7.3"` select their own sync and atomic
  types; replace `std::sync` and `std::sync::atomic` with `shuttle::sync` or
  `loom::sync` behind `#[cfg(shuttle)]` and `#[cfg(loom)]`, and gate `std`
  behind `#[cfg(not(any(loom, shuttle)))]`. `thread::spawn` and `Arc` need
  the same three-way gate; only `loom::sync::Arc` and `shuttle::sync::Arc`
  are instrumented, not `std::sync::Arc`.
- Selecting a scheduler is a compiler flag, not a feature: run
  `RUSTFLAGS="--cfg shuttle" cargo test` or `RUSTFLAGS="--cfg loom" cargo test`.
  Plain `cargo test` builds neither path; gate a fallback test behind
  `#[cfg(not(any(loom, shuttle)))]` if the crate should still have something
  to run with no flag.
- rustc's `unexpected_cfgs` lint does not know about `shuttle` or `loom` by
  default and warns on every use; `[lints.rust] unexpected_cfgs = "allow"`
  in `Cargo.toml` silences it.
- On this machine (cargo and rustc 1.94.1), `loom 0.7.3`'s dependency
  `generator 0.8.12` requires rustc 1.95 and fails to build. `cargo update -p
  generator --precise 0.8.11` resolves to a version that builds on 1.94.1;
  both example `Cargo.lock` files pin it. A newer rustc may not need this.
- `shuttle::check_random(f, n)` runs `f` under `n` random schedules and
  panics on the first one that fails; it prints a seed that
  `shuttle::check_random_with_seed` or the `SHUTTLE_RANDOM_SEED` environment
  variable replays. `loom::model(f)` runs `f` under every schedule Loom's
  model admits and panics on the first failure, with no seed to replay
  because the search is deterministic.
- A shared `CARGO_TARGET_DIR` reused across a crate copy that still has a
  stale, previously mutated source tree can serve a cached test binary built
  from that other tree instead of rebuilding. `fv-mutate` only ever builds
  from its own fresh copy of one example's root, so this does not affect a
  single `fv-mutate` run; it is a hazard only when a target directory is
  shared with some other, hand-edited copy of the same crate name.
