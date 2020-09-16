import pytest
from unittest.mock import Mock
from pymesis import _cache as pymesis_cache


@pytest.fixture
def do_costly_stuff():
    pymesis_cache.clear_cache()
    fetch_some_data = Mock()
    fetch_some_data.return_value = 'some data'
    return fetch_some_data
