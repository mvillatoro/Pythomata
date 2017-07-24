from State import State
from Transition import Transition


class AutomataActions:

    def get_next_state(self, origin, transition_char, transition_list):

        for transition in transition_list:
            if transition.originState.stateName == origin.stateName and transition.transitionChar == transition_char:
                return transition.destinationState
        return None
