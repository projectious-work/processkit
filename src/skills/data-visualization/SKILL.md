---
name: data-visualization
description: |
  Chart selection, color accessibility, annotation, and dashboard design. Use when creating charts, designing dashboards, choosing visualization types, improving chart readability, or reviewing data presentations for clarity.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-data-visualization
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: data
---

# Data Visualization

## Intro

A good chart matches the chart type to the data relationship,
annotates the insight rather than the raw point, and stays readable
for colorblind viewers. The default fallbacks are bar (categorical)
and scatter (continuous).

## Overview

### Chart type selection

Match chart to relationship, not to what looks impressive. Quick
guide: comparison = bar, trend = line, distribution = histogram,
relationship = scatter. When unsure, default to bar (categorical) or
scatter (continuous). Never use a pie chart with more than four
slices — use a horizontal bar instead. Avoid 3D charts entirely
unless you are visualizing actual three-dimensional data. Full
decision tree is in Level 3.

### Color and accessibility

Use colorblind-friendly palettes: seaborn `"colorblind"`, viridis,
cividis. Never rely on color alone — add patterns, markers, or
labels. Sequential data (low-to-high) needs a single-hue gradient or
viridis. Diverging data (deviation from center) needs coolwarm or
RdBu centered at zero. Categorical data needs distinct hues with
sufficient contrast. Limit to seven or fewer colors; group or facet
beyond that. Test with a colorblindness simulator before sharing.

### Annotation

Annotate the insight, not just the data point. Always annotate
max/min values that matter, threshold or target lines, and events
that explain trend changes. Use direct labels instead of legends
with 2–3 series. Arrows should point from label to data, not the
reverse. Keep annotation text concise: "Peak: 1,247 (Q3 launch)" not
"The maximum value occurred in Q3."

### Dashboard layout

Place the most important metric in the top-left (reading order).
Use a consistent grid: 2–3 columns, cards of equal height per row.
Group related metrics visually. Filters live at the top, not buried
in individual charts. Every dashboard needs a title, date range, and
data freshness indicator. Limit to 6–8 visualizations per dashboard
— more causes cognitive overload.

### Storytelling

Lead with the conclusion: "Revenue grew 40% in Q3," not "Here is a
chart of revenue." Structure as context → finding → implication. Use
progressive disclosure: summary first, then supporting detail.
Highlight the relevant; dim or remove the irrelevant. Annotate to
guide the viewer's eye to the key insight.

### Static vs interactive

Static charts (matplotlib, seaborn) for reports, papers,
presentations. Interactive (plotly, Altair, D3) for dashboards and
exploratory tools. Interactive needs tooltips, zoom for dense data,
and filter controls. Static needs readability at print size (12pt+
fonts, 300 dpi). Always provide a static fallback for interactive
charts.

## Full reference

### Chart selection decision tree

**Comparison across categories:**

- **Vertical bar** — magnitudes across < 15 categories. Avoid for
  time series (use line) or > 15 categories (use horizontal).
- **Horizontal bar** — long labels or > 10 categories. Avoid for
  time-based or continuous x-axis.
- **Grouped bar** — comparing 2–3 sub-groups within a category.
  Avoid > 3 sub-groups (facet instead) or when showing totals
  (stacked).

**Trend over time:**

- **Line** — continuous time axis, 1–5 series. Avoid with < 5 time
  points or > 7 lines.
- **Area** — emphasizing total volume or magnitude. Avoid for
  similar-magnitude series (lines occlude) or precise reading.

**Distribution:**

- **Histogram** — shape of one continuous variable.
- **Box plot** — comparing distributions across groups.
- **Violin** — like box plot but shows full shape; good for bimodal
  data.

**Relationship:**

- **Scatter** — two continuous variables. Use hexbin or 2D density
  for > 1000 points.
- **Bubble** — scatter with size as a third variable. Avoid for
  precise comparison (humans are bad at areas).
- **Heatmap** — magnitude across two categorical or ordinal
  dimensions. Avoid for sparse data or > 20 items per axis.

**Composition (parts of a whole):**

- **Stacked bar** — parts contributing to a total over time or
  category. Avoid > 5–6 segments.
- **Pie** — only with 2–4 slices and approximate proportions.
  Almost always replaceable with a horizontal bar.
- **Treemap** — hierarchical part-of-whole with many categories.
  Avoid when precise comparison matters.

**Geographic:**

- **Choropleth** — values for defined regions.
- **Point/dot map** — individual locations or events.

| Relationship | First choice | Alternative | Avoid |
|---|---|---|---|
| Compare categories | Vertical bar | Horizontal bar, lollipop | Pie |
| Trend over time | Line | Area | Bar (unless few points) |
| Distribution | Histogram | Box, violin | Pie |
| Two variables | Scatter | Hexbin, 2D density | Line |
| Parts of whole | Stacked bar | Treemap | Pie (> 4 slices) |
| Correlation matrix | Heatmap | Clustered pairs | Table of numbers |
| Geographic | Choropleth | Point map | Non-geographic |

### Universal rules

1. Start with the simplest chart that answers the question.
2. If the legend has > 7 entries, redesign.
3. If a colleague cannot understand it in 10 seconds, simplify.
4. When comparing, use the same axis scale across panels.
5. Titles state the insight: "Sales doubled in Q3," not "Sales by
   Quarter."

### Common mistakes

- Truncated y-axis on bar charts — bars must start at zero
- Dual y-axes — misleading; use two panels
- Overplotting — use alpha, jitter, hexbin, or density
- Missing units on axes
- Default titles ("Figure 1") instead of the finding
- Legend far from the data it describes
- Too many decimal places — round to meaningful precision

### Export checklist

Before sharing, verify: title states the finding; both axes labeled
with units; legend present or direct labels used; colorblind-friendly
palette; 300 dpi for print, SVG/PDF for scalable; fonts readable at
final display size.

### Worked examples

- **5 product lines × 24 months:** Multi-line chart, one line per
  product, distinct colorblind-safe colors with direct end-of-line
  labels instead of a legend. Title states the trend ("Product A
  overtook B in mid-2025"), annotate the crossover point, light
  gridlines on white background.
- **15-chart dashboard is overwhelming:** Audit for redundancy,
  group remaining charts by domain, move detail charts to a
  drill-down page, keep 6 key metrics on the main view, add a
  summary KPI row with sparklines at the top.
- **Overplotted scatter:** Reduce marker size, set `alpha=0.3`,
  switch dense regions to hexbin or 2D density, add marginal
  histograms, label outlier clusters.
