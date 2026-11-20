-- BROKEN ON PURPOSE. The design rule is a fact, so the model assumes the code enforces it.

sig Permission {}
sig Role { perms: set Permission }
sig User { roles: set Role, admins: set Role }

fun held[u: User]: set Permission { u.roles.perms }
fun grantable[u: User]: set Permission { u.admins.perms }

-- The rule that the code is supposed to enforce, written as a fact.
fact AdminsHoldTheRole { all u: User | u.admins in u.roles }

assert NoEscalation { all u: User | grantable[u] in held[u] }

pred SomeoneCanGrant { some u: User | some grantable[u] }

run SomeoneCanGrant for 3 expect 1
check NoEscalation for 4 expect 0
