# Decide: check the choice, then deliver it

Use this workflow for a consequential choice with real alternatives. Resolve
`SOLVE_ROOT` to the installed `skills/solve` directory. Read
[runtime](runtime.md), [roles](roles.md), and [confidence](confidence.md) for the
receipt schema and review protocol. Apply [operating rules](operating-rules.md)
throughout. Load method cards only after their triggers apply.

This packaged workflow uses `--portable-html` and offline prose lint. Do not run
startup update checks, `html-sync`, or the legacy HTML download/build path.

## Contract

- Preserve all 25 framework gates and the three required gates: evidence,
  refutation, and consumer. Quick reduces depth and budget, not this contract.
- Use exactly **FIRED**, **N/A**, or **BLOCKED**. FIRED requires hashed artifacts
  and actual expected/observed checks; it can report a failed check. N/A requires
  the exact written trigger and evidence that it is false. Unknown applicability
  is BLOCKED. Time pressure never makes a gate inapplicable.
- Check every critical claim. Both reviewers must also look for material claims
  omitted from the ledger. A claim is material if its negation could change the
  choice, its conditions, or its next action.
- Use actual fresh agents with `fork_turns="none"` for the refuter and consumer.
  They need distinct identities and bounded inputs. Roleplay is not independent
  review. A shared workspace does not enforce secrecy.
- Only successful `bin/gates finalize`, with current receipts, establishes
  verified completion. A file, an agent's completion message, or a manually set
  phase does not. Verification covers recorded checks, not future success.

If the executor or fresh agents are unavailable, still provide a useful
**unverified draft** with the best supported recommendation, decisive unknowns,
and next test. Name which checks could not run. Never invent receipts, agent
identities, observations, source captures, or completion.

## 1. Frame and initialize

Preserve the original request verbatim in a brief. Put only user-provided
constraints, success criteria, and consumer context in `intake.json`; keep
builder reasoning out of both original-input files. Use a new run directory or
resume a compatible run after checking receipt freshness. Preserve prior work.

Default to Standard. Honor explicit user or launcher tier/time overrides. The
existing tier ceilings are Quick: 15 minutes/$2; Standard: 30 minutes/$5; Deep:
60 minutes/$15. **The plugin's paid research budget defaults to $0.** A tier or
preseed alone does not authorize a paid provider. Use an already approved spend
limit when present; explicit budget overrides take precedence. `tokens_usd` is
the legacy name for external research spend, not subscription model-token use.

```bash
"$SOLVE_ROOT/bin/gates" init --run-dir "$RUN_DIR" --request "$BRIEF" \
  --builder-id "$BUILDER_ID" --tier "$TIER" --slug "$SLUG"
"$SOLVE_ROOT/bin/state-rw" write "$RUN_DIR" budget "$BUDGET_JSON"
```

Before any research, serialize `BUDGET_JSON` from the selected time cap and the
authorized spend cap, with `tokens_usd: 0` when no paid spend was approved.
Follow runtime.md to bind the budget helpers to this run's real start time and
cost ledger. Do not reset the clock to hide elapsed work.

Write a short framing artifact, separate from the original-input files:

- Name the objective, beneficiary, observable success condition, and deadline
  when supplied. Mark any inferred objective as an assumption.
- Compare feasible alternatives with the status quo or smallest useful change.
  Include deferral or a reversible test when that is a real alternative.
- Identify binding constraints, reversal cost, downside if wrong, and the
  actual bottleneck. Distinguish feasibility from usefulness and economics.
- Name the strongest version of each serious option and what must hold for it
  to work. Identify the fastest test that could reject the leading option.
- State what evidence or threshold would change the recommendation, and when
  to stop. Do not invent numerical weights, user preferences, owners, or dates.

Ask only for missing information that can change the action or a required
check. Do not turn the 25 triggers into 25 ritual questions. Proceed on explicit,
reversible assumptions when the task permits it.

## 2. Define claims and applicability

Write `claims.json` using runtime.md: statement, fact/forecast/preference,
critical Boolean, and an acceptance surface with an expected observation.
Forecasts require assumptions and follow-up; preferences require the user's
stated source. Include inconvenient material claims, not only easy checks.

```bash
"$SOLVE_ROOT/bin/prose-check" --offline --run-dir "$RUN_DIR" --scope claims
"$SOLVE_ROOT/bin/gates" catalog
```

Fix true prose findings before inspecting gates. Preserve meaning, modality,
numbers, conditions, identifiers, quotations, and uncertainty. Automated lint is
advisory; a skipped linter did not run.

For every catalog trigger, record its observed applicability fact, explanation,
and hashed evidence in `facts.json`. Assess relevance within this decision's
scope. Silence is not evidence of absence. A single observation can support
several facts only when it actually establishes each one.

