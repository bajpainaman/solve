#!/usr/bin/env bash
# Isolated smoke test for the Codex installer, launcher, and core helpers.

set -euo pipefail

ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
TEST_TMP=$(mktemp -d "${TMPDIR:-/tmp}/solve-codex-test.XXXXXX")

cleanup() {
  case "$TEST_TMP" in
    "${TMPDIR:-/tmp}"/solve-codex-test.*)
      [ ! -d "$TEST_TMP" ] || rm -rf -- "$TEST_TMP"
      ;;
    *)
      printf 'refusing to clean unexpected test path: %s\n' "$TEST_TMP" >&2
      ;;
  esac
}
trap cleanup EXIT

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_file() {
  [ -f "$1" ] || fail "missing file: $1"
}

assert_line() {
  local expected=$1 file=$2
  grep -Fqx -- "$expected" "$file" || fail "expected line '$expected' in $file"
}

mkdir -p "$TEST_TMP/bin" "$TEST_TMP/home"

cat > "$TEST_TMP/bin/codex" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  --version)
    echo "codex-cli 999.0.0-test"
    ;;
  features)
    [ "${2:-}" = "list" ] || exit 2
    echo "multi_agent stable true"
    ;;
  *)
    : "${CODEX_STUB_CAPTURE:?CODEX_STUB_CAPTURE must be set for launch tests}"
    printf '%s\n' "$#" > "$CODEX_STUB_CAPTURE.count"
    printf '%s\n' "$@" > "$CODEX_STUB_CAPTURE.args"
    {
      printf 'tier=%s\n' "${SOLVE_PRESEED_TIER:-}"
      printf 'time=%s\n' "${SOLVE_PRESEED_TIME:-}"
      printf 'spend=%s\n' "${SOLVE_PRESEED_SPEND:-}"
      printf 'tokens=%s\n' "${SOLVE_PRESEED_TOKENS:-}"
      printf 'root=%s\n' "${SOLVE_SKILL_ROOT:-}"
    } > "$CODEX_STUB_CAPTURE.env"
    ;;
esac
STUB
chmod +x "$TEST_TMP/bin/codex"

HOME="$TEST_TMP/home" \
PATH="$TEST_TMP/bin:$PATH" \
CODEX_BIN=codex \
SOLVE_SKILL_DEST="$TEST_TMP/home/.agents/skills/solve" \
SOLVE_SHIM_DIR="$TEST_TMP/bin" \
SOLVE_INSTALL_NONINTERACTIVE=1 \
SOLVE_SKIP_HTML_SYNC=1 \
  "$ROOT/install" > "$TEST_TMP/install.log"

[ -L "$TEST_TMP/home/.agents/skills/solve" ] || fail "installer did not create the Codex skill symlink"
[ "$(readlink -f "$TEST_TMP/home/.agents/skills/solve")" = "$ROOT" ] || fail "skill symlink points to the wrong source"
assert_file "$TEST_TMP/bin/solve"
[ ! -e "$TEST_TMP/home/.claude" ] || fail "installer created legacy Claude configuration"
[ ! -e "$TEST_TMP/home/.codex/config.toml" ] || fail "installer changed Codex configuration"

HOME="$TEST_TMP/home" \
PATH="$TEST_TMP/bin:$PATH" \
CODEX_BIN=codex \
SOLVE_SKILL_DEST="$TEST_TMP/home/.agents/skills/solve" \
SOLVE_SHIM_DIR="$TEST_TMP/bin" \
SOLVE_INSTALL_NONINTERACTIVE=1 \
SOLVE_SKIP_HTML_SYNC=1 \
  "$ROOT/install" > "$TEST_TMP/install-second.log"
if compgen -G "$TEST_TMP/home/.agents/skills/solve.bak.*" >/dev/null; then
  fail "idempotent install created an unnecessary skill backup"
fi

CAPTURE="$TEST_TMP/launch"
HOME="$TEST_TMP/home" \
PATH="$TEST_TMP/bin:$PATH" \
CODEX_BIN=codex \
CODEX_STUB_CAPTURE="$CAPTURE" \
  "$TEST_TMP/bin/solve" --tier quick --budget time=15min spend=2 "should we migrate?"

assert_line "1" "$CAPTURE.count"
assert_line '$solve should we migrate?' "$CAPTURE.args"
assert_line "tier=quick" "$CAPTURE.env"
assert_line "time=900" "$CAPTURE.env"
assert_line "spend=2" "$CAPTURE.env"
assert_line "tokens=2" "$CAPTURE.env"
assert_line "root=$TEST_TMP/home/.agents/skills/solve" "$CAPTURE.env"

