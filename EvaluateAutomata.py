from AutomataActions import AutomataActions


class EvaluateAutomata:
    def evaluate_dfa(self, test_string, automata):
        current_node = automata.get_inital_node()
        for c in test_string:
            current_node = AutomataActions().get_next_state(current_node, c, automata.transitionList)
            if current_node is None:
                return False
        return current_node.accepted

