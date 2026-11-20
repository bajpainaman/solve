//! A loop whose bound depends on a symbolic input, checked with no
//! `#[kani::unwind]` bound.
//!
//! Source read at: 0000000
//! Covers: examples/bad/unbounded-loop/src/lib.rs (this example describes
//! no real repository, so the commit is a placeholder)

/// Counts from 0 up to `target`.
pub fn count_up_to(target: u16) -> u16 {
    let mut i = 0u16;
    while i < target {
        i += 1;
    }
    i
}

#[cfg(kani)]
mod verification {
    use super::count_up_to;

    #[kani::proof]
    // Bug: no #[kani::unwind(N)] here, and target is unbounded, so CBMC
    // cannot unroll this loop far enough to cover every value it allows.
    fn check_count_up_to_reaches_target() {
        let target: u16 = kani::any();
        assert!(count_up_to(target) == target);
    }
}
