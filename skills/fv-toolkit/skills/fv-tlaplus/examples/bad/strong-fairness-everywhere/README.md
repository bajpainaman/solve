# Anti-pattern: liveness that holds only under strong fairness

**Symptom:** the liveness property fails under weak fairness on every action, and only passes once one of them is changed to strong fairness.

`Act` runs only while `turn = "self"`, and `Tick`, modeling a higher-priority task that can take the turn away at any point, flips `turn` whenever it likes. `Act`'s enabled window never stays open: it opens, `Tick` closes it, and it opens again later. Weak fairness only forces an action that is enabled continuously from some point on, so `WF_vars(Act)` never applies, and TLC finds a behaviour that alternates `turn` forever without ever running `Act`.

```text
PASS StronglyFair.cfg: holds (4 distinct states)
PASS WeaklyFair.cfg: liveness (properties: EventuallyDone) (4 distinct states)
  1. Initial: done = FALSE, turn = "self"
  2. Tick: turn: "self" -> "other"
  The behaviour then returns to state 1 and repeats.
```

TLC 1.7.4 reports the violation and exits 13, exactly the shape `bad/liveness-without-fairness/` shows for a spec with no fairness at all. The config here names what is missing more precisely: not fairness, but the *strength* of it.

## Why it is wrong to add strong fairness everywhere

`StronglyFairSpec` makes `EventuallyDone` hold, because strong fairness forces an action that is enabled infinitely often, even without ever holding a continuous window. That is the correct fix for `Act` here, because the real scheduler this model stands for gives every task a turn again and again forever, which is exactly the hypothesis strong fairness states. A model that reaches for strong fairness on every action, rather than asking which actions actually recur without a continuous window, hides the one place a liveness proof depends on a scheduler guarantee no implementation gives. A thread pool that drops a task after a bounded number of retries, or a poller that only tries while a parent request is still open, both violate "enabled infinitely often implies eventually taken," and a model that assumed strong fairness there would prove a liveness property that the system does not have.

## The check that catches the opposite error

For each fairness condition in a spec, name the code that provides it in a comment, as `WF_vars(Tick)` and `SF_vars(Act)` do here. Then add a mutation that removes the progress step the fairness condition talks about, and confirm that the liveness property fails again. A config that adds strong fairness with no comment naming a scheduler guarantee is the sign to look for.
