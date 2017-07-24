from AutomataActions import AutomataActions
from DrawAutomata import DrawAutomata
from Automata import Automata
from EvaluateAutomata import EvaluateAutomata

class main:
    def __init__(self):
        au = Automata("dfa")

#        au.generate_automata("1,I|2,F*1,a,1|1,b,2|2,b,1|2,a,2")
        au.generate_automata("a,I|b,N|c,F|d,N|e,N|f,N|g,N|h,N*a,0,b|a,1,f|b,1,c|b,0,g|c,1,c|c,0,a|d,0,c|d,1,g|e,1,f|e,0,h|f,1,g|f,0,c|g,0,g|g,1,e|h,0,g|h,1,c")
        au.list_states()
        au.list_transitions()

        if EvaluateAutomata().evaluate_dfa("00000000001011", au):
            print("Acepta")
        else:
            print("NO acepta")

mn = main()
