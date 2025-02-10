import polars as pl


def test_swap_operation():
    """Test column swap operation"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})

    result = df.permute.swap("a", "d")
    assert result.columns == ["d", "b", "c", "a"], "swap column order incorrect"
    assert result.select("a").item() == 1, "swap data integrity failed for first column"
    assert result.select("d").item() == 4, (
        "swap data integrity failed for second column"
    )
