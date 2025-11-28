# import numpy as np
# import pandas as pd

# def laplace_mechanism(df, numeric_cols, epsilon):
#     df2 = df.copy()
#     scale = 1 / max(epsilon, 1e-6)

#     for col in numeric_cols:
#         if col in df2.columns:
#             noise = np.random.laplace(0, scale, size=len(df2))
#             df2[col] = df2[col].astype(float) + noise

#     return df2


import numpy as np
import pandas as pd
from datetime import timedelta
import random


# ---------------------------------------------------------
# 1) LAPLACE MECHANISM (for numeric columns)
# ---------------------------------------------------------
def laplace_mechanism(df, numeric_cols, epsilon):
    df2 = df.copy()
    scale = 1 / max(epsilon, 1e-6)

    for col in numeric_cols:
        if col in df2.columns:
            noise = np.random.laplace(0, scale, size=len(df2))
            df2[col] = pd.to_numeric(df2[col], errors='coerce').fillna(0)
            df2[col] = df2[col] + noise

    return df2


# ---------------------------------------------------------
# 2) GAUSSIAN MECHANISM (Normal Distribution Noise)
# ---------------------------------------------------------
def gaussian_mechanism(df, numeric_cols, sigma=1.0):
    df2 = df.copy()

    for col in numeric_cols:
        if col in df2.columns:
            noise = np.random.normal(0, sigma, size=len(df2))
            df2[col] = pd.to_numeric(df2[col], errors='coerce').fillna(0)
            df2[col] = df2[col] + noise

    return df2


# ---------------------------------------------------------
# 3) RANDOMIZED RESPONSE (for categorical columns)
# ---------------------------------------------------------
def randomized_response(df, cat_cols, prob=0.15):
    df2 = df.copy()

    for col in cat_cols:
        if col in df2.columns:
            unique_vals = df2[col].dropna().unique().tolist()

            def rr(x):
                if pd.isna(x) or len(unique_vals) == 0:
                    return x
                if np.random.rand() < prob:
                    return random.choice(unique_vals)
                return x

            df2[col] = df2[col].apply(rr)

    return df2


# ---------------------------------------------------------
# 4) MICROAGGREGATION (k-anonymity enhancement)
# ---------------------------------------------------------


def microaggregation(df, numeric_cols, k):
    df2 = df.copy()

    for col in numeric_cols:
        # ensure numeric column
        df2[col] = pd.to_numeric(df2[col], errors='coerce')

        # sort values
        sorted_df = df2.sort_values(by=col)

        # create groups of size k
        groups = []
        for i in range(0, len(sorted_df), k):
            group = sorted_df.iloc[i:i+k]
            avg = group[col].mean()
            groups.append((group.index, avg))

        # assign new averaged values
        for idx, avg in groups:
            df2.loc[idx, col] = avg

    return df2



# ---------------------------------------------------------
# 5) DATE NOISE (± random days)
# ---------------------------------------------------------
def date_noise(df, date_cols, max_days=30):
    df2 = df.copy()

    for col in date_cols:
        if col in df2.columns:
            try:
                df2[col] = pd.to_datetime(df2[col], errors="coerce")
                df2[col] = df2[col] + df2[col].apply(
                    lambda x: timedelta(days=random.randint(-max_days, max_days))
                    if pd.notnull(x) else x
                )
            except:
                pass

    return df2


# ---------------------------------------------------------
# 6) MASKING / REDACTION
# ---------------------------------------------------------
def mask_column(df, cols, start=2, end=2):
    df2 = df.copy()

    for col in cols:
        if col in df2.columns:
            df2[col] = df2[col].astype(str).apply(
                lambda x: x[:start] + "*" * (len(x) - start - end) + x[-end:]
                if len(x) > (start + end) else x
            )

    return df2


# ---------------------------------------------------------
# FULL PRIVACY PIPELINE (optional)
# ---------------------------------------------------------
def full_privacy_pipeline(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(exclude=['number']).columns.tolist()

    df2 = laplace_mechanism(df, numeric_cols, epsilon=1.0)
    df2 = randomized_response(df2, cat_cols, prob=0.10)

    return df2
