"""Portable HTML boundaries, delivery behavior, and decision hash binding."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_contract as c
import solve_portable as portable
from solve_output import render_report
from test_contract import RunFixture


class PortableArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-portable-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.page = self.root / "note.html"
        self.data = {"title": "Run the reversible pilot", "summary": "Measure success before the wider rollout.",
                     "sections": [{"heading": "Evidence", "paragraphs": ["The available measurement is incomplete."],
                                   "table": {"headers": ["Option", "Observed"], "rows": [["Pilot", "Not yet measured"]]}},
                                  {"heading": "Raw observation", "collapsed": True, "preformatted": "Synthetic example only."}],
                     "sources": [{"label": "Primary source", "url": "https://example.com/source?a=1&b=2"}]}

    def build(self, **kwargs):
        return portable.build_document(self.data, self.page, **kwargs)

    def test_all_author_text_is_inert_and_page_has_no_external_assets(self):
        hostile = '<script>alert("x")</script><img src=x onerror=alert(1)>'
        self.data["title"] = hostile
        self.data["sections"][0]["paragraphs"] = [hostile]
        self.data["sections"][0]["table"]["rows"][0][0] = hostile
        self.data["sources"][0]["label"] = hostile
        result = self.build()
        page = self.page.read_text()
        self.assertNotIn("<script>", page)
        self.assertNotIn("<img", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertEqual(result["static"]["status"], "passed")
        self.assertEqual(result["browser"]["status"], "not_run")
        self.assertFalse(result["verified_decision"])
        self.assertEqual(portable.verify(self.page)["static"]["status"], "passed")

    def test_unsafe_source_urls_are_rejected_before_writing(self):
        for url in ("javascript:alert(1)", "data:text/html,hi", "file:///etc/passwd", "//example.com/x", "https://user:password@example.com", "https://example.com/\nnext", "https://example.com/?access_token=privatevalue"):
            with self.subTest(url=url):
                self.data["sources"][0]["url"] = url
                with self.assertRaises(c.ContractError):
                    self.build()
                self.assertFalse(self.page.exists())
                self.assertFalse(self.page.with_name("note.src.json").exists())

    def test_credential_shapes_do_not_reach_html_or_source_copy(self):
        for secret in ("sk-" + "a" * 32, "-----BEGIN PRIVATE KEY-----", 'api_key = "' + "x" * 32 + '"'):
            with self.subTest(kind=secret[:6]):
                self.data["sections"][0]["paragraphs"] = [secret]
                with self.assertRaisesRegex(c.ContractError, "credential"):
                    self.build()
                self.assertFalse(self.page.exists())
                self.assertFalse(self.page.with_name("note.src.json").exists())

    def test_schema_errors_do_not_generate_partial_artifacts(self):
        self.data["sections"][0]["table"]["rows"] = [["missing column"]]
        with self.assertRaisesRegex(c.ContractError, "width"):
            self.build()
        self.assertFalse(self.page.exists())

    def test_existing_output_is_preserved_without_explicit_overwrite(self):
        self.page.write_text("original")
        with self.assertRaisesRegex(c.ContractError, "already exists"):
            self.build()
        self.assertEqual(self.page.read_text(), "original")
        self.assertFalse(self.page.with_name("note.src.json").exists())

    def test_existing_source_is_preserved_without_explicit_overwrite(self):
        source = self.page.with_name("note.src.json")
        source.write_text("original source")
        with self.assertRaisesRegex(c.ContractError, "already exists"):
            self.build()
        self.assertEqual(source.read_text(), "original source")
        self.assertFalse(self.page.exists())

    def test_symlink_output_cannot_replace_its_target_even_with_overwrite(self):
        original = self.root / "original.txt"
        original.write_text("keep")
        self.page.symlink_to(original)
        with self.assertRaisesRegex(c.ContractError, "symlink"):
            self.build(overwrite=True)
        self.assertEqual(original.read_text(), "keep")

    def test_output_cannot_alias_the_input(self):
        source = self.root / "input.json"
        source.write_text(json.dumps(self.data))
        self.page.hardlink_to(source)
        original = source.read_bytes()
        with self.assertRaisesRegex(c.ContractError, "alias"):
            self.build(overwrite=True, input_path=source)
        self.assertEqual(source.read_bytes(), original)

    def test_using_named_source_preserves_exact_input_bytes(self):
        source = self.root / "note.src.json"
        source.write_text(json.dumps(self.data, separators=(",", ":")))
        original = source.read_bytes()
        result = self.build(input_path=source)
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(result["source_sha256"], c.file_hash(source))

    def test_source_copy_can_rebuild_the_same_page(self):
        result = self.build()
        copied_data = json.loads(Path(result["source"]).read_text())
        rebuilt = self.root / "rebuilt.html"
        portable.build_document(copied_data, rebuilt)
        self.assertEqual(rebuilt.read_bytes(), self.page.read_bytes())

    def test_static_verification_rejects_injected_active_content(self):
        self.build()
        self.page.write_text(self.page.read_text().replace("</body>", '<script src="https://example.com/x.js"></script></body>'))
        result = portable.verify(self.page, browser=True)
        self.assertFalse(result["ok"])
        self.assertEqual(result["static"]["status"], "failed")
        self.assertEqual(result["browser"]["status"], "not_run")

    def test_relative_dependencies_are_not_standalone(self):
        self.build()
        self.page.write_text(self.page.read_text().replace("https://example.com/source?a=1&amp;b=2", "evidence.txt"))
        self.assertFalse(portable.verify(self.page)["ok"])

    @unittest.skipUnless(os.environ.get("SOLVE_RUN_BROWSER_TESTS") == "1" and shutil.which("chromium") and importlib.util.find_spec("playwright"),
                         "live browser test is opt-in: SOLVE_RUN_BROWSER_TESTS=1")
    def test_real_browser_checks_dark_mobile_layout_and_disclosure(self):
        self.data["sections"][0]["table"]["rows"][0][0] = "LongIdentifier" * 80
        self.build()
        result = portable.verify(self.page, browser=True)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["browser"]["status"], "passed")
        self.assertEqual(len(result["browser"]["samples"]), 4)
        self.assertEqual(result["browser"]["network_requests"], [])


class PortableDecisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-portable-decision-")
        self.addCleanup(self.temp.cleanup)
        self.fixture = RunFixture(self.temp.name)
        self.page = self.fixture.report.with_suffix(".html")

    def test_decision_embeds_evidence_without_missing_relative_links(self):
        self.fixture.nonconsumer()
        result = render_report(self.fixture.run, self.fixture.report, "fixture", portable_html=True)
        page = self.page.read_text()
        self.assertIn("Fixture reader was exercised", page)
        self.assertIn("Snapshot: gates/evidence.json", page)
        self.assertIn("Snapshot: claims.json", page)
        self.assertIn("independent consumer review and finalization remain separate", page)
        self.assertNotIn('href="', page)
        self.assertEqual(result["subject"]["views"], [{"path": str(self.page.resolve()), "sha256": c.file_hash(self.page)}])
        self.assertFalse(result["html"]["verified_decision"])

    def test_portable_view_tamper_invalidates_completion(self):
        self.fixture.nonconsumer()
        render_report(self.fixture.run, self.fixture.report, "fixture", portable_html=True)
        c.prepare_review(self.fixture.run, "consumer", "consumer-1", self.fixture.report)
        c.record_gate(self.fixture.run, self.fixture.record("consumer"))
        c.finalize(self.fixture.run)
        self.assertTrue(c.completion_valid(self.fixture.run))
        self.page.write_text(self.page.read_text() + "<!-- changed -->")
        self.assertFalse(c.completion_valid(self.fixture.run))

    def test_blocked_run_remains_an_unverified_draft(self):
        render_report(self.fixture.run, self.fixture.report, "fixture", portable_html=True)
        self.assertIn("Unverified draft", self.page.read_text())
        self.assertIn("Not checked", self.page.read_text())
        self.assertFalse(c.completion_valid(self.fixture.run))

    def test_failed_check_is_never_shown_as_a_passing_claim(self):
        c.record_gate(self.fixture.run, self.fixture.record("evidence", passed=False))
        render_report(self.fixture.run, self.fixture.report, "fixture", portable_html=True)
        self.assertIn("Failed a check", self.page.read_text())
        self.assertIn("Unverified draft", self.page.read_text())

    def test_two_renderers_cannot_be_selected_together(self):
        with self.assertRaisesRegex(c.ContractError, "not both"):
            render_report(self.fixture.run, self.fixture.report, "fixture", html=True, portable_html=True)
        self.assertFalse(self.fixture.report.exists())

    def test_json_evidence_cannot_add_unrelated_snapshot_files(self):
        private = self.fixture.run / "evidence/private.txt"
        private.write_text("SHOULD_NOT_APPEAR_INTERNAL_PRIVATE_CONTENT")
        payload = self.fixture.run / "evidence/payload.json"
        payload.write_text(json.dumps({"injected_reference": c.reference(self.fixture.run, "evidence/private.txt")}))
        self.fixture.ref = c.reference(self.fixture.run, "evidence/payload.json")
        self.fixture.nonconsumer()
        render_report(self.fixture.run, self.fixture.report, "fixture", portable_html=True)
        page = self.page.read_text()
        self.assertIn("Snapshot: evidence/payload.json", page)
        self.assertNotIn("Snapshot: evidence/private.txt", page)
        self.assertNotIn("SHOULD_NOT_APPEAR_INTERNAL_PRIVATE_CONTENT", page)


if __name__ == "__main__":
    unittest.main()
