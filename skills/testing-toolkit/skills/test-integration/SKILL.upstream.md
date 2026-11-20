---
name: test-integration
description: "Writes integration and component tests for code whose bugs are at the database, cache, queue or filesystem boundary. Runs the real dependency in a disposable container with Testcontainers, at the version production runs, with fresh state for every test. Also writes fault-injection tests with Toxiproxy for timeouts, 5xx and slow responses. Use for integration tests, repository or DAO tests, SQL, migrations, Redis, Kafka, Testcontainers, \"test against a real Postgres\", or when the testing skill routes here. Not for pure logic (use test-unit) or for the agreement between two services (use test-contract)."
---

# Integration tests

An integration test runs the code against the real dependency. It exists because SQL dialects, constraints, transactions and serialisation behave differently in a mock or an in-memory substitute, and those differences are where this code breaks.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` for every test. This file adds the rules that are specific to integration tests.

| Python | TypeScript / JS | JVM | Go | Rust |
|---|---|---|---|---|
| pytest + testcontainers-python | Testcontainers Node | Testcontainers Java | testcontainers-go | testcontainers-rs |

## Five rules

1. **Use the real dependency in a disposable container.** Never replace Postgres with SQLite or H2, and never mock the driver or the connection.
2. **Pin the image to the production version.** Read the version from the compose file, the Dockerfile, the infra config or the migrations. Write `postgres:16.4`, never `postgres:latest`.
3. **Give every test fresh state.** Start the container once per session, and isolate each test with a rolled-back transaction, a truncate, or a database cloned from a template. No test reads a row that another test wrote.
4. **Build the schema with the real migrations.** A schema written by hand in the test drifts from the one production runs.
5. **Test through the code's own boundary.** Call the repository, the handler or the consumer, and assert on what it returns or stores. Assert on the outcome of the SQL, never on the SQL text.

## Reject the test if

- It uses H2, SQLite or an in-memory fake in place of the production store.
- Tests share state, or pass only in one order.
- The image tag is `latest` or differs from production without a stated reason.

## Workflow

1. **Find the boundary and the spec.** Name the dependency, its production version and the behaviour the code promises at that boundary: uniqueness, ordering, upsert semantics, isolation, retries.
2. **Apply step 0** of assured generation. The credible bug here usually needs the real engine to appear: a constraint violation, a conflict, a dialect feature, a transaction that does not roll back.
3. **Write the fixture**: one container per session, the real migrations, and isolation per test.
4. **Write the tests** through the code's boundary.
5. **Run the steps** of assured generation. When Docker is not available, write the tests anyway and list steps 2 to 4 under "Not run". Never switch to an in-memory store to get a passing run.
6. **Report** with the table from step 6 of assured generation, plus the image and its version.

## Fault injection

For a client of another service or a store, add tests that put Toxiproxy between the code and the dependency. Cover a timeout, a 5xx or a dropped connection, and a slow response. Each test asserts what the caller promises in that case: a retry, a fallback, or a clear error.

## The report

End your reply with this table, even when you wrote one test. The user reads it to decide whether each row earns its place.

| Test | Contract it protects | Bug that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```python
# Bad. SQLite accepts this insert, and the mock asserts the call. The upsert
# under test uses ON CONFLICT, which the test never executes on Postgres.
def test_save_user():
    repo = UserRepo(sqlite3.connect(":memory:"))
    repo.save(User(email="a@example.com"))
```

```python
# Good. The engine and the version match production, the schema comes from
# the migrations, and each test runs in a transaction that is rolled back.
@pytest.fixture(scope="session")
def pg():
    with PostgresContainer("postgres:16.4") as container:
        run_migrations(container.get_connection_url())
        yield container

@pytest.fixture
def conn(pg):
    with connect(pg.get_connection_url()) as c, c.transaction(force_rollback=True):
        yield c

def test_saving_the_same_email_twice_keeps_one_row_with_the_latest_name(conn):
    repo = UserRepo(conn)
    repo.save(User(email="a@example.com", name="Ada"))
    repo.save(User(email="a@example.com", name="Ada L."))
    assert repo.find_by_email("a@example.com").name == "Ada L."
    assert repo.count() == 1
```

Check the fixture calls against the installed Testcontainers version before you rely on them, because the helper names differ between versions.

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/anti-patterns.md` | Before you show the tests |
