import pandas as pd

try:
    from sdv.tabular import CTGAN
    _HAS_SDV = True
except:
    _HAS_SDV = False

def synthesize(df, rows=None):
    rows = rows or len(df)
    if _HAS_SDV:
        model = CTGAN()
        model.fit(df)
        return model.sample(rows)

    # fallback
    out = df.sample(n=rows, replace=True).reset_index(drop=True)
    return out
