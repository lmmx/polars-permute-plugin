import polars as pl


def test_move_after():
    """Test moving columns after a reference column"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})

    # Move single column after another
    result = df.permute.move("c", ["a"], where="after")
    assert result.columns == [*"bcad"], "move after column order incorrect"
    assert result.select("a").item() == 1, "move after data integrity failed"

    # Move multiple columns after a reference
    result = df.permute.move("d", ["a", "b"], where="after")
    assert result.columns == [*"cdab"], "move multiple after column order incorrect"
    assert result.select(["a", "b"]).to_dicts() == [
        {"a": 1, "b": 2}
    ], "move multiple after data integrity failed"


def test_move_before():
    """Test moving columns before a reference column"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3], "d": [4]})

    # Move single column before another
    result = df.permute.move("b", ["d"], where="before")
    assert result.columns == [*"adbc"], "move before column order incorrect"
    assert result.select("d").item() == 4, "move before data integrity failed"

    # Move multiple columns before a reference
    result = df.permute.move("a", ["c", "d"], where="before")
    assert result.columns == [*"cdab"], "move multiple before column order incorrect"
    assert result.select(["c", "d"]).to_dicts() == [
        {"c": 3, "d": 4}
    ], "move multiple before data integrity failed"


def test_move_data_integrity():
    """Test that data remains intact after move operations"""
    df = pl.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [10, 11, 12]}
    )

    result = df.permute.move("c", ["a", "b"], where="after")

    # Check all values in all columns remain the same
    assert result.get_column("a").to_list() == [1, 2, 3], "column a data integrity failed"
    assert result.get_column("b").to_list() == [4, 5, 6], "column b data integrity failed"
    assert result.get_column("c").to_list() == [7, 8, 9], "column c data integrity failed"
    assert result.get_column("d").to_list() == [
        10,
        11,
        12,
    ], "column d data integrity failed"

    # Check column order
    assert result.columns == [*"cabd"], "move column order incorrect"