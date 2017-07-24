from State import State
from Transition import Transition
from Automata import Automata
from EvaluateAutomata import EvaluateAutomata

class DrawAutomata:

    def accepString(self, test_string, automata):

        result = False

        if automata.automataType == "dfa":
            result = EvaluateAutomata.evaluate_dfa(test_string, automata)


