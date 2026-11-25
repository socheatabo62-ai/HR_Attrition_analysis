"""Overview: totals, attrition rate, income and tenure."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from frontend.components import charts  # noqa: E402
from frontend.components.data import load_everything  # noqa: E402
from frontend.components.filters import sidebar_filters  # noqa: E402
from frontend.components.ui import setup  # noqa: E402

setup("Overview", "📊")
df, res = load_everything()
f = sidebar_filters(df, "ov📊")

st.title("📊 Overview")
if f.empty:
    st.warning("No employees match the filters. Change the filters in the sidebar.")
    st.stop()

k = st.columns(6)
k[0].metric("Employees", f"{len(f):,}")
k[1].metric("Left the company", f"{int(f['Left'].sum()):,}")
k[2].metric("Attrition rate", f"{f['Left'].mean():.1%}")
k[3].metric("Avg monthly income", f"${f['MonthlyIncome'].mean():,.0f}")
k[4].metric("Avg years at company", f"{f['YearsAtCompany'].mean():.1f}")
k[5].metric("Avg age", f"{f['Age'].mean():.0f}")

a, b = st.columns(2)
a.plotly_chart(charts.headcount_bar(f, "Department", "Employees by department"))
fig, _ = charts.rate_bar(f, "Department", "Attrition rate by department")
b.plotly_chart(fig)

a, b = st.columns(2)
a.plotly_chart(charts.histogram(f, "MonthlyIncome", "Monthly income: current vs left"))
b.plotly_chart(charts.histogram(f, "YearsAtCompany", "Years at company: current vs left",
                                nbins=20))
st.caption("Employees who left tend to earn less and have worked fewer years at the company.")


