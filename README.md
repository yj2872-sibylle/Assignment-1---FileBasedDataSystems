# Street Closures due to Construction Activities by Block

## Why I Chose This Dataset

I chose the NYC Open Data dataset Street Closures due to Construction
Activities by Block because it is a real, actively-updated civic dataset
that anyone in NYC could use. For example, to check whether a street near
them is closed before driving or biking through it. It has a clean mix of
column types (geometry, IDs, text/categorical fields, and dates), which made
it a good fit for practicing filtering, counting, and two-condition
breakdowns.

## Three Data Questions

### Question 1: How many street closures are recorded in each borough?

```python
closures_per_borough = df["BOROUGH_CODE"].value_counts()
```

**Output:**
```
BOROUGH_CODE
Q    1706
M     874
B     549
S     384
X     223
```

**Why the data supports this:** `BOROUGH_CODE` is a categorical column with
one value per row, so grouping and counting rows by that category is a
direct, one-step operation (`value_counts`). This works because every row
represents a single closure tied to exactly one borough.

### Question 2: What are the five most common reasons (PURPOSE) for a street closure?

```python
top_purposes = df["PURPOSE"].value_counts().head(5)
```

**Output:**
```
PURPOSE
DOT IN-HOUSE PAVING                         1499
DOT IN-HOUSE MILLING                         710
OCCUPANCY OF ROADWAY AS STIPULATED           412
PLACE EQUIPMENT OTHER THAN CRANE OR SHOV     253
OCCUPANCY OF SIDEWALK AS STIPULATED          170
```

**Why the data supports this:** `PURPOSE` is a free-text but controlled
categorical field (a limited set of standardized reason codes), so counting
frequencies of each unique string is straightforward and meaningful. It
tells us that street paving and milling dominate the reasons streets get
closed.

### Question 3: For each borough, how many closures last more than 30 days vs. 30 days or fewer? (two-condition breakdown)

```python
df["duration_days"] = (df["WORK_END_DATE"] - df["WORK_START_DATE"]).dt.days
duration_breakdown = pd.crosstab(df["BOROUGH_CODE"], df["duration_days"] > 30)
```

**Output:**
```
              30 days or fewer  more than 30 days
BOROUGH_CODE
B                          248                301
M                          223                651
Q                           46               1660
S                           79                305
X                           37                186
```

**Why the data supports this:** Because the dataset provides both a start
and an end date for every closure, a derived numeric column (`duration_days`)
can be computed, and then cross-tabulated against the categorical
`BOROUGH_CODE` column. This combines a categorical condition (borough) with
a numeric/boolean condition (duration > 30 days), which is exactly the kind
of two-condition breakdown that relational joins/group-bys will formalize
later.

## What the Data Cannot Answer

One question I wish I could answer is how much these closures actually
inconvenienced residents or businesses (e.g., traffic delays, lost revenue,
or how many people were affected), but the dataset has no measure of impact,
only the physical location and duration of the closure. It's also missing
any information about the contractor or agency actually doing the work
beyond the coded `PURPOSE` field, the cost of the project, or whether the
closure was extended/completed on schedule (there's no "actual completion
date," only a planned `WORK_END_DATE`). It would be misleading to assume
that a row's date range reflects exactly when a street was physically
closed, since permitted work windows are often wider than the actual
disruption, and to assume that closure counts are the same as "distinct
projects," since a single construction project can span many contiguous
block segments and therefore many rows.
