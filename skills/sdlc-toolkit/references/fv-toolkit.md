# Running the formal-verification toolkit

The [fv-toolkit](https://github.com/aasimsani/formal-verification-toolkit) settles a claim that says never, always, at most once or exactly once. A test checks the cases someone wrote. A model checker tries every ordering of the modelled steps, and a model finder tries every small structure. Its `formal-verification` skill triages the claims, picks one tool by the question, and runs the check. Invoke `fv-toolkit:formal-verification` with the Skill tool, and let it load the tool skills. `sdlc:setup` installs it with the rest of the stack.

Most features have no such claim, and the skill's triage says so in one paragraph. That answer is a result. Record it as the skip reason and go on.

The skill writes its model from the code. This loop has a design before it has code, so it uses the skill twice. RFC models the design. Test dispatches a subagent that models the code, without the first model in view.

## RFC checks the design

Invoke it after the RFC is written and checked against the spec.

| Input | What to pass |
|---|---|
| The claims | Each sentence in `spec.md` and the RFC that says never, always, only when, at most once or exactly once |
| The system | The RFC's chosen design: who acts, how they coordinate, what fails and what depends on time |

1. **The approver confirms the properties.** The skill writes each property as one sentence and asks its user to confirm the list. Here that person is the stage's approver. A property changes later only if they agree.
2. **The model describes the design.** No code exists yet, so each step in the model names the RFC sentence it transcribes. Leave out the skill's sync record and its replay in the code, because both need code.
3. **A counterexample changes the design.** Fix the RFC before the gate, and keep the rejected design as a config that must fail. Never weaken a property until the check passes.
4. **The files stay with the RFC.** Put the model, its configs, its mutations file and its pins in `docs/sdlc/<slug>/fv/design/`. The property ledger goes in that folder's `README.md`, with the bounds, the faults and what the model leaves out.

## Plan turns the properties into tests

When the feature has a property ledger, pass it to the testing skill along with the spec. Each confirmed property gets rows in the plan's Tests section:

- **A Build test** replays each counterexample the design model produced, so the code can't repeat the rejected design.
- **A final test** checks the property on the running code, such as a stateful property test, a simulation with faults or a conformance run.

## Test models the code afresh

Do both of these only when the feature has a property ledger. Without one, do neither, unless the diff adds concurrency, retries, shared state, permissions or a rule table that the RFC never mentioned. In that case ask the subagent for its triage alone.

1. **Check the pins.** Run the toolkit's `fv-pin check` on `fv/design/`. A property that changed since the approver confirmed it is a finding.
2. **Dispatch the `fv-verifier` subagent.** Give it the path to `spec.md`, the confirmed properties as sentences, the base branch and the path for its report, `docs/sdlc/<slug>/fv/code-report.md`. Copy the sentences out of the ledger. Don't give it the RFC, the plan or anything in `fv/design/`, because a second model is worth its cost only when it doesn't share the first one's assumptions. Then wait until its report exists. Don't end your turn while the subagent is running, because a session that isn't interactive ends there, and the subagent stops with it.
3. **Compare the two models, property by property.** A property that holds on the design and fails on the code is a finding about the code. A claim the subagent found that the ledger lacks goes to the approver.
4. **Send a failure back.** A counterexample the code can reach becomes a Build phase in `plan.md`, with its replay as the first failing test. When the design itself is wrong, the RFC goes back to draft.
5. **Keep the code's model.** Commit the model the subagent wrote beside the code. It carries the sync record, so it's the one that gets kept in step from here on. The design model stays with the RFC.
6. **Say what a pass covers.** `verify.md` gives each property its bounds and faults. A bounded pass is never "verified" or "proved".

## Maintain keeps the models in step

In `drift` mode, invoke `fv-toolkit:fv-maintain` when the repo holds a model with a sync record. It gives each model one outcome: in sync, updated, bug or blocked. A bug becomes a new intent. A model update goes in a change of its own, apart from any product fix.

## When the toolkit isn't installed

The session lists `fv-toolkit:formal-verification` among its skills when the toolkit is installed. Without it, read the spec and the RFC for a claim that says never, always, at most once or exactly once. Tell the approver about each one, and record the RFC stage's `formal-verification` tool as skipped, with that reason.
