"""A plain WSGI item store, with an OpenAPI schema that declares links.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository

No framework and no network: Schemathesis drives this app in-process through
`schemathesis.openapi.from_wsgi`, which calls it the way a WSGI test client
would. The two links on POST /items, GetById and DeleteById, are what let
`as_state_machine()` chain create -> get -> delete without being told to.
"""
import json

ITEMS = {}
NEXT_ID = [1]

SCHEMA = {
    "openapi": "3.0.0",
    "info": {"title": "Items", "version": "1.0.0"},
    "paths": {
        "/items": {
            "post": {
                "operationId": "createItem",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name"],
                                "properties": {"name": {"type": "string", "minLength": 1}},
                            }
                        }
                    },
                },
                "responses": {
                    "400": {"description": "the body is not a valid item"},
                    "201": {
                        "description": "created",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["id", "name"],
                                    "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
                                }
                            }
                        },
                        "links": {
                            "GetById": {
                                "operationId": "getItem",
                                "parameters": {"path.item_id": "$response.body#/id"},
                            },
                            "DeleteById": {
                                "operationId": "deleteItem",
                                "parameters": {"path.item_id": "$response.body#/id"},
                            },
                        },
                    },
                },
            }
        },
        "/items/{item_id}": {
            "get": {
                "operationId": "getItem",
                "parameters": [
                    {"name": "item_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {
                        "description": "ok",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["id", "name"],
                                    "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
                                }
                            }
                        },
                    },
                    "404": {"description": "not found"},
                },
            },
            "delete": {
                "operationId": "deleteItem",
                "parameters": [
                    {"name": "item_id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {"204": {"description": "deleted"}, "404": {"description": "not found"}},
            },
        },
    },
}


def app(environ, start_response):
    """Serve the schema and the three item operations from one in-memory dict."""
    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    def respond(status, body=None, allow=None):
        headers = [("Allow", allow)] if allow else []
        if body is None:
            start_response(status, headers)
            return [b""]
        start_response(status, headers + [("Content-Type", "application/json")])
        return [json.dumps(body).encode()]

    if path == "/openapi.json" and method == "GET":
        return respond("200 OK", SCHEMA)

    if path == "/items" and method != "POST":
        return respond("405 Method Not Allowed", allow="POST")

    if path.startswith("/items/") and method not in ("GET", "DELETE"):
        return respond("405 Method Not Allowed", allow="GET, DELETE")

    if path == "/items" and method == "POST":
        length = int(environ.get("CONTENT_LENGTH") or 0)
        try:
            body = json.loads(environ["wsgi.input"].read(length) or b"{}")
        except ValueError:
            return respond("400 Bad Request")
        if not isinstance(body, dict) or not isinstance(body.get("name"), str) or not body["name"]:
            return respond("400 Bad Request")
        item_id = NEXT_ID[0]
        NEXT_ID[0] += 1
        ITEMS[item_id] = {"id": item_id, "name": body["name"]}
        return respond("201 Created", ITEMS[item_id])

    if path.startswith("/items/"):
        try:
            item_id = int(path.rsplit("/", 1)[-1])
        except ValueError:
            return respond("404 Not Found")
        if method == "GET":
            return respond("200 OK", ITEMS[item_id]) if item_id in ITEMS else respond("404 Not Found")
        if method == "DELETE":
            ITEMS.pop(item_id, None)
            return respond("204 No Content")

    return respond("404 Not Found")
