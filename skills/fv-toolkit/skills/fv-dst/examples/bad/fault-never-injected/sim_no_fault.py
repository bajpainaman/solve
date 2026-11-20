#!/usr/bin/env python3
"""Broken on purpose: the loss fault the sweep claims to cover never fires.

Source read at: 0000000
Covers: no real repository.

This runs the rejected ack-then-replicate design from
examples/good/primary-backup (the client is acked before the backup applies
the write). That design should lose an acked write whenever a replicate
message is lost, so the sweep below is meant to cover P_LOSS. See `lost =`:
`rng.random() < 0` can never be true, so no message is ever lost, and the
sweep passes on a design that the good example's own rejected-design check
finds a counterexample for in the first seed.

Usage: sim_no_fault.py --sweep N [--seed-start N] [--steps N]
"""
import argparse
import random
import sys

P_LOSS = 0.3  # the probability the sweep is meant to cover


def run(seed, steps):
    rng = random.Random(seed)
    acked, delivered = set(), set()
    next_index = 0
    for _tick in range(steps):
        if rng.random() < 0.5:
            entry = next_index
            acked.add(entry)  # ack-then-replicate: acked before the backup applies it
            next_index += 1
            lost = rng.random() < 0  # BUG: should read `< P_LOSS`; this can never be true
            if not lost:
                delivered.add(entry)
    return sorted(acked - delivered)


def sweep(steps, seed_start, count):
    for seed in range(seed_start, seed_start + count):
        if run(seed, steps):
            print(f"FAIL sweep NeverAckedWriteLost: expected holds, got violated at seed {seed}")
            return 1
    print(f"PASS sweep NeverAckedWriteLost: holds for {count} seeds")
    return 0


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--sweep", type=int, required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    return sweep(args.steps, args.seed_start, args.sweep)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
