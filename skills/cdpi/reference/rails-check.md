# Rails check: how close is this to infrastructure?

Sources: [Is my system a DPI?](https://docs.cdpi.dev/the-dpi-wiki/is-my-system-a-dpi) and its
[TL;DR](https://docs.cdpi.dev/the-dpi-wiki/is-my-system-a-dpi/tl-dr-is-my-system-a-dpi).

CDPI is explicit that this is **maturity, not a yes/no checklist**. Never answer only "yes" or "no". Give a stage,
the evidence for it and the next step.

## Four baseline tests

Mark each test **observed** (you saw the code, spec or endpoint), **claimed** (someone says so) or **unknown**.

1. **Open interface.** Open APIs, open standards or open specs exist and are published. Open-source code alone
   does not pass this test, and closed code does not fail it.
2. **Reuse by others.** Parties other than the builder get value, and they can be public or private, incumbents or challengers.
3. **Signed, machine-readable data** wherever data crosses a boundary.
4. **The five principles in practice.** Run [lens.md](lens.md). A principle that appears only in a strategy doc does not count.

## Pattern table (CDPI's, generalised)

| Pattern | Still a solution | Moving toward rails |
|---|---|---|
| Identity | Closed accounts. Non-verifiable credentials | A yes/no auth API, then several auth modes, then profile sharing with consent, then SSO and signing |
| Records or registry | Closed, central database | Signed, machine-readable records that others can read. First as verifiable outputs, then as system-to-system APIs |
| Value transfer | Works inside one provider | Any account, any app, any channel, any recipient. Programmable and extensible |
| Credentials or proofs | PDF in your app | Signed, machine-readable, verifiable by anyone, ideally offline |
| Data network | Central warehouse | Federated network any provider or consumer can join under published rules, with consent |
| Public data | Bulk file dumps | Machine-consumable API with a licence |
| Service access | One portal or bus | Each service publishes its API. Any client integrates |

## Stages

**solution** → **early rails** (open interface exists) → **maturing** (others use it, data is signed) →
**mature** (multiple independent implementations or clients, all five principles hold).

## Output

Stage, the single fact that limits it most, an evidence table for the four tests, and the next +1
(see [plus-one.md](plus-one.md)). Also say what was not assessed: CDPI calls governance and market adoption
"equally crucial", and a code review cannot see them.

Not evidence: "it's open source", "it's on a blockchain", "it's a DPG", "it's a platform", or a vendor's label.
