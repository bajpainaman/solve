# Allocate bonus

**Pattern:** pricing and fee calculation (catalog A3).
**Teaches:** `kani::any()` over every input, a bounds property, an unwind
bound on a fixed-size loop, a `kani::cover!` witness, and a mutations
file that plants a bug in the checked line and a second one beside it.

## The system

`allocate(total, percents)` returns one part per percent, each the floor
of `total * percent / 100`. The caller must keep every percent at or
below 100. The claim is that no part can ever exceed the total.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Every part is at most the total | bounds | three `assert!` calls in `check_every_part_is_at_most_the_total` |
| A share can take the whole total | witness | `kani::cover!(parts[0] == total && percents[0] == 100, ...)` |

## Run

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/fv-kani check_every_part_is_at_most_the_total
${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate allocate-bonus.mutations
```

This is the real output of a verified run, run in Docker because this
development machine's cargo has no rustup (see the skill's report for
which outputs came from Docker):

```text
Check 12: verification::check_every_part_is_at_most_the_total.cover.1
	 - Status: SATISFIED
	 - Description: "a share can equal the whole total"
	 - Location: src/lib.rs:27:9 in function verification::check_every_part_is_at_most_the_total

SUMMARY:
 ** 0 of 55 failed (1 unreachable)

 ** 1 of 1 cover properties satisfied

VERIFICATION:- SUCCESSFUL
Verification Time: 1.3802127s

Manual Harness Summary:
Complete - 1 successfully verified harnesses, 0 failures, 1 total.
```

The other 54 checks are Kani's own automatic overflow, bounds and
reachability checks on `allocate` and on the standard library code the
harness's comparisons pull in; none of them is a check this README wrote.

## Telling a counterexample

This is the real output of the first mutation, which drops the promotion
to `u32` before multiplying:

```text
SUMMARY:
 ** 1 of 55 failed (1 unreachable)

Failed Checks: attempt to multiply with overflow
 File: "src/lib.rs", line 8, in allocate

VERIFICATION:- FAILED
Verification Time: 0.28930858s
```

Read as steps:

```text
1. total and percents[0] are symbolic u16 and u8 values.
2. `total * percents[0] as u16` multiplies in u16, which overflows once
   total exceeds about 650 for a percent of 100.
3. Kani finds a concrete total and percent where this overflow happens
   and reports it as the counterexample.
```

## Bounds and limits

The harness checks every `u16` total and every `[u8; 3]` percents array
with each entry at most 100, which Kani explores exhaustively within
`#[kani::unwind(4)]`. It says nothing about a `total` stored as a wider
or narrower integer type in the real code, and the property checked is a
bound, not conservation: it does not claim the three parts sum to the
total.
