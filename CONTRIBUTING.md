# Contributing to solve

Thanks for considering. This skill is opinionated by design but PRs are welcome on the seams.

## What's safe to PR

- **New frameworks.** Add a 26th framework if you have a strong case. Follow `frameworks/_TEMPLATE.md` (17 sections), match `frameworks/cynefin.md` for depth, add it to the routing table in `SKILL.md` Step 7's decider brief, update the table in README.
- **Voice fixes.** If a framework drifts into AI vocabulary (delve, robust, comprehensive, multifaceted, etc.) or em dashes, it's a bug. PR a fix; the adversary teammate enforces this rule live but the static files can drift.
- **Worked example continuity.** All 25 frameworks use OFTv2 migration as the canonical example. If a framework's worked example contradicts an upstream framework's output, fix it.
- **Budget + calibration tooling.** `bin/budget-track` and `bin/calibration` are intentionally simple; if you hit a real edge case, PR.
- **Mermaid diagram fixes.** GitHub's mermaid parser is strict. Test diagrams render cleanly on github.com before pushing.

## What's likely to be rejected

- Adding more "soft" guidance in SKILL.md without a corresponding hard gate. The skill works because of explicit gates (regime check, kickoff guard, tool-call cap). Soft suggestions without enforcement degrade the workflow.
- Reducing the 25 frameworks. Removing one breaks the canonical worked-example chain. If a framework feels redundant, write a justification in the PR; we'll decide together.
- Removing the adversary teammate or its enforcement responsibilities (no-AI-vocab, question auto-conversion). The adversary is what makes the skill adversarial-by-construction.

## Local development

```bash
git clone https://github.com/bajpainaman/solve.git
cd solve

# point your global skill at this clone
rm -f ~/.claude/skills/solve
ln -s "$(pwd)" ~/.claude/skills/solve

# run smoke tests
bash install                                    # smoke tests run as part of install
bin/calibration help
bin/budget-track --help

# verify each framework follows the template
for f in frameworks/*.md; do
  [ "$(basename "$f")" = "_TEMPLATE.md" ] && continue
  for section in "Entry Predicate" "Operating Principles" "Pushback Patterns" "Method" "Output Schema" "Decision Hook" "Worked Example"; do
    grep -q "^## $section\|^### $section" "$f" || echo "MISSING: $section in $(basename $f)"
  done
done
```

## Style

- No em dashes anywhere. Use commas or periods.
- No AI vocabulary in framework files: delve, crucial, robust, comprehensive, nuanced, multifaceted, furthermore, moreover, additionally, pivotal, landscape, tapestry, underscore, foster, showcase, intricate, vibrant, fundamental, significant.
- Builder voice: name files, frameworks, commands explicitly. Lead with the point.
- No exclamation marks. No hedging ("perhaps", "might be", "could potentially").

## Versioning

Semver-ish. Bumps:

- **Patch (0.5.0 → 0.5.1)**: bug fix, doc update, framework prose polish without method changes.
- **Minor (0.5.0 → 0.6.0)**: new framework, new bin helper, new SKILL.md step, new guarantee.
- **Major (0.x → 1.0)**: signature change of agent-team protocol, breaking change to CLI shim.

Bump `SKILL.md::version` and add a `## [X.Y.Z]` block to `CHANGELOG.md` in the same PR.

## Tag + release flow

After merging to main:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z: <one-line summary>"
git push origin vX.Y.Z
gh release create vX.Y.Z --notes-file CHANGELOG.md   # or write notes inline
```

## Reporting bugs

Open an issue with: `solve status` output, the problem statement that triggered the bug, the framework file the bug appeared in (if applicable), and the expected vs actual behavior.
