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


sm = StateMachine()


@sm.state({'button_press': 'menu'}, start=True)
def intro():
    print 'showing intro'

    raw_input('waiting for button press')
    return 'button_press'


@sm.state(trans={
    'select_move': 'movie',
    'select_extras': 'extras',
    'timeout': 'intro',
})
def menu():
    print 'your menu: '
    print '* view movie'
    print '* view extras'

    val = raw_input('select movie or extras')

    if val == 'movie':
        return 'select_movie'
    elif val == 'extras':
        return 'select_extras'

    return 'timeout'


@sm.state({'movie_finished': 'menu'})
def movie():
    print 'showing movie'
    import time
    for i in range(4):
        time.sleep(500)
        print '.'

    return 'movie_finished'


@sm.state({'extras_finished': 'menu'})
def extras():
    print 'showing extras'
    import time
    for i in range(8):
        time.sleep(100)
        print '.',

    return 'extras_finished'


import pygraphviz as pgv


def render_graphviz(sm):
    def add_node(g, name, *args, **kwargs):
        g.add_node(name, *args, **kwargs)
        return g.get_node(name)

    g = pgv.AGraph(strict=False, directed=True, rankdir='LR')

    # draw state-nodes
    for name in sm.iter_names():
        s_node = add_node(g, name)

        # missing state functions are red
        if name not in sm.state_funcs:
            s_node.attr['color'] = 'red'
            s_node.attr['fontcolor'] = 'red'

    # mark starting state, if any
    if sm._starting_state is not None:
        # create invisible node for starting state
        ivs_start = add_node(g, '__I0', style='invis', shape='none',
                             width=0, height=0, label='')
        g.add_edge(ivs_start, sm._starting_state, rank='same')

    # draw transitions
    for state, input, next_state in sm.iter_transitions():
        g.add_edge(state, next_state, label=input, fontsize=8)

    return g


render_graphviz(sm).write('output.dot')
