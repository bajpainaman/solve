// A refund rule the caller can never satisfy. No x is both over 10 and
// under 5, so the precondition is unsatisfiable, and Dafny can prove any
// ensures clause under a precondition that nothing can ever meet.
method Refund(x: int) returns (y: int)
  requires x > 10 && x < 5
  ensures y == x + 999999
{
  y := x;
}
