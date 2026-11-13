# STE writing cheatsheet

## Pick the profile

| Reader's task | Profile | Sentence limit | Main form |
|---|---|---:|---|
| do a task | Procedure | 20 words | Imperative command |
| understand a system or result | Description | 25 words | Active statement |
| prevent injury, death, or damage | Safety | 20 words | Label + command/condition + result |
| act on UI or CLI feedback | Interface | Keep minimal | State + next action |

## Pick strictness

| Content | Default mode |
|---|---|
| Procedure, runbook, safety text, error message | Strict |
| README, PR description, release note, docs, comment | STE-flavored |
| Marketing, essay, fiction, branded voice | Do not use without confirmation |

## Rewrite decision tree

1. Can one reader identify the actor, action, object, and condition?
   - No: restore the missing element or ask.
2. Does the sentence contain more than one action or topic?
   - Yes: split it.
3. Is the main action hidden in a noun?
   - Yes: make the action a verb.
4. Is the actor known?
   - Yes: use active voice.
   - No: passive voice can be acceptable in a description.
5. Does a term have multiple possible referents or meanings?
   - Yes: repeat the exact noun or define the term.
6. Does the rewrite alter modality or uncertainty?
   - Yes: reject the rewrite.

## Safety triad

| Risk | Label | Required content |
|---|---|---|
| Injury or death | WARNING | Clear command or condition, then possible injury/death |
| Object damage only | CAUTION | Clear command or condition, then possible damage |
| Both levels | WARNING | Use the higher risk level |

## Fast AI-slop cuts

| Cut | Replace with |
|---|---|
| "It is important to note that X" | `X` |
| `In order to X` | `To X` |
| "Leverage X to facilitate Y" | Name the actual action |
| `Robust / seamless / scalable` | Observable behavior or measurement |
| Preview + list + recap | Keep the list once |
| Rotating synonyms | One stable technical term |
| Generic closing paragraph | Delete it |

## Meaning locks

Never change without authority:

- `must` to or from `should`, `may`, or `can`.
- a warning to a caution, or the reverse.
- numbers, units, thresholds, names, IDs, URLs, flags, or code.
- conditions, exceptions, sequence, or uncertainty.

Never rewrite code, identifiers, command syntax, or exact literals.

## Paragraph check

- one topic.
- no more than six sentences.
- first sentence states the topic or result.
- examples directly support the topic.
- no repeated summary.
