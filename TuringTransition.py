class TuringTransition:
    def __init__(self, origin__state, destination_state, transition_char, push_char, mov_dir):
        self.originState = origin__state
        self.destinationState = destination_state
        self.transition_char = transition_char
        self.push_char = push_char
        self.mov_dir = mov_dir
