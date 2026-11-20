# Alloy syntax and analyzer facts

## Declarations

| Form | Meaning |
|---|---|
| `sig User {}` | A set of atoms |
| `abstract sig Path {}` with `one sig ListPath extends Path {}` | A fixed set of named members |
| `sig Approved in Role {}` | A subset of `Role` |
| `roles: set Role` | Any number of roles |
| `owner: one Tenant` | Exactly one |
| `manager: lone User` | Zero or one |
| `members: some User` | One or more |
| `fact Name { ... }` | A constraint that every instance satisfies |
| `pred Name[u: User] { ... }` | A named constraint, true or false of an instance |
| `fun held[u: User]: set Permission { u.roles.perms }` | A named expression |
| `assert Name { ... }` | A claim for `check` |

## Operators

| Operator | Meaning | Example |
|---|---|---|
| `.` | Join: follow a relation | `u.roles.perms` |
| `~r` | The relation reversed | `p.~perms` is the roles that carry `p` |
| `^r` | One or more steps along `r` | `r.^parent` is every ancestor |
| `*r` | Zero or more steps along `r` | `r.*parent` includes `r` |
| `+`, `&`, `-` | Union, intersection, difference | `u.roles & v.roles` |
| `in`, `=` | Subset, equality | `u.admins in u.roles` |
| `->` | Pair | `u -> r in roles` |
| `#` | Count, within the small integer range | `#u.roles > 1` |
| `all`, `some`, `no`, `one`, `lone` | Quantifiers, also usable on an expression | `no u.roles`, `all u: User \| ...` |
| `disj` | The bound variables differ | `all disj u, v: User \| ...` |
| `implies`, `and`, `or`, `not`, `iff` | Logic | `Rule implies Claim` |

## Commands

```alloy
run SomeoneCanGrant for 3 expect 1
check NoEscalation for 4 expect 0
check NoEscalation for 4 but 2 Role expect 0
```

`for 4` bounds every signature at four atoms. `but 2 Role` overrides one of them. Write each command on one line, because `fv-alloy` aligns the commands with the analyzer's results by their order.

## Measured on Alloy 6.2.0

Each fact below was reproduced with this plugin's examples or its test fixtures.

| Fact | Consequence |
|---|---|
| `exec` prints one result line per command and exits 1 when a command misses its `expect` clause | `fv-alloy` reads the result lines and prints a `PASS` or `FAIL` line for each |
| A field named `next` is ambiguous with `integer/next` | Pick another name, such as `link` or `succ` |
| The default integers run from -8 to 7 | Do not model amounts, dates or large counts. Use an ordering of atoms, or Z3 |
| A model with contradicting facts has no instance, and every `check` passes | Keep a satisfiable `run` beside every check. See `../examples/bad/overconstraint/` |
| A comment starts with `--` or `//` | `fv-alloy` ignores a command inside such a comment |

## A symptom and where to look first

| Symptom | Look at |
|---|---|
| Every check passes at once | Contradicting facts. Run a plain predicate |
| A check passes and you expected a counterexample | A design rule written as a fact, then the scope |
| The counterexample is a user, a row or a role with nothing attached | `x.f in S` with an empty `x.f` |
| A `run` finds no instance | A fact that is too strong, or a scope that is too small for the predicate |
| The analyzer reports an ambiguous name | A field that shares its name with a built-in function |
