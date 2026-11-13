"""Prose lint: field extraction, linter handling, and CLI behavior. No model calls."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_contract as c
import solve_prose
from test_contract import RunFixture


class ProseCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-prose-")
        self.addCleanup(self.temp.cleanup)
        self.f = RunFixture(self.temp.name)

    def test_extract_scopes_and_maps_lines_to_fields(self):
        c.update_state(self.f.run, {"tldr": ["First point.", "Second point."]})
        text, labels = solve_prose.extract(self.f.run, "all")
        rows = text.splitlines()
        self.assertNotIn("#", text)
        self.assertEqual(labels[rows.index("Use the fixture reader.") + 1], "recommendation")
        self.assertEqual(labels[rows.index("Second point.") + 1], "tldr 2")
        self.assertEqual(labels[rows.index("The reader returns ready") + 1], "claim reader-ready statement")
        claims_only, _ = solve_prose.extract(self.f.run, "claims")
        self.assertNotIn("Use the fixture reader.", claims_only)

    def test_missing_linters_are_reported_not_hidden(self):
        with patch.object(solve_prose.shutil, "which", return_value=None):
            result = solve_prose.lint(self.f.report, Path(self.temp.name), "description")
        self.assertEqual(result["findings"], [])
        self.assertEqual(len(result["skipped"]), 2)

    def test_cli_does_not_change_decision_digest(self):
        before = c.decision_digest(self.f.run)
        try:
            solve_prose.locate_simplify_writing()
        except c.ContractError as exc:
            self.skipTest(str(exc))
        self.assertEqual(solve_prose.main(["--run-dir", str(self.f.run), "--scope", "all"]), 0)
        self.assertEqual(c.decision_digest(self.f.run), before)
        self.assertIn("findings", json.loads((self.f.run / "prose/all-lint.json").read_text()))


class SimplifyWritingLocatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-prose-locate-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_env_override_wins(self):
        (self.root / "vale").mkdir()
        (self.root / "vale/description.ini").write_text("")
        with patch.dict(solve_prose.os.environ, {solve_prose.SIMPLIFY_WRITING_ENV: str(self.root)}):
            self.assertEqual(solve_prose.locate_simplify_writing(), self.root)

    def test_bad_env_override_fails(self):
        with patch.dict(solve_prose.os.environ, {solve_prose.SIMPLIFY_WRITING_ENV: str(self.root)}):
            with self.assertRaisesRegex(c.ContractError, "no vale/description.ini"):
                solve_prose.locate_simplify_writing()

    def test_missing_install_names_the_fix(self):
        with patch.dict(solve_prose.os.environ, {}, clear=True), patch.object(solve_prose, "SKILL_DIRS", ()), \
                patch.object(solve_prose, "PLUGIN_CACHE", self.root), patch.object(solve_prose, "BUILT_IN", self.root / "none"):
            with self.assertRaisesRegex(c.ContractError, "simplify-writing is not installed"):
                solve_prose.locate_simplify_writing()


    def test_built_in_write_mode_is_preferred(self):
        with patch.dict(solve_prose.os.environ, {}, clear=True):
            self.assertEqual(solve_prose.locate_simplify_writing(), solve_prose.BUILT_IN)
        self.assertTrue((solve_prose.BUILT_IN / "WRITE.md").is_file())


class ProseTextTests(unittest.TestCase):
    def test_html_keeps_visible_prose_only(self):
        with tempfile.TemporaryDirectory() as d:
            page = Path(d) / "p.html"
            page.write_text("<style>.x{}</style><h1>Ship it</h1><script>var secret=1</script><pre>code()</pre><p>Now.</p>")
            text = solve_prose.prose_text(page)
        self.assertIn("Ship it", text)
        self.assertIn("Now.", text)
        for hidden in (".x{}", "secret", "code()", "<h1>"):
            self.assertNotIn(hidden, text)

    def test_markdown_is_linted_as_is(self):
        with tempfile.TemporaryDirectory() as d:
            doc = Path(d) / "p.md"
            doc.write_text("# Title\n")
            self.assertIsNone(solve_prose.prose_text(doc))


class ProseCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-prose-cli-")
        self.addCleanup(self.temp.cleanup)
        self.f = RunFixture(self.temp.name)

    def test_needs_exactly_one_target(self):
        self.assertEqual(solve_prose.main([]), 2)
        self.assertEqual(solve_prose.main(["--run-dir", str(self.f.run), "--file", str(self.f.root / "original.md")]), 2)

    def test_file_mode_lints_without_a_run(self):
        doc = self.f.root / "note.md"
        doc.write_text("In order to leverage this, we utilize it.\n")
        fake = {"file": str(doc), "profile": "description", "findings": [], "skipped": [], "counts": {}}
        with patch.object(solve_prose, "locate_simplify_writing", return_value=self.f.root), \
                patch.object(solve_prose, "lint", return_value=fake) as lint:
            self.assertEqual(solve_prose.main(["--file", str(doc)]), 0)
        self.assertEqual(lint.call_args.args[0], doc.resolve())
        self.assertFalse((self.f.run / "prose").exists())

    def test_missing_run_dir_blocks(self):
        self.assertEqual(solve_prose.main(["--run-dir", str(self.f.root / "absent")]), 2)

    def test_report_mode_rejects_non_markdown(self):
        other = self.f.root / "report.html"
        other.write_text("<p>x</p>")
        with patch.object(solve_prose, "locate_simplify_writing", return_value=self.f.root):
            self.assertEqual(solve_prose.main(["--run-dir", str(self.f.run), "--report", str(other)]), 2)

    def test_claims_scope_without_claims_blocks(self):
        (self.f.run / "claims.json").unlink()
        with patch.object(solve_prose, "locate_simplify_writing", return_value=self.f.root):
            self.assertEqual(solve_prose.main(["--run-dir", str(self.f.run), "--scope", "claims"]), 2)


if __name__ == "__main__":
    unittest.main()
