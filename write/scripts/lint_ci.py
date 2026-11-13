#!/usr/bin/env python3
"""Lint changed maintained prose, or all maintained prose for a manual run."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSE = {".md", ".txt", ".rst", ".adoc", ".html"}


def main() -> int:
    base = os.environ.get("STE_BASE_SHA", "")
    command = ["git", "diff", "--name-only", "--diff-filter=ACMR", "-z", base, "HEAD"] if (
        re.fullmatch(r"[0-9a-fA-F]{40,64}", base) and set(base) != {"0"}
    ) else ["git", "ls-files", "-z"]
    result = subprocess.run(command, capture_output=True, check=True, cwd=ROOT)
    files = []
    for name in result.stdout.split(b"\0"):
        if not name:
            continue
        path = Path(os.fsdecode(name))
        # These fixtures intentionally demonstrate linter findings. Vocabulary
        # lists and Harper's rule configuration are machine data.
        if path.parts[:2] == ("vale", "examples") or str(path) == "harper/ignore.txt":
            continue
        if any(path.parts[i:i + 3] == ("styles", "config", "vocabularies") for i in range(len(path.parts) - 2)):
            continue
        if path.suffix.lower() in PROSE and (ROOT / path).is_file():
            files.append(str(ROOT / path))
    if not files:
        print("English lint: no changed maintained prose.")
        return 0
    print(f"English lint: {len(files)} maintained prose files.", flush=True)
    return subprocess.run([sys.executable, str(ROOT / "scripts/review.py"), "--no-jev", "--strict-exit",
                           "--profile", os.environ.get("STE_VALE_PROFILE", "description"), *files], cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
