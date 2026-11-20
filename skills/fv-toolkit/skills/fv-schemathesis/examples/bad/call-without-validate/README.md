# Anti-pattern: `case.call()` with no validation

**Symptom:** `test_calls_without_validating` passes on an app whose delete does not delete.

`app.py` is the same item store as `examples/good/items-api/`, with `DELETE /items/{item_id}` left as a no-op. `test_calls_without_validating` makes the same generated requests as the good example's conformance test, but calls `case.call()` and never looks at the response.

Real output, from the pinned schemathesis 4.33.4 and pytest 9.2.0:

```text
...F                                                                     [100%]
=================================== FAILURES ===================================
_______________________ test_stateful_workflow_validated _______________________
...
- ST301 Deleted resource still available

    The API did not return a `HTTP 404 Not Found` response (got `HTTP 200 OK`) for a resource that was previously deleted.

    The resource was deleted with `DELETE /items/50`

[200] OK:

    `{"id": 50, "name": "integer"}`

1 failed, 3 passed in 0.95s
```

The three dots are `test_calls_without_validating`. It makes the same requests, including the delete, and passes regardless, because `case.call()` runs no check.

## The fix

Call `case.call_and_validate()`, or run a specific check function against the response `case.call()` returns. A test that only makes a request and discards the response checks nothing, however many requests it generates.

## The check that catches it

None, mechanically, for the conformance test itself; it does exactly what `case.call()` asks it to do. `test_stateful_workflow_validated`, which calls `schema.as_state_machine().run()`, validates every response by default and catches the same bug.
