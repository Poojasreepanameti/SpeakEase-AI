"""Speech Analyzer - run with: streamlit run app.py"""
import os
import tempfile

import streamlit as st

import auth
import db
import pipeline
import visualize

st.set_page_config(page_title="Speech Analyzer")
db.init_db()


def login_page():
    st.title("Speech Analyzer")
    tab_login, tab_register = st.tabs(["Login", "Register"])
    with tab_login:
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if auth.login(u, p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid username or password.")
    with tab_register:
        u = st.text_input("Username", key="reg_user")
        p = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            ok, msg = auth.register(u, p)
            (st.success if ok else st.error)(msg)


def analyze_page():
    st.header("Record or Upload Speech")
    recorded = st.audio_input("Record your speech")
    uploaded = st.file_uploader("Or upload an audio file", type=["wav", "mp3", "m4a"])
    source = recorded or uploaded

    if source and st.button("Analyze"):
        suffix = os.path.splitext(source.name)[1] or ".wav"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(source.getvalue())
            path = f.name
        try:
            with st.spinner("Transcribing and analyzing..."):
                result = pipeline.run_pipeline(path)
        finally:
            os.remove(path)
        db.save_session(st.session_state.user, result)
        visualize.show_results(result)


def progress_page():
    st.header("Your Progress")
    visualize.show_progress(db.get_sessions(st.session_state.user))


if "user" not in st.session_state:
    login_page()
else:
    st.sidebar.write(f"Logged in as **{st.session_state.user}**")
    page = st.sidebar.radio("Menu", ["Record & Analyze", "Progress"])
    if st.sidebar.button("Logout"):
        del st.session_state.user
        st.rerun()
    analyze_page() if page == "Record & Analyze" else progress_page()
