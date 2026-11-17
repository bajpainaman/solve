# Spec first: the contract before the code

Sources: [Interoperability](https://docs.cdpi.dev/the-dpi-wiki/dpi-tech-architecture-principles/interoperability),
[Execution guidance #4 and #8](https://docs.cdpi.dev/the-dpi-wiki/dpi-implementation-and-execution-guidance),
[Data standards](https://docs.cdpi.dev/technical-notes/data-and-credentialing-infra/data-standards),
[Curated specifications](https://docs.cdpi.dev/references/home).

CDPI tells builders not to leave the "how" to vendors. Own the blueprint and the interoperability standard, and let
implementations compete under it. For software, the protocol is the product and each implementation is one
client of it.

## Procedure

1. **Reuse before you invent.** Check whether an existing standard fits: OAuth/OIDC, W3C VC, SD-JWT, ISO 20022,
   OpenAPI, FHIR, EIPs, and so on. Run `cdpi search "<topic> standard"` for CDPI's curated list. A custom spec needs a reason.
2. **Minimal core.** Keep required fields and operations to what the first use case needs. Mark everything else optional
   or an extension.
3. **Roots for tomorrow.** Put a version field, extension points, and room for more modes (auth types, currencies,
   transports) in the core, even when one ships first.
4. **Identifiers and addressing.** Define a stable, portable identifier and address format, so data and value can move
   between providers.
5. **Signatures and verification.** Say who signs what, how keys are found and rotated, and how a verifier checks
   offline.
6. **Privacy defaults.** Say what each party must **not** learn. Prefer yes/no answers over raw data and tokens over permanent IDs.
7. **Conformance.** Ship test vectors or a test suite that a stranger can run against their own implementation.
8. **Then build.** One reference implementation and one client that is not yours, before you add features.

## Output

A spec outline: purpose, roles, identifiers, messages or endpoints, signing, privacy, versioning, conformance.
Then the list of standards it reuses, with links, and the open questions.
