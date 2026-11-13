# Safety instructions

## Core idea

A safety instruction must identify the risk level, tell the reader how to avoid
the risk, and state the possible result.

## Risk labels

- **WARNING**: injury or death can occur.
- **CAUTION**: damage to an object can occur.
- **Both**: use `WARNING`.

Other industries can use different labels. Obey the governing safety standard.

## Safety triad

1. Select the risk label from an actual risk analysis.
2. Start with a clear command or condition.
3. State the risk or possible result.

Put a condition first when the reader must know it before acting.

## Failure modes

- Guessing the risk level from wording alone.
- Using a caution for a combined damage and injury risk.
- Stating that something is dangerous without telling the reader what to do.
- Giving a command without explaining the consequence.
- Adding a consequence that the source does not support.

## Worked example

Incomplete:

```text
Be careful when you rotate the key.
```

Structured form:

```text
CAUTION: Before you rotate the key, release the lock. The key can break if the
lock remains engaged.
```

Use this rewrite only if the source confirms object damage and the stated cause.
If injury is possible, the label and consequence need a domain review.

## Connects to

- [ch06](ch06-procedures.md): conditions and commands
- [references/finding-taxonomy.md](../references/finding-taxonomy.md): high
  severity safety findings
