import streamlit as st

def program_steps_guide(user_actual_step_id):
    if user_actual_step_id == 1:
        st.success(f"### Inicio del programa")
        with st.expander("See explanation"):
            st.write("The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're *guaranteed* to be random.")