import pandas as pd

CSV_FILE = "Street_Closures_due_to_Construction_Activities_by_Block_20260913.csv"

df = pd.read_csv(CSV_FILE)

# Parse the date columns so they can be used for duration calculations later
df["WORK_START_DATE"] = pd.to_datetime(df["WORK_START_DATE"], format="%m/%d/%Y %I:%M:%S %p")
df["WORK_END_DATE"] = pd.to_datetime(df["WORK_END_DATE"], format="%m/%d/%Y %I:%M:%S %p")

# Task 1: Print the first 2 rows
print(df.head(2))

# Task 2: Print the first row
print(df.head(1))

# Task 3: Print rows 10-19
print(df.iloc[10:20])

# Task 4: Print column names
print(df.columns.tolist())

# Task 5: Print the first 10 values of one column
print(df["ONSTREETNAME"].head(10))

# Task 6: Print the first 10 rows of three columns
print(df[["ONSTREETNAME", "BOROUGH_CODE", "PURPOSE"]].head(10))

# Task 7: Three data questions

# Question 1: How many street closures are recorded in each borough?
closures_per_borough = df["BOROUGH_CODE"].value_counts()
print(closures_per_borough)

# Question 2: What are the five most common reasons (PURPOSE) for a closure?
top_purposes = df["PURPOSE"].value_counts().head(5)
print(top_purposes)

# Question 3: For each borough, how many closures last longer than 30 days versus 30 days or fewer? (two-condition breakdown: borough x duration)
df["duration_days"] = (df["WORK_END_DATE"] - df["WORK_START_DATE"]).dt.days
duration_breakdown = pd.crosstab(df["BOROUGH_CODE"], df["duration_days"] > 30)
duration_breakdown.columns = ["30 days or fewer", "more than 30 days"]
print(duration_breakdown)