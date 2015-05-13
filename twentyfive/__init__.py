from .util import coroutine


def _error():
    print 'RAN INTO ERROR'
    return 'unhandled_error'


class StateMachine(object):
    def __init__(self):
        self.state_funcs = {}
        self.transitions = {}
        self._starting_state = None

        self.state_funcs['_error'] = _error
        self.add_transition('_error', 'missing_transition', '_error')

    def _missing_state_transition():
        print 'missing state transition'
        return

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

    def create_runner(self, start_state=None):
        # S: load starting state
        state = start_state or self._starting_state

        # T: not found
        if not state:
            state = '_error'
            input = 'missing_start_function'
            skip_execution = True  # almost tempted to ask for a goto
        else:
            skip_execution = False  # T: found

        while True:
            if not skip_execution:
                # S: Execute/Yield
                try:
                    # retrieve state function
                    input = yield state, self.state_funcs[state]
                    yield
                except Exception as e:  # T: exc
                    # S: turn exc into transition
                    pass  # FIXME: Missing
                else:
                    if input is None:  # T: None
                        # S: check current state is valid end state
                        pass  # FIXME: Missing

                # T: state input
            else:
                skip_execution = False  # skip only once

            # S: transition
            while True:
                state = self.transitions.get(state, {}).get(input, None)

                if state is None:  # T: missing transition
                    input = 'missing_transition'
                    state = '_error'
                    continue

                if not state in self.state_funcs:
                    input = 'missing_state_function'
                    state = '_error'
                    continue

                break  # T: state and state func found

            # proceed to execution state at this point

    def run(self, start_state=None):
        machine = self.create_runner(start_state)

        for state, state_func in machine:
            print 'TRACE -- running state', state, 'with statefunc', state_func
            result = state_func()
            print 'TRACE -- result:', result
            machine.send(result)
