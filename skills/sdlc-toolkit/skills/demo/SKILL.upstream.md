---
name: demo
description: Shows a finished feature working, as the optional demo in the Prove half of SDLC stage 6. Records a video of the change when the feature has a UI, runs a walkthrough with its literal output when it doesn't, and puts the demo on the feature's proof page. Use when the user runs /sdlc:demo, asks for a demo, a recording or a walkthrough of a feature, or the test stage's approver wants one.
argument-hint: "<slug>"
---

# Demo — show the feature working

Read `${CLAUDE_PLUGIN_ROOT}/references/stage-rules.md` first, then `${CLAUDE_PLUGIN_ROOT}/references/proof.md`, which says where the demo goes on the proof page.

A demo is a show for the approver, and it isn't a check. The tests and the verifier decide whether the feature works. The demo lets a person watch it work. So a demo is optional, and the approver decides whether there is one. The test stage asks them, and this skill runs on a yes. It also runs by itself, for example to record a feature again after a fix.

Feature: `$ARGUMENTS`

## Steps

1. **Write the script.** Read the acceptance criteria in `spec.md`. Choose three to seven steps that a user or a caller would take, in the order they would take them. When the verifier's report in `verify.md` already walks the criteria, start from its steps, because the demo shows the same feature. Each step names what is done, what should appear, and the criterion it shows. Start `docs/sdlc/<slug>/proof/demo.md` from the template with these steps, before you run anything.

2. **Pick the kind of demo.** A feature that a person sees in a browser or an app window gets a recording. A feature with no UI, such as an API endpoint, a CLI command, a job or a library, gets a walkthrough. A feature with both gets both.

3. **Start the feature as it was built.** Use the feature branch at its current commit. Launch the app the way the repo's verification skill at `.claude/skills/verify-*/` says, or with the run command in `CLAUDE.md`. Use test data only, so no secret and no real customer shows in the demo.

4. **Record a UI.** Follow the script from its first step to its last, and record with the best recorder the session has. Try them in this order. Say in `proof/demo.md` which one you used, and why a better one wasn't there.
   1. The repo's own recorder. This is a recording command that `CLAUDE.md` or the verification skill names, or an end-to-end runner that saves video, such as Playwright or Cypress.
   2. A browser tool in the session that records, such as the GIF recorder of Claude in Chrome.
   3. A filmstrip, which is one screenshot per step, numbered in order.

   Save a video or a GIF as `proof/demo.<ext>`, and a filmstrip as `proof/frames/<nn>-<step>.png`.

   Check what the recorder left before you use it. A recorder can exit cleanly and still record nothing. Never present a file that isn't a recording as one. When no recorder can make a real recording, say so in `proof/demo.md` and on the page, show the steps the best way the session can, and tell the approver what a real recording needs.

5. **Walk through a feature with no UI.** Run each step for real, with a request, a CLI call or a script. Keep the literal command, its output, and its exit or HTTP status. Trim a long output, and mark where you trimmed it. Never copy output from a test log, and never write it from memory.

6. **Keep what happened.** A step that goes wrong stays in the demo as it happened. Don't change the product's code or a test to make a step pass, and don't rerun a step until it does. Report the failure to the stage, whose gate decides what happens next.

7. **Finish `proof/demo.md`**, then put the demo on the proof page, as `proof.md` describes. Create the page from its template when it doesn't exist yet. Tell the user where the page is.

When the test stage called this skill, the stage records `demo: proof/demo.md` in its `tools`. This skill approves nothing.

## Template

~~~markdown
# <Feature title> — demo

Kind: <recording of the UI | walkthrough | both>
Recorder: <what made the recording, and why a better one wasn't used. "none" for a walkthrough>
Ran on: <branch> at <commit>, <date>
Recording: <`proof/demo.webm`, or the frames folder. Leave this line out for a walkthrough>

| # | Step | Shows | Result |
|---|---|---|---|
| 1 | <what is done> | AC1 | <as expected, or what appeared instead> |

## Steps as run
### 1. <what is done>
```
$ <the command>
<the output>
```
Status: <exit or HTTP status>

## Not shown
- <an acceptance criterion the demo leaves out, and where its evidence is>
~~~
