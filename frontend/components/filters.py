"""Sidebar filters shared by the pages."""
import streamlit as st

GROUPS = ["All employees", "Current employees", "Employees who left"]


def sidebar_filters(df, key: str, default_group: str = "All employees"):
    st.sidebar.header("Filters")
    group = st.sidebar.radio("Employee group", GROUPS,
                             index=GROUPS.index(default_group), key=f"{key}_group")
    depts = st.sidebar.multiselect("Department", sorted(df["Department"].unique()),
                                   key=f"{key}_dept", placeholder="All departments")
    roles = st.sidebar.multiselect("Job role", sorted(df["JobRole"].unique()),
                                   key=f"{key}_role", placeholder="All job roles")
    overtime = st.sidebar.radio("Overtime", ["All", "Yes", "No"], key=f"{key}_ot")
    lo, hi = int(df["Age"].min()), int(df["Age"].max())
    age = st.sidebar.slider("Age", lo, hi, (lo, hi), key=f"{key}_age")

    f = df
    if group == "Current employees":
        f = f[f["Status"] == "Current"]
    elif group == "Employees who left":
        f = f[f["Status"] == "Left"]
    if depts:
        f = f[f["Department"].isin(depts)]
    if roles:
        f = f[f["JobRole"].isin(roles)]
    if overtime != "All":
        f = f[f["OverTime"] == overtime]
    f = f[(f["Age"] >= age[0]) & (f["Age"] <= age[1])]

    st.sidebar.caption(f"Showing {len(f):,} of {len(df):,} employees")
    return f
