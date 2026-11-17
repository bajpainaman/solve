"""Original, offline HTML artifacts with explicit static and browser checks.

The JSON authoring format accepts title, summary, optional eyebrow and sources,
and sections containing heading plus paragraphs, bullets, table, or preformatted
text. This module does not fetch resources, execute author-supplied code, or use
html-artifact. A successful render is never a verified decision.
"""

import argparse
import base64
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import parse_qsl, urlsplit

from solve_contract import ContractError, check_reference, file_hash, inside, read_json, require

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_SNAPSHOT_BYTES = 512 * 1024
SECRET_PATTERNS = (
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
    r"\b(?:sk-(?:proj-|svcacct-)?|gh[pousr]_|github_pat_)[A-Za-z0-9_-]{20,}\b",
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    r"\bxox[baprs]-[A-Za-z0-9-]{15,}\b",
    r"\bBearer\s+[A-Za-z0-9._~+/-]{20,}=*",
)
SECRET_QUERY_KEYS = {"token", "access_token", "api_key", "apikey", "password", "secret", "client_secret", "sig", "signature", "x-amz-signature", "x-amz-credential"}
STYLE = """:root{color-scheme:light dark;--bg:#f4f5f8;--panel:#fff;--ink:#17202c;
--muted:#4d5c70;--line:#d7dfe8;--accent:#2258b0;--soft:#eaf0fa}
@media(prefers-color-scheme:dark){:root{--bg:#111722;--panel:#1b2432;
--ink:#ecf0f7;--muted:#b3c0d2;--line:#3a485c;--accent:#9ac1ff;--soft:#25344b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
overflow-wrap:anywhere}main{max-width:1120px;margin:0 auto;padding:28px 24px 64px}
header{padding:24px 0 28px;border-bottom:2px solid var(--line);margin-bottom:24px}
.eyebrow{color:var(--muted);font-size:14px;letter-spacing:.06em;font-weight:650}
h1{font-size:clamp(28px,5vw,46px);line-height:1.16;max-width:26ch;margin:12px 0 20px;
letter-spacing:-.035em}h2{font-size:22px;line-height:1.3;margin:0 0 16px}
.summary{font-size:19px;max-width:70ch}.card,details{background:var(--panel);
border:1px solid var(--line);border-radius:14px;padding:24px;margin:18px 0}
p{margin:12px 0}li{margin:8px 0}a{color:var(--accent);text-underline-offset:3px}
a:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:4px}
.table-wrap{max-width:100%;overflow-x:auto;border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;min-width:560px;text-align:left;font-size:14px}
th,td{padding:13px 15px;border-bottom:1px solid var(--line);vertical-align:top;
min-width:90px;max-width:420px;overflow-wrap:anywhere}th{background:var(--soft);font-weight:700}
tr:last-child td{border-bottom:0}summary{cursor:pointer;font-weight:650;font-size:17px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.6;
max-width:100%;font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
footer{color:var(--muted);font-size:14px;margin-top:28px;border-top:1px solid var(--line);padding-top:16px}
@media(max-width:500px){main{padding:12px 16px 36px}.card,details{padding:17px}h2{font-size:20px}}
@media print{body{background:#fff;color:#111}main{max-width:none;padding:0}
.card,details{break-inside:avoid;border-color:#bbb}a{color:#111}.table-wrap{overflow:visible}
table{min-width:0}summary{list-style:none}details>*{display:block!important}}
""".strip()


def safe_url(value):
    require(isinstance(value, str) and bool(value), "source URL must be a nonempty string")
    require(not re.search(r"[\s\x00-\x1f\x7f\\\\]", value), "source URL cannot contain whitespace, controls, or backslashes")
    try:
        parts = urlsplit(value)
        require(parts.scheme in ("http", "https") and bool(parts.hostname), "source URL must use absolute HTTP or HTTPS")
        require(parts.username is None and parts.password is None, "source URL cannot contain credentials")
        require(not any(key.lower() in SECRET_QUERY_KEYS and val for key, val in parse_qsl(parts.query)),
                "source URL contains a credential-shaped query parameter; use a public canonical URL")
        parts.port
    except ValueError as exc:
        raise ContractError(f"invalid source URL: {exc}") from exc
    return value


