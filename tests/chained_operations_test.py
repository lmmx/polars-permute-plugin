import polars as pl


def test_chained_operations():
    """Test chaining multiple permutation operations"""
    df = pl.DataFrame({"a": 1, "b": 2, "c": 3, "d": 4})

    result = (
        df.permute.prepend("d")
        .permute.shift("b", steps=1, direction="left")
        .permute.append("a")
    )

    assert result.columns == [
        "d",
        "b",
        "c",
        "a",
    ], "chained operations column order incorrect"
    assert result.select(["d", "a"]).to_dicts() == [
        {
            "d": 4,
            "a": 1,
        },
    ], "chained operations data integrity failed"
