"""cdpi: route, search and cite CDPI's DPI knowledge from the shell. Standard library only.

Source text is untrusted data. This module only reads it as text; it never runs it.
"""

import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources.json"
ROUTES = ROOT / "data/routes.json"
CACHE = Path(os.environ.get("CDPI_CACHE") or Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "cdpi")
SITE = "https://docs.cdpi.dev"
GIT_TIMEOUT = 60
DOCS_WEIGHT = 1.5  # The wiki is CDPI's canonical text; ai-skills is secondary depth.
WORD = re.compile(r"[a-z0-9+]+")
STOP = set("a an and are as at be by can do does for from has have how i if in into is it its my of on or our "
           "should so that the their them this to use we what when which who why will with yes no you your".split())


class CdpiError(Exception):
    pass


def load_json(path):
    return json.loads(Path(path).read_text())


def sources():
    data = load_json(SOURCES)
    if data.get("schema_version") != 1:
        raise CdpiError("unsupported sources.json")
    return data["sources"]


def source_dir(source_id):
    return CACHE / "sources" / source_id


def git(*args, cwd=None):
    try:
        done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                              timeout=GIT_TIMEOUT, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return (done.stdout.strip(), None) if done.returncode == 0 else (None, done.stderr.strip() or f"exit {done.returncode}")


def local_ref(source_id):
    out, _ = git("rev-parse", "HEAD", cwd=source_dir(source_id)) if source_dir(source_id).is_dir() else (None, None)
    return out


# ---------- text ----------

