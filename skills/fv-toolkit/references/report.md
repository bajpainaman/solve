# Report and hand-off

Write the report for a reader who knows the code and has used none of these tools.

## Order of the report

1. **Findings first, in the code's terms.** For each counterexample, give:
   - what goes wrong for a user or a caller, and for whom;
   - the steps in order, each with its `file:line`;
   - the disposition from `fidelity.md`: reproduced, reachable, bounded away or model gap;
   - the command that reproduces it;
   - the fix options with the cost of each. Do not pick the fix for the reader;
   - whether the defect existed before the change or came with it.
2. **One row per claim.**

   | Claim | Check | Bounds and faults | Verdict | Mutations | Link to code |
   |---|---|---|---|---|---|
   | A customer is never refunded more than they paid | TLA+ `NeverOverRefund` | 2 jobs, no crash | fails on check-then-refund, holds on the atomic update | 2 of 2 detected | regression test `test_two_refunds_race` |

3. **What each kind of evidence means**, the first time it appears. Use the table below.
4. **What a pass leaves open.** List the sizes that were checked, the faults that were switched off, the code constraints the model omits, the properties that could not be expressed, and every claim that stayed unchecked.
5. **The commands that rerun every check**, with the verdict lines they print.

## Evidence vocabulary

| Evidence | Say this |
|---|---|
| TLC reports no error | TLC tried every ordering of the modelled steps at the listed sizes and found none that breaks the property. The state count is the size of that search. It is not a count of real runs. |
| An Alloy `check` is UNSAT | The analyzer found no counterexample among all structures up to the stated scope. Larger structures are not covered. |
| An Alloy `run` is SAT | At least one structure satisfies the model, so the checks did not pass on an empty model. |
| A Hypothesis property passes | The stated number of generated inputs passed. This is a search. It is exhaustive only when the strategy enumerates a finite domain. |
| Mutations detected | Deliberate bugs were planted in copies of the model or the code, and the check caught each one. |
| A past fix detected | The check fails on the behaviour from before a recorded bug fix. |
| `UNAVAILABLE` | The tool could not run, so this target was not checked. |
| reproduced | A deterministic test or a race detector fails on the real code in the same way. |
| reachable | Every step maps to code and the shipped settings allow it. No test reproduces it yet. |
| bounded away | The counterexample needs a setting or a caller that the shipped code does not use. |

Give each tool term its meaning beside it the first time. An invariant is true in every reachable state. A liveness property says that something eventually happens. Fairness assumes that a step that stays possible is eventually taken. A scope is the largest structure the analyzer tries.

Never write "verified", "proved", "guaranteed" or "correct" for a bounded check. A pass covers the model and the bound. It does not cover the whole system.

## The recheck record

The next agent reads the record cold, in the middle of a change. Leave these beside the code that the model describes:

- the model, its configs and its `.mutations` file;
- a `README.md` that holds the property ledger, the bounds, the faults, the assumptions, what the model leaves out, and the one command that reruns everything;
- the sync record in the header of every model:

  ```text
  Source read at: <commit>
  Covers: <path>, <path>
  ```

Move the sync commit forward only after you confirm that the model describes the code at the new commit. `fv-drift` reads this record.

`properties.pins` sits in the same directory. It holds the SHA-256 of each property and each declared outcome that the user confirmed, and `fv-pin check` reports any that changed.

For each confirmed bug, keep one file under `findings/` with the property, the date, the trace as numbered steps in the system's words, and the change that fixed it. Add to these files and never regenerate them, so that a later weakening of a property shows up as a changed verdict in a diff.

## A project-local recheck skill

When the repository will keep the check, offer to write a small skill into it at `.claude/skills/verify-<area>/SKILL.md`. An agent that changes the covered code then finds the check without this plugin in its context. The skill needs frontmatter, because a skill without it never registers.

```markdown
---
name: verify-<area>
description: "Rechecks that <the property in one sentence>. Use before a change to <the covered files or functions> is reported as done."
---

# Verify <area>

The property is that <one sentence>. When it breaks, <the harm in one sentence>.

- Covers: <paths and functions>
- Source read at: <commit>
- Bounds and assumptions: <sizes, faults switched on, fairness>

## Run

<The one command, with pinned tools.> A pass prints <the verdict lines>.

## When it fails

Walk the counterexample through the code, as <the model's README> describes. A step that cannot happen in the code means that the model is stale. Update the model from the code, and never weaken the property.

## When the covered code changes on purpose

Update the model first and rerun. Then move `Source read at:` to the new commit.
```

Use the repository's real commands, paths and names, and leave no placeholder. Before you hand off, follow the new skill once on a scratch change that breaks the property in the real code. It must catch the break. Then drop the scratch change and confirm that the check is back where it started.
