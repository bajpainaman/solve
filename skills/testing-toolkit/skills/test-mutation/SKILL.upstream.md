---
name: test-mutation
description: "Runs mutation testing on the changed lines of a diff, removes the survivors that carry no signal, and reports the score with the top one to three surviving mutants, each with the test that would kill it. Hands accepted survivors to test-unit. Use for mutation testing, mutmut, cosmic-ray, StrykerJS, PIT, cargo-mutants, gremlins, \"do these tests catch anything\", checking tests an agent wrote, a mutation score, or when the testing skill routes here. Not for writing the killing tests (use test-unit) or for line coverage (use test-quality-review)."
---

# Mutation testing

A mutation tool makes one small wrong change to the code at a time and runs the tests. A change that no test notices is a surviving mutant, and it marks behaviour that the suite does not check. This is the strongest check that tests catch real bugs, and the main defence against tests that restate the code.

This skill writes no tests. It runs the tool, removes the noise, explains the findings, and hands the real gaps to an authoring skill.

## Three rules

1. **Mutate only the changed lines.** Run on the diff during review. A run over the whole codebase belongs in a nightly or weekly job on core modules.
2. **Filter hard.** Skip lines where a mutant teaches nothing: logging, metrics, debug output, generated code and plain boilerplate. Cap the mutants per line and per review.
3. **Show few survivors, and make each one actionable.** Report at most three per review, each with the line, the change, and the test that would kill it. A long list gets ignored, and then the useful findings in it get ignored too.

## Tools

| Language | Tool | How to limit it to the diff |
|---|---|---|
| Python | mutmut, or cosmic-ray for larger codebases | Limit by file, then keep only the results on changed lines |
| JS / TS | StrykerJS | `--mutate "file:lines"` and incremental mode |
| JVM | PIT | Target the classes in the diff |
| Rust | cargo-mutants | `--in-diff git.diff` |
| Go | gremlins, go-mutesting | Targeting is limited, so limit by package |

Read the tool's `--help` before the first run, because flags differ between versions. When the repo has no mutation tool, adding one is a dependency decision that belongs to the user. Offer it once. Without a tool, plant the mutants by hand as the last section describes.

## Workflow

1. **Compute the diff** against the base branch, and list the changed lines of production code.
2. **Estimate the cost.** Multiply the mutant count by the time of the tests that cover those lines. Ask the user before a run of more than about 15 minutes.
3. **Run the tool** on those lines, with only the tests that cover them.
4. **Drop survivors with no signal**: an equivalent mutant, which changes the code and not its behaviour, and a mutant on a line from rule 2.
5. **Rank what remains.** Put first the mutants on a boundary, a condition, a return value or an error path in the code the PR is about.
6. **Report** the score on changed lines, the count of mutants run, killed and filtered, and the top one to three survivors in the format below.
7. **Hand each accepted survivor to `test-unit`**, or to `test-integration` when the line needs a real dependency. Rerun the mutant to confirm that the new test kills it.

## Survivor format

```text
src/pricing.py:41   `if quantity >= 10`  became  `if quantity > 10`   SURVIVED
Meaning: no test checks an order of exactly 10 items.
Killing test: bulk discount applies at 10 items, expecting 900 cents for 10 x 100.
```

## In CI

Run on the PR diff as an advisory comment first. Make it blocking on critical paths only after the team trusts the findings. Run the full set on core modules nightly or weekly to follow the trend of the score. `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` places both runs.

## Planted mutants by hand

When no tool is available, plant up to five mutants by hand on the changed lines. Flip a comparison, move a boundary by one, negate a condition, replace a return value with a constant, and remove a call. Run the tests after each, record whether it was killed, and restore the code before the next. Confirm at the end that the working tree holds no leftover change, and say in the report that the mutants were planted by hand.
