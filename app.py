# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from pathlib import Path

# # AUTH + DB
# from backend.auth import authenticate_user, create_user, get_all_users
# from backend.db import get_connection

# # BACKEND MODULES
# from backend.utils import save_uploaded_csv, to_csv_download_bytes, UPLOAD_DIR, PROTECTED_DIR, REPORT_DIR
# from backend.risk_assessment import summarize_risk
# from backend.differential_privacy import laplace_mechanism
# from backend.synthetic_data import synthesize
# from backend.sdc import top_code, generalize_binning, suppress_rare
# from backend.utility_metrics import basic_stats, utility_score
# from backend.report_generator import generate_privacy_report

# # ---------------- CUSTOM CSS ----------------
# CUSTOM_CSS = """
# <style>
# body {
#     background-color: #f5f5f5 !important;
# }
# .sidebar .sidebar-content {
#     background-color: #1a1a1a !important;
# }
# h1, h2, h3, h4 {
#     color: #222;
# }
# .stButton>button {
#     background: #4CAF50;
#     color: white;
#     border-radius: 8px;
#     padding: 8px 16px;
#     border: none;
# }
# .card {
#     background: white;
#     padding: 20px;
#     border-radius: 12px;
#     box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
#     margin-bottom: 20px;
# }
# .metric-card {
#     background: #ffffff;
#     padding: 25px;
#     border-radius: 14px;
#     text-align: center;
#     box-shadow: 0px 4px 8px rgba(0,0,0,0.08);
# }
# .metric-title {
#     font-size: 16px;
#     font-weight: bold;
#     color: #555;
# }
# .metric-value {
#     font-size: 28px;
#     font-weight: bold;
#     color: #4CAF50;
# }
# </style>
# """

# st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# # ---------------- SESSION STATE ----------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
#     st.session_state.user = None
#     st.session_state.anon_df = None
#     st.session_state.truth_df = None
#     st.session_state.protected_df = None
#     st.session_state.risk_summary = {}

# # ---------------- LOGIN UI ----------------
# def login_signup_page():
#     st.markdown("<h1 style='text-align:center;'>🔐 KavachX</h1>", unsafe_allow_html=True)

#     tab1, tab2 = st.tabs(["Login", "Signup"])

#     with tab1:
#         st.subheader("Login to your account")
#         user = st.text_input("Username")
#         pwd = st.text_input("Password", type="password")

#         if st.button("Login"):
#             auth_user = authenticate_user(user, pwd)
#             if auth_user:
#                 st.session_state.logged_in = True
#                 st.session_state.user = auth_user
#                 st.success(f"Welcome {auth_user['username']} ({auth_user['role']})")
#                 st.experimental_rerun()
#             else:
#                 st.error("Invalid username or password")

#     with tab2:
#         st.subheader("Create a new account")
#         new_user = st.text_input("New Username")
#         new_pass = st.text_input("New Password", type="password")
#         role = st.selectbox("Role", ["Admin", "Analyst", "Viewer"])

#         if st.button("Sign Up"):
#             ok = create_user(new_user, new_pass, role)
#             if ok:
#                 st.success("Account created successfully! Please log in.")
#             else:
#                 st.error("Username already exists!")

#     st.stop()

# if not st.session_state.logged_in:
#     login_signup_page()

# # ROLE GUARD
# def require_role(roles):
#     if st.session_state.user["role"] not in roles:
#         st.error("🚫 You don't have access to this section.")
#         st.stop()

# # ---------------- SIDEBAR NAV ----------------
# with st.sidebar:
#     st.header(f"👤 {st.session_state.user['username']} ({st.session_state.user['role']})")
#     page = st.radio(
#         "Navigation",
#         ["Dashboard", "Upload Data", "Risk Assessment", "Privacy Tools", "Utility & Report"]
#     )

#     if st.session_state.user["role"] == "Admin":
#         admin_page = st.radio("Admin Panel", ["Manage Users", " "])

#     if st.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.user = None
#         st.experimental_rerun()

