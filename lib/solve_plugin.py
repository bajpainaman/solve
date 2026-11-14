"""Build a reproducible skills-only plugin from Solve's licensed source files."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ("benchmarks", "frameworks", "gates", "references", "templates", "write")
COMMANDS = ("artifact", "benchmark", "budget-track", "calibration", "cost-track",
            "gates", "progress", "prose-check", "render-report", "state-rw", "templates", "tier")
MODULES = ("solve_benchmark.py", "solve_contract.py", "solve_html.py", "solve_output.py",
           "solve_portable.py", "solve_prose.py", "solve_templates.py")
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
FORBIDDEN_PARTS = {".git", ".env", "__pycache__", "node_modules", "private", ".DS_Store"}


class PackageError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise PackageError(message)


def read_file(path):
    require(not path.is_symlink(), f"symlinks are not package inputs: {path}")
    require(path.is_file(), f"missing package input: {path}")
    require(not (FORBIDDEN_PARTS & set(path.parts)), f"private or generated package input: {path}")
    return path.read_bytes()


def git_output(root, *args):
    done = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                          check=False, timeout=15)
    require(done.returncode == 0, "build inside the Solve Git checkout")
    return done.stdout


def collect(root=ROOT):
    root = Path(root).resolve()
    manifest = json.loads(read_file(root / "plugin/plugin.json"))
    entries = {"plugin.json": read_file(root / "plugin/plugin.json"),
               "LICENSE": read_file(root / "LICENSE")}
    skill = "skills/solve/"
    tracked = git_output(root, "ls-files", "-z").decode().split("\0")
    for relative in tracked:
        if relative and PurePosixPath(relative).parts[0] in DIRECTORIES:
            entries[skill + relative] = read_file(root / relative)
    for relative in ["LICENSE", "VERSION", "sources.json", *["bin/" + n for n in COMMANDS],
                     *["lib/" + n for n in MODULES]]:
        entries[skill + relative] = read_file(root / relative)
    # Preserve the original licensed writing guide separately from the portable adaptation.
    entries[skill + "write/UPSTREAM.md"] = read_file(root / "write/WRITE.md")
    override_root = root / "plugin/overrides"
    for path in sorted(override_root.rglob("*")):
        require(not path.is_symlink(), f"symlink in plugin overrides: {path}")
        if path.is_file():
            entries[skill + path.relative_to(override_root).as_posix()] = read_file(path)
    lock = {
        "repository": manifest["repository"],
        "source_commit": git_output(root, "rev-parse", "HEAD").decode().strip(),
        "source_dirty": bool(git_output(root, "status", "--porcelain", "--untracked-files=normal").strip()),
        "runtime_version": entries[skill + "VERSION"].decode().strip(),
        "plugin_version": manifest["version"],
        "excluded_dependency": "html-artifact; no upstream license, never redistributed",
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(entries.items())},
    }
    entries["SOURCE.json"] = (json.dumps(lock, indent=2, sort_keys=True) + "\n").encode()
    return entries


def validate(entries):
    try:
        import yaml
    except ImportError as exc:
        raise PackageError("package validation needs PyYAML in the build environment") from exc
    for name, value in entries.items():
        path = PurePosixPath(name)
        require(not path.is_absolute() and ".." not in path.parts, f"unsafe archive path: {name}")
        require(not (FORBIDDEN_PARTS & set(path.parts)), f"forbidden archive path: {name}")
        require(not name.startswith("skills/solve/html/"), "html-artifact must not be redistributed")
        require(isinstance(value, bytes), f"non-byte archive value: {name}")
    manifest = json.loads(entries["plugin.json"])
    require(manifest.get("$schema") == SCHEMA, "portable plugin schema is required")
    require(manifest.get("name") == "solve", "package name must be solve")
    require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest.get("version", "")), "invalid version")
    require(not any(k in manifest for k in ("skills", "mcpServers", "apps", "interface")), "legacy top-level manifest keys")
    interface = manifest["extensions"]["com.openai"]["interface"]
    require(0 < len(interface["shortDescription"]) <= 30, "subtitle must be 1-30 characters")
    require(interface["category"] == "Productivity", "unexpected listing category")
    require(isinstance(interface["capabilities"], list), "capabilities must be an array")
    prompts = interface["defaultPrompt"]
    require(isinstance(prompts, list) and 1 <= len(prompts) <= 3, "need 1-3 listing prompts")
    require(all(isinstance(p, str) and 0 < len(p) <= 128 and "\n" not in p for p in prompts), "invalid listing prompt")
    skill_path = "skills/solve/SKILL.md"
    skill = entries[skill_path].decode("utf-8")
    require(skill.startswith("---\n") and "\n---\n" in skill[4:], "missing skill frontmatter")
    frontmatter = yaml.safe_load(skill.split("\n---\n", 1)[0][4:])
    require(isinstance(frontmatter, dict) and frontmatter.get("name") == "solve", "invalid skill name")
    require(isinstance(frontmatter.get("description"), str) and frontmatter["description"].strip(), "missing skill description")
    require(len(entries[skill_path]) < 1024 * 1024, "skill too large")
    agent = yaml.safe_load(entries["skills/solve/agents/openai.yaml"])
    require(agent["interface"]["display_name"] and agent["interface"]["short_description"], "invalid agent interface")
    require(type(agent.get("policy", {}).get("allow_implicit_invocation")) is bool, "invalid invocation policy")
    for name in ("LICENSE", "skills/solve/write/LICENSE", "skills/solve/templates/html-effectiveness/LICENSE",
                 "skills/solve/templates/html-effectiveness/NOTICE.md", "skills/solve/references/decision.md",
                 "skills/solve/references/artifacts.md", "skills/solve/references/writing.md"):
        require(name in entries and entries[name].strip(), f"missing component: {name}")
    catalog = json.loads(entries["skills/solve/gates/catalog.json"])
    require(len(catalog["gates"]) == 28, "do not weaken the 28-gate contract while packaging")
    require({g["id"] for g in catalog["gates"] if g["kind"] == "required"} ==
            {"evidence", "refutation", "consumer"}, "required reviews changed")
    templates = json.loads(entries["skills/solve/templates/catalog.json"])
    for item in templates["templates"]:
        if item["file"]:
            require("skills/solve/templates/" + item["file"] in entries, f"missing exemplar: {item['file']}")
    source = json.loads(entries["SOURCE.json"])
    require(set(source["files"]) == set(entries) - {"SOURCE.json"}, "incomplete source index")
    for name, digest in source["files"].items():
        require(hashlib.sha256(entries[name]).hexdigest() == digest, f"source index mismatch: {name}")
    # Check all local links in authored portable instructions, excluding quoted upstream examples.
    instructions = [n for n in entries if n in (skill_path, "skills/solve/write/WRITE.md") or
                    n.startswith("skills/solve/references/") and n.split("/")[-1] in
                    {"decision.md", "operating-rules.md", "artifacts.md", "writing.md", "router.md", "output.md"}]
    import posixpath
    for name in instructions:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", entries[name].decode()):
            if ":" in target or target.startswith("#"):
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target.split("#")[0]))
            require(resolved in entries, f"broken instruction link in {name}: {target}")
    return {"name": manifest["name"], "version": manifest["version"], "files": len(entries),
            "skills": ["solve"], "gates": len(catalog["gates"]), "templates": len(templates["templates"]),
            "entry_words": len(skill.split()), "entry_bytes": len(entries[skill_path]),
            "source_commit": source["source_commit"], "source_dirty": source["source_dirty"]}


def archive_bytes(entries):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, contents in sorted(entries.items()):
            info = zipfile.ZipInfo("solve/" + name, date_time=(2026, 1, 1, 0, 0, 0))
            mode = 0o755 if name.startswith("skills/solve/bin/") else 0o644
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, contents)
    return buf.getvalue()


def inspect_archive(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "duplicate archive entries")
        require(all(n.startswith("solve/") for n in names), "archive must contain exactly one plugin")
        entries = {}
        for info in archive.infolist():
            require(not stat.S_ISLNK(info.external_attr >> 16), "archive contains a symlink")
            entries[info.filename[len("solve/"):]] = archive.read(info)
    return validate(entries)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, help="new .zip path outside the source components")
    args = parser.parse_args(argv)
    try:
        output = Path(args.output).resolve()
        require(output.suffix.lower() == ".zip", "output must be a ZIP file")
        require(not output.exists(), "output exists; choose a new archive path")
        require(ROOT / "plugin" not in output.parents and ROOT / "write" not in output.parents,
                "do not write an archive inside packaged source")
        entries = collect()
        validate(entries)
        data = archive_bytes(entries)
        summary = inspect_archive(data)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(data)
        print(json.dumps({**summary, "archive": str(output), "archive_bytes": len(data),
                          "sha256": hashlib.sha256(data).hexdigest()}, indent=2))
        return 0
    except (PackageError, OSError, KeyError, ValueError, subprocess.SubprocessError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
