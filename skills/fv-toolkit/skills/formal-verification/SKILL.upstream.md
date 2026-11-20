---
name: formal-verification
description: "Decides which kind of check can settle a correctness question, and then runs it: a model checker for orderings, crashes and retries, a model finder for permissions and data shapes, property tests for functions over all inputs, and the other tools in its registry. Use whenever someone asks whether something can ever happen or always holds, such as a double charge, a lost update, a race between two jobs, a crash between two writes, a leaked permission, or a calculation that is wrong for some input. Use it also when they ask which test, model or proof would give certainty, when a PR or a design doc claims never, always, at most once or exactly once, and before you recommend TLA+, Alloy, Z3, property-based testing or any other formal tool from memory, because this skill holds the selection rules and knows which tools are installed. Not for ordinary unit tests, linting, type errors or general debugging."
---

# Formal verification

A test checks the cases that someone wrote. A formal check covers every case in a stated scope: every order of steps in a model, every structure up to a bound, or every generated input. This skill finds the claims that are worth that cost, picks the cheapest tool that can produce the failure, and reports a pass only after the check has failed on a planted bug.

The person who asks does not need to read TLA+ or Alloy. They judge sentences, traces and verdicts, and the checker judges the rest. `${CLAUDE_PLUGIN_ROOT}/references/trust.md` explains that contract in words you can give to the user.

## What a good check is

- **True to the code.** Each part of the model names the code it transcribes. One indivisible step in the model is one indivisible step in the code.
- **Able to fail.** Each property fails on a planted bug before the report calls it checked.
- **Findings stay findings.** When the code breaks a property, report the counterexample. Never weaken the property or the model until the check passes. Change product code only when the user asks.
- **Honest about scope.** State the bounds, the faults that were switched on, the assumptions, and what the model leaves out.
- **Readable without the tool.** State each property and its harm in one plain sentence. Tell each counterexample as numbered steps in the system's own words.
- **Cheap to rerun.** The check is one command with pinned tools, and it is short enough to repeat on every relevant change.
- **Kept in step with the code.** Each model records the files it covers and the commit it was read at.

## Scripts

The scripts are in `${CLAUDE_PLUGIN_ROOT}/scripts/`. Run each one by its full path, and read its `--help` before the first use. In a harness that does not set `${CLAUDE_PLUGIN_ROOT}`, the plugin root is the directory two levels above this file, and every path in these skills starts there.

| Script | Use |
|---|---|
| `fv-install` | Installs the pinned TLC and Alloy jars. Run it once before the first check. |
| `fv-tlc` | Runs TLC on each config and compares the outcome with the config's `\* expect:` header. |
| `fv-alloy` | Runs every command of an Alloy model and compares each result with its `expect` clause. |
| `fv-mutate` | Plants each bug from a `.mutations` file in a copy and confirms that the check fails. |
| `fv-replay` | Turns a TLC counterexample into a pytest file that replays it against the code. |
| `fv-conform` | Checks a recorded run of the real system against a TLA+ spec. |
| `fv-pin` | Pins the confirmed properties and reports when one of them changes. |
| `fv-drift` | Reports whether the covered code changed since a model's sync commit. |

A script exits 3 and prints `UNAVAILABLE` when a tool is missing. Report that target as "not checked" and give the printed remedy. It is neither a pass nor a failure.

## Workflow

### 1. Triage

Read `${CLAUDE_PLUGIN_ROOT}/references/claims.md` and write the claims table. When no claim earns a formal check, say so in one paragraph and stop.

Ask the user once for sources outside the repository: design docs, incident reports and closed bugs. Treat each statement in them as a lead, and confirm it in the code before you build on it.

Answer four questions about the system before any modelling, because every property rests on the answers:

| Question | What to pin down |
|---|---|
| Who acts? | The actors, their roles, and the local state each one holds |
| How do they coordinate? | Messages or shared state. For messages: lossy or reliable, ordered or not |
| What fails? | The faults from `${CLAUDE_PLUGIN_ROOT}/references/faults.md` that apply |
| What depends on time? | Timeouts, leases, clocks, retries with backoff |

