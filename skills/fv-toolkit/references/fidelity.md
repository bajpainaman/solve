# Fidelity: the model must describe the code

A correct analysis of a wrong model gives false confidence. The first part applies while you write the model. The second part applies when the checker returns a counterexample.

## Part 1. While you write the model

1. **Each action names the function it transcribes.** Put the function and its file in a comment on the action. An action with no source is a design proposal. Label it so in the model and in the report, or delete it.
2. **Each action writes only what its writer can write.** Before the first run, compare the values that each action assigns with the values that the real writer can produce. A sync job does not write a status that no upstream system reports.
3. **Atomicity follows the code.** A check and a write that are two statements in the code are two actions in the model. A region under one lock, or one SQL statement, is one action. A fix that holds only because the model made two steps atomic is unchecked.
4. **Data matches the code's version.** Rule tables, reference rows and configuration come from the commit under review.
5. **Parties you do not own need evidence.** For a third-party API, a workflow engine, a database's locking or a browser, cite their documentation or a payload captured from the real system. Without evidence, model the behaviour as a choice and check every branch. A finding that needs one branch is a hypothesis that names the branch.
6. **"This config is the current system" needs a code trace.** Show the read, every guard between, and the write. "I could not find a guard" is weaker than "there is no guard", and the report says which one you have.
7. **Retries follow the effective policy.** Model the retry policy that the call really has, including the framework's default when the code passes none, and include a retry that fails the same way every time.
8. **Names carry no verdicts.** Name configs and constants for their mechanism, such as `SyncViaFullUpdate` or `CheckThenCredit`. Names such as `Safe`, `Buggy` or `Broken` state a conclusion before the checker has run.

## Part 2. When the checker returns a counterexample

A counterexample is either a bug in the code or a gap in the model. The most common false alarm is a trace whose preconditions the real system prevents, because the model left out a guard.

### Step 1. Write down the preconditions

List the conditions that the violating state needs. Be specific. "Worker A held an expired lease while it received the write acknowledgement from B" is a precondition. "Worker A misbehaved" is not one.

### Step 2. For each precondition, ask what stops it in the real system

Search the code for a mechanism of one of these kinds:

| Mechanism | What it looks like in code |
|---|---|
| Reactive suppression | Receiving X resets or clears state Y, as when a heartbeat resets an election timer |
| Conditional acceptance | A message is acted on only when a field passes a check: a term, a version, a sequence number, a signature |
| Mutual exclusion or a lease | State X locks out action Y for a time or until a condition holds |
| A reentrancy guard | An action runs only while a "not already running" flag holds |
| Authentication or a quorum proof | A message is acted on only when it is signed or attested by a quorum |
| A budget | An action runs only inside a counter or a rate limit that the system tracks |

A guard at the top of a function is evidence that its authors believed the guarded condition can occur. The model should let the condition occur and should model the guard.

### Step 3. Compare with the model

- The model has the guard with the same condition. The guard is faithful, so move to the next precondition.
- The model has the guard with a weaker condition, or does not have it. The model reaches states that the code cannot reach. This is a **model gap**.
- The code has no guard for this precondition. The precondition can occur, and the trace stays a candidate bug.

### Step 4. Fix the model and rerun

For a model gap, add the guard to the model and rerun the checker. Record the precondition, the guard with its `file:line`, and the change to the model. If the violation remains, start again from step 1, because a second mechanism can be missing.

### Step 5. Give the counterexample a disposition

| Disposition | Meaning |
|---|---|
| **reproduced** | A deterministic test, a race detector or a stress loop fails on the real code in the same way |
| **reachable** | Every step maps to code, the shipped settings allow each step, and no test reproduces it yet |
| **bounded away** | The trace needs a constant or a caller that the shipped code does not use. Keep the config, and say that the result holds only while that setting stays |
| **model gap** | A step cannot happen in the code. The model was fixed and rerun |

Reproduce a reachable trace before you propose a fix. Hooks, barriers or a small pool size can force the interleaving. When a test built from the trace passes on the real code, suspect the model first.

Never drop a candidate without a disposition, and never count a candidate that was not reproduced as a confirmed bug.
