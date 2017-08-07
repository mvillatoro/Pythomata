from AutomataActions import AutomataActions
from Automata import Automata
from State import State

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
        new_dfa_automata = Automata("dfa")
        states_list = []
        dfa_table = []
        alphabet = nfa_automata.get_alphabet()

        dfa_nodes = [nfa_automata.get_initial_node()]

        for dn in dfa_nodes:
            for symbol in alphabet:
                transition = nfa_automata.get_transition_data(dn, symbol)

                new_state_text = ""

                for tr in transition:
                    new_state_text = new_state_text + tr.destinationState.stateName + ","

                new_state_text = new_state_text[:-1]

                new_state = State(new_state_text, False, False)

                if new_state not in dfa_nodes:
                    print(new_state)
                    dfa_nodes.append(new_state)

                new_state_text = ""

        for dn2 in dfa_nodes:
            print(dn2.stateName)

        return False

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
