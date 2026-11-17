# Word choice

## Selection algorithm

For each questionable word:

1. Check whether it is a technical noun or technical verb with a stable domain
   meaning. If yes, keep it and use it consistently.
2. Otherwise, check the official dictionary for approved status, part of speech,
   meaning, and permitted form.
3. If the dictionary does not approve the word, inspect the suggested alternatives.
4. Use a word-for-word alternative only when meaning and grammar stay equal.
5. Otherwise, rewrite the sentence.

Dictionary examples are models, not mandatory wording.

## High-frequency review map

These entries summarize recurring errors in Issue 9. They are review prompts,
not blind replacements.

| Review term | Preferred direction | Meaning guard |
|---|---|---|
| acceptable | permitted | Keep legal wording if `acceptable` is a defined term. |
| alternate | alternative | Do not change a verb that means to switch repeatedly. |
| avoid | prevent | Use `prevent` only when prevention is possible. |
| both | the two | Use only when exactly two known items exist. |
| ensure | make sure | Keep requirement strength unchanged. |
| fit | install | Use only when the action is installation. |
| follow | obey | Use `obey` for instructions, not physical movement. |
| further | more | Confirm whether distance or degree is meant. |
| however | but | Put `but` between the contrasted clauses. |
| insert | put | Preserve domain terms such as SQL `INSERT`. |
| main | primary | Keep identifiers and official titles exact. |
| may | can | Do not replace legal permission or uncertain likelihood blindly. |
| now | at this time | Delete it if time is not relevant. |
| perform | do | Prefer the primary action verb when available. |
| portion | part | Keep defined data or legal terms exact. |
| press | push | Keep UI labels and hardware names exact. |
| repeat | `do ... again` | Keep commands and identifiers exact. |
| shall | must | Change only when both state the same requirement. |
| should | must | Never strengthen advice into a requirement without authority. |
| since | because | Use only for cause. Keep `since` when it means time if allowed by local policy. |
| therefore | thus / as a result | Use only for a proved consequence. |
| using | use / with | Prefer the primary action as the main verb. |

## Terms that usually require sentence reconstruction

- `any`: identify the actual set or condition.
- `have to`: use an imperative command in a procedure or state the requirement.
- `need`: state what is necessary and for whom.
- `required`: separate the requirement from the action.
- nominalized actions: `implementation`, `execution`, `utilization`,
  `completion`, `validation`, `configuration`.
- phrasal verbs: replace only after you identify the exact meaning.

## Consistency rules

- Use one term for one item.
- Use a technical noun only as a noun.
- Use a technical verb only as a verb.
- Prefer short, accepted domain terms.
- Do not use slang, regional language, or unexplained team jargon.
- Use American English unless another governing directive applies.

## Pronouns

Use a pronoun only when one antecedent is possible. Repeat the noun when `it`,
`they`, `this`, `these`, or `those` can refer to multiple items.

Use gender-neutral wording. Preserve gender-specific language that the context
requires. A quoted source or a medical distinction can require that wording.
