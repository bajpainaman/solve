# Fault models

Each template should expose these faults as switches so a model can run with them on or off.

| Fault | Model as | Applies to |
| --- | --- | --- |
| Process crash + restart | Lose volatile state, keep durable state, at any step | Every stateful service |
| Crash between two writes | Split one logical operation into separate atomic steps | Outbox, sagas, dual writes |
| Message loss / duplication / reordering | Network as a bag (unordered multiset) with nondeterministic drop/dup | Queues, RPC, CDC |
| Network partition | Subsets of nodes cannot exchange messages | Replication, leader election |
| Timeout / slow node / GC pause | Process takes no steps for an unbounded period, then resumes with stale beliefs | Leases, locks |
| Clock skew | Each node has its own clock variable with bounded drift | Leases, TTLs, watermarks, schedulers |
| Concurrent writers | Two actors run the same action interleaved | OCC, upserts, caches |
| Partial failure of a batch | Some items succeed, some fail, caller sees one result | Bulk APIs, ETL loads |
| Storage faults | Torn writes, lost fsync, misdirected reads ([TigerBeetle](https://pierrez.github.io/moonpool/part1-why/04-history.html)) | Storage engines, WALs |
| Byzantine / malicious input | Adversary controls fields or messages | Webhooks, auth, protocols |
