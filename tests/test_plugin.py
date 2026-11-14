"""The actual archive must remain self-contained, reproducible, and inspectable."""

import copy
import hashlib
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import solve_plugin as plugin


class PluginPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = plugin.collect()

    def reindex(self, entries):
        lock = json.loads(entries["SOURCE.json"])
        lock["files"] = {n: hashlib.sha256(b).hexdigest() for n, b in entries.items() if n != "SOURCE.json"}
        entries["SOURCE.json"] = json.dumps(lock).encode()
        return entries

    def test_actual_archive_contains_complete_runtime_and_preserved_contract(self):
        archive = plugin.archive_bytes(self.entries)
        result = plugin.inspect_archive(archive)
        self.assertEqual(result["gates"], 28)
        self.assertEqual(result["templates"], 32)
        self.assertEqual(result["skills"], ["solve"])
        self.assertLess(result["entry_words"], 700)
        with zipfile.ZipFile(io.BytesIO(archive)) as opened:
            for executable in ("gates", "artifact", "prose-check", "render-report", "benchmark"):
                info = opened.getinfo("solve/skills/solve/bin/" + executable)
                self.assertTrue((info.external_attr >> 16) & stat.S_IXUSR)
            self.assertIn("solve/skills/solve/benchmarks/cases.jsonl", opened.namelist())
            self.assertFalse(any("/html/" in n or "/.git/" in n or "/.context/" in n for n in opened.namelist()))

    def test_same_source_produces_identical_archive_bytes(self):
        self.assertEqual(plugin.archive_bytes(self.entries), plugin.archive_bytes(self.entries))

    def test_source_hash_index_detects_tampering(self):
        entries = dict(self.entries)
        entries["skills/solve/lib/solve_contract.py"] += b"\n# tamper\n"
        with self.assertRaisesRegex(plugin.PackageError, "source index mismatch"):
            plugin.validate(entries)

    def test_instruction_links_and_licenses_are_required(self):
        for name in ("skills/solve/references/decision.md", "skills/solve/write/LICENSE"):
            entries = dict(self.entries)
            del entries[name]
            with self.subTest(name=name), self.assertRaisesRegex(plugin.PackageError, "missing component"):
                plugin.validate(self.reindex(entries))

    def test_manifest_and_skill_yaml_are_parsed(self):
        entries = dict(self.entries)
        entries["skills/solve/agents/openai.yaml"] = b'interface:\n  display_name: Solve\n  short_description: Solve\npolicy:\n  allow_implicit_invocation: "false"\n'
        with self.assertRaisesRegex(plugin.PackageError, "invocation policy"):
            plugin.validate(self.reindex(entries))

    def test_rejects_unlicensed_or_escaping_archive_entries(self):
        for name in ("skills/solve/html/HTML.md", "../escape.txt", "/absolute", "skills/solve/.env"):
            entries = dict(self.entries)
            entries[name] = b"not allowed"
            with self.subTest(name=name), self.assertRaises(plugin.PackageError):
                plugin.validate(self.reindex(entries))

    def test_duplicate_entries_cannot_hide_another_component(self):
        buffer = io.BytesIO()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(buffer, "w") as archive:
                archive.writestr("solve/plugin.json", b"{}")
                archive.writestr("solve/plugin.json", b"{}")
        with self.assertRaisesRegex(plugin.PackageError, "duplicate"):
            plugin.inspect_archive(buffer.getvalue())

    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory(prefix="solve-package-test-") as scratch:
            target = Path(scratch) / "real.txt"
            target.write_text("private")
            alias = Path(scratch) / "alias.txt"
            alias.symlink_to(target)
            with self.assertRaisesRegex(plugin.PackageError, "symlink"):
                plugin.read_file(alias)


if __name__ == "__main__":
    unittest.main()
