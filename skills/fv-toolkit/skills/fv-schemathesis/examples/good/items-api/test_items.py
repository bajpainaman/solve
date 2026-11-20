"""Schema conformance and the create -> get -> delete workflow for the items API.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: app.py
"""
import schemathesis

from app import app

schema = schemathesis.openapi.from_wsgi("/openapi.json", app)


@schema.parametrize()
def test_schema_conformance(case):
    """Every generated request gets a response the schema allows."""
    case.call_and_validate()


def test_create_get_delete_workflow():
    """A deleted item is gone: `use_after_free` walks every link schemathesis declares."""
    schema.as_state_machine().run()
