# Anti-patterns and facts measured on cedar-policy-cli 4.14.1

## Anti-patterns

| Anti-pattern | Symptom | Fix / check | Example |
|---|---|---|---|
| A `forbid` rule with a condition narrower than the `permit` it is meant to coexist with | The forbid shadows every case the permit covers, not only the one case it was meant to replace, because an applicable forbid always wins | Give the forbid every attribute condition the exempted case needs | `examples/bad/shadowed-permit/` |
| No test case for the attribute combination a forbid's condition leaves out | The check passes, because nothing asks the question the shadowing would answer wrong | Write a test case for every combination the policy's conditions mention, not only the one the author had in mind | `examples/bad/shadowed-permit/` |
| Treating `cedar validate` as evidence that the decisions are right | A policy set that type-checks against the schema can still produce the wrong decision for every request; validation only checks that attributes and entity types are used consistently | Use `run-tests` with a declared `decision` per request; validation and testing check different things | — |

## Facts measured on this pin

- The published `cedar-policy-cli` binary is not built with the
  experimental `analyze` feature, so `cedar symcc` (symbolic analysis)
  prints `Error: subcommand 'symcc' is experimental, but this executable
  was not built with 'analyze' experimental feature enabled` and exits 1.
  This skill does not use it.
- `run-tests` needs every field in a test case object, including
  `num_errors`; a test case missing it fails before any policy is
  evaluated, with `error: missing field 'num_errors'`.
- `run-tests`' own output has no `FAIL` line: a failing case prints `test
  <name> ... fail: expected <Decision>, got <Decision>` with a lowercase
  `fail`. `${CLAUDE_PLUGIN_ROOT}/scripts/fv-cedar` reprints this as `FAIL
  test <name>: expected <Decision>, got <Decision>`, which is why this
  skill needed a wrapper and `fv-hypothesis` and `fv-tlaplus` do not.
- `-f plain` keeps the per-test summary lines identical to the default
  `-f human` format and drops the box-drawing characters and ANSI colors
  from error diagnostics, which is why the wrapper always passes it.
- A policy or schema that fails to parse never reaches `running N
  test(s)`; `run-tests` exits 1 with only the parse error, no per-test
  line at all. The wrapper reports this as one `ERROR`, not a test
  failure, because no property was actually checked.
- `cedar install`'s version pin is cargo's own: `cargo install
  cedar-policy-cli --locked --version <pin>` rebuilds from crates.io's
  checksummed package, so there is no separate file to verify with a
  SHA-256 the way the tla and alloy jars need one.