For each target, list the commits that fixed a bug in its code. Step 6 replays each one as a mutation.

### 2. Pick the tool by the question

| The question is | Family | Default tool |
|---|---|---|
| Can a bad ordering happen? Concurrency, retries, crashes, message loss | A behavioural model checker | TLA+ with TLC |
| Can the data or the configuration reach an invalid shape? Relations, permissions, schemas, rules | A relational or constraint solver | Alloy 6 |
| Is this code correct for every input? Functions, calculations, state machines in one process | Checks on the real code | Hypothesis |
| Does the running system obey the model? | Conformance | The link techniques in `${CLAUDE_PLUGIN_ROOT}/references/linking.md` |

`${CLAUDE_PLUGIN_ROOT}/references/skills.md` lists every tool that has a skill, the question each one answers and the command that installs it. Read it, pick the row that matches the claim, and load that skill. A tool is installed on demand, so a missing tool is one `fv-install <name>` away.

Load the tool's skill before you recommend the tool, also when the user asks only which check to use. The skill states what the tool can express, what a pass means and what the check costs. A recommendation without it comes from memory.

Load it with the Skill tool, by its name, such as `fv-tlaplus`. Do not read its `SKILL.md` with a file tool or with `cat`, because the Skill tool also resolves the paths that the skill refers to.

Then find the architecture pattern in `${CLAUDE_PLUGIN_ROOT}/references/catalog/INDEX.md` and read only the catalog file that holds it. The row gives the failure that the model must be able to produce, the abstraction level, the properties and the link to code. When no pattern fits, say so and use the four questions alone.

Prefer the cheapest rung that can produce the failure:

1. Property tests on the real code.
2. Symbolic or bounded checks on the real code.
3. A design model with a model checker.
4. Conformance between the model and the code.
5. Proof, only where a bug is unacceptable.

For a tool that `skills.md` does not list, read `${CLAUDE_PLUGIN_ROOT}/references/tools.md`, say that no skill covers the tool yet, and follow this same workflow from the tool's own documentation. When the user names a tool, use it and report what it leaves unchecked.

Factory, Builder, Adapter, Decorator, Facade, Proxy, Singleton and DI containers have no invariant of their own. Say so and verify only the contract of what they wrap.

### 3. Freeze the properties

Write each property as one sentence in the system's vocabulary, with the source sentence quoted beside it. Use the families in `${CLAUDE_PLUGIN_ROOT}/references/properties.md` to find the ones the claims imply. Keep a ledger with one row per property:

| Property | Source | Kind | Encoded as |
|---|---|---|---|
| A customer is never refunded more than they paid | "refunds are capped at the payment" (ticket) | safety | `NeverOverRefund` invariant |
| Every job eventually finishes | unwritten; the design needs it | liveness | `EventuallyDone`, under weak fairness on each job |
| Refunds by webhook | PR description | — | not modelled |

Show the ledger to the user and get their confirmation before you write a model. A wrong property is the most expensive mistake in this workflow. After confirmation, a property changes only with the user's agreement or with evidence that the promise itself changed.

### 4. Write the model from the code

Load the tool's skill and start from its example. Follow the first part of `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md` while you write.

- Model only the state that a property mentions, plus the fault switches.
- Write one action per atomic step in the code, such as one database write or one message send. Never write one action per function.
- Write each design choice as a constant, with one config per variant. Name a config for its mechanism, such as `CheckThenRefund`, and never for a verdict, such as `Buggy`.
- Put the sync record in the header of every model:

  ```text
  Source read at: <commit>
  Covers: <path>, <path>
  ```

- Run the checker after every edit. Do not write the whole model before the first run.
- Keep each model under about 300 lines. Split by component when it grows.

### 5. Check, with a declared outcome for every run

Start with small bounds, such as two or three processes and one or two crashes, and then widen. Every run declares the outcome it must produce, and the wrapper script compares.

