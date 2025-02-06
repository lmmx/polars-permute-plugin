import polars as pl


def test_shift_operations():
    """Test shift operations in both directions"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})

    # Test left shift
    result = df.permute.shift("c", steps=1, direction="left")
    assert result.columns == ["a", "c", "b", "d"], "left shift column order incorrect"
    assert result.select("c").item() == 3, "left shift data integrity failed"

    # Test right shift
    result = df.permute.shift("b", steps=1, direction="right")
    assert result.columns == ["a", "c", "b", "d"], "right shift column order incorrect"
    assert result.select("b").item() == 2, "right shift data integrity failed"

    # Test multiple column shift
    result = df.permute.shift("a", "b", steps=1, direction="right")
    assert result.columns == [
        "c",
        "a",
        "b",
        "d",
    ], "multiple shift column order incorrect"
    assert result.select(["a", "b"]).to_dicts() == [
        {
            "a": 1,
            "b": 2,
        },
    ], "multiple shift data integrity failed"
