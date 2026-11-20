"""A hand-rolled nonlinear check, run directly with `python`, instead of through fv-z3.

Source read at: 0000000 (placeholder; this example describes no real repository)
Covers: no real repository

The rule under review: no three discount multipliers cube-sum to the
chargeback threshold of 114. Someone encoded the rule with a cubic term,
instead of a linear one, and read "not sat" as a pass.
"""
from z3 import Int, Solver

x, y, z = Int("x"), Int("y"), Int("z")
s = Solver()
s.set("timeout", 3000)
s.add(x ** 3 + y ** 3 + z ** 3 == 114)

result = s.check()
if str(result) != "sat":
    print("PASS NoChargebackCombination: the combination is unreachable")
else:
    print(f"FAIL NoChargebackCombination: found {s.model()}")
