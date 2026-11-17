# +1: make what exists reusable before you rewrite it

Sources: [Inputs for a DPI-informed strategy](https://docs.cdpi.dev/the-dpi-wiki/inputs-for-designing-a-dpi-informed-digital-transformation-strategy),
[Execution guidance #5 and #13](https://docs.cdpi.dev/the-dpi-wiki/dpi-implementation-and-execution-guidance),
[Data exchange: the +1 approach](https://docs.cdpi.dev/technical-notes/data-and-credentialing-infra/data-exchanges-system-to-system-data-sharing/getting-started-the-+1-approach).

CDPI's canonical example: a paper certificate plus a digitally signed QR becomes infrastructure. Anyone can verify it
without a new system. The lesson for software: **a small, open, signed interface on an existing system often
beats a rewrite.**

## Translations

| CDPI example | Software +1 | Unlocks |
|---|---|---|
| Paper certificate + signed QR | Sign the records you already emit (JWS, EIP-712, signed JSON) and publish the verification key | Anyone verifies offline, without calling you |
| Department database + open API | A read-only, documented wrapper API over the existing store | Others reuse it. Nothing is migrated or centralised |
| ID card + signed QR, then eAuth and eKYC | Add a yes/no verification endpoint before any profile-sharing endpoint | Minimal disclosure. Integrators stop collecting copies |
| ID Account Mapper (4-field registry) | A tiny lookup service from a stable ID to a routing address | Many senders route to many receivers without bilateral setup |
| Interoperable QR for many wallets | Publish one payload or address format that every client parses | Any client works with any provider |
| ESB or single portal → per-service open APIs | Each service publishes its own API. One catalogue lists them | No central bus to coordinate or fail |
| Excel or PDF dumps → API + licence | A machine-readable export endpoint with a stated licence | Analytics and indexers build on it |

## Procedure

1. Inventory the assets: data stores, outputs, identifiers, existing integrations, and who already uses them.
2. For each asset, ask: *what is the smallest signed, open, machine-readable interface that lets someone else reuse it?*
3. Rank the moves by how often people would use them, how many people they reach, and whether the owner will agree
   (see [rails-check.md](rails-check.md) for the stage each move reaches).
4. Write the +1 as a spec first (see [spec-first.md](spec-first.md)), then the smallest implementation.
5. State what the +1 does **not** fix, so nobody mistakes it for the whole migration.

## When to rewrite anyway

Rewrite only when the +1 cannot meet a principle. Example: the existing store logs data that it must not hold.
Name the principle the existing system cannot meet.
