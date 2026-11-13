"""Build the decision-memo HTML view of a rendered report with html-artifact.

The view is derived only from validated run data, never from builder prose that
the report omits. Its hash joins the report's render subject, so the consumer
review and the completion receipt cover what the reader actually opens.
"""

from datetime import date
from html import escape
import os
from pathlib import Path
import re
import subprocess

from solve_contract import ContractError, file_hash, read_json, require

HTML_ARTIFACT_ENV = "SOLVE_HTML_ARTIFACT"
BUILD_TIMEOUT_SECONDS = 180
# Searched in order: the built-in copy from bin/html-sync, then installed plugin versions, then skills.
BUILT_IN = Path(__file__).resolve().parents[1] / "html"
PLUGIN_CACHE = Path.home() / ".claude/plugins/cache/html-artifact/html-artifact"
SKILL_DIRS = (Path.home() / ".claude/skills/html-artifact", Path.home() / ".agents/skills/html-artifact")
BUILD_SCRIPT = Path("scripts/build.mjs")


def _version_key(path):
    return tuple(int(part) if part.isdigit() else 0 for part in re.split(r"[.-]", path.name))


def locate_html_artifact():
    """Return the html-artifact skill directory, or fail with how to install it."""
    explicit = os.environ.get(HTML_ARTIFACT_ENV)
    if explicit:
        skill = Path(explicit).expanduser()
        require((skill / BUILD_SCRIPT).is_file(), f"{HTML_ARTIFACT_ENV}={explicit} has no {BUILD_SCRIPT}")
        return skill
    candidates = [v / "skills/html-artifact" for v in sorted(PLUGIN_CACHE.glob("*"), key=_version_key, reverse=True)]
    for skill in [BUILT_IN, *candidates, *SKILL_DIRS]:
        if (skill / BUILD_SCRIPT).is_file():
            return skill
    raise ContractError("the built-in HTML mode is missing. Run `$SOLVE_ROOT/bin/html-sync`, "
                        f"or set {HTML_ARTIFACT_ENV} to an html-artifact skill directory")


def _href(output, target):
    return escape(os.path.relpath(Path(target).resolve(), Path(output).resolve().parent), quote=True)


def _a(output, target, label):
    return f'<a href="{_href(output, target)}">{escape(label)}</a>'


def _claim_status(claim_id, claim, checks):
    """Map a claim's checks to html-artifact evidence levels and a tone."""
    own = [c for c in checks if c["claim"] == claim_id]
    if any(not c["passed"] for c in own):
        return "inferred", "crit", "Failed a check"
    if claim["kind"] == "forecast":
        return "guess", "med", "Forecast"
    if own:
        return "verified", "good", "Checked"
    return "inferred", "high", "Not checked"


