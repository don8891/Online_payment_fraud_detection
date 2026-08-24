import pandas as pd
import numpy as np
import gc
from pathlib import Path

processed_dir = Path("data/processed")

print("Converting X_train.pkl to float32 parquet...")
df = pd.read_pickle(processed_dir / "X_train.pkl")
print(f"Loaded X_train with shape: {df.shape}, memory usage: {df.memory_usage().sum() / 1e6:.2f} MB")

num_cols = df.select_dtypes(include=['number']).columns
df[num_cols] = df[num_cols].astype('float32')

print(f"Downcasted memory usage: {df.memory_usage().sum() / 1e6:.2f} MB")
df.to_parquet(processed_dir / "X_train.parquet")
del df
gc.collect()

print("Converting X_val.pkl to float32 parquet...")
df_val = pd.read_pickle(processed_dir / "X_val.pkl")
num_cols_val = df_val.select_dtypes(include=['number']).columns
df_val[num_cols_val] = df_val[num_cols_val].astype('float32')
df_val.to_parquet(processed_dir / "X_val.parquet")
del df_val
gc.collect()

print("Successfully converted datasets to float32 Parquet format!")