def assert_no_credentials(value):
    """Block common credential shapes; this is not a complete secret detector."""
    if isinstance(value, dict):
        for item in value.values():
            assert_no_credentials(item)
    elif isinstance(value, list):
        for item in value:
            assert_no_credentials(item)
    elif isinstance(value, str):
        require(not any(re.search(pattern, value) for pattern in SECRET_PATTERNS),
                "credential-shaped content detected; provide a redacted evidence excerpt before creating a shareable artifact")
        assignment = re.search(r'''(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|password)\b["']?\s*[:=]\s*["']?([A-Za-z0-9_./+-]{8,})''', value)
        if assignment:
            require(assignment.group(1).upper().startswith(("REDACTED", "EXAMPLE", "PLACEHOLDER", "REPLACE_")),
                    "credential-shaped assignment detected; provide a redacted evidence excerpt before creating a shareable artifact")


def _text(value, name, nonempty=True):
    require(isinstance(value, str), f"{name} must be a string")
    require(not nonempty or bool(value.strip()), f"{name} must not be blank")
    return value


def _texts(value, name):
    require(isinstance(value, list) and all(isinstance(x, str) for x in value), f"{name} must be a list of strings")
    return value


def validate_document(data):
    require(isinstance(data, dict), "artifact JSON must be an object")
    require(not set(data) - {"title", "summary", "eyebrow", "sections", "sources"}, "unknown artifact fields")
    _text(data.get("title"), "title")
    _text(data.get("summary", ""), "summary", False)
    _text(data.get("eyebrow", "Solve artifact"), "eyebrow")
    sections = data.get("sections", [])
    require(isinstance(sections, list), "sections must be a list")
    require(bool(sections) or bool(data.get("summary", "").strip()), "provide a summary or at least one section")
    for index, section in enumerate(sections):
        label = f"section {index + 1}"
        require(isinstance(section, dict), f"{label} must be an object")
        require(not set(section) - {"heading", "paragraphs", "bullets", "table", "preformatted", "collapsed"}, f"{label}: unknown fields")
        _text(section.get("heading"), f"{label} heading")
        require(type(section.get("collapsed", False)) is bool, f"{label} collapsed must be Boolean")
        for key in ("paragraphs", "bullets"):
            _texts(section.get(key, []), f"{label} {key}")
        if "preformatted" in section:
            _text(section["preformatted"], f"{label} preformatted", False)
        if "table" in section:
            table = section["table"]
            require(isinstance(table, dict) and set(table) == {"headers", "rows"}, f"{label} table needs headers and rows")
            headers = _texts(table["headers"], f"{label} table headers")
            require(headers and all(h.strip() for h in headers), f"{label} table needs nonempty headers")
            require(isinstance(table["rows"], list), f"{label} table rows must be a list")
            for row in table["rows"]:
                _texts(row, f"{label} table row")
                require(len(row) == len(headers), f"{label} table row width differs from headers")
    sources = data.get("sources", [])
    require(isinstance(sources, list), "sources must be a list")
    for source in sources:
        require(isinstance(source, dict) and set(source) == {"label", "url"}, "each source needs label and url")
        _text(source["label"], "source label")
        safe_url(source["url"])
    return data


