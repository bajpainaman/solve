---
name: fv-schemathesis
description: "Generates and runs requests against an OpenAPI schema and the real app behind it: schema conformance (status codes and bodies that match the spec, no 5xx), and stateful workflows such as create, get, update, delete that chain across several operations. Every check must fail on a planted bug in the app, never only on the schema. Use for REST/OpenAPI contract testing, fuzzing an API from its spec, or 'does this response match what we documented', or when the formal-verification skill routes here. Not for a Python function's own contracts with no HTTP layer (use fv-crosshair) or for request sequences with no OpenAPI spec to drive them (use fv-hypothesis stateful testing)."
---

# Schemathesis

Schemathesis reads an OpenAPI schema, generates requests from it, and checks each response against the schema and against a small set of built-in checks: no undocumented 5xx, no schema-violating body, no stale resource after it was deleted. It runs the real app in-process, through a WSGI or ASGI test client, so a bug in the app is a bug in the test, not a flaky network call.

If you came here directly, run steps 1 to 3 of the `formal-verification` skill first. They produce the claims table and the confirmed property ledger.

Pytest already prints `FAILED <file>::<test>` on a Schemathesis failure, so this skill needs no wrapper. Drive every check through `python -m pytest`, the same as `fv-hypothesis`.

## Five rules

1. **Validate the response, not just the request.** `case.call()` only makes the HTTP call. Nothing about the response is checked until `case.call_and_validate()` runs, or until a `response.raise_for_status()`-style assertion follows the call.
2. **State the response shape you actually expect.** A response schema with no `type`, no `required` field and no bound on a number accepts any JSON, so `response_schema_conformance` has nothing to compare against.
3. **Drive the real app in-process.** `schemathesis.openapi.from_wsgi` or `from_asgi` calls the app directly, with no network and no server process to start or stop.
4. **A stale resource needs a stateful check.** `schema.as_state_machine().run()` runs `use_after_free` and the other cross-call checks by default. A plain `@schema.parametrize()` test only ever sees one request at a time, so a resource that is still readable after being deleted looks fine to it.
5. **Keep the request body required when it is.** `requestBody.required: true` is what makes a missing body schema-invalid; without it, a request with no body is schema-valid, and a server that rejects it fails `positive_data_acceptance` for a reason that has nothing to do with the bug under test.

## Files to write

| File | Holds |
|---|---|
| `app.py` | The app under test, built as a plain WSGI or ASGI callable, and the OpenAPI schema it serves from `/openapi.json` |
| `test_<name>.py` | One `@schema.parametrize()` test that calls `case.call_and_validate()`, and one plain test function that calls `schema.as_state_machine().run()` when the schema has an operation sequence worth walking |
| `<name>.mutations` | The planted bugs, as `${CLAUDE_PLUGIN_ROOT}/references/bite.md` describes |
| `README.md` | The property ledger, the command table, the bounds and limits |

Copy `examples/good/items-api/` to start.

## Workflow

1. **Build the app in-process** as a WSGI or ASGI callable, and write its OpenAPI schema. A path parameter's type and an operation's declared responses, including the error ones, are part of the claim, not boilerplate.
2. **Write the schema-conformance test.**
3. **Run it.**

   ```bash
   uv run --with schemathesis --with pytest python -m pytest -q test_<name>.py
   ```

4. **Add the stateful workflow test** when the schema has operations that build on each other's results.
5. **Plant bugs.**

   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate <name>.mutations
   ```

## What a pass means

A pass means the generated cases, including Schemathesis's own boundary and negative-data probes, raised no failure within the run's example budget. It is a search over the schema's input space, not an exhaustive check, and `derandomize=True` makes it repeatable the same way it does for `fv-hypothesis`.

## Examples

`examples/INDEX.md` lists every example. `examples/good/items-api/` checks schema conformance and a create/get/delete workflow against a WSGI app, with mutations. `examples/bad/schema-too-loose/` and `examples/bad/call-without-validate/` reproduce rules 2 and 1 above.

## References

| File | Read when |
|---|---|
| `references/anti-patterns.md` | You review a Schemathesis test, yours or someone else's |
| `references/facts.md` | You need a fact measured on the pinned version, such as what `as_state_machine()` needs to chain operations |
| `${CLAUDE_PLUGIN_ROOT}/references/bite.md` | You write the mutations file |
