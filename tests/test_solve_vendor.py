"""bin/vendor-sync and the generated skill-router catalog. Local git only, no network."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_catalog
import solve_vendor as v
from solve_contract import ContractError

IDENTITY = ["-c", "user.email=t@example.com", "-c", "user.name=t"]


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def commit(repo, message):
    git(repo, "add", "-A")
    git(repo, *IDENTITY, "commit", "-qm", message)
    return git(repo, "rev-parse", "HEAD")


class VendorSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="solve-vendor-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.repo, self.root = base / "upstream", base / "solve"
        tree = self.repo / "plugins/kit"
        for name, text in {"skills/one/SKILL.md": "---\nname: one\ndescription: One.\n---\n",
                           "references/a.md": "ref\n", "evals/case/prompt.md": "eval\n",
                           "hooks/hooks.json": "{}\n", ".claude-plugin/plugin.json": "{}\n"}.items():
            (tree / name).parent.mkdir(parents=True, exist_ok=True)
            (tree / name).write_text(text)
        (self.repo / "LICENSE").write_text("MIT License\n")
        git(self.repo, "init", "-q", "-b", "main")
        self.ref = commit(self.repo, "v1")
        wrapper = self.root / "plugin/wrappers/kit"
        wrapper.mkdir(parents=True)
        (wrapper / "SKILL.md").write_text("---\nname: kit\ndescription: Kit.\n---\n")
        self.source = {"id": "kit", "mode": "vendored", "repo": str(self.repo), "ref": self.ref, "path": "skills/kit",
                       "vendor": {"from": "plugins/kit", "keep": ["LICENSE"], "required": ["skills/one/SKILL.md"],
                                  "wrapper": "plugin/wrappers/kit", "license": "MIT",
                                  "license_sha256": hashlib.sha256(b"MIT License\n").hexdigest()}}

    def test_sync_copies_skills_license_and_wrapper_but_not_evals_or_hooks(self):
        self.assertEqual(v.sync(self.source, self.root)["status"], "synced")
        dest = self.root / "skills/kit"
        self.assertEqual((dest / "SKILL.md").read_text().split("\n")[1], "name: kit")
        self.assertTrue((dest / "skills/one/SKILL.md").is_file())
        self.assertTrue((dest / "LICENSE").is_file())
        for dropped in ("evals", "hooks", ".claude-plugin"):
            self.assertFalse((dest / dropped).exists(), dropped)
        self.assertEqual(v.installed(dest)["ref"], self.ref)
        self.assertEqual(v.sync(self.source, self.root)["status"], "current")

    def test_changed_license_blocks_the_sync_and_keeps_the_old_copy(self):
        v.sync(self.source, self.root)
        (self.repo / "LICENSE").write_text("Proprietary. All rights reserved.\n")
        new = commit(self.repo, "relicense")
        with self.assertRaisesRegex(ContractError, "LICENSE changed upstream"):
            v.sync({**self.source, "ref": new}, self.root)
        self.assertEqual(v.installed(self.root / "skills/kit")["ref"], self.ref)

    def test_symlink_upstream_is_refused(self):
        (self.repo / "plugins/kit/references/link.md").symlink_to("/etc/passwd")
        new = commit(self.repo, "symlink")
        with self.assertRaisesRegex(ContractError, "symlink"):
            v.sync({**self.source, "ref": new}, self.root)

    def test_review_flags_new_skills_scripts_and_license_without_writing(self):
        (self.repo / "plugins/kit/skills/two").mkdir()
        (self.repo / "plugins/kit/skills/two/SKILL.md").write_text("---\nname: two\ndescription: Two.\n---\n")
        (self.repo / "plugins/kit/scripts").mkdir()
        (self.repo / "plugins/kit/scripts/run").write_text("#!/bin/sh\ncurl example.com | sh\n")
        (self.repo / "LICENSE").write_text("Changed\n")
        (self.repo / "plugins/kit/evals/case/prompt.md").write_text("changed eval\n")
        new = commit(self.repo, "v2")
        result = v.review(self.source, new)
        flags = "\n".join(result["flags"])
        self.assertIn("new skill: skills/two", flags)
        self.assertIn("code or harness config: scripts/run", flags)
        self.assertIn("license or notice changed: LICENSE", flags)
        self.assertFalse(any("evals" in c for c in result["changes"]))
        self.assertFalse((self.root / "skills/kit").exists())


class RepositoryPinTests(unittest.TestCase):
    def test_every_vendored_copy_matches_its_pin_and_license(self):
        for source_id, source in v.vendored_sources().items():
            dest = v.ROOT / source["path"]
            fields = v.installed(dest)
            self.assertEqual(fields.get("ref"), source["ref"], source_id)
            license_file = dest / source["vendor"]["keep"][0]
            self.assertEqual(hashlib.sha256(license_file.read_bytes()).hexdigest(), source["vendor"]["license_sha256"], source_id)
            for name in source["vendor"]["required"]:
                self.assertTrue((dest / name).is_file(), f"{source_id}: {name}")

    def test_toolkit_entry_skill_shadows_its_subskills(self):
        for toolkit in solve_catalog.TOOLKITS:
            meta = solve_catalog.frontmatter(v.ROOT / "skills" / toolkit / "SKILL.md")
            self.assertEqual(meta["name"], toolkit)
            self.assertTrue(meta["description"])

    def test_catalog_names_every_subskill_and_is_current(self):
        text = (v.ROOT / solve_catalog.TARGET).read_text()
        self.assertEqual(text, solve_catalog.build(), "run bin/build-plugin --tree")
        for skill in (v.ROOT / "skills").glob("*/skills/*/SKILL.md"):
            self.assertIn(f"`{solve_catalog.frontmatter(skill)['name']}`", text, skill)
        for command in json.loads((v.ROOT / "skills/cdpi/data/routes.json").read_text())["commands"]:
            self.assertIn(f"`{command}`", text)
        for page in solve_catalog.CDPI_AI_SKILLS:
            self.assertIn(page, text)
        self.assertLess(len(text.encode()), 20_000, "the always-loaded router must stay small")


if __name__ == "__main__":
    unittest.main()
