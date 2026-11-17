"""Fetch impeccable's skill into $SOLVE_ROOT/skills/impeccable at the commit pinned in sources.json.

impeccable is Apache-2.0. The copy keeps its LICENSE and NOTICE.md and is committed, so
`npx skills add bajpainaman/solve` installs it. Change it only by bumping the pin and syncing.
"""

import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time

from solve_bundle import _git
from solve_contract import ContractError, require

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "skills/impeccable"
SKILL_PATH = Path("plugin/skills/impeccable")
KEEP = ("LICENSE", "NOTICE.md")
REQUIRED = ("SKILL.md", "scripts/impeccable", "reference/craft-floor.md")


def pin(source_id="impeccable"):
    return next(s for s in json.loads((ROOT / "sources.json").read_text())["sources"] if s["id"] == source_id)


def installed_ref(dest=DEST):
    source = Path(dest) / "SOURCE"
    if not source.is_file():
        return None
    return dict(l.split("=", 1) for l in source.read_text().splitlines() if "=" in l).get("ref")


def sync(repo, ref, dest=DEST, force=False):
    dest = Path(dest)
    if not force and installed_ref(dest) == ref and (dest / "SKILL.md").is_file():
        return {"status": "current", "ref": ref, "path": str(dest)}
    with tempfile.TemporaryDirectory(prefix="solve-impeccable-sync-") as scratch:
        clone = Path(scratch) / "src"
        _git("clone", "--quiet", "--no-checkout", "--filter=blob:none", repo, str(clone))
        _git("checkout", "--quiet", ref, cwd=clone)
        resolved = _git("rev-parse", "HEAD", cwd=clone)
        skill = clone / SKILL_PATH
        missing = [n for n in REQUIRED if not (skill / n).is_file()] + [n for n in KEEP if not (clone / n).is_file()]
        require(not missing, f"{repo} at {ref} lacks {', '.join(missing)}")
        stage = dest.with_name(dest.name + ".new")
        shutil.rmtree(stage, ignore_errors=True)
        shutil.copytree(skill, stage, symlinks=False)
        for name in KEEP:
            shutil.copy2(clone / name, stage / name)
        (stage / "SOURCE").write_text(f"repo={repo}\nref={resolved}\nsynced_at={int(time.time())}\nlicense=Apache-2.0\n")
    shutil.rmtree(dest, ignore_errors=True)
    stage.rename(dest)
    return {"status": "synced", "ref": resolved, "path": str(dest)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="fetch again even when the pinned ref is installed")
    args = parser.parse_args(argv)
    source = pin()
    try:
        result = sync(source["repo"], source["ref"], force=args.force)
        print(f"impeccable-sync: {result['status']} {result['ref'][:12]} -> {result['path']}")
        return 0
    except (ContractError, OSError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
