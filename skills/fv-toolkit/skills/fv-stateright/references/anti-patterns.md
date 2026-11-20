# Anti-patterns and facts measured on Stateright 0.31.0

## Anti-patterns

| Anti-pattern | Symptom | Fix / check | Example |
|---|---|---|---|
| `actions()` never offers an action that `next_state` still handles | The checker explores a smaller state space than the real code allows, and a property that only fires on the missing action's effect never sees a violation | Add a `Property::sometimes` witness for every state the model claims it can reach | `examples/bad/narrow-actions/` |
| No `Property::sometimes` witness at all | The same vacuity as above, with nothing to catch it | Add one witness per interesting state, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes | `examples/bad/narrow-actions/` |
| `Property::always` checked only on the chosen design | A property that no design could ever violate gives the same green result as a property that actually holds | Check the same property on a rejected design too, with `#[should_panic(expected = "<property name>")]`; `examples/good/two-phase-commit/`'s `rms_agree_unilateral` is this |
| `spawn_dfs()` or `spawn_bfs()` with a state space too large to finish | The checker never completes, so nothing was checked, and a timeout looks the same as a long-running pass | Bound the model (fewer actors, fewer steps) until the search finishes in seconds, then widen |

## Facts measured on this pin

- `Model::State` needs `Clone + Debug + Hash + Eq`, and `Model::Action`
  needs `Clone + Debug + PartialEq + Eq + Hash` to satisfy
  `CheckerBuilder::spawn_bfs` and `Checker::assert_properties`; a plain
  `#[derive(Clone, Debug)]` on the action enum is not enough, and the
  compiler error names the missing bound.
- A closure passed to `Property::always` or `Property::sometimes` needs an
  explicit `&Self` and `&Self::State` type on its parameters; `|_, state|
  ...` alone fails to infer with `type annotations needed for &_`.
- `checker.assert_properties()` panics on the first `always` property a
  reachable state violates, printing `Unexpected "<name>" counterexample
  Path[n]:` followed by one `- <Action>` line per step and the state after
  the last one. It also panics if any `sometimes` property was never
  witnessed, with `Discovery for "<name>" not found.`, which is a built-in
  non-vacuity check that TLA+ and Alloy need a separate witness
  config or `run` command to get.
- `cargo test`'s own libtest output already has the shape `fv-mutate`
  needs: a failing `#[test]` function prints `<module>::<name> --- FAILED`,
  and `assert_properties()`'s panic message names the property, so no
  wrapper script was needed for this skill.
- A `#[should_panic(expected = "<property name>")]` test reports
  `test result: ok` when the rejected design's property is violated as
  designed, the same way `fv-tlc` reports `PASS <cfg>: violated P` for a
  witness config.
