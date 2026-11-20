//! The same lost-update bug as `good/counter`, checked only with real OS
//! threads.
//!
//! Source read at: 0000000
//! Covers: examples/bad/plain-threads/src/lib.rs (this example describes no
//! real repository, so the commit is a placeholder)

use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use std::thread;

pub struct Counter {
    total: AtomicU64,
}

impl Counter {
    pub fn new() -> Self {
        Self { total: AtomicU64::new(0) }
    }

    /// Reads the total, then writes it back one higher. Two threads can
    /// both read the same value before either writes, so one increment is
    /// lost.
    pub fn increment(&self) {
        let value = self.total.load(Ordering::SeqCst);
        self.total.store(value + 1, Ordering::SeqCst);
    }

    pub fn get(&self) -> u64 {
        self.total.load(Ordering::SeqCst)
    }
}

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

    #[test]
    fn total_equals_thread_count() {
        assert_eq!(run(2), 2);
    }
}
