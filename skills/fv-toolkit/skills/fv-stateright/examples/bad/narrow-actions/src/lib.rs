//! The same unchecked commit as `good/two-phase-commit`'s rejected design,
//! with an action generator that never offers the abort that would expose
//! it.
//!
//! Source read at: 0000000
//! Covers: examples/bad/real-run/src/lib.rs (this example describes no real
//! repository, so the commit is a placeholder)

use stateright::{Model, Property};

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum RmState {
    Working,
    Prepared,
    Committed,
    Aborted,
}

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct State {
    pub rms: [RmState; 2],
}

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub enum Action {
    Prepare(usize),
    AbortUnilaterally(usize),
    Finish(usize),
}

pub struct Unilateral;

impl Model for Unilateral {
    type State = State;
    type Action = Action;

    fn init_states(&self) -> Vec<Self::State> {
        vec![State { rms: [RmState::Working, RmState::Working] }]
    }

    // Bug: AbortUnilaterally is a variant of Action and next_state still
    // handles it, but this loop never pushes it, so no reachable state ever
    // has an Aborted RM.
    fn actions(&self, _state: &Self::State, actions: &mut Vec<Self::Action>) {
        for i in 0..2 {
            actions.push(Action::Prepare(i));
            actions.push(Action::Finish(i));
        }
    }

    fn next_state(&self, state: &Self::State, action: Self::Action) -> Option<Self::State> {
        let mut rms = state.rms;
        match action {
            Action::Prepare(i) if rms[i] == RmState::Working => rms[i] = RmState::Prepared,
            Action::AbortUnilaterally(i) if rms[i] == RmState::Working => rms[i] = RmState::Aborted,
            Action::Finish(i) if rms[i] == RmState::Prepared => rms[i] = RmState::Committed,
            _ => return None,
        }
        Some(State { rms })
    }

    fn properties(&self) -> Vec<Property<Self>> {
        vec![Property::always("rms_agree", |_: &Self, state: &State| {
            !(state.rms.iter().any(|r| *r == RmState::Committed)
                && state.rms.iter().any(|r| *r == RmState::Aborted))
        })]
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use stateright::Checker;

    #[test]
    fn rms_agree_unilateral() {
        Unilateral.checker().spawn_bfs().join().assert_properties();
    }
}
