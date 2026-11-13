# Descriptive writing

## Core idea

Give information gradually. Let the reader understand the system before you
present details and exceptions.

## Rules to apply

- Limit each sentence to 25 words.
- Use key terms and phrases to make the structure visible.
- Put related information in one paragraph.
- Keep one topic per paragraph.
- Limit each paragraph to six sentences.

## Recommended order

1. Purpose or primary result.
2. Main components or actors.
3. Normal behavior.
4. Conditions and state changes.
5. Exceptions, limits, and failure behavior.
6. Example or evidence.

## Failure modes

- Opening with implementation detail before the reader knows the purpose.
- Mixing architecture, setup steps, and limitations in one paragraph.
- Repeating the same summary before and after a list.
- Using a heading that does not match the paragraph topic.

## Worked example

Weak:

```text
By leveraging a distributed architecture and asynchronous processing, the
platform provides a robust and scalable solution that can help teams manage
workloads in a seamless manner.
```

Clear:

> The platform assigns each job to a worker queue. Workers process jobs
> asynchronously. The queue lets the service add workers when the pending job
> count increases.

The rewrite replaces claims with a mechanism. It does not call the system
scalable without a defined limit or measurement.

## Connects to

- [ch05](ch05-sentences.md): sentence structure
- [references/ai-prose-overlay.md](../references/ai-prose-overlay.md): evidence
  instead of hype
