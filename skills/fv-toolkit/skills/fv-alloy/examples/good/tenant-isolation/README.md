# Tenant isolation on a shared table (row-level security)

**Pattern:** row-level security, multi-tenant schemas (catalog D).
**Teaches:** a query path as a sig, a visibility function that branches on membership in a subset sig, the same claim checked with every path scoped and with no rule at all.

## The system

Rows and principals each belong to one tenant. A query path either carries the tenant predicate or it does not. The question is whether a principal can ever read a row that belongs to a different tenant.

## Property ledger

| Property | Kind | Encoded as |
|---|---|---|
| No principal reads a row that belongs to another tenant | safety | `NoCrossTenantRead_AllPathsTenantScoped` |
| A tenant-scoped path actually returns a row of the principal's own tenant | reachability | `run ATenantScopedPathReturnsAnOwnRow ... expect 1` |

## Commands

| Command | Design | Expectation |
|---|---|---|
| `run ATenantScopedPathReturnsAnOwnRow for 4` | every path is tenant-scoped | SAT: a scoped path returns an own-tenant row |
| `check NoCrossTenantRead_AllPathsTenantScoped for 4` | every path is tenant-scoped | UNSAT: no counterexample |
| `check NoCrossTenantRead_NoRule for 4` | no rule in force | SAT: a counterexample exists |

`AllPathsTenantScoped` is the rule under review: every query path in the router carries the tenant predicate. The third command drops that rule, so `QueryPath` may contain a path that is not in `TenantScopedPath`, the shape of the real bug: one query path in a router that forgot the predicate while every other path has it.

## Run

```bash
fv-alloy --show tenant-isolation.als
fv-mutate tenant-isolation.mutations
```

## The counterexample, as the user reads it

```text
this/Principal<:tenant={Principal$0->Tenant$1}
this/Row<:tenant={Row$0->Tenant$0}
this/TenantScopedPath={}
```

1. Principal 0 belongs to Tenant 1.
2. Row 0 belongs to Tenant 0, a different tenant.
3. The one query path in this instance carries no tenant predicate, so it is not in `TenantScopedPath`.
4. The router returns every row for that path, including Row 0, to Principal 0.

## Bounds and limits

The checks cover four tenants, principals, rows and query paths. The model has one visibility function and no admin role that is meant to see every tenant.
