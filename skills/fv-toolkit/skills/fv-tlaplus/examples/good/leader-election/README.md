# Leader election

**Pattern:** leader election under a partition (catalog B3).
**Teaches:** a candidate's own view of the cluster kept separate from the cluster's real size, a partition fault that splits reachability without touching the node set.

## The system

Five nodes vote for a leader for one term. Each node casts exactly one
vote, for itself or for another node it can reach, and never changes it. A
network partition can split the cluster into two sides that can each still
talk among themselves, but not across the split: {n4, n5} against
{n1, n2, n3}.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No two nodes are both leader for this term | safety | `AtMostOneLeaderPerTerm` |
| A leader really can be elected | reachability | `WitnessLeader.cfg` must violate `NeverAnyLeader` |

## Configs

| Config | Design | Partitioned | Declared outcome |
|---|---|---|---|
| `ClusterMajority.cfg` | a candidate needs a majority of the whole cluster | yes | holds |
| `LocalMajority.cfg` | a candidate needs a majority of what it can reach | yes | violated `AtMostOneLeaderPerTerm` |
| `NoPartition.cfg` | a candidate needs a majority of what it can reach | no | holds |
| `WitnessLeader.cfg` | a candidate needs a majority of the whole cluster | yes | violated `NeverAnyLeader` |

`LocalMajority.cfg` and `NoPartition.cfg` differ only in whether the
partition fires. With no partition, "what a candidate can reach" is the
whole cluster, so the two designs agree and the property holds either way;
the partition is what makes them diverge.

This pattern has no liveness property of its own: a single round of voting
can split without any side reaching a majority, which is expected, not a
bug, and is why the catalog lists only the safety property.

## Run

```bash
fv-tlc --trace LeaderElection.tla
fv-mutate LeaderElection.mutations
```

## The counterexample, as the user reads it

```text
1. n1, n2 and n3 vote for n1. n4 and n5 vote for n4.      election.py:14
2. The network splits {n4, n5} off from the rest.         election.py:9
3. n1 counts 2 of the 2 nodes it can still reach and declares itself
   leader with a local majority.                          election.py:22
4. n4 counts 2 of the 2 nodes it can still reach and declares itself
   leader too, for the same term, using the same rule.
```

## Bounds and limits

The model has five nodes, one term and one partition event. It does not
model a second election round, a node that changes its vote, or a leader
that steps down.
