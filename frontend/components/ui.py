import streamlit as st

def setup(title, icon):
    corporate_blue_css = """
    <style>
    .stApp {
        background-color: #E8F0FE !important; 
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #1A2B4C !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #D0E0F0;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #D0E0F0 !important;
        box-shadow: 0 4px 12px rgba(26, 43, 76, 0.08) !important;
        padding: 20px;
    }
    .stButton>button {
        background-color: #1A73E8 !important; 
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0D47A1 !important;
        box-shadow: 0 4px 8px rgba(26, 115, 232, 0.3) !important;
    }
    [data-testid="stMetricValue"] {
        color: #1A73E8 !important; 
        font-weight: 800 !important;
    }
    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border-radius: 8px;
        border: 1px solid #D0E0F0;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    </style>
    """
    st.markdown(corporate_blue_css, unsafe_allow_html=True)

def pick_employee(df, prefix=""):
    if df.empty:
        st.warning("No employees available.")
        st.stop()
    emp_list = df["EmployeeNumber"].unique()
    selected = st.selectbox("Select an Employee Number", emp_list, key=f"{prefix}_emp_select")
    row = df[df["EmployeeNumber"] == selected].iloc[0]
    return selected, row