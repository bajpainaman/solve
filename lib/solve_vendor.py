"""Copy a licensed upstream skill into $SOLVE_ROOT/skills/<id> at the commit pinned in sources.json.

Every `vendored` source with a `vendor` block in sources.json uses this script. A sync never follows
a branch. It checks out the pinned commit, refuses a license whose hash differs from the pin, refuses
symlinks, drops eval fixtures and harness hooks, and records the ref and license hash in SOURCE.
`--review REF` compares the pin with a newer commit and changes nothing, so a person reads the diff
of instructions, scripts and license before bumping the pin.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from solve_bundle import _git
from solve_contract import ContractError, require

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXCLUDE = ("evals", ".claude-plugin", ".codex-plugin", "hooks")
# Upstream files that can run code or change an agent's behaviour without being read first.
RISKY_NAMES = ("hooks.json", "mcp.json", ".mcp.json", "plugin.json", "settings.json")


def vendored_sources(root=ROOT):
    sources = json.loads((Path(root) / "sources.json").read_text())["sources"]
    return {s["id"]: s for s in sources if s.get("mode") == "vendored" and "vendor" in s}


def installed(dest):
    source = Path(dest) / "SOURCE"
    if not source.is_file():
        return {}
    return dict(l.split("=", 1) for l in source.read_text().splitlines() if "=" in l)


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _excluded(relative, exclude):
    return relative.parts[0] in exclude


def _checkout(repo, ref, scratch):
    clone = Path(scratch) / "src"
    _git("clone", "--quiet", "--no-checkout", "--filter=blob:none", repo, str(clone))
    _git("checkout", "--quiet", ref, cwd=clone)
    return clone, _git("rev-parse", "HEAD", cwd=clone)


def sync(source, root=ROOT, force=False):
    """Install source at its pinned ref. Keep the old copy if any check fails."""
    spec = source["vendor"]
    dest = Path(root) / source["path"]
    if not force and installed(dest).get("ref") == source["ref"] and (dest / "SKILL.md").is_file():
        return {"status": "current", "ref": source["ref"], "path": str(dest)}
    exclude = tuple(spec.get("exclude", DEFAULT_EXCLUDE))
    with tempfile.TemporaryDirectory(prefix=f"solve-vendor-{source['id']}-") as scratch:
        clone, resolved = _checkout(source["repo"], source["ref"], scratch)
        require(resolved == source["ref"], f"{source['id']}: {source['ref']} resolved to {resolved}")
        tree = clone / spec["from"]
        missing = [n for n in spec["required"] if not (tree / n).is_file()] + \
                  [n for n in spec["keep"] if not (clone / n).is_file()]
        require(not missing, f"{source['repo']} at {resolved} lacks {', '.join(missing)}")
        license_hash = _sha256(clone / spec["keep"][0])
        require(license_hash == spec["license_sha256"],
                f"{source['id']}: {spec['keep'][0]} changed upstream (sha256 {license_hash}). Read the new terms, "
                "then set license and license_sha256 in sources.json")
        stage = dest.with_name(dest.name + ".new")
        shutil.rmtree(stage, ignore_errors=True)
        for path in sorted(tree.rglob("*")):
            relative = path.relative_to(tree)
            if _excluded(relative, exclude):
                continue
            require(not path.is_symlink(), f"{source['id']}: symlink {relative} is not vendored")
            if path.is_file():
                (stage / relative).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, stage / relative)
        for name in spec["keep"]:
            shutil.copy2(clone / name, stage / name)
        wrapper = spec.get("wrapper")
        if wrapper:
            # Our entry SKILL.md shadows the upstream skills below it, so an installer sees one skill.
            for path in sorted((Path(root) / wrapper).rglob("*")):
                if path.is_file():
                    target = stage / path.relative_to(Path(root) / wrapper)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, target)
        require((stage / "SKILL.md").is_file(), f"{source['id']}: no SKILL.md at the vendored root")
        (stage / "SOURCE").write_text(f"repo={source['repo']}\nref={resolved}\nsynced_at={int(time.time())}\n"
                                      f"license={spec['license']}\nlicense_sha256={license_hash}\n")
    shutil.rmtree(dest, ignore_errors=True)
    stage.rename(dest)
    return {"status": "synced", "ref": resolved, "path": str(dest)}


def review(source, new_ref):
    """Summarize what a pin bump would change. Read-only."""
    spec = source["vendor"]
    exclude = tuple(spec.get("exclude", DEFAULT_EXCLUDE))
    with tempfile.TemporaryDirectory(prefix=f"solve-review-{source['id']}-") as scratch:
        clone, resolved = _checkout(source["repo"], new_ref, scratch)
        _git("fetch", "--quiet", "origin", source["ref"], cwd=clone)
        raw = _git("diff", "--name-status", "--no-renames", source["ref"], resolved, "--", spec["from"], *spec["keep"], cwd=clone)
        modes = _git("diff", "--raw", "--no-renames", source["ref"], resolved, "--", spec["from"], cwd=clone)
    changes, flags = [], []
    for line in raw.splitlines():
        status, name = line.split("\t", 1)
        relative = Path(name).relative_to(spec["from"]) if name.startswith(spec["from"] + "/") else Path(name)
        if _excluded(relative, exclude):
            continue
        changes.append(f"{status} {relative}")
        if name in spec["keep"]:
            flags.append(f"license or notice changed: {name}. Read it before the bump")
        if relative.name == "SKILL.md" and status == "A":
            flags.append(f"new skill: {relative.parent}")
        if relative.name in RISKY_NAMES or relative.parts[0] in ("scripts", "hooks", "bin"):
            flags.append(f"code or harness config: {relative}")
    for line in modes.splitlines():
        meta, name = line.split("\t", 1)
        if meta.split()[1].endswith("755") and not meta.split()[0].endswith("755"):
            flags.append(f"newly executable: {name}")
    return {"id": source["id"], "from": source["ref"], "to": resolved, "changes": changes, "flags": sorted(set(flags))}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("id", nargs="?", help="source id from sources.json; omit with --all")
    parser.add_argument("--all", action="store_true", help="sync every vendored source")
    parser.add_argument("--force", action="store_true", help="fetch again even when the pinned ref is installed")
    parser.add_argument("--review", metavar="REF", help="show what bumping the pin to REF would change; writes nothing")
    args = parser.parse_args(argv)
    sources = vendored_sources()
    try:
        require(args.all != bool(args.id), "name one source id or pass --all")
        require(not (args.all and args.review), "--review takes one source id")
        chosen = list(sources) if args.all else [args.id]
        for source_id in chosen:
            require(source_id in sources, f"unknown vendored source {source_id}; known: {', '.join(sources)}")
            if args.review:
                result = review(sources[source_id], args.review)
                print(f"review {result['id']}: {result['from'][:12]} -> {result['to'][:12]}, {len(result['changes'])} files")
                for flag in result["flags"]:
                    print(f"  FLAG {flag}")
                for change in result["changes"]:
                    print(f"  {change}")
                print("Read the flagged files and every changed SKILL.md before you set the new ref in sources.json.")
                continue
            result = sync(sources[source_id], force=args.force)
            print(f"vendor-sync {source_id}: {result['status']} {result['ref'][:12]} -> {result['path']}")
        return 0
    except (ContractError, OSError, subprocess.SubprocessError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
