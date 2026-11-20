-- Source read at: 0000000
-- Covers: warehouse/masking_policy.py
--
-- The header shows the form of a sync record. This example describes no real
-- repository, so the commit is a placeholder.
--
-- Columns, the transforms that derive one column from others, and a set of
-- sinks that expose columns downstream. The question is whether a sink ever
-- exposes, unmasked, a column that was computed from a PII column.

sig Column {
  derivesFrom: set Column  -- the columns a transform reads to compute this one
}
sig PIIColumn in Column {}  -- columns that directly hold PII, such as email or ssn

-- True by construction: the lineage graph the warehouse's catalog stores has no cycle.
fact Acyclic { no c: Column | c in c.^derivesFrom }

sig Sink {
  exposes: set Column,  -- columns a sink makes available to its readers
  masked: set Column    -- the subset of those columns the sink masks before exposing them
}
fact MaskedIsExposed { all s: Sink | s.masked in s.exposes }

-- A column that is PII, or that was computed, through any chain of
-- transforms, from a column that is PII.
pred DerivedFromPII[c: Column] { some (c.*derivesFrom & PIIColumn) }

-- Source: masking_policy.py, the rule under review: a sink must mask every
-- column it exposes that derives from PII through any number of transforms.
pred MaskingCoversLineage {
  all s: Sink, c: Column | (c in s.exposes and DerivedFromPII[c]) implies c in s.masked
}
-- The rejected rule: the policy masks a column only when it is itself
-- tagged PII, and misses a column a transform computed from one.
pred MaskingCoversDirectPIIOnly {
  all s: Sink, c: Column | (c in s.exposes and c in PIIColumn) implies c in s.masked
}

-- "No sink exposes, unmasked, a column derived from PII."
assert NoUnmaskedPIIAtASink_MaskingCoversLineage {
  MaskingCoversLineage implies no s: Sink, c: Column | c in s.exposes and DerivedFromPII[c] and c not in s.masked
}
assert NoUnmaskedPIIAtASink_MaskingCoversDirectPIIOnly {
  MaskingCoversDirectPIIOnly implies no s: Sink, c: Column | c in s.exposes and DerivedFromPII[c] and c not in s.masked
}

-- Witness: the lineage rule actually reaches a column that is not itself
-- tagged PII but was computed from one, and masks it.
pred ALineageOnlyColumnIsMasked {
  MaskingCoversLineage and
  some s: Sink, c: Column | c in s.masked and c not in PIIColumn and DerivedFromPII[c]
}

run ALineageOnlyColumnIsMasked for 4 expect 1
check NoUnmaskedPIIAtASink_MaskingCoversLineage for 4 expect 0
check NoUnmaskedPIIAtASink_MaskingCoversDirectPIIOnly for 4 expect 1
