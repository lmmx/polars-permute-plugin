import polars as pl


def test_edge_cases():
    """Test edge cases and error conditions"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3]})

    # Test non-existent column
    result = df.permute.prepend("x")
    assert result.columns == ["a", "b", "c"], "non-existent column handling failed"

    # Test empty column list
    result = df.permute.prepend([])
    assert result.columns == ["a", "b", "c"], "empty column list handling failed"

    # Test out-of-bounds shift
    result = df.permute.shift("a", steps=100, direction="right")
    assert result.columns == ["b", "c", "a"], "out-of-bounds shift handling failed"
