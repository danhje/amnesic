"""
Memoization for Python, with optional TTL (measured in time or function call count) for the cached results.
"""


from sys import modules


this = modules[__name__]
this.cache = {}


def memoize(func=None, ttl_minutes=None, ttl_call_count=None):
    if func is not None:
        def memoized_func(*args, **kwargs):
            invocation_string = func.__name__ + '~' + '~'.join((str(arg) for arg in args)) + '~' + '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
            invocation_hash = hash(invocation_string)
            if invocation_hash in this.cache:
                return this.cache[invocation_hash]
            function_result = func(*args, **kwargs)
            this.cache[invocation_hash] = function_result
            return function_result
        return memoized_func
    else:
        def decorator(func):
            def memoized_func(*args, **kwargs):
                invocation_string = func.__name__ + '~' + '~'.join((str(arg) for arg in args)) + '~' + '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
                invocation_hash = hash(invocation_string)
                if invocation_hash in this.cache:
                    return this.cache[invocation_hash]
                function_result = func(*args, **kwargs)
                this.cache[invocation_hash] = function_result
                return function_result
            return memoized_func
        return decorator
