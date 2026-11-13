"""Check solve and its pinned sources for upstream updates. Report only; never apply.

The result is cached for a day so a session-start check costs one cache read.
A failed lookup is reported as unknown, never as current.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from solve_contract import ContractError, require

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources.json"
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "solve/updates.json"
CACHE_TTL_SECONDS = 24 * 60 * 60
GIT_TIMEOUT_SECONDS = 20
MODES = ("self", "fetched", "vendored")
DISABLE_ENV = "SOLVE_NO_UPDATE_CHECK"


def load_sources(path=SOURCES):
    data = json.loads(Path(path).read_text())
    require(data.get("schema_version") == 1, "unsupported sources.json")
    for source in data["sources"]:
        require(source.get("mode") in MODES, f"{source.get('id')}: unknown mode")
        require(source["mode"] == "self" or len(source.get("ref", "")) == 40, f"{source['id']}: pin a full 40-character commit")
    return data["sources"]


def pinned_ref(source_id, path=SOURCES):
    return next(s["ref"] for s in load_sources(path) if s["id"] == source_id)


def _git(*args, cwd=None):
    try:
        done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                              timeout=GIT_TIMEOUT_SECONDS, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return (done.stdout.strip(), None) if done.returncode == 0 else (None, done.stderr.strip() or f"exit {done.returncode}")


def remote_head(repo, branch=None):
    out, error = _git("ls-remote", repo, f"refs/heads/{branch}" if branch else "HEAD")
    if error or not out:
        return None, error or "no such branch"
    return out.split()[0], None


def _compare_url(repo, old, new):
    base = repo.removesuffix(".git")
    return f"{base}/compare/{old[:12]}...{new[:12]}" if base.startswith("https://github.com/") else None


def check_source(source, root=ROOT):
    result = {"id": source["id"], "mode": source["mode"]}
    head, error = remote_head(source["repo"], source.get("branch"))
    if error:
        return {**result, "status": "unknown", "detail": f"could not reach {source['repo']}: {error}"}
    if source["mode"] == "self":
        local, local_error = _git("rev-parse", "HEAD", cwd=root)
        if local_error:
            return {**result, "status": "unknown", "detail": "not a git checkout; rerun the installer to update"}
        if local == head:
            return {**result, "status": "current", "ref": head}
        known, _ = _git("cat-file", "-e", f"{head}^{{commit}}", cwd=root)
        if known is None:
            return {**result, "status": "update", "ref": local, "latest": head,
                    "action": f"git -C {root} pull --ff-only"}
        return {**result, "status": "current", "ref": local, "detail": "local checkout is ahead of or diverged from upstream"}
    pin = source["ref"]
    if source["mode"] == "fetched":
        source_file = root / source["path"] / "SOURCE"
        fields = dict(l.split("=", 1) for l in source_file.read_text().splitlines() if "=" in l) if source_file.is_file() else {}
        if fields.get("ref") != pin:
            result["local"] = f"{source['path']}/ does not match the pin; run bin/html-sync"
    if head == pin:
        return {**result, "status": "current", "ref": pin}
    action = (f"review the diff, set its ref in sources.json, then run bin/html-sync" if source["mode"] == "fetched"
              else f"review the diff, copy the changes into {source['path']}/, then set its ref in sources.json")
    return {**result, "status": "update", "ref": pin, "latest": head, "action": action,
            "compare": _compare_url(source["repo"], pin, head)}


def check(force=False, cache=CACHE, sources_path=SOURCES, root=ROOT, now=None):
    now = time.time() if now is None else now
    if not force and cache.is_file():
        try:
            cached = json.loads(cache.read_text())
            if now - cached["checked_at"] < CACHE_TTL_SECONDS and cached.get("sources_mtime") == sources_path.stat().st_mtime:
                return {**cached, "cached": True}
        except (ValueError, KeyError, TypeError):
            pass  # A corrupt cache is replaced by a fresh check below.
    results = [check_source(s, root) for s in load_sources(sources_path)]
    report = {"checked_at": now, "sources_mtime": sources_path.stat().st_mtime, "results": results}
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(report, indent=2))
    return {**report, "cached": False}


def format_report(report, quiet=False):
    lines = []
    for r in report["results"]:
        if r["status"] == "update":
            lines.append(f"UPDATE   {r['id']}: {r['ref'][:12]} -> {r['latest'][:12]}. {r['action']}"
                         + (f" ({r['compare']})" if r.get("compare") else ""))
        elif r["status"] == "unknown":
            lines.append(f"UNKNOWN  {r['id']}: {r['detail']}")
        elif not quiet:
            lines.append(f"current  {r['id']} {r['ref'][:12]}" + (f" ({r['detail']})" if r.get("detail") else ""))
        if r.get("local"):
            lines.append(f"LOCAL    {r['id']}: {r['local']}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help=f"ignore the {CACHE_TTL_SECONDS // 3600}h cache")
    parser.add_argument("--quiet", action="store_true", help="print only updates, unknowns and local drift")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if os.environ.get(DISABLE_ENV) == "1":
        if not args.quiet:
            print(f"update check disabled by {DISABLE_ENV}=1")
        return 0
    try:
        report = check(force=args.force)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            text = format_report(report, args.quiet)
            if text:
                print(text)
        return 0
    except (ContractError, OSError, ValueError, KeyError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
