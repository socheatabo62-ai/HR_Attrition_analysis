"""Train, save, load and use the resignation-risk model.

The model is a Random Forest trained with 5-fold cross-validation.
Every employee is scored by the forest that did NOT see that employee,
so risk scores are honest (not memorised from the answer).
"""
import json

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from backend.config import (CATEGORIES, FEATURES, HIGH_CUT, MEDIUM_CUT, MODEL_FILE,
                            N_FOLDS, NUMERIC, RANDOM_STATE, RESULTS_JSON, RF_PARAMS,
                            SCORES_CSV)
from backend.services.features import build_features, model_columns, original_feature
from backend.services.load_data import load_clean
from backend.services.risk_levels import add_levels


def _typical_values(df: pd.DataFrame) -> dict:
    """The 'typical employee': median for numbers, most common for categories."""
    typ = {c: float(df[c].median()) for c in NUMERIC}
    for c in ["OverTime"] + list(CATEGORIES):
        typ[c] = df[c].mode().iloc[0]
    return typ


def train(save: bool = True) -> dict:
    df = load_clean()
    X = build_features(df)
    y = df["Left"].to_numpy()
    cols = list(X.columns)

    skf = StratifiedKFold(N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    models, fold_of = [], {}
    oof = np.zeros(len(df))
    for k, (tr, te) in enumerate(skf.split(X, y)):
        m = RandomForestClassifier(**RF_PARAMS).fit(X.iloc[tr], y[tr])
        oof[te] = m.predict_proba(X.iloc[te])[:, 1]
        models.append(m)
        for emp in df["EmployeeNumber"].iloc[te]:
            fold_of[int(emp)] = k

    pred = (oof >= HIGH_CUT).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred).ravel()

    # simple comparison models (same cross-validation)
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    lr_p = cross_val_predict(lr, X, y, cv=skf, method="predict_proba")[:, 1]
    lr_pred = (lr_p >= 0.5).astype(int)

    levels = add_levels(pd.Series(oof))
    bands = []
    for lv in ["High", "Medium", "Low"]:
        m_ = levels == lv
        bands.append({"level": lv, "employees": int(m_.sum()),
                      "left": int(y[m_.to_numpy()].sum()),
                      "actual_rate": float(y[m_.to_numpy()].mean()) if m_.any() else 0.0})

    imp = pd.Series(np.mean([m.feature_importances_ for m in models], axis=0), index=cols)
    grouped = imp.groupby([original_feature(c) for c in cols]).sum().sort_values(ascending=False)

    results = {
        "model": "Random Forest (5-fold cross-validated)",
        "employees": int(len(df)), "left": int(y.sum()), "attrition_rate": float(y.mean()),
        "rule": f"Predicted to resign when risk >= {HIGH_CUT:.0%}",
        "roc_auc": float(roc_auc_score(y, oof)),
        "accuracy": float(accuracy_score(y, pred)),
        "precision": float(precision_score(y, pred)),
        "recall": float(recall_score(y, pred)),
        "f1": float(f1_score(y, pred)),
        "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
        "bands": bands,
        "comparison": [
            {"model": "Always predict 'stays' (baseline)", "roc_auc": 0.5,
             "accuracy": float(1 - y.mean()), "precision": 0.0, "recall": 0.0},
            {"model": "Logistic Regression", "roc_auc": float(roc_auc_score(y, lr_p)),
             "accuracy": float(accuracy_score(y, lr_pred)),
             "precision": float(precision_score(y, lr_pred)),
             "recall": float(recall_score(y, lr_pred))},
            {"model": "Random Forest (this dashboard)", "roc_auc": float(roc_auc_score(y, oof)),
             "accuracy": float(accuracy_score(y, pred)),
             "precision": float(precision_score(y, pred)),
             "recall": float(recall_score(y, pred))},
        ],
        "importance": {k: float(v) for k, v in grouped.items()},
        "cutoffs": {"high": HIGH_CUT, "medium": MEDIUM_CUT},
        "sklearn_version": sklearn.__version__,
    }
    scores = pd.DataFrame({"EmployeeNumber": df["EmployeeNumber"], "Risk": oof,
                           "RiskLevel": levels.to_numpy()})
    art = {"models": models, "fold_of": fold_of, "columns": cols,
           "typical": _typical_values(df), "sklearn_version": sklearn.__version__}

    if save:
        MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(art, MODEL_FILE)
        RESULTS_JSON.write_text(json.dumps(results, indent=2))
        scores.to_csv(SCORES_CSV, index=False)
    return {"artifacts": art, "results": results, "scores": scores}


def load_or_train() -> dict:
    """Load the saved model; train it first if missing or made by another version."""
    try:
        art = joblib.load(MODEL_FILE)
        ok = (art.get("sklearn_version") == sklearn.__version__
              and art.get("columns") == model_columns()
              and RESULTS_JSON.exists() and SCORES_CSV.exists())
        if ok:
            return {"artifacts": art,
                    "results": json.loads(RESULTS_JSON.read_text()),
                    "scores": pd.read_csv(SCORES_CSV)}
    except Exception:
        pass
    return train(save=True)


def predict_employee(art: dict, emp_number: int, row: dict) -> float:
    """Risk (0-1) for one employee row, using the forest that never saw them."""
    X = build_features(pd.DataFrame([row]))
    model = art["models"][art["fold_of"][int(emp_number)]]
    return float(model.predict_proba(X[art["columns"]])[0, 1])
