# Reconciler

**Pattern:** Kubernetes-style reconcile loop over a stale cache (catalog E).
**Teaches:** a controller's own expectation count standing in for ground truth it has no way to read, a watch event that lowers that count instead of a second read of the resource.

## The system

A controller keeps a replica count at a fixed desired value of 2. It reads
the count from a local cache of the API server, which lags behind the
true count: a create it already issued can take a while to show up there.
The reconcile loop can run again before the cache has caught up.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| The controller never creates more replicas than desired | safety | `NeverOvershoots` |
| The true count and the cache both converge on the desired count | liveness | `EventuallyConverges`, under weak fairness on the controller and the cache |
| Convergence really does happen | reachability | `WitnessConverges.cfg` must violate `NeverConverges` |

## Configs

| Config | Design | Max reconciles | Declared outcome |
|---|---|---|---|
| `ResourceVersionCheck.cfg` | subtracts its own outstanding creates from the gap | 2 | holds |
| `StaleRead.cfg` | computes the gap from the cache alone | 2 | violated `NeverOvershoots` |
| `StaleReadOneRun.cfg` | computes the gap from the cache alone | 1 | holds |
| `WitnessConverges.cfg` | subtracts its own outstanding creates from the gap | 2 | violated `NeverConverges` |

The controller has no way to read the API server's true count directly;
it only ever sees its own cache. `ResourceVersionCheck.cfg` fixes the
cache's staleness without needing to know the true count, by tracking how
many of its own creates have not yet shown up there, the same way a
controller's expectations cache does.

## Run

```bash
fv-tlc --trace Reconciler.tla
fv-mutate Reconciler.mutations
```

## The counterexample, as the user reads it

```text
1. The cache shows 0 replicas, and the desired count is 2.
   replica_controller.py:15
2. The loop sees a gap of 2 and creates 2 replicas. The cache still shows
   0, because the watch has not delivered either event yet.
   replica_controller.py:22
3. The loop runs again before the cache has caught up. It still sees a
   gap of 2 and creates 2 more, for 4 replicas against a desired count
   of 2.
```

## Bounds and limits

The model has one resource and a desired count of 2. It does not model a
second controller replica racing the first, or a delete path.
