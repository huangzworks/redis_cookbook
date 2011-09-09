# file: ./h/cache/example.py

from functools import wraps
from string_implement import set, get

def make_unique_id(function, args, kwargs):
    return function.__name__ + repr(args) + repr(kwargs)

def cache(function):
    @wraps(function)
    def _(*args, **kwargs):
        id = make_unique_id(function, *args, **kwargs)
        cache = get(id)

        if cache:
            return cache
        else:
            result = function(*args, **kwargs)
            set(result)
            return result
    return _
