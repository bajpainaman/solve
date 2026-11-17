# Lens: review any design against the five principles

Source: [DPI Tech Architecture Principles](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles).
CDPI wrote these to tell infrastructure apart from ordinary digitisation. Here they review any
software: a protocol, an API, a smart contract system, an app, a PR.

## The five questions

| Principle | Ask | Good sign | Red flag |
|---|---|---|---|
| [Interoperability](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/interoperability) | Can a stranger integrate on equal terms, without asking us? | Published spec. Open API. Common identifiers and address formats. A conformance test others can run | Private endpoints. Bilateral integrations. "Talk to us for access". Our client is the only client |
| [Minimalist, reusable blocks](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/minimalist-and-reusable-building-blocks) | What is the one job each component does? What did we overspecify? | Small blocks that compose. Few required fields. Extensible later | One service that owns ID, data, payments and UI. Fields "just in case". Hard-coded modes |
| [Diverse, inclusive innovation](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/diverse-inclusive-innovation) | Does the back end assume one front end? Who can build on it besides us? | SDKs. Signed, machine-readable outputs. Offline and degraded modes. Adoption pulled by value | Online-only. One official app. Adoption only by mandate or lock-in |
| [Federated, decentralised](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/federated-and-decentralised-by-design) | Are we centralising data we could leave where it lives? | Wrapper APIs over existing stores. Data stays with its owner. Unification by protocol | New central database or data lake. A honeypot. One operator can stop everything |
| [Security, privacy by design](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/security-and-privacy-by-design) | Does each component know as little as possible? Can every change be audited? | Optimal ignorance. Tokens and masking. Signed data and change logs. Granular, revocable consent. Selective disclosure | Logs of purpose or location. One permanent ID reused across systems. Consent as a checkbox. Unsigned state |

## Procedure

1. Draw three layers: **rails** (identity, value transfer, data sharing) → **services** → **clients**.
   Any component that spans layers needs a reason.
2. For each principle, write one finding: **meets / partial / fails / unknown**. Name the component and the
   evidence (file, endpoint, contract, doc). Unknown is a finding. Don't guess.
3. Add the two CDPI build rules
   ([execution guidance](https://docs.cdpi.dev/the-dpi-wiki/dpi-implementation-and-execution-guidance)):
   - **Design for failure** (#7). Expect outages, missing connectivity and misaligned incentives.
   - **Architect for tomorrow, implement for today** (#8). Put extension points in the protocol root,
     even if one mode ships.
4. Recommend the smallest fix per failing principle. Use [plus-one.md](plus-one.md) for an existing system and
   [unbundle.md](unbundle.md) when one component does too much.

## Output

A five-row table (principle, finding, evidence, smallest fix), then the one change with the biggest effect.
Keep the principle names exact so readers can trace them to the source.

Proprietary code can pass. What matters is open specs and reuse, not the licence
([DPG and DPI](https://docs.cdpi.dev/the-dpi-wiki/dpg-and-dpi)).
