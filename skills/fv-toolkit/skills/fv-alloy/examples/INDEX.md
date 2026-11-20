# Alloy examples

`tests/test_examples.sh` in the repository runs every row of this table. A good example meets its expectations and detects its mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/rbac](good/rbac/README.md) | good | RBAC (E), permissions on shared content (F3) | A design rule is a predicate. Check the claim under the chosen design and under the rejected one |
| [good/rebac](good/rebac/README.md) | good | ReBAC in the Zanzibar style (E) | A rewrite rule that unions in the wrong relation turns a view grant on a folder into edit access on everything inside it |
| [good/schema-compat](good/schema-compat/README.md) | good | Data contracts (C1), API versioning (F1), rolling deploy (B6) | A field becomes required only after one version in which it merely exists. Otherwise two adjacent live versions break during a rollout |
| [good/scd2](good/scd2/README.md) | good | Slowly changing dimensions (C4) | Order the time points with `util/ordering` and not with arithmetic. The merge needs a unique successor for every closed row |
| [good/lineage-pii](good/lineage-pii/README.md) | good | Data lineage and PII propagation (C4) | A masking rule that reads only the direct PII tags misses a column that a transform computed from one |
| [good/tenant-isolation](good/tenant-isolation/README.md) | good | Row-level security (D) | One query path without the tenant predicate returns every tenant's rows |
| [bad/overconstraint](bad/overconstraint/README.md) | bad | Any | Contradicting facts leave no instance, so a false claim passes. Only the `run` shows it |
| [bad/vacuous-in](bad/vacuous-in/README.md) | bad | Any | `x.f in S` holds when `x.f` is empty |
| [bad/fact-forbids-the-bug](bad/fact-forbids-the-bug/README.md) | bad | RBAC (E) | A design rule written as a fact makes the claim hold by assumption, and no command catches it |
| [bad/lax-frame-conditions](bad/lax-frame-conditions/README.md) | bad | Any Alloy 6 temporal model | An event predicate that never mentions a `var` field leaves that field free to change in the next state |
