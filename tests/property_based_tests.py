import hypothesis.strategies as st
from hypothesis import given

from pymesis import _cache as pymesis_cache

strategies = (
    st.integers(),
    st.text(),
    st.binary(),
    st.booleans(),
    st.characters(),
    st.complex_numbers(allow_nan=False),
    st.dates(),
    st.datetimes(),
    st.decimals(allow_nan=False),
    st.dictionaries(st.text(), st.text()),
    st.floats(allow_nan=False),
    st.fractions(),
    st.functions(),
    st.iterables(st.text()),
    st.none(),
)


@given(st.one_of(strategies))
def test_cache(data):
    pymesis_cache.clear_cache()

    pymesis_cache.add_data(hash("key"), data)
    retrieved_data = pymesis_cache.get_data_if_cached(hash("key"))

    assert retrieved_data == data
