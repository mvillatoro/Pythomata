from Automata import Automata
from EvaluateAutomata import EvaluateAutomata

class main:
    def __init__(self):
#        au = Automata("dfa")
        au = Automata("nfa")

#        au.generate_automata("a,I|b,N|c,F|d,N|e,N|f,N|g,N|h,N*a,0,b|a,1,f|b,1,c|b,0,g|c,1,c|c,0,a|d,0,c|d,1,g|e,1,f|e,0,h|f,1,g|f,0,c|g,0,g|g,1,e|h,0,g|h,1,c")  #000000000010111111
        au.generate_automata("a,I|b,F*a,0,a|a,1,a|a,1,b")


        if EvaluateAutomata().evaluate_nfa("1", au):
            print("Acepta")
        else:
            print("NO acepta")

mn = main()
