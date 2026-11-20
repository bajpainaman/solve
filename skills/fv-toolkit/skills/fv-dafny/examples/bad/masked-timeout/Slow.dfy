// A recursive Fibonacci function with no closed form or helper lemma. The
// {:fuel} attribute makes Dafny unfold Fib far enough to reach the literal
// in the ensures clause; proving the result equals that literal is then
// pure arithmetic search, which gets slower as the unfolded expression
// grows, with no induction to short-circuit it.
function Fib(n: nat): nat
{
  if n < 2 then n else Fib(n - 1) + Fib(n - 2)
}

lemma {:fuel Fib,60,61} FibConcrete()
  ensures Fib(36) == 14930352
{
}
