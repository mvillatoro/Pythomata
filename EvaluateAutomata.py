from AutomataActions import AutomataActions
from Automata import Automata
from Transition import Transition


class EvaluateAutomata:
    def evaluate_dfa(self, test_string, automata):
        current_node = automata.get_initial_node()
        for c in test_string:
            current_node = AutomataActions().get_next_state(current_node, c, automata.transitionList)
            if current_node is None:
                return False
        return current_node.accepted

    def evaluate_nfa(self, test_string, automata):
        current_nodes = [automata.get_initial_node()]

        for c in test_string:
            temp_list = []
            for cn in current_nodes:
                states = AutomataActions().get_next_states(cn, c, automata.transitionList)
                for s in states:
                    temp_list.append(s)

            current_nodes = []

            for tl in temp_list:
                current_nodes.append(tl)

        for cn in current_nodes:
            if cn.accepted:
                return True

        return False

    def nfa_to_dfa(self, nfa_automata):
        new_states = [nfa_automata.get_initial_node()]
        new_transitions = []

        alphabet = nfa_automata.get_alphabet()

        for ns in new_states:
            for s in alphabet:
                next_states = []
                states = AutomataActions().get_next_states(ns, s, nfa_automata.transitionList)

                if len(states) == 0:
                    continue

                for nsa in states:
                    if nsa not in next_states:
                        next_states.append(nsa)

                state = AutomataActions().join_states(next_states)

                if not self.state_exists_in_automata(state.stateName, new_states):
                    new_states.append(state)

                if not self.check_dfa_transition_in_automata(ns, s, new_transitions):
                    new_transitions.append(Transition(ns, state, s))

        return AutomataActions().transformation_save_automata(new_states, new_transitions)

    def evaluate_nfa_e(self, test_string, automata):

        current_nodes = [automata.get_initial_node()]

        for c in test_string:
            temp_list = []
            for cn in current_nodes:
                closure_states = automata.state_closure(cn)

                for cs in closure_states:
                    states = AutomataActions().get_next_states(cs, c, automata.transitionList)
                    for s in states:
                        temp_list.append(s)

                    current_nodes = []

                    for tl in temp_list:
                        cf = automata.state_closure(tl)
                        for s in cf:
                            current_nodes.append(s)

        for cn in current_nodes:
            if cn.accepted:
                return True

        return False

    def state_exists_in_automata(self, state_name, state_list):
        for state in state_list:
            if state.stateName == state_name:
                return True
        return False

    def check_dfa_transition_in_automata(self, state, transition_char, transition_list):
        for transition in transition_list:
            if transition.originState.stateName == state.stateName and transition.transitionChar == transition_char:
                return True
        return False

    def nfae_to_dfa(self, nfae_automata):

        e_closure_states = []

        for state in nfae_automata.stateList:
            states = AutomataActions().state_e_closure(state, nfae_automata.transitionList)

            n_states = AutomataActions().join_states(states)

            e_closure_states.append(n_states)

        alphabet = nfae_automata.get_alphabet()
        alphabet.remove('e')

        new_states = [AutomataActions().get_initial_node(e_closure_states)]
        new_transitions = []

        for ns in new_states:
            for s in alphabet:
                next_states = []
                r_states = AutomataActions().get_next_states(ns, s, nfae_automata.transitionList)

                if len(r_states) == 0:
                    continue

                for rs in r_states:
                    if rs not in next_states:
                        next_states.append(rs)

                for rs2 in r_states:
                    c_states = AutomataActions().state_e_closure(rs2, nfae_automata.transitionList)
                    for cs in c_states:
                        if cs not in next_states:
                            next_states.append(cs)

                combined_states = AutomataActions().join_states(next_states)

                if not self.state_exists_in_automata(combined_states.stateName, new_states):
                    new_states.append(combined_states)

                if not self.check_dfa_transition_in_automata(ns, s, new_transitions):
                    new_transitions.append(Transition(ns, combined_states, s))

        return AutomataActions().transformation_save_automata(new_states, new_transitions)
