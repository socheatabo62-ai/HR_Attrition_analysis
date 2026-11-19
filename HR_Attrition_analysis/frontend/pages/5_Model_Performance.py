"""Model Performance: how good the model is and what matters most."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import plotly.express as px  # noqa: E402

from backend.config import HIGH_CUT, LABELS  # noqa: E402
from frontend.components.data import load_everything  # noqa: E402
from frontend.components.ui import setup  # noqa: E402

setup("Model Performance", "📈")
df, res = load_everything()

st.title("📈 Model Performance")
st.caption(f"{res['model']}. Results come from employees the model had not seen "
           f"(each person is scored by a model that did not train on them).")

k = st.columns(5)
k[0].metric("ROC-AUC", f"{res['roc_auc']:.2f}", help="1.0 = perfect, 0.5 = guessing")
k[1].metric("Accuracy", f"{res['accuracy']:.0%}")
k[2].metric("Precision", f"{res['precision']:.0%}",
            help="Of the people flagged High, how many really left")
k[3].metric("Recall", f"{res['recall']:.0%}",
            help="Of the people who really left, how many were flagged High")
k[4].metric("F1 score", f"{res['f1']:.2f}")
st.info(f"Why accuracy alone is misleading: {1 - res['attrition_rate']:.0%} of employees "
        "stayed, so a model that always says 'stays' is already that accurate. "
        "Recall and precision show how well it finds the people who leave.")

a, b = st.columns(2)
with a:
    c = res["confusion"]
    fig = px.imshow([[c["tn"], c["fp"]], [c["fn"], c["tp"]]], text_auto=True,
                    x=["Predicted: stays", f"Predicted: resigns (risk >= {HIGH_CUT:.0%})"],
                    y=["Actually stayed", "Actually left"],
                    color_continuous_scale="Blues")
    fig.update_layout(coloraxis_showscale=False, title="Confusion matrix",
                      margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig)
with b:
    bands = pd.DataFrame(res["bands"])
    fig = px.bar(bands, x="level", y=bands["actual_rate"] * 100,
                 text=(bands["actual_rate"] * 100).round(0).astype(int).astype(str) + "%",
                 color="level", category_orders={"level": ["High", "Medium", "Low"]},
                 color_discrete_map={"High": "#d62728", "Medium": "#ff9f1c", "Low": "#2ca02c"},
                 labels={"y": "Actually left (%)", "level": "Risk level"})
    fig.update_layout(title="Did the levels match reality?", showlegend=False,
                      margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig)
st.caption("Employees rated High really left far more often than those rated Low.")

st.subheader("Comparison with simpler models")
comp = pd.DataFrame(res["comparison"])
for col in ["accuracy", "precision", "recall"]:
    comp[col] = (comp[col] * 100).round(0).astype(int).astype(str) + "%"
comp["roc_auc"] = comp["roc_auc"].round(2)
comp.columns = ["Model", "ROC-AUC", "Accuracy", "Precision", "Recall"]
st.dataframe(comp, hide_index=True)

st.subheader("What matters most to the model")
imp = pd.DataFrame({"Factor": [LABELS[k] for k in res["importance"]],
                    "Importance (%)": [v * 100 for v in res["importance"].values()]})
imp = imp.head(12).sort_values("Importance (%)")
fig = px.bar(imp, x="Importance (%)", y="Factor", orientation="h")
fig.update_layout(margin=dict(l=10, r=10, t=30, b=10))
st.plotly_chart(fig)

with st.expander("Limitations"):
    st.write(
        "- One public, fictional company dataset (1,470 employees); results may not "
        "apply elsewhere.\n"
        "- The model finds patterns, not causes.\n"
        "- It cannot say when someone will resign.\n"
        "- Gender and marital status are not used.")
