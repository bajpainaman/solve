---
name: test-llm-evals
description: "Writes eval suites for prompts, RAG chains, agents and model upgrades. A versioned golden dataset in JSONL, deterministic checks on every case, a judge score with a threshold where a check can't be exact, and separate capability and regression sets. Also writes red-team and prompt-injection sets for user-facing input. Use for LLM evals, prompt regression tests, promptfoo, DeepEval, Inspect, an LLM-as-judge rubric, \"did this prompt change make it worse\", a model upgrade, or when the testing skill routes here. Not for ordinary code that happens to call an LLM behind a mock (use test-unit)."
---

# LLM evals

An eval suite is a dataset, a set of scorers and a threshold. It answers one question on every prompt or model change: is the output still at least as good as before? The answer is only as trustworthy as the dataset is stable, so the dataset has a version and every run records it.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` where it applies. This file adds the rules that are specific to evals.

| Python | TypeScript / JS |
|---|---|
| promptfoo, DeepEval, Inspect | promptfoo |

## Five rules

1. **Version the golden dataset.** Keep cases in JSONL files under version control, with the version in the file name or a field, and record that version in every run's output. Never edit the dataset in the same change as the prompt.
2. **Put a deterministic check on every case.** Use exact match, a required substring, a JSON schema, a regex or a tool-call check wherever the expected output allows one. These checks cost nothing and never drift.
3. **Give every judge a rubric and a threshold.** Use an LLM judge only for qualities that no deterministic check can state, such as tone or faithfulness to a source. Write the rubric as observable criteria, and set the score that passes.
4. **Separate regression evals from capability evals.** A regression set holds cases that already pass, and it must stay near 100%. A capability set holds hard cases with a low pass rate, and it tracks progress. Only the regression set gates a merge.
5. **Make runs repeatable.** Set temperature to 0 where the provider allows it, pin the model version, and run each case more than once when the output still varies.

## Reject the suite if

- Every scorer is an LLM judge.
- The dataset has no version, or it changed in the same commit as the prompt.
- A score rose in a run where the dataset also changed.

## Workflow

1. **Write the spec of the feature**: what a correct output is, as rules a person could check.
2. **Apply step 0** of assured generation to each case. The credible bug is a prompt or model change that breaks the rule the case stands for.
3. **Build the dataset.** Take cases from real inputs, past failures and the edges of each rule. Write each expected output from the spec, never from the current model's answer. Split the cases into the regression file and the capability file.
4. **Write the scorers**: deterministic checks first, then a judge with a rubric and a threshold where one is needed.
5. **Run the suite** and record the baseline pass rate with the dataset version. When no API key is available, write the suite and list the run under "Not run".
6. **Show that the suite can fail.** Break the prompt on purpose, such as removing the output-format instruction, and confirm that the pass rate falls. Restore the prompt.
7. **For user-facing input, add a red-team file**: injection attempts, requests to reveal the system prompt, and inputs outside the feature's scope, each with a deterministic check on what must not appear.
8. **Report** the dataset version and size, the scorers, the baseline, the gate, and the CI placement: the small regression set on a prompt change, the full set and the red-team set nightly.

When the regression set has sat at 100% for weeks, promote cases from the capability set that now pass.

## The report

End your reply with this table, even when you wrote one case. The user reads it to decide whether each row earns its place.

| Case or group | Rule it protects | Prompt or model change that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```yaml
# Bad. One judge with no threshold scores everything, the cases sit inline
# with no version, and the temperature is the provider's default.
prompts: [file://prompts/triage.txt]
providers: [anthropic:messages:claude-sonnet-5-5]
tests:
  - vars: {ticket: "I was charged twice"}
    assert:
      - type: llm-rubric
        value: The answer is good
```

```yaml
# Good. The dataset is a versioned file, each case carries its own exact
# check, and the judge has a rubric and a threshold.
description: support-triage regression, dataset v3
prompts: [file://prompts/triage.txt]
providers:
  - id: anthropic:messages:claude-sonnet-5-5
    config: {temperature: 0}
tests: file://datasets/regression.v3.jsonl
defaultTest:
  assert:
    - type: is-json
    - type: llm-rubric
      value: The reply names the next step for the customer and makes no promise of a refund.
      threshold: 0.8
```

```json
{"vars": {"ticket": "I was charged twice for order 1182"}, "assert": [{"type": "javascript", "value": "JSON.parse(output).category === 'billing'"}], "description": "duplicate charge routes to billing"}
```

Check the config keys against the installed version of the tool before you rely on them.

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Before the first case |
| `${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` | Before you show the suite |
