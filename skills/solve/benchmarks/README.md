# Synthetic verification benchmark

Fourteen cases form seven changed-premise pairs: reader visibility, rollback,
current pricing, stakeholder conflict, feedback, forecast labeling, and omitted
material claims. All documents and outcomes are synthetic. No external knowledge
or paid provider is needed to inspect the corpus.

Each case includes relevance judgments (qrels, grades 0/1/2), expected gate
decisions, contradicted claims, coverage gaps, an abstention target, and an action
label. A changed premise should change the action for the reason in the evidence.
Unknown evidence is not the same as a contradicted claim.

These cases assess decisions from supplied observations. Predicting FIRED in a
case is not a real solve gate receipt and cannot finalize a real run.

## Export without labels

```bash
bin/benchmark export --output /tmp/solve-cases.jsonl
```

The export excludes gold labels and pair identifiers and includes the gate's
written trigger and response contract. The public corpus is small and inspectable;
it is not a private held-out evaluation set. Avoid tuning prompts on all cases
and then describing the result as independent generalization.

## Run an adapter

An adapter receives one exported JSON case on stdin and returns one JSON
prediction on stdout. It may invoke a configured model or an existing baseline.
No model is called by default. The runner executes only the supplied command,
without a shell, and measures elapsed time for each completed case.

```bash
bin/benchmark run --output /tmp/solve-candidate.jsonl \
  --label 'model/version/settings; candidate revision' --timeout 60 \
  --command python3 /path/to/your_adapter.py
```

Prediction shape:

```json
{
  "case_id": "<exported case ID>",
  "gate_states": {"consumer": "FIRED"},
  "retrieved": ["reader", "disk"],
  "refuted_claims": ["gone"],
  "missing_claims": [],
  "abstain": false,
  "decision": "do-not-confirm",
  "usage": {"input_tokens": 123, "output_tokens": 45}
}
```

The token values above only illustrate the schema. Include usage only when the
provider reports it. The runner records latency; the scorer does not infer tokens
from document bytes. Store model and parameter provenance in the run label.
Adapter failures and timeouts preserve partial predictions, which cannot be scored
as a complete benchmark. Existing output files are not overwritten.

## Score and compare

```bash
bin/benchmark score --predictions /tmp/solve-candidate.jsonl \
  --output /tmp/solve-candidate-score.json
```

Use the same corpus hash, adapter/model settings, and measurement method for a
baseline and candidate. Keep measurements separate:

- Gate accuracy, false N/A, and false FIRED when evidence is BLOCKED.
- Refutation precision/recall, including false accusations.
- Omitted-claim detection precision/recall.
- Retrieval recall@3 and graded nDCG@3 (ranking relevant evidence first).
- Abstention accuracy and action accuracy.
- Paired action accuracy, requiring both sides of the premise change to be correct.
- Reported input/output tokens and observed latency, or null if unavailable.

There is no composite quality score that hides a regression in false N/A or
refutation. The scorer requires the whole corpus exactly once and rejects missing
cases, duplicate IDs, unknown documents, illegal states, and invalid usage.

## What the tests establish

Scorer tests construct known-correct and deliberately wrong predictions to check
the calculations and rejection paths. Runner tests use a local deterministic
adapter. They are software tests, not live-model scores. This release makes no
claim of token savings, model accuracy, or real-world decision success. Actual
model evaluation and outcome follow-up are separate measurements.
