#!/usr/bin/env python3
"""Combine this fork's Vale rules with the installed STE writing review engine."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def engine() -> Path:
    candidates = [Path(value).expanduser() for name in ("STE_WRITING_ROOT", "CLAUDE_PLUGIN_ROOT")
                  if (value := os.environ.get(name))]
    candidates += [Path.home() / client / "skills/ste-writing" for client in (".claude", ".agents", ".codex")]
    for candidate in candidates:
        if (candidate / "scripts/writing_check.py").is_file() and (candidate / "scripts/style_book.py").is_file():
            return candidate.resolve()
    raise ValueError("Install ste-writing for the optional review bridge, or set STE_WRITING_ROOT. Direct Vale and Harper checks remain available.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--profile", choices=("description", "procedure", "safety"), default="description")
    parser.add_argument("--original", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    remote = parser.add_mutually_exclusive_group()
    remote.add_argument("--jev", action="store_true", help="Request hosted Jev and configured local book context")
    remote.add_argument("--no-jev", action="store_true", help="Keep all checks local")
    parser.add_argument("--no-book", action="store_true")
    parser.add_argument("--strict-exit", action="store_true")
    args = parser.parse_args()
    try:
        command = [sys.executable, str(engine() / "scripts/writing_check.py"), "--base",
                   "--config", str(ROOT / "vale" / (args.profile + ".ini")),
                   "--profile", args.profile, "--format", args.format]
        if args.original:
            command.extend(["--original", str(args.original)])
        for name in ("jev", "no_jev", "no_book", "strict_exit"):
            if getattr(args, name):
                command.append("--" + name.replace("_", "-"))
        command.extend(args.paths)
        return subprocess.run(command, check=False).returncode
    except (OSError, ValueError) as error:
        print(f"Writing review did not complete: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
