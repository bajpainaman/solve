"""Fetch html-artifact into $SOLVE_ROOT/html as solve's built-in HTML mode.

html-artifact has no license file, so this public MIT repository must not
redistribute it. The sync runs on the user's machine at a pinned commit, and
.gitignore keeps the fetched copy out of every commit.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from solve_contract import ContractError, require

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "html"
# Pinned in sources.json so a change upstream reaches solve only through a deliberate bump.
_PIN = next(s for s in json.loads((ROOT / "sources.json").read_text())["sources"] if s["id"] == "html-artifact")
REPO, REF = _PIN["repo"], _PIN["ref"]
SKILL_PATH = Path("plugins/html-artifact/skills/html-artifact")
REQUIRED = ("SKILL.md", "scripts/build.mjs", "scripts/verify.mjs", "references/components.md")
GIT_TIMEOUT_SECONDS = 180
HEADER = """<!-- Built-in HTML mode of solve, fetched by bin/html-sync from
     {repo} at {ref}.
     The upstream repository has no license file. Do not commit or redistribute this directory.
     `<skill-dir>` below means `$SOLVE_ROOT/html`, the directory that holds this file. -->
"""


def _git(*args, cwd=None):
    try:
        done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                              timeout=GIT_TIMEOUT_SECONDS, check=False)
    except FileNotFoundError as exc:
        raise ContractError("bin/html-sync needs git on PATH") from exc
    except subprocess.TimeoutExpired as exc:
        raise ContractError(f"git {args[0]} exceeded {GIT_TIMEOUT_SECONDS}s") from exc
    require(done.returncode == 0, f"git {' '.join(args[:2])} failed (exit {done.returncode}): {done.stderr.strip()}")
    return done.stdout.strip()


def _strip_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:].lstrip("\n")
    return text


def installed_ref(dest=DEST):
    source = dest / "SOURCE"
    if not source.is_file():
        return None
    fields = dict(line.split("=", 1) for line in source.read_text().splitlines() if "=" in line)
    return fields.get("ref")


def sync(repo=REPO, ref=REF, dest=DEST, force=False):
    """Install html-artifact at ref into dest. Keep the old copy if any step fails."""
    dest = Path(dest)
    if not force and installed_ref(dest) == ref and (dest / "HTML.md").is_file():
        return {"status": "current", "ref": ref, "path": str(dest)}
    with tempfile.TemporaryDirectory(prefix="solve-html-sync-") as scratch:
        clone = Path(scratch) / "src"
        _git("clone", "--quiet", "--no-checkout", repo, str(clone))
        _git("checkout", "--quiet", ref, cwd=clone)
        resolved = _git("rev-parse", "HEAD", cwd=clone)
        skill = clone / SKILL_PATH
        missing = [name for name in REQUIRED if not (skill / name).is_file()]
        require(not missing, f"{repo} at {ref} has no {', '.join(missing)} under {SKILL_PATH}")
        stage = dest.with_name(dest.name + ".new")
        shutil.rmtree(stage, ignore_errors=True)
        shutil.copytree(skill, stage)
        guide = stage / "SKILL.md"
        (stage / "HTML.md").write_text(HEADER.format(repo=repo, ref=resolved) + _strip_frontmatter(guide.read_text()))
        guide.unlink()
        (stage / "SOURCE").write_text(f"repo={repo}\nref={resolved}\nsynced_at={int(time.time())}\n"
                                      "license=none (upstream has no license file; never commit this directory)\n")
    old = dest.with_name(dest.name + ".old")
    shutil.rmtree(old, ignore_errors=True)
    if dest.exists():
        dest.rename(old)
    stage.rename(dest)
    shutil.rmtree(old, ignore_errors=True)
    return {"status": "synced", "ref": resolved, "path": str(dest)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=os.environ.get("SOLVE_HTML_ARTIFACT_REPO", REPO))
    parser.add_argument("--ref", default=os.environ.get("SOLVE_HTML_ARTIFACT_REF", REF))
    parser.add_argument("--force", action="store_true", help="fetch again even when the pinned ref is installed")
    args = parser.parse_args(argv)
    try:
        result = sync(args.repo, args.ref, force=args.force)
        print(f"html-sync: {result['status']} {result['ref'][:12]} -> {result['path']}")
        return 0
    except (ContractError, OSError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