def clean(text):
    """Strip GitBook markup so text reads plainly and tokenizes well."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"{%.*?%}", "", text)
    text = re.sub(r"<figure>.*?</figure>", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&#x20;", " ").replace("&nbsp;", " ").replace("\\\n", "\n")
    text = re.sub(r"\*\*\*\*", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def tokens(text):
    return [w for w in WORD.findall(text.lower()) if w not in STOP and len(w) > 1]


def url_for(source_id, relative):
    if source_id != "docs":
        repo = next(s for s in sources() if s["id"] == source_id)["repo"]
        return f"{repo}/blob/main/{relative}"
    path = relative.removesuffix(".md")
    path = re.sub(r"(^|/)README$", "", path)
    path = re.sub(r"^dpi/", "technical-notes/", path)
    return f"{SITE}/{path}".rstrip("/")


def documents():
    """Yield (source_id, relative_path, cleaned_text) for every cached Markdown file."""
    for source in sources():
        base = source_dir(source["id"])
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            relative = path.relative_to(base).as_posix()
            if relative.startswith(".") or relative in ("SUMMARY.md", "languages.md"):
                continue
            yield source["id"], relative, clean(path.read_text(errors="replace"))


def chunks(text):
    """Split at headings so a hit points at the section that answers the query."""
    parts, title, lines = [], "", []
    for line in text.splitlines():
        if line.startswith("#") and lines:
            parts.append((title, "\n".join(lines)))
            lines = []
        if line.startswith("#"):
            title = line.lstrip("# ").strip()
        lines.append(line)
    if lines:
        parts.append((title, "\n".join(lines)))
    return parts


# ---------- commands ----------

def cmd_sync(args):
    """Fetch each source at its pinned commit. With --check, report upstream drift without fetching."""
    code = 0
    for source in sources():
        sid, pin, target = source["id"], source["ref"], source_dir(source["id"])
        if args.check:
            out, error = git("ls-remote", source["repo"], "HEAD")
            head = out.split()[0] if out else None
            have = local_ref(sid)
            state = "UNKNOWN" if error else ("current" if head == pin else "UPDATE")
            print(f"{state:8} {sid}: pin {pin[:12]}, upstream {head[:12] if head else error}, local {have[:12] if have else 'missing'}")
            continue
        if local_ref(sid) == pin:
            print(f"current  {sid} {pin[:12]} at {target}")
            continue
        target.mkdir(parents=True, exist_ok=True)
        steps = [] if (target / ".git").is_dir() else [("init", "-q"), ("remote", "add", "origin", source["repo"])]
        steps += [("fetch", "-q", "--depth", "1", "origin", pin), ("checkout", "-q", "--force", "FETCH_HEAD")]
        for step in steps:
            _, error = git(*step, cwd=target)
            if error:
                print(f"FAILED   {sid}: git {step[0]}: {error}", file=sys.stderr)
                code = 1
                break
        else:
            print(f"synced   {sid} {pin[:12]} at {target}")
    return code


def cmd_status(args):
    """One call per session: sources, commands, and what to do when sources are missing."""
    routes = load_json(ROUTES)
    missing = []
    for source in sources():
        have = local_ref(source["id"])
        state = "ok" if have == source["ref"] else ("STALE" if have else "MISSING")
        if state != "ok":
            missing.append(source["id"])
        print(f"source   {source['id']:10} {state:8} {source['license']}")
    if missing:
        print(f"ACTION   run {ROOT}/bin/cdpi sync  (search and show need the sources; cards in reference/ work without them)")
    print("commands " + ", ".join(routes["commands"]))
    return 0


def score_route(text, routes):
    words = set(tokens(text))
    lowered = " " + re.sub(r"\s+", " ", text.lower()) + " "

    def hits(phrases):
        return sum(2 if " " in p else 1 for p in phrases
                   if (p in lowered if " " in p else p in words))

    commands = sorted(((hits(c["triggers"]), name) for name, c in routes["commands"].items()), reverse=True)
    blocks = sorted(((hits(b["triggers"]), name) for name, b in routes["blocks"].items()), reverse=True)
    return [c for c in commands if c[0] > 0], [b for b in blocks if b[0] > 0]


def cmd_route(args):
    """Pick the playbook and the concerns (identity, signing, data sharing...) a request touches, and list what to read."""
    routes = load_json(ROUTES)
    text = " ".join(args.request)
    commands, blocks = score_route(text, routes)
    if args.json:
        print(json.dumps({"commands": commands, "blocks": blocks}))
        return 0
    command = commands[0][1] if commands else routes["default"]
    spec = routes["commands"][command]
    print(f"command  {command}  ({spec['summary']})")
    for name in [n for _, n in commands[1:3]]:
        print(f"also     {name}  ({routes['commands'][name]['summary']})")
    print(f"read     {ROOT / 'reference' / spec['card']}")
    for _, name in blocks[:3]:
        block = routes["blocks"][name]
        print(f"concern  {name}")
        for page in block["docs"]:
            print(f"  wiki   {url_for('docs', page)}   cdpi show {page}")
        for skill in block.get("skills", []):
            print(f"  depth  cdpi show {skill}   (domain detail; load only if the card leaves a question open)")
    if not blocks:
        print("concern  none detected; apply the playbook to the system as described")
    return 0


def cmd_search(args):
    """BM25 over heading-level chunks of every cached source."""
    query = tokens(" ".join(args.query))
    if not query:
        raise CdpiError("empty query")
    corpus = []
    for sid, relative, text in documents():
        if args.source and sid != args.source:
            continue
        for title, body in chunks(text):
            corpus.append((sid, relative, title, body, tokens(title + " " + title + " " + body)))
    if not corpus:
        raise CdpiError(f"no sources cached; run {ROOT}/bin/cdpi sync")
    avg = sum(len(c[4]) for c in corpus) / len(corpus)
    df = {term: sum(1 for c in corpus if term in c[4]) for term in set(query)}
    ranked = []
    for sid, relative, title, body, words in corpus:
        score = 0.0
        for term in set(query):
            tf = words.count(term)
            if tf:
                idf = math.log(1 + (len(corpus) - df[term] + 0.5) / (df[term] + 0.5))
                score += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * len(words) / avg))
        if score:
            score *= DOCS_WEIGHT if sid == "docs" else 1.0
            ranked.append((score, sid, relative, title, body))
    ranked.sort(reverse=True)
    seen = set()
    shown = 0
    for score, sid, relative, title, body in ranked:
        if (relative, title) in seen:
            continue
        seen.add((relative, title))
        line = max((l for l in body.splitlines() if l.strip()),
                   key=lambda l: sum(t in l.lower() for t in query), default="")
        print(f"{score:5.1f}  {url_for(sid, relative)}  §{title or '-'}\n       cdpi show {sid}:{relative}\n       {line.strip()[:220]}")
        shown += 1
        if shown >= args.n:
            break
    return 0 if shown else 1


def resolve(name):
    """Accept 'docs:path.md', a docs path, an ai-skills skill id such as dpi-payments, or a docs.cdpi.dev URL."""
    if name.startswith(SITE):
        wanted = name.removeprefix(SITE).strip("/")
        for sid, relative, _ in documents():
            if sid == "docs" and url_for(sid, relative).removeprefix(SITE).strip("/") == wanted:
                return sid, relative
        raise CdpiError(f"no cached page for {name}")
    sid, _, relative = name.partition(":") if ":" in name else ("", "", name)
    candidates = [(sid, relative)] if sid else [("docs", relative), ("ai-skills", relative),
                                                 ("ai-skills", f"skills/{relative}.md")]
    for sid, relative in candidates:
        if (source_dir(sid) / relative).is_file():
            return sid, relative
    raise CdpiError(f"not found: {name}. Try cdpi search, or cdpi sync if sources are missing")


def cmd_show(args):
    sid, relative = resolve(args.name)
    text = clean((source_dir(sid) / relative).read_text(errors="replace"))
    if args.section:
        wanted = args.section.lower()
        picked = [body for title, body in chunks(text) if wanted in title.lower()]
        if not picked:
            raise CdpiError(f"no heading containing '{args.section}'. Headings: "
                            + "; ".join(t for t, _ in chunks(text) if t))
        text = "\n\n".join(picked)
    print(f"source: {url_for(sid, relative)}  ({next(s['license'] for s in sources() if s['id'] == sid)})\n")
    print(text)
    return 0


def cmd_list(args):
    routes = load_json(ROUTES)
    if args.what == "commands":
        for name, spec in routes["commands"].items():
            print(f"{name:16} {spec['summary']}")
    elif args.what == "blocks":
        for name, spec in routes["blocks"].items():
            print(f"{name:16} {', '.join(spec.get('skills', [])) or '-'}")
    else:
        for sid, relative, text in documents():
            title = next((l.lstrip("# ") for l in text.splitlines() if l.startswith("# ")), relative)
            print(f"{sid}:{relative}\t{title}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cdpi", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("sync", help="fetch pinned sources into the cache")
    p.add_argument("--check", action="store_true", help="compare pins with upstream; fetch nothing")
    p.set_defaults(run=cmd_sync)
    sub.add_parser("status", help="sources and commands; run once per session").set_defaults(run=cmd_status)
    p = sub.add_parser("route", help="pick the playbook and DPI blocks for a request")
    p.add_argument("request", nargs="+")
    p.add_argument("--json", action="store_true")
    p.set_defaults(run=cmd_route)
    p = sub.add_parser("search", help="ranked passages with citation URLs")
    p.add_argument("query", nargs="+")
    p.add_argument("-n", type=int, default=6)
    p.add_argument("--source", choices=["docs", "ai-skills"])
    p.set_defaults(run=cmd_search)
    p = sub.add_parser("show", help="print one page, cleaned, with its URL")
    p.add_argument("name")
    p.add_argument("--section", help="only sections whose heading contains this text")
    p.set_defaults(run=cmd_show)
    p = sub.add_parser("list", help="commands, blocks, or every cached page")
    p.add_argument("what", choices=["commands", "blocks", "pages"])
    p.set_defaults(run=cmd_list)
    args = parser.parse_args(argv)
    try:
        return args.run(args)
    except CdpiError as exc:
        print(f"cdpi: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