# # ---------------- DASHBOARD ----------------
# if page == "Dashboard":
#     st.markdown("<h1>📊 Dashboard Overview</h1>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown("<div class='metric-card'><div class='metric-title'>Uploaded Datasets</div><div class='metric-value'>"
#                     f"{len(list(UPLOAD_DIR.glob('*.csv')))}</div></div>", unsafe_allow_html=True)
#     with col2:
#         st.markdown("<div class='metric-card'><div class='metric-title'>Protected Files</div><div class='metric-value'>"
#                     f"{len(list(PROTECTED_DIR.glob('*.csv')))}</div></div>", unsafe_allow_html=True)
#     with col3:
#         st.markdown("<div class='metric-card'><div class='metric-title'>Reports Generated</div><div class='metric-value'>"
#                     f"{len(list(REPORT_DIR.glob('*.pdf')))}</div></div>", unsafe_allow_html=True)

# # ---------------- UPLOAD DATA ----------------
# elif page == "Upload Data":
#     require_role(["Admin", "Analyst"])

#     st.markdown("<h1>📤 Upload Datasets</h1>", unsafe_allow_html=True)
#     col1, col2 = st.columns(2)

#     with col1:
#         up1 = st.file_uploader("Upload anonymized dataset", type="csv")
#         if up1:
#             path = save_uploaded_csv(up1)
#             st.session_state.anon_df = pd.read_csv(path)
#             st.success("Anonymized dataset uploaded")
#             st.dataframe(st.session_state.anon_df.head())

#     with col2:
#         up2 = st.file_uploader("Upload ground truth dataset (optional)", type="csv")
#         if up2:
#             path = save_uploaded_csv(up2)
#             st.session_state.truth_df = pd.read_csv(path)
#             st.info("Ground truth dataset uploaded")
#             st.dataframe(st.session_state.truth_df.head())

# # ---------------- RISK ASSESSMENT ----------------
# elif page == "Risk Assessment":
#     require_role(["Admin", "Analyst"])

#     st.markdown("<h1>🛑 Risk Assessment</h1>", unsafe_allow_html=True)

#     if st.session_state.anon_df is None:
#         st.warning("Upload anonymized dataset first")
#     else:
#         columns = st.multiselect("Select quasi-identifiers", st.session_state.anon_df.columns)

#         if columns:
#             truth_df = st.session_state.truth_df
#             risk = summarize_risk(st.session_state.anon_df, truth_df, columns)
#             st.session_state.risk_summary = risk

#             col1, col2, col3 = st.columns(3)
#             col1.metric("Uniqueness Ratio", f"{risk['uniqueness_ratio']*100:.2f}%")
#             col2.metric("k-Anonymity", risk['k_anonymity'])
#             col3.metric("Re-ID Risk", f"{risk['linkage_reid_rate']*100:.2f}%")

#             grp = st.session_state.anon_df.groupby(columns).size().reset_index(name="count")
#             fig = px.histogram(grp, x="count", nbins=20, title="Group Size Distribution")
#             st.plotly_chart(fig, use_container_width=True)

# # ---------------- PRIVACY TOOLS ----------------
# elif page == "Privacy Tools":
#     require_role(["Admin"])

#     st.markdown("<h1>🛡 Privacy Tools</h1>", unsafe_allow_html=True)
#     tool = st.selectbox("Choose a method", ["Differential Privacy", "Synthetic Data", "SDC (Topcoding/Generalization/Suppression)"])

#     if tool == "Differential Privacy":
#         eps = st.slider("Epsilon", 0.05, 5.0, 1.0)
#         num_cols = st.multiselect("Numeric Columns", st.session_state.anon_df.columns)

#         if st.button("Apply DP"):
#             prot = laplace_mechanism(st.session_state.anon_df, num_cols, eps)
#             st.session_state.protected_df = prot
#             st.success("DP applied")
#             st.dataframe(prot.head())

#     elif tool == "Synthetic Data":
#         rows = st.number_input("Rows", value=len(st.session_state.anon_df))
#         if st.button("Generate Synthetic"):
#             prot = synthesize(st.session_state.anon_df, rows)
#             st.session_state.protected_df = prot
#             st.success("Synthetic data generated")
#             st.dataframe(prot.head())

#     elif tool == "SDC (Topcoding/Generalization/Suppression)":
#         col = st.selectbox("Column for topcoding", st.session_state.anon_df.columns)
#         thr = st.number_input("Threshold", value=100.0)
#         if st.button("Apply SDC"):
#             df = top_code(st.session_state.anon_df, col, thr)
#             st.session_state.protected_df = df
#             st.success("SDC applied")
#             st.dataframe(df.head())

