import numpy as np
import pandas as pd

def laplace_mechanism(df, numeric_cols, epsilon):
    df2 = df.copy()
    scale = 1 / max(epsilon, 1e-6)

    for col in numeric_cols:
        if col in df2.columns:
            noise = np.random.laplace(0, scale, size=len(df2))
            df2[col] = df2[col].astype(float) + noise

    return df2
