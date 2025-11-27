import os
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = BASE_DIR / "datasets"
UPLOAD_DIR = DATASET_DIR / "uploaded"
PROTECTED_DIR = DATASET_DIR / "protected"
REPORT_DIR = BASE_DIR / "reports"

for d in [UPLOAD_DIR, PROTECTED_DIR, REPORT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def save_uploaded_csv(uploaded_file, subdir="uploaded"):
    target = UPLOAD_DIR if subdir == "uploaded" else PROTECTED_DIR
    path = target / uploaded_file.name
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def load_csv(path):
    return pd.read_csv(path)

def to_csv_download_bytes(df):
    return df.to_csv(index=False).encode("utf-8")
