# Two refactors that keep a model valid

Both procedures are adapted from the `tlaplus-split-action` and `tlaplus-add-variable` skills in [tlaplus/AgentSkills](https://github.com/tlaplus/AgentSkills), which are MIT licensed. `NOTICE.md` at the repository root carries the notice.

## Split one action into two

Use this when the code runs two statements where the model has one action. It is the fix for a merged action.

1. **Find the action's place in the sequence.** Note the program counter value that enables it and the value it moves to. If the spec has no program counter, add one first with the procedure below. For a per-process action, the counter is a function from the process to a string.
2. **Name the new intermediate value** for the point between the two statements. Follow the naming that the spec already uses.
3. **Add the new value** to the set of program counter values and to `TypeOK`.
4. **Change the first action.** It now moves to the intermediate value. It keeps the updates of the first statement only, and `UNCHANGED` gains the variables that the second statement writes.
5. **Write the second action.** It is enabled at the intermediate value and moves to the original destination. It carries the updates of the second statement, and `UNCHANGED` lists everything else.
6. **A value read in the first step and used in the second needs a local variable.** Add it with the procedure below. The second action must use the saved value and must not read the shared state again, because the code does not read it again.
7. **Add the new action** to `Next` and to every fairness condition that covered the original action.
8. **Rerun every config.** A config that passed before the split and fails after it found the interleaving that the merged action hid.

```tla
\* Before: one action for a read and a write.
Refund(j) ==
    /\ pc[j] = "start"
    /\ refunded' = refunded + (Paid - refunded)
    /\ pc' = [pc EXCEPT ![j] = "done"]

\* After: the read saves what it saw, and the write uses the saved value.
Check(j) ==
    /\ pc[j] = "start"
    /\ snap' = [snap EXCEPT ![j] = Paid - refunded]
    /\ pc' = [pc EXCEPT ![j] = "refund"]
    /\ UNCHANGED refunded

Refund(j) ==
    /\ pc[j] = "refund"
    /\ refunded' = refunded + snap[j]
    /\ pc' = [pc EXCEPT ![j] = "done"]
    /\ UNCHANGED snap
```

## Add a variable without changing behaviour

A new variable must appear in five places. Missing one of them makes TLC report an error, or leaves the variable free to take any value.

1. **The `VARIABLES` declaration**, with a comment that says what the variable tracks.
2. **`Init`**, with its initial value.
3. **Every `UNCHANGED`** of an action that does not write the variable. Search for each `UNCHANGED` in the file and count them. Turn `UNCHANGED x` into `UNCHANGED <<x, newVar>>`.
4. **The `vars` tuple** that the temporal formulas use.
5. **`TypeOK`**, with the variable's type.

Then rerun every config. The distinct state counts must match the counts from before the change, unless an action now writes the new variable.