# # ---------------- UTILITY + REPORT ----------------
# elif page == "Utility & Report":
#     require_role(["Admin", "Analyst", "Viewer"])

#     st.markdown("<h1>📑 Utility Analysis & Report</h1>", unsafe_allow_html=True)

#     if st.session_state.protected_df is None:
#         st.warning("Apply a privacy method first!")
#     else:
#         stats = basic_stats(st.session_state.anon_df, st.session_state.protected_df)
#         st.dataframe(stats)

#         score = utility_score(stats)
#         st.metric("Utility Score", score)

#         title = st.text_input("Report Title", "Safe Data Privacy Report")
#         technique = st.text_input("Technique Used", "Differential Privacy (example)")

#         if st.button("Generate PDF Report"):
#             path = generate_privacy_report(REPORT_DIR, title, st.session_state.risk_summary, technique, {}, score)
#             st.success("Report generated!")
#             with open(path, "rb") as f:
#                 st.download_button("Download Report", f, file_name=path.name)


import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from backend.utils import save_protected_csv


# AUTH + DB
# Assuming these imports work and the backend files are present
from backend.auth import authenticate_user, create_user, get_all_users
from backend.db import get_connection

# BACKEND MODULES
from backend.utils import save_uploaded_csv, to_csv_download_bytes, UPLOAD_DIR, PROTECTED_DIR, REPORT_DIR
from backend.risk_assessment import summarize_risk
from backend.differential_privacy import laplace_mechanism
from backend.synthetic_data import synthesize
from backend.sdc import top_code, generalize_binning, suppress_rare
from backend.utility_metrics import basic_stats, utility_score
from backend.report_generator import generate_privacy_report

