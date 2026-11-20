"""Turn employee rows into the numeric table the model needs."""
import pandas as pd

from backend.config import BINARY, CATEGORIES, NUMERIC


def model_columns() -> list:
    cols = list(NUMERIC) + list(BINARY)
    for name, values in CATEGORIES.items():
        cols += [f"{name}={v}" for v in values]
    return cols


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    X = df[NUMERIC].astype(float).copy()
    for b in BINARY:
        X[b] = (df[b] == "Yes").astype(float)
    for name, values in CATEGORIES.items():
        for v in values:
            X[f"{name}={v}"] = (df[name] == v).astype(float)
    return X[model_columns()]


def original_feature(column: str) -> str:
    """'JobRole=Manager' -> 'JobRole'."""
    return column.split("=")[0]
