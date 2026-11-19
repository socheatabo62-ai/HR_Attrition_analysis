"""Retention Cost: expected cost of likely resignations."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import plotly.express as px  # noqa: E402

from backend.services.risk_levels import COLORS, LEVELS  # noqa: E402
from frontend.components.data import load_everything  # noqa: E402
from frontend.components.filters import sidebar_filters  # noqa: E402
from frontend.components.ui import setup  # noqa: E402

setup("Retention Cost", "💰")
df, res = load_everything()
f = sidebar_filters(df, "rc", default_group="Current employees")

st.title("💰 Retention Cost")
st.caption("Estimate what resignations may cost. The dataset has no replacement cost, "
           "so you enter your own assumption.")
if f.empty:
    st.warning("No employees match the filters. Change the filters in the sidebar.")
    st.stop()

st.subheader("Your assumptions")
a, b = st.columns(2)
basis = a.radio("Cost of replacing one employee", ["% of annual salary", "Fixed amount ($)"])
if basis == "% of annual salary":
    pct = a.slider("Replacement cost (% of annual salary)", 10, 200, 50, step=5)
    cost = f["MonthlyIncome"] * 12 * pct / 100
else:
    amount = a.number_input("Replacement cost per employee ($)", min_value=0,
                            value=15000, step=500)
    cost = pd.Series(float(amount), index=f.index)
keep = b.slider("Share of High-risk employees HR manages to keep (%)", 0, 100, 30, step=5)

d = f.assign(Cost=cost)
d["ExpectedCost"] = d["Risk"] * d["Cost"]
high = d[d["RiskLevel"] == "High"]
expected_leavers = d["Risk"].sum()
total = d["ExpectedCost"].sum()
saved = high["ExpectedCost"].sum() * keep / 100

st.subheader("Estimate")
k = st.columns(4)
k[0].metric("Employees in this group", f"{len(d):,}")
k[1].metric("Expected resignations", f"{expected_leavers:,.0f}")
k[2].metric("Expected replacement cost", f"${total:,.0f}")
k[3].metric("Cost avoided if you keep them", f"${saved:,.0f}",
            help=f"Keeping {keep}% of the {len(high):,} High-risk employees")

g = d.groupby(["Department", "RiskLevel"])["ExpectedCost"].sum().reset_index()
fig = px.bar(g, x="Department", y="ExpectedCost", color="RiskLevel", barmode="stack",
             color_discrete_map=COLORS, category_orders={"RiskLevel": LEVELS},
             labels={"ExpectedCost": "Expected cost ($)"})
fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), legend_title_text="",
                  title="Expected replacement cost by department")
st.plotly_chart(fig)
st.caption("Expected resignations = the sum of each employee's risk. The dataset does not say "
           "how long the period is, so read the numbers as a rough guide. "
           "Costs depend entirely on the assumption you enter.")
