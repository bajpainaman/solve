# Ladder of Inference

**Phase:** Decide · **Source:** https://untools.co/ladder-of-inference

## Entry Predicate
`always_run` — sanity check on the team's reasoning.

## Inputs
- Top recommendation from Decision Matrix
- Evidence used to support it

## Method
Trace the reasoning that produced the recommendation, climbing the ladder:
1. **Observable data** — raw facts, evidence, research.
2. **Selected data** — which facts the team focused on (and which were ignored).
3. **Interpreted meaning** — what those facts were taken to mean.
4. **Assumptions** — beliefs added to make the meaning coherent.
5. **Conclusions** — the recommendation.
6. **Beliefs** — generalizations from this conclusion that will affect future decisions.
7. **Action** — what gets done.

For each rung, write the explicit content. Highlight where unjustified leaps occur.

## Output Schema
```
RUNG 7: ACTION
  → <action>
RUNG 6: BELIEFS
  → <belief>
RUNG 5: CONCLUSIONS
  → <conclusion>
RUNG 4: ASSUMPTIONS
  → <assumption>          [TEST: how could this be false?]
RUNG 3: INTERPRETED MEANING
  → <meaning>
RUNG 2: SELECTED DATA
  → <data>                [IGNORED: <data>]
RUNG 1: OBSERVABLE DATA
  → <fact>
```

## Decision Hook
Any **unjustified leap** between rungs is a vulnerability. The adversary subagent receives the ladder and challenges the weakest leap as part of Dissent.

## What This Means For The Decision
Decisions feel obvious because the team skipped rungs unconsciously. Making the ladder explicit reveals where confidence is borrowed instead of earned.
