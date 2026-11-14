# Plugin validation record

Date: 2026-11-13
Package: Solve 0.1.1, based on Solve runtime 2.1.0.

## Completed checks

| Check | Observed result |
|---|---|
| `python3 -m unittest discover -s tests` | 139 tests discovered; 136 passed, 3 skipped |
| `env -u CODEX_HOME SOLVE_SKIP_LIVE_CODEX_TEST=1 tests/test_port.sh` | Passed isolated installer, launcher, adaptive package, and helper checks; live Codex discovery explicitly skipped |
| Package build and archive inspection | Passed manifest/YAML parsing, component and license checks, local instruction links, file hashes, safe paths, and archive layout |
| Deterministic package regression | Same source entries produce identical archive bytes |
| `git diff --check` | Passed |
| Fresh-agent writing trial | Preserved numbers, units, modality, cohort restriction, retry exception, identifiers, and unresolved rollback; removed promotional filler |
| Fresh-agent artifact trial | Produced an incident HTML page and editable JSON; static verification passed; independent content review found no preservation error |

The writing trial used a synthetic pilot statement with 24 requests, an uncertain
18% latency improvement, cohort B, 3 retries and 2 authorized extra attempts.
The artifact trial used synthetic incident facts with a database deploy and an
import-worker pause. It preserved the competing explanation, missing impact
measurement, unassigned owner, and absence of causal proof. These two trials
are qualitative workflow checks, not a measured model benchmark.

## Checks that did not complete

- The three optional Python skips cover live browser execution and the absent
  legacy HTML dependency. No downloaded legacy dependency is included.
- Chromium was actually launched for browser verification but stopped before
  rendering: the environment denied its socket operation. An attempt to run
  outside the sandbox was automatically rejected. No visual, dark-mode, or
  browser interaction success is claimed.
- The live Codex prompt-discovery check failed in this environment. A direct
  probe returned a read-only filesystem error. The isolated port test was then
  run with its explicit live-discovery skip; that skip is not an integration pass.
- Vale and Harper were absent. The offline helper explicitly reported both as
  skipped. Manual semantic review ran; automated prose-lint success is not claimed.

## What this establishes

The package can be assembled and its bundled commands can produce a standalone
artifact without runtime downloads. Tests cover escaped content, unsafe URLs,
credential-shaped content, source/output preservation, evidence traversal,
blocked/failed decision status, and invalidation after a reviewed view changes.

The entry file contains 593 whitespace-delimited words, compared with 1,659 in
the original entry file. Conditional references remain in the bundle. This is
a smaller entry point, not a measurement of total token savings or latency.

The 14-case public synthetic decision benchmark is bundled but no baseline-vs-
plugin model comparison was run. Nothing here establishes the smartest possible
decisions, improved strategic success, or lower model cost. Measure those claims
under equal model/settings and on fresh tasks before making them.
