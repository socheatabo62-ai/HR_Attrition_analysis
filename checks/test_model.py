"""Checks on the model, risk levels, explanation and what-if."""
import pytest

from backend.config import FEATURES, HIGH_CUT, MEDIUM_CUT
from backend.services.explain import explain_employee
from backend.services.load_data import load_clean
from backend.services.model_service import predict_employee, train
from backend.services.risk_levels import level


@pytest.fixture(scope="module")
def bundle():
    return train(save=False)


def test_levels():
    assert level(HIGH_CUT) == "High"
    assert level(MEDIUM_CUT) == "Medium"
    assert level(MEDIUM_CUT - 0.01) == "Low"


def test_model_beats_guessing(bundle):
    r = bundle["results"]
    assert r["roc_auc"] > 0.75
    assert r["recall"] > 0.3


def test_scores_are_probabilities_for_every_employee(bundle):
    s = bundle["scores"]
    assert len(s) == 1470
    assert s["Risk"].between(0, 1).all()


def test_high_risk_group_leaves_more_than_low(bundle):
    b = {x["level"]: x["actual_rate"] for x in bundle["results"]["bands"]}
    assert b["High"] > b["Medium"] > b["Low"]


def test_explanation_and_whatif(bundle):
    art, scores = bundle["artifacts"], bundle["scores"]
    df = load_clean().set_index("EmployeeNumber")
    emp = int(scores.sort_values("Risk").iloc[-1]["EmployeeNumber"])
    row = df.loc[emp].to_dict()
    row["EmployeeNumber"] = emp
    risk = predict_employee(art, emp, row)
    assert risk == pytest.approx(scores.set_index("EmployeeNumber").loc[emp, "Risk"])
    ex = explain_employee(art, emp, row)
    assert list(ex["Factor"]) and len(ex) == len(FEATURES)
    changed = dict(row, OverTime="No" if row["OverTime"] == "Yes" else "Yes")
    assert 0 <= predict_employee(art, emp, changed) <= 1
