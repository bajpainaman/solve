# Unbundle: blocks and protocols, not a full solution

Sources: [Minimalist & reusable building blocks](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/minimalist-and-reusable-building-blocks),
[Building a SuperApp](https://docs.cdpi.dev/the-dpi-wiki/building-a-superapp-applying-dpi-thinking),
[Platforms to protocols](https://docs.cdpi.dev/technical-notes/digital-payment-networks/discovery-and-fulfillment-networks/platforms-to-protocols).

CDPI's claim: you cannot predict every need, so one full-stack solution excludes people and stops innovation.
Build small blocks that each do one job, connect them with open specs, and let others compose them.

## Procedure

1. **List the jobs.** Write every job the planned system does as a verb phrase, such as "prove who the user is",
   "move value", "store the record", "show the dashboard".
2. **Sort each job into a layer:**
   - **Rail**: many products need it. Examples: identity or auth, signing, value transfer, data exchange, discovery.
   - **Service**: domain logic one owner runs.
   - **Client**: any UI, CLI, bot or agent.
3. **Cut at the seams.** Every rail gets an interface spec before code (see [spec-first.md](spec-first.md)).
   Services call rails only through that spec. Clients call services only through published APIs.
4. **Strip each block.** Remove fields, modes and options that no first use case needs. Keep extension
   points in the protocol instead.
5. **Check federation.** When unbundling would create one central store that everything shares, replace it
   with each owner exposing a wrapper API.
6. **Name the first adopter of each rail** other than yourself. A rail no one else could use is a service.

## The SuperApp test

One app for everything is a delivery choice, not infrastructure. It can be a good client when the rails under it are open:
- each service keeps its own data and API
- other clients can reach the same services
- users can pick their auth method

A failure in one part should not take down the rest.

## Output

A table of job, layer, block name, interface (spec or API), owner, first outside adopter, and what was removed.
Then the build order: rails before the clients that need them, phases in parallel where blocks are independent.
