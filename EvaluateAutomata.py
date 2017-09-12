import itertools

from AutomataActions import AutomataActions
from Transition import Transition
from PdaTransition import PdaTransition
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
        current_nodes = [automata.get_initial_nodes()]

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
                states = AutomataActions().get_next_dot_state(ns, s, nfa_automata.transitionList)

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

        return AutomataActions().transformation_save_automata(new_states, new_transitions, "NFA")

    def evaluate_nfa_e(self, test_string, automata):

        initial_nodes = automata.get_initial_nodes()
        current_nodes = []

        for ins in initial_nodes:
            current_nodes.append(ins)

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
                r_states = AutomataActions().get_next_dot_state(ns, s, nfae_automata.transitionList)

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

        return AutomataActions().transformation_save_automata(new_states, new_transitions, "NFA")

    def automata_operations(self, automata, operation):

        if operation == "r":
            print(self.reflexion_automtata(automata))

            return self.reflexion_automtata(automata)
        elif operation == "c":
            print("compliment")
        elif operation == "d":
            print("difference")

        return self.join_automata(automata, operation)

    def join_automata(self, automata, operation):
        alphabet = automata.get_alphabet()

        current_states = [AutomataActions().join_states_operation(automata.get_initial_nodes(), operation)]
        new_transitions = []

        for cn in current_states:
            for a in alphabet:
                states = AutomataActions().join_states_operation(AutomataActions().get_next_dot_state(cn, a, automata.transitionList), operation)

                if not self.state_exists_in_automata(states.stateName, current_states):
                    current_states.append(states)

                if not self.check_dfa_transition_in_automata(cn, a, new_transitions):
                    new_transitions.append(Transition(cn, states, a))

        return AutomataActions().transformation_save_automata(current_states, new_transitions, "NFA")

    def reflexion_automtata(self, automata):
        text_automata = automata.save_automata("none", "n")

        print(text_automata)

        i = 0
        for ta in text_automata:
            if ta == "I":
                text_automata = text_automata[:i] + "F" + text_automata[i + 1:]
            elif ta == "F":
                text_automata = text_automata[:i] + "I" + text_automata[i + 1:]
            i += 1

        a = text_automata.split("*")
        b = a[1].split("|")

        x = a[0] + "*"

        for c in b:
            d = c.split(",")
            e = d[0]
            f = d[2]

            val = f + "," + d[1] + "," + e

            x += val + "|"

        x = x[:-1]

        print(x)

        return x

    def evaluate_pda(self, test_string, automata):

        automata_stack = ["z"]

        init_states = automata.get_initial_nodes()

        result = self.pda_transition_function(init_states, test_string, automata_stack, automata)

        return False

    def pda_transition_function(self, states, test_string, automata_stack, automata):
        test_char = test_string[0]
        new_test_string = test_string[1:]

        if len(test_string) == 1:
            for state in states:
                r_stack = []
                stack_array = []
                for au in automata_stack:
                    r_stack.append(au)
                pop_char = r_stack.pop(len(automata_stack)-1)
                next_states = automata.get_next_pda_states(state, test_string, pop_char)
                for ns in next_states:
                    r_stack_2 = []
                    for au in r_stack:
                        r_stack_2.append(au)

                    for y in ns[1]:
                        if y != "e":
                            r_stack_2.append(y)
                    stack_array.append(r_stack_2)
                for sa in stack_array:
                    if len(sa) == 1 and sa[len(sa)-1] == "z":
                        return True
                return False
        else:
            for state in states:
                r_stack = []
                for au in automata_stack:
                    r_stack.append(au)
                pop_char = r_stack.pop(len(automata_stack)-1)

                next_states = automata.get_next_pda_states(state, test_char, pop_char)

                for ns in next_states:
                    r_stack_2 = []
                    for au in r_stack:
                        r_stack_2.append(au)

                    for y in ns[1]:
                        if y != "e":
                            r_stack_2.append(y)

                    lol = [ns[0]]
                    return self.pda_transition_function(lol, new_test_string, r_stack_2, automata)

    def pda_to_glc(self, automata):

        glc_string_builder = ""

        final_states = automata.get_final_nodes()
        initial_state = automata.get_initial_node()

        #Paso 1
        for fs in final_states:
            if len(glc_string_builder) == 0:
                glc_string_builder += "S > [" + initial_state.stateName + " z " + fs.stateName + "]" + "\n"
            else:
                glc_string_builder += "S > [" + initial_state.stateName + " z " + fs.stateName + "]" + "\n"
        #paso 2
        for transition in automata.transitionList:
            if transition.push_char == "e":
                glc_string_builder += "[ " + transition.originState.stateName + " " + transition.pop_char + " " +\
                                      transition.destinationState.stateName + "] > " + transition.transition_char + "\n"
        #Paso 3 tan tan taaaaaan...
        for transition in automata.transitionList:
            if transition.push_char != "e":
                push_string_array = []
                for tp in transition.push_char:
                    push_string_array.append(tp)
                super_tabla = self.create_super_tabla(automata.stateList, len(push_string_array))

                if len(push_string_array) == 1:
                    for st in super_tabla:
                        glc_string_builder += "[" + transition.originState.stateName + " " + transition.pop_char + " " + \
                                              st[len(st)-1] + "] > " + transition.transition_char + "[" + \
                                              transition.originState.stateName + " " + push_string_array[0] + \
                                              " " + st[0] + "]\n"
                else:
                    for st in super_tabla:
                        glc_string_builder += "[" + transition.originState.stateName + " " + transition.pop_char + " " + \
                                              st[len(st) - 1] + "] > " + transition.transition_char + "[" + \
                                              transition.originState.stateName + " " + push_string_array[0] + " " + \
                                              st[0] + "]" + self.satanic_function(st, push_string_array[1:])

        return glc_string_builder

    def satanic_function(self, super_row, push_list):
        string_builder = ""

        i = 0
        for pl in push_list:
            string_builder += "[" + super_row[i] + " " + pl + " " + super_row[i+1] + "]"
            i += 1

        string_builder += "\n"

        return string_builder

    def create_super_tabla(self, state_list, k_size):
        states_name_list = []
        for state in state_list:
            states_name_list.append(state.stateName)
        return itertools.product(states_name_list, repeat=k_size)

    def save_glc(self, save_name, text):
        f = open("C:\\Users\\mvill\\Desktop\\" + save_name + ".txt", "w+")
        f.write(text)

    def glc_to_pda(self, glc_data):
        productions = glc_data.split("\n")
        terminals = AutomataActions().get_terminals(glc_data)

        init_state = State("A", True, True)
        state_list = [init_state]
        transition_list = []

        transition_list.append(PdaTransition(init_state, init_state, "e", "e", "z"))

        for p in productions:
            if p:
                prod = p.split(">")
                transition_list.append(PdaTransition(init_state, init_state, "e", prod[0], prod[1]))

        for t in terminals:
            transition_list.append(PdaTransition(init_state, init_state, t, t, "e"))
        return AutomataActions().transformation_save_automata(state_list, transition_list, "PDA")

    def evaluate_turing(self, test_string, automata):
        return True
