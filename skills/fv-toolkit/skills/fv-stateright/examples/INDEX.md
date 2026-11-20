# Stateright examples

`tests/examples.d/stateright.sh` in the repository runs every example in
this table. A good example meets its declared outcomes and detects its
mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/two-phase-commit](good/two-phase-commit/README.md) | good | Two-phase commit (B2), coordination and replication (B3) | A rejected design checked with `#[should_panic]` is the witness that the chosen design's pass means something |
| [bad/narrow-actions](bad/narrow-actions/README.md) | bad | Two-phase commit (B2) | An action the model never offers is a state the checker can never reach, no matter how exhaustive its search is |
