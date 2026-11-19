"""Small helpers shared by every page."""
import streamlit as st


def setup(title: str, icon: str = "👥"):
    """Must be the first Streamlit call on each page."""
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")


def employee_options(df):
    """Employee numbers sorted from highest risk, plus readable labels."""
    d = df.sort_values("Risk", ascending=False)
    labels = {int(r.EmployeeNumber):
              f"#{int(r.EmployeeNumber)}  |  {r.JobRole}  |  {r.RiskLevel} ({r.Risk:.0%})"
              for r in d.itertuples()}
    return list(labels), labels


def pick_employee(df, key: str):
    """Drop-down to choose one employee. Returns (employee number, row)."""
    include_left = st.checkbox("Include employees who already left", value=False,
                               key=f"{key}_incl")
    pool = df if include_left else df[df["Status"] == "Current"]
    ids, labels = employee_options(pool)
    emp = st.selectbox("Choose an employee (type a number to search)", ids,
                       format_func=lambda n: labels[n], key=f"{key}_emp")
    return emp, df[df["EmployeeNumber"] == emp].iloc[0]
