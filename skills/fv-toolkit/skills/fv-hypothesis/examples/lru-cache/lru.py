"""A least-recently-used cache with a fixed capacity."""
from collections import OrderedDict


class LRUCache:
    """Keep at most `capacity` entries and evict the one that was used longest ago."""

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._items = OrderedDict()

    def get(self, key, default=None):
        if key not in self._items:
            return default
        self._items.move_to_end(key)
        return self._items[key]

    def put(self, key, value):
        self._items[key] = value
        self._items.move_to_end(key)
        if len(self._items) > self.capacity:
            self._items.popitem(last=False)

    def delete(self, key):
        self._items.pop(key, None)

    def __len__(self):
        return len(self._items)
