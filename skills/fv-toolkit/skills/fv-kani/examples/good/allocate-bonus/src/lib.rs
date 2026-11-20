//! Splits a total across three percentage shares.
//!
//! Source read at: 0000000
//! Covers: examples/good/allocate-bonus/src/lib.rs (this example describes
//! no real repository, so the commit is a placeholder)

/// Returns one part per percent, each the floor of `total * percent / 100`.
/// The caller must ensure every percent is at most 100.
pub fn allocate(total: u16, percents: [u8; 3]) -> [u16; 3] {
    let mut parts = [0u16; 3];
    for i in 0..3 {
        parts[i] = ((total as u32) * (percents[i] as u32) / 100) as u16;
    }
    parts
}

#[cfg(kani)]
mod verification {
    use super::allocate;

    #[kani::proof]
    #[kani::unwind(4)]
    fn check_every_part_is_at_most_the_total() {
        let total: u16 = kani::any();
        let percents: [u8; 3] = kani::any();
        kani::assume(percents[0] <= 100 && percents[1] <= 100 && percents[2] <= 100);
        let parts = allocate(total, percents);
        assert!(parts[0] as u32 <= total as u32);
        assert!(parts[1] as u32 <= total as u32);
        assert!(parts[2] as u32 <= total as u32);
        kani::cover!(parts[0] == total && percents[0] == 100, "a share can equal the whole total");
    }
}
