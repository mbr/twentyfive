from twentyfive import StateMachine
from twentyfive.render import render_graphviz


def debug(msg):
    print 'TRACE: {}'.format(msg)


sm = StateMachine()


@sm.state({'button_press': 'menu'}, start=True)
def intro():
    print 'showing intro'

    raw_input('waiting for button press')
    return 'button_press'


@sm.state(trans={
    'select_movie': 'movie',
    'select_extras': 'extras',
    'timeout': 'intro',
})
def menu():
    print 'your menu: '
    print '* view movie'
    print '* view extras'

    val = raw_input('select movie or extras: ')

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
        print '.',
    print

    return 'movie_finished'


@sm.state({'extras_finished': 'menu'})
def extras():
    print 'showing extras'
    import time
    for i in range(8):
        time.sleep(0.1)
        print '.',
    print

    return 'extras_finished'


render_graphviz(sm).write('output.dot')

sm.run(trace=debug)
