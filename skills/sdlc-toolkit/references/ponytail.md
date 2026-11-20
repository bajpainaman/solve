# Running ponytail

[ponytail](https://github.com/DietrichGebert/ponytail) pushes code toward the smallest change that works. Its skills accept model invocation, so call them with the Skill tool. `sdlc:setup` installs it.

| Stage | How ponytail runs |
|---|---|
| Plan | The plan's self-challenge applies ponytail's ladder to every file and function the plan adds. |
| Build | Invoke `ponytail:ponytail` before the first phase. It stays on for the rest of the session. |
| Build, Test | pr-review runs with its ponytail lens, which checks the code ponytail shaped. `pr-review.md` covers the flag. |
| Maintain | `drift` also runs `ponytail:ponytail-audit` on the whole repo. |

## The ladder

The ladder asks five questions in order. Does it need to exist at all? Does this codebase already have it? Does the standard library or the platform do it? Does an installed dependency solve it? Can it be one line? The first "yes" names the smaller option.

## What ponytail may not change

Ponytail never overrides the loop's own rules. Every test in `plan.md` gets written, and so does every test the testing toolkit keeps, even where ponytail's "one runnable check" minimum would stop sooner, because those tests prove the acceptance criteria. Every requirement in `spec.md` gets built, including its non-functional requirements, because the approver already decided they're needed. When ponytail and the plan disagree, follow the plan and raise the disagreement with the engineer.

If ponytail isn't installed, the lens still runs through pr-review. Record the Build stage's `ponytail` tool as skipped, with that reason.
