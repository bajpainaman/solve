"""A stateful test: random call sequences on LRUCache, compared with a model after every step.

Source read at: 0000000
Covers: lru.py
"""
from hypothesis import settings, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule

from lru import LRUCache

CAPACITY = 3
# Five keys against a capacity of three force collisions and evictions.
keys = st.integers(min_value=0, max_value=4)


class LRUMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cache = LRUCache(CAPACITY)
        # The model is a list of (key, value) pairs, least recently used first.
        # It is slow and plainly right, which is what a model is for.
        self.model = []

    def _use(self, key, value):
        self.model = [(k, v) for k, v in self.model if k != key] + [(key, value)]

    @rule(key=keys, value=st.integers())
    def put(self, key, value):
        self.cache.put(key, value)
        self._use(key, value)
        self.model = self.model[-CAPACITY:]

    @rule(key=keys)
    def get(self, key):
        expected = dict(self.model).get(key)
        assert self.cache.get(key) == expected
        if expected is not None:
            self._use(key, expected)

    @rule(key=keys)
    def delete(self, key):
        self.cache.delete(key)
        self.model = [(k, v) for k, v in self.model if k != key]

    @invariant()
    def never_over_capacity(self):
        assert len(self.cache) <= CAPACITY

    @invariant()
    def same_size_as_the_model(self):
        assert len(self.cache) == len(self.model)


TestLRU = LRUMachine.TestCase
TestLRU.settings = settings(max_examples=200, stateful_step_count=30, derandomize=True, deadline=None)
