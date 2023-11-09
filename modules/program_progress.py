import streamlit as st
import datetime

def general_progress():
    st.success('My douglas')
    st.progress(10, text = f"Progreso general: **{10}%**")