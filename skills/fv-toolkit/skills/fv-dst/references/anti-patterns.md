# Anti-patterns in hand-built simulators

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| A sweep shares one `random.Random` across its runs instead of a fresh one per seed | A seed the sweep reports as failing does not fail when replayed on its own | Create `random.Random(seed)` inside each run, never once before a loop. Reproduced in `examples/bad/unseeded-rng/` |
| A fault the sweep declares is never wired into the decision it should drive | The sweep passes on a design that is known to fail, because the fault that would expose it never fires | Assert that each declared fault's rate over a sweep is non-zero, not only that the property holds. Reproduced in `examples/bad/fault-never-injected/` |
| The simulator reads the wall clock (`time.time()`, `datetime.now()`) for a timing or ordering decision | Two runs of the same seed take different paths, so a failure cannot be isolated to one seed | Model time as a tick counter the scheduler advances, never the real clock |
| The scheduler always resolves ties and enabled-task races in the same order (for example, always delivering before crashing) | The simulation only exercises one interleaving per tick, so most of the state space is never reached | Let the scheduler choose among every currently enabled task, as `examples/good/primary-backup/simulate.py`'s `run()` does |

## The hosted alternative

[Antithesis](https://antithesis.com/resources/deterministic_simulation_testing/) runs the whole system, unmodified, inside a deterministic hypervisor and injects faults at the hardware and network level instead of inside hand-written code. Reach for it when the system is too large or too many-layered to put behind a hand-built scheduler; reach for the pattern in this skill when the system is small enough that a simulator you write is cheaper than standing up a hypervisor.
