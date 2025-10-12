# Polars Permute Plugin

A Polars plugin for easily reordering DataFrame columns.

Supports column permutations like prepending, appending, shifting, and swapping.

## Installation

```python
pip install polars-permute[polars]
```

On older CPUs run:

```python
pip install polars-permute[polars-lts-cpu]
```

## Features

- Supports both string column names and Polars expressions
- Handles single or multiple columns
- Maintains relative ordering of moved columns
- Chain operations together
- Gracefully handles edge cases (non-existent columns, empty inputs)

## Usage

The plugin adds a `permute` namespace to Polars DataFrames with methods for column reordering:

```python
import polars as pl
import polars_permute

# Create a sample DataFrame
df = pl.DataFrame({
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9],
    "d": [10, 11, 12]
})

# Move column 'd' to the start
df.permute.prepend("d")

# Move multiple columns to the end
df.permute.append(["a", "b"])

# Move columns to a specific position
df.permute.at(["b", "c"], index=0)

# Shift columns left/right
df.permute.shift("a", "b", steps=1, direction="right")

# Swap two columns
df.permute.swap("a", "d")

# Move columns before or after another column
df.permute.before("d", "b")  # Move 'd' before 'b'
df.permute.after(["a", "b"], "c")  # Move 'a' and 'b' after 'c'
```

## API Reference

### prepend(cols)
Move specified column(s) to the start (index 0).
```python
df.permute.prepend("d")  # Single column
df.permute.prepend(["c", "d"])  # Multiple columns
df.permute.prepend(pl.col("a").alias("x"))  # Using expressions
```

### append(cols)
Move specified column(s) to the end.
```python
df.permute.append("a")
df.permute.append(["a", "b"])
```

### at(cols, index)
Move specified column(s) to exact position.
```python
df.permute.at("d", 1)  # Move 'd' to index 1
df.permute.at(["b", "c"], 0)  # Move multiple columns
```

### shift(cols, steps=1, direction="left")
Shift column(s) left or right by steps.
```python
df.permute.shift("c", steps=1, direction="left")
df.permute.shift("a", "b", steps=2, direction="right")
```

### swap(col1, col2)
Swap positions of two columns.
```python
df.permute.swap("a", "d")
```

### before(cols, reference)
Move specified column(s) before a reference column.
```python
df.permute.before("d", "b")  # Move 'd' before 'b'
df.permute.before(["c", "d"], "a")  # Move multiple columns before 'a'
```

### after(cols, reference)
Move specified column(s) after a reference column.
```python
df.permute.after("a", "c")  # Move 'a' after 'c'
df.permute.after(["a", "b"], "d")  # Move multiple columns after 'd'
```

## Notes

- Operations create a new DataFrame; the original is not modified
- Column order is preserved for multiple column operations
- Invalid columns are ignored gracefully
- Out-of-bounds indexes are clamped to valid range

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

MIT License
