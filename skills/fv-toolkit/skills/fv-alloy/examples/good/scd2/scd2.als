-- Source read at: 0000000
-- Covers: warehouse/scd2.py
--
-- The header shows the form of a sync record. This example describes no real
-- repository, so the commit is a placeholder.
--
-- A slowly changing dimension, type 2. Each key has a history of rows, every
-- row valid from one instant to another. A row with no validTo is current.
-- Alloy's built-in integers run from -8 to 7, so time points are atoms of an
-- ordered signature, with no arithmetic on them.

open util/ordering[Instant]

sig Instant {}
sig Key {}
sig Row {
  key: one Key,
  validFrom: one Instant,
  validTo: lone Instant  -- absent means the row is current
}

-- True by construction: the database check constraint the table carries.
fact FromBeforeTo { all r: Row | some r.validTo implies lt[r.validFrom, r.validTo] }

pred Current[r: Row] { no r.validTo }

-- A row is the active one for its key at instant i.
pred Covers[r: Row, i: Instant] { gte[i, r.validFrom] and (Current[r] or lt[i, r.validTo]) }

-- "At most one row of a key is active at any instant it has a row at all."
pred AtMostOneActiveRow { all k: Key, i: Instant | lone r: Row | r.key = k and Covers[r, i] }
-- "A key with any history has exactly one current row."
pred ExactlyOneCurrentRow { all k: Key | (some r: Row | r.key = k) implies one r: Row | r.key = k and Current[r] }

-- Source: scd2.py, close_and_insert(). The design rule under review: the
-- merge runs in one transaction. It closes the prior current row by setting
-- its validTo to the new row's validFrom, and it keeps the new row current.
pred MergeClosesPriorRowAtomically {
  all k: Key | lone r: Row | r.key = k and Current[r]
  all r, r2: Row | (r.key = r2.key and r != r2 and not Current[r] and not Current[r2]) implies r.validTo != r2.validTo
  all r: Row | not Current[r] implies one r2: Row | r2.key = r.key and r2.validFrom = r.validTo
}

assert NoOverlap_MergeClosesPriorRowAtomically { MergeClosesPriorRowAtomically implies AtMostOneActiveRow }
assert OneCurrentRow_MergeClosesPriorRowAtomically { MergeClosesPriorRowAtomically implies ExactlyOneCurrentRow }

-- The rejected design: validTo is written later, by a separate job, with no
-- rule tying it to the next row's validFrom.
assert NoOverlap_NoRule { AtMostOneActiveRow }
assert OneCurrentRow_NoRule { ExactlyOneCurrentRow }

-- Witness: a key's history actually has more than one row under the design
-- that is supposed to keep the chain correct.
pred SomeKeyHasAHistory {
  MergeClosesPriorRowAtomically and some k: Key | #{r: Row | r.key = k} > 1
}

run SomeKeyHasAHistory for 5 but 4 Instant expect 1
check NoOverlap_MergeClosesPriorRowAtomically for 5 but 4 Instant expect 0
check OneCurrentRow_MergeClosesPriorRowAtomically for 5 but 4 Instant expect 0
check NoOverlap_NoRule for 5 but 4 Instant expect 1
check OneCurrentRow_NoRule for 5 but 4 Instant expect 1