```bash
"$SOLVE_ROOT/bin/gates" inspect --run-dir "$RUN_DIR" --gate "$GATE"
```

Record supported N/A and specific BLOCKED receipts. For a true framework
trigger, read only its compact method card. Read a deep-reference section only
to answer a named remaining question. Do not add methods or agents to meet a
quota. Every applied method must affect a claim or the choice.

## 3. Check the deciding claims

Use primary evidence for changing facts and exact source versions for code.
Research named gaps. Delegate independent evidence lanes when useful; keep the
brief and output paths bounded. Record actual observations under `evidence/`,
including source identity, observation time, and limitations. Recheck changing
facts when their validity window or a decision-relevant condition changes.

Each check names the claim, actual surface, expected result, observed result,
Boolean outcome, and hashed observation. File creation is not a successful API,
reader, page, or application check. Preserve a failed observation as a failure.
Record receipts with the digest obtained before the check:

```bash
"$SOLVE_ROOT/bin/gates" record --run-dir "$RUN_DIR" --file "$RECEIPT"
```

Changed inputs require a new check, not an old receipt with a new digest. Use
ranges and sensitivity when estimates drive the choice. Quantify probabilities
only from an identified model or dataset; agreement is not a probability.

At work boundaries, check budget and progress. At 80%, finish necessary checks
and start no optional work or new paid research. At 100%, stop workers, call
`bin/gates halt` with the exhausted resource, render an unverified draft, and
name the unfinished checks and resume conditions. Preserve completed evidence.

## 4. Refute independently

Write nonempty `recommendation` and `next_action` strings through `state-rw`.
State what to choose, why it beats the baseline, downside if wrong, and the
evidence that would reverse the choice. Tag substantive output claims
`[Certain]`, `[Likely]`, or `[Guessing]` according to the operating rules.

```bash
"$SOLVE_ROOT/bin/prose-check" --offline --run-dir "$RUN_DIR" --scope decision
```

Follow the exact two-stage protocol in roles.md. Spawn a fresh refuter with
`fork_turns="none"`; have it wait for the manifest. Prepare it with its actual
returned identity. Initially disclose only the original request and user
constraints. It finds its own evidence and commits `blind.json` before reveal.

After the builder's claims, facts, recommendation, and next action are stable,
run `bin/gates reveal`. Give the refuter the reveal and disclosed snapshot,
without builder rationale, confidence, or framework outputs. Require checks of
every critical claim, missing claims, unsupported recommendations, and unjustified
N/A declarations. Preserve dissent and actual evidence.

The builder may record the refuter's receipt; it must not author the refuter's
observations or substitute a favorable verdict. Changed claims, recommendation,
or next action require a new refuter and blind/reveal cycle. Do not rehash a
stale review. Optional perspectives never replace this gate or raise confidence.

## 5. Render and review the delivered result

Render from validated run data using the bundled renderer:

```bash
"$SOLVE_ROOT/bin/render-report" --run-dir "$RUN_DIR" --slug "$SLUG" \
  --output "$REPORT" --portable-html
```

`REPORT` must end in `.md`. Use Markdown alone when the user requests it; omit
`--portable-html` in that case. Keep the checked recommendation and next action
unchanged. An HTML build failure is a failure to fix or disclose, not evidence
that the page passed. Follow the artifact workflow for available browser checks;
a static check is not a visual/runtime test.

After pre-consumer checks pass, spawn a second fresh agent with
`fork_turns="none"`, wait for its manifest, and prepare it against the exact
delivered report path. Use roles.md's consumer brief. It must read all declared
views, follow evidence, exercise each critical acceptance surface, and identify
material omissions or unsupported conclusions. A forecast check validates
assumptions and follow-up, not future truth. An inaccessible required surface is
BLOCKED. Record the actual review without editing its observations.

Do not rewrite report or view bytes after review. A change requires rendering
again and a fresh consumer review. Preserve referenced evidence and receipts in
the delivery packet so that a saved page does not lose its audit trail.

## 6. Finish

```bash
"$SOLVE_ROOT/bin/gates" validate --run-dir "$RUN_DIR"
"$SOLVE_ROOT/bin/gates" finalize --run-dir "$RUN_DIR"
```

Deliver the recommendation, decisive evidence, remaining uncertainty, downside,
and next action with the saved artifacts. Distinguish verified recorded checks
from an unverified draft. Name exactly what blocked completion when applicable.
Do not claim that packaging, attractive presentation, or a successful finalizer
establishes the best possible decision. Use host message/wait controls, not
shell polling; complete authorized follow-through within the task's scope.
