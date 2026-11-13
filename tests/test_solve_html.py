"""HTML view: build, locate, and binding into the consumer subject. No model calls."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_contract as c
import solve_html
from solve_output import render_report
from test_contract import RunFixture


def fake_build(source, output, verify=True):
    """Stand in for html-artifact so binding tests need neither Node nor Chrome."""
    Path(output).write_text(Path(source).read_text())
    return {"path": str(Path(output).resolve()), "sha256": c.file_hash(output)}, "fake build", "fake-skill"


class HtmlViewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-html-")
        self.addCleanup(self.temp.cleanup)
        self.f = RunFixture(self.temp.name)
        self.page = self.f.report.with_suffix(".html")

    def render(self):
        with patch.object(solve_html, "build", fake_build):
            return render_report(self.f.run, self.f.report, "fixture", html=True)

    def complete(self):
        self.f.nonconsumer()
        self.render()
        c.prepare_review(self.f.run, "consumer", "consumer-1", self.f.report)
        c.record_gate(self.f.run, self.f.record("consumer"))
        c.finalize(self.f.run)

    def test_view_joins_subject_and_completion(self):
        self.complete()
        self.assertTrue(c.completion_valid(self.f.run))
        subject = c.read_json(self.f.run / "completion.json")["subject"]
        self.assertEqual(subject["views"], [{"path": str(self.page.resolve()), "sha256": c.file_hash(self.page)}])

    def test_edited_view_invalidates_completion(self):
        self.complete()
        self.page.write_text(self.page.read_text() + "<!-- edited -->")
        self.assertFalse(c.completion_valid(self.f.run))

    def test_view_edited_before_consumer_cannot_be_prepared(self):
        self.f.nonconsumer()
        self.render()
        self.page.write_text("<p>Different decision</p>")
        with self.assertRaisesRegex(c.ContractError, "view changed"):
            c.prepare_review(self.f.run, "consumer", "consumer-1", self.f.report)

    def test_deleted_view_cannot_be_prepared(self):
        self.f.nonconsumer()
        self.render()
        self.page.unlink()
        with self.assertRaisesRegex(c.ContractError, "view path"):
            c.prepare_review(self.f.run, "consumer", "consumer-1", self.f.report)

    def test_malformed_views_rejected(self):
        report = str(self.f.report.resolve())
        self.f.report.write_text("report")
        for views in ("page.html", [{"path": report}], [{"path": report, "sha256": "x", "extra": 1}]):
            with self.subTest(views=views):
                with self.assertRaisesRegex(c.ContractError, "views must be"):
                    c.check_subject({"path": report, "sha256": c.file_hash(self.f.report), "views": views})

    def test_render_without_html_keeps_plain_subject(self):
        self.f.nonconsumer()
        result = render_report(self.f.run, self.f.report, "fixture")
        self.assertNotIn("views", result["subject"])
        self.assertFalse(self.page.exists())

    def test_failed_build_blocks_render_and_writes_no_render_receipt(self):
        self.f.nonconsumer()

        def broken(source, output, verify=True):
            raise c.ContractError("html-artifact build failed (exit 1): ✗ text under 12px")

        with patch.object(solve_html, "build", broken), self.assertRaisesRegex(c.ContractError, "under 12px"):
            render_report(self.f.run, self.f.report, "fixture", html=True)
        self.assertFalse((self.f.run / "render.json").exists())

    def test_page_escapes_text_and_shows_failed_claim(self):
        claims = c.read_json(self.f.run / "claims.json")
        claims[0]["statement"] = "The reader returns <script>alert(1)</script> ready"
        c.write_json(self.f.run / "claims.json", claims)
        for gate in c.catalog().values():
            if gate["kind"] == "framework":
                c.record_gate(self.f.run, self.f.record(gate["id"], "N/A"))
        c.record_gate(self.f.run, self.f.record("evidence", passed=False))
        self.render()
        source = self.f.report.with_name("delivered.src.html").read_text()
        self.assertNotIn("<script>alert", source)
        self.assertIn("&lt;script&gt;", source)
        self.assertIn("Failed a check", source)
        self.assertIn("Unverified draft", source)
        self.assertIn("<h1>Use the fixture reader.</h1>", source)

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_real_html_artifact_build_verifies(self):
        try:
            solve_html.locate_html_artifact()
        except c.ContractError as exc:
            self.skipTest(str(exc))
        self.f.nonconsumer()
        result = render_report(self.f.run, self.f.report, "fixture", html=True)
        self.assertIn("✓", result["html"]["build_log"])
        self.assertEqual(result["subject"]["views"][0]["sha256"], c.file_hash(self.page))


class HtmlArtifactLocatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-html-locate-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_env_override_wins(self):
        (self.root / "scripts").mkdir()
        (self.root / "scripts/build.mjs").write_text("")
        with patch.dict(solve_html.os.environ, {solve_html.HTML_ARTIFACT_ENV: str(self.root)}):
            self.assertEqual(solve_html.locate_html_artifact(), self.root)

    def test_env_override_without_build_script_fails(self):
        with patch.dict(solve_html.os.environ, {solve_html.HTML_ARTIFACT_ENV: str(self.root)}):
            with self.assertRaisesRegex(c.ContractError, "has no scripts/build.mjs"):
                solve_html.locate_html_artifact()

    def test_newest_cache_version_is_preferred(self):
        for version in ("2.0.0", "10.1.0", "9.9.9"):
            script = self.root / version / "skills/html-artifact/scripts/build.mjs"
            script.parent.mkdir(parents=True)
            script.write_text("")
        with patch.dict(solve_html.os.environ, {}, clear=True), patch.object(solve_html, "PLUGIN_CACHE", self.root), \
                patch.object(solve_html, "BUILT_IN", self.root / "none"):
            self.assertEqual(solve_html.locate_html_artifact().parts[-3], "10.1.0")

    def test_built_in_copy_wins_over_plugins(self):
        built_in = self.root / "html"
        (built_in / "scripts").mkdir(parents=True)
        (built_in / "scripts/build.mjs").write_text("")
        plugin = self.root / "cache/9.0.0/skills/html-artifact/scripts"
        plugin.mkdir(parents=True)
        (plugin / "build.mjs").write_text("")
        with patch.dict(solve_html.os.environ, {}, clear=True), patch.object(solve_html, "BUILT_IN", built_in), \
                patch.object(solve_html, "PLUGIN_CACHE", self.root / "cache"):
            self.assertEqual(solve_html.locate_html_artifact(), built_in)

    def test_missing_install_names_the_fix(self):
        with patch.dict(solve_html.os.environ, {}, clear=True), patch.object(solve_html, "PLUGIN_CACHE", self.root), \
                patch.object(solve_html, "SKILL_DIRS", ()), patch.object(solve_html, "BUILT_IN", self.root / "none"):
            with self.assertRaisesRegex(c.ContractError, "bin/html-sync"):
                solve_html.locate_html_artifact()


class HtmlBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-html-build-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.output = self.root / "r.src.html", self.root / "r.html"
        self.source.write_text("<p>x</p>")
        self.locate = patch.object(solve_html, "locate_html_artifact", return_value=self.root)
        self.locate.start()
        self.addCleanup(self.locate.stop)

    def done(self, code, out=""):
        return subprocess.CompletedProcess([], code, out, "")

    def test_nonzero_exit_reports_build_log(self):
        with patch.object(solve_html.subprocess, "run", return_value=self.done(1, "✗ text under 12px")):
            with self.assertRaisesRegex(c.ContractError, "(?s)exit 1.*under 12px"):
                solve_html.build(self.source, self.output)

    def test_missing_node_is_reported(self):
        with patch.object(solve_html.subprocess, "run", side_effect=FileNotFoundError("node")):
            with self.assertRaisesRegex(c.ContractError, "Node.js"):
                solve_html.build(self.source, self.output)

    def test_success_without_output_file_fails(self):
        with patch.object(solve_html.subprocess, "run", return_value=self.done(0, "✓")):
            with self.assertRaisesRegex(c.ContractError, "wrote no file"):
                solve_html.build(self.source, self.output)

    def test_success_returns_hash_and_passes_verify(self):
        def run(command, **_):
            self.assertIn("--verify", command)
            self.output.write_text("<html></html>")
            return self.done(0, "✓")
        with patch.object(solve_html.subprocess, "run", side_effect=run):
            view, log, _ = solve_html.build(self.source, self.output)
        self.assertEqual(view["sha256"], c.file_hash(self.output))
        self.assertEqual(log, "✓")


if __name__ == "__main__":
    unittest.main()
