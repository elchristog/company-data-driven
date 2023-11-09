import streamlit as st
import datetime

def general_progress():
    st.header('Program progress and steps')
    st.progress(5, text = f"Global progress: **{5}%**")