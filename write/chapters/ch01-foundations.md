# Foundations and scope

## Core idea

ASD-STE100 is a controlled form of English for technical documentation. It
reduces ambiguity by restricting vocabulary and sentence construction.

## Apply it

Use STE discipline when a reader must understand or execute technical
information correctly. First identify whether the block is procedural or
descriptive. Apply the stricter sentence limit and command rules to procedures.

This skill adds an AI-prose overlay for general technical writing. The overlay
removes model-favored filler and hype. It is not part of the official standard.

## Mental models

- **Reader over writer**: select wording that reduces reader interpretation.
- **One term, one meaning**: consistency is more important than stylistic variety.
- **Structure before vocabulary**: prefer a different sentence construction
  when a one-word substitution would change meaning.
- **Controlled does not mean incomplete**: keep all facts, conditions,
  exceptions, and risks.

## Failure modes

- Claiming formal compliance after a heuristic check.
- Applying dictionary restrictions to code, identifiers, or command syntax.
- Removing domain terms that carry precise meaning.
- Making ordinary prose sound like an aircraft maintenance procedure.
- Strengthening a recommendation into a requirement.

## Worked example

Source:

```text
It is important to note that the deployment process may potentially result in
service disruption under certain circumstances.
```

STE-flavored:

```text
The deployment can interrupt the service.
```

Keep the original sentence if `may potentially` expresses a probability that
`can` does not preserve. Ask for the intended modality when it matters.

## Connects to

- [ch02](ch02-words.md): vocabulary control
- [ch06](ch06-procedures.md): executable instructions
- [references/rewrite-workflow.md](../references/rewrite-workflow.md): full pass
