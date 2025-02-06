import polars as pl


def test_basic_permutations():
    """Test basic column permutation operations"""
    df = pl.DataFrame({"a": 1, "b": 2, "c": 3, "d": 4})
    original_columns = df.columns

    # Test prepend
    result = df.permute.prepend("d")
    assert result.columns == ["d", "a", "b", "c"], "prepend column order incorrect"
    assert result.select("d").item() == 4, "prepend data integrity failed"

    # Test append
    result = df.permute.append("a")
    assert result.columns == ["b", "c", "d", "a"], "append column order incorrect"
    assert result.select("a").item() == 1, "append data integrity failed"

    # Test at specific index
    result = df.permute.at("d", 1)
    assert result.columns == ["a", "d", "b", "c"], "at() column order incorrect"
    assert result.select("d").item() == 4, "at() data integrity failed"

    # Test original df wasn't modified
    assert df.columns == original_columns, "original DataFrame was modified"
