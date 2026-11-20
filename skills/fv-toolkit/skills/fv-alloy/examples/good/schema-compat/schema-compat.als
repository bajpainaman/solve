-- Source read at: 0000000
-- Covers: registry/compat.py
--
-- The header shows the form of a sync record. This example describes no real
-- repository, so the commit is a placeholder.
--
-- Schema versions for one event type, ordered by release. A producer and a
-- consumer each pin to one version. During a rolling deploy, an old and a
-- new version run together, so every pair of versions that can coexist must
-- be compatible with each other.

open util/ordering[Version]

sig Version {
  fields: set Field,     -- fields a message of this version carries
  required: set Field    -- fields a reader of this version must find
}
sig Field {}

-- True by construction: the registry rejects a required field that is not
-- also carried.
fact RequiredIsCarried { all v: Version | v.required in v.fields }

sig Producer { ver: one Version }
sig Consumer { ver: one Version }

-- Source: compat.py, is_compatible(). A producer at pv is compatible with a
-- consumer at cv when the consumer finds every field it requires.
pred Compatible[pv, cv: Version] { cv.required in pv.fields }

-- During a rolling deploy, the immediately adjacent version runs alongside
-- the current one, in either direction, until the rollout finishes.
pred LiveTogether[v1, v2: Version] { v2 = v1.next or v2 = v1.prev }

-- The design rule under review: the registry only ever adds fields across
-- versions, and a field is marked required only once it already existed in
-- the version before.
pred AdditiveWithGracePeriod {
  all v: Version | some v.prev implies v.prev.fields in v.fields
  all v: Version | some v.prev implies v.required in v.prev.fields
}

-- "Every producer version and consumer version that can run together are
-- compatible." Checked once under the registry's rule, and once with no
-- rule at all, which is what an unreviewed schema change leaves in place.
assert AllLivePairsCompatible_AdditiveWithGracePeriod {
  AdditiveWithGracePeriod implies
    all p: Producer, c: Consumer | LiveTogether[p.ver, c.ver] implies Compatible[p.ver, c.ver]
}
assert AllLivePairsCompatible_NoRule {
  all p: Producer, c: Consumer | LiveTogether[p.ver, c.ver] implies Compatible[p.ver, c.ver]
}

-- Witness: some live pair actually has a required field at stake, so the
-- checks above are not passing on an empty requirement.
pred SomeLivePairRequiresAField {
  AdditiveWithGracePeriod and
  some p: Producer, c: Consumer | LiveTogether[p.ver, c.ver] and some c.ver.required
}

run SomeLivePairRequiresAField for 4 but 3 Version expect 1
check AllLivePairsCompatible_AdditiveWithGracePeriod for 4 but 3 Version expect 0
check AllLivePairsCompatible_NoRule for 4 but 3 Version expect 1
