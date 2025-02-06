import polars as pl


def test_data_integrity():
    """Test that data values remain correct after permutations"""
    df = pl.DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [10, 11, 12]},
    )

    result = df.permute.shift("a", "b", steps=1, direction="right")

    # Check all values in all columns remain the same
    assert result.get_column("a").to_list() == [
        1,
        2,
        3,
    ], "column a data integrity failed"
    assert result.get_column("b").to_list() == [
        4,
        5,
        6,
    ], "column b data integrity failed"
    assert result.get_column("c").to_list() == [
        7,
        8,
        9,
    ], "column c data integrity failed"
    assert result.get_column("d").to_list() == [
        10,
        11,
        12,
    ], "column d data integrity failed"

    # Check order of columns
    assert result.columns == ["c", "a", "b", "d"], "final column order incorrect"
