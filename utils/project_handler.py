import streamlit as st
import projects.enfermera_en_estados_unidos.architect as eeeu_architect

@st.cache_data 
def project_handler(user_id, project_id, role_id, role_name, project_name, project_title, project_icon, project_logo_url, client):
    # enfermera_en_estados_unidos
    if project_id == 1:
        eeeu_architect.architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url, client)