# ---------------- CUSTOM CSS ----------------
CUSTOM_CSS = """
<style>
body {
    background-color: #f5f5f5 !important;
}
.st-emotion-cache-16txte9 { /* Targets Streamlit sidebar container */
    background-color: #1a1a1a !important;
}
h1, h2, h3, h4 {
    color: #222;
}
.stButton>button {
    background: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    border: none;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.metric-card {
    background: #ffffff;
    padding: 25px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.08);
}
.metric-title {
    font-size: 16px;
    font-weight: bold;
    color: #555;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #4CAF50;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
# Initialize all necessary session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "anon_df" not in st.session_state:
    st.session_state.anon_df = None
if "truth_df" not in st.session_state:
    st.session_state.truth_df = None
if "protected_df" not in st.session_state:
    st.session_state.protected_df = None
if "risk_summary" not in st.session_state:
    st.session_state.risk_summary = {}

# ---------------- LOGIN UI ----------------
def login_signup_page():
    st.markdown("<h1 style='text-align:center;'>🔐 KavachX</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login to your account")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            auth_user = authenticate_user(user, pwd)
            if auth_user:
                st.session_state.logged_in = True
                st.session_state.user = auth_user
                st.success(f"Welcome **{auth_user['username']}** (**{auth_user['role']}**)")
                # FIX 1: Replace st.experimental_rerun() with st.rerun()
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Create a new account")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["Admin", "Analyst", "Viewer"])

        if st.button("Sign Up"):
            ok = create_user(new_user, new_pass, role)
            if ok:
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists!")

    st.stop()

if not st.session_state.logged_in:
    login_signup_page()

# ROLE GUARD
def require_role(roles):
    if st.session_state.user["role"] not in roles:
        st.error("🚫 You don't have access to this section.")
        st.stop()

# ---------------- SIDEBAR NAV ----------------
with st.sidebar:
    st.header(f"👤 {st.session_state.user['username']} ({st.session_state.user['role']})")
    
    # Ensure a default page is selected
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    page = st.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload Data",
        "Risk Assessment",
        "Privacy Tools",
        "Utility & Report",
        "Protected Files"       # <-- ADD THIS
    ],
    key="current_page"
)


    if st.session_state.user["role"] == "Admin":
        # FIX 4: Removed unnecessary placeholder " " from admin panel options
        admin_page = st.radio("Admin Panel", ["Manage Users"])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.anon_df = None
        st.session_state.truth_df = None
        st.session_state.protected_df = None
        st.session_state.risk_summary = {}
        # FIX 1: Replace st.experimental_rerun() with st.rerun()
        st.rerun()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.markdown("<h1>📊 Dashboard Overview</h1>", unsafe_allow_html=True)

    # Check if directories exist before counting (optional, but robust)
    upload_count = len(list(UPLOAD_DIR.glob('*.csv'))) if UPLOAD_DIR.exists() else 0
    protected_count = len(list(PROTECTED_DIR.glob('*.csv'))) if PROTECTED_DIR.exists() else 0
    report_count = len(list(REPORT_DIR.glob('*.pdf'))) if REPORT_DIR.exists() else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Uploaded Datasets</div><div class='metric-value'>{upload_count}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Protected Files</div><div class='metric-value'>{protected_count}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Reports Generated</div><div class='metric-value'>{report_count}</div></div>", unsafe_allow_html=True)

# ---------------- UPLOAD DATA ----------------
elif page == "Upload Data":
    require_role(["Admin", "Analyst"])

    st.markdown("<h1>📤 Upload Datasets</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        up1 = st.file_uploader("Upload anonymized dataset", type="csv")
        if up1:
            path = save_uploaded_csv(up1)
            st.session_state.anon_df = pd.read_csv(path)
            st.session_state.protected_df = None # Reset protected DF on new upload
            st.success("Anonymized dataset uploaded")
            st.dataframe(st.session_state.anon_df.head())

    with col2:
        up2 = st.file_uploader("Upload ground truth dataset (optional)", type="csv")
        if up2:
            path = save_uploaded_csv(up2)
            st.session_state.truth_df = pd.read_csv(path)
            st.info("Ground truth dataset uploaded")
            st.dataframe(st.session_state.truth_df.head())

# ---------------- RISK ASSESSMENT ----------------
elif page == "Risk Assessment":
    require_role(["Admin", "Analyst"])

    st.markdown("<h1>🛑 Risk Assessment</h1>", unsafe_allow_html=True)
    

    if st.session_state.anon_df is None:
        st.warning("Upload anonymized dataset first in the **Upload Data** page.")
    else:
        # Check if the dataframe is empty
        if st.session_state.anon_df.empty:
            st.error("Uploaded DataFrame is empty.")
            st.stop()
        
        columns = st.multiselect("Select quasi-identifiers", st.session_state.anon_df.columns)

        if columns:
            truth_df = st.session_state.truth_df
            # Note: The risk function is assumed to handle truth_df being None gracefully
            risk = summarize_risk(st.session_state.anon_df, truth_df, columns)
            st.session_state.risk_summary = risk

            st.markdown("### Risk Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Uniqueness Ratio", f"{risk.get('uniqueness_ratio', 0.0)*100:.2f}%")
            col2.metric("k-Anonymity", risk.get('k_anonymity', 'N/A'))
            col3.metric("Re-ID Risk", f"{risk.get('linkage_reid_rate', 0.0)*100:.2f}%")

            st.markdown("### Group Size Analysis")
            try:
                grp = st.session_state.anon_df.groupby(columns, dropna=False).size().reset_index(name="count")
                # Filter out single-count groups for a clearer visualization of risk
                fig = px.histogram(grp, x="count", log_y=True, nbins=20, title="Group Size Distribution (Log Scale Count)")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not generate group size histogram. Check selected columns. Error: {e}")

# -----------------------------------------------------------
# PRIVACY TOOLS (FULLY UPDATED WITH ADVANCED METHODS)
# -----------------------------------------------------------
elif page == "Privacy Tools":
    require_role(["Admin"])

    st.markdown("<h1>🛡 Privacy Tools</h1>", unsafe_allow_html=True)

    if st.session_state.anon_df is None:
        st.warning("Upload anonymized dataset first in the Upload Data page.")
        st.stop()

    df = st.session_state.anon_df.copy()
    all_cols = df.columns.tolist()

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
    date_cols = [c for c in all_cols if "date" in c.lower()]

    tool = st.selectbox(
        "Choose a method",
        [
            "Differential Privacy (Laplace)",
            "Differential Privacy (Gaussian)",
            "Randomized Response (Categorical Noise)",
            "Microaggregation (k-Anonymity)",
            "Date Noise",
            "Masking / Redaction",
            "Synthetic Data Generation",
            "SDC (Topcoding / Generalization / Suppression)"
        ]
    )

    st.info("A protected dataset will overwrite the previously generated one and will be SAVED automatically.")

    # -----------------------------------------------------------
    # 1) LAPLACE DP
    # -----------------------------------------------------------
    if tool == "Differential Privacy (Laplace)":
        st.subheader("Laplace Mechanism")

        eps = st.slider("Epsilon ε", 0.01, 5.0, 1.0)
        cols = st.multiselect("Select Numeric Columns", numeric_cols)

        if st.button("Apply Laplace DP"):
            try:
                prot = laplace_mechanism(df, cols, eps)
                st.session_state.protected_df = prot

                # SAVE FILE
                save_protected_csv(prot, "laplace_dp")

                st.success("Laplace DP applied and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 2) GAUSSIAN DP
    # -----------------------------------------------------------
    if tool == "Differential Privacy (Gaussian)":
        st.subheader("Gaussian Mechanism")

        sigma = st.slider("Sigma (Standard Deviation)", 0.1, 10.0, 1.0)
        cols = st.multiselect("Select Numeric Columns", numeric_cols)

        if st.button("Apply Gaussian DP"):
            try:
                from backend.differential_privacy import gaussian_mechanism
                prot = gaussian_mechanism(df, cols, sigma)
                st.session_state.protected_df = prot

                save_protected_csv(prot, "gaussian_dp")

                st.success("Gaussian DP applied and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 3) RANDOMIZED RESPONSE
    # -----------------------------------------------------------
    if tool == "Randomized Response (Categorical Noise)":
        st.subheader("Randomized Response")

        prob = st.slider("Noise Probability", 0.01, 0.90, 0.15)
        cols = st.multiselect("Select Categorical Columns", categorical_cols)

        if st.button("Apply Randomized Response"):
            try:
                from backend.differential_privacy import randomized_response
                prot = randomized_response(df, cols, prob)
                st.session_state.protected_df = prot

                save_protected_csv(prot, "randomized_response")

                st.success("Randomized response applied and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 4) MICROAGGREGATION
    # -----------------------------------------------------------
    if tool == "Microaggregation (k-Anonymity)":
        st.subheader("Microaggregation")

        k = st.slider("Cluster Size (k)", 2, 10, 3)
        cols = st.multiselect("Select Numeric Columns", numeric_cols)

        if st.button("Apply Microaggregation"):
            try:
                from backend.differential_privacy import microaggregation
                prot = microaggregation(df, cols, k)
                st.session_state.protected_df = prot

                save_protected_csv(prot, "microaggregation")

                st.success(f"Microaggregation applied (k={k}) and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 5) DATE NOISE
    # -----------------------------------------------------------
    if tool == "Date Noise":
        st.subheader("Date Noise (± Random Days)")

        days = st.slider("Maximum Days to Add/Remove", 1, 60, 30)
        cols = st.multiselect("Select Date Columns", date_cols)

        if st.button("Apply Date Noise"):
            try:
                from backend.differential_privacy import date_noise
                prot = date_noise(df, cols, max_days=days)
                st.session_state.protected_df = prot

                save_protected_csv(prot, "date_noise")

                st.success("Date noise applied and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 6) MASKING / REDACTION
    # -----------------------------------------------------------
    if tool == "Masking / Redaction":
        st.subheader("Data Masking")

        cols = st.multiselect("Select Columns to Mask", all_cols)
        start = st.slider("Visible Characters (Start)", 1, 5, 2)
        end = st.slider("Visible Characters (End)", 1, 5, 2)

        if st.button("Apply Masking"):
            try:
                from backend.differential_privacy import mask_column
                prot = mask_column(df, cols, start, end)
                st.session_state.protected_df = prot

                save_protected_csv(prot, "masking")

                st.success("Masking applied and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 7) SYNTHETIC DATA
    # -----------------------------------------------------------
    if tool == "Synthetic Data Generation":
        st.subheader("Synthetic Data")

        rows = st.number_input("Synthetic Rows", min_value=10, value=len(df))

        if st.button("Generate Synthetic Data"):
            try:
                prot = synthesize(df, rows)
                st.session_state.protected_df = prot

                save_protected_csv(prot, "synthetic_data")

                st.success("Synthetic data generated and saved.")
                st.dataframe(prot.head())
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------------------------------------
    # 8) SDC
    # -----------------------------------------------------------
    if tool == "SDC (Topcoding / Generalization / Suppression)":
        st.subheader("SDC Tools")

        sdc_method = st.selectbox("Choose SDC Method", ["Topcoding", "Generalization/Binning", "Suppression"])

        if sdc_method == "Topcoding":
            col = st.selectbox("Column", numeric_cols)
            thr = st.number_input("Threshold", value=100.0)

            if st.button("Apply Topcoding"):
                try:
                    df2 = top_code(df.copy(), col, thr)
                    st.session_state.protected_df = df2

                    save_protected_csv(df2, "topcoding")

                    st.success("Topcoding applied and saved.")
                    st.dataframe(df2.head())
                except Exception as e:
                    st.error(f"Error: {e}")


# ---------------- UTILITY + REPORT ----------------
elif page == "Utility & Report":
    require_role(["Admin", "Analyst", "Viewer"])

    st.markdown("<h1>📑 Utility Analysis & Report</h1>", unsafe_allow_html=True)
    

    if st.session_state.anon_df is None:
        st.warning("Upload original anonymized dataset first in the **Upload Data** page.")
        st.stop()

    if st.session_state.protected_df is None:
        st.warning("Apply a privacy method in the **Privacy Tools** page to generate a protected dataset for comparison.")
    else:
        st.markdown("## Basic Statistical Comparison")
        try:
            stats = basic_stats(st.session_state.anon_df, st.session_state.protected_df)
            st.dataframe(stats)

            st.markdown("## Calculated Utility Score")
            score = utility_score(stats)
            st.metric("Utility Score", f"{score:.4f}")

            st.markdown("---")
            st.markdown("## Privacy Report Generation")
            
            # Use sensible defaults and allow user input
            title = st.text_input("Report Title", "Safe Data Privacy Report")
            technique = st.text_input("Technique Used", "Differential Privacy, Synthetic Data, or SDC")

            if st.button("Generate PDF Report"):
                with st.spinner("Generating report..."):
                    # Assuming generate_privacy_report handles the required inputs gracefully
                    # The risk_summary needs to be a dict, which it is if Risk Assessment was run
                    path = generate_privacy_report(
                        REPORT_DIR, 
                        title, 
                        st.session_state.get('risk_summary', {}), # Use .get() for safety
                        technique, 
                        # Assuming the function accepts an empty dict if no utility details are needed beyond score
                        stats.to_dict('records') if not stats.empty else {}, 
                        score
                    )
                    st.success(f"Report generated: {path.name}")
                    with open(path, "rb") as f:
                        st.download_button(
                            "Download Report PDF", 
                            f.read(), # Read bytes from file handle
                            file_name=path.name,
                            mime="application/pdf" # Specify mime type
                        )
        except Exception as e:
             st.error(f"An error occurred during Utility Analysis: {e}")

# ---------------- PROTECTED FILE MANAGER ----------------
elif page == "Protected Files":
    require_role(["Admin", "Analyst", "Viewer"])

    st.markdown("<h1>🗂 Protected File Manager</h1>", unsafe_allow_html=True)

    if not PROTECTED_DIR.exists():
        st.error("Protected directory does not exist.")
        st.stop()

    protected_files = list(PROTECTED_DIR.glob("*.csv"))

    if not protected_files:
        st.info("No protected files generated yet.")
        st.stop()

    # Show file list
    file_names = [f.name for f in protected_files]
    selected_file = st.selectbox("Select a protected file", file_names)

    file_path = PROTECTED_DIR / selected_file

    st.markdown("### File Preview")

    try:
        df_preview = pd.read_csv(file_path)
        st.dataframe(df_preview.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Could not read CSV: {e}")

    st.markdown("---")

    # Download button
    with open(file_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Protected CSV",
            data=f.read(),
            file_name=selected_file,
            mime="text/csv"
        )

    # Delete button
    if st.button("🗑 Delete This File"):
        try:
            file_path.unlink(missing_ok=True)
            st.success(f"{selected_file} deleted successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Error deleting file: {e}")

             