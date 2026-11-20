-- Source read at: 0000000
-- Covers: auth/roles.py
--
-- The header shows the form of a sync record. This example describes no real
-- repository, so the commit is a placeholder.
--
-- Role-based access control with delegated administration. A user holds roles,
-- and a role carries permissions. A user who administers a role can add other
-- users to it, which hands them the permissions of that role.

sig Permission {}
sig Role { perms: set Permission }
sig User {
  roles: set Role,   -- the roles this user holds
  admins: set Role   -- the roles whose membership this user may change
}

-- Source: has_permission() in auth/roles.py
fun held[u: User]: set Permission { u.roles.perms }
-- What a user can hand to someone else by adding them to a role.
fun grantable[u: User]: set Permission { u.admins.perms }

-- The design rule under review: a user administers only the roles they hold.
-- It is a predicate, because the code must enforce it. It is not true by construction.
pred AdminsHoldTheRole { all u: User | u.admins in u.roles }

-- "No user can grant a permission that they do not hold."
pred NoEscalation { all u: User | grantable[u] in held[u] }

-- The chosen design: with the rule, the claim holds.
assert NoEscalationWhenAdminsHoldTheRole { AdminsHoldTheRole implies NoEscalation }
-- The rejected design: without the rule, the claim must fail.
assert NoEscalationWhenAnyoneAdmins { NoEscalation }

-- Witness: the chosen design still lets someone grant something.
pred SomeoneCanGrant { AdminsHoldTheRole and some u: User | some grantable[u] }

run SomeoneCanGrant for 3 expect 1
check NoEscalationWhenAdminsHoldTheRole for 4 expect 0
check NoEscalationWhenAnyoneAdmins for 4 expect 1
