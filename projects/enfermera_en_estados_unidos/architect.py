import streamlit as st
import modules.title_and_paragraph as tap

def architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url):
    # admin
    if role_id == 1:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu = st.sidebar.radio(project_title, ["Home", "Trafico y SEO", "Whatsapp", "Trip Wire"])
            st.write("---") 

        if menu == "Home":
            tap.title_and_paragraph(project_title + project_icon, "Seguimiento y mantenimiento de los usuarios")

    # customer
    if role_id == 6:
        pass