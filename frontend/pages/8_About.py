import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st
from frontend.components.ui import setup

st.set_page_config(page_title="About Me", page_icon="👤", layout="wide")
setup("About Me", "👤")

st.title("👤 About This Project")

st.markdown("""
### What is this project?
This HR Attrition Dashboard is designed to help companies understand **why employees leave** and **predict who might resign next**. By analyzing employee data—such as overtime, income, and job roles—the system uses Machine Learning to calculate a "resignation risk" percentage for every current employee.

Our goal is to help HR teams take proactive steps to support their staff and improve employee retention before it's too late.

### Meet the Developers
**Socheata,KouyEng, Borith**
*Students at Royal University of Phnom Penh*

We built this dashboard to make HR data actionable and easy to understand. If you have any questions or want to connect, feel free to reach out!

📱 **Facebook:** [Your Facebook Name](https://facebook.com/yourprofile)
✈️ **Telegram:** @yourtelegramname
📧 **Email:** your.email@example.com
""")