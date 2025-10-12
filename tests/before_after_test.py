import polars as pl
from pytest import mark


@mark.parametrize(
    ("method", "cols", "ref", "expected"),
    [
        ("after", "a", "c", [*"bcad"]),
        ("after", ["a", "b"], "d", [*"cdab"]),
        ("before", "d", "b", [*"adbc"]),
        ("before", ["c", "d"], "a", [*"cdab"]),
        # Edge cases
        ("after", "a", "x", [*"abcd"]),  # non-existent reference
        ("before", "x", "b", [*"abcd"]),  # non-existent column to move
        ("after", [], "c", [*"abcd"]),  # empty column list
        ("after", "b", "b", [*"abcd"]),  # move column relative to itself
    ],
)
def test_before_after(method, cols, ref, expected):
    """Test moving columns before/after a reference column"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})
    result = getattr(df.permute, method)(cols, ref)
    assert result.columns == expected


@mark.skip("Expression support not yet implemented")
@mark.parametrize(
    ("method", "cols", "ref", "expected"),
    [
        ("after", pl.col("a"), "c", [*"bcad"]),
        ("before", pl.col("d"), "b", [*"adbc"]),
        ("after", [pl.col("a"), pl.col("b")], "d", [*"cdab"]),
        ("before", "d", pl.col("b"), [*"adbc"]),
    ],
)
def test_before_after_expressions(method, cols, ref, expected):
    """Test moving columns before/after using expressions (not yet supported)"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})
    result = getattr(df.permute, method)(cols, ref)
    assert result.columns == expected