- A config or command for the design you believe in must hold.
- A config for a design you rejected must fail on the property it threatens.
- At least one witness per model must show that the interesting state is reachable: the commit, the crash recovery, the compensation. A property that holds because the dangerous state is unreachable proves nothing.
- Check liveness wherever the pattern has a progress property, under a fairness assumption that the code provides.

When the config for the chosen design fails, you have the most valuable result this workflow produces. Investigate it before you touch the model.

When the model encodes every row of the ledger, pin the properties and the declared outcomes:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/fv-pin write <model dir> <file>:<Property> <config or test file> ...
```

From then on, run `fv-pin check <model dir>` before every report. Run `fv-pin write` again only after the user agreed to change a property.

### 6. Make the check bite

Read `${CLAUDE_PLUGIN_ROOT}/references/bite.md`. Write a `.mutations` file beside the model and run `fv-mutate` on it. Every mutation must print `DETECTED`, and no property may print `UNCOVERED`.

Then offer the independent review that `${CLAUDE_PLUGIN_ROOT}/references/review.md` describes. A second agent reads the code and the properties without your reasoning, and returns the bugs that the properties would let pass.

### 7. Read each counterexample back into the code

Follow the second part of `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md`. Map every step of the trace to a code event and a line. Give each counterexample one disposition: reproduced, reachable, bounded away, or model gap. A step that cannot happen in the code means that the model is wrong, so fix the model and rerun.

### 8. Link the model to the code

Every model ships with at least one link from `${CLAUDE_PLUGIN_ROOT}/references/linking.md`. The usual first link is a deterministic regression test that forces the interleaving or the input of the counterexample. When no link is possible, name the gap in the report.

### 9. Report and hand off

Write the report as `${CLAUDE_PLUGIN_ROOT}/references/report.md` describes. Keep the model, its configs, its mutations file and a README with the property ledger beside the code they describe. Commit them only when the user asked for commits. When the repository will keep the check, offer to write the project-local recheck skill that `report.md` describes, so that an agent who changes the covered code finds the check. Tell the user that `/fv-toolkit:fv-maintain` brings the models back in line after the code changes.

## Guardrails

- Never write "verified" or "proved" for a bounded check. Say what was checked, at which bounds, with which faults, and through which link to the code.
- Never weaken a property to make a checker pass. Ask the user.
- Never report `UNAVAILABLE` as a pass.
- Never count a run without a declared outcome.
- Treat a failed trace validation as "mapping error or bug" until you have checked the log mapping.
- When you pick a tool outside `${CLAUDE_PLUGIN_ROOT}/references/tools.md`, say why.

## Reference files

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/claims.md` | Step 1, always |
| `${CLAUDE_PLUGIN_ROOT}/references/catalog/INDEX.md` | Step 2, to find the pattern |
| `${CLAUDE_PLUGIN_ROOT}/references/skills.md` | Step 2, to find the skill and the install command of a tool |
| `${CLAUDE_PLUGIN_ROOT}/references/tools.md` | A tool without a skill, or a tool the catalog names that is not core |
| `${CLAUDE_PLUGIN_ROOT}/references/properties.md` | Step 3 |
| `${CLAUDE_PLUGIN_ROOT}/references/faults.md` | Steps 1 and 4 |
| `${CLAUDE_PLUGIN_ROOT}/references/fidelity.md` | Steps 4 and 7 |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | Step 6 |
| `${CLAUDE_PLUGIN_ROOT}/references/review.md` | Step 6, when the user wants an independent review |
| `${CLAUDE_PLUGIN_ROOT}/references/linking.md` | Step 8 |
| `${CLAUDE_PLUGIN_ROOT}/references/report.md` | Step 9 |
| `${CLAUDE_PLUGIN_ROOT}/references/trust.md` | The user asks how to trust a model they cannot read |
| `${CLAUDE_PLUGIN_ROOT}/references/setup.md` | A tool is missing |
