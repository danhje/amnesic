from pymesis import memoize, TTLUnit
from pymesis import _cache as pymesis_cache
from unittest.mock import Mock


def test_cache():
    pymesis_cache.clear_cache()

    original_data = 'data'
    pymesis_cache.add_data(hash('key'), original_data)
    retrieved_data = pymesis_cache.get_data_if_cached(hash('key'))
    assert retrieved_data == original_data


def test_memoization_decorator_basic():
    pymesis_cache.clear_cache()

    get_data = Mock()
    get_data.return_value = 'data'

    @memoize
    def func(param):
        return get_data()

    first = func('arg')
    second = func('arg')

    assert first == second
    get_data.call_count == 1


def test_memoization_decorator_ttl_count_1():
    pymesis_cache.clear_cache()

    get_data = Mock()
    get_data.return_value = 'data'

    @memoize(ttl=1, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return get_data()

    first = func('arg')
    second = func('arg')
    third = func('arg')

    assert first == second == third
    assert get_data.call_count == 2


def test_memoization_decorator_ttl_count_100():
    pymesis_cache.clear_cache()

    get_data = Mock()
    get_data.return_value = 'data'

    @memoize(ttl=100, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return get_data()

    results = [func('arg') for i in range(102)]

    assert all(('data' == result for result in results))
    assert get_data.call_count == 2


def test_memoization_decorator_ttl_count_0():
    pymesis_cache.clear_cache()

    get_data = Mock()
    get_data.return_value = 'data'

    @memoize(ttl=0, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return get_data()

    first = func('arg')
    second = func('arg')
    third = func('arg')

    assert first == second == third
    assert get_data.call_count == 3
