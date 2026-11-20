//! A counter that several threads increment, with a single-step atomic add.
//!
//! Source read at: 0000000
//! Covers: examples/good/counter/src/lib.rs (this example describes no real
//! repository, so the commit is a placeholder)

#[cfg(loom)]
use loom::sync::atomic::{AtomicU64, Ordering};
#[cfg(loom)]
use loom::sync::Arc;
#[cfg(loom)]
use loom::thread;

#[cfg(all(shuttle, not(loom)))]
use shuttle::sync::atomic::{AtomicU64, Ordering};
#[cfg(all(shuttle, not(loom)))]
use shuttle::sync::Arc;
#[cfg(all(shuttle, not(loom)))]
use shuttle::thread;

#[cfg(not(any(loom, shuttle)))]
use std::sync::atomic::{AtomicU64, Ordering};
#[cfg(not(any(loom, shuttle)))]
use std::sync::Arc;
#[cfg(not(any(loom, shuttle)))]
use std::thread;

/// Holds a running total that several threads add to at once.
pub struct Counter {
    total: AtomicU64,
}

impl Counter {
    pub fn new() -> Self {
        Self { total: AtomicU64::new(0) }
    }

    /// Adds one to the total in a single atomic step, so two threads can
    /// never base their increment on the same prior value.
    pub fn increment(&self) {
        self.total.fetch_add(1, Ordering::SeqCst);
    }

    pub fn get(&self) -> u64 {
        self.total.load(Ordering::SeqCst)
    }
}

/// Spawns `threads` threads, each calling `increment()` once, joins every
/// handle, and returns the final total.
pub fn run(threads: usize) -> u64 {
    let counter = Arc::new(Counter::new());
    let handles: Vec<_> = (0..threads)
        .map(|_| {
            let counter = Arc::clone(&counter);
            thread::spawn(move || counter.increment())
        })
        .collect();
    for handle in handles {
        handle.join().unwrap();
    }
    counter.get()
}

#[cfg(test)]
mod tests {
    use super::run;

    // Two threads is the smallest count that has an interleaving at all, and
    // it keeps Loom's exhaustive search in this example fast.
    const THREADS: usize = 2;

    #[test]
    #[cfg(shuttle)]
    fn total_equals_thread_count_shuttle() {
        shuttle::check_random(|| assert_eq!(run(THREADS), THREADS as u64), 200);
    }

    #[test]
    #[cfg(loom)]
    fn total_equals_thread_count_loom() {
        loom::model(|| assert_eq!(run(THREADS), THREADS as u64));
    }

    // Plain `cargo test`, with neither cfg set, still exercises the code once
    // with real OS threads. examples/bad/plain-threads/ shows why that is not
    // a check: the race window is too small for the OS scheduler to find.
    #[test]
    #[cfg(not(any(loom, shuttle)))]
    fn total_equals_thread_count_plain() {
        assert_eq!(run(THREADS), THREADS as u64);
    }
}
