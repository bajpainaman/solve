# Linking a model to the real code

A model that is never tied to code drifts. Datadog found a year-old bug, conflicting placements in under 0.01% of cases that crashed backfill recovery, only after it started checking production telemetry against its TLA+ specs continuously ([Datadog, Nov 2026](https://www.datadoghq.com/blog/engineering/continuous-formal-spec-validation)). Every model the skill writes should therefore ship with at least one of these links.

| Technique | Direction | How it works | Tooling | Use when |
| --- | --- | --- | --- | --- |
| Model-based testing (MBT) | Model → code | Generate traces from the model; a driver replays each action on the implementation and compares state after every step | `quint run --mbt` + quint-connect (Rust, TS); Hypothesis stateful; XState graph; Schemathesis | You can call the implementation's operations directly in a test |
| Counterexample → regression test | Model → code | Translate each violating trace into a deterministic test that forces the same interleaving | Hand-written driver; quint-connect saves failing traces as replayable files | Every time the checker finds a bug |
| Trace validation | Code → model | Log events from real runs, merge logs, check that some spec behavior matches the trace | TLC trace specs ([Kuppe et al.](https://conf.tlapl.us/2024/MarkusAKuppe-ValidatingSystemExecutionsWithTheTLAPlusTools.pdf)); MongoDB, CCF, etcd used it | Distributed code you can instrument but not drive step-by-step |
| Runtime monitoring | Code → model, continuously | Compile spec actions into monitors that check preconditions on live telemetry | FETCh (TLA+ → Rust, ~2% p90 CPU overhead on 1,300 pods); PObserve for P | Long-lived systems where implementations evolve |
| Differential random testing | Both ways | Executable reference model and production code run on millions of random inputs; outputs must match | Cedar: Lean model vs. Rust; Lean evaluates an input in ~5 µs vs. 7 µs for Rust ([AWS](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development)) | Pure functions: evaluators, calculators, policy engines |
| Deterministic simulation testing | Code under faults | Run the whole system in a deterministic simulator or hypervisor, inject faults, replay any failure by seed | Antithesis; TigerBeetle VOPR; FoundationDB simulation | Systems where concurrency and faults dominate |
| Black-box history checking | Code → consistency model | Record client operations, check histories for anomalies | Jepsen + Elle; Stateright and Porcupine for linearizability | Databases and anything claiming an isolation or consistency level |
| Refinement | Model → model | Prove or check that a detailed model implements an abstract one | TLA+ refinement (Cosmos DB); Anvil/Verus for code | Layered designs; keeping a monitorable spec and a checkable spec in sync |

**Practical defaults for the skill:**

- Python services: Hypothesis stateful tests as the driver, TLC random traces as input (`-simulate file=…,num=N` writes one file per behaviour; a small adapter maps each step to a method call), CrossHair for contracts.
- TypeScript: fast-check + `fc.commands` or XState graph.
- Rust: Kani, plus Shuttle/Loom or Stateright when the specialist trigger applies.
- Distributed services you can't drive directly: structured event logs → TLA+ trace validation, then a runtime monitor once stable.

**Trace-validation pitfalls to encode:** implementations are finer-grained than specs, so log at the spec's atomicity; when logs come from separate nodes, use logical or vector clocks; a failed validation can mean a bad log mapping, not a bug, so check the mapping first ([Demirbas on CCF](https://muratbuffalo.blogspot.com/2025/02/smart-casual-verification-of.html)).

## Scripts for the two links you will use most

| Script | Direction | What it does |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}/scripts/fv-replay` | Model to code | Turns a TLC counterexample into a pytest file. A driver that you write once maps each action to a call on the code, and the test checks the property after every step |
| `${CLAUDE_PLUGIN_ROOT}/scripts/fv-conform` | Code to model | Takes a log of a real run, one JSON line per step, and asks TLC whether some behaviour of the spec matches it |
| `${CLAUDE_PLUGIN_ROOT}/scripts/fv-tlc --json` | Model to anything | Prints each counterexample as parsed states, for a driver in another language |

`${CLAUDE_PLUGIN_ROOT}/skills/fv-tlaplus/examples/linking/README.md` shows both scripts on one small service.