HOME="$TEST_TMP/home" \
PATH="$TEST_TMP/bin:$PATH" \
CODEX_BIN=codex \
  "$TEST_TMP/bin/solve" --status > "$TEST_TMP/status.log"
grep -Fq "skill version:    2.1.0" "$TEST_TMP/status.log" || fail "status omitted skill version"
grep -Fq "subagents:        enabled" "$TEST_TMP/status.log" || fail "status did not detect subagents"

REAL_CODEX=$(command -v codex 2>/dev/null || true)
if [ "${SOLVE_SKIP_LIVE_CODEX_TEST:-0}" = "1" ]; then
  printf 'SKIPPED: live Codex discovery (SOLVE_SKIP_LIVE_CODEX_TEST=1); isolated launcher checks still run\n'
elif [ -n "$REAL_CODEX" ] && [ "$REAL_CODEX" != "$TEST_TMP/bin/codex" ]; then
  env -u CODEX_HOME HOME="$TEST_TMP/home" \
    "$REAL_CODEX" debug prompt-input '$solve discovery smoke test' \
    > "$TEST_TMP/prompt-input.json" 2>/dev/null
  grep -Fq -- '- solve: One skill for decisions, clear writing and reviewable HTML pages' "$TEST_TMP/prompt-input.json" || fail "real Codex did not discover the installed skill"
grep -Fq -- '$solve discovery smoke test' "$TEST_TMP/prompt-input.json" || fail "real Codex did not retain the explicit invocation"
fi

COPY_HOME="$TEST_TMP/copy-home"
mkdir -p "$COPY_HOME/.local/bin"
printf 'export USER_SETTING=preserved\n' > "$COPY_HOME/.bashrc"
printf '#!/usr/bin/env bash\necho unrelated launcher\n' > "$COPY_HOME/.local/bin/solve"
chmod +x "$COPY_HOME/.local/bin/solve"
HOME="$COPY_HOME" \
PATH="$TEST_TMP/bin:$PATH" \
CODEX_BIN=codex \
SOLVE_INSTALL_MODE=copy \
SOLVE_INSTALL_NONINTERACTIVE=1 \
SOLVE_SKIP_HTML_SYNC=1 \
  "$ROOT/install" > "$TEST_TMP/install-copy.log"
