"""Render only from the same gate validator used by finalization."""

import argparse
import json
import os
from pathlib import Path
import sys
import time
from urllib.parse import quote

from solve_contract import (ContractError, PROFILES, atomic_write, catalog, completion_valid,
                            decision_digest, evaluate, file_hash, load_run, read_json,
                            read_object, require, run_lock, update_state, write_json)
import solve_html


def link(output, target, label):
    relative = os.path.relpath(Path(target).resolve(), Path(output).resolve().parent)
    return f"[{label}]({quote(relative, safe='/.-_')})"


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_report(run, output, slug, fmt="pyramid", html=False):
    require(fmt in ("pyramid", "build-up", "tldr"), "format must be pyramid, build-up, or tldr")
    run, output = Path(run), Path(output).resolve()
    require(output.suffix == ".md", "report output must be a Markdown file")
    require(run.resolve() not in output.parents or output == run.resolve() / "report.md",
            "inside the run, use report.md so rendering cannot overwrite inputs or evidence")
    with run_lock(run):
        try:
            state, claims, _ = load_run(run)
        except ContractError as exc:
            body = f"# Unverified solve report: {slug}\n\n{exc}\n\n"
            body += "Existing files are preserved. This legacy or incomplete run has no verified gate contract.\n"
            try:
                state = read_object(run / "state.json")
                if state.get("partial"):
                    body += f"\n## Halted At Budget\n\n{state.get('halt_reason', 'Resource budget exhausted.')}\n\n"
                    body += "Decision claims remain unverified. Resume intake with an explicitly renewed budget.\n"
            except ContractError:
                pass
            atomic_write(output, body.encode())
            return {"output": str(output), "verified": False, "reason": str(exc)}
        if state.get("format") != fmt:
            update_state(run, {"format": fmt})
            state["format"] = fmt
        result = evaluate(run, include_consumer=False)
        catalog_by_id = catalog()
        header = [f"# Decision report: {slug}", "", f"**Tier:** {state['tier']} (adaptive)",
                  f"**Original request:** {link(output, run / 'request.md', 'request.md')}", ""]
        if state.get("partial") or not result["ready"]:
            header.extend(["**Unverified draft.** Required checks are blocked or have failed. Do not treat this report as verified.", ""])
        if state.get("partial"):
            header.extend(["## Halted At Budget", "", state.get("halt_reason", "The declared resource budget was exhausted."),
                           "Resume the same run with an explicitly renewed budget and finish the blocked checks.", ""])
        decision = ["## Decision", "", str(state.get("recommendation") or "No recommendation has been established."), ""]
        decision.extend(["## Next action", "", str(state.get("next_action") or "No next action has been established."), ""])
        if fmt == "tldr":
            tldr = state.get("tldr", [])
            if isinstance(tldr, str):
                tldr = [tldr]
            decision = ["## TL;DR", "", *[f"- {line}" for line in tldr], "", *decision]
        claim_lines = ["## Claims and acceptance", "", "| Claim | Kind | Critical | Consumer surface | Expected observation |",
                       "|---|---|---|---|---|"]
        forecast_notes = []
        for claim in claims.values():
            claim_lines.append(f"| {cell(claim['id'])}: {cell(claim['statement'])} | {claim['kind']} | {'yes' if claim['critical'] else 'no'} | {cell(claim['acceptance']['surface'])} | {cell(claim['acceptance']['expected'])} |")
            if claim["kind"] == "forecast":
                forecast_notes.extend(["", f"**Forecast {claim['id']}:** Assumptions: {claim['assumptions']}. Follow-up: {claim['followup']}."])
        claim_lines.extend(["", *forecast_notes, ""])
        evidence = ["## Evidence and uncertainty", "", "Gate execution is not a vote. FIRED records can contain failed checks. Forecasts remain forecasts.", ""]
        dissent = []
        for row in result["gates"]:
            if row["state"] == "FIRED":
                record = read_json(run / "gates" / f"{row['gate']}.json")
                if catalog_by_id[row["gate"]]["kind"] == "required":
                    evidence.append(f"**{row['gate'].capitalize()}**: {link(output, run / record['artifact']['path'], 'review artifact')}")
                    for check in record["checks"]:
                        refs = ", ".join(link(output, run / ref["path"], ref["path"]) for ref in check["evidence"])
                        evidence.append(f"- {check['claim']}: {'passed' if check['passed'] else 'FAILED'} at {check['surface']}. Expected: {check['expected']}. Observed: {check['observed']}. Evidence: {refs}.")
                for check in record["checks"]:
                    if not check["passed"]:
                        dissent.append(f"{row['gate']} / {check['claim']}: {check['observed']}")
                if "coverage" in record and not record["coverage"]["complete"]:
                    dissent.append(f"{row['gate']}: {record['coverage']['reason']}")
            elif row["state"] == "BLOCKED":
                dissent.append(f"{row['gate']}: {row['reason']}. Unverified: {', '.join(row.get('unverified', []))}.")
        dissent.extend(result["failures"])
        dissent = list(dict.fromkeys(dissent))
        evidence.extend(["", "## Dissent and unverified claims", "", *([f"- {line}" for line in dissent] or ["No unresolved failure was recorded by the checks before delivery. Consumer verification is recorded separately below."]), ""])
        receipts = ["## Gate receipts", "", "| Gate | State | Reason | Receipt |", "|---|---|---|---|"]
        for row in result["gates"]:
            path = run / "gates" / f"{row['gate']}.json"
            receipt_link = link(output, path, "receipt") if path.exists() else "No receipt"
            receipts.append(f"| {row['gate']} | {row['state']} | {cell(row['reason'])} | {receipt_link} |")
        methods = ["", "## Applied methods", ""]
        for row in result["gates"]:
            if row["state"] == "FIRED" and catalog_by_id[row["gate"]]["kind"] == "framework":
                record = read_json(run / "gates" / f"{row['gate']}.json")
                methods.append(f"- {link(output, run / record['artifact']['path'], row['gate'])}: {row['reason']}")
        if len(methods) == 3:
            methods.append("No optional framework was needed.")
        consumer = ["", "## Verification of this delivered report", "",
                    "The consumer review checks this exact report and each declared acceptance surface. It also checks whether material claims are missing from the ledger.",
                    "Rendering alone establishes no completion. A current completion receipt binds this report's path and SHA-256 to the decision and consumer review.",
                    f"- {link(output, run / 'gates/consumer.json', 'Consumer gate receipt')}",
                    f"- {link(output, run / 'completion.json', 'Completion receipt')}",
                    "Changing the report, its decision inputs, or referenced evidence invalidates that verification. Use `bin/gates validate` to check freshness.", ""]
        blocks = [header, evidence, claim_lines, decision] if fmt == "build-up" else [header, decision, claim_lines, evidence]
        body = "\n".join(line for block in [*blocks, receipts, methods, consumer] for line in block)
        atomic_write(output, body.encode())
        subject = {"path": str(output), "sha256": file_hash(output)}
        extra = {}
        if html:
            # The HTML view joins the subject, so the consumer and completion bind both files.
            page = output.with_suffix(".html")
            source = solve_html.write_source(run, output, page, slug, state, claims, result, catalog_by_id, dissent)
            view, log, skill = solve_html.build(source, page)
            subject["views"] = [view]
            extra = {"html": {"source": str(source), "html_artifact": skill, "build_log": log}}
        rendered = {"subject": subject, "decision_digest": decision_digest(run)}
        write_json(run / "render.json", rendered)
        return {"output": str(output), "pre_consumer_ready": result["ready"], "verified": False, **rendered, **extra}


