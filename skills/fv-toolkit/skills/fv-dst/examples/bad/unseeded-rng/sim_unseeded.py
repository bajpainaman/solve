#!/usr/bin/env python3
"""Broken on purpose: the sweep shares one random.Random across every run.

Source read at: 0000000
Covers: no real repository.

This is the same primary-backup model as examples/good/primary-backup, cut
down to the one difference that breaks replay: sweep() below creates a
single random.Random before its loop and passes it to every run, instead of
a fresh random.Random(seed) per run. See README.md for what that does to
--replay.

Usage:
  sim_unseeded.py --sweep N [--seed-start N] [--steps N]
  sim_unseeded.py --replay SEED [--steps N]
"""
import argparse
import random
import sys

P_SUBMIT = 0.1
P_LOSS = 0.1


def run(rng, steps):
    """Run one simulation with the ack-then-replicate policy, using the given rng."""
    acked, delivered = set(), set()
    next_index = 0
    for tick in range(steps):
        if rng.random() < P_SUBMIT:
            entry = next_index
            acked.add(entry)
            next_index += 1
            if rng.random() >= P_LOSS:
                delivered.add(entry)
    violated = sorted(acked - delivered)
    return violated


def sweep(steps, seed_start, count):
    rng = random.Random(seed_start)  # BUG: one Random object, shared by every run in the sweep
    for i in range(count):
        if run(rng, steps):
            print(f"FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed {seed_start + i}")
            return 1
    print(f"PASS sweep NeverAckedWriteLost: holds for {count} seeds")
    return 0


def replay(steps, seed):
    rng = random.Random(seed)  # a fresh stream, not the state the sweep actually had at index `seed`
    if run(rng, steps):
        print("FAIL replay NeverAckedWriteLost: expected holds, got violated")
        return 1
    print("PASS replay NeverAckedWriteLost: holds")
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
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
        return replay(args.steps, args.replay)
    return sweep(args.steps, args.seed_start, args.sweep)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
