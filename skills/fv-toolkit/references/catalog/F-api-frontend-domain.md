# Catalog F — APIs, frontend, and domain logic

These patterns sit closest to users and money, and most of them are checked best on the real code: schema-driven API fuzzing, state-machine path coverage, and properties over calculations. Z3 handles the rule tables that encode business policy: eligibility, pricing, promotions, routing, or jurisdiction rules.

### F1. APIs and protocols

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| REST / OpenAPI contract | Responses violate schema; 500s on edge inputs; spec drift | Schemathesis | Generated from the spec | Status codes and bodies conform; no 5xx | `st run` in CI |
| Stateful API workflows (create → get → update → delete) | Resource lifecycle bugs | Schemathesis state machine (OpenAPI links) or Hypothesis stateful | Links between operations | Created resources retrievable; deleted resources gone | `schema.as_state_machine()` |
| Idempotency keys on POST | Retry creates a duplicate charge; key reuse with different body accepted | TLA+/Quint for concurrent retries; Hypothesis for API | Client retries, concurrent duplicates, server crash after effect | Same key ⇒ same result and one effect; different body ⇒ rejected | Concurrent duplicate-request test |
| Cursor pagination | Items skipped or repeated when data changes mid-scan | TLA+ or Hypothesis stateful | Inserts/deletes interleaved with page fetches | Every item present for the whole scan is returned exactly once | Stateful test |
| API versioning | Old clients break on new server | Alloy (version matrix) + contract tests | Client versions × server versions | Supported pairs compatible | Contract tests per pair (Pact) |
| gRPC / event schema evolution (protobuf, Avro) | Field reuse; required-field changes | Z3/Alloy over schema diffs; buf breaking | Old and new schema | Wire compatibility rules hold | `buf breaking` in CI |
| Rate-limited public API | Limits bypassed via concurrency or multiple keys | TLA+ | Concurrent requests, token bucket | Never above limit per principal | Concurrency test |

### F2. Frontend and client

| Pattern | What breaks | Tool | Model | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| UI flows as state machines (XState) | Unreachable screens; dead ends; impossible states | XState graph path generation | The machine itself | Every state reachable; every path testable | `getShortestPaths` → Playwright tests |
| Redux / reducers / Elm architecture | Reducer breaks invariants on some action sequence | Hypothesis-style (fast-check `commands`) | Random action sequences | Store invariants hold; reducer pure | fast-check model-based test |
| Optimistic UI updates | UI shows success that the server rejected; rollback fails | TLA+ or fast-check | Client state, pending requests, server responses (out of order) | UI eventually equals server state | Model-based test with mocked server |
| Offline-first sync / local-first (CRDT or op log) | Conflicts lost; divergence after reconnect | Hypothesis/fast-check + TLA+ for protocol | Devices, offline edits, sync | Convergence; no lost edits | Multi-client simulation |
| Forms and multi-step wizards | Validation bypass via back button; partial submits | XState graph | Steps and guards | Submit only reachable with all valid fields | Generated path tests |
| Auth session handling in client | Refresh-token races log users out or double refresh | TLA+ | Tabs, refresh timers, token store | One refresh in flight; no valid session lost | Multi-tab test |

### F3. Domain logic (any industry)

Rows are grouped by the shape of the business rule, not by industry. The same template covers seat booking, hotel rooms, and warehouse stock. Money and tax rows stay, as one domain among many.

