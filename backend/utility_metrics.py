import numpy as np
import pandas as pd

def basic_stats(orig, prot):
    stats = []
    for col in orig.select_dtypes(include=['int', 'float']).columns:
        if col in prot.columns:
            stats.append({
                "column": col,
                "orig_mean": orig[col].mean(),
                "prot_mean": prot[col].mean()
            })
    return pd.DataFrame(stats)

def utility_score(df):
    if df.empty:
        return 0.0
    gap = abs(df["orig_mean"] - df["prot_mean"]).mean()
    return round(max(0, 1 - gap / (df["orig_mean"].mean() + 1e-6)), 3)
