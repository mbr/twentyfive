from functools import wraps


def coroutine(f):
    @wraps(f)
    def _(*args, **kwargs):
        co = f(*args, **kwargs)
        co.next()
        return co
    return _
