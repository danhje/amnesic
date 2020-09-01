"""
Memoization for Python, with optional TTL (measured in time or function call count  ) for the cached results.
"""


from inspect import signature


cached = {'a': 1}


def cache(func):
    def memoized_func(*args, **kwargs):
        print(func.__name__)
        invocation_string = func.__name__ + '~' + '~'.join((str(arg) for arg in args)) + '~' + '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
        print(invocation_string)
        invocation_hash = hash(invocation_string)
        if invocation_hash in cached:
            return cached[invocation_hash]
        function_result = func(*args, **kwargs)
        cached[invocation_hash] = function_result
        return function_result

    return memoized_func
