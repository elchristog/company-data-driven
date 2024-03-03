import streamlit as st
import os

import projects.enfermera_en_estados_unidos.architect as eeeu_architect

def project_handler(user_id, project_id, role_id, role_name, project_name, project_title, project_icon, project_logo_url, project_url_clean, project_keyword):
    os.write(1, '🥏 Executing project_handler \n'.encode('utf-8'))
    if project_id == 1:
        os.write(1, '- project_handler: enfermera_en_estados_unidos \n'.encode('utf-8'))
        eeeu_architect.architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url, project_url_clean, project_keyword)
