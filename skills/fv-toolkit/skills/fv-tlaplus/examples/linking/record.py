"""Run one schedule on a refund service and print one log line per step.

Usage: python record.py check-then-refund|atomic > logs/<name>.jsonl

The schedule is the one the model checker found: both jobs read, then both refund.
Each line holds the state that the service exposes after the step.
"""
import json
import sys

from refunds import AtomicRefund, CheckThenRefund

service = (AtomicRefund if sys.argv[1] == "atomic" else CheckThenRefund)(10)
print(json.dumps({"event": "init", "vars": {"refunded": service.refunded}}))
for event, job in [("check", "a"), ("check", "b"), ("refund", "a"), ("refund", "b")]:
    getattr(service, event)(job)
    print(json.dumps({"event": event, "job": job, "vars": {"refunded": service.refunded}}))
