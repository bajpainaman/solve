# Anti-patterns and facts measured on Kani 0.68.0

All facts below were measured by running the pinned Kani in Docker
(`rust:1.99.1-slim-trixie`, rustup, `cargo install --locked kani-verifier
--version 0.68.0`, `cargo kani setup`), because this development
machine's cargo has no rustup. The report says which commands this
covers.

## Anti-patterns

| Anti-pattern | Symptom | Fix / check | Example |
|---|---|---|---|
| No `#[kani::unwind(N)]` on a loop bounded by a symbolic value | The harness unwinds one more iteration at a time and never reaches a verdict | Bound the loop and `kani::assume` the input to within the bound | `examples/bad/unbounded-loop/` |
| `kani::assume` not derived from how the function is actually called | The proof passes because it never explores the input where the bug lives | Build the assume from the real callers' input domain, as rule 2 says | `examples/bad/narrow-assume/` |
| A property that forces the solver to relate several division results across loop iterations | The harness that correctly computes each part one at a time still took minutes per run in this environment, instead of the usual sub-second-to-low-seconds Kani run | Check a property that holds per iteration (a bound), not one that needs the solver to reconstruct a global arithmetic fact (a sum across iterations) | `examples/good/allocate-bonus/` checks a bound, not conservation, for this reason |

## Facts measured on this pin

- `cargo kani` reports a harness's result with `VERIFICATION:- SUCCESSFUL`
  or `VERIFICATION:- FAILED`, never naming the harness on that line. A
  failure also prints one `Failed Checks: <description>` and `File:
  "<path>", line <n>` pair per failed check, and the per-harness name
  only appears in `Checking harness <name>...` at the start and
  `Manual Harness Summary: Verification failed for - <name>` at the end.
  Neither `FAIL` line (case-sensitive) carries the harness name on the
  same line, so `${CLAUDE_PLUGIN_ROOT}/scripts/fv-kani` wraps `cargo kani
  --harness <name>` to produce one.
- `kani::cover!(condition, "label")` adds a check reported as `Check N:
  <harness>.cover.<n>` with `- Status: SATISFIED` or `UNSATISFIED` and
  `- Description: "<label>"`. The overall summary adds a line `** X of Y
  cover properties satisfied` separate from the ordinary pass/fail count.
- Kani's own automatic checks (array bounds, arithmetic overflow,
  unreachable code, and safety checks inside standard library functions
  the harness calls, such as `PartialOrd` on `usize`) dominate the check
  count. A harness with three `assert!` calls and one `kani::cover!`
  still produced 55 checks in `examples/good/allocate-bonus/`.
- `cargo kani` ignores `CARGO_TARGET_DIR` and always writes to
  `<crate>/target/kani/`, unlike plain `cargo build` or `cargo test`.
  `fv-mutate` leaves a crate's `target/` out of its copy, so each mutation
  check rebuilds from a cold cache.
- The published Kani release bundle for `aarch64-unknown-linux-gnu`
  needs glibc 2.39 or newer; Debian bookworm (glibc 2.36) cannot run it,
  and Debian trixie (glibc 2.41) can.
- `cargo kani setup` downloads a Kani-specific nightly toolchain and
  registers it with rustup; it fails outright on a cargo installation
  that has no rustup, which is this development machine's state.