[ -d "$COPY_HOME/.agents/skills/solve" ] || fail "copy-mode skill directory missing"
[ ! -L "$COPY_HOME/.agents/skills/solve" ] || fail "copy mode created a symlink"
[ "$(grep -Fc '# solve-cli >>>' "$COPY_HOME/.bashrc")" = "1" ] || fail "PATH block was not written exactly once"
grep -Fq 'export USER_SETTING=preserved' "$COPY_HOME/.bashrc" || fail "installer changed an existing shell setting"
shopt -s nullglob
SHIM_BACKUPS=("$COPY_HOME"/.local/bin/solve.bak.*)
shopt -u nullglob
[ ${#SHIM_BACKUPS[@]} -eq 1 ] || fail "installer did not preserve a pre-existing launcher"
grep -Fq 'unrelated launcher' "${SHIM_BACKUPS[0]}" || fail "launcher backup did not preserve its original content"

HOME="$COPY_HOME" SOLVE_SHIM_DIR="$COPY_HOME/.local/bin" \
  "$COPY_HOME/.local/bin/solve" --uninstall > "$TEST_TMP/uninstall-copy.log"
[ ! -e "$COPY_HOME/.agents/skills/solve" ] || fail "uninstall left the copied skill active"
[ ! -e "$COPY_HOME/.local/bin/solve" ] || fail "uninstall left the launcher active"
shopt -s nullglob
COPY_ARCHIVES=("$COPY_HOME"/.agents/skills/solve.uninstalled.*)
shopt -u nullglob
[ ${#COPY_ARCHIVES[@]} -eq 1 ] || fail "copied skill was not preserved in one recoverable archive"
[ "$(grep -Fc '# solve-cli >>>' "$COPY_HOME/.bashrc")" = "0" ] || fail "uninstall left the PATH block"
grep -Fq 'export USER_SETTING=preserved' "$COPY_HOME/.bashrc" || fail "uninstall removed an existing shell setting"

DISABLED_HOME="$TEST_TMP/disabled-home"
mkdir -p "$DISABLED_HOME/.codex"
printf '[agents]\nenabled = false\n' > "$DISABLED_HOME/.codex/config.toml"
if HOME="$DISABLED_HOME" \
   PATH="$TEST_TMP/bin:$PATH" \
   CODEX_BIN=codex \
   SOLVE_INSTALL_NONINTERACTIVE=1 \
   SOLVE_SKIP_HTML_SYNC=1 \
   "$ROOT/install" > "$TEST_TMP/install-disabled.log" 2>&1; then
  fail "installer ignored agents.enabled=false"
fi
grep -Fq 'agents.enabled=false' "$TEST_TMP/install-disabled.log" || fail "disabled-agent error lacked remediation"
[ ! -e "$DISABLED_HOME/.agents/skills/solve" ] || fail "installer wrote the skill after a disabled-agent failure"

python3 - "$ROOT" <<'PY_TEST'
from pathlib import Path
import json
import subprocess
import sys

root = Path(sys.argv[1])
for name, seconds, spend in (("quick", 900, 2), ("standard", 1800, 5), ("deep", 3600, 15)):
    profile = json.loads(subprocess.check_output([root / "bin/tier", name, "--json"], text=True))
    assert profile["selection"] == "adaptive"
    assert profile["time_seconds"] == seconds and profile["tokens_usd"] == spend
    assert profile["required_checks"] == ["evidence", "refutation", "consumer"]
    assert "total" not in profile and "counts" not in profile
    assert subprocess.run([root / "bin/tier", name, "--count"], capture_output=True).returncode == 2

catalog = json.loads((root / "gates/catalog.json").read_text())
assert catalog["states"] == ["FIRED", "N/A", "BLOCKED"]
frameworks = [g for g in catalog["gates"] if g["kind"] == "framework"]
assert len(frameworks) == 25
assert {g["id"] for g in frameworks} == {p.stem for p in (root / "frameworks").glob("*.md") if p.stem != "_TEMPLATE"}
for gate in frameworks:
    card = root / gate["method"]
    assert card.stat().st_size <= 4096, f"method card too large: {card}"
    text = card.read_text()
    for heading in ("Entry Predicate", "Method", "Output Schema", "Decision Hook"):
        assert "## " + heading in text
    assert (root / "references/deep" / card.name).is_file(), "deep reference was not preserved"
    assert gate["trigger"] in text
bootstrap = ["SKILL.md", "references/runtime.md", "references/roles.md", "references/confidence.md", "gates/catalog.json"]
assert sum((root / name).stat().st_size for name in bootstrap) < 40000, "bootstrap instructions exceeded the restraint budget"
metadata = (root / "agents/openai.yaml").read_text()
assert 'display_name: "Solve"' in metadata
assert 'default_prompt: "Use $solve ' in metadata
assert (root / "VERSION").read_text().strip() == "2.1.0"
PY_TEST

RUN_DIR="$TEST_TMP/run"
mkdir -p "$RUN_DIR/frameworks"
"$ROOT/bin/state-rw" init "$RUN_DIR" test-decision "Test decision"
"$ROOT/bin/state-rw" write "$RUN_DIR" tier '"quick"' >/dev/null
"$ROOT/bin/state-rw" write "$RUN_DIR" budget '{"time_seconds":900,"tokens_usd":2}' >/dev/null
for index in $(seq 1 12); do
  "$ROOT/bin/state-rw" write "$RUN_DIR" "concurrent_$index" "$index" >/dev/null &
done
wait
python3 - "$RUN_DIR/state.json" <<'PY'
import json
import sys

with open(sys.argv[1]) as handle:
    state = json.load(handle)
for index in range(1, 13):
    assert state[f"concurrent_{index}"] == index
PY
printf '# First principles\n' > "$RUN_DIR/frameworks/first-principles.md"
printf '# Issue tree\n' > "$RUN_DIR/frameworks/issue-tree.md"
printf '%s\n' '{"framework":"issue-tree","attacks":["root may be too narrow"],"score":7}' > "$RUN_DIR/adversary.jsonl"
printf '%s\n' '{"skill":"investigate","phase":"define","reason":"component failure surfaced"}' > "$RUN_DIR/handoffs.jsonl"

"$ROOT/bin/progress" --run-dir "$RUN_DIR" --plain --no-color > "$TEST_TMP/progress.log"
grep -Fq 'FIRED 0 | N/A 0 | BLOCKED 28' "$TEST_TMP/progress.log" || fail "legacy files were incorrectly counted as verified gates"

FLOAT_START=$("$ROOT/bin/state-rw" read "$RUN_DIR" started_at)
TEL_START="$FLOAT_START" SOLVE_COST_FILE="$RUN_DIR/cost-usd" \
  "$ROOT/bin/budget-track" --check time --run-dir "$RUN_DIR" >/dev/null

"$ROOT/bin/render-report" \
  --slug test-decision \
  --format pyramid \
  --run-dir "$RUN_DIR" \
  --output "$TEST_TMP/report.md" >/dev/null
grep -Fq 'Unverified solve report' "$TEST_TMP/report.md" || fail "legacy report was not labeled unverified"
if "$ROOT/bin/gates" finalize --run-dir "$RUN_DIR" >/dev/null 2>&1; then
  fail "legacy run finalized without verification"
fi

# The Python suite exercises complete adaptive rendering, consumer review, and
# budget-halting flows; this shell suite retains legacy compatibility coverage.

mkdir -p "$TEST_TMP/research"
cat > "$TEST_TMP/queries.json" <<'JSON'
[
  {"id":"q1","objective":"find comparable migrations\nincluding failed cases","search_queries":["comparable migrations"]},
  {"id":"q2","objective":"find failure base rates","search_queries":["migration failure rates"]}
]
JSON
HOME="$TEST_TMP/home" PARALLEL_API_KEY='' \
  "$ROOT/bin/parallel-research" "$TEST_TMP/queries.json" "$TEST_TMP/research" > "$TEST_TMP/research.log"
python3 - "$TEST_TMP/research/manifest.json" <<'PY'
import json
import sys

with open(sys.argv[1]) as handle:
    manifest = json.load(handle)
assert manifest["count"] == 2
assert {item["backend"] for item in manifest["queries"]} == {"websearch-fallback"}
PY

printf '%s\n' '[{"id":"../escape","objective":"must not escape output"}]' > "$TEST_TMP/bad-queries.json"
if HOME="$TEST_TMP/home" PARALLEL_API_KEY='' \
   "$ROOT/bin/parallel-research" "$TEST_TMP/bad-queries.json" "$TEST_TMP/research" >/dev/null 2>&1; then
  fail "parallel research accepted a path-like query id"
fi
[ ! -e "$TEST_TMP/escape.json" ] || fail "parallel research wrote outside its output directory"

mkdir -p "$TEST_TMP/parallel-bin"
cat > "$TEST_TMP/parallel-bin/curl" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail

args="$*"
if [[ "$args" == *"%{http_code}"* ]]; then
  printf '%s' "${MOCK_HTTP_CODE:-404}"
elif [[ "$args" == *"/result"* ]]; then
  printf '%s\n' '{"run":{"run_id":"trun_test","status":"completed"},"output":{"summary":"mock result","key_findings":[],"sources":[]}}'
elif [[ "$args" == *"/v1/tasks/runs/trun_test"* ]]; then
  printf '%s\n' '{"run_id":"trun_test","status":"completed"}'
elif [[ "$args" == *"-X POST"* && "$args" == *"/v1/tasks/runs"* ]]; then
  [[ "$args" == *'"processor": "base"'* ]] || exit 22
  printf '%s\n' '{"run_id":"trun_test","status":"queued"}'
else
  exit 22
fi
STUB
chmod +x "$TEST_TMP/parallel-bin/curl"

MOCK_KEY="parallel_test_key_0000000000000000"
HOME="$TEST_TMP/home" PATH="$TEST_TMP/parallel-bin:$PATH" \
PARALLEL_API_KEY="$MOCK_KEY" MOCK_HTTP_CODE=404 \
  "$ROOT/bin/parallel-setup" --check > "$TEST_TMP/parallel-check.log"
grep -Fq 'STATUS: ok' "$TEST_TMP/parallel-check.log" || fail "Parallel setup rejected an authenticated 404 probe"

if HOME="$TEST_TMP/home" PATH="$TEST_TMP/parallel-bin:$PATH" \
   PARALLEL_API_KEY="$MOCK_KEY" MOCK_HTTP_CODE=401 \
   "$ROOT/bin/parallel-setup" --check > "$TEST_TMP/parallel-check-invalid.log" 2>&1; then
  fail "Parallel setup accepted a 401 probe"
else
  [ "$?" = "2" ] || fail "Parallel setup returned the wrong invalid-key status"
fi

printf '%s\n' '[{"id":"paid","objective":"run one mocked paid query"}]' > "$TEST_TMP/paid-queries.json"
PAID_COST_FILE="$TEST_TMP/paid-cost"
mkdir -p "$TEST_TMP/paid-research"
HOME="$TEST_TMP/home" PATH="$TEST_TMP/parallel-bin:$PATH" \
PARALLEL_API_KEY="$MOCK_KEY" MOCK_HTTP_CODE=404 \
SOLVE_COST_FILE="$PAID_COST_FILE" SOLVE_EXTERNAL_SPEND_CAP=unlimited \
  "$ROOT/bin/parallel-research" "$TEST_TMP/paid-queries.json" "$TEST_TMP/paid-research" \
  > "$TEST_TMP/paid-research.log"
[ "$(tr -d '[:space:]' < "$PAID_COST_FILE")" = "0.0100" ] || fail "Parallel base-run cost was not tracked at the current rate"
python3 - "$TEST_TMP/paid-research/manifest.json" <<'PY'
import json
import sys

with open(sys.argv[1]) as handle:
    manifest = json.load(handle)
assert manifest["count"] == 1
assert manifest["queries"][0]["backend"] == "parallel.ai"
assert manifest["queries"][0]["run_id"] == "trun_test"
PY

mkdir -p "$TEST_TMP/capped-research"
HOME="$TEST_TMP/home" PATH="$TEST_TMP/parallel-bin:$PATH" \
PARALLEL_API_KEY="$MOCK_KEY" MOCK_HTTP_CODE=404 \
SOLVE_COST_FILE="$TEST_TMP/capped-cost" SOLVE_EXTERNAL_SPEND_CAP=0 \
  "$ROOT/bin/parallel-research" "$TEST_TMP/paid-queries.json" "$TEST_TMP/capped-research" \
  > "$TEST_TMP/capped-research.log" 2>&1
grep -Fq 'projected spend' "$TEST_TMP/capped-research.log" || fail "Parallel fan-out did not report its spend-cap fallback"
grep -Fq 'websearch-fallback' "$TEST_TMP/capped-research/paid.json" || fail "Parallel fan-out exceeded a zero spend cap"
[ "$(tr -d '[:space:]' < "$TEST_TMP/capped-cost")" = "0" ] || fail "capped Parallel fan-out recorded paid spend"

COST_FILE="$TEST_TMP/concurrent-cost"
for _ in $(seq 1 20); do
  SOLVE_COST_FILE="$COST_FILE" "$ROOT/bin/cost-track" 0.05 >/dev/null &
done
wait
[ "$(tr -d '[:space:]' < "$COST_FILE")" = "1.0000" ] || fail "concurrent spend updates were lost"

ZERO_RUN="$TEST_TMP/zero-spend-run"
"$ROOT/bin/state-rw" init "$ZERO_RUN" zero-spend "No paid research"
"$ROOT/bin/state-rw" write "$ZERO_RUN" budget '{"time_seconds":null,"tokens_usd":0}' >/dev/null
printf '0\n' > "$ZERO_RUN/cost-usd"
SOLVE_COST_FILE="$ZERO_RUN/cost-usd" "$ROOT/bin/budget-track" --check both --run-dir "$ZERO_RUN" >/dev/null
printf '0.01\n' > "$ZERO_RUN/cost-usd"
if SOLVE_COST_FILE="$ZERO_RUN/cost-usd" "$ROOT/bin/budget-track" --check both --run-dir "$ZERO_RUN" >/dev/null; then
  fail "zero external-spend cap allowed a paid call"
else
  [ "$?" = "2" ] || fail "zero external-spend cap returned the wrong halt code"
fi

CALIB_DIR="$TEST_TMP/calibration"
SOLVE_CALIB_LEDGER="$CALIB_DIR/ledger.jsonl" SOLVE_CALIB_CONFIG="$CALIB_DIR/config.json" \
  "$ROOT/bin/calibration" log demo run-1 HIGH 8 0.80 "ship it" >/dev/null
SOLVE_CALIB_LEDGER="$CALIB_DIR/ledger.jsonl" SOLVE_CALIB_CONFIG="$CALIB_DIR/config.json" \
  "$ROOT/bin/calibration" log-outcome demo success >/dev/null
SOLVE_CALIB_LEDGER="$CALIB_DIR/ledger.jsonl" SOLVE_CALIB_CONFIG="$CALIB_DIR/config.json" \
  "$ROOT/bin/calibration" status > "$TEST_TMP/calibration.log"
grep -Fq '"high_success_rate_pct": 100.0' "$TEST_TMP/calibration.log" || fail "calibration ledger did not round-trip"

printf 'PASS: Codex installation, adaptive package, and helper smoke test\n'
