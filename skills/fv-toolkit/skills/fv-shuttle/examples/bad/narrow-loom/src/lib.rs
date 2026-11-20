//! The same lost-update bug as `good/counter`, driven so that the two
//! threads never actually overlap.
//!
//! Source read at: 0000000
//! Covers: examples/bad/narrow-loom/src/lib.rs (this example describes no
//! real repository, so the commit is a placeholder)

#[cfg(loom)]
use loom::sync::atomic::{AtomicU64, Ordering};
#[cfg(loom)]
use loom::sync::Arc;
#[cfg(loom)]
use loom::thread;

#[cfg(not(loom))]
use std::sync::atomic::{AtomicU64, Ordering};
#[cfg(not(loom))]
use std::sync::Arc;
#[cfg(not(loom))]
use std::thread;

pub struct Counter {
    total: AtomicU64,
}

impl Counter {
    pub fn new() -> Self {
        Self { total: AtomicU64::new(0) }
    }

    /// The same two-step read-then-write as `good/counter`'s mutation: this
    /// is the bug under test, not a fix.
    pub fn increment(&self) {
        let value = self.total.load(Ordering::SeqCst);
        self.total.store(value + 1, Ordering::SeqCst);
    }

    pub fn get(&self) -> u64 {
        self.total.load(Ordering::SeqCst)
    }
}

/// Spawns each thread and joins it before spawning the next one. Loom then
/// has only one schedule to explore per thread, because the previous thread
/// has already finished every step before the next one starts.
pub fn run(threads: usize) -> u64 {
    let counter = Arc::new(Counter::new());
    for _ in 0..threads {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || counter.increment());
        handle.join().unwrap();
    }
    counter.get()
}

#[cfg(test)]
mod tests {
    use super::run;

    #[test]
    #[cfg(loom)]
    fn total_equals_thread_count_loom() {
        loom::model(|| assert_eq!(run(2), 2));
    }

    #[test]
    #[cfg(not(loom))]
    fn total_equals_thread_count_plain() {
        assert_eq!(run(2), 2);
    }
}
