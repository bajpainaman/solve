# Minto Pyramid

**Phase:** Decide (final synthesis) · **Source:** https://untools.co/minto-pyramid

## Entry Predicate
`always_run` — runs **last** in Phase 3, consumes all prior outputs.

## Inputs
- All Phase 1, 2, 3 framework outputs
- Computed confidence (rubric + posterior + bucket)
- Adversary findings

## Method
Build the answer top-down, not bottom-up:
1. **Question** — the canonical question (from `frameworks/productive-thinking.md::question`).
2. **Answer** — single-sentence recommendation. Top of the pyramid.
3. **Why** — 3 grouped supporting arguments (MECE).
4. For each Why, list the **evidence** (from research, frameworks, second-order analysis).

Pyramid principle: every level **summarizes** the level below; every level is **MECE**.

## Output Schema
```
QUESTION
  <canonical question>

ANSWER
  <single-sentence recommendation>

WHY
  1. <argument 1>
     - <evidence>
     - <evidence>
  2. <argument 2>
     - <evidence>
     - <evidence>
  3. <argument 3>
     - <evidence>
     - <evidence>

CONFIDENCE
  Rubric: <0-10>
  Posterior: <0-1>
  Bucket: <HIGH | MEDIUM | LOW>

DISSENT
  <continuous adversary's strongest 3 attacks>
```

## Decision Hook
Minto **is** the synthesis section in the final report. Pyramid format means a reader can stop at any level and still have a coherent answer.

## What This Means For The Decision
A decision document that buries the recommendation under 30 pages of analysis is a decision nobody reads. Minto puts the call up top, evidence below — so the decision is communicable, not just defensible.
