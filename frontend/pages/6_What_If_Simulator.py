"""What-If Simulator: change one employee's situation and see the risk change."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from backend.config import CATEGORIES  # noqa: E402
from backend.services.model_service import predict_employee  # noqa: E402
from backend.services.risk_levels import level  # noqa: E402
from frontend.components.data import get_artifacts, load_everything  # noqa: E402
from frontend.components.ui import pick_employee, setup  # noqa: E402

setup("What-If Simulator", "🧪")
df, res = load_everything()
art = get_artifacts()

st.title("🧪 What-If Simulator")
st.caption("Change a few things for one employee and see how the model's risk estimate moves.")
emp, row = pick_employee(df, "wi")
base = row.to_dict()

st.subheader("Change the situation")
a, b = st.columns(2)
ot = a.selectbox("Overtime", ["No", "Yes"], index=["No", "Yes"].index(base["OverTime"]),
                 key=f"ot_{emp}")
travel_opts = CATEGORIES["BusinessTravel"]
travel = b.selectbox("Business travel", travel_opts,
                     index=travel_opts.index(base["BusinessTravel"]), key=f"tr_{emp}")
income = a.number_input("Monthly income ($)", min_value=1000, max_value=50000,
                        value=int(base["MonthlyIncome"]), step=100, key=f"inc_{emp}")
promo = b.slider("Years since last promotion", 0, 15,
                 int(min(base["YearsSinceLastPromotion"], 15)), key=f"pr_{emp}")
sat = a.slider("Job satisfaction (1-4)", 1, 4, int(base["JobSatisfaction"]), key=f"sa_{emp}")
wlb = b.slider("Work-life balance (1-4)", 1, 4, int(base["WorkLifeBalance"]), key=f"wl_{emp}")
stock = a.slider("Stock option level (0-3)", 0, 3, int(base["StockOptionLevel"]),
                 key=f"st_{emp}")
train = b.slider("Trainings last year", 0, 6, int(base["TrainingTimesLastYear"]),
                 key=f"tn_{emp}")

changes = {"OverTime": ot, "BusinessTravel": travel, "MonthlyIncome": float(income),
           "YearsSinceLastPromotion": float(promo), "JobSatisfaction": float(sat),
           "WorkLifeBalance": float(wlb), "StockOptionLevel": float(stock),
           "TrainingTimesLastYear": float(train)}
new_row = {**base, **changes}
cur = predict_employee(art, int(emp), base)
new = predict_employee(art, int(emp), new_row)

st.subheader("Result")
a, b, c = st.columns(3)
a.metric("Current risk", f"{cur:.0%}")
b.metric("New risk", f"{new:.0%}", delta=f"{(new - cur) * 100:+.1f} points",
         delta_color="inverse")
c.metric("Level", f"{level(cur)} -> {level(new)}")

def same(a, b):
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return str(a) == str(b)


changed = [(k, base[k], v) for k, v in changes.items() if not same(base[k], v)]
if changed:
    st.write("**What you changed:** " + ", ".join(f"{k} ({o} -> {n})" for k, o, n in changed))
else:
    st.write("Nothing changed yet. Move one of the controls above.")
st.caption("This is the model's estimate from patterns in past data. It does not prove that "
           "making this change would stop the person from resigning.")
