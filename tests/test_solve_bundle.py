"""bin/html-sync: pinned fetch of html-artifact into the built-in HTML mode. Local git only."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_bundle as b
from solve_contract import ContractError


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-bundle-")
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.repo, self.dest = root / "upstream", root / "solve/html"
        self.dest.parent.mkdir()
        skill = self.repo / b.SKILL_PATH
        for name in b.REQUIRED:
            (skill / name).parent.mkdir(parents=True, exist_ok=True)
            (skill / name).write_text(f"// {name}\n")
        (skill / "SKILL.md").write_text("---\nname: html-artifact\n---\n\n# html-artifact\n\nRun `<skill-dir>/scripts/build.mjs`.\n")
        git(self.repo, "init", "-q")
        git(self.repo, "-c", "user.email=t@example.com", "-c", "user.name=t", "add", ".")
        git(self.repo, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qm", "v1")
        self.ref = git(self.repo, "rev-parse", "HEAD")

    def sync(self, **kw):
        return b.sync(str(self.repo), kw.pop("ref", self.ref), self.dest, **kw)

    def test_sync_installs_guide_without_skill_frontmatter(self):
        self.assertEqual(self.sync()["status"], "synced")
        guide = (self.dest / "HTML.md").read_text()
        self.assertNotIn("name: html-artifact", guide)
        self.assertIn("Do not commit or redistribute", guide)
        self.assertIn("`<skill-dir>` below means `$SOLVE_ROOT/html`", guide)
        self.assertFalse((self.dest / "SKILL.md").exists(), "a SKILL.md would register a second skill")
        self.assertTrue((self.dest / "scripts/build.mjs").is_file())
        self.assertEqual(b.installed_ref(self.dest), self.ref)

    def test_second_sync_is_a_no_op_unless_forced(self):
        self.sync()
        self.assertEqual(self.sync()["status"], "current")
        self.assertEqual(self.sync(force=True)["status"], "synced")

    def test_bad_ref_keeps_the_existing_copy(self):
        self.sync()
        with self.assertRaisesRegex(ContractError, "git checkout"):
            self.sync(ref="0" * 40, force=True)
        self.assertEqual(b.installed_ref(self.dest), self.ref)
        self.assertFalse(self.dest.with_name("html.new").exists())

    def test_upstream_without_build_script_is_rejected(self):
        (self.repo / b.SKILL_PATH / "scripts/build.mjs").unlink()
        git(self.repo, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qam", "drop build")
        with self.assertRaisesRegex(ContractError, "scripts/build.mjs"):
            self.sync(ref=git(self.repo, "rev-parse", "HEAD"))
        self.assertFalse(self.dest.exists())

    def test_fetched_copy_is_git_ignored(self):
        ignore = (b.ROOT / ".gitignore").read_text().splitlines()
        self.assertIn("/html/", ignore)
        self.assertIn("/html.new/", ignore)


if __name__ == "__main__":
    unittest.main()
