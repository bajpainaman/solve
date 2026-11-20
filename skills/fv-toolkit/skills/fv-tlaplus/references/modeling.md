# Modelling rules for TLA+

## Size and shape

- Write about 150 concrete lines whose trace reads as a story in the system's domain. A generic, heavily parameterised spec is harder to audit.
- Take every name from the repository. Name configs and constants for a mechanism and never for a verdict.
- Write a `TypeOK` invariant first. It catches a model that drifts out of its own types.
- Group the variables that one actor owns and name the group, so that an action lists the groups it leaves alone.

## State

- Keep only the state that a property mentions.
- Abstract a pure function to an opaque outcome, such as `"taxed"` or `"exempt"`. Model time and structure, and leave the arithmetic to a property test.
- Count an effect where it leaves the system. Add a ghost variable for what an outsider sees, such as requests sent or rows written, and update it in its own step.
- Use a ghost variable for an audit claim. An append-only record of first-written values checks "never overwrite". A flag captured at decision time checks "no change while the flag was off".

## Atomicity

- Split wherever another actor can run. A check and a write that are separate statements are separate actions, even when the function looks short.
- Model each database lock as a wait in the real statement order, and hold it until the commit. A model with one side locking shows no deadlock.
- Never collapse a transaction of several statements into one step when another actor locks the same rows.
- Keep the real gaps in a fix. Rerun the fixed design with retries capped at one. A fix that holds only because the model made two steps atomic, or because a retry hides the failure, is unchecked.

## Actors

- A repeating actor loops for ever. A worker, a poller or a scheduled job that runs once makes "eventually" true by construction. Keep the loop small with a counter or with time modulo the window.
- Model the retry policy that each call really has, including the framework's default and a retry that fails the same way every time.
- Let a user or an external caller act at any point where the real one can: before the first call, after the last item, after an error.

## Constants

- Use tiny constants: two or three actors, two values, one or two faults. Past about 100,000 states, abstract more before you add memory.
- Keep the ratios that matter at the smallest numbers that overflow: producers against capacity, retries against timeouts, writers against locks.
- Write each design choice as a constant, with one config per variant. TLC stops at the first violation, so a config for a rejected design checks only the invariant that design threatens.

## Faults

Each fault from `${CLAUDE_PLUGIN_ROOT}/references/faults.md` becomes a switch, so one model runs with the fault on and off.

| Fault | Encoding |
|---|---|
| Crash and restart | An action that resets the volatile variables and keeps the durable ones, bounded by a `MaxCrashes` constant. Zero switches it off |
| Crash between two writes | Two actions for the two writes, plus the crash action above |
| Message loss, duplication, reordering | The network is a set or a bag of messages. A `Drop` action removes one, and delivery does not remove a message that can be duplicated |
| Partition | A constant or a variable names the pairs that cannot exchange messages, and each delivery action checks it |
| Timeout or pause | The lease expiry is its own action. The paused actor keeps its stale local variables and acts on them later |
| Clock skew | One clock variable per node, with a bound on the difference |
| Concurrent writers | Two actors that run the same actions |
| Partial failure of a batch | A nondeterministic choice of the subset that succeeds |

Give a fault no fairness. Fairness on a crash forces the crash to happen.

## Time

Time moves only when nothing else can, unless the real system can stall between steps. A clock that ticks freely produces false traces and breaks "eventually" on the time bound alone.

## Liveness

- State the fairness of each process next to the code that provides it. `WF_vars(A)` says that A happens when it stays possible. `SF_vars(A)` says that A happens when it is possible again and again. Use strong fairness only when the code guarantees a turn. Polling does not.
- A bound such as `MaxCrashes` or `MaxAttempts` needs a liveness property that fails when the bound alone stopped the run.
- When a fix removes a give-up path, a cap or a timeout, recheck for starvation, where one actor loses every round, under weak fairness only.
- A fix can trade safety for liveness. Check both on every variant.

## End states and deadlock

Deadlock checking is on by default, and it reports a correct end state as a deadlock. Give each correct end state a `Done` action that is true only there and leaves every variable unchanged. A stall anywhere else then still shows up.

## PlusCal or plain actions

Use PlusCal for an algorithm with numbered steps and worker processes. Its labels set the atomicity, so place a label wherever another process can run. Use plain actions for independent events that can happen in any order. Commit the translation that `pcal.trans` writes.
