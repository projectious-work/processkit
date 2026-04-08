---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-pandas-polars
  name: pandas-polars
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "DataFrame operations with pandas and polars — groupby, joins, reshaping, performance."
  category: data
  layer: null
  when_to_use: "Use when manipulating tabular data, choosing between pandas and polars, optimizing DataFrame code, or translating between the two libraries."
---

# Pandas and Polars

## Level 1 — Intro

Pandas is the mature, broad-ecosystem default for exploratory work
under ~1 GB; polars is faster, leaner, and lazy-evaluated for
production pipelines and larger data. Both read the same formats —
when in doubt, match what the project already uses.

## Level 2 — Overview

### Choosing between them

- **Pandas** — mature ecosystem, broader library compatibility
  (sklearn, plotly), familiar API, best for EDA and < 1 GB datasets
- **Polars** — faster execution, lower memory, lazy evaluation,
  better for production pipelines and 1 GB+ datasets
- Polars has no index — use explicit columns instead
- If the project already uses one, prefer consistency over switching

### I/O

Prefer Parquet over CSV for performance and type preservation.
Specify `dtype` / `schema` on read to enforce types upfront. For
large CSVs, use chunked reads (pandas) or lazy scans (polars).
Always specify `parse_dates` or date columns explicitly —
auto-detection is unreliable. Use `usecols` / `columns` to read only
the columns you need.

### Selection and filtering

Select columns by name, not position. In polars, use expressions:
`df.select(pl.col("name"), pl.col("age"))`. In pandas, use `.loc[]`
for label-based and `.iloc[]` for position-based. Chain filters
with `&` and `|`, wrapping conditions in parentheses. Polars
`filter()` is preferred over boolean indexing for clarity.

### GroupBy and aggregation

Always name aggregated columns explicitly:

```python
# Polars
df.group_by("category").agg(pl.col("price").mean().alias("avg_price"))

# Pandas
df.groupby("category")["price"].mean().reset_index(name="avg_price")
```

Use multiple aggregations in one pass for efficiency. Polars
supports `over()` for window functions without groupby. Avoid
iterating over groups — use vectorized aggregations.

### Joins and merges

Specify join type explicitly: `inner`, `left`, `outer`, `cross`,
`anti`, `semi`. Use `on=` for same-named keys, `left_on=`/
`right_on=` otherwise. Check for duplicates before joining to avoid
row explosion. Polars anti-join is efficient for "rows not in
other table." Use `validate="m:1"` in pandas to catch unexpected
duplicates.

### Reshaping

Pivot to wide format for summary tables; melt to long for analysis
and plotting:

```python
# Polars
df.pivot(on="category", index="date", values="sales")

# Pandas
df.pivot_table(index="date", columns="category", values="sales", aggfunc="sum")
```

Use `stack()`/`unstack()` in pandas for multi-level index reshaping.

### Missing data, strings, datetimes

Check missing with `df.null_count()` (polars) or `df.isna().sum()`
(pandas). Fill with `fill_null` / `fillna`, or forward/backward
fill. Drop only when appropriate. Strip whitespace and lowercase
strings early. Parse dates on read with explicit format. Always be
explicit about timezones — naive datetimes cause subtle bugs.

### Performance

Use lazy evaluation in polars: `df.lazy().filter(...).select(...).
collect()`. Polars optimizes the query plan, pushing filters and
projections down. In pandas, avoid `apply()` with Python functions —
use vectorized operations. Use categorical dtype for low-cardinality
strings. Profile with `%timeit` and check memory with
`df.estimated_size()` (polars).

## Level 3 — Full reference

### API comparison — reading data

```python
# Pandas
df = pd.read_csv("data.csv", usecols=["a", "b"], dtype={"a": "int64"})
df = pd.read_parquet("data.parquet", columns=["a", "b"])

# Polars
df = pl.read_csv("data.csv", columns=["a", "b"], schema={"a": pl.Int64})
df = pl.read_parquet("data.parquet", columns=["a", "b"])

# Polars lazy (recommended for large files)
lf = pl.scan_csv("data.csv")
df = lf.filter(...).select(...).collect()
```

### Selecting columns

```python
# Pandas
df[["name", "age"]]
df.loc[:, "name":"age"]

# Polars
df.select("name", "age")
df.select(pl.col("name"), pl.col("age"))
df.select(pl.col("^sales_.*$"))  # regex column selection
```

