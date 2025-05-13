import pandas as pd
import numpy as np

df = pd.read_csv('food_coded.csv')
df = df.loc[:, ~df.columns.duplicated()]
df = df.drop_duplicates()
df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
numeric_cols = df.select_dtypes(include=[np.number]).columns
non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
df_mean = df.copy()
df_median = df.copy()
df_mode = df.copy()
df_mean[numeric_cols] = df_mean[numeric_cols].fillna(df_mean[numeric_cols].mean())
df_median[numeric_cols] = df_median[numeric_cols].fillna(df_median[numeric_cols].median())
for col in numeric_cols:
    mode_val = df_mode[col].mode()
    if not mode_val.empty:
        df_mode[col] = df_mode[col].fillna(mode_val[0])
for col in non_numeric_cols:
    mode_val = df[col].mode()
    if not mode_val.empty:
        df_mean[col] = df_mean[col].fillna(mode_val[0])
        df_median[col] = df_median[col].fillna(mode_val[0])
        df_mode[col] = df_mode[col].fillna(mode_val[0])
df_mean.to_csv('food_cleaned_mean.csv', index=False)
df_median.to_csv('food_cleaned_median.csv', index=False)
df_mode.to_csv('food_cleaned_mode.csv', index=False)

print("Preview of cleaned data (filled with mode):")
print(df_mode.head())

