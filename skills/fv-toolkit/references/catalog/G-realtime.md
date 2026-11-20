# Catalog G — Real-time communication and collaboration

Real-time systems combine distributed protocols with hard timing, so they need two kinds of tool: TLA+/Quint or P for signaling and session state, and UPPAAL or timed TLA+ where deadlines matter. Media quality itself is out of scope for formal tools; verify the control plane, and load-test the data plane.

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Session / meeting lifecycle | Ghost participants after crash; meeting never ends; host transfer races | Quint/TLA+ or P | Participants, host role, join/leave/crash, server failover | Exactly one host while active; meeting ends when last leaves; no ghosts after timeout | MBT on session service |
| Signaling (SDP offer/answer, ICE, renegotiation) | Glare (both sides offer); stuck renegotiation | P or TLA+ | Two peers + signaling server, message reordering | Every negotiation terminates in a stable state; glare resolved deterministically | Trace validation on signaling logs |
| SFU / media routing control plane | Subscriber routed to a dead forwarder; duplicate streams after migration | TLA+/Quint | Rooms, SFU nodes, subscriptions, node failure | Each subscription served by exactly one live node; migration loses no subscription | Fault-injection test |
| Presence | Users shown online after disconnect; flapping | TLA+ with heartbeats and clock skew | Heartbeats, TTLs, multi-device | Eventually accurate presence; bounded staleness | Simulation with dropped heartbeats |
| Chat / message delivery and ordering | Messages reordered per conversation; duplicates on reconnect; read receipts regress | TLA+/Quint; Hypothesis stateful client | Per-conversation sequence numbers, offline clients, resend | Per-conversation total order; at-most-once display; read pointer monotonic | Multi-client simulation |
| Typing indicators / ephemeral state | Stale indicators never cleared | TLA+ or UPPAAL | Timers + lossy delivery | Indicators expire within bound | Timer test |
| Recording and transcription pipelines | Segments missing or duplicated; transcript doesn't match recording | TLA+ for pipeline; Hypothesis for stitching | Segment upload, retries, assembly | Every segment assembled exactly once, in order | Oracle test on stitcher |
| Permissions in live sessions (waiting room, breakout rooms, screen-share rights) | Unadmitted user receives media; breakout reassignment leaks audio | Alloy + TLA+ | Roles, rooms, admissions, moves | Media only to admitted members of the same room | Generated negative tests |
| Shared whiteboard / co-editing | Diverging canvases | Hypothesis CRDT laws + TLA+ sync | Concurrent ops, reconnects | Convergence | Multi-client simulation |
| Notifications and calendar integration | Duplicate invites; reminders at wrong time across time zones | Hypothesis + TLA+ | Calendar sync, recurrence, time zones | One invite per change; reminders at correct local time | Property tests |
