from pymesis import Cache, memoize


def test_pytest():
    assert True


def test_cache():
    cache = Cache()

    original_data = 'data'
    cache.add_data(hash('key'), original_data)
    retrieved_data = cache.get_data_if_cached(hash('key'))
    assert retrieved_data == original_data

