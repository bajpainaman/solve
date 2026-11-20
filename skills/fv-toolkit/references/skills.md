# Tools that have a skill

Pick the row whose question matches the claim, load that skill, and install the tool if it is missing. `fv-install <name>` installs one tool. `fv-install` with no argument installs the two core jars.

## Core tools

| The question is | Tool | Skill | Install |
|---|---|---|---|
| Can a bad ordering happen? Concurrency, retries, crashes, message loss, leases | TLA+ with TLC | `fv-tlaplus` | `fv-install tla` |
| Can the data or the configuration reach an invalid shape? Relations, permissions, ownership, compatibility | Alloy 6 | `fv-alloy` | `fv-install alloy` |
| Is this Python code correct for every input, or for every sequence of calls? | Hypothesis | `fv-hypothesis` | The project's package manager |

## On-demand tools

Each of these tools installs when it is named. Load its skill first, because the skill says what the installer needs.

| The question is | Tool | Skill | Install |
|---|---|---|---|
| Does a rule table, a policy or a set of numeric constraints have a gap, an overlap or a contradiction? Arithmetic and boolean conditions over a few variables | Z3 | `fv-z3` | `fv-install z3` |
| Does a running HTTP API keep to its OpenAPI schema, for single requests and for sequences of calls such as create, get, delete? | Schemathesis | `fv-schemathesis` | `fv-install schemathesis` |
| Do two versions of a pure Python function ever disagree, or does one small pure function break its own contract on some input? | CrossHair | `fv-crosshair` | `fv-install crosshair` |
| Can real Rust code deadlock or lose an update under some thread interleaving? | Shuttle and Loom | `fv-shuttle` | `fv-install shuttle` |
| Does a protocol that is written in Rust hold under every message interleaving, when the checked model must be the Rust code itself? | Stateright | `fv-stateright` | `fv-install stateright` |
| Does a Cedar policy set allow and deny what it should, and does a policy change widen access? | Cedar | `fv-cedar` | `fv-install cedar` |
| Can a Rust function panic, overflow or index out of bounds on some input? | Kani | `fv-kani` | `fv-install kani` |
| Does the real code of a distributed system survive crashes, restarts, message loss and reordering, with every failure replayable from a seed? | Deterministic simulation | `fv-dst` | `fv-install dst` |
| Does a UI flow or a workflow implementation follow its state machine through every reachable path? | XState graph | `fv-xstate` | `fv-install xstate` |
| Can an active attacker forge, replay or redirect messages in a security protocol? | Tamarin | `fv-tamarin` | `fv-install tamarin` |
| Do two SQL queries return the same rows on every table, with NULLs and duplicates included? | Bounded check on SQLite | `fv-sqlequiv` | `fv-install sqlequiv` |
| Does a TLA+ invariant hold when TLC cannot enumerate the states, such as wide integer ranges, or is an invariant inductive? | Apalache | `fv-tlaplus`, with its `references/apalache.md` | `fv-install apalache` |
| Does a recorded history of database transactions break an isolation level such as serializability or snapshot isolation? | Elle | `fv-elle` | `fv-install elle` |
| Must a small algorithm be proved correct for every input, with no bound on the input? | Dafny | `fv-dafny` | `fv-install dafny` |

A tool that is not in this file has no skill yet. Read `tools.md`, say that no skill covers the tool, and follow the router's workflow from the tool's own documentation.
