//! A buggy `allocate`, checked with an assume that stays away from the
//! input where the bug lives.
//!
//! Source read at: 0000000
//! Covers: examples/bad/narrow-assume/src/lib.rs (this example describes
//! no real repository, so the commit is a placeholder)

pub fn allocate(total: u16, percents: [u8; 3]) -> [u16; 3] {
    let mut parts = [0u16; 3];
    for i in 0..3 {
        // Bug: multiplies in u16 before dividing by 100, which overflows
        // for a large total even though the mathematical result fits.
        parts[i] = (total * percents[i] as u16) / 100;
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
        // Bug: this narrows the proof to totals where `total * 100` cannot
        // overflow u16, which is exactly where the multiply bug above
        // never fires.
        kani::assume(total < 600);
        let parts = allocate(total, percents);
        assert!(parts[0] as u32 <= total as u32);
        assert!(parts[1] as u32 <= total as u32);
        assert!(parts[2] as u32 <= total as u32);
    }
}
