"""Template catalog integrity and routing. No model calls."""

from pathlib import Path
import contextlib
import io
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_templates as t

TEMPLATE_DIR = t.ROOT / "templates/html-effectiveness"


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.data = t.load()
        self.templates = self.data["templates"]

    def test_every_exemplar_is_cataloged_once(self):
        on_disk = {str(p.relative_to(t.ROOT / "templates")) for p in TEMPLATE_DIR.rglob("*.html") if p.name != "index.html"}
        cataloged = [x["file"] for x in self.templates if x["file"]]
        self.assertEqual(len(cataloged), len(set(cataloged)))
        self.assertEqual(set(cataloged), on_disk)
        self.assertEqual(len(on_disk), 31)

    def test_each_renderer_has_instructions_and_needed_fields(self):
        self.assertEqual(set(self.data["renderers"]), set(t.RENDERERS))
        for x in self.templates:
            with self.subTest(template=x["id"]):
                if x["renderer"] == "artifact":
                    self.assertTrue(x["artifact_type"] and x["components"])
                if x["renderer"] == "bespoke":
                    self.assertIsNone(x["artifact_type"])
                    self.assertTrue(x["file"], "a bespoke page needs an exemplar")
                self.assertTrue(all(p == p.lower() for p in x["use_when"]), "phrases are matched in lower case")

    def test_artifact_types_exist_in_installed_html_artifact(self):
        skill = t.html_artifact_dir()
        if skill is None:
            self.skipTest("html-artifact is not installed")
        for x in self.templates:
            if x.get("artifact_type"):
                with self.subTest(template=x["id"]):
                    self.assertTrue((skill / "references/types" / (x["artifact_type"] + ".md")).is_file())

    def test_licenses_travel_with_vendored_code(self):
        self.assertIn("Apache License", (TEMPLATE_DIR / "LICENSE").read_text())
        self.assertIn("MIT License", (t.ROOT / "write/LICENSE").read_text())


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.templates = t.load()["templates"]

    def top(self, request):
        hits = t.match(request, self.templates)
        return hits[0][1]["id"] if hits else None

    def test_requests_route_to_expected_template(self):
        cases = {
            "write up the outage from last night": "incident-report",
            "should we build or buy our feature flag system": "decision-memo",
            "review this PR as a page": "pr-review",
            "what am I missing before I start on the auth module": "blindspot-pass",
            "make slides for friday": "slide-deck",
            "tune the prompt for the classifier": "prompt-tuner",
            "weekly status report for the team": "status-report",
            "interview me about this ambiguous feature": "interview",
            "quiz me on this change before I merge": "change-quiz",
            "draw the deploy pipeline as a flowchart": "flowchart",
        }
        for request, expected in cases.items():
            with self.subTest(request=request):
                self.assertEqual(self.top(request), expected)

    def test_unrelated_request_matches_nothing(self):
        self.assertIsNone(self.top("zzz qqq"))

    def test_artifact_templates_fall_back_to_bespoke_without_html_artifact(self):
        plan = next(x for x in self.templates if x["id"] == "implementation-plan")
        memo = next(x for x in self.templates if x["id"] == "decision-memo")
        self.assertEqual(t.effective_renderer(plan, None), "bespoke")
        self.assertEqual(t.effective_renderer(plan, Path("/x")), "artifact")
        self.assertEqual(t.effective_renderer(memo, None), "solve")

    def test_cli_show_and_unknown_id(self):
        with patch.object(t, "html_artifact_dir", return_value=None):
            self.assertEqual(t.main(["show", "pr-review"]), 0)
            self.assertEqual(t.main(["show", "nope"]), 2)
            self.assertEqual(t.main(["match", "make slides", "--json"]), 0)

    def test_portable_routing_never_discovers_or_suggests_unbundled_html(self):
        with patch.object(t, "html_artifact_dir", side_effect=AssertionError("should not inspect external plugins")):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(t.main(["show", "pr-review", "--portable"]), 0)
                self.assertEqual(t.main(["show", "decision-memo", "--portable"]), 0)
                self.assertEqual(t.main(["show", "prompt-tuner", "--portable"]), 0)
            self.assertNotIn("html-sync", output.getvalue())
            self.assertIn("bin/artifact build", output.getvalue())
            self.assertIn("--portable-html", output.getvalue())
            self.assertIn("host browser workflow", output.getvalue())


if __name__ == "__main__":
    unittest.main()
