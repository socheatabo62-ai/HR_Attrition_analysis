import streamlit as st
# COLOR THEME

COLORS = {
    "primary": "#EF2EDB",
    "dark": "#172554",
    "background": "#F5F7FC",
    "text": "#1E293B",
    "muted": "#5284CA",
    "green": "#16A34A",
    "red": "#DC2626",
    "purple": "#7C3AED",
}
# PAGE CONFIGURATION

def setup(title: str, icon: str = "👥"):
    """Configure page settings and dashboard styling."""

    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background-color: #F5F7FC;
        }

        /* Main content */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #172554 !important;
            font-weight: 700 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #EEF3FF;
            border-right: 1px solid #DBEAFE;
        }

        /* Sidebar text */
        [data-testid="stSidebar"] p {
            color: #334155;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background: white;
            padding: 18px;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        /* Selectbox */
        div[data-baseweb="select"] > div {
            border-radius: 9px;
            border-color: #CBD5E1;
            background-color: white;
        }

        /* Buttons */
        .stButton > button {
            background-color: #2563EB;
            color: white;
            border-radius: 9px;
            border: none;
            font-weight: 600;
        }

        .stButton > button:hover {
            background-color: #1D4ED8;
            color: white;
        }

        /* Checkbox */
        .stCheckbox label {
            color: #334155;
            font-weight: 500;
        }

        /* Containers */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px;
            border-color: #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)


# ==============================
# EMPLOYEE OPTIONS
# ==============================

def employee_options(df):
    """Return employee IDs sorted by highest risk."""

    d = df.sort_values("Risk", ascending=False)

    labels = {
        int(r.EmployeeNumber):
        f"Employee #{int(r.EmployeeNumber)}  |  "
        f"{r.JobRole}  |  "
        f"{r.RiskLevel} ({r.Risk:.1%})"
        for r in d.itertuples()
    }

    return list(labels), labels


# ==============================
# EMPLOYEE SELECTION
# ==============================

def pick_employee(df, key: str):
    """Display employee selection and return employee number and row."""

    st.markdown("""
        <div style="margin-bottom: 12px;">
            <h3 style="color:#172554; margin-bottom:4px;">
                👤 Employee Selection
            </h3>
            <p style="color:#64748B; font-size:14px;">
                Select an employee to explore their attrition risk profile.
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        include_left = st.checkbox(
            "Include employees who already left",
            value=False,
            key=f"{key}_incl"
        )

        # Filter employee status
        pool = (
            df if include_left
            else df[df["Status"] == "Current"]
        )

        # Prepare employee dropdown
        ids, labels = employee_options(pool)

        if not ids:
            st.warning("No employees available for selection.")
            return None, None

        emp = st.selectbox(
            "Choose an employee",
            ids,
            format_func=lambda n: labels[n],
            key=f"{key}_emp",
            help="Employees are sorted from highest risk to lowest risk."
        )

    # Return selected employee
    employee = df[
        df["EmployeeNumber"] == emp
    ].iloc[0]

    return emp, employee
