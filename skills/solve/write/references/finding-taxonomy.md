# Finding taxonomy

## Severity

| Severity | Meaning | Action |
|---|---|---|
| High | Safety, meaning, requirement force, or execution can change | Stop or ask before rewriting |
| Medium | A reader can misunderstand the actor, action, condition, or result | Rewrite before delivery |
| Low | The text is correct but longer, noisier, or less consistent than needed | Fix when it improves the result |
| Advisory | A heuristic found a possible issue that needs human judgment | Review in context |

## Categories and IDs

| Prefix | Category | Typical findings |
|---|---|---|
| SEM | Semantic integrity | changed modality, missing condition, invented actor, dropped exception |
| WRD | Word choice | vague word, unstable term, unapproved high-frequency term, jargon |
| VRB | Verbs and voice | passive voice, nominalization, complex tense, weak primary verb |
| SEN | Sentences | over limit, contraction, omitted word, multiple instructions |
| STR | Structure | mixed topic, long paragraph, buried result, list needed |
| SAF | Safety | wrong risk label, missing command, missing consequence |
| PUN | Punctuation | semicolon, unclear hyphenation, dense parentheses |
| PRO | Pronouns | ambiguous antecedent, unclear `this` |
| AIP | AI prose | throat-clearing, hype, canned transition, repetition, fake certainty |
| LIT | Literal integrity | changed code, identifier, URL, number, unit, or quotation |

## Readiness score

The score measures style readiness, not certification.

Start at 100 and deduct:

- 20 for each unresolved high finding.
- 8 for each medium finding.
- 2 for each low finding.
- 0 for an advisory finding until human review confirms it.

Do not report a score below zero. A high score does not prove dictionary
compliance.

## Audit issue format

```markdown
### 1. SEN-001: Sentence exceeds the profile limit

| Field | Value |
|---|---|
| Severity | medium |
| Location | line 14 |
| Profile | procedure |

**Source:** <short excerpt>

**Reader impact:** The sentence combines two instructions and hides their order.

**Fix:** Split the sentence into two imperative steps.

**Proposed wording:** <rewrite>
```

## Final audit summary

```markdown
# STE100-Style Audit

| Field | Value |
|---|---|
| Source | <file or pasted text> |
| Profile | procedure / description / safety / interface |
| Readiness | N/100 |
| Certification | Not assessed |

## Counts

| Severity | Before | After |
|---|---:|---:|
| High | N | N |
| Medium | N | N |
| Low | N | N |
| Advisory | N | N |

## Findings

<numbered findings>

## Intentional exceptions

<exception, reason, and governing source>
```
