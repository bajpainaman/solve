# Notices and attribution

This project is MIT licensed. See `LICENSE`. Parts of its text adapt the open-source work below, and each adapted part keeps the notice of its source.

## Adapted text

| Source | License | Revision read | What this project adapts |
|---|---|---|---|
| [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, in `cursor/plugins` | MIT | `a5539b15a3d5` | The criteria under "What a good check is" in `skills/formal-verification/SKILL.md`, from `create-formal-verification-skill`. The outcomes and the pass in `skills/fv-maintain/SKILL.md`, from `maintain-formal-verification-skill`. The project-local recheck skill in `references/report.md`, from the hand-off of `create-formal-verification-skill`. All three were reworded and bound to this project's scripts. |
| [Specula](https://github.com/specula-org/Specula) | Apache-2.0 | `1a86e7e5ca7f` | Part 2 of `references/fidelity.md`, from `skills/tla-checking-workflow/references/spec-fidelity-checklist.md`. The procedure was reworded, generalized beyond consensus protocols, and extended with dispositions. |
| [tlaplus/AgentSkills](https://github.com/tlaplus/AgentSkills) | MIT | `f2adb5e4e2c6` | `skills/fv-tlaplus/references/refactors.md`, from the `tlaplus-split-action` and `tlaplus-add-variable` skills. Both procedures were condensed and reworded. |

## Generated code

| Source | License | Version | What this project ships |
|---|---|---|---|
| [Dafny](https://github.com/dafny-lang/dafny) | MIT | 4.11.0 | `skills/fv-dafny/examples/good/allocation/Allocate-py/`, which is the output of `dafny build --target:py`. The folders `_dafny/` and `System_/` in it are Dafny's runtime for Python, unchanged. |

## Ideas with no text or code copied

- [agent-formal-verify](https://github.com/michael-denyer/agent-formal-verify) (GPL-3.0): a mutations file whose runner prints DETECTED, MISSED and UNCOVERED, and replaying past fix commits as mutations. `scripts/fv-mutate` is an independent implementation with its own file format.
- [proof-skills](https://github.com/opum-ai/proof-skills) (MIT): shipping a config that must fail beside the config that must pass.
- [younes-io/agent-skills](https://github.com/younes-io/agent-skills) (MIT): a ledger that maps each requirement to the place that encodes it.
- [quint-llm-kit](https://github.com/informalsystems/quint-llm-kit) (Apache-2.0): asking about actors, communication, failures and time before modelling.
- [antithesis-skills](https://github.com/antithesishq/antithesis-skills) (Apache-2.0): treating statements in documents as leads to confirm, and turning closed bugs into properties.

## pstack license

```text
MIT License

Copyright (c) 2026 Lauren Tan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## tlaplus/AgentSkills license

tlaplus/AgentSkills is under the same MIT License text as above, with the notice "Copyright (c) 2026 TLA+".

## Dafny license

Dafny is under the same MIT License text as above, with the notice "Copyright (c) Microsoft Corporation".

## Specula license

Specula is licensed under the Apache License, Version 2.0. A copy of the license is at <https://www.apache.org/licenses/LICENSE-2.0>. The adapted file was modified as the table above states.
