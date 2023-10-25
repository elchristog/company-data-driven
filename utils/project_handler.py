import streamlit as st
import projects.enfermera_en_estados_unidos.architect as eeeu_architect

def project_handler(user_id, project_id, role_id, role_name):
    # enfermera_en_estados_unidos
    if project_id == 1:
        st.set_page_config(page_title="Company data driven", page_icon="💺", layout="centered", initial_sidebar_state="expanded")

        eeeu_architect.architect(user_id, role_id)
