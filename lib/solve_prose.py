"""Lint decision prose with simplify-writing's Vale and Harper rules.

Run it before the text is hashed. Claim statements enter every gate's input
digest, and the recommendation and next action enter the refutation digest, so
rewording them after those receipts exist requires the checks to run again.
The lint is advisory: it reports findings and never edits the run.
"""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from solve_contract import ContractError, read_object, require, write_json

SIMPLIFY_WRITING_ENV = "SOLVE_SIMPLIFY_WRITING"
# The built-in copy of simplify-writing. An installed standalone copy is the fallback.
BUILT_IN = Path(__file__).resolve().parents[1] / "write"
# Pinned third-party Vale packages that `vale sync` downloads once.
SYNCED_STYLE = Path("vale/styles/Google")
SKILL_DIRS = (Path.home() / ".claude/skills/simplify-writing", Path.home() / ".agents/skills/simplify-writing")
PLUGIN_CACHE = Path.home() / ".claude/plugins/cache/simplify-writing"
LINT_TIMEOUT_SECONDS = 120
# Vale and harper-cli both exit 1 when they find something; that is not a failure.
FINDINGS_EXIT = 1
PROFILES = ("description", "procedure")
SCOPES = ("claims", "decision", "all")


def locate_simplify_writing():
    explicit = os.environ.get(SIMPLIFY_WRITING_ENV)
    candidates = [Path(explicit).expanduser()] if explicit else [BUILT_IN, *SKILL_DIRS, *sorted(PLUGIN_CACHE.glob("*/*"), reverse=True)]
    for skill in candidates:
        if (skill / "vale/description.ini").is_file():
            return skill
    if explicit:
        raise ContractError(f"{SIMPLIFY_WRITING_ENV}={explicit} has no vale/description.ini")
    raise ContractError("simplify-writing is not installed. Clone https://github.com/bajpainaman/simplify-writing "
                        f"into ~/.claude/skills/simplify-writing, or set {SIMPLIFY_WRITING_ENV}")


def extract(run, scope):
    """Return (markdown, labels) where labels maps a line number to the field it holds."""
    run = Path(run)
    # No headings: they would draw heading-style findings about field names, not prose.
    lines, labels = [], {}

    def add(label, text):
        if not isinstance(text, str) or not text.strip():
            return
        for row in text.strip().splitlines():
            lines.append(row)
            labels[len(lines)] = label
        lines.append("")

    if scope in ("decision", "all"):
        state = read_object(run / "state.json")
        add("recommendation", state.get("recommendation"))
        add("next_action", state.get("next_action"))
        tldr = state.get("tldr", [])
        for index, line in enumerate([tldr] if isinstance(tldr, str) else tldr, 1):
            add(f"tldr {index}", line)
    if scope in ("claims", "all"):
        claims_path = run / "claims.json"
        require(claims_path.is_file(), "write claims.json before checking claim prose")
        claims = json.loads(claims_path.read_text())
        require(isinstance(claims, list), "claims.json must be a list")
        for claim in claims:
            cid = claim.get("id", "?") if isinstance(claim, dict) else "?"
            if isinstance(claim, dict):
                add(f"claim {cid} statement", claim.get("statement"))
                add(f"claim {cid} assumptions", claim.get("assumptions"))
                add(f"claim {cid} followup", claim.get("followup"))
    return "\n".join(lines) + "\n", labels


def _run(command):
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=LINT_TIMEOUT_SECONDS, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ContractError(f"{command[0]} exceeded {LINT_TIMEOUT_SECONDS}s") from exc
    require(done.returncode in (0, FINDINGS_EXIT), f"{command[0]} failed (exit {done.returncode}): {done.stderr.strip()}")
    return done.stdout


def ensure_synced(skill, profile):
    """Download the pinned Vale packages once, as the write mode's step 0 says."""
    if (skill / SYNCED_STYLE).is_dir():
        return
    print(f"prose-check: syncing pinned Vale packages into {skill / 'vale/styles'}", file=sys.stderr)
    done = subprocess.run(["vale", "--no-global", f"--config={profile}.ini", "sync"], cwd=skill / "vale",
                          capture_output=True, text=True, timeout=LINT_TIMEOUT_SECONDS, check=False)
    require(done.returncode == 0, f"vale sync failed (exit {done.returncode}): {done.stderr.strip()}")


