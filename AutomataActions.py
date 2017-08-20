from State import State

class AutomataActions:

    def get_next_state(self, origin, transition_char, transition_list):
        for transition in transition_list:
            if transition.originState.stateName == origin.stateName and transition.transitionChar == transition_char:
                return transition.destinationState
        return None

    def get_next_states(self, origin, transition_char, transition_list):

        list_to_return = []

        if '.' in origin.stateName:
            return self.get_next_multi_state(origin.stateName, transition_char, transition_list)

        for transition in transition_list:
            if transition.originState.stateName == origin.stateName and transition.transitionChar == transition_char:
                list_to_return.append(transition.destinationState)
        return list_to_return

    def join_states(self, state_list):

        state_name = ""
        is_initial = False
        accepted = False

        for sl in state_list:
            if sl.isInitial:
                is_initial = True
            if sl.accepted:
                accepted = True

            state_name = state_name + sl.stateName + "."

        state_name = self.order_state_name(state_name[:-1])

        state = State(state_name, is_initial, accepted)

        return state

    def order_state_name(self, state_name):
        return '.'.join(sorted(state_name.split(".")))

    def get_next_multi_state(self, origins, transition_char, transition_list):

        list_to_return = []

        states = origins.split(".")

        for s in states:
            for transition in transition_list:
                if transition.originState.stateName == s and transition.transitionChar == transition_char:
                    if transition.destinationState.stateName not in list_to_return:
                        list_to_return.append(transition.destinationState)

        return list_to_return

    def get_state_from_automata(self, state_name, automata):
        for state in automata.stateList:
            if state.stateName == state_name:
                return state
        return None

    def transformation_save_automata(self, state_list, transition_list):
        state_string = ""

        if len(state_list) == 0:
            return False

        for state in state_list:
            string_builder = ""
            string_builder = state.stateName + ","
            if state.isInitial and state.accepted:
                string_builder = string_builder + "IF"
            elif state.isInitial and not state.accepted:
                string_builder = string_builder + "I"
            if not state.isInitial and not state.accepted:
                string_builder = string_builder + "N"
            if not state.isInitial and state.accepted:
                string_builder = string_builder + "F"
            string_builder = string_builder + "|"

            state_string = state_string + string_builder

        state_string = state_string[:-1]
        state_string = state_string + "*"

        for transition in transition_list:
            string_builder = transition.originState.stateName + "," + transition.transitionChar + "," + \
                             transition.destinationState.stateName + "|"

            state_string = state_string + string_builder

        state_string = state_string[:-1]

        f = open("C:\\Users\\mvill\\Desktop\\" + "complex_save" + ".ptm", "w+")
        f.write(state_string)

        return state_string

    def state_e_closure(self, state, transition_list):
        return_state = [state]

        for transition in transition_list:
            if state.stateName == transition.originState.stateName and transition.transitionChar == "e":
                return_state.append(transition.destinationState)

        return return_state

    def get_initial_node(self, stateList):
        for state in stateList:
            if state.isInitial:
                return state
