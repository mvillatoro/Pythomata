class PdaTransition:

    def __init__(self, origin__state, destination_state, pop, push):
        self.originState = origin__state
        self.destinationState = destination_state
        self.pop = pop
        self.push = push
