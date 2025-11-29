# Safe Data Protection Platform

## Installation
git clone https://github.com/YOUR-USERNAME/safe-data-platform.git
cd safe-data-platform

python -m venv .venv
.venv\Scripts\activate     # Windows
# OR
source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

## Run the App
streamlit run app.py

# Features
- Login / Signup + Roles
- Upload datasets
- Risk Assessment (k-anonymity, linkage risk)
- Differential Privacy
- Synthetic Data (CTGAN)
- SDC Tools
- Utility Score
- PDF Report Generation
