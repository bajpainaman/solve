# Schemathesis anti-patterns

Each row is a way a check passes while it proves nothing, with the symptom and the fix.

| Anti-pattern | Symptom | Fix / check |
|---|---|---|
| `case.call()` with no validation | Every generated case "passes," because nothing about the response was ever checked | Use `case.call_and_validate()`, or call a check function directly on the response. See `examples/bad/call-without-validate/` |
| A response schema with no `type`, `required` or bound | `response_schema_conformance` never fails, because any JSON satisfies an empty schema | State what the field actually is. See `examples/bad/schema-too-loose/` |
| `requestBody` with no `required: true` | A request with an empty body is schema-valid, so a server that rejects it fails `positive_data_acceptance` for a reason unrelated to the bug under review | Mark the body `required` when the operation needs one |
| Testing only `@schema.parametrize()`, never `as_state_machine()` | A resource that is still readable after being deleted looks fine, because each request is checked on its own | Add the stateful workflow test; `use_after_free` runs by default inside it |
| Reading `1 failed, 3 passed` as "the API is 75% correct" | The count mixes unrelated operations; one failing operation can hide behind three unrelated passing ones | Read which test id failed, not the ratio |
