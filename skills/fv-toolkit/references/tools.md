# Tools

`skills.md` lists the tools that have a skill. For any other tool in this file, say that no skill covers it yet, follow the same loop from the tool's own documentation, and install it as `setup.md` describes.

## Core toolkit

After the review, the ~35 tools above reduce to **9 core tools plus 7 opt-in specialists**. Most of the rest are the same technique in a different syntax or language. The skill should install and template only the core set, and reach for a specialist only when its trigger applies.

### Substitution groups

| Job | Substitutable tools | Keep | Why this one | Drop / demote |
| --- | --- | --- | --- | --- |
| Behavioral model checking | TLA+ (TLC, Apalache), PlusCal, Quint, P, FizzBee, Spin, NuSMV, Event-B, UPPAAL | **TLA+** (PlusCal allowed inside it) | Same semantics as Quint and covers what P and FizzBee do; the only one with trace validation, runtime monitors (FETCh), proofs (TLAPS), and a large corpus of real specs (Raft, Kafka, Cosmos DB) to template from | Quint: same semantics, nicer syntax and MBT. Switch to it *instead of* TLA+ if readability matters more, never alongside. P, FizzBee, Spin, NuSMV, Event-B dropped. UPPAAL → model clocks in TLA+ |
| Structural / relational modeling | Alloy 6, TLA+ (sets), Z3 | **Alloy** | Relations, permissions, and schemas are its native shape; instant visual counterexamples | Use Alloy for structure only; its temporal mode duplicates TLA+ |
| Constraint / rule / policy solving | Z3, cvc5, Zelkova-style encodings, Cedar analyzer | **Z3** | Python API; same SMT core the AWS policy tools use | cvc5 dropped; Cedar analyzer is a specialist |
| Property-based + stateful testing | Hypothesis, fast-check, proptest, jqwik, QuickCheck | **Hypothesis** (+ the one PBT library per other language in use) | Stateful `RuleBasedStateMachine` doubles as the MBT driver | Libraries for languages you don't ship |
| API contract testing | Schemathesis, Hypothesis by hand | **Schemathesis** | Generates tests from the OpenAPI spec you already have | — |
| Function contracts on code | CrossHair, Nagini, Gobra, Liquid Haskell, Stainless, Frama-C, CBMC | **CrossHair** for Python; **Kani** for Rust | Push-button counterexamples on real code | Per-language verifiers kept only for the language in use; Nagini/Gobra demoted |
| Proof of critical cores | Dafny, Lean 4, Rocq, Isabelle, F\*, Verus, Prusti, Creusot | **Dafny** | Most automation for small cores; compiles the model to Python/JS/Go for differential testing | Lean when proofs outgrow Dafny (Cedar's reason for moving); the rest dropped |
| Consistency checking of datastores | Jepsen + Elle, Porcupine, Knossos, Stateright tester | **Elle** | Checks many isolation levels from one history, in polynomial time | Others dropped |
| Model ↔ code conformance | TLC trace validation, FETCh, PObserve, quint-connect, Hypothesis MBT | **TLC trace validation + Hypothesis-driven MBT** | Both hang off the chosen TLA+ model | PObserve goes with P; quint-connect goes with Quint |

### Final shape

| Tier | Tools | Installed by default |
| --- | --- | --- |
| Core (9) | TLA+ (TLC, Apalache), Alloy 6, Z3, Hypothesis, Schemathesis, CrossHair, Kani (Rust repos only), Dafny, Elle | Yes |
| Specialists (7) | Tamarin (auth/crypto protocols), VeriEQL (SQL rewrites), Cedar analyzer (Cedar policies), Shuttle/Loom (Rust concurrency), Stateright (Rust actors as model), XState graph (XState UIs), Antithesis or hand-built DST (whole-cluster faults) | Only when its trigger appears |
| Dropped | Quint (unless chosen *instead of* TLA+), P, FizzBee, PlusCal as a separate tool, Spin, NuSMV, Event-B, UPPAAL, cvc5, Nagini, Gobra, Lean (unless Dafny is outgrown), Rocq, Isabelle, F\*, Verus, Prusti, Creusot, Coyote, Porcupine, Knossos, ProVerif, SQLSolver, QED, PObserve | No |

The catalogs keep mentioning dropped tools where they are the classic reference. The skill should map each such mention to the core tool in this table.

## Full tool catalog

The skill should carry about 30 tools, each grouped into one of six families. Every tool is listed with the one job it does best. The skill should never pick a tool outside this list without saying why.

### Behavioral model checkers (designs, before or beside code)

| Tool | Best at | Strength | Limit | Run |
| --- | --- | --- | --- | --- |
| [TLA+](https://lamport.azurewebsites.net/tla/tla.html) + TLC / Apalache / TLAPS | Concurrent and distributed protocols; safety + liveness | Industry standard; >100 models inside Amazon ([TLA+ conf 2023](https://conf.tlapl.us/2023/dragoischwiderski/)); proofs via TLAPS | Math syntax; engineers struggle to learn it ([CACM 2025](https://cacm.acm.org/practice/systems-correctness-practices-at-amazon-web-services)) | `java -cp tla2tools.jar tlc2.TLC Spec.tla` |
| PlusCal | Same as TLA+, written as pseudocode | Easier for engineers; translates to TLA+ | Labels set atomicity; easy to get wrong | `pcal.trans` then TLC |
| [Quint](https://github.com/informalsystems/quint) | TLA+ semantics with typed, programmer syntax | Random simulation + Apalache SMT checking; emits ITF traces for model-based testing ([quint-connect](https://docs.rs/quint-connect)) | Younger ecosystem | `npm i -g @informalsystems/quint`; `quint run --mbt`, `quint verify` |
| [P](https://p-org.github.io/P/casestudies) | Message-passing state machines (microservices, protocols) | Used for S3 strong consistency, DynamoDB, EBS, Aurora; PObserve checks prod logs against the model | Event/state-machine style only | `dotnet tool install P`; `p check` |
| [FizzBee](https://fizzbee.io) | Distributed designs in Python-like (Starlark) syntax | Lowest learning curve; sequence diagrams and state graphs out of the box | No proof system; does not spill state to disk ([Vanlightly](https://jack-vanlightly.com/analyses/2024/12/5/verifying-kafka-transactions-diary-entry-4-writing-an-initial-fizzbee-spec)) | Playground or bazel build |
| Spin / Promela, NuSMV / nuXmv | Classic protocol and hardware-style state machines | Mature, fast | Dated tooling | CLI |
| UPPAAL | Timed automata: timeouts, deadlines, SLAs | Real clocks in the model | Niche syntax | GUI + `verifyta` |
| Event-B (Rodin) | Refinement from abstract to concrete with proof obligations | Each refinement step is proved | Heavyweight | Rodin IDE |

### Relational and constraint solvers (structure, config, rules)

| Tool | Best at | Strength | Limit | Run |
| --- | --- | --- | --- | --- |
| [Alloy 6](https://alloytools.org/alloy6.html) | Data models, relationships, permissions, schemas; light behavior | Relational logic + (since v6) mutable state and temporal operators; latest 6.2.0 ([alloytools.org](https://alloytools.org/)) | Bounded scopes; long traces get weak | JAR GUI or CLI |
| [Z3](https://github.com/Z3Prover/z3) / cvc5 (SMT) | Rule tables, policy equivalence, "can X ever happen" queries | Proves or gives a concrete counterexample; Python API | You write the encoding | `pip install z3-solver` |
| [Zelkova](https://www.amazon.science/publications/projective-model-counting-for-ip-addresses-in-access-control-policies)-style policy SMT | IAM / access policy analysis | Encodes policies to SMT; 99% of real queries < 160 ms ([paper](https://discovery-pp.ucl.ac.uk/id/eprint/10081411/1/Semantic-based%20Automated%20Reasoning%20for%20AWS%20Access%20Policies%20using%20SMT.pdf)) | AWS-internal; replicate the idea with Z3 | Build on Z3 |
| Cedar analyzer | Authorization policies written in Cedar | Verified symbolic compiler to SMT ([SymCert](https://cdn.amazon.science/9f/c9/5d18658a41c48628b686493aa327/scipub-approval152134-46496997-symcert-verifying-smtbased-policy-analyses.pdf)) | Cedar only | `cedar` CLI |
| [VeriEQL](https://www.vldb.org/pvldb/vol17/p4437-zhao.pdf) / SQLSolver / QED | SQL query equivalence, rewrite safety | Proves or disproves with concrete counterexample tables | Bounded (VeriEQL) or SQL-subset limits | Research tools |

### Code-level verifiers (prove the real code)

| Tool | Language | Best at | Limit |
| --- | --- | --- | --- |
| Dafny | Own language, compiles to C#/Java/Go/Python/JS | Verified algorithms and core logic; was Cedar's first model | Proofs can turn brittle as code grows ([Cedar poster](https://bhaktishh.github.io/papers/popl-24-src-poster.pdf)) |
| Lean 4 | Own language | Executable reference models + proofs; Cedar's current model ([AWS blog](https://aws.amazon.com/blogs/opensource/lean-into-verified-software-development)) | Steep; strict termination checking |
| Rocq (Coq), Isabelle, F\* | Own languages | Deep proofs, verified compilers and crypto | Expert-only |
| [Kani](https://cdn.amazon.science/05/be/d3a0c9c241e1b6ffbf5b2e6eddb4/scipub-approval152129-47347564-kani-a-model-checker-for-rust.pdf) | Rust | Bounded model checking of panics, overflow, unsafe code; runs in Firecracker CI | Sequential Rust only, no concurrency ([summary](https://www.emergentmind.com/papers/2607.01504)) |
| Verus, Prusti, Creusot | Rust | Deductive proofs on Rust code | Annotation effort |
| CBMC, Frama-C | C | Memory safety, bounded proofs | C only |
| Gobra | Go | Viper-based verification | Research-grade |
| [Nagini](https://github.com/marcoeilers/nagini) | Python | Full Python verification | Annotation effort; research-grade |
| [CrossHair](https://crosshair.readthedocs.io/en/latest/related_work.html) | Python | Finds counterexamples to contracts/type hints with Z3; `diffbehavior` compares two functions | Finds bugs, cannot generally prove |
| Liquid Haskell, Stainless | Haskell, Scala | Refinement types | Language-bound |

### Concurrency testers (real code, controlled schedules)

| Tool | Language | Best at |
| --- | --- | --- |
| [Shuttle](https://github.com/awslabs/shuttle) | Rust | Randomized scheduling (PCT); scales; used on S3 ShardStore ([AWS](https://aws.amazon.com/blogs/storage/how-automated-reasoning-helps-us-innovate-at-s3-scale)) |
| Loom | Rust | Exhaustive interleavings of small tests |
| Coyote | .NET | Systematic testing of async actors |
| [Stateright](https://docs.rs/crate/stateright/latest) | Rust | Model checker embedded in an actor library; same code runs on a real network; linearizability tester |

### Property-based and model-based testing

| Tool | Language | Best at |
| --- | --- | --- |
| [Hypothesis](https://hypothesis.works/articles/rule-based-stateful-testing/) | Python | Properties + `RuleBasedStateMachine` stateful tests with invariants |
| fast-check, jqwik, proptest, QuickCheck | TS, Java, Rust, Haskell | Same idea per language |
| [Schemathesis](https://pypi.org/project/schemathesis/4.15.1/) | Any HTTP API | Generates tests from OpenAPI/GraphQL; stateful API workflows from links |
| [XState graph](https://stately.ai/docs/xstate-graph) | TS | Paths through UI/workflow state machines as test cases |
| quint-connect | Rust, TS | Replays Quint traces against the implementation |

### System-level conformance and fault testing

| Tool | Best at |
| --- | --- |
| [Antithesis](https://antithesis.com/resources/deterministic_simulation_testing/) | Deterministic hypervisor: any stack, reproducible fault injection |
| Hand-built DST (FoundationDB, [TigerBeetle VOPR](https://docs.tigerbeetle.com/about/vopr)) | Simulating a whole cluster in one deterministic process |
| Jepsen + [Elle](https://arxiv.org/pdf/2003.10554) | Black-box histories checked for isolation anomalies (G0, G1a–c, G-single, G2) |
| TLA+ trace validation, [FETCh](https://www.datadoghq.com/blog/engineering/continuous-formal-spec-validation), PObserve | Checking real logs against a spec, in test or production |
| Tamarin, ProVerif | Security protocols against an active attacker |
