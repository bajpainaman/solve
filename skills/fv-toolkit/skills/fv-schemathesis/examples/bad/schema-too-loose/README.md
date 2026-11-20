# Anti-pattern: a response schema so loose nothing can violate it

**Symptom:** `test_loose_schema_conformance` passes on a response that is always wrong.

`app.py` serves the same broken `GET /total`, which always returns `{"total": -1}`, from two WSGI apps. `loose_app` describes the response body with `{}`, an empty schema that accepts any JSON. `tight_app` describes it as `{"type": "object", "required": ["total"], "properties": {"total": {"type": "integer", "minimum": 0}}}`.

Real output, from the pinned schemathesis 4.33.4 and pytest 9.2.0:

```text
.F                                                                       [100%]
=================================== FAILURES ===================================
__________________ test_tight_schema_conformance[GET /total] ___________________
...
- ST108 Response violates schema

    -1 is less than the minimum of 0

    Validated against the response schema for status code 200.

    Schema at /properties/total:

        {
            "minimum": 0,
            "type": "integer"
        }

    Value:

        -1

[200] OK:

    `{"total": -1}`
```

`test_loose_schema_conformance`, the first dot, passes on the exact same bug, because `response_schema_conformance` has nothing in the schema to compare `-1` against.

## The fix

State what the field actually is: its type, whether it is required, and any bound that matters, such as "never negative." A schema that says nothing enforces nothing.

## The check that catches it

`response_schema_conformance`, but only once the schema states a shape narrow enough to rule the bug out. Review a response schema the same way you would review an assertion: ask what value would still pass it.
