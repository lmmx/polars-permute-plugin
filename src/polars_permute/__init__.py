from __future__ import annotations

from typing import Literal

import polars as pl
from polars.api import register_dataframe_namespace


@register_dataframe_namespace("permute")
class PermutePlugin:
    def __init__(self, df: pl.DataFrame):
        self._df = df

    @property
    def columns(self) -> list[str]:
        return self._df.columns

    def _normalize_columns(
        self,
        cols: str | list[str] | pl.Expr | list[pl.Expr],
    ) -> list[str]:
        """Helper to convert various column specifications to a list of column names."""
        if isinstance(cols, (str, pl.Expr)):
            cols = [cols]

        move_col_names: list[str] = []
        for col in cols:
            if isinstance(col, str):
                move_col_names.append(col)
            elif isinstance(col, pl.Expr):
                name = col.meta.output_name  # type: ignore[attr-defined]
                if name is not None:
                    move_col_names.append(name)
                else:
                    raise ValueError(
                        f"Cannot extract a column name from the expression: {col}",
                    )

        return move_col_names

    def prepend(
        self,
        cols: str | list[str] | pl.Expr | list[pl.Expr],
    ) -> pl.DataFrame:
        """Move the specified column(s) to the start (index 0)."""
        all_cols = list(self.columns)
        move_cols = self._normalize_columns(cols)

        # Gather columns in their original order
        block = []
        for c in move_cols:
            if c in set(all_cols):  # Using set for membership test
                idx = all_cols.index(c)
                block.append(all_cols.pop(idx))

        # Put them at the front maintaining relative order
        all_cols = block + all_cols
        return self._df.select(all_cols)

    def append(
        self,
        cols: str | list[str] | pl.Expr | list[pl.Expr],
    ) -> pl.DataFrame:
        """Move the specified column(s) to the end."""
        all_cols = list(self.columns)
        move_cols = self._normalize_columns(cols)

        # Gather columns in their original order
        block = []
        for c in move_cols:
            if c in set(all_cols):  # Using set for membership test
                idx = all_cols.index(c)
                block.append(all_cols.pop(idx))

        # Put them at the end maintaining relative order
        all_cols = all_cols + block
        return self._df.select(all_cols)

    def at(
        self,
        cols: str | list[str] | pl.Expr | list[pl.Expr],
        index: int,
    ) -> pl.DataFrame:
        """Move the specified column(s) to the exact position 'index'."""
        all_cols = list(self.columns)
        move_cols = self._normalize_columns(cols)

        # Gather columns in their original order
        block = []
        for c in move_cols:
            if c in set(all_cols):  # Using set for membership test
                idx = all_cols.index(c)
                block.append(all_cols.pop(idx))

        # Clamp index to valid range [0, len(all_cols)]
        index = max(0, min(index, len(all_cols)))

        # Insert maintaining relative order
        for i, c in enumerate(block):
            all_cols.insert(index + i, c)

        return self._df.select(all_cols)

    def shift(
        self,
        *col_names: str | pl.Expr,
        steps: int = 1,
        direction: Literal["left", "right"] = "left",
    ) -> pl.DataFrame:
        """Shift the specified column(s) left or right by `steps` positions."""
        move_col_names = self._normalize_columns(list(col_names))
        all_cols_set = set(self.columns)

        if not move_col_names:
            return self._df

        all_cols = list(self.columns)
        # Gather original indexes
        original_indexes = []
        for c in move_col_names:
            if c in all_cols_set:  # Using set for membership test
                original_indexes.append(all_cols.index(c))

        if not original_indexes:
            return self._df

        # Sort so we handle them in ascending index order
        original_indexes.sort()

        # Extract them as a contiguous block in their original order
        block = []
        for idx in reversed(original_indexes):
            block.insert(0, all_cols.pop(idx))

        # Calculate new position
        sign = -1 if direction == "left" else 1
        leftmost_idx = original_indexes[0]
        new_leftmost = leftmost_idx + steps * sign
        # Clamp to valid range
        new_leftmost = max(0, min(new_leftmost, len(all_cols)))

        # Insert them back in
        for i, col_name in enumerate(block):
            all_cols.insert(new_leftmost + i, col_name)

        return self._df.select(all_cols)

    def swap(
        self,
        col1: str | pl.Expr,
        col2: str | pl.Expr,
    ) -> pl.DataFrame:
        """Swap exactly two columns in place."""
        col1_name = self._normalize_columns(col1)[0]
        col2_name = self._normalize_columns(col2)[0]

        all_cols = list(self.columns)
        all_cols_set = set(all_cols)

        if (
            col1_name in all_cols_set and col2_name in all_cols_set
        ):  # Using set for membership test
            i1, i2 = all_cols.index(col1_name), all_cols.index(col2_name)
            all_cols[i1], all_cols[i2] = all_cols[i2], all_cols[i1]
        return self._df.select(all_cols)

    def before(
        self,
        cols: str | list[str],  # | pl.Expr | list[pl.Expr],  # TODO: Expression support
        reference: str,  # | pl.Expr,  # TODO: Expression support
    ) -> pl.DataFrame:
        """Move specified column(s) before a reference column."""
        all_cols = list(self.columns)
        move_cols = self._normalize_columns(cols)
        ref_col = self._normalize_columns(reference)[0]

        all_cols_set = set(all_cols)

        # Validate reference column exists
        if ref_col not in all_cols_set:
            return self._df

        # Gather columns to move in their original order
        block = []
        for c in move_cols:
            if c in all_cols_set and c != ref_col:
                idx = all_cols.index(c)
                block.append(all_cols.pop(idx))

        if not block:
            return self._df

        # Find reference position and insert before it
        ref_idx = all_cols.index(ref_col)
        for i, col_name in enumerate(block):
            all_cols.insert(ref_idx + i, col_name)

        return self._df.select(all_cols)

    def after(
        self,
        cols: str | list[str],  # | pl.Expr | list[pl.Expr],  # TODO: Expression support
        reference: str,  # | pl.Expr,  # TODO: Expression support
    ) -> pl.DataFrame:
        """Move specified column(s) after a reference column."""
        all_cols = list(self.columns)
        move_cols = self._normalize_columns(cols)
        ref_col = self._normalize_columns(reference)[0]

        all_cols_set = set(all_cols)

        # Validate reference column exists
        if ref_col not in all_cols_set:
            return self._df

        # Gather columns to move in their original order
        block = []
        for c in move_cols:
            if c in all_cols_set and c != ref_col:
                idx = all_cols.index(c)
                block.append(all_cols.pop(idx))

        if not block:
            return self._df

        # Find reference position and insert after it
        ref_idx = all_cols.index(ref_col)
        for i, col_name in enumerate(block):
            all_cols.insert(ref_idx + 1 + i, col_name)

        return self._df.select(all_cols)
