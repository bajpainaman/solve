"""bin/check-updates against local git remotes. No network."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_updates as u

IDENTITY = ["-c", "user.email=t@example.com", "-c", "user.name=t"]


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def commit(repo, name):
    (repo / name).write_text(name)
    git(repo, "add", ".")
    git(repo, *IDENTITY, "commit", "-qm", name)
    return git(repo, "rev-parse", "HEAD")


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-updates-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        git(self.upstream, "init", "-q", "-b", "main")
        self.v1 = commit(self.upstream, "v1")
        self.cache = self.root / "cache.json"
        self.sources = self.root / "sources.json"

    def write_sources(self, *sources):
        self.sources.write_text(json.dumps({"schema_version": 1, "sources": list(sources)}))

    def vendored(self, ref):
        return {"id": "lib", "mode": "vendored", "repo": str(self.upstream), "ref": ref, "path": "lib"}

    def run_check(self, **kw):
        return u.check(cache=self.cache, sources_path=self.sources, root=self.root, **kw)["results"]

    def test_current_pin(self):
        self.write_sources(self.vendored(self.v1))
        self.assertEqual(self.run_check(force=True)[0]["status"], "current")

    def test_new_upstream_commit_is_an_update_with_action(self):
        self.write_sources(self.vendored(self.v1))
        v2 = commit(self.upstream, "v2")
        result = self.run_check(force=True)[0]
        self.assertEqual((result["status"], result["latest"]), ("update", v2))
        self.assertIn("sources.json", result["action"])
        self.assertIn("UPDATE   lib:", u.format_report({"results": [result]}, quiet=True))

    def test_unreachable_repo_is_unknown_not_current(self):
        source = self.vendored(self.v1)
        source["repo"] = str(self.root / "missing")
        self.write_sources(source)
        result = self.run_check(force=True)[0]
        self.assertEqual(result["status"], "unknown")
        self.assertIn("UNKNOWN", u.format_report({"results": [result]}, quiet=True))

    def test_fetched_copy_out_of_sync_with_pin_is_flagged(self):
        self.write_sources({**self.vendored(self.v1), "mode": "fetched", "path": "html"})
        (self.root / "html").mkdir()
        (self.root / "html/SOURCE").write_text("ref=" + "0" * 40 + "\n")
        self.assertIn("bin/html-sync", self.run_check(force=True)[0]["local"])

    def test_self_behind_upstream_suggests_pull(self):
        clone = self.root / "clone"
        git(self.root, "clone", "-q", str(self.upstream), str(clone))
        commit(self.upstream, "v2")
        self.write_sources({"id": "solve", "mode": "self", "repo": str(self.upstream), "branch": "main", "path": "."})
        result = u.check(cache=self.cache, sources_path=self.sources, root=clone, force=True)["results"][0]
        self.assertEqual(result["status"], "update")
        self.assertIn("pull --ff-only", result["action"])

    def test_self_ahead_of_upstream_is_current(self):
        clone = self.root / "clone"
        git(self.root, "clone", "-q", str(self.upstream), str(clone))
        commit(clone, "local")
        self.write_sources({"id": "solve", "mode": "self", "repo": str(self.upstream), "branch": "main", "path": "."})
        result = u.check(cache=self.cache, sources_path=self.sources, root=clone, force=True)["results"][0]
        self.assertEqual(result["status"], "current")

    def test_cache_is_reused_within_a_day_and_refreshed_after(self):
        self.write_sources(self.vendored(self.v1))
        first = u.check(cache=self.cache, sources_path=self.sources, root=self.root, now=1000.0)
        commit(self.upstream, "v2")
        again = u.check(cache=self.cache, sources_path=self.sources, root=self.root, now=1000.0 + 60)
        self.assertTrue(again["cached"])
        self.assertEqual(again["results"], first["results"])
        later = u.check(cache=self.cache, sources_path=self.sources, root=self.root, now=1000.0 + u.CACHE_TTL_SECONDS + 1)
        self.assertFalse(later["cached"])
        self.assertEqual(later["results"][0]["status"], "update")

    def test_short_pin_is_rejected(self):
        self.write_sources(self.vendored(self.v1[:12]))
        with self.assertRaisesRegex(u.ContractError, "40-character"):
            u.load_sources(self.sources)

    def test_repo_pins_are_full_and_html_sync_reads_them(self):
        sources = u.load_sources()
        self.assertEqual({s["id"] for s in sources}, {"solve", "html-artifact", "html-effectiveness", "simplify-writing"})
        import solve_bundle
        self.assertEqual(solve_bundle.REF, u.pinned_ref("html-artifact"))


if __name__ == "__main__":
    unittest.main()
