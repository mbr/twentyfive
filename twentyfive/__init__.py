class StateMachine(object):
    def __init__(self):
        self.state_funcs = {}
        self.transitions = {}
        self.final_states = set(['error'])
        self.start_state = None

        self.state_funcs['error'] = lambda: None

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
        if self.start_state is not None:
            states.add(self.start_state)
        return iter(states)

    def state(self, trans={}, name=None, start=False, final=False):
        def decorator(f):
            state_name = name if name is not None else f.__name__
            self.state_funcs[state_name] = f

            for input, next_state in trans.iteritems():
                self.add_transition(state_name, input, next_state)

            if start:
                self.start_state = state_name

            self.final_states.discard(state_name)
            if final:
                self.final_states.add(state_name)

            f._state_name = state_name
            return f
        return decorator

    def create_runner(self, start_state=None):
        # S: load start state
        state = start_state or self.start_state
        if state is None or not state in self.state_funcs:  # T: not found
            state = 'error'

        while True:
            # S: execute current state
            try:
                # state is guaranteed to exist
                input = self.state_funcs[state]()
                yield state, input
            except BaseException:  # T: except
                input = 'err:unhandled_exception'

            # S: validate input
            if input is None:
                if state in self.final_states:
                    break  # T: halt
                input = 'err:invalid_final_state'

            # S: transition
            while True:
                state = self.transitions.get(state, {}).get(input, None)

                if state is None:  # T: missing delta
                    state = 'error'
                    break

                if not state in self.state_funcs:
                    input = 'err:missing_state_function'
                    continue

                break  # T: state and state func found

            # outer while repeats

    def run(self, start_state=None):
        for state, input in self.create_runner(start_state):
            print 'TRACE -- transitioned from state', state, 'with', input
