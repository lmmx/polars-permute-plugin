import polars as pl


def test_multiple_columns():
    """Test operations with multiple columns at once"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})

    # Test prepending multiple columns
    result = df.permute.prepend(["c", "d"])
    assert result.columns == [
        "c",
        "d",
        "a",
        "b",
    ], "multiple prepend column order incorrect"
    assert result.select(["c", "d"]).to_dicts() == [
        {
            "c": 3,
            "d": 4,
        },
    ], "multiple prepend data integrity failed"

    # Test appending multiple columns
    result = df.permute.append(["a", "b"])
    assert result.columns == [
        "c",
        "d",
        "a",
        "b",
    ], "multiple append column order incorrect"
    assert result.select(["a", "b"]).to_dicts() == [
        {
            "a": 1,
            "b": 2,
        },
    ], "multiple append data integrity failed"
