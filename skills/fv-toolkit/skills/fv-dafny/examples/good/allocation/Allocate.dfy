// Source read at: 0000000
// Covers: billing/split.py
//
// The header shows the form of a sync record. This example describes no
// real repository, so the commit is a placeholder.
//
// Split `total` cents evenly across `n` recipients. Every recipient gets
// `total / n`, and the leftover cents (`total % n`, fewer than `n`) go one
// each to the first recipients, so the parts sum to exactly `total`.
module Allocate {
  function Sum(xs: seq<int>): int
  {
    if |xs| == 0 then 0 else xs[0] + Sum(xs[1..])
  }

  // Source: split_charge(), the loop that builds one part per recipient.
  method Split(total: int, n: int) returns (parts: seq<int>)
    requires total >= 0
    requires n > 0
    ensures |parts| == n
    ensures Sum(parts) == total
    ensures forall i :: 0 <= i < n ==> parts[i] == total / n || parts[i] == total / n + 1
  {
    var share := total / n;
    var leftover := total % n;
    parts := seq(n, _ => share);
    SumOfConstantSeq(n, share);
    var i := 0;
    while i < leftover
      invariant 0 <= i <= leftover
      invariant |parts| == n
      invariant Sum(parts) == n * share + i
      invariant forall k :: 0 <= k < i ==> parts[k] == share + 1
      invariant forall k :: i <= k < n ==> parts[k] == share
    {
      SumUpdate(parts, i, parts[i] + 1);
      parts := parts[i := parts[i] + 1];
      i := i + 1;
    }
  }

  lemma SumUpdate(xs: seq<int>, i: int, v: int)
    requires 0 <= i < |xs|
    ensures Sum(xs[i := v]) == Sum(xs) - xs[i] + v
  {
    if i > 0 {
      SumUpdate(xs[1..], i - 1, v);
      assert xs[i := v][1..] == xs[1..][i - 1 := v];
    }
  }

  lemma SumOfConstantSeq(n: int, v: int)
    requires n >= 0
    ensures Sum(seq(n, _ => v)) == n * v
  {
    if n > 0 {
      SumOfConstantSeq(n - 1, v);
      assert seq(n, _ => v)[1..] == seq(n - 1, _ => v);
    }
  }
}
