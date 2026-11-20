#!/usr/bin/env python3
"""Deterministic simulation of primary-backup replication under crash, loss and duplication.

Source read at: 0000000
Covers: no real repository; this models the primary-backup pattern of
catalog B3, not a file in this project.

Usage:
  simulate.py --policy {commit-after-replicate,ack-then-replicate} --sweep N [--steps N] [--seed-start N]
  simulate.py --policy {commit-after-replicate,ack-then-replicate} --replay SEED [--steps N]

One seeded scheduler owns every nondeterministic choice in run(): which
enabled task runs next, message delay, loss, duplication, and node crash and
restart. Nothing here reads the wall clock or calls the unseeded `random`
module functions, so --replay SEED reproduces one run exactly.

The primary replicates every write to the backup. Two policies decide when
the client is told a write succeeded:

  commit-after-replicate   the client is acked only once the backup has
                            applied the entry (the chosen design)
  ack-then-replicate       the client is acked as soon as the primary
                            appends locally, before the backup applies it
                            (the rejected design)

At the last step the primary crashes permanently and the backup is promoted.

Property NeverAckedWriteLost: every index the client was told succeeded is
present in the promoted backup's log.

Verdict lines:
  PASS sweep NeverAckedWriteLost: holds for N seeds
  FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed S
  PASS replay NeverAckedWriteLost: holds
  FAIL replay NeverAckedWriteLost: expected holds, got violated

Exit codes: 0 pass, 1 fail, 2 usage error.
"""
import argparse
import random
import sys

P_LOSS = 0.15
P_DUP = 0.1
P_CRASH = 0.08
P_RESTART = 0.4
DELAY_RANGE = (1, 3)


class Node:
    """One replica. `log` is durable storage: a crash must never clear it."""

    def __init__(self):
        self.log = []  # list of (index, value); durable
        self.alive = True


def run(seed, steps, policy):
    """Run one deterministic simulation and return (violated_indices, trace)."""
    rng = random.Random(seed)
    primary, backup = Node(), Node()
    acked = set()  # ground truth: indices the client was told succeeded
    pending = {}  # primary-only, volatile: index -> value awaiting the backup's ack
    in_flight = []  # list of [deliver_tick, kind, payload]
    next_index = 0
    trace = []

    def send(deliver_tick, kind, payload):
        in_flight.append([deliver_tick, kind, payload])
        if rng.random() < P_DUP:
            in_flight.append([deliver_tick, kind, payload])
            trace.append(f"  duplicate of {kind} {payload} is also scheduled")

    for tick in range(steps):
        actions = []
        if primary.alive:
            actions += ["submit", "primary_crash"]
        else:
            actions.append("primary_restart")
        if backup.alive:
            actions.append("backup_crash")
        else:
            actions.append("backup_restart")
        due = [m for m in in_flight if m[0] <= tick]
        actions.extend(["deliver"] * len(due))

        choice = rng.choice(actions)
        if choice == "submit":
            entry = (next_index, f"v{next_index}")
            primary.log.append(entry)
            if policy == "ack-then-replicate":
                acked.add(entry[0])
                trace.append(f"tick {tick}: primary appends {entry} and acks it immediately")
            else:
                pending[entry[0]] = entry[1]
                trace.append(f"tick {tick}: primary appends {entry} and waits for the backup")
            if rng.random() < P_LOSS:
                trace.append(f"tick {tick}: replicate{entry} is lost")
            else:
                send(tick + rng.randint(*DELAY_RANGE), "replicate", entry)
            next_index += 1
        elif choice == "primary_crash":
            primary.alive = False
            forgotten = sorted(pending)
            pending.clear()  # volatile state does not survive a crash
            trace.append(f"tick {tick}: primary crashes, forgetting pending acks {forgotten}")
        elif choice == "primary_restart":
            primary.alive = True
            trace.append(f"tick {tick}: primary restarts with its durable log intact")
        elif choice == "backup_crash":
            backup.alive = False
            trace.append(f"tick {tick}: backup crashes")
        elif choice == "backup_restart":
            backup.alive = True
            trace.append(f"tick {tick}: backup restarts with its durable log intact")
        elif choice == "deliver":
            msg = rng.choice(due)
            in_flight.remove(msg)
            _, kind, payload = msg
            index, value = payload
            if backup.alive:
                backup.log.append((index, value))
                trace.append(f"tick {tick}: backup applies {payload}")
                if primary.alive and policy == "commit-after-replicate" and index in pending:
                    del pending[index]
                    acked.add(index)
                    trace.append(f"tick {tick}: primary acks {index} now that the backup applied it")
            else:
                trace.append(f"tick {tick}: replicate{payload} arrives at a dead backup and is dropped")

    primary.alive = False
    trace.append(f"tick {steps}: primary crashes permanently; the backup is promoted")
    present = {i for i, _ in backup.log}
    violated = sorted(acked - present)
    if violated:
        trace.append(f"tick {steps}: acked indices {violated} are missing from the backup's log")
    return violated, trace


def check(name, steps, policy, seed_start, count):
    for seed in range(seed_start, seed_start + count):
        violated, trace = run(seed, steps, policy)
        if violated:
            print(f"FAIL sweep {name}: expected holds, got violated at seed {seed}")
            for line in trace:
                print(f"  {line}")
            return 1
    print(f"PASS sweep {name}: holds for {count} seeds")
    return 0


def replay(name, steps, policy, seed):
    violated, trace = run(seed, steps, policy)
    for line in trace:
        print(f"  {line}")
    if violated:
        print(f"FAIL replay {name}: expected holds, got violated")
        return 1
    print(f"PASS replay {name}: holds")
    return 0


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--policy", required=True, choices=["commit-after-replicate", "ack-then-replicate"])
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--seed-start", type=int, default=0)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sweep", type=int)
    group.add_argument("--replay", type=int)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if args.replay is not None:
        return replay("NeverAckedWriteLost", args.steps, args.policy, args.replay)
    return check("NeverAckedWriteLost", args.steps, args.policy, args.seed_start, args.sweep)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
