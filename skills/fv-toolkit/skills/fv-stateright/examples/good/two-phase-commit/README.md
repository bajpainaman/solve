# Two-phase commit

**Pattern:** two-phase commit (catalog B2); coordination and replication (B3).
**Teaches:** a chosen design beside its rejected design as two `Model` impls,
a `sometimes` property as a built-in non-vacuity witness, and a mutations
file that plants a bug in the checked rule and a second one in its input.

## The system

Two resource managers (RMs) each start `Working`, may `Prepare` or
`AbortUnilaterally`, and then try to `Finish`. `Centralized::next_state`
lets an RM finish by committing only once it sees that no RM has aborted
and every RM has at least prepared; it aborts instead if any RM already
has. `Unilateral::next_state` is the rejected design: an RM commits once it
has prepared, with no check of the other RM's vote.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No RM commits while another has aborted | safety | `rms_agree` |
| Both RMs committing is reachable at all | witness | `Property::sometimes("both_commit", ...)` on `Centralized` |

## Checks

| Test | Model | Declared outcome |
|---|---|---|
| `rms_agree_centralized` | `Centralized` | passes: `rms_agree` and `both_commit` both hold |
| `rms_agree_unilateral` | `Unilateral` | `#[should_panic(expected = "rms_agree")]`: the checker must find the disagreement |

`rms_agree_unilateral` is this skill's witness config: a check that is
expected to find a counterexample, so that `rms_agree_centralized` passing
is evidence of the design, not of a property nothing can violate.

## Run

```bash
export CARGO_TARGET_DIR="${FV_HOME:-$HOME/.cache/fv}/stateright/target/two-phase-commit"
cargo test --quiet --lib
${CLAUDE_PLUGIN_ROOT}/scripts/fv-mutate two-phase-commit.mutations
```

## Telling a counterexample

`two-phase-commit.mutations`' first mutation plants `Unilateral`'s bug
directly in `Centralized`. This is the real output of
`rms_agree_centralized` failing on that mutation (the task id and the
cargo registry path before `stateright-0.31.0` vary by machine and run):

```text
thread 'tests::rms_agree_centralized' (2716442) panicked at .../stateright-0.31.0/src/checker.rs:518:13:
Unexpected "rms_agree" counterexample Path[3]:
- AbortUnilaterally(0)
- Prepare(1)
- Finish(1)
Last state: State { rms: [Aborted, Committed] }
```

Read as steps:

```text
1. Both RMs are Working.
2. RM 0 aborts on its own.                 AbortUnilaterally(0)
3. RM 1 prepares.                          Prepare(1)
4. RM 1 finishes and commits, without checking that RM 0 aborted.  Finish(1)
```

## Bounds and limits

The model checks two RMs with no retries, no crashes and no network. It
describes a design, so a regression test on the real commit protocol is
still needed if production code implements this differently.
