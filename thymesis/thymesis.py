"""
Memoization for Python, with optional TTL (measured in time or function call count) for the cached results.
"""


from sys import modules
from enum import Enum


class TTLUnit(Enum):
    MINUTES = 'minutes'
    CALL_COUNT = 'call_count'


class Cache(dict):
    def addData(self, hash, data, ttl=None, ttl_unit=TTLUnit.MINUTES):
        dataobj = {'data': data}
        if ttl is not None and ttl_unit is not None:
            dataobj['ttl'] = ttl
            dataobj['ttl_unit'] = ttl_unit
        self[hash] = dataobj

    def getDataIfCached(self, hash):
        if hash not in self:
            return None
        dataobj = self[hash]
        data = dataobj['data']
        if 'ttl' not in dataobj or 'ttl_unit' not in dataobj:
            return data
        if dataobj['ttl_unit'] == TTLUnit.CALL_COUNT:   
            dataobj['ttl'] -= 1
            if dataobj['ttl'] <= 0:
                del self[hash]
            return data
        elif dataobj['ttl_unit'] == TTLUnit.MINUTES:
            return data
        else:
            raise ValueError(f'Unknown ttl_unit: {dataobj["ttl_unit"]}')


this = modules[__name__]
this._cache = Cache()


def memoize(func=None, ttl=None, ttl_unit=None):
    if func is not None:
        def memoized_func(*args, **kwargs):
            invocation_string = '~'.join((
                func.__name__,
                str(id(func)),
                '~'.join((str(arg) for arg in args)),
                '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
            ))
            invocation_hash = hash(invocation_string)
            if (data := this._cache.getDataIfCached(invocation_hash)) is not None:
                return data
            function_result = func(*args, **kwargs)
            this._cache.addData(invocation_hash, function_result, ttl, ttl_unit)
            return function_result
        return memoized_func
    else:
        def decorator(func):
            def memoized_func(*args, **kwargs):
                invocation_string = '~'.join((
                    func.__name__,
                    str(id(func)),
                    '~'.join((str(arg) for arg in args)),
                    '~'.join((f'{str(k)}:{str(v)}' for k, v in kwargs.items()))
                ))
                invocation_hash = hash(invocation_string)
                if (data := this._cache.getDataIfCached(invocation_hash)) is not None:
                    return data
                function_result = func(*args, **kwargs)
                this._cache.addData(invocation_hash, function_result, ttl, ttl_unit)
                return function_result
            return memoized_func
        return decorator


if __name__ == '__main__':
    from time import time, sleep

    @memoize
    def slowGreetingGenerator(fname, lname, *args, **kwargs):
        sleep(1)
        return f'Hello, {fname} {lname}'

    start = time()
    slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34)
    assert(time() - start >= 1)

    start = time()
    slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34)
    assert(time() - start < 1)

    @memoize(ttl=1, ttl_unit=TTLUnit.CALL_COUNT)
    def slowGreetingGenerator(fname, lname, *args, **kwargs):
        sleep(1)
        return f'Hello, {fname} {lname}'

    start = time()
    slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34)
    assert(time() - start >= 1)

    start = time()
    slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34)
    assert(time() - start < 1)

    start = time()
    slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34)
    assert(time() - start >= 1)
