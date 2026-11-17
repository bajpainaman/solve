# Procedural writing

## Core idea

A procedure tells the reader exactly what to do and in what order. Each sentence
must be executable.

## Rules to apply

- Limit each sentence to 20 words.
- Put one instruction in each sentence unless actions must occur at the same
  time.
- Use the imperative form.
- Put a required condition before the command.
- Separate the condition from the command with a comma.
- Use notes for information only. Do not hide an instruction in a note.

## Procedure build

1. State prerequisites and conditions.
2. Write numbered steps.
3. Start each step with the primary action verb.
4. Put one action in each step.
5. State a result only when the reader must verify it.
6. Put background information outside the action sequence.

## Failure modes

- Starting every step with `Use` when another verb identifies the real action.
- Combining actions with `and` when order matters.
- Writing `You should...` instead of a command.
- Putting a mandatory step in a note.
- Moving a condition after the command it controls.

## Worked example

Weak:

> You should now use the deployment tool to perform a restart of the service and
> then check the logs.

Procedure:

1. Restart the service with the deployment tool.
2. Check the service logs.

If the log check must occur while the restart runs, keep the actions together and
state that they occur at the same time.

## Connects to

- [ch08](ch08-safety.md): safety instructions
- [ch09](ch09-punctuation.md): procedural word count
