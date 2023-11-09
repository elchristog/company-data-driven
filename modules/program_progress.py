import streamlit as st
import datetime

def general_progress():
    st.header('Program progress and steps')
    st.progress(10, text = f"Progreso general: **{10}%**")