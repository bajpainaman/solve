# One skill with a router and built-in modes

Date: 2026-11-13
Status: Accepted. Shipped in 2.1.0.

The user asked for one skill that combines solve, simplify-writing,
html-artifact, and the html-effectiveness templates, with a router that decides
what to use, where, and how.

## Decisions

- solve has four modes: decide, make, write, and answer. The router chooses the
  mode first, then Markdown or HTML, then the template. Bugs and unvalidated
  product ideas still go to other skills. The decide-mode contract from
  ADR-0001 is unchanged. Make and write modes never create gates or receipts.
- The write layer applies to all prose in every mode. In decide mode, claims
  are linted before any gate runs, and the recommendation and next action are
  linted before the refuter reveal. Both texts enter digests, so a later
  rewording would make receipts stale.
- The decision-memo page joins the render subject as `views`. The consumer
  prepares against it, and the completion receipt binds its hash. An edit to
  the page after review invalidates completion, the same as an edit to the report.
- html-effectiveness (Apache-2.0) and simplify-writing (MIT) are committed with
  their licenses. html-artifact publishes no license file, and this repository
  is public under MIT. Committing it would redistribute it without permission.
  `bin/html-sync` fetches it at a pinned commit into `html/` on the user's
  machine. `.gitignore` excludes `html/`.
- The template catalog maps each exemplar to trigger phrases, a shape, and a
  renderer. `artifact` pages use html-artifact components. `bespoke` pages need
  custom interaction and are written as one self-contained file. Without
  `html/`, `artifact` pages fall back to `bespoke`. Every page must pass the
  headless check, which the exemplars themselves fail. They are references
  for structure only.
- `sources.json` pins every upstream source to a full commit. `bin/check-updates`
  compares the pins and solve itself with upstream, once per session from a
  one-day cache. It reports and never applies. An unreachable source is UNKNOWN.

## Consequences

- A new template needs a catalog entry and a routing test.
- An upstream change reaches solve only through a reviewed pin bump.
- html-artifact can be committed only if its author publishes a license.
- The skill description covers three kinds of request, so standalone
  simplify-writing or html-artifact installs can compete for the same triggers.
