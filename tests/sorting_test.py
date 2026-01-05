import polars as pl
from pytest import importorskip, mark

import polars_permute  # noqa: F401


@mark.parametrize(
    ("input_cols", "descending", "expected"),
    [
        (["c", "a", "b"], False, ["a", "b", "c"]),
        (["c", "a", "b"], True, ["c", "b", "a"]),
        (["a"], False, ["a"]),
        ([], False, []),
    ],
)
def test_sort(input_cols, descending, expected):
    df = pl.DataFrame({c: [i] for i, c in enumerate(input_cols)})
    result = df.permute.sort(descending=descending)
    assert result.columns == expected


@mark.parametrize(
    ("input_cols", "descending", "expected"),
    [
        (["col10", "col2", "col1"], False, ["col1", "col2", "col10"]),
        (["col10", "col2", "col1"], True, ["col10", "col2", "col1"]),
        (["x1", "x10", "x2", "x20"], False, ["x1", "x2", "x10", "x20"]),
        (["a"], False, ["a"]),
        ([], False, []),
    ],
)
def test_natsort(input_cols, descending, expected):
    importorskip("natsort")
    df = pl.DataFrame({c: [i] for i, c in enumerate(input_cols)})
    result = df.permute.natsort(descending=descending)
    assert result.columns == expected
