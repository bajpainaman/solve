"""Evidence-bound gate receipts. Standard library only; not a semantic truth oracle."""

import argparse
import contextlib
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "gates/catalog.json"
STATES = ("FIRED", "N/A", "BLOCKED")
PROFILES = {
    "quick": {"time_seconds": 900, "tokens_usd": 2, "evidence_depth": "focused"},
    "standard": {"time_seconds": 1800, "tokens_usd": 5, "evidence_depth": "cross-check"},
    "deep": {"time_seconds": 3600, "tokens_usd": 15, "evidence_depth": "replicate"},
}


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (OSError, ValueError) as exc:
        raise ContractError(f"cannot read valid JSON at {path}: {exc}") from exc


def read_object(path):
    value = read_json(path)
    require(isinstance(value, dict), f"JSON object required at {path}")
    return value


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".solve-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def write_json(path, value):
    atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False).encode() + b"\n")


@contextlib.contextmanager
def run_lock(run):
    run = Path(run)
    run.mkdir(parents=True, exist_ok=True)
    with (run / ".gates.lock").open("a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def update_state(run, values):
    path = Path(run) / "state.json"
    with path.with_suffix(".json.lock").open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = read_object(path)
        state.update(values)
        write_json(path, state)


def catalog():
    data = read_object(CATALOG_PATH)
    require(data.get("version") == 2 and data.get("states") == list(STATES), "unsupported catalog contract")
    entries = data.get("gates", [])
    require(len({g["id"] for g in entries}) == len(entries), "duplicate gate IDs")
    return {g["id"]: g for g in entries}


def inside(run, name):
    require(isinstance(name, str) and name and not Path(name).is_absolute(), "evidence path must be relative to the run")
    require(".." not in Path(name).parts, "evidence path cannot contain '..'")
    root = Path(run).resolve()
    resolved = (root / name).resolve()
    require(root in resolved.parents, f"evidence path escapes run: {name}")
    return resolved


def reference(run, name):
    path = inside(run, name)
    require(path.is_file() and path.stat().st_size > 0, f"missing or empty artifact: {name}")
    return {"path": name, "sha256": file_hash(path)}


def check_reference(run, ref):
    require(isinstance(ref, dict), "evidence reference must be an object")
    actual = reference(run, ref.get("path"))
    require(ref.get("sha256") == actual["sha256"], f"stale evidence: {actual['path']}")
    return actual


def check_references(run, refs):
    require(isinstance(refs, list) and refs, "at least one hashed observation is required")
    for ref in refs:
        check_reference(run, ref)


def load_run(run):
    run = Path(run)
    state = read_json(run / "state.json")
    require(isinstance(state, dict) and state.get("schema_version") == 2,
            "legacy/uninitialized run is unverified; preserve it and initialize a new 2.0 run")
    require(text_value(state.get("builder_id")), "builder identity is missing")
    require(state.get("tier") in PROFILES, "invalid tier")
    reference(run, "request.md")
    intake = read_json(run / "intake.json")
    require(isinstance(intake, dict), "intake must be an object")
    claims = read_json(run / "claims.json")
    require(isinstance(claims, list) and claims, "claims must contain at least one critical claim")
    found = {}
    for claim in claims:
        require(isinstance(claim, dict), "claim must be an object")
        claim_id = claim.get("id")
        require(isinstance(claim_id, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", claim_id), "invalid claim ID")
        require(claim_id not in found, f"duplicate claim ID: {claim_id}")
        require(text_value(claim.get("statement")), f"{claim_id}: statement required")
        require(claim.get("kind") in ("fact", "forecast", "preference"), f"{claim_id}: kind must be fact, forecast, or preference")
        require(type(claim.get("critical")) is bool, f"{claim_id}: critical must be Boolean")
        acceptance = claim.get("acceptance", {})
        require(isinstance(acceptance, dict) and text_value(acceptance.get("surface")) and text_value(acceptance.get("expected")),
                f"{claim_id}: acceptance needs a consumer surface and expected result")
        if claim["kind"] == "forecast":
            require(text_value(claim.get("assumptions")) and text_value(claim.get("followup")), f"{claim_id}: forecast needs assumptions and followup")
        found[claim_id] = claim
    require(any(c["critical"] for c in claims), "at least one claim must be critical")
    facts = read_json(run / "facts.json")
    require(isinstance(facts, dict), "facts must be an object")
    return state, found, facts


def trigger_value(run, gate, facts):
    if gate["fact"] is None:
        return True, None
    fact = facts.get(gate["fact"])
    if not isinstance(fact, dict) or type(fact.get("value")) is not bool:
        return None, f"{gate['fact']} is unknown; {gate['trigger']}"
    try:
        require(text_value(fact.get("reason")), "applicability fact needs an explanation")
        check_references(run, fact.get("evidence"))
    except ContractError as exc:
        return None, str(exc)
    return fact["value"], None


def input_digest(run, gate, claim_ids, claims=None, facts=None):
    if claims is None:
        _, claims, facts = load_run(run)
    require(isinstance(claim_ids, list) and all(isinstance(c, str) for c in claim_ids)
            and len(set(claim_ids)) == len(claim_ids), "claims must be unique IDs")
    require(all(c in claims for c in claim_ids), "gate refers to an unknown claim")
    selected = claims if gate["kind"] == "required" else {c: claims[c] for c in claim_ids}
    state = read_object(Path(run) / "state.json")
    return digest({
        "catalog": file_hash(CATALOG_PATH), "request": file_hash(Path(run) / "request.md"),
        "intake": file_hash(Path(run) / "intake.json"), "claims": selected,
        "fact": facts.get(gate["fact"]) if gate["fact"] else None,
        "recommendation": state.get("recommendation") if gate["id"] == "refutation" else None,
        "next_action": state.get("next_action") if gate["id"] == "refutation" else None,
    })


def decision_digest(run):
    state, _, _ = load_run(run)
    files = {name: file_hash(Path(run) / name) for name in ("request.md", "intake.json", "claims.json", "facts.json")}
    receipts = {}
    for gate_id in catalog():
        if gate_id == "consumer":
            continue
        path = Path(run) / "gates" / f"{gate_id}.json"
        receipts[gate_id] = file_hash(path) if path.is_file() else None
    return digest({"catalog": file_hash(CATALOG_PATH), "inputs": files, "receipts": receipts,
                   "decision": {key: state.get(key) for key in ("recommendation", "next_action", "tldr", "format", "tier", "partial", "budget")}})


def inspect_gate(run, gate_id, claim_ids=None):
    gates = catalog()
    require(gate_id in gates, f"unknown gate: {gate_id}")
    _, claims, facts = load_run(run)
    ids = claim_ids if claim_ids is not None else list(claims)
    gate = gates[gate_id]
    value, reason = trigger_value(run, gate, facts)
    return {**gate, "trigger_value": value, "obstruction": reason, "claims": ids,
            "input_digest": input_digest(run, gate, ids, claims, facts)}


def check_coverage(run, record):
    coverage = record.get("coverage")
    require(isinstance(coverage, dict), "independent review requires a coverage assessment")
    require(type(coverage.get("complete")) is bool, "coverage.complete must be Boolean")
    require(isinstance(coverage.get("missing_claims"), list), "coverage.missing_claims must be a list")
    require(isinstance(coverage.get("unsupported_recommendations"), list), "coverage.unsupported_recommendations must be a list")
    require(all(text_value(item) for item in coverage["missing_claims"] + coverage["unsupported_recommendations"]),
            "coverage gaps must name the missing claim or unsupported recommendation")
    require(text_value(coverage.get("reason")), "coverage assessment needs reasoning")
    check_references(run, coverage.get("evidence"))
    gaps = coverage["missing_claims"] + coverage["unsupported_recommendations"]
    require(not coverage["complete"] or not gaps, "complete coverage cannot contain unresolved gaps")
    return [] if coverage["complete"] and not gaps else ["independent review found incomplete decision coverage"]


def check_review(run, record, state):
    role = "refuter" if record["gate"] == "refutation" else "consumer"
    review = record.get("review", {})
    require(isinstance(review, dict), "review must be an object")
    manifest_path = f"reviews/{role}/manifest.json"
    require(review.get("manifest") == reference(run, manifest_path), "review manifest is missing or stale")
    manifest = read_object(inside(run, manifest_path))
    require(manifest.get("role") == role and manifest.get("fork_turns") == "none", "review requires a fresh, non-inherited context")
    require(text_value(review.get("agent_id")) and review["agent_id"] == manifest.get("agent_id"), "reviewer identity differs from prepared identity")
    require(review["agent_id"] != state["builder_id"], "builder cannot review its own result")
    other = "consumer" if role == "refuter" else "refuter"
    other_path = Path(run) / "reviews" / other / "manifest.json"
    if other_path.exists():
        require(review["agent_id"] != read_object(other_path).get("agent_id"), "independent roles cannot reuse an agent")
    require(manifest.get("request_sha256") == file_hash(Path(run) / "request.md"), "review request changed")
    require(manifest.get("intake_sha256") == file_hash(Path(run) / "intake.json"), "review constraints changed")
    check_references(run, manifest.get("inputs"))
    if role == "refuter":
        reveal = read_object(Path(run) / "reviews/refuter/reveal.json")
        require(review.get("reveal") == reference(run, "reviews/refuter/reveal.json"), "refuter must bind the claim reveal receipt")
        check_reference(run, reveal.get("blind"))
        check_reference(run, reveal.get("claims"))
        require(reveal.get("definitions_digest") == definitions_digest(run), "claim definitions or gate declarations changed after reveal")
        require(reveal.get("manifest") == reference(run, manifest_path), "refutation was prepared under another context")
    else:
        subject = manifest.get("subject", {})
        require(subject == record.get("subject"), "consumer must identify the prepared report path and hash")
        check_subject(subject)
        require(manifest.get("decision_digest") == decision_digest(run), "decision changed after consumer preparation")
        rendered = read_object(Path(run) / "render.json")
        require(rendered.get("subject") == subject and rendered.get("decision_digest") == manifest["decision_digest"], "consumer did not review the current render")


def validate_record(run, record):
    require(isinstance(record, dict), "gate record must be an object")
    state, claims, facts = load_run(run)
    gates = catalog()
    gate_id = record.get("gate")
    require(gate_id in gates, f"unknown gate: {gate_id}")
    gate = gates[gate_id]
    require(record.get("state") in STATES, "only FIRED, N/A, and BLOCKED are legal gate states")
    require(record.get("trigger") == gate["trigger"], "receipt must quote the gate's own exact written trigger")
    ids = record.get("claims")
    require(isinstance(ids, list) and all(isinstance(c, str) for c in ids), "claims must be a list of IDs")
    require(record.get("input_digest") == input_digest(run, gate, ids, claims, facts), "gate inputs changed or input digest is missing")
    require(text_value(record.get("reason")), "gate record needs a reason")
    value, obstruction = trigger_value(run, gate, facts)
    if record["state"] == "BLOCKED":
        require(isinstance(record.get("unverified"), list) and record["unverified"] and all(text_value(x) for x in record["unverified"]),
                "BLOCKED must name what remains unverified")
        return []
    if record["state"] == "N/A":
        require(value is False, obstruction or "N/A is illegal because the gate's trigger fires")
        return []
    require(value is True, obstruction or "FIRED requires the gate's trigger to be true")
    require(ids, "FIRED must name affected claims")
    check_reference(run, record.get("artifact"))
    checks = record.get("checks")
    require(isinstance(checks, list) and checks, "FIRED requires expected/observed checks, not just an artifact")
    covered = set()
    failures = []
    for check in checks:
        require(isinstance(check, dict) and check.get("claim") in ids, "check must identify one of the gate's claims")
        claim_id = check["claim"]
        for field in ("surface", "expected", "observed"):
            require(text_value(check.get(field)), f"check requires {field}")
        require(type(check.get("passed")) is bool, "check.passed must be Boolean; FIRED is not a pass")
        check_references(run, check.get("evidence"))
        if gate_id == "consumer":
            acceptance = claims[claim_id]["acceptance"]
            require(check["surface"] == acceptance["surface"] and check["expected"] == acceptance["expected"],
                    f"{claim_id}: consumer check must exercise the declared acceptance surface and expectation")
        covered.add(claim_id)
        if not check["passed"]:
            failures.append(f"{gate_id}: failed check for {claim_id}")
    require(set(ids) <= covered, "every affected claim needs a check")
    if gate["kind"] == "required":
        require({c for c in claims if claims[c]["critical"]} <= covered, f"{gate_id}: every critical claim must be checked")
    if gate_id in ("refutation", "consumer"):
        check_review(run, record, state)
        failures.extend(check_coverage(run, record))
    return failures


def budget_obstruction(state, run=None, checked_at=None):
    require(type(state.get("partial")) is bool, "partial flag must be Boolean")
    status = state.get("budget_status", {})
    require(isinstance(status, dict), "budget status must be an object")
    budget = state.get("budget")
    require(isinstance(budget, dict), "budget must be an object with explicit caps or null values")
    require("tokens_usd" in budget and "time_seconds" in budget, "budget caps must be explicit; null means unlimited")
    if state.get("partial"):
        return "run is partial; unfinished verification cannot be finalized"
    if str(status.get("verdict", "")).startswith("halted"):
        return "declared resource budget was exhausted"
    spend_cap = budget.get("tokens_usd")
    if spend_cap is not None and run is not None:
        require(type(spend_cap) in (int, float) and math.isfinite(spend_cap) and spend_cap >= 0, "invalid spend budget")
        try:
            used = float((Path(run) / "cost-usd").read_text().strip())
        except (ValueError, OSError) as exc:
            raise ContractError("spend ledger is missing or invalid") from exc
        require(math.isfinite(used) and used >= 0, "invalid spend ledger")
        if used > 0 and (spend_cap == 0 or used >= spend_cap):
            return "declared external-spend budget was exhausted"
    cap = budget.get("time_seconds")
    if cap is not None:
        require(type(cap) in (int, float) and math.isfinite(cap) and cap > 0, "invalid time budget")
        start = state.get("started_at")
        require(type(start) in (int, float) and math.isfinite(start), "invalid start timestamp")
        if (time.time() if checked_at is None else checked_at) - start >= cap:
            return "declared time budget was exhausted"
    return None


def evaluate(run, include_consumer=True):
    gates = catalog()
    try:
        state, claims, facts = load_run(run)
        completion = bound_completion(run)
        obstruction = budget_obstruction(state, run, completion.get("verified_at") if completion else None)
    except (ContractError, TypeError) as exc:
        return {"ready": False, "complete": False, "counts": {"FIRED": 0, "N/A": 0, "BLOCKED": len(gates)},
                "gates": [{"gate": g, "state": "BLOCKED", "reason": str(exc), "unverified": ["decision claims"]} for g in gates],
                "failures": [str(exc)], "claims": []}
    rows, failures = [], []
    if obstruction:
        failures.append(obstruction)
    if not text_value(state.get("recommendation")):
        failures.append("a recommendation is required before independent review and finalization")
    if not text_value(state.get("next_action")):
        failures.append("a next action is required before independent review and finalization")
    for gate_id, gate in gates.items():
        if gate_id == "consumer" and not include_consumer:
            continue
        path = Path(run) / "gates" / f"{gate_id}.json"
        try:
            require(path.is_file(), "no valid gate receipt recorded")
            record = read_object(path)
            require(record.get("gate") == gate_id, "gate filename and identity differ")
            failures.extend(validate_record(run, record))
            row = {"gate": gate_id, "state": record["state"], "reason": record["reason"], "claims": record["claims"]}
            if record["state"] == "BLOCKED":
                row["unverified"] = record["unverified"]
        except (ContractError, TypeError, KeyError) as exc:
            value, reason = trigger_value(run, gate, facts)
            row = {"gate": gate_id, "state": "BLOCKED", "reason": reason or str(exc),
                   "unverified": [c for c in claims if claims[c]["critical"]], "trigger_value": value}
        rows.append(row)
    counts = {s: sum(r["state"] == s for r in rows) for s in STATES}
    ready = counts["BLOCKED"] == 0 and not failures
    return {"ready": ready, "complete": False, "counts": counts, "gates": rows, "failures": failures, "claims": list(claims.values())}


def record_gate(run, record):
    run = Path(run)
    with run_lock(run):
        validate_record(run, record)
        path = run / "gates" / f"{record['gate']}.json"
        if path.exists():
            with (run / "gate-history.jsonl").open("ab") as handle:
                handle.write(canonical({"replaced_at": time.time(), "record": read_json(path)}) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
        write_json(path, {**record, "recorded_at": time.time()})


def init_run(run, request, builder_id, tier, slug=None):
    run = Path(run)
    require(tier in PROFILES and text_value(builder_id), "valid tier and builder identity required")
    content = Path(request).read_bytes()
    require(content.strip(), "original user request is empty")
    with run_lock(run):
        require(not (run / "state.json").exists(), "run already exists; preserve and resume it, or choose a new directory")
        require(not any((run / name).exists() for name in ("request.md", "intake.json", "claims.json", "facts.json", "gates", "reviews")),
                "run contains prior artifacts; choose a new directory")
        for directory in ("gates", "frameworks", "evidence", "research", "reviews"):
            (run / directory).mkdir(exist_ok=True)
        atomic_write(run / "request.md", content)
        write_json(run / "intake.json", {"constraints": [], "success_criteria": "Unverified: derive from the user's request"})
        write_json(run / "claims.json", [])
        write_json(run / "facts.json", {})
        write_json(run / "state.json", {"schema_version": 2, "slug": slug or run.name, "problem": content.decode(),
                   "builder_id": builder_id, "tier": tier, "regime": "decision", "phase": "intake", "partial": False,
                   "format": "pyramid", "budget": {k: PROFILES[tier][k] for k in ("time_seconds", "tokens_usd")},
                   "started_at": time.time(), "completed_frameworks": []})
        atomic_write(run / "cost-usd", b"0\n")


def definitions_digest(run):
    state, claims, facts = load_run(run)
    return digest({"claims": claims, "facts": facts, "catalog": file_hash(CATALOG_PATH),
                   "recommendation": state.get("recommendation"), "next_action": state.get("next_action")})


def check_subject(subject):
    require(isinstance(subject, dict) and text_value(subject.get("path")), "consumer subject missing")
    path = Path(subject["path"])
    require(path.is_absolute() and path.is_file() and path.stat().st_size > 0, "consumer must read the actual report path")
    require(subject.get("sha256") == file_hash(path), "report changed after review")
    views = subject.get("views", [])
    require(isinstance(views, list) and all(isinstance(v, dict) and set(v) == {"path", "sha256"} for v in views),
            "report views must be a list of path and hash objects")
    for view in views:
        view_path = Path(str(view["path"]))
        require(view_path.is_absolute() and view_path.is_file() and view_path.stat().st_size > 0,
                "consumer must read the actual report view path")
        require(view["sha256"] == file_hash(view_path), "report view changed after review")


def prepare_review(run, role, agent_id, report=None):
    run = Path(run)
    require(role in ("refuter", "consumer"), "unknown independent review role")
    state = read_object(run / "state.json")
    require(state.get("schema_version") == 2 and text_value(agent_id) and agent_id != state.get("builder_id"), "reviewer must have a fresh identity distinct from the builder")
    with run_lock(run):
        for prior_path in (run / "reviews").glob("*/manifest.json"):
            require(read_object(prior_path).get("agent_id") != agent_id, "a fresh review cannot reuse any earlier review agent")
        subject = None
        if role == "consumer":
            result = evaluate(run, include_consumer=False)
            require(result["ready"], "pre-consumer checks are incomplete or failed; render only an unverified draft")
            require(report is not None, "consumer preparation requires --report")
            subject = {"path": str(Path(report).resolve()), "sha256": file_hash(report)}
            rendered = read_object(run / "render.json")
            # Views built with the report (the HTML page) are part of what the consumer reviews.
            views = rendered.get("subject", {}).get("views") if isinstance(rendered.get("subject"), dict) else None
            if views is not None:
                subject["views"] = views
            check_subject(subject)
            require(rendered.get("subject") == subject and rendered.get("decision_digest") == decision_digest(run), "report must be rendered from the current decision")
        folder = run / "reviews" / role
        if folder.exists():
            prior = read_object(folder / "manifest.json")
            require(prior.get("agent_id") != agent_id, "a repeated review needs a new agent identity")
            folder.rename(folder.with_name(f"{role}.previous.{time.time_ns()}"))
        folder.mkdir(parents=True)
        inputs = []
        for source in ("request.md", "intake.json"):
            target = f"reviews/{role}/inputs/{source}"
            atomic_write(run / target, (run / source).read_bytes())
            inputs.append(reference(run, target))
        manifest = {"role": role, "agent_id": agent_id, "fork_turns": "none", "created_at": time.time(),
                    "request_sha256": file_hash(run / "request.md"), "intake_sha256": file_hash(run / "intake.json"), "inputs": inputs}
        if role == "consumer":
            manifest.update(subject=subject, decision_digest=decision_digest(run))
        write_json(folder / "manifest.json", manifest)
        return manifest


def reveal_claims(run):
    run = Path(run)
    with run_lock(run):
        manifest = read_object(run / "reviews/refuter/manifest.json")
        require(manifest.get("request_sha256") == file_hash(run / "request.md") and manifest.get("intake_sha256") == file_hash(run / "intake.json"), "original review inputs changed")
        require(not (run / "reviews/refuter/reveal.json").exists(), "claims already revealed; changed claims require a new independent review")
        blind = read_object(run / "reviews/refuter/blind.json")
        require(text_value(blind.get("framing")) and isinstance(blind.get("material_claims"), list) and blind["material_claims"],
                "refuter must commit an independent framing and material claims before reveal")
        check_references(run, blind.get("evidence"))
        state, claims, facts = load_run(run)
        require(text_value(state.get("recommendation")), "record the proposed recommendation before revealing claims")
        require(text_value(state.get("next_action")), "record the proposed next action before revealing claims")
        # Deliberately omit builder evidence, rationale, confidence, and framework outputs.
        allowed = ("id", "statement", "kind", "critical", "acceptance", "assumptions", "followup")
        payload = {"claims": [{k: c[k] for k in allowed if k in c} for c in claims.values()],
                   "recommendation": state["recommendation"],
                   "next_action": state["next_action"],
                   "gate_facts": facts, "triggers": [{"id": g["id"], "trigger": g["trigger"], "fact": g["fact"]} for g in catalog().values()]}
        write_json(run / "reviews/refuter/claims.json", payload)
        receipt = {"revealed_at": time.time(), "manifest": reference(run, "reviews/refuter/manifest.json"),
                   "blind": reference(run, "reviews/refuter/blind.json"), "claims": reference(run, "reviews/refuter/claims.json"),
                   "definitions_digest": definitions_digest(run)}
        write_json(run / "reviews/refuter/reveal.json", receipt)
        return receipt


def finalize(run):
    run = Path(run)
    with run_lock(run):
        result = evaluate(run)
        require(result["ready"], "cannot finalize: " + "; ".join(result["failures"] + [r["gate"] + ": " + r["reason"] for r in result["gates"] if r["state"] == "BLOCKED"]))
        existing = bound_completion(run)
        if existing is not None:
            return existing
        subject = read_json(run / "reviews/consumer/manifest.json")["subject"]
        completion = {"schema_version": 2, "verified_at": time.time(), "subject": subject,
                      "decision_digest": decision_digest(run), "consumer": reference(run, "gates/consumer.json")}
        write_json(run / "completion.json", completion)
        update_state(run, {"phase": "complete", "completed_at": time.time(),
                     "completed_frameworks": [r["gate"] for r in result["gates"] if r["state"] == "FIRED" and catalog()[r["gate"]]["kind"] == "framework"]})
        return completion


def bound_completion(run):
    """Check receipt binding without evaluating gates or recursively checking budgets."""
    try:
        receipt = read_object(Path(run) / "completion.json")
        require(receipt.get("schema_version") == 2, "unsupported completion receipt")
        verified_at = receipt.get("verified_at")
        require(type(verified_at) in (int, float) and math.isfinite(verified_at) and verified_at <= time.time(),
                "invalid completion timestamp")
        consumer = read_object(Path(run) / "gates/consumer.json")
        recorded_at = consumer.get("recorded_at")
        require(type(recorded_at) in (int, float) and math.isfinite(recorded_at) and recorded_at <= verified_at,
                "completion predates its consumer check")
        check_subject(receipt.get("subject"))
        check_reference(run, receipt.get("consumer"))
        require(receipt.get("subject") == read_object(Path(run) / "reviews/consumer/manifest.json").get("subject"), "completion refers to another report")
        require(receipt.get("consumer") == reference(run, "gates/consumer.json"), "completion refers to another consumer receipt")
        require(receipt.get("decision_digest") == decision_digest(run), "decision changed after finalization")
        return receipt
    except (ContractError, OSError, TypeError, KeyError):
        return None


def completion_valid(run, result=None):
    result = result if result is not None else evaluate(run)
    return result["ready"] and bound_completion(run) is not None


def halt(run, reason):
    require(text_value(reason), "halt needs a resource obstruction")
    update_state(run, {"partial": True, "phase": "blocked", "halt_reason": reason})
    try:
        load_run(run)
    except ContractError:
        # Intake may exhaust the budget before any claim can be defined. The
        # validator already reports every gate BLOCKED; do not invent claims.
        return
    result = evaluate(run)
    for row in result["gates"]:
        if row["state"] != "BLOCKED":
            continue
        item = inspect_gate(run, row["gate"])
        record_gate(run, {"gate": row["gate"], "state": "BLOCKED", "trigger": item["trigger"],
                          "claims": item["claims"], "input_digest": item["input_digest"], "reason": reason,
                          "unverified": row.get("unverified") or item["claims"]})


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect and enforce solve's three-state gate contract")
    sub = parser.add_subparsers(dest="command", required=True)
    cat = sub.add_parser("catalog", help="list cheap triggers without loading methods")
    cat.add_argument("--gate")
    for name in ("init", "inspect", "record", "validate", "prepare", "reveal", "finalize", "hash", "halt"):
        p = sub.add_parser(name)
        p.add_argument("--run-dir", required=True)
        if name == "init":
            p.add_argument("--request", required=True)
            p.add_argument("--builder-id", required=True)
            p.add_argument("--tier", choices=PROFILES, default="standard")
            p.add_argument("--slug")
        elif name == "inspect":
            p.add_argument("--gate", required=True)
            p.add_argument("--claims", nargs="*")
        elif name == "record":
            p.add_argument("--file", required=True)
        elif name == "prepare":
            p.add_argument("--role", choices=("refuter", "consumer"), required=True)
            p.add_argument("--agent-id", required=True)
            p.add_argument("--report")
        elif name == "hash":
            p.add_argument("path")
        elif name == "halt":
            p.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    result, code = None, 0
    try:
        if args.command == "catalog":
            data = catalog()
            require(not args.gate or args.gate in data, "unknown gate")
            result = data[args.gate] if args.gate else list(data.values())
        elif args.command == "init":
            init_run(args.run_dir, args.request, args.builder_id, args.tier, args.slug)
            result = {"initialized": args.run_dir, "schema_version": 2}
        elif args.command == "inspect":
            result = inspect_gate(args.run_dir, args.gate, args.claims)
        elif args.command == "record":
            record_gate(args.run_dir, read_json(args.file))
            result = {"recorded": True}
        elif args.command == "validate":
            result = evaluate(args.run_dir)
            result["complete"] = completion_valid(args.run_dir, result)
            code = 0 if result["ready"] else 2
        elif args.command == "prepare":
            result = prepare_review(args.run_dir, args.role, args.agent_id, args.report)
        elif args.command == "reveal":
            result = reveal_claims(args.run_dir)
        elif args.command == "finalize":
            result = finalize(args.run_dir)
        elif args.command == "hash":
            result = reference(args.run_dir, args.path)
        elif args.command == "halt":
            halt(args.run_dir, args.reason)
            result = evaluate(args.run_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return code
    except (ContractError, OSError, TypeError, KeyError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
