-- Source read at: 0000000
-- Covers: api/query_router.py
--
-- The header shows the form of a sync record. This example describes no real
-- repository, so the commit is a placeholder.
--
-- Row-level security over a multi-tenant table. Each row and each principal
-- belongs to one tenant. A query path either carries the tenant predicate,
-- "WHERE tenant_id = :current_tenant", or it does not. The question is
-- whether a principal can ever read a row that belongs to another tenant.

sig Tenant {}
sig Principal { tenant: one Tenant }
sig Row { tenant: one Tenant }
sig QueryPath {}
sig TenantScopedPath in QueryPath {}  -- paths whose SQL carries the tenant predicate

-- Source: query_router.py, execute(). The rows a path returns for a principal.
fun visibleRows[p: Principal, q: QueryPath]: set Row {
  q in TenantScopedPath => { r: Row | r.tenant = p.tenant } else Row
}

-- The design rule under review: every query path in the router carries the
-- tenant predicate.
pred AllPathsTenantScoped { QueryPath in TenantScopedPath }

-- "No principal reads a row that belongs to another tenant."
assert NoCrossTenantRead_AllPathsTenantScoped {
  AllPathsTenantScoped implies
    no p: Principal, q: QueryPath, r: Row | r in visibleRows[p, q] and r.tenant != p.tenant
}
-- The rejected design: at least one path in the router has no tenant predicate.
assert NoCrossTenantRead_NoRule {
  no p: Principal, q: QueryPath, r: Row | r in visibleRows[p, q] and r.tenant != p.tenant
}

-- Witness: a tenant-scoped path actually returns a row for a principal of
-- its own tenant, so the checks above are not passing on an empty table.
pred ATenantScopedPathReturnsAnOwnRow {
  AllPathsTenantScoped and some p: Principal, q: QueryPath | some visibleRows[p, q] & { r: Row | r.tenant = p.tenant }
}

run ATenantScopedPathReturnsAnOwnRow for 4 expect 1
check NoCrossTenantRead_AllPathsTenantScoped for 4 expect 0
check NoCrossTenantRead_NoRule for 4 expect 1