def write_source(run, report, output, slug, state, claims, result, catalog_by_id, dissent):
    """Write <report>.src.html using the html-artifact decision-memo spine."""
    run, report, output = Path(run), Path(report), Path(output)
    records = {row["gate"]: read_json(run / "gates" / f"{row['gate']}.json")
               for row in result["gates"] if row["state"] == "FIRED"}
    checks = [check for gate_id, record in records.items() if catalog_by_id[gate_id]["kind"] == "required"
              for check in record["checks"]]
    verified = result["ready"] and not state.get("partial")
    recommendation = str(state.get("recommendation") or "No recommendation has been established.")
    next_action = str(state.get("next_action") or "No next action has been established.")
    counts = result["counts"]
    passed = sum(1 for c in checks if c["passed"])
    critical = sum(1 for c in claims.values() if c["critical"])
    statuses = {cid: _claim_status(cid, claim, checks) for cid, claim in claims.items()}

    out = ['<!doctype html>', '<html lang="en">', '<head>', '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           f'<meta name="artifact-id" content="solve-{escape(slug, quote=True)}">',
           '<meta name="review-label" content="Decision review">',
           f'<title>{escape(slug)} — decision</title>', '</head>', '<body>', '<header class="masthead">',
           f'<p class="eyebrow">Decision · {escape(str(state["tier"]).capitalize())} tier · {date.today().isoformat()}</p>',
           f'<h1>{escape(recommendation)}</h1>', f'<p class="lede">Next action: {escape(next_action)}</p>', '</header>',
           '<div class="page"><nav class="toc"></nav><main>']

    out += ['<section id="decision">', '<p class="eyebrow">01 · Decision</p>', '<h2>The recommendation and its status</h2>']
    if state.get("partial"):
        out.append(f'<aside class="callout" data-tone="crit"><b>Halted at budget.</b> {escape(str(state.get("halt_reason", "The declared resource budget was exhausted.")))}</aside>')
    if verified:
        out.append('<aside class="callout" data-tone="good"><b>All pre-consumer checks passed.</b> '
                   'The consumer review and the completion receipt in section 06 bind this page.</aside>')
    else:
        out.append('<aside class="callout" data-tone="crit"><b>Unverified draft.</b> '
                   'Required checks are blocked or have failed. Do not treat this page as verified.</aside>')
    out += ['<dl class="stats">',
            f'<div><dt>Critical claims</dt><dd>{critical}</dd></div>',
            f'<div data-tone="{"good" if checks and passed == len(checks) else "crit"}"><dt>Checks passed</dt><dd>{passed} / {len(checks)}</dd></div>',
            f'<div><dt>Gates fired</dt><dd>{counts["FIRED"]}</dd></div>',
            f'<div data-tone="{"crit" if counts["BLOCKED"] else "good"}"><dt>Gates blocked</dt><dd>{counts["BLOCKED"]}</dd></div>',
            '</dl>', '</section>']

    # Known knowns, known unknowns and failures, after html-effectiveness "Know your unknowns".
    out += ['<section id="claims">', '<p class="eyebrow">02 · Claims</p>', '<h2>What the decision depends on</h2>',
            '<table><thead><tr><th>Claim</th><th>Kind</th><th>Critical</th><th>Status</th><th>Consumer surface</th><th>Expected</th></tr></thead><tbody>']
    for cid, claim in claims.items():
        evidence, tone, label = statuses[cid]
        out.append(f'<tr><td><b>{escape(cid)}:</b> <span class="claim" data-evidence="{evidence}">{escape(claim["statement"])}</span></td>'
                   f'<td>{escape(claim["kind"])}</td><td>{"yes" if claim["critical"] else "no"}</td>'
                   f'<td data-tone="{tone}">{label}</td><td>{escape(claim["acceptance"]["surface"])}</td>'
                   f'<td>{escape(claim["acceptance"]["expected"])}</td></tr>')
    out += ['</tbody></table>', '</section>']

    out += ['<section id="change">', '<p class="eyebrow">03 · What would change it</p>', '<h2>Open risks, failures and forecasts</h2>']
    forecasts = [c for c in claims.values() if c["kind"] == "forecast"]
    if dissent or forecasts:
        out.append('<ul>')
        out += [f'<li data-tone="crit">{escape(line)}</li>' for line in dissent]
        out += [f'<li data-tone="med"><b>Forecast {escape(c["id"])}.</b> Assumptions: {escape(str(c["assumptions"]))}. '
                f'Follow-up: {escape(str(c["followup"]))}.</li>' for c in forecasts]
        out.append('</ul>')
    else:
        out.append('<p>The checks recorded no unresolved failure before delivery. Section 06 records the consumer review.</p>')
    out.append('</section>')

    out += ['<section id="next">', '<p class="eyebrow">04 · Next action</p>', '<h2>What to do next</h2>',
            '<ul class="checklist">',
            f'<li><label><input type="checkbox"> {escape(next_action)}</label> <span class="owner">Decision maker</span></li>',
            '</ul>', '</section>']

    out += ['<section id="evidence">', '<p class="eyebrow">05 · Evidence</p>', '<h2>Expected and observed results</h2>',
            '<table data-sortable><thead><tr><th>Gate</th><th>Claim</th><th>Result</th><th>Surface</th><th>Expected</th><th>Observed</th><th>Evidence</th></tr></thead><tbody>']
    for gate_id, record in records.items():
        if catalog_by_id[gate_id]["kind"] != "required":
            continue
        for check in record["checks"]:
            refs = ", ".join(_a(output, run / ref["path"], ref["path"]) for ref in check["evidence"])
            result_cell = '<td data-tone="good">passed</td>' if check["passed"] else '<td data-tone="crit">FAILED</td>'
            out.append(f'<tr><td>{escape(gate_id)}</td><td>{escape(check["claim"])}</td>{result_cell}'
                       f'<td>{escape(check["surface"])}</td><td>{escape(check["expected"])}</td>'
                       f'<td>{escape(check["observed"])}</td><td>{refs}</td></tr>')
    out += ['</tbody></table>', '<details><summary>Gate receipts</summary>',
            '<table data-sortable><thead><tr><th>Gate</th><th>State</th><th>Reason</th><th>Receipt</th></tr></thead><tbody>']
    tones = {"FIRED": "good", "N/A": "low", "BLOCKED": "crit"}
    for row in result["gates"]:
        path = run / "gates" / f"{row['gate']}.json"
        receipt = _a(output, path, "receipt") if path.exists() else "No receipt"
        out.append(f'<tr><td>{escape(row["gate"])}</td><td data-tone="{tones[row["state"]]}">{row["state"]}</td>'
                   f'<td>{escape(row["reason"])}</td><td>{receipt}</td></tr>')
    out += ['</tbody></table>', '</details>', '</section>']

    out += ['<section id="verification">', '<p class="eyebrow">06 · Verification</p>', '<h2>How this page is bound</h2>',
            f'<p>This page is a view of {_a(output, report, "the Markdown report")}. '
            'The consumer review checks both files, and the completion receipt binds their SHA-256 hashes.</p>',
            '<ul>', f'<li>{_a(output, run / "request.md", "Original request")}</li>',
            f'<li>{_a(output, run / "gates/consumer.json", "Consumer gate receipt")}</li>',
            f'<li>{_a(output, run / "completion.json", "Completion receipt")}</li>', '</ul>',
            '<p>A comment sent from this page changes nothing by itself. A change to the decision needs a new render and a new consumer review.</p>',
            '</section>', '</main></div>', '</body>', '</html>', '']
    source = output.with_name(output.stem + ".src.html")
    source.write_text("\n".join(out), encoding="utf-8")
    return source


def build(source, output, verify=True):
    """Run html-artifact's build (lint, inline components, headless verify)."""
    skill = locate_html_artifact()
    command = ["node", str(skill / BUILD_SCRIPT), str(source), str(output)] + (["--verify"] if verify else [])
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=BUILD_TIMEOUT_SECONDS, check=False)
    except FileNotFoundError as exc:
        raise ContractError("the HTML view needs Node.js on PATH") from exc
    except subprocess.TimeoutExpired as exc:
        raise ContractError(f"html-artifact build exceeded {BUILD_TIMEOUT_SECONDS}s") from exc
    log = (done.stdout + done.stderr).strip()
    require(done.returncode == 0, f"html-artifact build failed (exit {done.returncode}):\n{log}")
    require(Path(output).is_file(), f"html-artifact build wrote no file at {output}")
    return {"path": str(Path(output).resolve()), "sha256": file_hash(output)}, log, str(skill)
