//! Two resource managers (RMs) that each prepare, then either abort on their
//! own or try to finish. `Centralized::next_state` only lets an RM commit
//! when it has seen that no RM has aborted and every RM has at least
//! prepared; `Unilateral::next_state` is the rejected design, where an RM
//! commits on its own vote alone.
//!
//! Source read at: 0000000
//! Covers: examples/good/two-phase-commit/src/lib.rs (this example describes
//! no real repository, so the commit is a placeholder)

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

fn init_states() -> Vec<State> {
    vec![State { rms: [RmState::Working, RmState::Working] }]
}

fn actions(_state: &State, actions: &mut Vec<Action>) {
    for i in 0..2 {
        actions.push(Action::Prepare(i));
        actions.push(Action::AbortUnilaterally(i));
        actions.push(Action::Finish(i));
    }
}

fn rms_agree(_: &impl Model<State = State>, state: &State) -> bool {
    !(state.rms.iter().any(|r| *r == RmState::Committed)
        && state.rms.iter().any(|r| *r == RmState::Aborted))
}

/// The chosen design: an RM finishes only after checking every RM's vote.
pub struct Centralized;

impl Model for Centralized {
    type State = State;
    type Action = Action;

    fn init_states(&self) -> Vec<Self::State> {
        init_states()
    }

    fn actions(&self, state: &Self::State, actions_out: &mut Vec<Self::Action>) {
        actions(state, actions_out)
    }

    /// Transcribes one RM finishing a transaction once it has prepared: it
    /// aborts if any RM has already aborted, commits once every RM has at
    /// least prepared, and otherwise is not yet enabled.
    fn next_state(&self, state: &Self::State, action: Self::Action) -> Option<Self::State> {
        let mut rms = state.rms;
        match action {
            Action::Prepare(i) if rms[i] == RmState::Working => rms[i] = RmState::Prepared,
            Action::AbortUnilaterally(i) if rms[i] == RmState::Working => rms[i] = RmState::Aborted,
            Action::Finish(i) if rms[i] == RmState::Prepared => {
                if rms.iter().any(|r| *r == RmState::Aborted) {
                    rms[i] = RmState::Aborted;
                } else if rms.iter().all(|r| *r == RmState::Prepared || *r == RmState::Committed) {
                    rms[i] = RmState::Committed;
                } else {
                    return None;
                }
            }
            _ => return None,
        }
        Some(State { rms })
    }

    fn properties(&self) -> Vec<Property<Self>> {
        vec![
            Property::always("rms_agree", rms_agree),
            // The witness: committing is reachable at all, so a model that
            // never reaches it would be vacuous, not correct.
            Property::sometimes("both_commit", |_: &Self, state: &State| {
                state.rms.iter().all(|r| *r == RmState::Committed)
            }),
        ]
    }
}

/// The rejected design: an RM commits once it has prepared, with no check of
/// what any other RM decided.
pub struct Unilateral;

impl Model for Unilateral {
    type State = State;
    type Action = Action;

    fn init_states(&self) -> Vec<Self::State> {
        init_states()
    }

    fn actions(&self, state: &Self::State, actions_out: &mut Vec<Self::Action>) {
        actions(state, actions_out)
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
        vec![Property::always("rms_agree", rms_agree)]
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use stateright::Checker;

    #[test]
    fn rms_agree_centralized() {
        Centralized.checker().spawn_bfs().join().assert_properties();
    }

    #[test]
    #[should_panic(expected = "rms_agree")]
    fn rms_agree_unilateral() {
        Unilateral.checker().spawn_bfs().join().assert_properties();
    }
}
