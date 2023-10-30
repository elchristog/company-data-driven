import streamlit as st
import modules.title_and_paragraph as tap
import modules.tasks as t

def architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url, client):
    # admin
    if role_id != 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu = st.sidebar.radio(project_title, ["Home", "Trafico y SEO", "Whatsapp", "Trip Wire"])
            st.write("---") 

        if menu == "Home":
            tap.title_and_paragraph(project_title + project_icon, "Seguimiento y mantenimiento de los usuarios", "h1", 1)
            tap.title_and_paragraph("Tus tareas", "Gestiona tus tareas", "h2", 0)
            tasks = t.tasks_visualizer(user_id, project_name, client, 0)
            t.tips_tasks_ia(tasks, 0)
            tap.title_and_paragraph("Tus logros", "Visualiza tu crecimiento", "h3", 0)
            t.tasks_achievements(user_id, project_name, client, 1)




    # customer
    if role_id == 6:
        pass