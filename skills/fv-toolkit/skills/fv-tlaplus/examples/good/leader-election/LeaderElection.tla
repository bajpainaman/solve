---------------------------- MODULE LeaderElection ----------------------------
(* Source read at: 0000000
   Covers: cluster/election.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   Five nodes vote for a leader for one term. Each node casts exactly one
   vote for the term, for itself or for another node it can reach, and
   never changes it. A network partition can split the cluster into two
   sides that can each still talk among themselves, but not across the
   split.

   The knob Order chooses the design:
     "local_majority"   a candidate wins with a majority of the nodes it
                         can currently reach
     "cluster_majority"  a candidate wins only with a majority of every
                         node in the cluster, reachable or not
   The fault switch Partitioned lets the network split IsolatedNodes off
   from the rest. FALSE switches it off, so every node can reach every
   other. *)
EXTENDS Naturals, FiniteSets

CONSTANTS Node, Order, Partitioned, IsolatedNodes

VARIABLES isolated, split, votedFor, leader

vars == <<isolated, split, votedFor, leader>>

Init ==
    /\ isolated = {}
    /\ split = FALSE
    /\ votedFor = [n \in Node |-> "none"]
    /\ leader = [n \in Node |-> FALSE]

TypeOK ==
    /\ isolated \subseteq Node /\ split \in BOOLEAN
    /\ votedFor \in [Node -> Node \cup {"none"}]
    /\ leader \in [Node -> BOOLEAN]

\* Both on the isolated side, or both off it: this pair can still talk.
CanReach(a, b) == (a \in isolated) = (b \in isolated)

VotesFor(candidate) == {n \in Node : votedFor[n] = candidate}
Reachable(candidate) == {n \in Node : CanReach(n, candidate)}

\* Fault: the network splits the cluster into two sides, once.
Partition ==
    /\ Partitioned /\ ~split
    /\ isolated' = IsolatedNodes
    /\ split' = TRUE
    /\ UNCHANGED <<votedFor, leader>>

\* Source: node.request_vote(), the one vote this node casts for the term,
\* for itself or for another node it can reach.
Vote(voter, candidate) ==
    /\ votedFor[voter] = "none" /\ CanReach(voter, candidate)
    /\ votedFor' = [votedFor EXCEPT ![voter] = candidate]
    /\ UNCHANGED <<isolated, split, leader>>

\* Source: node.become_leader(), counting only the votes this node can see.
BecomeLeaderLocal(candidate) ==
    /\ Order = "local_majority" /\ ~leader[candidate]
    /\ 2 * Cardinality(VotesFor(candidate) \cap Reachable(candidate)) > Cardinality(Reachable(candidate))
    /\ leader' = [leader EXCEPT ![candidate] = TRUE]
    /\ UNCHANGED <<isolated, split, votedFor>>

\* Source: node.become_leader(), counting votes against the whole cluster.
BecomeLeaderCluster(candidate) ==
    /\ Order = "cluster_majority" /\ ~leader[candidate]
    /\ 2 * Cardinality(VotesFor(candidate)) > Cardinality(Node)
    /\ leader' = [leader EXCEPT ![candidate] = TRUE]
    /\ UNCHANGED <<isolated, split, votedFor>>

\* The end state gets its own action, so deadlock checking stays on. Once
\* every node has cast its one vote, nothing further can ever change.
Done == (\A n \in Node : votedFor[n] # "none") /\ UNCHANGED vars

Work == (\E a, b \in Node : Vote(a, b)) \/ (\E n \in Node : BecomeLeaderLocal(n) \/ BecomeLeaderCluster(n))
Next == Work \/ Partition \/ Done

Spec == Init /\ [][Next]_vars

\* "No two nodes are both leader for this term."
AtMostOneLeaderPerTerm == ~(\E l1, l2 \in Node : l1 # l2 /\ leader[l1] /\ leader[l2])
\* Witness: a leader really can be elected.
NeverAnyLeader == ~(\E n \in Node : leader[n])
=================================================================================
