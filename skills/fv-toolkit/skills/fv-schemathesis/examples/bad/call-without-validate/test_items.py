"""The same create -> get -> delete bug as examples/good/items-api, checked two ways.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: app.py
"""
import schemathesis

from app import app

schema = schemathesis.openapi.from_wsgi("/openapi.json", app)


@schema.parametrize()
def test_calls_without_validating(case):
    """The anti-pattern: `call()` makes the request and checks nothing about the response."""
    case.call()


def test_stateful_workflow_validated():
    """The fix: the state machine validates every response against the schema and its own checks."""
    schema.as_state_machine().run()
