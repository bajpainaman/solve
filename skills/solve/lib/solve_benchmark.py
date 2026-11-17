"""Small synthetic evaluation corpus, blind export, adapter runner, and scorer."""

import argparse
import collections
import json
import math
from pathlib import Path
import subprocess
import sys
import time

from solve_contract import ContractError, ROOT, STATES, catalog, file_hash, read_json, require, write_json

CASES = ROOT / "benchmarks/cases.jsonl"


def read_jsonl(path):
    try:
        return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    except (OSError, ValueError) as exc:
        raise ContractError(f"invalid JSONL: {path}: {exc}") from exc


def corpus(path=CASES):
    cases = read_jsonl(path)
    require(cases and len({c["id"] for c in cases}) == len(cases), "case IDs must be unique")
    return cases


def public_case(case):
    gates = catalog()
    result = {key: value for key, value in case.items() if key not in ("gold", "pair")}
    result["triggers"] = {gate: gates[gate]["trigger"] for gate in case["gates"]}
    result["response_contract"] = {
        "case_id": case["id"], "gate_states": "exactly the listed gates; FIRED, N/A, or BLOCKED",
        "retrieved": "ranked unique document IDs", "refuted_claims": "declared claim IDs contradicted by evidence; unknown is not false",
        "missing_claims": "material report claim IDs absent from the claim ledger", "abstain": "Boolean: insufficient evidence to choose",
        "decision": "short action label, e.g. confirm, do-not-confirm, direct, staged, defer, choose-a, resolve-conflict, proceed, add-cap, deliver, revise, covered, add-missing-claim",
        "usage": "optional actual provider input_tokens/output_tokens; omit when unavailable",
    }
    result["instructions"] = "Use only the synthetic supplied observations. Assess listed gates against their triggers and evidence availability. Return JSON, not prose. Do not claim to have executed a real deployment or solved a future outcome."
    return result


def id_list(value, allowed, field):
    require(isinstance(value, list) and all(isinstance(x, str) for x in value), f"{field} must be a list of IDs")
    require(len(value) == len(set(value)), f"duplicate IDs in {field}")
    require(set(value) <= set(allowed), f"unknown ID in {field}")
    return set(value)


def numeric(value, name, integer=False):
    require(type(value) in ((int,) if integer else (int, float)) and math.isfinite(value) and value >= 0,
            f"{name} must be finite and non-negative")
    return value


def validate_prediction(case, prediction):
    require(isinstance(prediction, dict) and prediction.get("case_id") == case["id"], "prediction case ID differs from request")
    states = prediction.get("gate_states")
    require(isinstance(states, dict) and set(states) == set(case["gates"]), "prediction must cover exactly the requested gates")
    require(all(v in STATES for v in states.values()), "illegal predicted gate state")
    docs = {d["id"] for d in case["documents"]}
    id_list(prediction.get("retrieved"), docs, "retrieved")
    id_list(prediction.get("refuted_claims"), case["claims"], "refuted_claims")
    id_list(prediction.get("missing_claims"), case.get("report_claims", {}), "missing_claims")
    require(type(prediction.get("abstain")) is bool, "abstain must be Boolean")
    require(isinstance(prediction.get("decision"), str) and prediction["decision"].strip(), "decision action label required")
    if "usage" in prediction:
        require(isinstance(prediction["usage"], dict), "usage must be an object")
        for key in ("input_tokens", "output_tokens"):
            numeric(prediction["usage"].get(key), key, integer=True)
    if "latency_ms" in prediction:
        numeric(prediction["latency_ms"], "latency_ms")


def precision_recall(tp, fp, fn):
    return {"precision": tp / (tp + fp) if tp + fp else (0.0 if fn else 1.0),
            "recall": tp / (tp + fn) if tp + fn else 1.0, "true_positive": tp, "false_positive": fp, "false_negative": fn}