### Filtering rows

```python
# Pandas
df[df["age"] > 30]
df[(df["age"] > 30) & (df["city"] == "Berlin")]
df.query("age > 30 and city == 'Berlin'")

# Polars
df.filter(pl.col("age") > 30)
df.filter((pl.col("age") > 30) & (pl.col("city") == "Berlin"))
```

### Adding / transforming columns

```python
# Pandas
df["total"] = df["price"] * df["qty"]
df = df.assign(total=lambda d: d["price"] * d["qty"])

# Polars
df = df.with_columns((pl.col("price") * pl.col("qty")).alias("total"))
df = df.with_columns(
    pl.col("name").str.to_uppercase().alias("name_upper"),
    (pl.col("price") * 1.1).alias("price_with_tax"),
)
```

### GroupBy and aggregation

```python
# Pandas
df.groupby("category").agg(
    avg_price=("price", "mean"),
    total_qty=("qty", "sum"),
    count=("id", "count"),
).reset_index()

# Polars
df.group_by("category").agg(
    pl.col("price").mean().alias("avg_price"),
    pl.col("qty").sum().alias("total_qty"),
    pl.col("id").count().alias("count"),
)
```

### Window functions

```python
# Pandas
df["rank"] = df.groupby("category")["price"].rank(ascending=False)
df["avg_in_group"] = df.groupby("category")["price"].transform("mean")

# Polars
df = df.with_columns(
    pl.col("price").rank(descending=True).over("category").alias("rank"),
    pl.col("price").mean().over("category").alias("avg_in_group"),
)
```

### Joins

```python
# Pandas
pd.merge(left, right, on="id", how="left")
pd.merge(left, right, left_on="user_id", right_on="id", how="inner")

# Polars
left.join(right, on="id", how="left")
left.join(right, left_on="user_id", right_on="id", how="inner")

# Anti-join (rows in left NOT in right)
left[~left["id"].isin(right["id"])]            # pandas
left.join(right, on="id", how="anti")          # polars
```

### Pivot and melt

```python
# Pivot — Pandas
df.pivot_table(index="date", columns="product", values="sales", aggfunc="sum")
# Pivot — Polars
df.pivot(on="product", index="date", values="sales", aggregate_function="sum")

# Melt — Pandas
df.melt(id_vars=["date"], value_vars=["product_a", "product_b"],
        var_name="product", value_name="sales")
# Melt — Polars
df.unpivot(index="date", on=["product_a", "product_b"],
           variable_name="product", value_name="sales")
```

### Missing data

```python
# Pandas
df.isna().sum()
df.fillna({"price": 0, "name": "Unknown"})
df.dropna(subset=["critical_col"])
df["value"].ffill()

# Polars
df.null_count()
df.with_columns(
    pl.col("price").fill_null(0),
    pl.col("name").fill_null("Unknown"),
)
df.drop_nulls(subset=["critical_col"])
df.with_columns(pl.col("value").forward_fill())
```

### When to use which

| Scenario | Recommendation |
|---|---|
| Exploratory data analysis | Pandas (Jupyter, wider ecosystem) |
| Dataset > 1 GB | Polars (lower memory, parallel) |
| Production data pipeline | Polars (lazy eval, deterministic) |
| sklearn / statsmodels integration | Pandas (native support) |
| Streaming / chunked processing | Polars lazy or pandas chunks |
| Simple one-off scripts | Either — use what the team knows |
| Multi-threaded workloads | Polars (releases GIL, built-in parallelism) |

### Worked examples

- **Large CSV → filter → group stats:** Polars lazy mode, scan the
  CSV, filter before collect, group with multiple aggregations in
  one `.agg()`, sort, write Parquet.
- **Pandas → polars conversion:** Replace `.loc[]` with
  `filter()`/`select()`, convert `groupby().agg()` to polars
  `group_by().agg()` with `pl.col()` expressions, drop index-based
  ops, add `.lazy()`/`.collect()` for optimization.
- **Messy dataset cleanup:** Drop exact duplicates, identify
  high-null columns, fill or drop based on context, lowercase and
  strip strings, parse dates with explicit format, validate value
  ranges via filter expressions.

### References

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Polars User Guide](https://docs.pola.rs/)
