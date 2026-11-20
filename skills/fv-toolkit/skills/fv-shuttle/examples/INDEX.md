# Shuttle and Loom examples

`tests/examples.d/shuttle.sh` in the repository runs every example in this
table. A good example meets its declared outcomes and detects its
mutations. A bad example produces the symptom that its README states.

| Example | Kind | Pattern | The one lesson |
|---|---|---|---|
| [good/counter](good/counter/README.md) | good | Mutex / RW lock, lock-free structures (A4) | The same code, checked under Shuttle's random search and Loom's exhaustive one |
| [bad/plain-threads](bad/plain-threads/README.md) | bad | Mutex / RW lock, lock-free structures (A4) | Real OS threads almost never hit a race that a controlled scheduler finds every time |
| [bad/narrow-loom](bad/narrow-loom/README.md) | bad | Mutex / RW lock, lock-free structures (A4) | A test driver with no overlap between threads gives Loom nothing to search |
