from AutomataActions import AutomataActions


class EvaluateAutomata:

    def evaluate_dfa(self, test_string, automata):
        current_node = automata.get_inital_node()
        for c in test_string:
            current_node = AutomataActions().get_next_state(current_node, c, automata.transitionList)
            if current_node is None:
                return False
        return current_node.accepted

    def evaluate_nfa(self, test_string, automata):
        current_nodes = [automata.get_inital_node()]

        for c in test_string:
            temp_list = []
            for cn in current_nodes:
                states = AutomataActions().get_next_states(cn, c, automata.transitionList)
                temp_list.append(states)

            current_nodes = []

            for tl in temp_list:
                current_nodes.append(tl)

        for cn in current_nodes:
            if cn.accepted:
                return True

        return False

