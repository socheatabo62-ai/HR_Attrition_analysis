"""Resignation Risk: every employee with a risk % and a Low/Medium/High level."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import plotly.express as px  # noqa: E402

from backend.config import HIGH_CUT, MEDIUM_CUT  # noqa: E402
from backend.services.risk_levels import COLORS, LEVELS  # noqa: E402
from frontend.components.data import load_everything  # noqa: E402
from frontend.components.filters import sidebar_filters  # noqa: E402
from frontend.components.ui import setup  # noqa: E402

setup("Resignation Risk", "⚠️")
df, res = load_everything()
f = sidebar_filters(df, "rk", default_group="Current employees")

st.title("⚠️ Resignation Risk")
st.caption(f"High = risk {HIGH_CUT:.0%} or more, Medium = {MEDIUM_CUT:.0%} to "
           f"{HIGH_CUT:.0%}, Low = below {MEDIUM_CUT:.0%}.")
if f.empty:
    st.warning("No employees match the filters. Change the filters in the sidebar.")
    st.stop()

k = st.columns(3)
for col, lv in zip(k, LEVELS):
    col.metric(f"{lv} risk", f"{int((f['RiskLevel'] == lv).sum()):,} employees")

# level choice (the Home page can pre-select one level)
preset = st.session_state.pop("preset_levels", None)
if preset or "risk_levels_pick" not in st.session_state:
    st.session_state["risk_levels_pick"] = preset or ["High", "Medium"]
levels = st.multiselect("Show risk levels", LEVELS, key="risk_levels_pick")
search = st.text_input("Find an employee number", placeholder="e.g. 959")

view = f[f["RiskLevel"].isin(levels)]
if search.strip().isdigit():
    view = view[view["EmployeeNumber"] == int(search)]
view = view.sort_values("Risk", ascending=False)

table = pd.DataFrame({
    "Employee #": view["EmployeeNumber"], "Department": view["Department"],
    "Job role": view["JobRole"], "Overtime": view["OverTime"],
    "Monthly income": view["MonthlyIncome"], "Years at company": view["YearsAtCompany"],
    "Risk": view["Risk"] * 100, "Level": view["RiskLevel"], "Status": view["Status"],
})
st.write(f"**{len(table):,} employees** shown, highest risk first.")
st.dataframe(table, hide_index=True, column_config={
    "Risk": st.column_config.ProgressColumn("Resignation risk", min_value=0,
                                            max_value=100, format="%.0f%%"),
    "Monthly income": st.column_config.NumberColumn(format="$%d"),
})
st.download_button("⬇️ Download this list (CSV)",
                   table.round(1).to_csv(index=False).encode("utf-8"),
                   file_name="resignation_risk_list.csv", mime="text/csv")

st.subheader("Risk level by department")
g = f.groupby(["Department", "RiskLevel"]).size().reset_index(name="Employees")
fig = px.bar(g, x="Department", y="Employees", color="RiskLevel", barmode="stack",
             color_discrete_map=COLORS, category_orders={"RiskLevel": LEVELS})
fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), legend_title_text="")
st.plotly_chart(fig)
st.caption("Open **Risk Explanation** to see why a person has their risk.")
