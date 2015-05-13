from cgi import escape
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
        s_func = sm.state_funcs.get(name, None)
        if not s_func:
            s_node.attr['color'] = 'red'
            s_node.attr['fontcolor'] = 'red'
        elif name != s_func.__name__:
            s_node.attr['label'] = (
                '<{}<BR /><FONT POINT-SIZE="10">func: {}</FONT>>'.format(
                    escape(name), escape(s_func.__name__))
            )

    # mark starting state, if any
    if sm.start_state is not None:
        # create invisible node for starting state
        ivs_start = add_node(g, '__I0', style='invis', shape='none',
                             width=0, height=0, label='')
        g.add_edge(ivs_start, sm.start_state, rank='same')

    # draw transitions
    for state, input, next_state in sm.iter_transitions():
        g.add_edge(state, next_state, label=input, fontsize=8)

    return g