def score(predictions, case_path=CASES):
    cases = corpus(case_path)
    require(all(isinstance(p, dict) and isinstance(p.get("case_id"), str) for p in predictions), "every prediction needs a case_id")
    by_id = {p["case_id"]: p for p in predictions}
    require(len(by_id) == len(predictions), "duplicate prediction case IDs")
    require(set(by_id) == {c["id"] for c in cases}, "predictions must cover the entire corpus exactly; partial runs cannot be scored")
    totals = collections.Counter()
    pairs = collections.defaultdict(list)
    details, recalls, ndcgs, token_values, latencies = [], [], [], [], []
    for case in cases:
        pred, gold = by_id[case["id"]], case["gold"]
        validate_prediction(case, pred)
        for gate, expected in gold["gate_states"].items():
            actual = pred["gate_states"][gate]
            totals["gate_total"] += 1
            totals["gate_correct"] += actual == expected
            totals["false_na"] += actual == "N/A" and expected != "N/A"
            totals["false_fired"] += actual == "FIRED" and expected == "BLOCKED"
        for field, prefix in (("refuted_claims", "refutation"), ("missing_claims", "coverage")):
            got, wanted = set(pred[field]), set(gold[field])
            totals[prefix + "_tp"] += len(got & wanted)
            totals[prefix + "_fp"] += len(got - wanted)
            totals[prefix + "_fn"] += len(wanted - got)
        relevant = {doc for doc, grade in gold["qrels"].items() if grade > 0}
        ranked = pred["retrieved"][:3]
        recall = len(set(ranked) & relevant) / len(relevant) if relevant else 1.0
        gains = [(2 ** gold["qrels"].get(doc, 0) - 1) / math.log2(i + 2) for i, doc in enumerate(ranked)]
        ideal = sum((2 ** grade - 1) / math.log2(i + 2) for i, grade in enumerate(sorted(gold["qrels"].values(), reverse=True)[:3]))
        ndcg = sum(gains) / ideal if ideal else 1.0
        recalls.append(recall)
        ndcgs.append(ndcg)
        decision_ok = pred["decision"].strip().lower() == gold["decision"]
        totals["decision_correct"] += decision_ok
        totals["abstention_correct"] += pred["abstain"] == gold["abstain"]
        pairs[case["pair"]].append(decision_ok)
        if "usage" in pred:
            token_values.append(pred["usage"])
        if "latency_ms" in pred:
            latencies.append(pred["latency_ms"])
        details.append({"case_id": case["id"], "decision_correct": decision_ok, "recall_at_3": recall, "ndcg_at_3": ndcg})
    count = len(cases)
    all_usage, all_latency = len(token_values) == count, len(latencies) == count
    return {
        "corpus_sha256": file_hash(case_path), "cases": count, "synthetic": True,
        "gate_accuracy": totals["gate_correct"] / totals["gate_total"], "gate_checks": totals["gate_total"],
        "false_na": totals["false_na"], "false_fired_on_blocked": totals["false_fired"],
        "refutation": precision_recall(totals["refutation_tp"], totals["refutation_fp"], totals["refutation_fn"]),
        "omitted_claim_detection": precision_recall(totals["coverage_tp"], totals["coverage_fp"], totals["coverage_fn"]),
        "retrieval": {"mean_recall_at_3": sum(recalls) / count, "mean_ndcg_at_3": sum(ndcgs) / count},
        "abstention_accuracy": totals["abstention_correct"] / count,
        "decision_accuracy": totals["decision_correct"] / count,
        "premise_pairs": len(pairs), "paired_decision_accuracy": sum(all(v) for v in pairs.values()) / len(pairs),
        "reported_usage": {"cases_with_tokens": len(token_values), "cases_with_latency": len(latencies),
                           "input_tokens": sum(v["input_tokens"] for v in token_values) if all_usage else None,
                           "output_tokens": sum(v["output_tokens"] for v in token_values) if all_usage else None,
                           "mean_latency_ms": sum(latencies) / count if all_latency else None},
        "limits": ["Synthetic, public, deterministic cases; not a real-world decision-success estimate.",
                   "Usage is supplied by the provider/adapter; absent measurements are not estimated.",
                   "Do not interpret tests using gold-derived predictions as model benchmark results."],
        "per_case": details,
    }


def run_adapter(command, output, case_path=CASES, timeout=60, label="unspecified"):
    require(command and timeout > 0 and math.isfinite(timeout), "adapter command and positive finite timeout required")
    output = Path(output)
    require(not output.exists(), "preserve existing predictions; choose a new output path")
    metadata_path = output.with_suffix(output.suffix + ".run.json")
    require(not metadata_path.exists(), "preserve existing run metadata; choose a new output path")
    cases = corpus(case_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = {"label": label, "adapter_executable": command[0], "corpus_sha256": file_hash(case_path),
                "timeout_seconds": timeout, "started_at": time.time(), "completed_cases": 0, "complete": False}
    write_json(metadata_path, metadata)
    with output.open("x") as handle:
        for case in cases:
            started = time.perf_counter()
            try:
                proc = subprocess.run(command, input=json.dumps(public_case(case)), text=True, capture_output=True, timeout=timeout, check=False)
            except subprocess.TimeoutExpired as exc:
                raise ContractError(f"adapter timed out on {case['id']}; partial predictions preserved") from exc
            require(proc.returncode == 0, f"adapter failed on {case['id']} with exit {proc.returncode}; partial predictions preserved")
            try:
                prediction = json.loads(proc.stdout)
            except ValueError as exc:
                raise ContractError(f"adapter returned invalid JSON for {case['id']}") from exc
            validate_prediction(case, prediction)
            prediction["latency_ms"] = (time.perf_counter() - started) * 1000
            handle.write(json.dumps(prediction) + "\n")
            handle.flush()
            metadata["completed_cases"] += 1
            write_json(metadata_path, metadata)
    metadata.update(complete=True, completed_at=time.time())
    write_json(metadata_path, metadata)
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evaluate synthetic solve verification cases without inventing model measurements")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("export", "score", "run"):
        p = sub.add_parser(name)
        p.add_argument("--cases", type=Path, default=CASES)
        p.add_argument("--output", type=Path)
        if name == "score":
            p.add_argument("--predictions", type=Path, required=True)
        if name == "run":
            p.add_argument("--timeout", type=float, default=60)
            p.add_argument("--label", default="unspecified")
            p.add_argument("--command", dest="adapter", nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            content = "".join(json.dumps(public_case(c)) + "\n" for c in corpus(args.cases))
            if args.output:
                require(not args.output.exists(), "choose a new export path")
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(content)
            else:
                print(content, end="")
        elif args.command == "score":
            result = score(read_jsonl(args.predictions), args.cases)
            if args.output:
                require(args.output.resolve() not in (args.predictions.resolve(), args.cases.resolve()), "score output cannot overwrite predictions or corpus")
                write_json(args.output, result)
            print(json.dumps(result, indent=2))
        else:
            require(args.output is not None, "run requires --output")
            result = run_adapter(args.adapter, args.output, args.cases, args.timeout, args.label)
            print(json.dumps(result, indent=2))
        return 0
    except (ContractError, OSError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
