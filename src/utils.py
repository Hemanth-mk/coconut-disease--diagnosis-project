import streamlit as st

def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

def login_user(username):
    st.session_state.logged_in = True
    st.session_state.username = username

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = None
