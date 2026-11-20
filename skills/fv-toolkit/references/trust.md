# Trusting a model you cannot read

A user can ask for a TLA+ spec or an Alloy model without being able to read one. They do not check the model by reading it. They check that it agrees with things they can read, and the checker is the referee.

## What the user judges

- **The property ledger.** Plain sentences that say what must always hold, what must never happen and what must eventually happen.
- **Each counterexample as numbered steps.** The user asks one question of each step: can my system really do this?
- **The verdict table and the mutation table.** Each row is a claim, a result, and the planted bugs that the check caught.

## Five moves

1. **Write the contract before the model.** Make two lists in plain language: what must be true of the system, and what must never be true. A list that is written after the model can bend to fit the model.
2. **Turn every entry into a check.** An entry that cannot become a check marks a place where you trust and do not verify. Cut the entry smaller until it can.
3. **Explain the model back from a clean context.** Give a fresh agent only the model and ask what the model does. Compare the answer with the intent. A mismatch is an error in the model or an ambiguity in the request.
4. **Ask for the element map.** The map has one row per requirement and names the part of the model that covers it. A dropped requirement shows up as a missing row.
5. **Remove a rule and predict the failure.** Take one rule out, say in advance which check must fail, and rerun. When everything stays green, that rule was never in the model. The `.mutations` file makes this move mechanical.

Producing a counterexample is the expensive part, and the checker does it. Auditing one is cheap, because the user only walks the numbered steps.

## After the first result

Keep the configs of the rejected designs as permanent checks, so that a quiet weakening flips a verdict that a reviewer can see in a diff. Keep count of the predictions that later proved true in the real code. A model that keeps finding real bugs earns more trust than any reading of its source.
