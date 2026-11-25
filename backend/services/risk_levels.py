"""Low / Medium / High cut-offs for resignation risk (probability 0-1)."""
import pandas as pd

from backend.config import HIGH_CUT, MEDIUM_CUT

LEVELS = ["High", "Medium", "Low"]
COLORS = {"High": "#d62728", "Medium": "#ff9f1c", "Low": "#2ca02c"}


def level(p: float) -> str:
    if p >= HIGH_CUT:
        return "High"
    if p >= MEDIUM_CUT:
        return "Medium"
    return "Low"


def add_levels(scores: pd.Series) -> pd.Series:
    return scores.apply(level)
