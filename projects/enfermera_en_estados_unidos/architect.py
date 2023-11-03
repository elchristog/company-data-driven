import streamlit as st

import modules.title_and_paragraph as tap
import modules.tasks as t
import modules.seo_traffic as seot
import utils.users_handling as uh
import modules.tester as tst

# https://docs.streamlit.io/library/api-reference/layout
# https://docs.streamlit.io/library/api-reference/control-flow/st.form

def architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url):
    # admin
    if role_id != 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu_options = ["Home", "Traffic and SEO", "Click bitly", "Whatsapp", "Trip Wire", "Remarketing", "Web tool", "Contract", "Contract Remarketing", "Step1", "Step2", "Customer view", "Team view"]
            if role_id == 1:
                menu_options.extend(['Users Admin'])
            menu = st.sidebar.radio(project_title, menu_options)
            st.write("---") 

        if menu == "Home":
            sub_menu_options=['Logros', 'Tareas', 'Asignar', 'Eliminar']
            sub_menu = st.sidebar.radio('Home options', options = sub_menu_options)
            if sub_menu == "Logros":
                tap.title_and_paragraph("Cumplimiento de tus tareas" + project_icon, "Visualiza tu crecimiento", "h2", 0)
                t.tasks_achievements(user_id, project_name, 0)
            if sub_menu == "Tareas":
                tap.title_and_paragraph("Tus tareas" + project_icon, "Gestiona tus tareas (Delayed tasks will be labeled as unfulfilled after 5 days of the commitment date)", "h3", 0)
                tasks = t.tasks_visualizer(user_id, project_name, 0)
                t.tips_tasks_ia(tasks, 0)
            if sub_menu == "Asignar":
                tap.title_and_paragraph("Asignar tareas", "Asigna tareas a tu equipo", "h3", 0)
                t.task_creation(user_id, role_id, project_id, project_name, 0)
            if sub_menu == "Eliminar":
                tap.title_and_paragraph("Eliminar tareas", "Elimina tareas de tu equipo", "h3", 0)
                t.task_deletion(user_id, role_id, project_id, project_name, 0)
            if sub_menu == "Hashing":
                tap.title_and_paragraph("Hashing passwords", "se asi asi y asi", "h3", 0)

        if menu == "Traffic and SEO":
            tab1, tab2, tab3 = st.tabs(["Traffic", "SEO", "Eliminar"])
            with tab1:
                tap.title_and_paragraph(project_title + project_icon, "Seguimiento y mantenimiento de los usuarios", "h1", 0)
                seot.createPage()

        if menu == "Web tool":
            sub_menu_options=['Nclex test creation']
            sub_menu = st.sidebar.radio('Web tool options', options = sub_menu_options)
            if sub_menu == "Nclex test creation":
                tap.title_and_paragraph("Creeate a new question in the NCLEX test " + project_icon, "Remember at the end hash the password and add to the config", "h3", 0)
                tst.add_question_to_test(project_name, 'nclex_questions', user_id)

        if menu == "Users Admin":
            sub_menu_options=['Create User', 'Update User', 'Hashing']
            sub_menu = st.sidebar.radio('Users Admin options', options = sub_menu_options)
            if sub_menu == "Create User":
                tap.title_and_paragraph("Create User " + project_icon, "Remember at the end hash the password and add to the config", "h3", 0)
                uh.user_creation(user_id, project_id, project_name)
            if sub_menu == "Hashing":
                tap.title_and_paragraph("Hashing " + project_icon, "Write the password and get the hashed version", "h3", 0)
                uh.hashing()
                


    # customer
    if role_id == 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu_options = ["Home", "Nclex"]
            menu = st.sidebar.radio(project_title, menu_options)
            st.write("---") 

        if menu == "Home":
            sub_menu_options=['Logros', 'Tareas']
            sub_menu = st.sidebar.radio('Home options', options = sub_menu_options)
            if sub_menu == "Logros":
                tap.title_and_paragraph("Cumplimiento de tus tareas" + project_icon, "Visualiza tu crecimiento", "h2", 0)
                t.tasks_achievements(user_id, project_name, 0)
            if sub_menu == "Tareas":
                tap.title_and_paragraph("Tus tareas" + project_icon, "Gestiona tus tareas (Delayed tasks will be labeled as unfulfilled after 5 days of the commitment date)", "h3", 0)
                tasks = t.tasks_visualizer(user_id, project_name, 0)
                t.tips_tasks_ia(tasks, 0)
            
        if menu == "Nclex":
            sub_menu_options=['Logros', 'Nclex test']
            sub_menu = st.sidebar.radio('Home options', options = sub_menu_options)
            if sub_menu == "Logros":
                tap.title_and_paragraph("Nclex" + project_icon, "Gestiona tus tareas (Delayed tasks will be labeled as unfulfilled after 5 days of the commitment date)", "h2", 0)
            if sub_menu == "Nclex test":
                tap.title_and_paragraph("Test diario Nclex" + project_icon, "Cada día un nuevo test", "h2", 0)
                tst.tester(project_name, 'nclex_questions_sample', user_id, 'nclex_attempts', 'https://chat.whatsapp.com/BvsGUAmKDscDXqEDQ74Xf6')