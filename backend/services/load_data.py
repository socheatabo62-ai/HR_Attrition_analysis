"""Load and clean the IBM HR dataset."""
import pandas as pd

from backend.config import CLEAN_CSV, DROP_COLUMNS, RAW_CSV

AGE_ORDER = ["18-24", "25-34", "35-44", "45-54", "55+"]
INCOME_ORDER = ["< $3k", "$3k-6k", "$6k-9k", "$9k-12k", "$12k+"]
TENURE_ORDER = ["0-1 yrs", "2-3 yrs", "4-5 yrs", "6-10 yrs", "11+ yrs"]


def load_raw() -> pd.DataFrame:
    if not RAW_CSV.exists():
        raise FileNotFoundError(
            f"Dataset not found. Put the IBM CSV here: {RAW_CSV}")
    return pd.read_csv(RAW_CSV)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=DROP_COLUMNS, errors="ignore").copy()
    df["Left"] = (df["Attrition"] == "Yes").astype(int)
    df["AgeGroup"] = pd.cut(df["Age"], [17, 24, 34, 44, 54, 100],
                            labels=AGE_ORDER).astype(str)
    df["IncomeBand"] = pd.cut(df["MonthlyIncome"], [0, 3000, 6000, 9000, 12000, 1e9],
                              labels=INCOME_ORDER).astype(str)
    df["TenureGroup"] = pd.cut(df["YearsAtCompany"], [-1, 1, 3, 5, 10, 100],
                               labels=TENURE_ORDER).astype(str)
    return df


def load_clean() -> pd.DataFrame:
    """Read the raw CSV, clean it, and save a copy in data/cleaned/."""
    df = clean(load_raw())
    try:
        CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV, index=False)
    except OSError:
        pass
    return df
