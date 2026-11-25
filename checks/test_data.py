"""Checks on the dataset and its cleaning."""
from backend.config import CATEGORIES, DROP_COLUMNS, NUMERIC
from backend.services.load_data import load_clean, load_raw


def test_raw_dataset_shape():
    df = load_raw()
    assert df.shape == (1470, 35)
    assert df.isna().sum().sum() == 0


def test_clean_removes_unused_columns_and_adds_helpers():
    df = load_clean()
    for col in DROP_COLUMNS:
        assert col not in df.columns
    assert {"Left", "AgeGroup", "IncomeBand", "TenureGroup"} <= set(df.columns)
    assert df["Left"].sum() == 237


def test_employee_numbers_are_unique():
    assert load_clean()["EmployeeNumber"].is_unique


def test_category_lists_match_the_data():
    df = load_clean()
    for name, values in CATEGORIES.items():
        assert set(df[name].unique()) == set(values), name
    assert set(NUMERIC) <= set(df.columns)
