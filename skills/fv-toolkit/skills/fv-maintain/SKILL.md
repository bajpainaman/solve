---
name: fv-maintain
description: "Brings formal models back in line with the code after the code changed: finds the commits that touched covered code, updates each model from the code, reruns the checks, and says whether each failure is drift in the model or a bug in the code. Use for \"is the model still true to the code\", after merges and refactors that touched modelled code, or before you rely on an old pass."
---

# Maintain formal models

A formal check establishes a property of what it describes. When the code changes and the model does not, the check keeps passing on code that no longer exists. That pass looks like evidence and is not. This skill handles the changes that reached the code without a recheck: merges, edits made without the model in view, and drift across many commits.

## Outcomes

Give each check one outcome, and name it in the report:

- **in sync**: no change since the sync commit alters what the model describes, and the check passes.
- **updated**: the code changed, the model now describes the new code, and the check passes.
- **bug**: the model describes the current code, and the code breaks the property. This is a finding about the code.
- **blocked**: the model could not be brought back in line, or the check could not run. Say exactly why.

A check can be both updated and bug. The update makes the model describe the code again, and the property then fails on it.

## Edit scope

Edit only the verification: models, configs, mutations files, property tests and their READMEs. Never edit product code during this pass unless the user asks. When a property fails on the current code, report the failure. Never weaken the property or the model to make it pass.

## The pass

1. **Find the models.** Run `${CLAUDE_PLUGIN_ROOT}/scripts/fv-drift <directory>` on the repository. It lists every file that carries a `Source read at:` record. For each model, collect the properties, the covered code, the bounds, the assumptions and the command that reruns it. A model that prints `NO RECORD` has no sync commit. Use the last commit that changed the model file, and say that you did. Then run `${CLAUDE_PLUGIN_ROOT}/scripts/fv-pin check <model dir>` for each model. A `CHANGED` line means that a property or a declared outcome is different from the one the user confirmed, so find the commit that changed it and the evidence for the change before you go on.

2. **Run every check as it is.** Run each check and its mutations once before you change anything, and record the results. A pass here means only that the old description still holds. A failure here can be drift or a bug. Do not decide which until step 5.

3. **Read every change to the covered code.** For each model that prints `CHANGED`, read each listed commit in full. Look for code that moved: a covered function that was renamed, split or moved to another file is still covered. Look for new code that writes the state a property guards. Classify each change:
   - **No effect.** The change alters nothing that the model describes. Decide this against the model. A commit message is not evidence.
   - **The model no longer describes the code.** A step that was indivisible is now two steps, a branch was added or removed, a guard moved, a new path reaches the guarded state, or a value has a new range. The model must change.
   - **The promise changed on purpose.** A doc comment, a test, a changelog entry or the commit message says so. The property must change, and you cite that evidence.
   - **The promise may be broken.** The code changed and nothing says that the promise changed. Treat a failure that follows as a candidate bug.

4. **Update from the code.** Write the update from the code before you rerun, and do not shape it by what makes the check pass. Each changed action again names the function it transcribes. One indivisible step in the code stays one step in the model. Change a property only for a promise that changed on purpose, and record the old wording, the new wording and the evidence. Keep the bounds unless the change makes them wrong.

5. **Rerun and judge each result.**
   - **A pass** can come from a model that lost the ability to fail. Add a mutation for each step, branch or guard that the update added, and run `${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate`. Every mutation must print `DETECTED`.
   - **A failure** needs a replay. Walk the counterexample through the real code step by step, as the second part of `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md` describes. If a step cannot happen in the code, the model is wrong, so fix it and say what was wrong. If every step can happen, the code has a bug. Name the commit that introduced it, tell the counterexample in the code's own words, and state the harm in one sentence.

6. **Update the record.** Set `Source read at:` to the commit you checked, and update `Covers:`, the README and the commands. Do not move the sync commit of a blocked check. When the covered code is gone, propose retiring the model, and delete its files only with the user's agreement.

## Report

For each check, give:

- the outcome and the commits you read;
- what changed in the model and why: the code changed shape, or the promise changed on purpose, with the evidence;
- the rerun result and the mutations that show the updated check can still fail;
- each bug as numbered steps in the code's words, with the harm and the commit that introduced it;
- what the model still does not cover, including new code that it should cover.

Say plainly which failures were drift in the model and which were bugs in the code. For a check that passed before the update and fails after it, say that the old pass was on a stale description.

Put the model updates in a change of their own, apart from any product fix.
