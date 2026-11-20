"""Explain why one employee has a high or low resignation risk.

Method (no extra libraries): for each factor we replace the employee's value
with the value of a 'typical employee' and see how much the risk changes.
  risk drops  -> this factor was pushing the risk UP
  risk rises  -> this factor was holding the risk DOWN
"""
import pandas as pd

from backend.config import FEATURES, LABELS
from backend.services.features import build_features


def explain_employee(art: dict, emp_number: int, row: dict) -> pd.DataFrame:
    model = art["models"][art["fold_of"][int(emp_number)]]
    typical = art["typical"]

    variants = [dict(row)]                       # first row = the real employee
    for f in FEATURES:
        v = dict(row)
        v[f] = typical[f]
        variants.append(v)

    X = build_features(pd.DataFrame(variants))[art["columns"]]
    p = model.predict_proba(X)[:, 1]
    base, others = p[0], p[1:]

    out = pd.DataFrame({
        "Factor": [LABELS[f] for f in FEATURES],
        "This employee": [row[f] for f in FEATURES],
        "Typical employee": [typical[f] for f in FEATURES],
        "Effect on risk (points)": (base - others) * 100,
    })
    return out.sort_values("Effect on risk (points)", ascending=False).reset_index(drop=True)
