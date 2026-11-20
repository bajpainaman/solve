"""The same bug, checked against a loose schema and a tight one.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: app.py
"""
import schemathesis

from app import loose_app, tight_app

loose_schema = schemathesis.openapi.from_wsgi("/openapi.json", loose_app)
tight_schema = schemathesis.openapi.from_wsgi("/openapi.json", tight_app)


@loose_schema.parametrize()
def test_loose_schema_conformance(case):
    """The anti-pattern: the response schema declares no shape, so nothing can violate it."""
    case.call_and_validate()


@tight_schema.parametrize()
def test_tight_schema_conformance(case):
    """The fix: the response schema states that the count is never negative."""
    case.call_and_validate()
