from pymesis import memoize, TTLUnit
from pymesis import _cache as pymesis_cache
from unittest.mock import Mock


def test_pytest():
    assert True


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
    get_data.assert_called_once


def test_memoization_decorator_ttl_count():
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
