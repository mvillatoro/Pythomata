from State import State
from Transition import Transition
from PdaTransition import PdaTransition


class Automata:
    def __init__(self, automata_type):
        self.transitionList = []
        self.stateList = []
        self.automataType = automata_type

    def get_state(self, state_name):
        for state in self.stateList:
            if state.stateName == state_name:
                return state
        return None

    def state_exists(self, state_name):
        for state in self.stateList:
            if state.stateName == state_name:
                return True
        return False

    def create_state(self, state_name, is_initial, is_accepted):
        if self.state_exists(state_name):
            return True
        else:
            new_state = State(state_name, is_initial, is_accepted)
            self.stateList.append(new_state)
            return False

    def create_transition(self, origin, destination, transition_char):
        origin_state = self.get_state(origin)
        destination_state = self.get_state(destination)

        if self.transition_exists(origin, destination, transition_char):
            print("Transition already exists.")
            return False
        else:
            if self.automataType == "nfa" or self.automataType == "nfae":
                new_transition = Transition(origin_state, destination_state, transition_char)
                self.transitionList.append(new_transition)
                return True
            elif self.automataType == "dfa":
                if self.check_dfa_transition(origin_state, transition_char):
                    return False
                else:
                    new_transition = Transition(origin_state, destination_state, transition_char)
                    self.transitionList.append(new_transition)
                    return True

    def create_pda_transition(self, origin, destination, transition_char, pop_char, push_char):
        origin_state = self.get_state(origin)
        destination_state = self.get_state(destination)

        if self.pda_transition_exists(origin, destination, transition_char, pop_char, push_char):
            print("Transition exists.")
            return False
        else:
            new_pda_transition = PdaTransition(origin_state, destination_state, transition_char, pop_char, push_char)
            self.transitionList.append(new_pda_transition)
            return True

    def pda_transition_exists(self, origin, destination, transition_char, pop, push):
        if not self.state_exists(origin) and self.state_exists(destination):
            return False

        for transition in self.transitionList:
            if transition.originState.stateName == origin and\
                            transition.destinationState.stateName == destination and\
                            transition.transition_char == transition_char and\
                            transition.pop_char == pop and\
                            transition.push_char == push:
                return True
        return False

    def check_dfa_transition(self, state, transition_char):
        for transition in self.transitionList:
            if transition.originState.stateName == state.stateName and transition.transitionChar == transition_char:
                return True
        return False

    def transition_exists(self, origin, destination, transition_char):

        if not self.state_exists(origin) and self.state_exists(destination):
            return False

        for transition in self.transitionList:
            if transition.originState.stateName == origin and transition.destinationState.stateName == destination and\
                            transition.transitionChar == transition_char:
                return True
        return False

    def list_states(self):
        for state in self.stateList:
            print(state.stateName)

    def list_transitions(self):
        for transition in self.transitionList:
            print(transition.originState.stateName + ", " + transition.destinationState.stateName
                  + ", " + transition.transitionChar)

    def get_initial_node(self):
        for state in self.stateList:
            if state.isInitial:
                return state

    def get_final_nodes(self):
        final_nodes = []
        for state in self.stateList:
            if state.accepted:
                final_nodes.append(state)
        return final_nodes

    def get_initial_nodes(self):
        initial_nodes = []
        for state in self.stateList:
            if state.isInitial:
                initial_nodes.append(state)
        return initial_nodes

    def generate_automata(self, automata_text):

        state_transition_division = automata_text.split("*")
        states_division = state_transition_division[0].split("|")
        transition_division = state_transition_division[1].split("|")

        for sd in states_division:
            states_components = sd.split(",")

            print(states_components[0])
            print(states_components[1])
            if states_components[1] == "N":
                self.create_state(states_components[0], False, False)
            if states_components[1] == "I":
                self.create_state(states_components[0], True, False)
            if states_components[1] == "F":
                self.create_state(states_components[0], False, True)
            if states_components[1] == "IF":
                self.create_state(states_components[0], True, True)

        for td in transition_division:
            transition_components = td.split(",")
            self.create_transition(transition_components[0],transition_components[2],transition_components[1])

    def delete_state(self, state_name):
        i = 0
        for state in self.stateList:
            if state.stateName == state_name:
                del self.stateList[i]
                self.delete_transitions_with_state_cascade(state_name)
            i += 1

    def delete_transitions_with_state_cascade(self, state_name):
        i = 0
        for transition in self.transitionList:
            if transition.originState.stateName == state_name or transition.destinationState.stateName == state_name:
                del self.transitionList[i]
                self.delete_transitions_with_state_cascade(state_name)
            i += 1

    def delete_transition(self, origin_name, transition_char, destiny_name):
        i = 0
        for transition in self.transitionList:
            if transition.originState.stateName == origin_name and transition.destinationState.stateName == destiny_name and\
                            transition.transitionChar == transition_char:
                del self.transitionList[i]

            i += 1

    def delete_pda_transition(self, origin_name, destiny_name, transition_char, pop_char, push_char):
        pass

    def get_alphabet(self):
        alphabet = []
        for transition in self.transitionList:
            if transition.transitionChar not in alphabet:
                alphabet.append(transition.transitionChar)

        return alphabet

    def get_transition_data(self, state, transition_char):
        transitions = []
        for transition in self.transitionList:
            if transition.originState.stateName == state.stateName and transition.transitionChar == transition_char:
                transitions.append(transition)

        return transitions

    def save_pda_automata(self,save_name,op):
        state_string = ""

        if len(self.stateList) == 0:
            return False

        for state in self.stateList:
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

        for transition in self.transitionList:
            string_builder = transition.originState.stateName + "," +\
                             transition.transition_char + "," +\
                             transition.pop_char + "," + \
                             transition.push_char + "," +\
                             transition.destinationState.stateName + "|"

            state_string = state_string + string_builder

        state_string = state_string[:-1]

        if op == "y":
            f = open("C:\\Users\\mvill\\Desktop\\" + save_name + ".ptm", "w+")
            f.write(state_string)
            return True
        else:
            return state_string

    def save_automata(self, save_name, op):
        state_string = ""

        if len(self.stateList) == 0:
            return False

        for state in self.stateList:
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

        for transition in self.transitionList:
            string_builder = transition.originState.stateName + "," + transition.transitionChar + "," + \
                             transition.destinationState.stateName + "|"

            state_string = state_string + string_builder

        state_string = state_string[:-1]

        if op == "y":
            f = open("C:\\Users\\mvill\\Desktop\\" + save_name + ".ptm", "w+")
            f.write(state_string)
            return True
        else:
            return state_string

    def load_automata(self, save_name):

        self.stateList = []

        self.transitionList = []

        text_automtata = ""
        f = open(save_name, "r")

        if f.mode == 'r':
            text_automtata = f.read()

        if not text_automtata:
            return False

        self.generate_automata(text_automtata)
        return True

    def state_closure(self, state):
        return_states = [state]

        for transition in self.transitionList:
            if transition.originState.stateName == state.stateName and transition.transitionChar == "e":
                if not self.check_if_exists_in_list(transition.destinationState, return_states):
                    return_states.append(transition.destinationState)

        for rt in return_states[1:]:
            new_rt = self.state_closure(rt)
            for nrt in new_rt:
                if not self.check_if_exists_in_list(nrt, return_states):
                    return_states.append(nrt)

        return return_states

    def check_if_exists_in_list(self, element, elem_list):
        for lst in elem_list:
            if element.stateName == lst.stateName:
                return True
        return False

    def minimize(self):
        minimize_table = self.minimize_table()

    def minimize_table(self):

        state_count = len(self.stateList)+1

        state_matrix = [["n" for x in range(state_count)] for y in range(state_count)]

        count = 0
        while count < len(self.stateList):
            state_matrix[0][count+1] = self.stateList[count]
            count += 1

        count_2 = 0
        while count_2 < len(self.stateList):
            state_matrix[count_2+1][0] = self.stateList[count_2]
            count_2 += 1

        count_3 = 0
        while count_3 < len(self.stateList):
            count_4 = 0
            while count_4 < len(self.stateList):
                if count_3 <= count_4:
                    state_matrix[count_3+1][count_4+1] = "E"
                count_4 += 1
            count_3 += 1

        state_matrix[0][0] = "p"

        count_5 = 0
        while count_5 < len(self.stateList)+1:
            count_6 = 0
            while count_6 < len(self.stateList)+1:

                if state_matrix[count_5][count_6] == "E":
                    pass
                elif isinstance(state_matrix[count_6][0], State) and isinstance(state_matrix[0][count_5], State):
                    if state_matrix[count_6][0].accepted and state_matrix[0][count_5].accepted:
                        pass
                    elif state_matrix[count_6][0].accepted or state_matrix[0][count_5].accepted:
                        state_matrix[count_5][count_6] = "X"
                    else:
                        print(state_matrix[count_6][0].stateName + ", " + state_matrix[0][count_5].stateName)

                        state_matrix[count_5][count_6] = "?"

                        result = self.compare_states(state_matrix[count_6][0], state_matrix[0][count_5], state_matrix,
                                                     count_5, count_6)

                count_6 += 1
            count_5 += 1

        self.print_matrix_state_matrix(state_matrix)

    def print_matrix_state_matrix(self, state_matrix):
        for x in state_matrix:
            string_data = ""
            for y in x:
                if isinstance(y, State):
                    string_data += y.stateName + ", "
                else:
                    string_data += y + ", "
            print(string_data)

    def compare_states(self, state_a, state_b, state_matrix, x, y):
        alphabet = self.get_alphabet()

        equivalent = []

        for a in alphabet:

            next_state_a = []
            next_state_b = []

            for transition in self.transitionList:
                if transition.originState.stateName == state_a.stateName and transition.transitionChar == a:

                    next_state_a.append(transition.destinationState)

            for transition_b in self.transitionList:
                if transition_b.originState.stateName == state_b.stateName and transition_b.transitionChar == a:
                    next_state_b.append(transition_b.destinationState)



            count = 0
            while count < len(next_state_a):

                if next_state_a[count].stateName == next_state_b[count].stateName:
                    state_matrix[x][y] = "O"
                else:
                    self.compare_states(next_state_a[count], next_state_b[count], state_matrix, )






                print(next_state_a[count].stateName + ", " + next_state_b[count].stateName + ", " + a)

                if next_state_a[count].stateName == next_state_b[count].stateName:
                    if state_matrix[x][y] == "?":
                        state_matrix[x][y] = "O"
                        equivalent.append(True)

                else:
                    if state_matrix[x][y] == "?":
                        state_matrix[x][y] = "O"
                    elif state_matrix[x][y] == "n":
                        state_matrix[x][y] = "?"
                        self.print_matrix_state_matrix(state_matrix)
                        equivalent.append(self.compare_states(next_state_a[count], next_state_b[count], state_matrix, x, y))
                    else:
                        state_matrix[x][y] = "X"

                count += 1

    def get_next_pda_states(self, state, transition_char, pop_char):
        next_state_list = []

        for transition in self.transitionList:
            if state.stateName == transition.originState.stateName and\
                    (transition_char == transition.transition_char or
                        transition_char == "e")and \
                    pop_char == transition.pop_char:

                input_char_reversed = transition.push_char[::-1]
                return_data = [transition.destinationState, input_char_reversed]
                next_state_list.append(return_data)

        return next_state_list

    def get_pda_transitions(self):
        string_builder = ""

        for transition in self.transitionList:
            string_builder += "δ(" + transition.originState.stateName + ", "
            string_builder += transition.transition_char + ", "
            string_builder += transition.pop_char + ") = ("
            string_builder += transition.destinationState.stateName + ", "
            string_builder += transition.push_char + ")\n"

        return string_builder
