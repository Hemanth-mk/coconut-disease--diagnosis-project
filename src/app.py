import streamlit as st
from utils import init_session
from login import login_page
from home import home_page

st.set_page_config(page_title="Coconut Disease Detection", layout="wide")

# Initialize session variables
init_session()

# Read page from URL
params = st.query_params
page = params.get("page", "login")

# Force login if not authenticated
if not st.session_state.logged_in:
    page = "login"

# Routing
if page == "login":
    login_page()
elif page == "home":
    home_page()

def logout_user():
    if "logged_in" in st.session_state:
        del st.session_state["logged_in"]
    st.success("Logged out successfully!")
    st.switch_page("login.py")
