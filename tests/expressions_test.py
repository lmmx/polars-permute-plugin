import polars as pl


def test_expressions():
    """Test handling of Polars expressions"""
    df = pl.DataFrame({"a": [1], "b": [2], "c": [3]})

    # Test with column expressions
    expr = pl.col("a").alias("x")
    result = df.permute.prepend(expr)
    assert result.columns == ["a", "b", "c"], "expression handling failed"
    assert result.select("a").item() == 1, "expression data integrity failed"
