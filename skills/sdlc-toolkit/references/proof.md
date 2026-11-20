# The proof page

The Prove half of stage 6 ends with one page that shows the approver the feature works. The page is `docs/sdlc/<slug>/proof/proof.html`. Every feature gets one, and the approver reads it before they approve the stage. `sdlc:test` builds it, and `sdlc:demo` adds the demo to it.

## Rules

- **The page adds no fact.** Build it from what the stage already recorded: `verify.md`, the reports under `testing/`, `pr-review/` and `fv/`, and `proof/demo.md`. Each claim names the file that holds its evidence. When the record lacks something, the page says that it's missing.
- **One file, readable from the repo.** Start from `${CLAUDE_PLUGIN_ROOT}/references/proof-template.html`. Keep the styles inline, and load no script, font or image from the network. A recording sits beside the page in `proof/`, and the page points at it with a relative path. Commit the page and everything else in `proof/`, whatever its size.
- **A failure stays on the page.** A criterion that fails, a property the code breaks and a demo step that goes wrong are all shown as they happened. The page reports the stage. It never argues for approval.
- **A bounded pass is called a bounded pass.** Never write "verified", "proved" or "guaranteed" about a formal check.

## Sections

Keep the sections in this order, with these ids. A section with nothing to show keeps its heading and says why in one line.

| Id | Shows | Comes from |
|---|---|---|
| `#verdict` | The feature, its branch and commit, the date, who approves, how many criteria pass, and the one thing the approver most needs to know | `sdlc.yaml`, `verify.md` |
| `#criteria` | Each acceptance criterion with its evidence and its result | `verify.md` |
| `#demo` | The demo, or the reason there isn't one | `proof/demo.md` |
| `#formal` | The formal checks, when the design was modelled | `fv/design/README.md`, `fv/code-report.md` |
| `#tests` | The scenario, the final tests, the testing report's `Verified:` line, the tests added to close a gap, and what the audit removed or merged | `testing/test.md`, `testing/audit.md` |
| `#verifier` | What the verifier ran and saw, and each mismatch with the plan or the spec | `verify.md` |
| `#review` | The final pr-review's verdict and totals, and each finding that is still open with its reason | the last report under `pr-review/` |
| `#gaps` | What the stage didn't check, and what a pass doesn't cover | `verify.md` |

## The demo section

- A recording of a UI plays in the page. Use `<video controls>` for a video file, `<img>` for a GIF, and one `<figure>` per step for a filmstrip of screenshots. Put each step's caption under it.
- A walkthrough of a feature with no UI shows each step as the command that ran and the output that came back, copied from `proof/demo.md`.
- Say which recorder made the recording, and the commit it ran on.
- When the approver declined a demo, write "No demo" and their reason. When nobody has answered yet, write that the demo waits on the approver's answer.

## The formal checks section

Present these parts for each confirmed property, and leave the models themselves in `fv/`.

1. The property, as the one sentence the approver confirmed.
2. The verdict of the design model and the verdict of the code model, side by side.
3. The bounds and the faults of each check, such as "two tills, one voucher, and a hold that can expire at any moment".
4. For a model that failed, the counterexample as numbered steps in the system's own words, so a reader who doesn't know the tool can follow them.
5. The evidence that a pass means something: the config that must fail, the witness configs, and how many planted bugs the check detected.
6. What the checks leave open, and the commands that rerun them.

A feature with no property ledger keeps the heading and says that no claim in the feature earned a formal check.

## Publishing

The page in the repo is the proof. When the session can publish a Claude artifact, offer to publish the page as a private one, and put its link in `verify.md` when the approver says yes. Never publish it unasked.
