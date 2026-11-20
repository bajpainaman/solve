"""Generate skills/skill-router/SKILL.md: the router header plus a one-line catalog of every skill and subskill.

The catalog is built from the vendored files at their pins, so a pin bump changes it in the same commit.
Run through `bin/build-plugin --tree`; a test fails when the committed file is stale.
"""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HEADER = Path("plugin/router/HEADER.md")
TARGET = Path("skills/skill-router/SKILL.md")
TOOLKITS = ("testing-toolkit", "fv-toolkit", "sdlc-toolkit", "pr-review")
# Names only. ai-skills publishes no license, so its text is never copied; `cdpi show <id>` reads the fetched page.
CDPI_AI_SKILLS = (
    "dpi-101", "dpi-+1-approach", "dpi-ai-blocks", "dpi-ai-framework", "dpi-ai-use-cases", "dpi-ai-workflows",
    "dpi-architect", "dpi-childhood", "dpi-cloud", "dpi-country-technical-recommendation", "dpi-credebl",
    "dpi-data-exchange", "dpi-data-sharing-models", "dpi-digital-id", "dpi-discovery-fulfilment", "dpi-e-signet",
    "dpi-health", "dpi-inji", "dpi-mcp-dpg", "dpi-n8n", "dpi-opencrvs", "dpi-openfn", "dpi-payments",
    "dpi-public-agents", "dpi-registries", "dpi-superapp", "dpi-trust-infra", "dpi-un-safeguards",
    "dpi-use-cases", "dpi-x-road", "verifiable-credentials")
MAX_LINE = 120


def frontmatter(path):
    import yaml
    text = Path(path).read_text()
    if not text.startswith("---\n"):
        return {}
    return yaml.safe_load(text[4:text.index("\n---\n", 4)]) or {}


def summary(description, limit=MAX_LINE):
    """The first sentence of a description, before its 'Use when' clause, shortened at a clause boundary."""
    text = " ".join(str(description).split())
    text = re.split(r"\s(?:Use (?:when|for|to|whenever)|Triggers include)\b", text, maxsplit=1)[0].strip()
    text = re.sub(r"^SDLC stage \d+(?:, [^.]+)?\.\s*", "", text)
    text = re.split(r"(?<=[a-z0-9)])\. ", text, maxsplit=1)[0].rstrip(".")
    for cut in (": ", ", ", " with ", " and "):
        if len(text) <= limit:
            break
        head = text[:limit].rsplit(cut, 1)[0]
        if cut in text[:limit] and len(head) >= 40:
            text = head
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0]
    return text.rstrip(",;: ")


def toolkit_lines(root, toolkit):
    lines = []
    for skill in sorted((root / "skills" / toolkit / "skills").glob("*/SKILL.md")):
        meta = frontmatter(skill)
        lines.append(f"  - `{meta['name']}`: {summary(meta['description'])}.")
    return lines


def build(root=ROOT):
    root = Path(root)
    out = [root.joinpath(HEADER).read_text().rstrip(), "", "## Catalog", ""]
    templates = json.loads((root / "templates/catalog.json").read_text())["templates"]
    out += ["- **solve** (`../solve/SKILL.md`): decisions, artifacts and writing.",
            "  - `decide`: a gated decision run with checked claims, a blind refuter and a consumer review, ending in a decision memo.",
            f"  - `make`: {len(templates)} page templates ({', '.join(t['id'] for t in templates)}), built with html-artifact components.",
            "  - `write`: simplify-writing (ASD-STE100 with Vale and Harper) to rewrite, audit or lint prose.",
            "  - `answer`: a short reply with no ledger."]
    routes = json.loads((root / "skills/cdpi/data/routes.json").read_text())
    out += ["- **cdpi** (`../cdpi/SKILL.md`): DPI thinking as an engineering lens; cites docs.cdpi.dev."]
    out += [f"  - `{name}`: {spec['summary']}." for name, spec in routes["commands"].items()]
    out += [f"  - concerns that `cdpi route` detects: {', '.join(routes['blocks'])}.",
            f"  - ai-skills domain pages, read with `cdpi show <id>` after `cdpi sync`: {', '.join(CDPI_AI_SKILLS)}."]
    out += ["- **impeccable** (`../impeccable/SKILL.md`): frontend design, critique and polish."]
    table = (root / "skills/impeccable/SKILL.md").read_text()
    for name, category, description in re.findall(r"^\| `([a-z]+)[^`]*` \| (\w+) \| ([^|]+) \|", table, re.M):
        out.append(f"  - `{name}` ({category.lower()}): {description.strip()}.")
    for toolkit in TOOLKITS:
        meta = frontmatter(root / "skills" / toolkit / "SKILL.md")
        out.append(f"- **{toolkit}** (`../{toolkit}/SKILL.md`; subskill `x` is `../{toolkit}/skills/x/SKILL.md`): "
                   f"{summary(meta['description'])}.")
        out += toolkit_lines(root, toolkit)
    return "\n".join(out) + "\n"


def write(root=ROOT):
    target = Path(root) / TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build(root))
    return target


if __name__ == "__main__":
    print(f"wrote {write()}")
