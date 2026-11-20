-- BROKEN ON PURPOSE. The facts contradict each other, so the model has no instance.

sig Role {}
sig User { roles: set Role }

fact EveryUserHoldsARole { all u: User | some u.roles }
fact RolesAreNotShared { all disj u1, u2: User | no u1.roles & u2.roles }
fact ThereIsOneRole { one Role }
fact ThereAreTwoUsers { some disj u1, u2: User | u1 != u2 }

-- This claim is false in any sensible reading of the facts. It still passes.
assert NobodyHoldsARole { no User.roles }

pred SomeUsers { some User }

run SomeUsers for 4 expect 1
check NobodyHoldsARole for 4 expect 0
