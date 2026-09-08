import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_benchmark as b
from solve_contract import ContractError


def oracle_predictions():
    # A scorer oracle, explicitly not a measured model run.
    result = []
    for case in b.corpus():
        gold = case["gold"]
        result.append({"case_id": case["id"], "gate_states": gold["gate_states"].copy(),
                       "retrieved": [doc for doc, grade in sorted(gold["qrels"].items(), key=lambda item: item[1], reverse=True) if grade > 0],
                       "refuted_claims": gold["refuted_claims"].copy(), "missing_claims": gold["missing_claims"].copy(),
                       "abstain": gold["abstain"], "decision": gold["decision"]})
    return result


class BenchmarkTests(unittest.TestCase):
    def test_known_correct_predictions_score_correctly_without_fake_usage(self):
        result = b.score(oracle_predictions())
        self.assertEqual(result["cases"], 14)
        self.assertEqual(result["premise_pairs"], 7)
        for key in ("gate_accuracy", "abstention_accuracy", "decision_accuracy", "paired_decision_accuracy"):
            self.assertEqual(result[key], 1)
        self.assertEqual(result["refutation"]["precision"], 1)
        self.assertEqual(result["omitted_claim_detection"]["recall"], 1)
        self.assertAlmostEqual(result["retrieval"]["mean_ndcg_at_3"], 1)
        self.assertIsNone(result["reported_usage"]["input_tokens"])
        self.assertIsNone(result["reported_usage"]["mean_latency_ms"])

    def test_all_na_strategy_is_penalized(self):
        pred = oracle_predictions()
        for row in pred:
            row["gate_states"] = {key: "N/A" for key in row["gate_states"]}
        result = b.score(pred)
        self.assertGreater(result["false_na"], 0)
        self.assertLess(result["gate_accuracy"], 0.5)

    def test_retrieval_rewards_primary_observation_over_distractor(self):
        pred = oracle_predictions()
        for row, case in zip(pred, b.corpus()):
            row["retrieved"] = [d for d, grade in case["gold"]["qrels"].items() if grade == 0]
        result = b.score(pred)
        self.assertEqual(result["retrieval"]["mean_ndcg_at_3"], 0)
        self.assertEqual(result["retrieval"]["mean_recall_at_3"], 0)

    def test_parroting_unchanged_action_fails_premise_pairs(self):
        pred = oracle_predictions()
        first = {}
        for case, row in zip(b.corpus(), pred):
            first.setdefault(case["pair"], row["decision"])
            row["decision"] = first[case["pair"]]
        self.assertEqual(b.score(pred)["paired_decision_accuracy"], 0)

    def test_unknown_is_not_a_refutation(self):
        pred = oracle_predictions()
        for case, row in zip(b.corpus(), pred):
            if case["gold"]["abstain"]:
                row["refuted_claims"] = list(case["claims"])
        self.assertGreater(b.score(pred)["refutation"]["false_positive"], 0)

    def test_ignoring_omitted_claims_is_detected(self):
        pred = oracle_predictions()
        for row in pred:
            row["missing_claims"] = []
        self.assertEqual(b.score(pred)["omitted_claim_detection"]["recall"], 0)

    def test_incomplete_or_duplicate_runs_cannot_inflate_score(self):
        pred = oracle_predictions()
        for bad in (pred[:-1], pred + [pred[0]]):
            with self.assertRaises(ContractError):
                b.score(bad)

    def test_illegal_states_unknown_ids_and_negative_usage_are_rejected(self):
        for mutate in (
            lambda row: row["gate_states"].update({next(iter(row["gate_states"])): "DONE"}),
            lambda row: row.update(retrieved=["fabricated-source"]),
            lambda row: row.update(usage={"input_tokens": -1, "output_tokens": 5}),
            lambda row: row.update(latency_ms=float("nan")),
        ):
            pred = oracle_predictions()
            mutate(pred[0])
            with self.assertRaises(ContractError):
                b.score(pred)

    def test_export_does_not_disclose_gold_or_pair_labels(self):
        for case in b.corpus():
            public = b.public_case(case)
            self.assertNotIn("gold", public)
            self.assertNotIn("pair", public)
            self.assertEqual(set(public["triggers"]), set(case["gates"]))

    def test_real_runner_measures_adapter_time_and_preserves_outputs(self):
        with tempfile.TemporaryDirectory(prefix="solve-benchmark-") as temp:
            adapter, output = Path(temp) / "adapter.py", Path(temp) / "predictions.jsonl"
            adapter.write_text('''import json, sys
case = json.load(sys.stdin)
assert "gold" not in case
print(json.dumps({"case_id": case["id"], "gate_states": {g:"BLOCKED" for g in case["gates"]}, "retrieved": [], "refuted_claims": [], "missing_claims": [], "abstain": True, "decision": "defer"}))
''')
            meta = b.run_adapter([sys.executable, str(adapter)], output, label="deterministic-test-adapter")
            self.assertTrue(meta["complete"])
            pred = b.read_jsonl(output)
            self.assertTrue(all(row["latency_ms"] > 0 for row in pred))
            self.assertIsNone(b.score(pred)["reported_usage"]["input_tokens"])
            with self.assertRaises(ContractError):
                b.run_adapter([sys.executable, str(adapter)], output)

    def test_cli_runner_honors_command_and_label(self):
        with tempfile.TemporaryDirectory(prefix="solve-benchmark-cli-") as temp:
            output = Path(temp) / "predictions.jsonl"
            code = 'import json,sys; c=json.load(sys.stdin); print(json.dumps(dict(case_id=c["id"], gate_states={g:"BLOCKED" for g in c["gates"]}, retrieved=[], refuted_claims=[], missing_claims=[], abstain=True, decision="defer")))'
            result = subprocess.run([str(b.ROOT / "bin/benchmark"), "run", "--output", str(output), "--label", "cli-test", "--command", sys.executable, "-c", code], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["label"], "cli-test")


if __name__ == "__main__":
    unittest.main()
