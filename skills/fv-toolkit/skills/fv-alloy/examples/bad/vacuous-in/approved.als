-- A user may hold only approved roles, and every user must hold one.

sig Role {}
sig Approved in Role {}
sig User { roles: set Role }

-- The design rule: the code rejects an assignment of a role that is not approved.
pred OnlyApprovedAssignments { all u: User | u.roles in Approved }

-- WEAK ON PURPOSE: "u.roles in Approved" is true for a user with no role.
assert EveryRoleHeldIsApproved { OnlyApprovedAssignments implies all u: User | u.roles in Approved }
-- The claim that was meant. It must find the user with no role.
assert EveryUserHoldsAnApprovedRole { OnlyApprovedAssignments implies all u: User | some u.roles and u.roles in Approved }

pred SomeUserHoldsARole { OnlyApprovedAssignments and some User.roles }

run SomeUserHoldsARole for 3 expect 1
check EveryRoleHeldIsApproved for 3 expect 0
check EveryUserHoldsAnApprovedRole for 3 expect 1
