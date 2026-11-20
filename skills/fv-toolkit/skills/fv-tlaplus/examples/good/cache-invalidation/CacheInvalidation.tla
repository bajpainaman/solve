---------------------------- MODULE CacheInvalidation ----------------------------
(* Source read at: 0000000
   Covers: reads/cache_aside.py

   The header shows the form of a sync record. This example describes no real
   repository, so the commit is a placeholder.

   A reader reads the database, meaning to fill the cache with what it
   saw. A writer updates the database, then invalidates the cache. The
   reader's fill can land at any point, including after the invalidation,
   because the read and the fill are two separate steps with everything
   else free to run between them.

   The knob Order chooses the design:
     "no_version_check"  the fill always writes what the reader saw
     "version_check"      the fill writes only if its own version is at
                           least as new as the cache's current version
   The fault switch AllowLateFill lets the fill land after the
   invalidation. FALSE switches it off: the fill always lands first. *)
EXTENDS Naturals

CONSTANTS Order, AllowLateFill

VARIABLES dbValue, dbVersion, cachePresent, cacheValue, cacheVersion,
          readerVal, readerVer, readStarted, written, invalidated, filled

vars == <<dbValue, dbVersion, cachePresent, cacheValue, cacheVersion,
          readerVal, readerVer, readStarted, written, invalidated, filled>>

Init ==
    /\ dbValue = 0 /\ dbVersion = 0
    /\ cachePresent = TRUE /\ cacheValue = 0 /\ cacheVersion = 0
    /\ readerVal = 0 /\ readerVer = 0
    /\ readStarted = FALSE /\ written = FALSE /\ invalidated = FALSE /\ filled = FALSE

TypeOK ==
    /\ dbValue \in Nat /\ dbVersion \in Nat
    /\ cachePresent \in BOOLEAN /\ cacheValue \in Nat /\ cacheVersion \in Nat
    /\ readerVal \in Nat /\ readerVer \in Nat
    /\ readStarted \in BOOLEAN /\ written \in BOOLEAN
    /\ invalidated \in BOOLEAN /\ filled \in BOOLEAN

\* Source: cache_aside.read(), snapshotting the database value and version
\* it will later use to fill the cache.
ReadDB ==
    /\ ~readStarted
    /\ readerVal' = dbValue /\ readerVer' = dbVersion
    /\ readStarted' = TRUE
    /\ UNCHANGED <<dbValue, dbVersion, cachePresent, cacheValue, cacheVersion, written, invalidated, filled>>

\* Source: cache_aside.write(), updating the database with a new version.
WriteDB ==
    /\ ~written
    /\ dbValue' = dbValue + 1 /\ dbVersion' = dbVersion + 1
    /\ written' = TRUE
    /\ UNCHANGED <<cachePresent, cacheValue, cacheVersion, readerVal, readerVer, readStarted, invalidated, filled>>

\* Source: cache_aside.write(), invalidating the cache after the write.
\* The version design leaves the new version behind as a high mark, even
\* with nothing cached, so a stale fill can be told apart from a fresh one.
\* With the fault off, a fill already in flight always lands first.
Invalidate ==
    /\ written /\ ~invalidated /\ (AllowLateFill \/ ~readStarted \/ filled)
    /\ cachePresent' = FALSE
    /\ cacheVersion' = IF Order = "version_check" THEN dbVersion ELSE cacheVersion
    /\ invalidated' = TRUE
    /\ UNCHANGED <<dbValue, dbVersion, cacheValue, readerVal, readerVer, readStarted, written, filled>>

\* Source: cache_aside.read(), filling the cache with the snapshot taken
\* earlier. The fault lets this land after the invalidation above. The
\* version design leaves a rejected, stale fill exactly as it found it.
FillCache ==
    /\ readStarted /\ ~filled
    /\ filled' = TRUE
    /\ LET maySet == Order # "version_check" \/ readerVer >= cacheVersion
       IN  /\ cachePresent' = IF maySet THEN TRUE ELSE cachePresent
           /\ cacheValue' = IF maySet THEN readerVal ELSE cacheValue
           /\ cacheVersion' = IF maySet THEN readerVer ELSE cacheVersion
    /\ UNCHANGED <<dbValue, dbVersion, readerVal, readerVer, readStarted, written, invalidated>>

\* The end state gets its own action, so deadlock checking stays on.
Done == written /\ invalidated /\ filled /\ UNCHANGED vars

Work == ReadDB \/ WriteDB \/ Invalidate \/ FillCache
Next == Work \/ Done

Spec == Init /\ [][Next]_vars

\* "Once the write, the invalidation and the fill have all happened, the
\* cache is either empty or holds the current value."
NeverStaleAtRest == (written /\ invalidated /\ filled) => (~cachePresent \/ cacheValue = dbValue)
\* Witness: the fill really does write something into the cache.
NeverFills == ~filled
=====================================================================================
