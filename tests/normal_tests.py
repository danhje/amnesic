import datetime
import math
import time
from unittest.mock import Mock

import pytest

from pymesis import TTLUnit
from pymesis import _cache as pymesis_cache
from pymesis import memoize


def test_cache():
    pymesis_cache.clear_cache()

    original_data = "some data"
    pymesis_cache.add_data(hash("key"), original_data)
    retrieved_data = pymesis_cache.get_data_if_cached(hash("key"))
    assert retrieved_data == original_data


def test_memoization_decorator_basic(do_costly_stuff):
    @memoize
    def func(param):
        return do_costly_stuff()

    first = func("arg")
    second = func("arg")

    assert first == second
    assert do_costly_stuff.call_count == 1


def test_memoization_decorator_different_args(do_costly_stuff):
    @memoize
    def func(param):
        return do_costly_stuff()

    func("arg")
    func("different arg")

    assert do_costly_stuff.call_count == 2


def test_memoization_decorator_ttl_count_1(do_costly_stuff):
    @memoize(ttl=1, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return do_costly_stuff()

    first = func("arg")
    second = func("arg")
    third = func("arg")

    assert first == second == third
    assert do_costly_stuff.call_count == 2


def test_memoization_decorator_ttl_count_100(do_costly_stuff):
    @memoize(ttl=100, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return do_costly_stuff()

    results = [func("arg") for i in range(102)]

    assert all(("some data" == result for result in results))
    assert do_costly_stuff.call_count == 2


def test_memoization_decorator_ttl_count_0(do_costly_stuff):
    @memoize(ttl=0, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return do_costly_stuff()

    first = func("arg")
    second = func("arg")
    third = func("arg")

    assert first == second == third
    assert do_costly_stuff.call_count == 3


def test_memoization_decorator_ttl_count_negative(do_costly_stuff):
    @memoize(ttl=-1, ttl_unit=TTLUnit.CALL_COUNT)
    def func(param):
        return do_costly_stuff()

    first = func("arg")
    second = func("arg")
    third = func("arg")

    assert first == second == third
    assert do_costly_stuff.call_count == 3


def test_memoization_decorator_ttl_seconds_1(do_costly_stuff):

    time.time = Mock()

    @memoize(ttl=1, ttl_unit=TTLUnit.SECONDS)
    def func(param):
        return do_costly_stuff()

    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:00:00", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    first = func("arg")
    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:00:00", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    second = func("arg")
    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:00:02", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    third = func("arg")

    assert first == second == third
    assert do_costly_stuff.call_count == 2


def test_memoization_decorator_ttl_seconds_100(do_costly_stuff):

    time.time = Mock()

    @memoize(ttl=100, ttl_unit=TTLUnit.SECONDS)
    def func(param):
        return do_costly_stuff()

    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:00:00", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    first = func("arg")
    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:01:35", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    second = func("arg")
    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:01:41", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    third = func("arg")

    assert first == second == third
    assert do_costly_stuff.call_count == 2


def test_memoization_decorator_ttl_seconds_0(do_costly_stuff):

    time.time = Mock()

    @memoize(ttl=0, ttl_unit=TTLUnit.SECONDS)
    def func(param):
        return do_costly_stuff()

    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:00:00", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    first = func("arg")
    time.time.return_value = datetime.datetime.strptime(
        "2020-09-15 19:00:00", "%Y-%m-%d %H:%M:%S"
    ).timestamp()
    second = func("arg")

    assert first == second
    assert do_costly_stuff.call_count == 2


def test_memoization_decorator_on_method_same_instance(do_costly_stuff):
    class Circle:
        def __init__(self, radius):
            self._radius = radius

        @memoize
        def area(self):
            do_costly_stuff()
            return math.pi * self._radius ** 2

    circle = Circle(10)

    first_result = circle.area()
    second_result = circle.area()

    assert first_result == second_result
    assert do_costly_stuff.call_count == 1


def test_memoization_decorator_on_method_different_instance(do_costly_stuff):
    class Circle:
        def __init__(self, radius):
            self._radius = radius

        @memoize
        def area(self):
            do_costly_stuff()
            return math.pi * self._radius ** 2

    circle_1 = Circle(10)
    circle_2 = Circle(15)

    circle_1_area = circle_1.area()
    circle_2_area = circle_2.area()

    assert circle_1_area != circle_2_area
    assert do_costly_stuff.call_count == 2


def test_invalid_TTL_unit_raises_ValueError():
    @memoize(ttl=1, ttl_unit="minutes")
    def func(param):
        return "data"

    with pytest.raises(ValueError):
        func("arg")
        func("arg")