def render_document(data):
    validate_document(data)
    assert_no_credentials(data)
    out = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'">',
           f'<title>{escape(data["title"])}</title>', f"<style>{STYLE}</style></head><body><main>",
           '<header>', f'<p class="eyebrow">{escape(data.get("eyebrow", "Solve artifact"))}</p>',
           f'<h1>{escape(data["title"])}</h1>']
    if data.get("summary"):
        out.append(f'<p class="summary">{escape(data["summary"])}</p>')
    out.append("</header>")
    for index, section in enumerate(data.get("sections", []), 1):
        collapsed = section.get("collapsed", False)
        tag = "details" if collapsed else "section"
        out.append(f'<{tag} class="card" id="section-{index}">')
        heading_tag = "summary" if collapsed else "h2"
        out.append(f'<{heading_tag}>{escape(section["heading"])}</{heading_tag}>')
        out.extend(f"<p>{escape(p)}</p>" for p in section.get("paragraphs", []))
        if section.get("bullets"):
            out.extend(["<ul>", *[f"<li>{escape(p)}</li>" for p in section["bullets"]], "</ul>"])
        if "table" in section:
            table = section["table"]
            out += ['<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable table"><table><thead><tr>',
                    *[f'<th scope="col">{escape(h)}</th>' for h in table["headers"]], "</tr></thead><tbody>"]
            for row in table["rows"]:
                out.append("<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>")
            out.append("</tbody></table></div>")
        if "preformatted" in section:
            out.append(f'<pre>{escape(section["preformatted"])}</pre>')
        out.append(f"</{tag}>")
    if data.get("sources"):
        out += ['<section class="card" id="sources"><h2>Sources</h2><ul>']
        out += [f'<li><a href="{escape(s["url"], quote=True)}" rel="noopener noreferrer">{escape(s["label"])}</a></li>' for s in data["sources"]]
        out.append("</ul></section>")
    out += ["<footer>Generated by Solve. Rendering and layout checks do not establish that the claims are true.</footer>",
            "</main></body></html>", ""]
    page = "\n".join(out)
    require(len(page.encode()) <= MAX_FILE_BYTES, "artifact exceeds the 8 MiB portable page limit")
    return page


class StaticInspector(HTMLParser):
    ALLOWED = set("html head meta title style body main header section h1 h2 p ul li div table thead tbody tr th td details summary pre a footer".split())

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.errors, self.ids, self.anchors = [], set(), []
        self.h1 = self.titles = 0
        self.viewport = self.lang = self.csp = False
        self.in_style = False
        self.css = ""

    def handle_starttag(self, tag, attrs):
        if len({key for key, _ in attrs}) != len(attrs):
            self.errors.append("duplicate HTML attributes are not allowed")
        attrs = {key: value or "" for key, value in attrs}
        if tag not in self.ALLOWED:
            self.errors.append(f"unsupported or active element: {tag}")
        if any(k.lower().startswith("on") for k in attrs):
            self.errors.append("inline event handlers are not allowed")
        if any(k in attrs for k in ("src", "srcset", "action", "formaction", "srcdoc")):
            self.errors.append("external resources, embedded documents, and forms are not allowed")
        if "style" in attrs:
            self.css += attrs["style"] or ""
        if tag == "style":
            self.in_style = True
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.titles += 1
        if tag == "html":
            self.lang = bool(attrs.get("lang"))
        if tag == "meta":
            if attrs.get("name", "").lower() == "viewport":
                self.viewport = "width=device-width" in attrs.get("content", "")
            if attrs.get("http-equiv", "").lower() == "refresh":
                self.errors.append("automatic redirects are not allowed")
            if attrs.get("http-equiv", "").lower() == "content-security-policy":
                content = attrs.get("content", "")
                self.csp = "default-src 'none'" in content and "form-action 'none'" in content
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append("duplicate element ID")
            self.ids.add(attrs["id"])
        if "href" in attrs:
            href = attrs["href"] or ""
            if tag != "a":
                self.errors.append("only source anchors may use href")
            elif href.startswith("#"):
                self.anchors.append(href[1:])
            else:
                try:
                    safe_url(href)
                except ContractError as exc:
                    self.errors.append(str(exc))

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.css += data


