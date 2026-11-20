# Rules every stage follows

## The feature folder

Each feature lives in `docs/sdlc/<slug>/` in the target repo. The folder holds the artifacts, the reports reviewers wrote about them, and one state file, `sdlc.yaml`.

```yaml
feature: bulk-export
ticket: ENG-1234            # Linear/Jira/GitHub id, if the work started from one
branch: aasim/eng-1234-bulk-export
stages:
  intent:   {status: approved, owner: Aasim, approver: Aasim, approved_by: Aasim, date: 2026-11-11, artifact: intent.md, tools: {goldfish: egm/concepts_brief.md}}
  spec:     {status: draft,    owner: Priya, approver: Aasim, artifact: spec.md}
  rfc:      {status: skipped,  reason: "one-file change, approved by Aasim"}
```

- `status` is `draft`, `approved` or `skipped`. A stage is done when it's `approved` or `skipped`.
- `owner` is the person who produces the artifact. `approver` is the person who must approve it. Ask for both at the start of a stage if they're unknown. Never invent a name. Write `unassigned` instead.
- `artifact` is a path in the folder, or a URL when the artifact lives elsewhere, such as a Notion page.
- `tools` accounts for each tool the stage requires. It maps each one to the file the tool produced, as a path in the folder, or to `"skipped: <reason>"` when the approver skipped it or it isn't installed. The table under "The gate" lists each stage's tools.
- An optional top-level `pr_review` block sets the feature's pr-review panel and lenses. `pr-review.md` describes it.

## Three modes

Every stage runs in one of three modes. The arguments pick the mode, and author is the default.

| Mode | When | What Claude does |
|---|---|---|
| `author` | Claude produces the artifact with the owner. | Run the stage's steps, then the gate. |
| `adopt <path\|url>` | The owner, or a teammate, already wrote it somewhere else. | Fetch the source with the right tool (Read, a Notion, Google Drive or Linear MCP, or `gh`). Put it into the stage's template without changing its decisions. List every template section the source leaves empty as an open question. Record the source as `source:` in `sdlc.yaml`, then run the gate. |
| `review` | You're managing the stage, and someone else owns the artifact. | Don't edit the artifact. Run the stage's Goldfish review and give the findings to the approver. Record the approver's decision, approve or request changes, in `sdlc.yaml`. When the artifact sits on a teammate's branch, read it with `git show origin/<branch>:<path>`, and commit to that branch only if the approver says to. |

## Running a stage

Before the first step, put the stage's steps in the task list, one item per step. A step you skip stays on the list with its reason.

When a step names a skill or a subagent, invoke it. Don't do its work by hand, even when the step says enough to try, because the tool holds rules that the step doesn't repeat. Do the work yourself only when the session doesn't list the tool. In `sdlc.yaml`, work done by hand counts as a skipped tool, with that reason.

## The gate

Every stage ends with the same gate.

1. **Run the Goldfish review** the stage names. The approver may skip it for a small change. Fix what the owner agrees to fix.
2. **Ask the approver** to approve the artifact or request changes. Revise until they approve. Claude never approves its own work.
3. **Update `sdlc.yaml`** with `status: approved`, `approved_by`, `date` and the stage's `tools`.
4. **Commit the stage on its own.** One commit holds the artifact, its review reports and `sdlc.yaml`. Follow the repo's commit conventions. When it has none, use `docs(sdlc): <stage> for <slug>`.

A stage isn't approved until its `tools` entry accounts for each tool in its row.

| Stage | Tools |
|---|---|
| Intent | `goldfish` |
| Spec | `goldfish` |
| RFC | `rfc-skill`, `formal-verification`, `goldfish` |
| Plan | `testing`, `goldfish` |
| Build | `ponytail`, `testing`, `pr-review` |
| Test | `testing`, `test-audit`, `verifier`, `pr-review`, `demo` |
| Ship | `pr-review` |
| ADR | `goldfish` |
| Maintain | none |

- `goldfish` is the stage's EGM review, and its file is the report under `egm/`.
- `rfc-skill` is the `rfc` skill, and its file is `rfc.src.html`.
- `formal-verification` is the fv-toolkit's `formal-verification` skill, and its file is the property ledger, `fv/design/README.md`. When its triage finds no claim to check, that's the skip reason. When the ledger exists, Test also accounts for `fv-verifier`, the subagent that models the code afresh, and its file is `fv/code-report.md`.
- `ponytail` is ponytail mode during Build. It writes no file of its own, so its file is the last Build pr-review report, whose ponytail lens checked the code.
- `testing` is the testing toolkit's `testing` skill. At Plan its file is `plan.md`, whose Tests section holds the skill's choice. At Build and Test its file is the stage's report under `testing/`.
- `test-audit` is the testing toolkit's `test-audit` skill, and its file is its ledger, `testing/audit.md`.
- `pr-review` is the stage's last report under `pr-review/`.
- `verifier` is the verifier subagent, and its file is `verify.md`, which holds its report.
- `demo` is the `demo` skill, and its file is its record, `proof/demo.md`. A demo is optional, so the stage asks the approver whether they want one, and a no is the skip reason. Only the approver's answer settles this entry.

## Branches and history

- Never commit on the default branch. Before the first commit for a feature, create a feature branch with the repo's branch-naming convention, and record it in `sdlc.yaml`.
- A repo may have installed the gate hook that `sdlc:setup` offers. The hook denies a commit on the default branch, and a commit that approves a stage while one of its tools is missing from `tools`. It makes Claude Code ask the user before a PR is approved or merged. When the hook stops a command, do what its message says and don't route around it.
- Earlier artifacts don't change silently. When a later stage finds that an earlier artifact is wrong, show the conflict. If the approver agrees, fix the earlier artifact in its own commit and set that stage back to `draft` until it's re-approved.
- When Claude makes the same mistake twice in any stage, or a review finding repeats one from an earlier feature, propose a check that catches it, such as a lint rule, a test or a hook. When no check can express it, propose a one-line addition to the "Things Claude gets wrong" section of `CLAUDE.md`.

## When instructions overlap

A session usually carries more instructions than this plugin's. The user's own instructions, the repo's `CLAUDE.md` and other workflow plugins all speak to the same work.

- **The user's instructions and the repo's `CLAUDE.md` win** over a stage's steps and templates. Follow them and say that you did. Keep the artifact file names and the `sdlc.yaml` fields as they are, because other stages read them.
- **Inside a stage, the stage is the workflow.** Superpowers, agent-skills and similar plugins define their own lifecycles, and some of their skills repeat what a stage already does. Before you invoke one, read `${CLAUDE_PLUGIN_ROOT}/references/companions.md`. It lists, stage by stage, which of their skills add something and which repeat the stage.

## Skipping stages

The approver may skip a stage when it adds nothing. For example, a one-file fix rarely needs an RFC. Record the reason. When the RFC is skipped, the ADR is skipped too. Build, Test and Ship are never skipped.
