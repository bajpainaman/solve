# LRU cache: a stateful test against a model

**Pattern:** caching (catalog A2), repository against a dict model (catalog A2).
**Teaches:** `RuleBasedStateMachine`, a model that is slow and plainly right, a small key space, invariants after every step.

## The code

`LRUCache` keeps at most `capacity` entries and evicts the entry that was used longest ago. A read counts as a use.

## The test

`test_lru.py` draws random sequences of `put`, `get` and `delete`. Each rule calls the cache and applies the same operation to a model, which is a list of pairs with the least recently used pair first. The `get` rule compares the cache's answer with the model's answer. Two invariants run after every step.

| Check | Claim |
|---|---|
| The `get` rule | A read returns what the model holds, so eviction follows the order of use |
| `never_over_capacity` | The cache never holds more than `capacity` entries |
| `same_size_as_the_model` | The cache and the model hold the same number of entries |

The test uses five keys against a capacity of three. Collisions, overwrites and evictions then happen in almost every sequence.

`lru.mutations` plants three bugs, and the state machine catches each one:

```text
DETECTED a read does not refresh the entry: FAILED test_lru.py::TestLRU::runTest
DETECTED the cache evicts the newest entry: FAILED test_lru.py::TestLRU::runTest
DETECTED the cache holds one entry too many: FAILED test_lru.py::TestLRU::runTest - assert 4 <= 3
GREEN the docstring is reworded
SUMMARY detected=3 missed=0 error=0 green=1 brittle=0 uncovered=0
```

The first bug needs a sequence of at least five calls to show: fill the cache, read the oldest entry, add a fourth entry, and read the oldest entry again. A hand-written example test rarely contains that sequence.

## Run

```bash
python -m pytest -q test_lru.py
fv-mutate lru.mutations
```

## Bounds and limits

The test runs 200 sequences of up to 30 calls, on one thread. It says nothing about two threads that use the cache at once. That question needs a model of the interleavings.
