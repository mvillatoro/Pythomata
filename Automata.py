from State import State
from Transition import Transition


class Automata:
    def __init__(self, automata_type):
        Automata.automataType = automata_type
        self.transitionList = []
        self.stateList = []
        self.automataType = ""

    def get_state(self, state_name):
        for state in self.stateList:
            if state.stateName == state_name:
                return state
        return None

    def state_exists(self, state_name):
        for state in self.stateList:
            if state.stateName == state_name:
                return True
            else:
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
        else:
            new_transition = Transition(origin_state, destination_state, transition_char)
            self.transitionList.append(new_transition)

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

    def get_inital_node(self):
        for state in self.stateList:
            if state.isInitial:
                return state

    def generate_automata(self, automata_text):

        state_transition_division = automata_text.split("*")
        states_division = state_transition_division[0].split("|")
        transition_division = state_transition_division[1].split("|")

        for sd in states_division:
            states_components = sd.split(",")
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
