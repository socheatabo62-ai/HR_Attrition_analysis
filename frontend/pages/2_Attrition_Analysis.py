"""Attrition Analysis: who leaves, by one factor at a time."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from backend.services.load_data import AGE_ORDER, INCOME_ORDER, TENURE_ORDER  # noqa: E402
from frontend.components import charts  # noqa: E402
from frontend.components.data import load_everything  # noqa: E402
from frontend.components.filters import sidebar_filters  # noqa: E402
from frontend.components.ui import setup  # noqa: E402

setup("Attrition Analysis", "🔎")
df, res = load_everything()
f = sidebar_filters(df, "an")

st.title("🔎 Attrition Analysis")
st.caption("Compare the attrition rate (share of employees who left) across groups.")
if f.empty:
    st.warning("No employees match the filters. Change the filters in the sidebar.")
    st.stop()

OPTIONS = {
    "Job role": ("JobRole", None), "Department": ("Department", None),
    "Overtime": ("OverTime", None), "Business travel": ("BusinessTravel", None),
    "Age group": ("AgeGroup", AGE_ORDER), "Income band": ("IncomeBand", INCOME_ORDER),
    "Years at company": ("TenureGroup", TENURE_ORDER),
    "Job level": ("JobLevel", None), "Job satisfaction (1-4)": ("JobSatisfaction", None),
    "Work-life balance (1-4)": ("WorkLifeBalance", None),
    "Stock option level": ("StockOptionLevel", None),
    "Education field": ("EducationField", None),
}
choice = st.selectbox("Compare employees by", list(OPTIONS))
col, order = OPTIONS[choice]
fig, table = charts.rate_bar(f, col, f"Attrition rate by {choice.lower()}", order)
st.plotly_chart(fig)

big = table[table["Employees"] >= 20]
if len(big) >= 2:
    hi = big.loc[big["Attrition rate (%)"].idxmax()]
    lo = big.loc[big["Attrition rate (%)"].idxmin()]
    st.info(f"Highest attrition: **{hi[col]}** ({hi['Attrition rate (%)']:.1f}%). "
            f"Lowest: **{lo[col]}** ({lo['Attrition rate (%)']:.1f}%). "
            "Only groups with 20+ employees are compared.")
shown = table.rename(columns={col: choice})
shown["Attrition rate (%)"] = shown["Attrition rate (%)"].round(1)
st.dataframe(shown, hide_index=True)

st.subheader("Key patterns")
a, b = st.columns(2)
fig1, _ = charts.rate_bar(f, "OverTime", "Overtime")
fig2, _ = charts.rate_bar(f, "BusinessTravel", "Business travel")
a.plotly_chart(fig1)
b.plotly_chart(fig2)
fig3, _ = charts.rate_bar(f, "JobRole", "Job role")
st.plotly_chart(fig3)
st.caption("A pattern is not a cause. Use it to decide where to look first.")
