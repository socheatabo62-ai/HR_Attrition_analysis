"""Train the resignation-risk model and save it.

Run from the project folder:
    python backend/training/train_model.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.config import MODEL_FILE, RESULTS_JSON, SCORES_CSV  # noqa: E402
from backend.services.model_service import train  # noqa: E402

if __name__ == "__main__":
    out = train(save=True)
    r = out["results"]
    print(f"Model: {r['model']}")
    print(f"Employees: {r['employees']}  (left: {r['left']}, {r['attrition_rate']:.1%})")
    print(f"ROC-AUC:   {r['roc_auc']:.3f}")
    print(f"Accuracy:  {r['accuracy']:.3f}   Precision: {r['precision']:.3f}   "
          f"Recall: {r['recall']:.3f}")
    print(f"Saved: {MODEL_FILE.name}, {RESULTS_JSON.name}, {SCORES_CSV.name} "
          f"in {MODEL_FILE.parent}")
