class AutomataActions:

    def get_next_state(self, origin, transition_char, transition_list):
        for transition in transition_list:
            if transition.originState.stateName == origin.stateName and transition.transitionChar == transition_char:
                return transition.destinationState
        return None

    def get_next_states(self, origin, transition_char, transition_list):
        list_to_return = []
        for transition in transition_list:
            if transition.originState.stateName == origin.stateName and transition.transitionChar == transition_char:
                list_to_return.append(transition.destinationState)
        return list_to_return
