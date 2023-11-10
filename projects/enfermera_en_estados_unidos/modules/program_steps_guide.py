import streamlit as st

def program_steps_guide(user_actual_step_id):
    if user_actual_step_id == 1:
        st.success("# Inicio del programa")