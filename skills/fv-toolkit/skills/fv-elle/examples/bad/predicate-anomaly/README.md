# A predicate anomaly the check cannot see

**Pattern:** transactions at a given isolation level (catalog D).
**Teaches:** `list-append` and `rw-register` model only appends and reads of named keys. Neither has a delete or an update, so a bug that depends on a row leaving a predicate's matching set is not representable in either model, and no mechanical check here can catch it.

## The history

Key 1 holds the ids of jobs an approvals worker still considers pending. Key 2 holds the ids of approved jobs. Process 0 creates job 42 as pending (`[:append 1 42]`). Process 1 approves job 42 (`[:append 2 42]`) and, in the same transaction, rereads key 1 for its own bookkeeping, seeing `[42]`.

## The real output

```text
PASS History.edn: valid
```

## Why the artifact is wrong

The real approvals code almost certainly clears a job's pending flag when it approves it, so a later `SELECT id FROM jobs WHERE status = 'pending'` would not return job 42 once process 1 has run. `list-append` has no operation that removes an element from a list; `:append` only ever adds one. To write this history at all, job 42's presence in key 1 has to stay forever, because there is no micro-operation that would clear it. The history elle-cli checks is therefore not a faithful recording of what "still pending" means in the real system; it is a recording of what `list-append` can express, and the two differ exactly where the bug would show up. A second worker that reads key 1 to decide what to reprocess still sees job 42 as pending, and elle-cli has no way to flag that, because nothing in its model says key 1 should have stopped including it.

## The fix

There is no fix to this check. Pick a different model or a different source of truth: an `rw-register` history keyed by job id, where approval is a write of a status value the register can overwrite, can at least represent the field flipping, though still only within the anomalies `rw-register` searches for. A direct assertion against the real table (`SELECT status FROM jobs WHERE id = 42`, taken after the approval transaction commits) catches this kind of bug where `elle-cli` cannot.

## The check that catches the error

None. Say so plainly: this is a gap in what `list-append` and `rw-register` can represent, not a gap in how carefully the history was checked.

## Run

```bash
fv-elle History.edn
```
