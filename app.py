import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# AUTH + DB
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
.sidebar .sidebar-content {
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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.anon_df = None
    st.session_state.truth_df = None
    st.session_state.protected_df = None
    st.session_state.risk_summary = {}

# ---------------- LOGIN UI ----------------
def login_signup_page():
    st.markdown("<h1 style='text-align:center;'>🔐 Safe Data Platform</h1>", unsafe_allow_html=True)

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
                st.success(f"Welcome {auth_user['username']} ({auth_user['role']})")
                st.experimental_rerun()
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
    page = st.radio(
        "Navigation",
        ["Dashboard", "Upload Data", "Risk Assessment", "Privacy Tools", "Utility & Report"]
    )

    if st.session_state.user["role"] == "Admin":
        admin_page = st.radio("Admin Panel", ["Manage Users", " "])

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.markdown("<h1>📊 Dashboard Overview</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><div class='metric-title'>Uploaded Datasets</div><div class='metric-value'>"
                    f"{len(list(UPLOAD_DIR.glob('*.csv')))}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><div class='metric-title'>Protected Files</div><div class='metric-value'>"
                    f"{len(list(PROTECTED_DIR.glob('*.csv')))}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><div class='metric-title'>Reports Generated</div><div class='metric-value'>"
                    f"{len(list(REPORT_DIR.glob('*.pdf')))}</div></div>", unsafe_allow_html=True)

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
        st.warning("Upload anonymized dataset first")
    else:
        columns = st.multiselect("Select quasi-identifiers", st.session_state.anon_df.columns)

        if columns:
            truth_df = st.session_state.truth_df
            risk = summarize_risk(st.session_state.anon_df, truth_df, columns)
            st.session_state.risk_summary = risk

            col1, col2, col3 = st.columns(3)
            col1.metric("Uniqueness Ratio", f"{risk['uniqueness_ratio']*100:.2f}%")
            col2.metric("k-Anonymity", risk['k_anonymity'])
            col3.metric("Re-ID Risk", f"{risk['linkage_reid_rate']*100:.2f}%")

            grp = st.session_state.anon_df.groupby(columns).size().reset_index(name="count")
            fig = px.histogram(grp, x="count", nbins=20, title="Group Size Distribution")
            st.plotly_chart(fig, use_container_width=True)

# ---------------- PRIVACY TOOLS ----------------
elif page == "Privacy Tools":
    require_role(["Admin"])

    st.markdown("<h1>🛡 Privacy Tools</h1>", unsafe_allow_html=True)
    tool = st.selectbox("Choose a method", ["Differential Privacy", "Synthetic Data", "SDC (Topcoding/Generalization/Suppression)"])

    if tool == "Differential Privacy":
        eps = st.slider("Epsilon", 0.05, 5.0, 1.0)
        num_cols = st.multiselect("Numeric Columns", st.session_state.anon_df.columns)

        if st.button("Apply DP"):
            prot = laplace_mechanism(st.session_state.anon_df, num_cols, eps)
            st.session_state.protected_df = prot
            st.success("DP applied")
            st.dataframe(prot.head())

    elif tool == "Synthetic Data":
        rows = st.number_input("Rows", value=len(st.session_state.anon_df))
        if st.button("Generate Synthetic"):
            prot = synthesize(st.session_state.anon_df, rows)
            st.session_state.protected_df = prot
            st.success("Synthetic data generated")
            st.dataframe(prot.head())

    elif tool == "SDC (Topcoding/Generalization/Suppression)":
        col = st.selectbox("Column for topcoding", st.session_state.anon_df.columns)
        thr = st.number_input("Threshold", value=100.0)
        if st.button("Apply SDC"):
            df = top_code(st.session_state.anon_df, col, thr)
            st.session_state.protected_df = df
            st.success("SDC applied")
            st.dataframe(df.head())

# ---------------- UTILITY + REPORT ----------------
elif page == "Utility & Report":
    require_role(["Admin", "Analyst", "Viewer"])

    st.markdown("<h1>📑 Utility Analysis & Report</h1>", unsafe_allow_html=True)

    if st.session_state.protected_df is None:
        st.warning("Apply a privacy method first!")
    else:
        stats = basic_stats(st.session_state.anon_df, st.session_state.protected_df)
        st.dataframe(stats)

        score = utility_score(stats)
        st.metric("Utility Score", score)

        title = st.text_input("Report Title", "Safe Data Privacy Report")
        technique = st.text_input("Technique Used", "Differential Privacy (example)")

        if st.button("Generate PDF Report"):
            path = generate_privacy_report(REPORT_DIR, title, st.session_state.risk_summary, technique, {}, score)
            st.success("Report generated!")
            with open(path, "rb") as f:
                st.download_button("Download Report", f, file_name=path.name)
