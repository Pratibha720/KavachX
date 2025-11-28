# import os
# from pathlib import Path
# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parents[1]
# DATASET_DIR = BASE_DIR / "datasets"
# UPLOAD_DIR = DATASET_DIR / "uploaded"
# PROTECTED_DIR = DATASET_DIR / "protected"
# REPORT_DIR = BASE_DIR / "reports"

# for d in [UPLOAD_DIR, PROTECTED_DIR, REPORT_DIR]:
#     d.mkdir(parents=True, exist_ok=True)

# def save_uploaded_csv(uploaded_file, subdir="uploaded"):
#     target = UPLOAD_DIR if subdir == "uploaded" else PROTECTED_DIR
#     path = target / uploaded_file.name
#     with open(path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     return path

# def load_csv(path):
#     return pd.read_csv(path)

# def to_csv_download_bytes(df):
#     return df.to_csv(index=False).encode("utf-8")


# from pathlib import Path
# from datetime import datetime
# import pandas as pd

# PROTECTED_DIR = Path("backend/datasets/protected")
# PROTECTED_DIR.mkdir(parents=True, exist_ok=True)

# def save_protected_csv(df):
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"protected_{timestamp}.csv"
#     path = PROTECTED_DIR / filename
#     df.to_csv(path, index=False)
#     return path

# def list_protected_files():
#     return sorted(PROTECTED_DIR.glob("*.csv"))

# def load_protected_csv(file_path):
#     return pd.read_csv(file_path)

# def delete_protected_file(file_path):
#     file_path.unlink(missing_ok=True)


import pandas as pd
from pathlib import Path
import uuid

# ---------------- DIRECTORIES ----------------
BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploaded"
PROTECTED_DIR = BASE_DIR / "protected"
REPORT_DIR = BASE_DIR / "reports"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
PROTECTED_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


# ---------------- SAVE UPLOADED CSV ----------------
def save_uploaded_csv(uploaded_file):
    """
    Save uploaded CSV to /uploaded directory with a unique name.
    """
    file_id = uuid.uuid4().hex
    save_path = UPLOAD_DIR / f"{file_id}_{uploaded_file.name}"

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path


# ---------------- SAVE PROTECTED CSV ----------------
def save_protected_csv(df, filename="protected"):
    """
    Save protected dataset to /protected directory.
    File is auto-versioned using random unique ID.
    """
    file_id = uuid.uuid4().hex
    file_path = PROTECTED_DIR / f"{filename}_{file_id}.csv"

    df.to_csv(file_path, index=False)
    return file_path


# ---------------- LOAD PROTECTED FILE ----------------
def load_protected_csv(file_path):
    """
    Load a protected CSV file into a DataFrame.
    """
    return pd.read_csv(file_path)


# ---------------- DELETE PROTECTED FILE ----------------
def delete_protected_file(file_path):
    """
    Delete a protected file from disk.
    """
    file_path.unlink(missing_ok=True)


# ---------------- CSV DOWNLOAD BYTES ----------------
def to_csv_download_bytes(df):
    """
    Convert DataFrame to downloadable CSV byte string.
    Useful for Streamlit download buttons.
    """
    return df.to_csv(index=False).encode("utf-8")
