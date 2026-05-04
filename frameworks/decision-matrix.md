# Decision Matrix (Weighted Criteria)

**Phase:** Decide · **Source:** https://untools.co/decision-matrix

## Entry Predicate
`always_run` if `|options| ≥ 2`; skip if only 1 option survives prior phases.

## Inputs
- Options from `frameworks/zwicky-box.md::archetypes` ∪ `frameworks/productive-thinking.md::forged_solutions`
- Constraints from `frameworks/inversion-define.md::constraints` (act as disqualifiers)
- Success criteria from `intake.success_criteria`

## Method
1. List **options** (rows). Disqualify any that violate inversion-define constraints (score 0).
2. List **criteria** (columns) derived from success criteria + research evidence.
3. Assign **weights** (1-10) to each criterion. Justify each weight.
4. Score each option × criterion (0-10).
5. Compute weighted scores: `score(option) = Σ (weight_i × score_i,option)`.
6. Rank.

## Output Schema (table)
| Option | Criterion 1 (w=8) | Criterion 2 (w=5) | Criterion 3 (w=7) | **Total** |
|---|---|---|---|---|
| Option A | 9 (72) | 6 (30) | 7 (49) | **151** |
| Option B | 7 (56) | 9 (45) | 8 (56) | **157** |
| Option C | 5 (40) | 8 (40) | 4 (28) | **108** |

Top option: **B** (157)

## Decision Hook
- If top option ≥ 1.5× second option → confidence rubric +2.
- If top three within 10% of each other → flag for Hard Choice or re-run with refined criteria.
- Top option becomes the **recommendation**.

## What This Means For The Decision
The matrix forces the team to make weights explicit. If two people pick different options, they almost always have different weights — surfacing the disagreement is half the value.
