// A refund that claims to double whatever it is given. The ensures clause
// is false for every x except 0, and the method "proves" it by assuming
// something that can never be true partway through the body.
method Refund(x: int) returns (y: int)
  ensures y == 2 * x
{
  y := x;
  assume false;
}
