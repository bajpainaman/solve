---
name: test-data
description: "Writes tests for dbt models, ETL jobs and warehouse tables. dbt unit tests with static mock rows check the transformation logic, schema and data tests check uniqueness, nulls, relationships and freshness on real data, and each test has a severity so that a warning does not block the pipeline. Use for dbt tests, dbt unit tests, data quality tests, Great Expectations, Soda, testing a SQL model or a pipeline, a data diff on a pipeline change, or when the testing skill routes here. Not for application code that queries a database (use test-integration)."
---

# Data tests

A pipeline fails in two ways. The transformation logic is wrong, or the data that arrives is not what the logic assumes. Each needs its own kind of test: a unit test with fixed rows for the logic, and data tests on real rows for the assumptions.

Follow `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` for every test. This file adds the rules that are specific to data tests.

Tools: dbt data tests and dbt unit tests, Great Expectations, Soda. Use what the project already has.

## Five rules

1. **Unit-test the transformation logic with static rows.** A dbt unit test gives mock input rows and the expected output rows. Use one for each rule in the SQL: a `case` branch, a join that can fan out, a window, a date boundary, a null.
2. **Write the expected rows from the spec.** Take them from the model's description, the ticket or the metric definition. Never run the model and paste its output.
3. **Put data tests where the data enters.** Test sources and staging models for `unique`, `not_null`, `accepted_values` and `relationships`, and add freshness to sources. A check that exists only on the final mart reports a problem far from its cause.
4. **Set a severity on every test.** A broken primary key is an `error` and stops the run. A soft expectation, such as a rare null in an optional column, is a `warn`. When every check blocks, the pipeline alerts all the time and people stop reading the alerts.
5. **Test the grain.** State the grain of each model in one line, and test it with `unique` on the key or a uniqueness test on the combination of columns.

## Reject the tests if

- They exist only on the final marts.
- Every check has the default blocking severity.
- A unit test's expected rows were pasted from the model's own output.

## Workflow

1. **Read the spec of the model**: its description, its grain, and the rules it applies.
2. **Apply step 0** of assured generation. The credible bugs are a join that duplicates rows, a wrong sign, a wrong date boundary, a null that falls out of a filter, and a duplicate key from upstream.
3. **Write the unit tests**, one per rule, with the smallest rows that show the rule.
4. **Write the data tests** on sources and staging, each with a severity.
5. **Run** `dbt build --select <model>+`. When no warehouse is available, write the tests and list the run under "Not run".
6. **For a change to an existing model**, compare the table before and after the change, and explain every difference.
7. **Report** with the table from step 6 of assured generation.

## The report

End your reply with this table, even when you wrote one test. The user reads it to decide whether each row earns its place.

| Test | Rule or assumption it protects | Bug or bad data that would make it fail | Evidence |
|---|---|---|---|

In the last column, write what you saw: a planted bug that made it fail, a failing run on the current code, or "not run". Under the table, list each finding, each step that did not run and why, and the command that runs everything.

## Example

```yaml
# Bad. The only tests are on the mart, each one blocks, and no test
# checks the refund rule in the SQL.
models:
  - name: fct_revenue
    columns:
      - name: revenue_cents
        data_tests: [not_null]
```

```yaml
# Good. A unit test fixes the refund rule with rows from the spec. The key is
# tested where the data enters, and the soft expectation is a warning.
unit_tests:
  - name: refund_counts_as_negative_revenue
    model: fct_revenue
    given:
      - input: ref('stg_payments')
        rows:
          - {payment_id: 1, order_id: 10, amount_cents: 1000, kind: charge}
          - {payment_id: 2, order_id: 10, amount_cents: 400, kind: refund}
    expect:
      rows:
        - {order_id: 10, revenue_cents: 600}

sources:
  - name: billing
    freshness:
      warn_after: {count: 6, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _loaded_at
    tables:
      - name: payments

models:
  - name: stg_payments
    columns:
      - name: payment_id
        data_tests: [unique, not_null]
      - name: kind
        data_tests:
          - accepted_values: {values: [charge, refund]}
      - name: customer_email
        data_tests:
          - not_null:
              config: {severity: warn}
```

Check the keys against the installed dbt version. Unit tests need dbt 1.8 or later, and older versions name data tests `tests`.

## References

| File | Read when |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/references/assured-generation.md` | Always, before the first test |
| `${CLAUDE_PLUGIN_ROOT}/references/pipeline.md` | You place the tests in a CI stage |