def progress(run, plain=False):
    result = evaluate(run)
    result["complete"] = completion_valid(run, result)
    counts = result["counts"]
    summary = f"FIRED {counts['FIRED']} | N/A {counts['N/A']} | BLOCKED {counts['BLOCKED']}"
    outcome = "verified completion" if result["complete"] else "unverified"
    if result["failures"]:
        outcome += f"; {len(result['failures'])} failed check(s) or run obstruction(s)"
    if plain:
        return f"[{summary}] {outcome}"
    lines = [f"solve: {Path(run).name}", summary, outcome]
    for row in result["gates"]:
        if row["state"] == "BLOCKED":
            lines.append(f"  BLOCKED {row['gate']}: {row['reason']}")
    lines.extend(f"  {failure}" for failure in result["failures"])
    try:
        status = read_object(Path(run) / "state.json").get("budget_status", {})
        require(isinstance(status, dict), "budget status must be an object")
        lines.append(f"Time: {status.get('time_used', 0)}s | External spend: ${status.get('tokens_used', 0):.2f}")
    except (ContractError, TypeError, ValueError):
        pass
    return "\n".join(lines)


def tier_main(argv):
    if not argv or argv[0] in ("help", "-h", "--help"):
        print("tier quick|standard|deep [--json] | defaults <tier> | list\nTiers set budgets and evidence depth. There are no fixed framework counts.")
        return 0
    if argv[0] == "list":
        for name, profile in PROFILES.items():
            print(f"{name}: {profile['evidence_depth']}, {profile['time_seconds'] // 60}m, ${profile['tokens_usd']}; adaptive methods")
        return 0
    if argv[0] == "defaults":
        require(len(argv) == 2 and argv[1] in PROFILES, "defaults requires quick, standard, or deep")
        profile = PROFILES[argv[1]]
        print(profile["time_seconds"], profile["tokens_usd"])
        return 0
    require(argv[0] in PROFILES, "unknown tier")
    require(len(argv) == 1 or argv[1:] == ["--json"], "fixed framework lists/counts were retired; use bin/gates catalog and inspect")
    print(json.dumps({"tier": argv[0], **PROFILES[argv[0]], "selection": "adaptive", "required_checks": ["evidence", "refutation", "consumer"]}))
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        if args and args[0] == "tier":
            return tier_main(args[1:])
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command", required=True)
        p = sub.add_parser("progress")
        p.add_argument("--run-dir", default=os.environ.get("RUN_DIR") or os.environ.get("SOLVE_RUN_DIR"))
        p.add_argument("--plain", action="store_true")
        p.add_argument("--watch", action="store_true")
        p.add_argument("--no-color", action="store_true")
        p.add_argument("--width", type=int, default=20)
        p = sub.add_parser("render")
        p.add_argument("--run-dir", required=True)
        p.add_argument("--slug", required=True)
        p.add_argument("--format", default="pyramid")
        p.add_argument("--output", required=True)
        p.add_argument("--html", action="store_true", help="also build a reviewable HTML view with html-artifact")
        parsed = parser.parse_args(args)
        if parsed.command == "render":
            print(json.dumps(render_report(parsed.run_dir, parsed.output, parsed.slug, parsed.format, parsed.html), indent=2))
        else:
            require(parsed.run_dir and Path(parsed.run_dir).is_dir(), "pass an existing --run-dir")
            require(parsed.width > 0, "--width must be positive")
            while True:
                if parsed.watch and sys.stdout.isatty():
                    print("\033[H\033[2J", end="")
                print(progress(parsed.run_dir, parsed.plain), flush=True)
                if not parsed.watch:
                    break
                time.sleep(2)
        return 0
    except (ContractError, OSError, TypeError, KeyError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
