class StateMachine(object):
    def __init__(self):
        self.state_funcs = {}
        self.transitions = {}
        self._starting_state = None

    def add_transition(self, state, input, next_state):
        trans = self.transitions.setdefault(state, {})
        trans[input] = next_state

    def iter_transitions(self):
        for state, transitions in self.transitions.iteritems():
            for input, next_state in transitions.iteritems():
                yield state, input, next_state

    def iter_names(self):
        states = set()
        states.update(self.state_funcs.keys())
        states.update(self.transitions.keys())
        if self._starting_state is not None:
            states.add(self._starting_state)
        return iter(states)

    def state(self, trans={}, name=None, start=False):
        def decorator(f):
            state_name = name if name is not None else f.__name__
            self.state_funcs[state_name] = f

            for input, next_state in trans.iteritems():
                self.add_transition(state_name, input, next_state)

            if start:
                self.set_start(state_name)

            f._state_name = state_name
            return f
        return decorator

    def set_start(self, name):
        self._starting_state = name

    def run(self, start_state=None, trace=None):
        state = start_state or self._starting_state

        if not state:
            raise ValueError('No starting state set.')

        # FIXME: allow for exit states
        while True:
            state_func = self.state_funcs[state]

            if trace:
                trace('enter {}'.format(state))

            output = state_func()

            if trace:
                trace('exit {}: {}'.format(state, output))

            # look up transition
            state = self.transitions[state][output]
