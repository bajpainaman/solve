"""Find the page template for a request: list, show, or match the catalog."""

import argparse
import json
from pathlib import Path
import re
import sys

from solve_contract import ContractError, require
import solve_html

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "templates/catalog.json"
RENDERERS = ("artifact", "bespoke", "solve")
# A matched use_when phrase outweighs scattered word overlap.
PHRASE_WEIGHT = 3
MATCH_LIMIT = 3
STOPWORDS = frozenset("a an and are as at be by for from how i in is it me my of on or that the this to we what with you".split())


def load():
    data = json.loads(CATALOG.read_text())
    require(data.get("schema_version") == 1, "unsupported template catalog")
    templates = data["templates"]
    ids = [t["id"] for t in templates]
    require(len(ids) == len(set(ids)), "template ids must be unique")
    for t in templates:
        require(t["renderer"] in RENDERERS, f"{t['id']}: unknown renderer {t['renderer']}")
        require(t["file"] is None or (ROOT / "templates" / t["file"]).is_file(), f"{t['id']}: missing exemplar {t['file']}")
        require(t["use_when"], f"{t['id']}: needs use_when phrases")
    return data


def html_artifact_dir():
    try:
        return solve_html.locate_html_artifact()
    except ContractError:
        return None


def effective_renderer(template, artifact_dir):
    """Without html-artifact, component pages fall back to their exemplar."""
    if template["renderer"] == "artifact" and artifact_dir is None:
        return "bespoke"
    return template["renderer"]


def _words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOPWORDS}


def match(request, templates, limit=MATCH_LIMIT):
    text = " ".join(re.findall(r"[a-z0-9/]+", request.lower()))
    words = _words(request)
    scored = []
    for t in templates:
        phrases = sum(PHRASE_WEIGHT for p in t["use_when"] if p in text)
        overlap = len(words & _words(" ".join([t["title"], t["shape"], *t["use_when"]])))
        if phrases or overlap:
            scored.append((phrases + overlap, t))
    scored.sort(key=lambda pair: -pair[0])
    return scored[:limit]


def describe(template, data, artifact_dir):
    renderer = effective_renderer(template, artifact_dir)
    lines = [f"{template['id']}: {template['title']} ({template['family']})",
             f"  shape:    {template['shape']}",
             f"  renderer: {renderer}" + (" (HTML mode missing: run bin/html-sync)" if renderer != template["renderer"] else "")]
    if template["file"]:
        lines.append(f"  exemplar: {ROOT / 'templates' / template['file']}")
    if template.get("artifact_type") and artifact_dir:
        lines.append(f"  type:     {artifact_dir / 'references/types' / (template['artifact_type'] + '.md')}")
    if template.get("components"):
        lines.append(f"  components: {', '.join(template['components'])}")
    lines.append(f"  how:      {data['renderers'][renderer]}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("list")
    p.add_argument("--family")
    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("match")
    p.add_argument("request", help="the request text, quoted")
    p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        data = load()
        templates = data["templates"]
        artifact_dir = html_artifact_dir()
        if args.command == "list":
            for t in templates:
                if not args.family or t["family"] == args.family:
                    print(f"{t['family']:<12} {t['id']:<22} {effective_renderer(t, artifact_dir):<9} {t['title']}")
        elif args.command == "show":
            found = [t for t in templates if t["id"] == args.id]
            require(found, f"unknown template: {args.id}. Run `bin/templates list`")
            print(describe(found[0], data, artifact_dir))
        else:
            hits = match(args.request, templates)
            if args.json:
                print(json.dumps([{"score": s, "id": t["id"], "renderer": effective_renderer(t, artifact_dir)} for s, t in hits]))
            elif not hits:
                print("No template matches. Use markdown, or pick one from `bin/templates list`.")
            else:
                print("\n\n".join(f"[score {s}] " + describe(t, data, artifact_dir) for s, t in hits))
        return 0
    except (ContractError, OSError, KeyError, ValueError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
