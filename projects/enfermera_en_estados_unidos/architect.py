import streamlit as st

import modules.title_and_paragraph as tap
import modules.tasks as t
import modules.seo_traffic_web as seotw
import modules.seo_traffic_youtube as seoty
import modules.seo as seo
import utils.users_handling as uh
import modules.tester as tst
import modules.web_app_activity as wap
import modules.resources as r
import modules.program_progress as pp
import projects.enfermera_en_estados_unidos.modules.program_steps_guide as psg



# https://docs.streamlit.io/library/api-reference/layout
# https://docs.streamlit.io/library/api-reference/control-flow/st.form

def architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url, project_url_clean, project_keyword):
    """
    description: The developing interfaces must be approved just for users id 1 and 3
    input:
    output:
    """
    # admin ###################################################################
    if role_id != 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu_options = ["Home", "Traffic", "Click bitly", "Whatsapp", "Trip Wire", "Remarketing", "Web App", "Contract", "Contract Remarketing", "Step1: Inicio del programa", "Step2: Trámite de documentos", "Step3: Inscripción ante la Junta de Enfermería", "Step4: Preparación NCLEX", "Step5: Preparación de inglés", "Step6: Entrevistas de trabajo", "Step7: Visa Screen", "Step8: Trámite NVC", "Step9: Trámite embajada", "Step10: Vida en estados Unidos"]
            if role_id == 1:
                menu_options.extend(['Users Admin'])
            if user_id == 1: #------ in develop -----------
                menu_options.extend(['Developing'])
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

        if menu == "Traffic":
            sub_menu_options=['Traffic', 'Content creation guide']
            if role_id == 1:
                sub_menu_options.extend(['SEO ideation', 'SEO writting', 'Web creation guide'])
            sub_menu = st.sidebar.radio('Traffic options', options = sub_menu_options)
            if sub_menu == "Traffic":
                tap.title_and_paragraph("Trafico" + project_icon, "Seguimiento y mantenimiento de los usuarios", "h3", 0)
                seotw.get_data_save_to_bq(role_id, project_name, project_url_clean)
                seotw.show_web_metrics(project_name)
                seoty.get_youtube_data_save_to_bq(role_id, project_name, project_url_clean)
                seoty.show_youtube_metrics(project_name)

            if sub_menu == "Content creation guide":
                tap.title_and_paragraph("Creacion de contenido" + project_icon, "Seguimiento y mantenimiento de los usuarios", "h3", 0)
                seo.content_creation_guide_effective_communication_storytelling(user_id, project_name)

            if sub_menu == "SEO ideation":
                tap.title_and_paragraph("SEO Ideation" + project_icon, "Generation of 6 long tail ideas based on Keyword research", "h3", 0)
                seo.seo_ideation(project_name, project_keyword, user_id, role_id)

            if sub_menu == "Web creation guide":
                tap.title_and_paragraph("Web creation guide" + project_icon, "Sigue estos pasos", "h3", 0)
                seo.web_creation_guide()

        if menu == "Web App":
            sub_menu_options=["Customer view", 'Nclex test creation', 'Update customer progress']
            if role_id < 4:
                sub_menu_options.extend(['Team view'])
            sub_menu = st.sidebar.radio('Web tool options', options = sub_menu_options)
            if sub_menu == "Customer view":
                tap.title_and_paragraph("Visualize the activity of your customers in the Web App " + project_icon, "Remember not add the letters [A), B), C), D)] in the options", "h3", 0)
                wap.login_activity('customer')
            if sub_menu == "Team view":
                tap.title_and_paragraph("Visualize the activity of your team in the Web App " + project_icon, "Remember not add the letters [A), B), C), D)] in the options", "h3", 0)
                wap.login_activity('team')
            if sub_menu == "Nclex test creation":
                tap.title_and_paragraph("Create a new question in the NCLEX test " + project_icon, "Remember not add the letters [A), B), C), D)] in the options", "h3", 0)
                tst.add_question_to_test(project_name, 'nclex_questions', user_id)
            if sub_menu == "Update customer progress":
                tap.title_and_paragraph("Update customer progress " + project_icon, "Select carefully the actual step", "h3", 0)
                pp.update_customer_progress(user_id, project_id, project_name, 'program_steps', 'user_program_steps_progress')

        if menu == "Users Admin":
            sub_menu_options=['Create User', 'Update User', 'Hashing']
            sub_menu = st.sidebar.radio('Users Admin options', options = sub_menu_options)
            if sub_menu == "Create User":
                tap.title_and_paragraph("Create User " + project_icon, "Remember at the end hash the password and add to the config", "h3", 0)
                uh.user_creation(user_id, project_id, project_name)
            if sub_menu == "Hashing":
                tap.title_and_paragraph("Hashing " + project_icon, "Write the password and get the hashed version", "h3", 0)
                uh.hashing()


        



         
                


    # customer ###################################################################
    if role_id == 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu_options = ["Home", "Nclex", "Recursos", "Ofertas de trabajo"]
            if user_id == 3: #------ in develop -----------
                menu_options.extend(['Progreso'])
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
            sub_menu = st.sidebar.radio('Nclex options', options = sub_menu_options)
            if sub_menu == "Logros":
                tap.title_and_paragraph("Tu progreso en Nclex" + project_icon, "Evalúa tu progreso en la preparación para el examen", "h2", 0)
                tst.test_achievements(project_name, user_id, 'nclex_attempts')
            if sub_menu == "Nclex test":
                tap.title_and_paragraph("Test diario Nclex" + project_icon, "Cada día un nuevo test", "h2", 0)
                tst.tester(project_name, 'nclex_questions_sample', user_id, 'nclex_attempts', 'https://chat.whatsapp.com/BvsGUAmKDscDXqEDQ74Xf6')

        if menu == "Recursos":
            tap.title_and_paragraph("Tus recursos" + project_icon, "Accede a los recursos habilitados para ti", "h2", 0)
            r.resources(user_id, [':closed_book:', 'Saunders Book', 'https://drive.google.com/uc?export=download&id=1-eLwUvGPgXHpmhcrJzi1nlLs2oZhqgXX'], [':closed_book:','Saunders Strategies','https://drive.google.com/uc?export=download&id=1Bkr-4VGyTUOj9rhw6nqKTOItKQiL4jKU'], [':notebook:','Kaplan Book','https://drive.google.com/uc?export=download&id=1zuJ9HOSMrYWwOH-txKmD8o1asgmfVHAL'], [':ledger:','LaCharity Book','https://drive.google.com/uc?export=download&id=1E8DsdgNqXimVWMeQKD9K82-nx3dHFrfJ'])

        if menu == "Ofertas de trabajo":
            tap.title_and_paragraph("Ofertas de trabajo" + project_icon, "Accede a ofertas de trabajo activas en USA", "h2", 0)
            r.resources(user_id, [':hospital:', 'AdventHealth', 'https://jobs.adventhealth.com/jobs/'], [':health_worker:', 'Piedmont Care', 'https://piedmontcareers.org/search/?filter[category][]=Allied+Health&filter[specialty][]=Behavioral+Health+-+Allied+Health&src=DM-10960&utm_source=Google&utm_medium=Search&utm_campaign=Bayard&gclid=Cj0KCQiAgqGrBhDtARIsAM5s0_nfl0k48Akzmv1LYGQkLGRlwlxaI8xxwgnVrKOMEE1Gr1QuZXjHg5caAoFlEALw_wcB'], [':office:', "St Joseph's Candler", 'https://careers.sjchs.org/search/nursing/jobs'], [':metro:', "Indeed", 'https://www.indeed.com/jobs?q=Nurse+RN&l=United+States&from=mobRdr&utm_source=%2Fm%2F&utm_medium=redir&utm_campaign=dt&vjk=109125595fdaa081'])

        if menu == "Progreso":
            tap.title_and_paragraph("Tus progreso" + project_icon, "Verifica tu progreso en el programa", "h2", 0)
            user_actual_step_id = pp.general_progress(user_id, project_name, 'program_steps', 'user_program_steps_progress')
            psg.program_steps_guide(user_actual_step_id)
