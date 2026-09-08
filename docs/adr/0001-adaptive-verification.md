# Adaptive verification for solve

Date: 2026-09-07
Status: Accepted direction; implementation details recorded here

The user approved replacing fixed framework counts with adaptive selection,
three gate states, independent refutation, and verification through the consumer.
This is a breaking run-contract change targeting 2.0.0.

## Decisions

- Quick, Standard, and Deep specify time, external spend, and evidence depth.
  They never excuse an applicable check or promise a framework count.
- Keep 25 compact method cards. Preserve the existing long explanations as
  optional deep references. Read a card only after its written trigger fires;
  read an individual deep section only to answer a named unresolved question.
- The catalog owns each trigger. Applicability facts carry observations and
  hashed evidence. A false fact permits N/A; an unknown or unsupported fact
  leaves the gate BLOCKED. Silence in an intake is not evidence of absence.
- Every gate has exactly one of FIRED, N/A, or BLOCKED. FIRED means a check ran,
  not that its result was favorable. There is no DONE, skipped, or waived gate.
- A FIRED record names an artifact, affected claims, and checks with expected
  and observed results, a named surface, a Boolean outcome, and hashed evidence.
  N/A quotes the catalog trigger and explains the false evaluation. BLOCKED
  names the obstruction and what remains unverified. Invalid, missing, or stale
  receipts are reported as BLOCKED by the consumer of the ledger.
- Define critical claims before relying on them. Each has an explicit acceptance
  surface and expectation. Facts, forecasts, and preferences are distinguished.
  Forecast checks establish visible assumptions and limits, never future truth.
- Evidence, independent refutation, and consumer verification are required in
  every decision run. Frameworks are optional methods, not substitutes for these.
- Start the refuter with `fork_turns="none"`, a new agent identity, the original
  request, and user-provided constraints. It independently records its framing
  before a helper reveals the builder's claim statements, recommendation and next action,
  and gate declarations. Refutation binds that snapshot; changing
  the recommendation or next action requires a new independent refutation.
  Do not pass builder analysis, rationale, confidence, or roleplay outputs.
- The consumer reviewer is another fresh agent. It reads the actual rendered
  report and exercises each critical claim's declared acceptance surface. Its
  receipt binds the exact report path and bytes. Changed reports or changed
  decision inputs invalidate completion. Publishing a file is not verification.
- Both independent reviewers assess coverage, not just declared claim IDs.
  They name material claims missing from the ledger and unsupported parts of the
  recommendation. Material means that negating the claim could change the choice,
  its conditions, or the stated next action. Unresolved coverage gaps and failed
  checks supporting the current recommendation prevent finalization.
- Keep the report immutable after consumer review. A completion receipt beside
  the run records the report hash, decision digest, and review receipt. Rendering
  makes a draft; only explicit finalization can mark the run complete.
- Progress and rendering use the same validator. Neither counts non-empty files
  as proof. A failed check remains FIRED but prevents verified completion when
  it affects the decision; failure is not disguised as BLOCKED or N/A.
- Confidence reports verified claims, refutations, remaining uncertainty, and
  forecast assumptions. Remove points for framework count or agreement, tier
  score caps, and the default heuristic Bayesian posterior.
- At a resource limit, stop new work, preserve finished receipts, and mark
  unfinished checks BLOCKED with the exhausted resource and unverified claims.
  An unverified draft and resume instructions are permitted; finalization is not.

## Data and command boundaries

Use Python's standard library behind Bash entry points. Retain the existing
launcher, installer, state locking, spend ledger, and budget defaults.

`bin/gates` owns catalog inspection, initialization, applicability inspection,
recording, review preparation/reveal, validation, and finalization. Records bind
the catalog version and the request, relevant claim definitions, applicability
facts, artifacts, and observations. Writers use a lock and atomic replacement;
replaced gate receipts remain in a history ledger.

The run holds `request.md`, `intake.json`, `claims.json`, `facts.json`,
`gates/*.json`, `frameworks/*.md`, `evidence/*`, and `reviews/*`. `state.json`
retains operational metadata; manually writing `phase=complete` cannot satisfy
the independent completion validator. Paths in evidence receipts must resolve
inside the run. The explicitly prepared report is the sole external subject.

Changing a claim invalidates checks of that claim. Changing an applicability
fact invalidates that gate's receipt. Changing the request or constraints
invalidates prior checks. Completion also binds the current decision and all
non-consumer gate receipts, so post-review edits require another consumer review.

Digest rules: file references use SHA-256 of exact bytes. Structured digests use
UTF-8 JSON with sorted object keys and compact separators. A gate input digest
includes the catalog digest, original request hash, intake hash, its declared
claim IDs and current definitions, and its applicability fact (including evidence
references). Refutation also binds the recommendation and next action. Required gates
bind the whole claim set, including additions and
deletions. The decision digest binds the catalog, request, intake, complete claims
and facts files, recommendation, next_action, TL;DR, format, tier, partial flag, budget caps,
and every non-consumer gate receipt. Source and artifact freshness is validated
separately. Operational timestamps, budget polling counters, consumer receipts,
and completion receipts are excluded to avoid self-referential digests.
The time budget is checked at finalization. A still-current completion receipt
preserves that timestamp, so elapsed idle time does not invalidate finished work.
Changed inputs or receipts require current-time budget checks again; live spend
and evidence validation still apply. Repeated finalization is idempotent.

Old runs stay readable as unverified legacy artifacts. They are never silently
converted to verified records. Resume into the new contract requires a new run
or explicitly archiving the old directory; no fabricated migration receipts.

## Limits of the guarantee

The validator enforces structure, coverage, current evidence bytes, and review
protocol declarations. It is not a truth oracle or an OS sandbox. A malicious
agent can lie about observations or read outside an allowed manifest in a shared
workspace. Use fresh contexts and narrow copied inputs; record that isolation is
an orchestration requirement rather than claiming cryptographic independence.
The actual reviewer must use the named consumer surface, not merely attest that
a file exists. Tests cover the mechanical boundary; model quality is measured
separately.

## Validation and evaluation

- Contract tests exercise false N/A, unknown triggers, illegal states, missing
  evidence, stale receipts, reused review identities, early claim disclosure,
  report mutation, failed checks, and refusal to finalize incomplete work.
- Installation and CLI tests retain isolated homes and mocked paid APIs.
- Publish small synthetic decision cases, relevance judgments (qrels), expected
  applicability, planted false claims, and premise-change pairs. A scorer requires
  predictions for the entire corpus and reports retrieval, applicability,
  refutation, abstention, and measured token/time fields separately.
- Test the scorer with known good and deliberately bad predictions. Those are
  scorer tests, not claims of model accuracy. Do not publish invented latency,
  cost, decision success, or live-model benchmark results.

## Alternatives

- Keep 8/16/25 and strengthen verification: rejected by the user because fixed
  counts retain irrelevant work.
- Delete the framework library: unnecessary; optional reference bytes have no
  context cost until read.
- Add independent review without changing completion: insufficient; non-empty
  files would still look verified to progress and reporting consumers.
