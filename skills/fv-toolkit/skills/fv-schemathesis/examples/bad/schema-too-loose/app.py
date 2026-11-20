"""Two WSGI apps sharing one bug, described by a loose schema and a tight one.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository

GET /total always returns a negative count, a real bug. The loose schema
declares no shape for the response body, so Schemathesis has nothing to check
it against. The tight schema states what the field actually is.
"""
import json


def _total_body(environ, start_response):
    if environ["REQUEST_METHOD"] != "GET":
        start_response("405 Method Not Allowed", [("Allow", "GET")])
        return [b""]
    start_response("200 OK", [("Content-Type", "application/json")])
    return [json.dumps({"total": -1}).encode()]  # the bug: a count can never be negative


def _openapi(schema):
    def handler(environ, start_response):
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(schema).encode()]

    return handler


def _make_app(schema):
    serve_schema = _openapi(schema)

    def app(environ, start_response):
        if environ["PATH_INFO"] == "/openapi.json":
            return serve_schema(environ, start_response)
        if environ["PATH_INFO"] == "/total":
            return _total_body(environ, start_response)
        start_response("404 Not Found", [])
        return [b""]

    return app


LOOSE_RESPONSE = {}  # accepts any JSON at all
TIGHT_RESPONSE = {
    "type": "object",
    "required": ["total"],
    "properties": {"total": {"type": "integer", "minimum": 0}},
}


def _schema(response_body_schema):
    return {
        "openapi": "3.0.0",
        "info": {"title": "Totals", "version": "1.0.0"},
        "paths": {
            "/total": {
                "get": {
                    "operationId": "getTotal",
                    "responses": {
                        "200": {
                            "description": "ok",
                            "content": {"application/json": {"schema": response_body_schema}},
                        }
                    },
                }
            }
        },
    }


loose_app = _make_app(_schema(LOOSE_RESPONSE))
tight_app = _make_app(_schema(TIGHT_RESPONSE))
