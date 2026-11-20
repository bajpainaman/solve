# Strategy models

No single shape fits every codebase. Pick a shape for each component from where that component's logic and bugs are.

| Model | Shape | Fits | Fails when |
|---|---|---|---|
| **Test pyramid** | Many unit tests, fewer integration tests, very few E2E tests | Code with dense logic: calculators, rules engines, parsers, domain models | The logic is mostly wiring. Unit tests with heavy mocking then catch nothing. |
| **Testing trophy** | Static checks at the base, and integration tests as the widest band | Frontend and full-stack apps, where the test acts as the user does | The logic is rich. Reproducing every rule case through integration tests is slow and still misses edges. |
| **Testing honeycomb** | Few tests of implementation detail, a thick middle of tests on one service through its real API and real DB, few tests across services | Microservices | A service holds complex internal logic. Add a pyramid inside it. |
| **Testing diamond** | A thin unit layer, wide integration, thin E2E | Data-heavy systems and pipelines | Transformations have tricky logic. Add property tests per transform. |
| **Testing in production** | Canary, shadow traffic, synthetic probes, SLO gates | Distributed systems where staging can't reproduce production | The system has no observability or rollback. Without them this ships bugs to users. |

## How to choose, per component

1. Ask where the bug is most likely if this component breaks.
   - In its own logic: pyramid.
   - At the boundary with a DB, a queue or another service: honeycomb or trophy.
   - In the user flow: trophy plus a few E2E tests.
2. Turn on static analysis and types before you write tests. They are the bottom layer of every model, and they cost nothing to run.
3. Write committed E2E tests only for the few journeys whose failure would be an incident, such as signup, checkout and the core workflow. Move every other check down a layer. Every change with a user path still gets one run of the real system before it is done, because tests that the agent wrote from its own reading of the code can pass while the feature is broken.
4. Add a harness where the input space is large: property-based tests for logic, fuzzing for parsers, load tests for hot paths. Add a differential test, with the old code as the oracle, wherever a change must keep behaviour.
5. Add runtime practice once the service has real traffic. The test suite can't see production data shapes or production load.

Microservices change the picture further. Each service gets its own small pyramid, and the emphasis moves to contract tests and to integration tests of one service at a time.

## Which skill writes each layer

| Layer | Skill |
|---|---|
| Unit | `test-unit` |
| One service with a real DB, cache, queue or filesystem | `test-integration` |
| The agreement between two services | `test-contract` |
| A user journey in a browser | `test-e2e` |
| Legacy behaviour before a refactor | `test-characterization` |
| A rule over a large input space | `test-property` |
| A parser of untrusted bytes | `test-fuzz` |
| A hot path under load | `test-load` |
| A dbt model or a pipeline | `test-data` |
| A prompt, a RAG chain or an agent | `test-llm-evals` |
