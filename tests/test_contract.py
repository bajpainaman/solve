"""Adversarial contract fixtures. No model calls or paid APIs."""

import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_contract as c
from solve_output import progress, render_report


class RunFixture:
    def __init__(self, root):
        self.root = Path(root)
        self.run = self.root / "run"
        request = self.root / "original.md"
        request.write_text("Synthetic case: verify that the fixture reader returns ready. No optional analytical trigger applies.\n")
        c.init_run(self.run, request, "builder-1", "quick")
        c.update_state(self.run, {"budget": {"time_seconds": None, "tokens_usd": None},
                                 "recommendation": "Use the fixture reader.", "next_action": "Read through the fixture reader."})
        self.claim = {"id": "reader-ready", "statement": "The reader returns ready", "kind": "fact", "critical": True,
                      "acceptance": {"surface": "fixture://reader", "expected": "ready"}}
        c.write_json(self.run / "claims.json", [self.claim])
        self.proof = self.run / "evidence/observation.md"
        self.proof.write_text("Fixture reader was exercised: expected ready, observed ready. Optional triggers are explicitly absent in this synthetic case.\n")
        self.ref = c.reference(self.run, "evidence/observation.md")
        facts = {g["fact"]: {"value": False, "reason": "The synthetic case explicitly excludes this trigger.", "evidence": [self.ref]}
                 for g in c.catalog().values() if g["fact"]}
        c.write_json(self.run / "facts.json", facts)
        self.report = self.root / "delivered.md"

    def record(self, gate, state="FIRED", passed=True):
        ids = [] if state == "N/A" else [self.claim["id"]]
        ticket = c.inspect_gate(self.run, gate, ids)
        record = {"gate": gate, "state": state, "trigger": ticket["trigger"], "claims": ids,
                  "input_digest": ticket["input_digest"], "reason": "Test observation and result are in the referenced fixture."}
        if state == "FIRED":
            record.update(artifact=self.ref, checks=[{"claim": self.claim["id"], "surface": "fixture://reader", "expected": "ready",
                                                    "observed": "ready" if passed else "missing", "passed": passed, "evidence": [self.ref]}])
        elif state == "BLOCKED":
            record["unverified"] = [self.claim["id"]]
        if gate in ("refutation", "consumer") and state == "FIRED":
            role = "refuter" if gate == "refutation" else "consumer"
            manifest = c.read_json(self.run / f"reviews/{role}/manifest.json")
            record["review"] = {"agent_id": manifest["agent_id"], "manifest": c.reference(self.run, f"reviews/{role}/manifest.json")}
            if role == "refuter":
                record["review"]["reveal"] = c.reference(self.run, "reviews/refuter/reveal.json")
            else:
                record["subject"] = manifest["subject"]
            record["coverage"] = {"complete": True, "missing_claims": [], "unsupported_recommendations": [],
                                  "reason": "The fixture has one material claim and the recommendation depends only on it.", "evidence": [self.ref]}
        return record

    def nonconsumer(self):
        for gate in c.catalog().values():
            if gate["kind"] == "framework":
                c.record_gate(self.run, self.record(gate["id"], "N/A"))
        c.record_gate(self.run, self.record("evidence"))
        c.prepare_review(self.run, "refuter", "refuter-1")
        self.blind()
        c.reveal_claims(self.run)
        c.record_gate(self.run, self.record("refutation"))

    def blind(self):
        c.write_json(self.run / "reviews/refuter/blind.json", {"framing": "Independently check what the reader returns.",
                     "material_claims": ["Reader availability"], "evidence": [self.ref]})

    def ready(self):
        self.nonconsumer()
        render_report(self.run, self.report, "fixture")
        c.prepare_review(self.run, "consumer", "consumer-1", self.report)
        c.record_gate(self.run, self.record("consumer"))


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-contract-")
        self.addCleanup(self.temp.cleanup)
        self.f = RunFixture(self.temp.name)

    def assertBlocked(self, gate):
        result = c.evaluate(self.f.run)
        self.assertFalse(result["ready"])
        self.assertEqual(next(row["state"] for row in result["gates"] if row["gate"] == gate), "BLOCKED")

    def test_complete_flow_binds_actual_delivered_report(self):
        self.f.ready()
        self.assertTrue(c.evaluate(self.f.run)["ready"])
        self.assertFalse(c.completion_valid(self.f.run))
        c.finalize(self.f.run)
        self.assertTrue(c.completion_valid(self.f.run))
        self.assertIn("verified completion", progress(self.f.run, True))

    def test_nonempty_markdown_does_not_count_as_fired(self):
        (self.f.run / "frameworks/first-principles.md").write_text("# Done\n")
        c.update_state(self.f.run, {"phase": "complete", "completed_frameworks": list(c.catalog())})
        self.assertEqual(c.evaluate(self.f.run)["counts"]["FIRED"], 0)
        self.assertFalse(c.completion_valid(self.f.run))
        self.assertIn("unverified", progress(self.f.run, True))

    def test_only_three_states_accepted(self):
        for state in ("DONE", "skipped", "PASS", "pending", "WAIVED"):
            with self.subTest(state=state):
                record = self.f.record("evidence")
                record["state"] = state
                with self.assertRaisesRegex(c.ContractError, "only FIRED"):
                    c.record_gate(self.f.run, record)

    def test_na_cannot_bypass_required_check(self):
        with self.assertRaisesRegex(c.ContractError, "trigger fires"):
            c.record_gate(self.f.run, self.f.record("refutation", "N/A"))

    def test_na_requires_exact_catalog_trigger(self):
        record = self.f.record("minto", "N/A")
        record["trigger"] = "The budget is too small."
        with self.assertRaisesRegex(c.ContractError, "exact written trigger"):
            c.record_gate(self.f.run, record)

    def test_unknown_trigger_is_blocked_not_na(self):
        facts = c.read_json(self.f.run / "facts.json")
        facts.pop("synthesis_complex")
        c.write_json(self.f.run / "facts.json", facts)
        self.assertIsNone(c.inspect_gate(self.f.run, "minto")["trigger_value"])
        with self.assertRaisesRegex(c.ContractError, "unknown"):
            c.record_gate(self.f.run, self.f.record("minto", "N/A"))
        self.assertBlocked("minto")

    def test_unsupported_false_fact_is_unknown(self):
        facts = c.read_json(self.f.run / "facts.json")
        facts["synthesis_complex"]["evidence"] = []
        c.write_json(self.f.run / "facts.json", facts)
        self.assertIsNone(c.inspect_gate(self.f.run, "minto")["trigger_value"])

    def test_true_trigger_cannot_be_na(self):
        facts = c.read_json(self.f.run / "facts.json")
        facts["synthesis_complex"]["value"] = True
        c.write_json(self.f.run / "facts.json", facts)
        with self.assertRaisesRegex(c.ContractError, "trigger fires"):
            c.record_gate(self.f.run, self.f.record("minto", "N/A"))
        c.record_gate(self.f.run, self.f.record("minto"))
        self.assertEqual(c.evaluate(self.f.run)["counts"]["FIRED"], 1)

    def test_changed_fact_invalidates_its_receipt(self):
        c.record_gate(self.f.run, self.f.record("minto", "N/A"))
        facts = c.read_json(self.f.run / "facts.json")
        facts["synthesis_complex"]["value"] = True
        c.write_json(self.f.run / "facts.json", facts)
        self.assertBlocked("minto")

    def test_changed_evidence_invalidates_na_and_fired(self):
        c.record_gate(self.f.run, self.f.record("minto", "N/A"))
        c.record_gate(self.f.run, self.f.record("evidence"))
        self.f.proof.write_text("The observation was corrected.\n")
        self.assertBlocked("minto")
        self.assertBlocked("evidence")

    def test_fired_needs_observation_not_only_artifact(self):
        record = self.f.record("evidence")
        record.pop("checks")
        with self.assertRaisesRegex(c.ContractError, "expected/observed"):
            c.record_gate(self.f.run, record)

    def test_blocked_names_unverified_claims(self):
        record = self.f.record("evidence", "BLOCKED")
        record.pop("unverified")
        with self.assertRaisesRegex(c.ContractError, "remains unverified"):
            c.record_gate(self.f.run, record)

    def test_failed_check_stays_fired_and_cannot_finalize(self):
        c.record_gate(self.f.run, self.f.record("evidence", passed=False))
        result = c.evaluate(self.f.run)
        self.assertEqual(next(r["state"] for r in result["gates"] if r["gate"] == "evidence"), "FIRED")
        self.assertIn("evidence: failed check for reader-ready", result["failures"])
        with self.assertRaises(c.ContractError):
            c.finalize(self.f.run)

    def test_path_escape_and_symlink_escape_rejected(self):
        external = self.f.root / "external.txt"
        external.write_text("outside")
        (self.f.run / "evidence/outside").symlink_to(external)
        for path in ("../external.txt", str(external), "evidence/outside"):
            with self.subTest(path=path), self.assertRaises(c.ContractError):
                c.reference(self.f.run, path)

    def test_reveal_requires_independent_blind_record(self):
        c.prepare_review(self.f.run, "refuter", "refuter-1")
        with self.assertRaises(c.ContractError):
            c.reveal_claims(self.f.run)
        self.assertFalse((self.f.run / "reviews/refuter/claims.json").exists())
        self.f.blind()
        c.reveal_claims(self.f.run)
        with self.assertRaisesRegex(c.ContractError, "already revealed"):
            c.reveal_claims(self.f.run)

    def test_refuter_inputs_do_not_contain_builder_analysis(self):
        (self.f.run / "frameworks/private.md").write_text("Builder's private reasoning.")
        c.prepare_review(self.f.run, "refuter", "refuter-1")
        files = list((self.f.run / "reviews/refuter/inputs").iterdir())
        self.assertEqual({p.name for p in files}, {"request.md", "intake.json"})
        self.assertNotIn("private reasoning", "".join(p.read_text() for p in files))
        self.assertFalse((self.f.run / "reviews/refuter/claims.json").exists())

    def test_builder_and_previous_review_agents_cannot_be_reused(self):
        with self.assertRaises(c.ContractError):
            c.prepare_review(self.f.run, "refuter", "builder-1")
        c.prepare_review(self.f.run, "refuter", "refuter-1")
        c.prepare_review(self.f.run, "refuter", "refuter-2")
        with self.assertRaises(c.ContractError):
            c.prepare_review(self.f.run, "refuter", "refuter-1")

    def test_refuter_and_consumer_cannot_share_context(self):
        self.f.nonconsumer()
        render_report(self.f.run, self.f.report, "fixture")
        with self.assertRaises(c.ContractError):
            c.prepare_review(self.f.run, "consumer", "refuter-1", self.f.report)

    def test_edited_blind_record_invalidates_refutation(self):
        self.f.nonconsumer()
        (self.f.run / "reviews/refuter/blind.json").write_text('{"framing":"rewritten after seeing the answer"}')
        self.assertBlocked("refutation")

    def test_new_recommendation_requires_fresh_refutation(self):
        self.f.nonconsumer()
        c.update_state(self.f.run, {"recommendation": "Use a different reader."})
        self.assertBlocked("refutation")

    def test_next_action_is_reviewed_and_cannot_change_after_completion(self):
        self.f.ready()
        c.finalize(self.f.run)
        self.assertIn("Read through the fixture reader.", self.f.report.read_text())
        c.update_state(self.f.run, {"next_action": "Delete the reader instead."})
        self.assertBlocked("refutation")
        self.assertFalse(c.completion_valid(self.f.run))

    def test_new_critical_claim_invalidates_required_checks(self):
        self.f.nonconsumer()
        second = {**copy.deepcopy(self.f.claim), "id": "missing-critical", "statement": "The second surface works"}
        c.write_json(self.f.run / "claims.json", [self.f.claim, second])
        self.assertBlocked("evidence")
        self.assertBlocked("refutation")

    def test_false_coverage_prevents_completion_even_when_declared_claim_passes(self):
        self.f.nonconsumer()
        record = self.f.record("refutation")
        record["coverage"].update(complete=False, missing_claims=["An unlisted assertion changes the choice"])
        c.record_gate(self.f.run, record)
        self.assertIn("incomplete decision coverage", " ".join(c.evaluate(self.f.run)["failures"]))
        with self.assertRaises(c.ContractError):
            c.finalize(self.f.run)

    def test_consumer_must_check_declared_surface(self):
        self.f.ready()
        record = self.f.record("consumer")
        record["checks"][0]["surface"] = "local filesystem existence"
        with self.assertRaisesRegex(c.ContractError, "declared acceptance surface"):
            c.record_gate(self.f.run, record)

    def test_deleted_file_still_served_by_reader_blocks_completion(self):
        class Reader(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200 if self.server.cached else 404)
                self.end_headers()
                self.wfile.write(b"cached page" if self.server.cached else b"not found")

            def log_message(self, *args):
                pass

        reader = ThreadingHTTPServer(("127.0.0.1", 0), Reader)
        reader.cached = True
        thread = threading.Thread(target=reader.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(reader.server_close)
        self.addCleanup(thread.join, 2)
        self.addCleanup(reader.shutdown)
        url = f"http://127.0.0.1:{reader.server_port}/page"
        source = self.f.run / "deleted-page.md"
        source.write_text("cached page")
        source.unlink()
        self.assertFalse(source.exists())
        self.f.claim.update(statement="The page is absent from the reader",
                            acceptance={"surface": url, "expected": "HTTP 404"})
        c.write_json(self.f.run / "claims.json", [self.f.claim])
        # The earlier fixture checks are optimistic. The actual reader must get
        # the final say, even with a report and passing earlier receipts present.
        self.f.nonconsumer()
        render_report(self.f.run, self.f.report, "cached-reader")
        c.prepare_review(self.f.run, "consumer", "consumer-1", self.f.report)

        def observe(name):
            try:
                response = urlopen(url, timeout=2)
            except HTTPError as exc:
                response = exc
            with response:
                observed = {"url": url, "status": response.code, "body": response.read().decode()}
            c.write_json(self.f.run / name, observed)
            ref = c.reference(self.f.run, name)
            record = self.f.record("consumer")
            record.update(artifact=ref, checks=[{"claim": self.f.claim["id"], "surface": url,
                          "expected": "HTTP 404", "observed": f"HTTP {observed['status']}",
                          "passed": observed["status"] == 404, "evidence": [ref]}])
            c.record_gate(self.f.run, record)

        observe("reviews/consumer/evidence/cached.json")
        self.assertIn("consumer: failed check", " ".join(c.evaluate(self.f.run)["failures"]))
        with self.assertRaises(c.ContractError):
            c.finalize(self.f.run)
        reader.cached = False
        observe("reviews/consumer/evidence/absent.json")
        c.finalize(self.f.run)
        self.assertTrue(c.completion_valid(self.f.run))

    def test_changed_report_invalidates_completion(self):
        self.f.ready()
        c.finalize(self.f.run)
        self.f.report.write_text(self.f.report.read_text() + "\nUnchecked additional recommendation.\n")
        self.assertFalse(c.completion_valid(self.f.run))
        self.assertBlocked("consumer")

    def test_rendering_is_not_finalization(self):
        self.f.nonconsumer()
        for fmt in ("pyramid", "build-up", "tldr"):
            render_report(self.f.run, self.f.report, "fixture", fmt)
            self.assertFalse(c.completion_valid(self.f.run))
            self.assertIn("Gate receipts", self.f.report.read_text())
            self.assertNotIn("Bayesian Posterior", self.f.report.read_text())

    def test_forged_completion_cannot_name_another_consumer_or_report(self):
        self.f.ready()
        receipt = c.finalize(self.f.run)
        other = self.f.root / "another.md"
        other.write_text(self.f.report.read_text())
        receipt["subject"] = {"path": str(other), "sha256": c.file_hash(other)}
        c.write_json(self.f.run / "completion.json", receipt)
        self.assertFalse(c.completion_valid(self.f.run))

    def test_budget_halt_preserves_fired_and_blocks_unfinished(self):
        c.record_gate(self.f.run, self.f.record("evidence"))
        c.halt(self.f.run, "External spend cap exhausted; reader check unverified")
        result = c.evaluate(self.f.run)
        self.assertEqual(next(r["state"] for r in result["gates"] if r["gate"] == "evidence"), "FIRED")
        self.assertBlocked("consumer")
        with self.assertRaises(c.ContractError):
            c.finalize(self.f.run)
        render_report(self.f.run, self.f.report, "fixture")
        self.assertIn("Halted At Budget", self.f.report.read_text())

    def test_live_cost_ledger_cannot_be_hidden_by_stale_budget_status(self):
        self.f.ready()
        c.update_state(self.f.run, {"budget": {"time_seconds": None, "tokens_usd": 0}})
        (self.f.run / "cost-usd").write_text("0.01")
        self.assertIn("external-spend", " ".join(c.evaluate(self.f.run)["failures"]))
        with self.assertRaises(c.ContractError):
            c.finalize(self.f.run)

    def test_halt_during_intake_preserves_unknown_claims(self):
        c.write_json(self.f.run / "claims.json", [])
        c.halt(self.f.run, "Time cap exhausted during intake")
        self.assertEqual(c.evaluate(self.f.run)["counts"]["BLOCKED"], 28)
        self.assertEqual(c.read_json(self.f.run / "claims.json"), [])
        render_report(self.f.run, self.f.report, "incomplete-intake")
        self.assertIn("Time cap exhausted during intake", self.f.report.read_text())

    def test_completed_run_does_not_expire_while_idle(self):
        c.update_state(self.f.run, {"budget": {"time_seconds": 60, "tokens_usd": None}})
        self.f.ready()
        receipt = c.finalize(self.f.run)
        with patch.object(c.time, "time", return_value=time.time() + 120):
            self.assertTrue(c.completion_valid(self.f.run))
            self.assertEqual(c.finalize(self.f.run), receipt)
            self.f.report.write_text("An unreviewed decision")
            self.assertFalse(c.completion_valid(self.f.run))
            self.assertIn("time budget", " ".join(c.evaluate(self.f.run)["failures"]))

    def test_empty_recommendation_cannot_be_revealed_or_finalized(self):
        c.update_state(self.f.run, {"recommendation": ""})
        c.prepare_review(self.f.run, "refuter", "refuter-1")
        self.f.blind()
        with self.assertRaisesRegex(c.ContractError, "recommendation"):
            c.reveal_claims(self.f.run)
        self.assertFalse((self.f.run / "reviews/refuter/reveal.json").exists())
        self.assertIn("recommendation", " ".join(c.evaluate(self.f.run)["failures"]))

    def test_operational_state_updates_do_not_invalidate_finished_review(self):
        self.f.ready()
        c.finalize(self.f.run)
        c.update_state(self.f.run, {"budget_status": {"time_used": 4, "tokens_used": 0, "verdict": "under_cap"}})
        self.assertTrue(c.completion_valid(self.f.run))

    def test_replaced_records_are_preserved(self):
        c.record_gate(self.f.run, self.f.record("evidence", passed=False))
        c.record_gate(self.f.run, self.f.record("evidence"))
        history = [json.loads(line) for line in (self.f.run / "gate-history.jsonl").read_text().splitlines()]
        self.assertFalse(history[0]["record"]["checks"][0]["passed"])

    def test_legacy_run_cannot_acquire_verified_status(self):
        state = c.read_json(self.f.run / "state.json")
        state.pop("schema_version")
        c.write_json(self.f.run / "state.json", state)
        self.assertIn("legacy", c.evaluate(self.f.run)["failures"][0])
        with self.assertRaises(c.ContractError):
            c.finalize(self.f.run)

    def test_malformed_gate_is_reported_blocked(self):
        (self.f.run / "gates/evidence.json").write_text("not json")
        self.assertBlocked("evidence")

    def test_wrong_json_shapes_are_blocked_without_crashing(self):
        self.f.ready()
        for name in ("gates/evidence.json", "reviews/refuter/manifest.json", "reviews/refuter/reveal.json",
                     "reviews/consumer/manifest.json", "render.json", "state.json"):
            with self.subTest(name=name):
                path = self.f.run / name
                original = path.read_bytes()
                try:
                    path.write_text("[]")
                    self.assertFalse(c.evaluate(self.f.run)["ready"])
                    self.assertIn("unverified", progress(self.f.run, True))
                finally:
                    path.write_bytes(original)
        for value in ([], "bad", False):
            with self.subTest(budget_status=value):
                c.update_state(self.f.run, {"budget_status": value})
                self.assertFalse(c.evaluate(self.f.run)["ready"])
                self.assertIn("unverified", progress(self.f.run))

    def test_forecasts_require_assumptions_and_followup(self):
        claim = {**self.f.claim, "kind": "forecast"}
        c.write_json(self.f.run / "claims.json", [claim])
        with self.assertRaisesRegex(c.ContractError, "forecast needs"):
            c.load_run(self.f.run)

    def test_cli_uses_same_validator(self):
        result = subprocess.run([str(c.ROOT / "bin/gates"), "validate", "--run-dir", str(self.f.run)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stdout)["ready"])

    def test_statusline_reports_validated_completion(self):
        self.f.ready()
        c.finalize(self.f.run)
        result = subprocess.run([str(c.ROOT / "bin/statusline"), "--run-dir", str(self.f.run)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FIRED 3 | N/A 25 | BLOCKED 0", result.stdout)
        self.assertIn("verified completion", result.stdout)


if __name__ == "__main__":
    unittest.main()