def verify_static(path):
    path = Path(path)
    require(path.is_file(), f"no such artifact: {path}")
    require(path.stat().st_size <= MAX_FILE_BYTES, "artifact exceeds the 8 MiB portable page limit")
    inspector = StaticInspector()
    inspector.feed(path.read_text(encoding="utf-8"))
    inspector.close()
    if inspector.h1 != 1 or inspector.titles != 1:
        inspector.errors.append("provide exactly one title and one h1")
    if not (inspector.lang and inspector.viewport and inspector.csp):
        inspector.errors.append("missing language, responsive viewport, or restrictive content security policy")
    if "prefers-color-scheme" not in inspector.css:
        inspector.errors.append("dark-mode styling is missing")
    if re.search(r"@import|url\s*\(|expression\s*\(|-moz-binding", inspector.css, re.I):
        inspector.errors.append("CSS may not import resources or execute expressions")
    if any(a not in inspector.ids for a in inspector.anchors):
        inspector.errors.append("broken internal anchor")
    return {"status": "passed" if not inspector.errors else "failed", "errors": list(dict.fromkeys(inspector.errors)),
            "scope": "Static structure, escaping boundary, source URLs, and absence of active/external resources. No claim or visual verification."}


def verify_browser(path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"status": "blocked", "errors": ["Playwright is not installed. Browser verification did not run."]}
    errors, requests, samples = [], [], []
    executable = os.environ.get("SOLVE_BROWSER_EXECUTABLE") or shutil.which("chromium") or shutil.which("google-chrome")
    try:
        with sync_playwright() as playwright:
            args = {"headless": True, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
            if executable:
                args["executable_path"] = executable
            browser = playwright.chromium.launch(**args)
            context = browser.new_context(service_workers="block")
            # Do not allow author content to fetch the network during verification.
            context.route("**/*", lambda route: route.abort() if urlsplit(route.request.url).scheme in ("http", "https", "ws", "wss") else route.continue_())
            page = context.new_page()
            page.on("request", lambda request: requests.append(request.url) if urlsplit(request.url).scheme in ("http", "https", "ws", "wss") else None)
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
            for width, scheme in ((390, "light"), (1280, "light"), (390, "dark"), (1280, "dark")):
                page.set_viewport_size({"width": width, "height": 900})
                page.emulate_media(color_scheme=scheme)
                page.goto(Path(path).resolve().as_uri(), wait_until="load", timeout=15000)
                observed = page.evaluate("""() => ({
                  overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
                  smallText: Array.from(document.body.querySelectorAll('*')).filter(e =>
                    e.getClientRects().length && Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim()) &&
                    parseFloat(getComputedStyle(e).fontSize) < 12).length,
                  background: getComputedStyle(document.body).backgroundColor
                })""")
                samples.append({"width": width, "scheme": scheme, **observed})
                if observed["overflow"] or observed["smallText"]:
                    errors.append(f"layout failed at {width}px/{scheme}: {observed}")
            if samples[0]["background"] == samples[2]["background"]:
                errors.append("light and dark backgrounds are identical")
            details = page.locator("details")
            if details.count():
                details.first.locator("summary").click()
                if not details.first.evaluate("e => e.open"):
                    errors.append("details disclosure did not open")
            context.close()
            browser.close()
    except Exception as exc:
        return {"status": "blocked", "errors": [f"Browser verification did not complete: {exc}"]}
    if requests:
        errors.append("page attempted external network requests")
    return {"status": "passed" if not errors else "failed", "errors": list(dict.fromkeys(errors)), "samples": samples,
            "network_requests": requests, "scope": "Chromium at 390/1280 pixels, light/dark mode, console, page overflow, minimum font size, and disclosure interaction. No claim verification."}


def verify(path, browser=False):
    static = verify_static(path)
    checked = {"status": "not_run", "errors": []}
    if browser and static["status"] == "passed":
        checked = verify_browser(path)
    return {"path": str(Path(path).resolve()), "sha256": file_hash(path), "static": static, "browser": checked,
            "ok": static["status"] == "passed" and (not browser or checked["status"] == "passed")}


def _check_output(path, overwrite, input_path=None):
    path = Path(path).absolute()
    require(not path.is_symlink(), f"refusing symlink output: {path}")
    if input_path is not None:
        require(path.resolve() != Path(input_path).resolve(), "output cannot replace the input")
        if path.exists() and Path(input_path).exists():
            require(not path.samefile(input_path), "output cannot replace an alias of the input")
    require(not path.exists() or (overwrite and path.is_file()), f"output already exists: {path}; use --overwrite to replace it")
    return path


def _atomic_text(path, text, overwrite=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=".solve-artifact-", delete=False) as stream:
        staged = Path(stream.name)
        stream.write(text)
    try:
        if overwrite:
            os.replace(staged, path)
        else:
            # An exclusive link also protects against another writer creating
            # the destination between the preflight and this publication.
            os.link(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def build_document(data, output, overwrite=False, input_path=None):
    page = render_document(data)
    output = Path(output).absolute()
    require(output.suffix.lower() == ".html", "artifact output must have an .html extension")
    source = output.with_name(output.stem + ".src.json")
    _check_output(output, overwrite, input_path)
    source_is_input = input_path is not None and source.resolve() == Path(input_path).resolve()
    if not source_is_input:
        _check_output(source, overwrite, input_path)
    # Verify generated bytes before publishing either file.
    with tempfile.TemporaryDirectory(prefix="solve-artifact-") as scratch:
        candidate = Path(scratch) / "candidate.html"
        candidate.write_text(page, encoding="utf-8")
        checked = verify_static(candidate)
        require(checked["status"] == "passed", "portable render failed static checks: " + "; ".join(checked["errors"]))
    if not source_is_input:
        _atomic_text(source, json.dumps(data, indent=2, ensure_ascii=False) + "\n", overwrite)
    _atomic_text(output, page, overwrite)
    return {"path": str(output.resolve()), "sha256": file_hash(output), "source": str(source.resolve()),
            "source_sha256": file_hash(source), "static": checked, "browser": {"status": "not_run"}, "verified_decision": False}


def _snapshot_sections(run, roots):
    """Embed referenced run files as inert text, with exact byte hashes."""
    seen, sections = set(), []
    for name in roots:
        if name in seen:
            continue
        seen.add(name)
        path = inside(run, name)
        require(path.is_file(), f"missing snapshot file: {name}")
        require(path.stat().st_size <= MAX_SNAPSHOT_BYTES, f"{name}: snapshot exceeds 512 KiB; use a bounded evidence excerpt with a source hash")
        raw = path.read_bytes()
        try:
            content, encoding = raw.decode("utf-8"), "UTF-8"
        except UnicodeDecodeError:
            content, encoding = base64.b64encode(raw).decode("ascii"), "Base64 binary snapshot"
        sections.append({"heading": f"Snapshot: {name}", "collapsed": True,
                         "paragraphs": [f"SHA-256: {file_hash(path)} · {len(raw)} bytes · {encoding}"], "preformatted": content})
    return sections


def _snapshot_names(run, result, records):
    """Follow only fields in the known contract, never links inside evidence."""
    names = [name for name in ("request.md", "intake.json", "claims.json", "facts.json") if (run / name).is_file()]

    def add(ref):
        checked = check_reference(run, ref)
        names.append(checked["path"])

    def add_many(refs):
        for ref in refs:
            add(ref)

    if (run / "facts.json").is_file():
        facts = read_json(run / "facts.json")
        for fact in facts.values() if isinstance(facts, dict) else []:
            if isinstance(fact, dict) and isinstance(fact.get("evidence"), list):
                for ref in fact["evidence"]:
                    # A malformed fact stays visible in its raw snapshot and
                    # is BLOCKED by the contract; do not follow an invalid ref.
                    try:
                        add(ref)
                    except ContractError:
                        pass
    names += [f"gates/{row['gate']}.json" for row in result["gates"]
              if row["gate"] != "consumer" and (run / "gates" / f"{row['gate']}.json").is_file()]
    for gate, record in records.items():
        add(record["artifact"])
        for check in record["checks"]:
            add_many(check["evidence"])
        if "coverage" in record:
            add_many(record["coverage"]["evidence"])
        if gate == "refutation":
            review = record["review"]
            add(review["manifest"])
            manifest = read_json(inside(run, review["manifest"]["path"]))
            add_many(manifest["inputs"])
            add(review["reveal"])
            reveal = read_json(inside(run, review["reveal"]["path"]))
            add(reveal["blind"])
            add(reveal["claims"])
            blind = read_json(inside(run, reveal["blind"]["path"]))
            add_many(blind["evidence"])
    return names


def build_decision(run, output, slug, state, claims, result, catalog_by_id, dissent):
    run = Path(run)
    output = Path(output).absolute()
    require(run.resolve() not in output.resolve().parents or output.resolve() == run.resolve() / "report.html",
            "inside a run, portable decision output must be report.html")
    records = {row["gate"]: read_json(run / "gates" / f"{row['gate']}.json")
               for row in result["gates"] if row["state"] == "FIRED"}
    checks = [(gate, check) for gate, record in records.items() if catalog_by_id[gate]["kind"] == "required" for check in record["checks"]]
    rows = []
    for cid, claim in claims.items():
        own = [check for _, check in checks if check["claim"] == cid]
        status = "Failed a check" if any(not check["passed"] for check in own) else "Forecast" if claim["kind"] == "forecast" else "Checked" if own else "Not checked"
        rows.append([cid, claim["statement"], claim["kind"], "yes" if claim["critical"] else "no", status,
                     claim["acceptance"]["surface"], claim["acceptance"]["expected"]])
    status = "Pre-consumer checks passed; independent consumer review and finalization remain separate." if result["ready"] and not state.get("partial") else "Unverified draft. Required checks are blocked, failed, or halted."
    sections = [{"heading": "Decision status", "paragraphs": [status,
                 "This is an immutable render-time snapshot. The page does not claim completed consumer verification. A separate completion receipt must bind these exact HTML bytes and the Markdown report."]},
                {"heading": "What the decision depends on", "table": {"headers": ["Claim", "Statement", "Kind", "Critical", "Status", "Surface", "Expected"], "rows": rows}}]
    changes = list(dissent)
    changes += [f"Forecast {cid}: assumptions: {claim['assumptions']}. Follow-up: {claim['followup']}"
                for cid, claim in claims.items() if claim["kind"] == "forecast"]
    sections.append({"heading": "What would change the choice", "bullets": changes or ["No unresolved failure was recorded before the consumer review. This does not rule out omitted claims or future changes."]})
    sections.append({"heading": "Observed checks", "table": {"headers": ["Gate", "Claim", "Outcome", "Surface", "Expected", "Observed", "Evidence snapshot"],
                    "rows": [[gate, check["claim"], "passed" if check["passed"] else "FAILED", check["surface"], check["expected"], check["observed"],
                              ", ".join(ref["path"] for ref in check["evidence"])] for gate, check in checks]}})
    sections.append({"heading": "Gate status", "collapsed": True, "table": {"headers": ["Gate", "State", "Reason"],
                    "rows": [[row["gate"], row["state"], row["reason"]] for row in result["gates"]]}})
    sections += _snapshot_sections(run, _snapshot_names(run, result, records))
    doc = {"title": str(state.get("recommendation") or "No recommendation has been established."),
           "summary": "Next action: " + str(state.get("next_action") or "No next action has been established."),
           "eyebrow": f"Solve · Decision snapshot · {slug}", "sections": sections}
    return build_document(doc, output, overwrite=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="build a standalone HTML page from inert JSON content")
    build.add_argument("input")
    build.add_argument("--output", required=True)
    build.add_argument("--overwrite", action="store_true")
    check = sub.add_parser("verify", help="check static structure; optionally run Chromium checks")
    check.add_argument("input")
    check.add_argument("--browser", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            source = Path(args.input)
            require(source.is_file() and source.stat().st_size <= MAX_FILE_BYTES, "input is missing or exceeds 8 MiB")
            result = build_document(json.loads(source.read_text(encoding="utf-8")), args.output, args.overwrite, source)
        else:
            result = verify(args.input, args.browser)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("ok", True) else 2
    except (ContractError, OSError, ValueError, TypeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
