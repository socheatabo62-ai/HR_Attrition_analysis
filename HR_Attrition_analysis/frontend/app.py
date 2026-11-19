"""Home page. Run with:  streamlit run frontend/app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

from backend.config import HIGH_CUT, MEDIUM_CUT, RAW_CSV  # noqa: E402
from backend.services.risk_levels import LEVELS  # noqa: E402
from frontend.components.data import load_everything  # noqa: E402
from frontend.components.ui import setup  # noqa: E402

setup("HR Attrition Dashboard", "👥")
df, res = load_everything()

st.title("👥 HR Attrition Dashboard")
st.caption("See which employees may resign, and why, so HR can act early.")

# ---- what is loaded ------------------------------------------------------
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

# ---- risk levels (click to open the list) -----------------------------------
st.subheader("Resignation risk of current employees")
st.caption("Click a level to see those employees.")
current = df[df["Status"] == "Current"]
rule = {"High": f"risk {HIGH_CUT:.0%} or more",
        "Medium": f"risk {MEDIUM_CUT:.0%} to {HIGH_CUT:.0%}",
        "Low": f"risk below {MEDIUM_CUT:.0%}"}
icons = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
cols = st.columns(3)
for col, lv in zip(cols, LEVELS):
    with col.container(border=True):
        n = int((current["RiskLevel"] == lv).sum())
        st.metric(f"{icons[lv]} {lv} risk", f"{n:,} employees")
        st.caption(rule[lv])
        if st.button(f"See {lv.lower()}-risk employees", key=f"go_{lv}"):
            st.session_state["preset_levels"] = [lv]
            st.switch_page("pages/3_Resignation_Risk.py")

# ---- open any page -----------------------------------------------------------
st.subheader("Open a page")
pages = [
    ("pages/1_Overview.py", "📊 Overview", "Totals, attrition rate, income and tenure"),
    ("pages/2_Attrition_Analysis.py", "🔎 Attrition Analysis",
     "Who leaves: by job role, overtime, age, travel, income"),
    ("pages/3_Resignation_Risk.py", "⚠️ Resignation Risk",
     "Risk list with filters and CSV download"),
    ("pages/4_Risk_Explanation.py", "💡 Risk Explanation",
     "Why one employee has a high or low risk"),
    ("pages/5_Model_Performance.py", "📈 Model Performance",
     "How accurate the model is, and what matters most"),
    ("pages/6_What_If_Simulator.py", "🧪 What-If Simulator",
     "Change overtime or pay and see the risk change"),
    ("pages/7_Retention_Cost.py", "💰 Retention Cost",
     "Estimated cost of likely resignations"),
]
cols = st.columns(3)
for i, (path, label, desc) in enumerate(pages):
    with cols[i % 3].container(border=True):
        st.page_link(path, label=label)
        st.caption(desc)

with st.expander("How to read the risk"):
    st.write(
        "The risk is the model's estimate of the chance that an employee resigns. "
        "It is a prompt for a conversation, not a verdict. Gender and marital status "
        "are not used. Every employee is scored by a model that never saw that "
        "employee's own outcome.")
