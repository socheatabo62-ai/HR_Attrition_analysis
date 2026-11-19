"""Cached loading of the dataset, the model and the risk scores."""
import streamlit as st

from backend.services import model_service
from backend.services.load_data import load_clean


@st.cache_resource(show_spinner="Preparing the model (first run only, a few seconds)...")
def get_bundle():
    return model_service.load_or_train()


@st.cache_data
def get_employees():
    scores = get_bundle()["scores"]
    df = load_clean().merge(scores, on="EmployeeNumber")
    df["Status"] = df["Left"].map({1: "Left", 0: "Current"})
    df["RiskPct"] = df["Risk"] * 100
    return df


def load_everything():
    """Returns (employees table, model results). Stops the page with a clear
    message if the dataset file is missing."""
    try:
        return get_employees(), get_bundle()["results"]
    except FileNotFoundError as err:
        st.error(str(err))
        st.stop()


def get_artifacts():
    return get_bundle()["artifacts"]
