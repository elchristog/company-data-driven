import streamlit as st
import modules.title_and_paragraph as tap
import modules.tasks as t

# https://docs.streamlit.io/library/api-reference/layout

def architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url):
    # admin
    if role_id != 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu = st.sidebar.radio(project_title, ["Home", "Trafico y SEO", "Whatsapp", "Trip Wire"])
            st.write("---") 

        if menu == "Home":
            tab1, tab2, tab3 = st.tabs(["Tareas", "Asignar", "Eliminar"])
            with tab1:
                tap.title_and_paragraph(project_title + project_icon, "Seguimiento y mantenimiento de los usuarios", "h1", 0)
                tap.title_and_paragraph("Tus tareas", "Gestiona tus tareas (delayed tasks will be labeled as unfulfilled after 5 days of the commitment date)", "h2", 0)
                with st.expander("Administrar tareas"):
                    tasks = t.tasks_visualizer(user_id, project_name, 0)
                    t.tips_tasks_ia(tasks, 0)
                tap.title_and_paragraph("Tus logros", "Visualiza tu crecimiento", "h3", 0)
                t.tasks_achievements(user_id, project_name, tasks, 1)
            with tab2:
                tap.title_and_paragraph("Asignar tareas", "Asigna tareas a tu equipo", "h3", 0)
                t.task_creation(user_id, role_id, project_id, project_name, 1)
            with tab3:
                tap.title_and_paragraph("Eliminar tareas", "Elimina tareas de tu equipo", "h3", 0)
                t.task_deletion(user_id, role_id, project_id, project_name, 1)







    # customer
    if role_id == 6:
        pass