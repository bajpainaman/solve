# Items API: schema conformance beside a stateful workflow

**Pattern:** REST / OpenAPI contract (catalog F1), stateful API workflow via links (catalog F1).
**Teaches:** a plain WSGI app checked in-process, and why a conformance test and a workflow test catch different bugs.

## The system

`app.py` is a plain WSGI callable, no framework, that stores items in a dict. `POST /items` creates one and declares two OpenAPI links, `GetById` and `DeleteById`, that feed the new item's `id` into `GET /items/{item_id}` and `DELETE /items/{item_id}`.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Every response conforms to the schema, no undocumented 5xx | schema conformance | `test_schema_conformance`, `@schema.parametrize()` |
| A deleted item is gone | stateful workflow | `test_create_get_delete_workflow`, `schema.as_state_machine().run()` |

## Run

```bash
uv run --with schemathesis --with pytest python -m pytest -q test_items.py
fv-mutate items.mutations
```

Real output, from the pinned schemathesis 4.33.4 and pytest 9.2.0:

```text
....                                                                     [100%]
4 passed in 1.77s
```

## The counterexample a planted bug produces

Planting "delete does not remove the item" and rerunning `test_create_get_delete_workflow` gives:

```text
- ST301 Deleted resource still available

    The API did not return a `HTTP 404 Not Found` response (got `HTTP 200 OK`) for a resource that was previously deleted.

    The resource was deleted with `DELETE /items/11`

[200] OK:

    `{"id": 11, "name": "POST"}`
```

Read as the system: an item was deleted, and a `GET` for the same id still returns it, so a caller that checks "is this gone" after a delete gets the wrong answer.

## Bounds and limits

`test_schema_conformance` generates cases per operation up to Schemathesis's default example budget; it is a search, not an exhaustive check. `test_create_get_delete_workflow` walks sequences the state machine builds from the declared links and from path-parameter correlation (see `references/facts.md`), not every possible sequence of calls.
