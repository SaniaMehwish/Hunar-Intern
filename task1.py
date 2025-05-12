import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('food_coded.csv')  # or the correct path if different

# Step 1: Remove duplicate columns
df = df.loc[:, ~df.columns.duplicated()]

# Step 2: Remove duplicate rows
df = df.drop_duplicates()

# Step 3: Convert relevant object columns to numeric
df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
df['weight'] = pd.to_numeric(df['weight'], errors='coerce')

# Step 4: Identify numeric and non-numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns

# Step 5: Create copies for different fill strategies
df_mean = df.copy()
df_median = df.copy()
df_mode = df.copy()

# Fill numeric columns
df_mean[numeric_cols] = df_mean[numeric_cols].fillna(df_mean[numeric_cols].mean())
df_median[numeric_cols] = df_median[numeric_cols].fillna(df_median[numeric_cols].median())
for col in numeric_cols:
    mode_val = df_mode[col].mode()
    if not mode_val.empty:
        df_mode[col] = df_mode[col].fillna(mode_val[0])

# Fill non-numeric columns with mode
for col in non_numeric_cols:
    mode_val = df[col].mode()
    if not mode_val.empty:
        df_mean[col] = df_mean[col].fillna(mode_val[0])
        df_median[col] = df_median[col].fillna(mode_val[0])
        df_mode[col] = df_mode[col].fillna(mode_val[0])

# Optional: Save to new CSV files
df_mean.to_csv('food_cleaned_mean.csv', index=False)
df_median.to_csv('food_cleaned_median.csv', index=False)
df_mode.to_csv('food_cleaned_mode.csv', index=False)

print("Preview of cleaned data (filled with mode):")
print(df_mode.head())

