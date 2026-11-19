"""Risk Explanation: why one employee has a high or low risk."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import plotly.express as px  # noqa: E402

from backend.services.explain import explain_employee  # noqa: E402
from frontend.components.data import get_artifacts, load_everything  # noqa: E402
from frontend.components.ui import pick_employee, setup  # noqa: E402

setup("Risk Explanation", "💡")
df, res = load_everything()
art = get_artifacts()

st.title("💡 Risk Explanation")
st.caption("Which factors push one employee's risk up or down, compared with a typical employee.")
emp, row = pick_employee(df, "ex")

a, b, c, d = st.columns(4)
a.metric("Resignation risk", f"{row['Risk']:.0%}")
b.metric("Level", row["RiskLevel"])
c.metric("Job role", row["JobRole"])
d.metric("Department", row["Department"])
a, b, c, d = st.columns(4)
a.metric("Overtime", row["OverTime"])
b.metric("Monthly income", f"${row['MonthlyIncome']:,.0f}")
c.metric("Years at company", f"{row['YearsAtCompany']}")
d.metric("Age", f"{row['Age']}")

ex = explain_employee(art, int(emp), row.to_dict())
up = ex[ex["Effect on risk (points)"] > 0.5].head(6)
down = ex[ex["Effect on risk (points)"] < -0.5].tail(6)
plot = pd.concat([up, down]).sort_values("Effect on risk (points)")
plot["Direction"] = plot["Effect on risk (points)"].apply(
    lambda v: "Raises risk" if v > 0 else "Lowers risk")
fig = px.bar(plot, x="Effect on risk (points)", y="Factor", orientation="h",
             color="Direction",
             color_discrete_map={"Raises risk": "#d62728", "Lowers risk": "#2ca02c"})
fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), legend_title_text="",
                  title="Main factors for this employee")
st.plotly_chart(fig)

st.subheader("In words")
def fmt(v):
    if isinstance(v, str):
        return v
    v = float(v)
    return str(int(v)) if v == int(v) else f"{v:.1f}"


if up.empty:
    st.write("No single factor clearly raises this employee's risk.")
for r in up.head(3).itertuples(index=False):
    st.write(f"- 🔴 **{r[0]}**: {fmt(r[1])} (typical: {fmt(r[2])}) "
             f"raises the risk by about **{r[3]:.0f} points**.")
for r in down.tail(2).iloc[::-1].itertuples(index=False):
    st.write(f"- 🟢 **{r[0]}**: {fmt(r[1])} (typical: {fmt(r[2])}) "
             f"lowers the risk by about **{abs(r[3]):.0f} points**.")
st.caption("Method: each factor is replaced by the typical employee's value and the risk is "
           "recalculated. These are patterns in the data, not proven causes.")
with st.expander("See all factors"):
    show = ex.copy()
    show["This employee"] = ex["This employee"].map(fmt)
    show["Typical employee"] = ex["Typical employee"].map(fmt)
    show["Effect on risk (points)"] = ex["Effect on risk (points)"].round(1)
    st.dataframe(show, hide_index=True)
