# Setup

## Checkers with a skill in this version

| Tool | Install | A good install prints |
|---|---|---|
| TLC 1.7.4, for TLA+ and PlusCal | `${CLAUDE_PLUGIN_ROOT}/scripts/fv-install tla` | `READY tla <path>` |
| Alloy 6.2.0 | `${CLAUDE_PLUGIN_ROOT}/scripts/fv-install alloy` | `READY alloy <path>` |
| Hypothesis | The project's own package manager, for example `uv add --dev hypothesis pytest` | — |

`fv-install` needs a JDK 17 or later. On macOS, `brew install openjdk` provides one. On Debian or Ubuntu, `sudo apt-get install -y openjdk-21-jdk` provides one. The script downloads each jar into `$FV_HOME`, which defaults to `~/.cache/fv`, and verifies it against a pinned SHA-256. Set `JAVA` when `java` on `PATH` is not the JDK you want.

Adding Hypothesis to a project that lacks it is a dependency decision that belongs to the user. Offer it once, with the property you would write, and accept either answer.

### TLC facts, measured on 1.7.4

- TLC exits 0 when it finds no error, 12 on an invariant violation, 13 on a violated temporal property, 11 on a deadlock and 150 on a parse error.
- The `-deadlock` flag switches deadlock checking off. Prefer `CHECK_DEADLOCK FALSE` in the config, where a reader sees it.
- `-simulate file=traces/t,num=50 -depth 20` writes 50 random behaviours, one file each. Simulation mode does not detect deadlocks.
- This release does not accept `-dumpTrace`. `fv-tlc --trace` prints each counterexample as the variables each step changed.
- PlusCal translates with `java -cp ~/.cache/fv/tla2tools.jar pcal.trans Spec.tla`. Commit the translation.

### Hypothesis profile for CI

```python
import os
from hypothesis import settings
settings.register_profile("ci", max_examples=500, derandomize=True, deadline=None)
settings.register_profile("dev", max_examples=100)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```

Pin a failure that Hypothesis finds with `@example(...)`, so that the case stays in the suite.

## Tools without a skill yet

These installs follow each tool's documented path. Pin a version before you rely on one in CI.

### Z3

```bash
pip install z3-solver
python -c "from z3 import *; x=Int('x'); s=Solver(); s.add(x>2,x<4); print(s.check(), s.model())"
# expect: sat [x = 3]
```

### Schemathesis

```bash
pip install schemathesis              # or: uvx schemathesis run <url>
schemathesis run https://example.schemathesis.io/openapi.json   # smoke test
```

### CrossHair

```bash
pip install crosshair-tool
crosshair check mypackage/            # exit 0 = no counterexample found (NOT a proof)
crosshair watch mypackage/            # background mode while you edit
crosshair diffbehavior mod.old_fn mod.new_fn
```

### Kani (Rust repos only)

```bash
cargo install --locked kani-verifier
cargo kani setup
cargo kani                            # runs every #[kani::proof] harness
cargo kani --harness my_harness --default-unwind 8
```

### Dafny

```bash
dotnet tool install --global dafny
dafny verify file.dfy
dafny translate py file.dfy           # emit Python for differential testing
```

Editor: VS Code extension **Dafny**.

### Elle (datastore consistency)

Elle is a Clojure library inside Jepsen.

- **Clojure / Jepsen tests:** add `elle/elle` to your deps and call `elle.list-append/check` on a history.
- **Other stacks:** record histories as EDN or JSON and run a standalone Elle CLI wrapper (e.g. the community `elle-cli` project). Check its `--help` for the history format and the `--model list-append` option.

### Specialists (install only when the trigger appears)

| Tool | Trigger | Install |
| --- | --- | --- |
| Tamarin | Auth / crypto protocol design | `brew install tamarin-prover/tap/tamarin-prover` |
| VeriEQL | SQL rewrite equivalence | clone the research repo; follow its README |
| Cedar CLI / analyzer | Policies written in Cedar | `cargo install cedar-policy-cli` |
| Shuttle / Loom | Rust concurrency tests | `cargo add --dev shuttle` / `cargo add --dev loom` |
| Stateright | Rust actor systems as the model | `cargo add stateright` |
| XState graph | XState-based UIs and workflows | `npm i xstate` (graph utils in `xstate/graph`) |
| Antithesis / DST | Whole-cluster fault testing | commercial (antithesis.com) or hand-built simulator |
