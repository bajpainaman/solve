# Portable Solve plugin

Date: 2026-11-13
Status: Proposed and implemented on the plugin branch.

## Problem

The user requested an installable plugin with decisions, artifacts, and writing
bundled. The CLI skill loads its decision instructions for every task and relies
on a separately fetched HTML package. That package has no published license.
Its export also links to local evidence that may be lost when a page is shared.

## Decisions

- Add a private-ready Agent Plugins 1.0 package, built by `bin/build-plugin`.
  Keep the existing CLI source and behavior. Put portable instruction overrides
  in `plugin/overrides/`; assemble shared runtime files into `skills/solve/`.
- Use one concise entry skill and load decision, artifact, or writing instructions
  only for the matching task. Keep all 28 gates and all 32 artifact patterns.
  A package contains the references; loading them is conditional.
- Add an original Python HTML renderer and optional browser verifier. Ship no
  `html-artifact` code and make no startup downloads. Keep the legacy `--html`
  mode unchanged; select this renderer through `--portable-html`.
- Embed supporting snapshots in a decision page. Preserve exact report and view
  hashes in the existing consumer/completion contract. A static render is always
  pre-consumer; the separate completion receipt establishes reviewed completion.
- Add `prose-check --offline` to use installed tools and packages only. Missing
  engines or packages remain skipped, and manual writing rules remain available.
- Default paid external research to zero in the plugin workflow. A numerical
  budget ceiling is not authorization to buy services or call a paid API.
- Do not create a server solely to wrap an instruction workflow. Reuse available
  host executors, connected tools, browsers, and agents. Report missing capability
  explicitly; do not manufacture reviewer identities or passing checks.
- Preserve MIT and Apache notices, record source revision and packaged file
  hashes, validate the archive itself, and exclude downloaded dependencies,
  credentials, local runs, and generated files.

## Limits and evidence

Software tests establish packaging, escaping, contract integration, and runtime
behavior. They do not establish higher decision accuracy, lower model cost, or
better real-world outcomes. Compare baseline and plugin on identical models and
fresh changed-premise tasks before claiming a measured decision-quality gain.

The validator checks declarations and evidence bytes. It cannot guarantee source
truth or independent behavior in a shared filesystem. Fresh independent reviews
and honest observation remain orchestration obligations.
