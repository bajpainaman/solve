---
name: test-contract
description: "Writes consumer-driven contract tests with Pact for two services, or a frontend and an API, that keep breaking each other. The consumer test records only the fields the consumer reads, the provider verifies against its real implementation, and deploys are gated with can-i-deploy. Use for contract tests, Pact, consumer-driven contracts, provider verification, a pact broker, \"the API changed and broke the client\", a new client of another service, or when the testing skill routes here. Not for testing one service against its own database (use test-integration) or a full user journey (use test-e2e)."
---

# Contract tests

A contract test checks the agreement between a consumer and a provider without running both together. The consumer states what it sends and what it reads. The provider replays those interactions against its real code. A broker stores the contracts and answers whether a version is safe to deploy.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` for every test. This file adds the rules that are specific to contract tests.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| pact-python | pact-js | pact-jvm | pact-go | pact-rust through the FFI |

Check the installed Pact version before you write, because the API differs between major versions.

## Five rules

1. **Record only the fields the consumer reads.** Read the consumer's code and list the fields it uses from each response. The expected body holds those fields and no others, so that the provider stays free to change the rest.
2. **Match on type and shape.** Use the library's matchers for types, patterns and array shapes. Use an exact value only where the consumer branches on that value, such as a status enum.
3. **Call the real client code.** The consumer test drives the consumer's own HTTP client against the Pact mock server. A test that calls the mock server with a raw HTTP library tests nothing of the consumer.
4. **Verify the provider against its real implementation.** Each interaction names a provider state, and the provider sets that state up with real data before it replays the request. Never verify against a stub of the provider.
5. **Publish, gate and record.** Publish each pact with the commit SHA and the branch. Run `can-i-deploy` before every deploy, and run `record-deployment` after it. Without deployment records the broker can't say which versions are in an environment.

## Reject the test if

- The expected body lists a field that the consumer never reads.
- Every value is matched exactly, and the consumer does not branch on those values.
- The pipeline has no `record-deployment` step, so `can-i-deploy` has nothing to reason about.

## Workflow

1. **List what the consumer uses.** For each call, write the request it sends and the fields it reads. This is the contract, and it comes from the consumer's code.
2. **Apply step 0** of assured generation. The credible bug is a provider change that breaks this consumer: a renamed field, a changed type, a removed enum value.
3. **Write the consumer test**, one interaction per behaviour the consumer depends on, including the error responses it handles.
4. **Write the provider verification** with a state handler for every provider state.
5. **Add the pipeline steps**, with the commands below.
6. **Report** with the table from step 6 of assured generation. For each interaction, list the fields recorded and the fields left out on purpose.

```bash
pact-broker publish ./pacts --consumer-app-version "$GIT_SHA" --branch "$GIT_BRANCH"
pact-broker can-i-deploy --pacticipant orders-web --version "$GIT_SHA" --to-environment production
pact-broker record-deployment --pacticipant orders-web --version "$GIT_SHA" --environment production
```

## The report

End your reply with this table, even when you wrote one interaction. The user reads it to decide whether each row earns its place.

| Interaction | What the consumer depends on | Provider change that would break it | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

The consumer shows an order's `id` and `status`, and it branches on `status`. The provider's response also holds `customer`, `lines` and `created_at`.

```js
// Bad. The body copies the provider's whole response with exact values. A
// provider that renames `customer.tier` now breaks a consumer that never reads it.
willRespondWith({ status: 200, body: { id: 42, status: 'shipped',
  customer: { id: 7, tier: 'gold' }, lines: [{ sku: 'A1', qty: 2 }], created_at: '2026-01-05T10:00:00Z' } })
```

```js
// Good. The body holds the two fields the consumer reads. The id is matched
// by type, and the status is matched by the values the consumer branches on.
provider
  .given('order 42 exists and has shipped')
  .uponReceiving('a request for order 42')
  .withRequest({ method: 'GET', path: '/orders/42' })
  .willRespondWith({
    status: 200,
    body: { id: integer(42), status: regex('pending|shipped|cancelled', 'shipped') },
  });
```

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | You add the publish, gate and record steps to CI |