| Pattern | Examples | What breaks | Tool | Properties | Code link |
| --- | --- | --- | --- | --- | --- |
| Rule / eligibility / decision tables | Insurance eligibility, loan approval, content moderation rules, shipping zones, tax jurisdictions, feature entitlement | Overlapping or missing rules; two outcomes apply; none applies; effective dates overlap | Z3 (Alloy for small tables) | Completeness and uniqueness for every valid input; date ranges non-overlapping | Generate SMT from the rule tables in CI |
| Pricing, fee, and discount calculation | Cart pricing, ride fares, SaaS usage bills, shipping cost, sales tax | Line items don't sum to total; order dependence; rounding drift | Hypothesis; Dafny/Lean core if stakes justify | Sum(lines) == total under the rounding rule; order-independent; refund reverses charge | Property tests on the calculator |
| Promotion / coupon stacking | Retail promos, loyalty multipliers, referral credits | Stacking produces negative price or exceeds caps; exclusive promos combine | Z3 | Price ≥ 0; caps respected; exclusivity constraints hold for every combination | SMT over promo config |
| Inventory and reservations | Seat booking, hotel rooms, warehouse stock, appointment slots, concert tickets | Overbooking under concurrency; holds never released | TLA+/Quint or FizzBee; Hypothesis stateful | Reserved ≤ capacity; every hold expires or converts; no double allocation | Concurrency test from counterexample |
| Order / fulfillment lifecycle | E-commerce orders, food delivery, returns/RMAs | Shipping a cancelled order; refunding twice; stuck states | Quint/TLA+ or XState | Only allowed transitions; terminal states final; each order eventually terminal | MBT on order service |
| Subscriptions and entitlements | SaaS plans, streaming access, software licences, trials | Access after cancellation; proration errors; double renewals | Hypothesis stateful + Alloy for plan/feature matrix | Entitlement == f(current plan, time); one renewal per period | Stateful test with fake clock |
| Quotas, limits, and threshold accumulators | API quotas, spend limits, fraud velocity rules, compliance thresholds | Limit crossed on the wrong event; double-counted on replay | Hypothesis; TLA+ if concurrent ingestion | Crossing point order-independent and idempotent under replay; never exceed hard limit | Oracle test vs. batch recompute |
| Matching and allocation | Ride dispatch, marketplace order books, job scheduling, ad auctions, school/residency matching | Same resource matched twice; unfair or unstable match; auction rule violated | TLA+/Quint for concurrency; Z3 or Hypothesis for the algorithm | Each resource matched at most once; price/priority rules hold (e.g. second-price, stability) | Property tests on matcher + concurrency test |
| Approval and submission workflows | Expense approvals, PR reviews, claims processing, regulatory filings, KYC | Approved without required approvers; submitted twice; amended before accepted | Quint/TLA+ or XState; Alloy for approver rules | Required approvals before submit; one accepted submission per period; separation of duties | MBT on workflow service |
| Permissions on shared content | Docs/folders sharing, project roles, healthcare record access | Inherited access leaks; revocation doesn't propagate | Alloy | Expected access matrix; revocation removes all derived paths | Generated negative tests |
| Collaborative editing / versioning | Document editors, design tools, wikis, config versioning | Concurrent edits lost; merges diverge; history rewritten | Hypothesis (OT/CRDT laws) + TLA+ for sync protocol | Convergence; intention preservation; history append-only | Multi-client simulation |
| Notification and messaging dedup | Email/SMS/push, alerting, reminders | Duplicate sends on retry; missed sends on failover | TLA+/Quint | Each notification sent at most once per key and at least once eventually | Crash-injection test |
| Counters, leaderboards, voting, polls | Likes, game scores, elections, rankings | Lost increments; double votes; ranking ties mishandled | TLA+ (concurrency) + Hypothesis (ranking rules) | Count == accepted events; one vote per voter; total order on ties | Concurrency + property tests |
| Game and simulation state | Turn-based games, physics steps, multiplayer lobbies | Illegal moves accepted; desync between clients | Hypothesis stateful; TLA+ for lobby/sync | Only legal moves; deterministic replay; clients converge | Replay tests |
| Money and rounding | Any currency handling | Float use; half-up vs banker's mismatch; currency mixing | Hypothesis + CrossHair contracts | Allocations sum exactly (largest-remainder); no cross-currency arithmetic | Contracts on a Money type |
| Units and measurement | Dosage, logistics weights, engineering units | Unit mix-ups; precision loss | Hypothesis; type-level units | Round-trip conversions within tolerance; no mixed-unit arithmetic | Unit-typed APIs + property tests |
| Time zones, calendars, periods | Billing periods, payroll, reporting windows, SLAs | Off-by-one at DST and month/year boundaries | Hypothesis datetime strategies | Each instant maps to exactly one period; periods contiguous | Property tests |
| Scheduling and recurrence | Calendars, shift rosters, maintenance windows | Missed or duplicated occurrences across DST; double-booked staff | Hypothesis; Z3 for constraint-based rostering | Occurrences unique and complete; no person in two shifts at once | Property tests + SMT check of roster |
| Search, ranking, recommendation rules | Catalog search filters, feed ranking constraints | Filtered-out items appear; business boosts break hard constraints | Hypothesis metamorphic tests | Adding a filter never adds results; hard constraints always enforced | Metamorphic property tests |
| Reports and exports | Dashboards, CSV exports, invoices, statements | Export totals disagree with source or UI | Hypothesis differential | Export totals == report totals == source aggregates | Oracle test |
