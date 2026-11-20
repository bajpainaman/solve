# Linking a model to the code: replay and trace validation

**Pattern:** counterexample to regression test, and trace validation (the "Linking" table of the shared `linking.md`).
**Teaches:** `fv-replay` turns a counterexample into a test on the real code. `fv-conform` checks a recorded run of the real code against the spec.

Both examples use the model in `../good/refund-race/` and the toy service in `refunds.py`, which has the two designs of that model.

## Replay: from the model to the code

`fv-replay` runs a config that produces a violation and writes a pytest file with the counterexample as data. The test drives the code through the same steps and checks the property after each one.

```bash
fv-replay ../good/refund-race/RefundRace.tla ../good/refund-race/CheckThenRefund.cfg -o test_replay_check_then_refund.py
python -m pytest -q test_replay_check_then_refund.py
```

`conftest.py` holds the driver, which you write once per model. It maps each action of the model to a call on the code, and its `check` method asserts the property on the code's own state.

| Driver method | What it does here |
|---|---|
| `reset(state)` | Creates the service with a payment of 10 |
| `step(action, changed, state)` | Calls `check` or `refund` for the job whose program counter moved |
| `check()` | Asserts that the refunded total is at most the payment |

On the check-then-refund service, the replay fails at the last step:

```text
E       AssertionError: refunded 20 on a payment of 10
FAILED test_replay_check_then_refund.py::test_checkthenrefund_counterexample
```

The counterexample now has the disposition "reproduced". On the atomic service, selected with `REFUND_DESIGN=atomic`, the same test passes, so the test is red on the design with the bug and green on the fix.

## Trace validation: from the code to the model

`record.py` runs one schedule on a service and prints one log line per step, with the state the service exposes after the step. `fv-conform` asks TLC whether some behaviour of the spec matches every line.

```bash
python record.py check-then-refund > logs/check_then_refund.jsonl
fv-conform ../good/refund-race/RefundRace.tla ../good/refund-race/CheckThenRefund.cfg logs/check_then_refund.jsonl
```

```text
PASS trace check_then_refund.jsonl: accepted (5 events)
```

The log of the atomic service is not a behaviour of the check-then-refund design. The second refund leaves the total at 10, and that design can only move it to 20.

```text
FAIL trace atomic.jsonl: expected accepted, got rejected at event 5: {"event": "refund", "job": "b", "vars": {"refunded": 10}}
```

Here the rejection has a good cause: the code was fixed, and the config under check still describes the old design. This is the drift that `fv-maintain` looks for. A rejection can also mean a bug in the code or an error in the log mapping, so check the mapping first.

## Limits

- The log holds only `refunded`. A log with more variables rejects more wrong behaviours.
- `fv-conform` takes one log line for one step of the spec. Code that logs twice inside one atomic step, or once across two, needs its log mapped first.
- The replay test checks one schedule. It is a regression test for that counterexample, and it says nothing about other schedules.
