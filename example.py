from twentyfive import StateMachine


sm = StateMachine()


@sm.state({'button_press': 'menu'}, start=True)
def intro():
    print 'showing intro'

    raw_input('waiting for button press')
    return 'button_press'


@sm.state(final=True, trans={
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
    elif val == 'e':
        return 'non_existant_state'
    elif val == 'q':
        return None

    return 'timeout'


@sm.state({'movie_finished': 'menu'})
def movie():
    print 'showing movie'
    import time
    for i in range(4):
        time.sleep(0.05)
        print '.'
    print

    return 'movie_finished'


@sm.state({'extras_finished': 'menu'})
def extras():
    print 'showing extras'
    import time
    for i in range(8):
        time.sleep(0.1)
        print '.'
    print

    return 'extras_finished'


@sm.state({'restart': 'intro'})
def error():
    print 'reached error state'
    return 'restart'


if __name__ == '__main__':
    history = sm.run_trace()

    print ' -> '.join('{} [{}]'.format(node, edge) for node, edge in history), '.'
