
"""Home page. Run with: streamlit run frontend/app.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from backend.config import HIGH_CUT, MEDIUM_CUT, RAW_CSV
from backend.services.risk_levels import LEVELS
from frontend.components.data import load_everything
from frontend.components.ui import setup


# =====================================
# HOME DASHBOARD
# =====================================

def show_home():

    # PAGE SETUP
    setup("HR Attrition Dashboard", "👥")

    df, res = load_everything()

    # DASHBOARD HEADER
    st.title("👥 HR Attrition Dashboard")

    st.caption(
        "See which employees may resign, and why, so HR can act early."
    )

    # WHAT IS LOADED
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

        st.caption(
            "Predicts the chance (0-100%) that an employee resigns."
        )

        a, b, c = st.columns(3)

        a.metric("ROC-AUC", f"{res['roc_auc']:.2f}")
        b.metric("Recall", f"{res['recall']:.0%}")
        c.metric("Precision", f"{res['precision']:.0%}")

    # RESIGNATION RISK LEVELS
    st.subheader("Resignation risk of current employees")

    st.caption("Click a level to see those employees.")

    current = df[df["Status"] == "Current"]

    rule = {
        "High": f"Risk {HIGH_CUT:.0%} or more",
        "Medium": f"Risk {MEDIUM_CUT:.0%} to {HIGH_CUT:.0%}",
        "Low": f"Risk below {MEDIUM_CUT:.0%}"
    }

    icons = {
        "High": "🔴",
        "Medium": "🟠",
        "Low": "🟢"
    }

    cols = st.columns(3)

    for col, lv in zip(cols, LEVELS):

        with col.container(border=True):

            n = int((current["RiskLevel"] == lv).sum())

            st.metric(
                f"{icons[lv]} {lv} risk",
                f"{n:,} employees"
            )

            st.caption(rule[lv])

            if st.button(
                f"See {lv.lower()}-risk employees",
                key=f"go_{lv}"
            ):

                st.session_state["preset_levels"] = [lv]

                st.switch_page("pages/3_Resignation_Risk.py")

    # RISK EXPLANATION
    with st.expander("How to read the risk"):

        st.write(
            "The risk is the model's estimate of the chance that an "
            "employee resigns. It is a prompt for a conversation, "
            "not a verdict. Gender and marital status are not used. "
            "Every employee is scored by a model that never saw that "
            "employee's own outcome."
        )


# =====================================
# PAGE NAVIGATION
# =====================================

home = st.Page(
    show_home,
    title="Home",
    icon="🏠",
    default=True
)

overview = st.Page(
    "pages/1_Overview.py",
    title="Overview",
    icon="📊"
)

attrition = st.Page(
    "pages/2_Attrition_Analysis.py",
    title="Attrition Analysis",
    icon="🔎"
)

risk = st.Page(
    "pages/3_Resignation_Risk.py",
    title="Resignation Risk",
    icon="⚠️"
)

explanation = st.Page(
    "pages/4_Risk_Explanation.py",
    title="Risk Explanation",
    icon="💡"
)

performance = st.Page(
    "pages/5_Model_Performance.py",
    title="Model Performance",
    icon="📈"
)

simulator = st.Page(
    "pages/6_What_If_Simulator.py",
    title="What-If Simulator",
    icon="🧪"
)

retention = st.Page(
    "pages/7_Retention_Cost.py",
    title="Retention Cost",
    icon="💰"
)


# =====================================
# RUN NAVIGATION
# =====================================

pg = st.navigation([
    home,
    overview,
    attrition,
    risk,
    explanation,
    performance,
    simulator,
    retention
])

pg.run()
