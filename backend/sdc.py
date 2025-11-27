import numpy as np
import pandas as pd

def top_code(df, col, threshold):
    out = df.copy()
    out[col] = np.where(out[col] > threshold, threshold, out[col])
    return out

def generalize_binning(df, col, bins, labels):
    out = df.copy()
    out[col] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)
    return out

def suppress_rare(df, cols, min_count=3):
    out = df.copy()
    freq = out.groupby(cols).size().reset_index(name="cnt")
    rare = freq[freq["cnt"] < min_count][cols]
    if not rare.empty:
        out.loc[out[cols].apply(tuple, axis=1).isin(rare.apply(tuple, axis=1)), cols] = "***"
    return out
