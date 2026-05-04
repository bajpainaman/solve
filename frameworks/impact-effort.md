# Impact-Effort Matrix

**Phase:** Decide · **Source:** https://untools.co/impact-effort-matrix

## Entry Predicate
`always_run` if Decision Matrix has multiple options; useful as a sanity check.

## Inputs
- Options from `frameworks/decision-matrix.md`

## Method
Plot each option on a 2×2: Impact (low/high) × Effort (low/high).

## Output Schema
```
              EFFORT
              Low                   High
   ┌───────────────────┬───────────────────┐
H  │   QUICK WINS      │   BIG BETS        │
i  │   (do these)      │   (commit if      │
g  │                   │    confident)     │
h  │                   │                   │
   ├───────────────────┼───────────────────┤
L  │   FILL-INS        │   THANKLESS       │
o  │   (low priority)  │   (avoid)         │
w  │                   │                   │
   └───────────────────┴───────────────────┘
        IMPACT
```

| Option | Impact (L/H) | Effort (L/H) | Quadrant |
|---|---|---|---|
| Option A | H | L | Quick Win |
| Option B | H | H | Big Bet |
| Option C | L | H | Thankless |

## Decision Hook
- Quick Wins → recommend immediate action (combine with top Decision Matrix option if compatible).
- Big Bets → require highest confidence (rubric ≥ 8) before committing.
- Thankless → flag in Dissent as "considered and rejected."

## What This Means For The Decision
Decision Matrix tells you which option scores best on criteria. Impact-Effort tells you whether it's worth the cost. Both matter — a high-criteria option that's also Thankless quadrant is rarely the right move.
