# Cache invalidation

**Pattern:** cache-aside read fills a stale entry (catalog A2).
**Teaches:** a version mark left behind on an otherwise empty cache entry, a rejected fill that leaves the cache exactly as it found it, a mixed-type variable replaced with a boolean plus a same-typed value to avoid a TLC equality error.

## The system

A reader reads the database, meaning to fill the cache with what it saw.
A writer updates the database, then invalidates the cache. The reader's
fill can land at any point, including after the invalidation, because the
read and the fill are two separate steps with everything else free to run
between them.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| Once the write, the invalidation and the fill have all happened, the cache is either empty or holds the current value | safety | `NeverStaleAtRest` |
| The fill really does write something into the cache | reachability | `WitnessFills.cfg` must violate `NeverFills` |

## Configs

| Config | Design | Late fill | Declared outcome |
|---|---|---|---|
| `VersionChecked.cfg` | a fill lands only if its version is current | on | holds |
| `NoVersionCheck.cfg` | a fill always writes what the reader saw | on | violated `NeverStaleAtRest` |
| `NoVersionCheckNoLateFill.cfg` | a fill always writes what the reader saw | off | holds |
| `WitnessFills.cfg` | a fill lands only if its version is current | on | violated `NeverFills` |

`NoVersionCheck.cfg` and `NoVersionCheckNoLateFill.cfg` differ only in
whether the fill can land after the invalidation. With the fault off, a
fill already in flight always lands before the invalidation runs, so the
design looks safe for a reason that has nothing to do with checking
anything: there is simply no window left for a stale write to land in.

## Run

```bash
fv-tlc --trace CacheInvalidation.tla
fv-mutate CacheInvalidation.mutations
```

## The counterexample, as the user reads it

```text
1. The reader reads the database and sees the old value.
   cache_aside.py:11
2. The writer updates the database to a new value and invalidates the
   cache.                                                 cache_aside.py:24
3. The reader's fill lands after the invalidation and writes the old
   value it saw back into the now-empty cache. Nothing else ever
   invalidates it again.
```

## Bounds and limits

The model has one write and one concurrent read. It does not model a
second writer, a cache with a TTL, or a reader whose own read spans more
than one row.
