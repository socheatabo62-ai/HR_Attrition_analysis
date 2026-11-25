"""Home page. Run with:  streamlit run frontend/app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from backend.config import HIGH_CUT, MEDIUM_CUT, RAW_CSV
from backend.services.risk_levels import LEVELS
from frontend.components.data import load_everything
from frontend.components.ui import setup

# 1. Setup page config and CSS
st.set_page_config(page_title="HR Attrition Dashboard", page_icon="👥", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# CUSTOM SIDEBAR NAVIGATION (No Loops!)
# ==========================================
# We hide Streamlit's default menu so it doesn't conflict

st.markdown("""
<style>
/* Hide the default Streamlit menu */
[data-testid="stSidebarNav"] {display: none;}

/* Target the button container and the button itself */
[data-testid="stSidebar"] div.stButton {
    display: flex !important;
    justify-content: flex-start !important;
    margin-bottom: -15px !important; /* Removes the giant gap between buttons */
}

/* Target the actual button */
[data-testid="stSidebar"] div.stButton > button {
    background-color: transparent !important;
    color: #1A2B4C !important;
    border: none !important;
    text-align: left !important;
    justify-content: flex-start !important; 
    padding: 10px 20px !important; 
    font-weight: 600 !important;
    box-shadow: none !important;
    font-size: 16px !important;
    width: 100% !important; 
}

/* Target the text inside the button to force it left */
[data-testid="stSidebar"] div.stButton > button > div {
    justify-content: flex-start !important;
    text-align: left !important;
}

/* Hover effect */
[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #E8F0FE !important;
    color: #1A73E8 !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("")

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

def set_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# Sidebar Buttons
st.sidebar.button("🏠 Home", on_click=set_page, args=("Home",), use_container_width=True)
st.sidebar.button("📊 Overview", on_click=set_page, args=("Overview",), use_container_width=True)
st.sidebar.button("🔎 Analysis", on_click=set_page, args=("Analysis",), use_container_width=True)
st.sidebar.button("⚠️ Risk", on_click=set_page, args=("Risk",), use_container_width=True)
st.sidebar.button("💡 Explanation", on_click=set_page, args=("Explanation",), use_container_width=True)
st.sidebar.button("📈 Model", on_click=set_page, args=("Model",), use_container_width=True)
st.sidebar.button("🧪 Simulator", on_click=set_page, args=("Simulator",), use_container_width=True)
st.sidebar.button("💰 Cost", on_click=set_page, args=("Cost",), use_container_width=True)
st.sidebar.button("👤 About Me", on_click=set_page, args=("About",), use_container_width=True)

# ==========================================
# PAGE ROUTING (Loads the file smoothly)
# ==========================================
page = st.session_state.current_page

if page == "Home":
    df, res = load_everything()
    st.title("👥 HR Attrition Dashboard")
    st.caption("See which employees may resign, and why, so HR can act early.")

    st.subheader("What is loaded")
    c1, c2 = st.columns(2)
    with c1.container(border=True):
        st.markdown("**📁 Dataset**")
        st.write("IBM HR Analytics Employee Attrition & Performance")
        st.caption(f"File: {RAW_CSV.name}")
        a, b, c = st.columns(3)
        a.metric("Employees", f"{res['employees']:,}")
        b.metric("Left the company", f"{res['left']:,}")
        c.metric("Attrition rate", f"{res['attrition_rate']:.1%}")
    with c2.container(border=True):
        st.markdown("**🤖 Model**")
        st.write(res["model"])
        st.caption("Predicts the chance (0-100%) that an employee resigns.")
        a, b, c = st.columns(3)
        a.metric("ROC-AUC", f"{res['roc_auc']:.2f}")
        b.metric("Recall", f"{res['recall']:.0%}")
        c.metric("Precision", f"{res['precision']:.0%}")

    st.subheader("Resignation risk of current employees")
    current = df[df["Status"] == "Current"]
    rule = {"High": f"risk {HIGH_CUT:.0%} or more", "Medium": f"risk {MEDIUM_CUT:.0%} to {HIGH_CUT:.0%}", "Low": f"risk below {MEDIUM_CUT:.0%}"}
    icons = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
    cols = st.columns(3)
    for i, (col, lv) in enumerate(zip(cols, LEVELS)):
        with col.container(border=True):
            n = int((current["RiskLevel"] == lv).sum())
            st.metric(f"{icons[lv]} {lv} risk", f"{n:,} employees")
            st.caption(rule[lv])

elif page == "Overview":
    exec(open("frontend/pages/1_Overview.py", encoding="utf-8").read())
elif page == "Analysis":
    exec(open("frontend/pages/2_Attrition_Analysis.py", encoding="utf-8").read())
elif page == "Risk":
    exec(open("frontend/pages/3_Resignation_Risk.py", encoding="utf-8").read())
elif page == "Explanation":
    exec(open("frontend/pages/4_Risk_Explanation.py", encoding="utf-8").read())
elif page == "Model":
    exec(open("frontend/pages/5_Model_Performance.py", encoding="utf-8").read())
elif page == "Simulator":
    exec(open("frontend/pages/6_What_If_Simulator.py", encoding="utf-8").read())
elif page == "Cost":
    exec(open("frontend/pages/7_Retention_Cost.py", encoding="utf-8").read())
elif page == "About":
    exec(open("frontend/pages/8_About.py", encoding="utf-8").read())