def prose_text(path):
    """Harper reads HTML as plain text, so give it the visible prose only."""
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix.lower() not in (".html", ".htm"):
        return None
    text = re.sub(r"(?is)<(script|style|pre|code)\b.*?</\1>", " ", text)
    return re.sub(r"[ \t]+", " ", re.sub(r"<[^>]+>", " ", text))


def lint(path, skill, profile, labels=None):
    labels = labels or {}
    result = {"file": str(path), "profile": profile, "findings": [], "skipped": []}
    if shutil.which("vale"):
        ensure_synced(skill, profile)
        raw = _run(["vale", "--no-global", f"--config={skill / 'vale' / (profile + '.ini')}", "--output=JSON", str(path)])
        for alerts in (json.loads(raw) if raw.strip() else {}).values():
            for alert in alerts:
                result["findings"].append({"tool": "vale", "check": alert["Check"], "severity": alert["Severity"],
                                           "line": alert["Line"],
                                           # Readability scores the whole file, so it has no field.
                                           "field": None if alert["Check"].startswith("Readability.") else labels.get(alert["Line"]),
                                           "match": alert.get("Match", ""), "message": alert["Message"]})
    else:
        result["skipped"].append("vale is not installed (brew install vale)")
    if shutil.which("harper-cli"):
        ignore = (skill / "harper/ignore.txt").read_text().strip() if (skill / "harper/ignore.txt").is_file() else ""
        visible = prose_text(path)
        with tempfile.TemporaryDirectory(prefix="solve-prose-") as scratch:
            target = path
            if visible is not None:
                target = Path(scratch) / (Path(path).stem + ".txt")
                target.write_text(visible, encoding="utf-8")
            raw = _run(["harper-cli", "lint", "--no-color", "--format", "compact", *(["--ignore", ignore] if ignore else []), str(target)])
        for row in raw.splitlines():
            if row.strip():
                result["findings"].append({"tool": "harper", "severity": "warning", "message": row.strip()})
    else:
        result["skipped"].append("harper-cli is not installed (brew install harper)")
    counts = {}
    for finding in result["findings"]:
        counts[finding["severity"]] = counts.get(finding["severity"], 0) + 1
    result["counts"] = counts
    return result


def _print(result, label):
    for finding in result["findings"]:
        where = f"[{finding['field']}] " if finding.get("field") else ""
        line = f"line {finding['line']}: " if "line" in finding and not finding.get("field") else ""
        print(f"{finding['severity']:>10}  {finding['tool']}  {where}{line}{finding.get('check', '')} {finding['message']}".rstrip())
    for reason in result["skipped"]:
        print(f"SKIPPED: {reason}", file=sys.stderr)
    print(f"prose-check {label}: {sum(result['counts'].values())} finding(s) {result['counts']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run-dir")
    parser.add_argument("--file", help="lint any Markdown, text or HTML file and print findings (no run needed)")
    parser.add_argument("--scope", choices=SCOPES, default="all",
                        help="claims before gate inspection; decision before the refuter reveal")
    parser.add_argument("--report", help="lint a rendered report instead (advisory only; edits need a new review)")
    parser.add_argument("--profile", choices=PROFILES, default="description")
    args = parser.parse_args(argv)
    try:
        require(bool(args.run_dir) != bool(args.file), "pass exactly one of --run-dir or --file")
        if args.file:
            target = Path(args.file)
            require(target.is_file(), f"no such file: {args.file}")
            result = lint(target.resolve(), locate_simplify_writing(), args.profile)
            _print(result, args.file)
            return 0
        run = Path(args.run_dir)
        require(run.is_dir(), "pass an existing --run-dir")
        skill = locate_simplify_writing()
        out_dir = run / "prose"
        out_dir.mkdir(exist_ok=True)
        if args.report:
            report = Path(args.report)
            require(report.is_file() and report.suffix == ".md", "--report must be a rendered Markdown report")
            result = lint(report.resolve(), skill, args.profile)
            name = "report"
        else:
            text, labels = extract(run, args.scope)
            source = out_dir / f"{args.scope}.md"
            source.write_text(text, encoding="utf-8")
            result = lint(source.resolve(), skill, args.profile, labels)
            name = args.scope
        write_json(out_dir / f"{name}-lint.json", result)
        _print(result, f"{name} -> {out_dir / (name + '-lint.json')}")
        return 0
    except (ContractError, OSError, ValueError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
