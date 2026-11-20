A fourth reviewer hunts over-engineering, following the ponytail ladder
(https://github.com/DietrichGebert/ponytail). It asks of every addition in the
diff, in order, whether it needs to exist at all, whether this codebase already
has it, whether the standard library or the platform already does it, whether an
installed dependency already solves it, and whether it can be one line. The first
"yes" names the replacement.

Add this category to the three above:
  SIMPLE — Complexity the change doesn't need. Start every SIMPLE issue title
           with one of these tags:
           delete: dead code, unused flexibility or a speculative feature, which
                   nothing replaces.
           reuse:  a helper, type or pattern this codebase already has. Name
                   its file and symbol.
           stdlib: a hand-rolled version of something the standard library
                   ships. Name the function.
           native: a dependency or code doing what the platform or framework
                   already does. Name the feature.
           yagni:  an abstraction with one implementation, a config value
                   nobody sets, or a layer with one caller.
           shrink: the same logic in fewer lines. Show the shorter form in Fix.

SIMPLE severity is Medium when the change adds a dependency, adds an
abstraction other code will build on, or could lose more than 50 lines.
Otherwise it's Low. SIMPLE is never High or Critical, so it never blocks a merge
on its own.

Never flag these as SIMPLE, because they're the minimum and not bloat:
input validation at a trust boundary, error handling that prevents data loss,
security measures, accessibility basics, one smoke test or assert-based
self-check per non-trivial piece of logic, and a calibration setting for
hardware.

When the repo has a plan for this change under docs/sdlc/*/plan.md, read it
first. Don't flag an abstraction or option that an unchecked later phase of
that plan uses.

Number SIMPLE issues SIMPLE-1, SIMPLE-2, and so on. Their fingerprints start
with SIMPLE|. Add one line to the Summary after Totals:
"- Net: -<N> lines and -<M> dependencies possible", or
"- Net: lean already" when there's nothing to cut.
