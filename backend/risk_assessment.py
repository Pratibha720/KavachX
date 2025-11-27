import pandas as pd

def uniqueness_ratio(df, quasi):
    grp = df.groupby(quasi).size().reset_index(name="count")
    return round((grp["count"] == 1).sum() / len(df), 4)

def k_anonymity(df, quasi):
    return int(df.groupby(quasi).size().min())

def linkage_reid_rate(anon, truth, quasi):
    if truth is None:
        return 0.0
    merged = anon.merge(truth[quasi].drop_duplicates(), on=quasi, how="inner")
    return round(len(merged) / len(anon), 4)

def summarize_risk(anon_df, truth_df, quasi_cols):
    return {
        "uniqueness_ratio": uniqueness_ratio(anon_df, quasi_cols),
        "k_anonymity": k_anonymity(anon_df, quasi_cols),
        "linkage_reid_rate": linkage_reid_rate(anon_df, truth_df, quasi_cols)
    }
