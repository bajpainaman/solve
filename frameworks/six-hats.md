# Six Thinking Hats (de Bono)

**Phase:** Decide · **Source:** https://untools.co/six-thinking-hats

## Entry Predicate
`always_run` — every recommendation benefits from explicit multi-perspective evaluation.

## Inputs
- Top recommendation from Decision Matrix (or top 2-3 if matrix was inconclusive)

## Method (Parallel Fan-Out — 6 concurrent subagents)

Spawn 6 Agent subagents (`subagent_type: general-purpose` or `critic` for Black). Each writes to `$RUN_DIR/frameworks/six-hats-<color>.md`. Briefs:

### White Hat — Facts
> Role: pure objectivity. List only verifiable facts and data about the recommendation. What evidence supports it? What evidence is missing? What facts would change the call? No opinions, no emotions, no judgment.

### Red Hat — Emotions / Intuition
> Role: gut feeling without justification. Articulate the team's emotional reaction to the recommendation. What does intuition say? Where does it feel wrong even if logic supports it? Where does it feel right even if logic is mixed?

### Black Hat — Caution / Devil's Advocate
> Role: critical judgment. List every plausible failure mode of the recommendation. What's the worst-case? What hidden risks lurk? What would someone hostile to this idea say? Be relentless but specific (no FUD).

### Yellow Hat — Optimism
> Role: justified positivity. List the genuine upsides if the recommendation succeeds. What's the best plausible outcome? What second-order benefits compound? Why might this be a 10x decision?

### Green Hat — Creativity
> Role: lateral thinking. Generate 5+ alternative recommendations the matrix didn't consider. What if a constraint were lifted? What's the unconventional move? What would a different domain (biology, military, art) do here?

### Blue Hat — Process / Meta
> Role: oversight. Comment on the decision process itself. Was the right question asked? Were the right options considered? What's missing from how this run has been conducted? What should change in the methodology?

## Synthesis
After all 6 hat-files exist, synthesize:
- **Agreement** — where do ≥ 4 hats agree?
- **Tension** — where do hats conflict (especially Black vs Yellow, Red vs White)?
- **Blind spots** — what did Blue Hat flag as missing?

## Output Schema
```
WHITE: <facts summary>
RED: <gut summary>
BLACK: <risks summary>
YELLOW: <upsides summary>
GREEN: <alternatives summary>
BLUE: <process critique>

AGREEMENT: <where hats converge>
TENSION: <where hats conflict>
BLIND SPOTS: <what's missing>
```

## Decision Hook
- Agreement across ≥ 4 hats → confidence rubric +2.
- Strong Black-Hat case → feeds Dissent section.
- Green-Hat alternatives → if compelling, may trigger re-run with that option in Decision Matrix.

## What This Means For The Decision
Most decisions are made wearing one hat (usually Black or Yellow). Six Hats forces every angle to be considered explicitly. The synthesis surfaces what one perspective alone hides.
