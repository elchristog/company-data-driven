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
import modules.bitly as btl
import modules.bitly_clicks_s_networks_whatsapp as btlcsnwsp
import modules.whatsapp_leads as wls
import modules.contracts as c
import modules.bitly_groupal_session as bgs
import modules.groupal_session_assistance as gsa
import projects.enfermera_en_estados_unidos.modules.step_1_program_start as s1ps
import projects.enfermera_en_estados_unidos.modules.step_3_nursing_board_registration as s3nbr
import utils.g_gemini_gestor as ggg








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
        # retrieve metrics ###
        if role_id == 1:
            btl.save_bitly_metrics_bulk(project_name)
        # retrieve metrics ###
        
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            #------ Menu according to each user-----------
            if user_id == 1: #chris
                menu_options = ["Home", "Traffic", "Click bitly Whatsapp", "Whatsapp", "Click bitly Groupal session", "Groupal session", "Remarketing", "Contract", "Contract Remarketing", "Contract Payments", "Web App", "Step1: Inicio del programa", "Step2: Trámite de documentos", "Step3: Inscripción ante la Junta de Enfermería", "Step4: Preparación NCLEX", "Step5: Preparación de inglés", "Step6: Entrevistas de trabajo", "Step7: Visa Screen", "Step8: Trámite NVC", "Step9: Trámite embajada", "Step10: Vida en estados Unidos", 'Users Admin', "IA questions"]
            if user_id == 2: #flaca
                menu_options = ["Home", "Traffic", "IA questions"]
            if user_id == 19: #bingley
                menu_options = ["Home", "Whatsapp", "Groupal session", "Contract", "IA questions"]
            if user_id == 9: #santiago
                menu_options = ["Home", "Whatsapp", "Step3: Inscripción ante la Junta de Enfermería", "IA questions"]
            #------ Menu according to each user-----------

          
            menu = st.sidebar.radio(project_title, menu_options)
            st.write("---") 

        if menu == "Home":
            sub_menu_options=['Tareas', 'Asignar', 'Eliminar']
            sub_menu = st.sidebar.radio('Home options', options = sub_menu_options)
            if sub_menu == "Tareas":
                tap.title_and_paragraph("Tus tareas" + project_icon, "Gestiona tus tareas (Delayed tasks will be labeled as unfulfilled after 5 days of the commitment date)", "h2", 0)
                tasks = t.tasks_visualizer(user_id, project_name, 0)
                t.tips_tasks_ia(tasks, 0)
                st.write("---")
                tap.title_and_paragraph("Cumplimiento de tus tareas" + project_icon, "Visualiza tu crecimiento", "h2", 0)
                t.tasks_achievements(user_id, project_name, 0)
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
                sub_menu_options.extend(['SEO ideation', 'SEO writting', 'Web creation guide', 'Post content prompt'])
            sub_menu = st.sidebar.radio('Traffic options', options = sub_menu_options)
            if sub_menu == "Traffic":
                tap.title_and_paragraph("Trafico" + project_icon, "Seguimiento del trafico y los contenidos generados", "h3", 0)
                seo.days_since_last_content(project_name)
                seotw.get_data_save_to_bq(role_id, project_name, project_url_clean)
                seotw.show_web_metrics(project_name)
                seoty.get_youtube_data_save_to_bq(role_id, project_name, project_url_clean)
                seoty.show_youtube_metrics(project_name)

            if sub_menu == "Content creation guide":
                tap.title_and_paragraph("Creacion de contenido" + project_icon, "Usa un editor externo primero, pasa cada bloque de texto por https://www.text-utils.com/remove-special-characters/ antes de ponerlo aca, con la opcion Keep alphanumeric only", "h3", 0)
                seo.content_creation_guide_effective_communication_storytelling(user_id, project_name)

            if sub_menu == "SEO ideation":
                tap.title_and_paragraph("SEO Ideation" + project_icon, "Generation of 6 long tail ideas based on Keyword research", "h3", 0)
                seo.seo_ideation(project_name, project_keyword, user_id, role_id)

            if sub_menu == "SEO writting":
                tap.title_and_paragraph("SEO writting" + project_icon, "Estimated time: 20 minutes", "h3", 0)
                seo.seo_writing(project_name, user_id, role_id)

            if sub_menu == "Web creation guide":
                tap.title_and_paragraph("Web creation guide" + project_icon, "Sigue estos pasos", "h3", 0)
                seo.web_creation_guide()

            if sub_menu == "Post content prompt":
                tap.title_and_paragraph("Post content prompt" + project_icon, "Sigue estos pasos", "h3", 0)
                seo.post_content_prompt()


        if menu == "Click bitly Whatsapp":
            sub_menu_options=['Clicks', 'Something']
            if role_id == 1:
                sub_menu_options.extend(['Something else'])
            sub_menu = st.sidebar.radio('Click bitly options', options = sub_menu_options)
            if sub_menu == "Clicks":
                tap.title_and_paragraph("Clicks" + project_icon, "Seguimiento de los clicks en los enlaces para chatear", "h3", 0)
                btlcsnwsp.show_bitly_web_youtube_metrics(project_name, 'bit.ly/3R6RbFW', 'bit.ly/45SidF6', 'bit.ly/3R6SrJa')




        if menu == "Whatsapp":
            sub_menu_options=['Leads', 'Add new lead', 'Answer guide']
            if role_id == 1:
                sub_menu_options.extend(['Something else'])
            sub_menu = st.sidebar.radio('Whatsapp options', options = sub_menu_options)
            if sub_menu == "Leads":
                tap.title_and_paragraph("Whatsapp" + project_icon, "Seguimiento de los nuevos leads en whatsapp", "h3", 0)
                wls.whatsapp_leads_show_metrics(project_name, 'bit.ly/3R6RbFW', 'bit.ly/45SidF6')
            if sub_menu == "Add new lead":
                tap.title_and_paragraph("Whatsapp" + project_icon, "Actualizacion de nuevos leads en whatsapp", "h3", 0)
                wls.whatsapp_leads_creation(user_id, project_name)
            if sub_menu == "Answer guide":
                tap.title_and_paragraph("Whatsapp" + project_icon, "Guia de conversacion en whatsapp", "h3", 0)
                st.success("Recordar crear el lead en la plataforma, etiquetar el lead en Whatsapp, guardar el contacto con el nombre de la persona")
                wls.wsp_answer_text(project_id)






        if menu == "Click bitly Groupal session":
            sub_menu_options=['Clicks', 'Something']
            if role_id == 1:
                sub_menu_options.extend(['Something else'])
            sub_menu = st.sidebar.radio('Whatsapp options', options = sub_menu_options)
            if sub_menu == "Clicks":
                tap.title_and_paragraph("Groupal session Bitly clicks" + project_icon, "Seguimiento de los clicks para asistir a la reunion grupal", "h3", 0)
                bgs.bitly_groupal_session_show_metrics(project_name, 'bit.ly/3vtB3Wi')





        if menu == "Groupal session":
            sub_menu_options=['Assistants', 'Add new CRM contact GS', 'Add new assistant', 'Add new absent', 'Contact guide']
            if role_id == 1:
                sub_menu_options.extend(['Development'])
            sub_menu = st.sidebar.radio('Whatsapp options', options = sub_menu_options)
            if sub_menu == "Assistants":
                tap.title_and_paragraph("Groupal session" + project_icon, "Seguimiento de los asistentes a la reunion grupal", "h3", 0)
                gsa.groupal_session_show_metrics(project_name, 'bit.ly/3vtB3Wi')
                tap.title_and_paragraph("Opportunities" + project_icon, "Oportunidades de invitar personas a la sesion grupal", "h3", 0)
                gsa.groupal_session_absents_and_opportunities(project_name)
                tap.title_and_paragraph("Your performance" + project_icon, "Visualiza tu rendimiento", "h3", 0)
                gsa.groupal_session_team_member_performance(user_id, project_name)
            if sub_menu == "Add new CRM contact GS":
                tap.title_and_paragraph("CRM Groupal session" + project_icon, "Creacion de contactos CRM para asistir a la sesion grupal", "h3", 0)
                gsa.add_new_crm_groupal_session_contact(user_id, project_name)
            if sub_menu == "Add new assistant":
                tap.title_and_paragraph("Add new assistant" + project_icon, "Seguimiento de los asistentes a la reunion grupal", "h3", 0)
                gsa.add_new_assistant(user_id, project_name)
            if sub_menu == "Add new absent":
                tap.title_and_paragraph("Add new absent" + project_icon, "Seguimiento de los ausentes en la reunion grupal", "h3", 0)
                gsa.add_new_absent(user_id, project_name)
            if sub_menu == "Contact guide":
                tap.title_and_paragraph("Whatsapp" + project_icon, "Guia de conversacion en whatsapp", "h3", 0)
                gsa.groupal_session_contact_text(project_id)






        if menu == "Contract":
            sub_menu_options=['Contracts', 'Add new CRM contact', 'Add new contract', 'Contact guide']
            if role_id == 1:
                sub_menu_options.extend(['Something else'])
            sub_menu = st.sidebar.radio('Contract options', options = sub_menu_options)
            if sub_menu == "Contracts":
                tap.title_and_paragraph("Contracts" + project_icon, "Seguimiento de los contratos acordados", "h3", 0)
                c.contracts_show_metrics(project_name)
                tap.title_and_paragraph("Contracts CRM opportunities" + project_icon, "Proximos contactos a realizar", "h3", 0)
                c.contracts_crm_show_metrics(project_name)
                tap.title_and_paragraph("Your performance" + project_icon, "Contactos realizados", "h3", 0)
                c.contract_team_member_performance(user_id, project_name)
            if sub_menu == "Add new CRM contact":
                tap.title_and_paragraph("Add new CRM contact" + project_icon, "Seguimiento de los contactos para cerrar nuevos contratos", "h3", 0)
                c.add_new_crm_contact(user_id, project_name)
            if sub_menu == "Add new contract":
                tap.title_and_paragraph("Contracts" + project_icon, "Actualizacion de nuevos contratos y creacion del usuario correspondiente", "h3", 0)
                st.success("Al crear el contrato debe crearse el hashing, el usuario y clave, verificar que si tenga acceso, y crear el pago")
                c.customer_creation(user_id, project_id, project_name)
            if sub_menu == "Contact guide":
                tap.title_and_paragraph("Whatsapp" + project_icon, "Guia de conversacion en whatsapp", "h3", 0)
                c.contract_contact_text(project_id)





        if menu == "Contract Payments":
            sub_menu_options=['Contract Payments', 'Add new payment']
            if role_id == 1:
                sub_menu_options.extend(['Something else'])
            sub_menu = st.sidebar.radio('Contract options', options = sub_menu_options)
            if sub_menu == "Contract Payments":
                tap.title_and_paragraph("Contracts Payments" + project_icon, "Seguimiento de los pagos", "h3", 0)
                c.contract_payments_show_metrics(project_name)
            if sub_menu == "Add new payment":
                tap.title_and_paragraph("Contracts" + project_icon, "Agregar nuevos pagos", "h3", 0)
                c.add_new_contract_payment(user_id, project_id, project_name)



                
        

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






        if menu == "Step1: Inicio del programa":
            sub_menu_options=['User welcome', 'User credentials', 'English program', 'Cv creation', 'Content creation guide']
            if role_id == 1:
                sub_menu_options.extend(['Something'])
            sub_menu = st.sidebar.radio('Traffic options', options = sub_menu_options)
            if sub_menu == "User welcome":
                tap.title_and_paragraph("User welcome" + project_icon, "Bienvenida al usuario y solicitud de datos", "h3", 0)
                s1ps.user_welcome()
            if sub_menu == "User credentials":
                tap.title_and_paragraph("User credentials" + project_icon, "Entrega de usuario y clave", "h3", 0)
                s1ps.platform_user_creation_text_guide()
            if sub_menu == "English program":
                tap.title_and_paragraph("English program" + project_icon, "Entrega servicio de ingles", "h3", 0)
                s1ps.babbel_english_text_guide()
            if sub_menu == "Cv creation":
                tap.title_and_paragraph("Cv creation" + project_icon, "Creacion del resumee", "h3", 0)
                s1ps.cv_creation_guide()






        if menu == "Step3: Inscripción ante la Junta de Enfermería":
            sub_menu_options=['CGFNS guide']
            if role_id == 1:
                sub_menu_options.extend(['Something'])
            sub_menu = st.sidebar.radio('Step3 options', options = sub_menu_options)
            if sub_menu == "CGFNS guide":
                tap.title_and_paragraph("Guia de registro" + project_icon, "Registro ante la junta de enfermeria CGFNS", "h3", 0)
                s3nbr.cgfns_video_guide()


        

        if menu == "Users Admin":
            sub_menu_options=['Create User', 'Update User', 'Hashing']
            sub_menu = st.sidebar.radio('Users Admin options', options = sub_menu_options)
            if sub_menu == "Create User":
                tap.title_and_paragraph("Create User " + project_icon, "Remember at the end hash the password and add to the config", "h3", 0)
                uh.user_creation(user_id, project_id, project_name)
            if sub_menu == "Hashing":
                tap.title_and_paragraph("Hashing " + project_icon, "Write the password and get the hashed version", "h3", 0)
                uh.hashing()



        if menu == "IA questions":
            messages = st.container(height=300)
            prompt = st.chat_input("Say something")                
            if prompt:
                st.session_state.prompt = prompt
                st.session_state.ia_answer = ggg.gemini_knowledge_base_ia(project_name, "​Ahora soy un experto en el proceso de homologacion de enfermeria en estados unidos", prompt)
                st.write(st.session_state.ia_answer)
            if 'prompt' in st.session_state:
                messages.chat_message("user").write(st.session_state.prompt)
                messages.chat_message("assistant").write(f"Echo: {st.session_state.ia_answer}")








    








    
                


    # customer ###################################################################
    if role_id == 6:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu_options = ["Home", "Nclex", "Recursos", "Ofertas de trabajo", "Mis cursos"]
            if user_id == 3: #------ in develop -----------
                menu_options.extend(['Progreso'])
            menu = st.sidebar.radio(project_title, menu_options)
            st.write("---") 

        if menu == "Home":
            sub_menu_options=['Tareas']
            sub_menu = st.sidebar.radio('Home options', options = sub_menu_options)
            if sub_menu == "Tareas":
                tap.title_and_paragraph("Tus tareas" + project_icon, "Gestiona tus tareas (Delayed tasks will be labeled as unfulfilled after 5 days of the commitment date)", "h2", 0)
                tasks = t.tasks_visualizer(user_id, project_name, 0)
                t.tips_tasks_ia(tasks, 0)
                tap.title_and_paragraph("Cumplimiento de tus tareas" + project_icon, "Visualiza tu crecimiento", "h2", 0)
                t.tasks_achievements(user_id, project_name, 0)
            
        if menu == "Nclex":
            sub_menu_options=['Nclex test', 'Logros']
            sub_menu = st.sidebar.radio('Nclex options', options = sub_menu_options)
            if sub_menu == "Nclex test":
                tap.title_and_paragraph("Test diario Nclex" + project_icon, "Cada día un nuevo test", "h2", 0)
                tst.tester(project_name, 'nclex_questions_sample', user_id, 'nclex_attempts', 'https://chat.whatsapp.com/BvsGUAmKDscDXqEDQ74Xf6')
            if sub_menu == "Logros":
                tap.title_and_paragraph("Tu progreso en Nclex" + project_icon, "Evalúa tu progreso en la preparación para el examen", "h2", 0)
                tst.test_achievements(project_name, user_id, 'nclex_attempts')
            
        if menu == "Recursos":
            tap.title_and_paragraph("Tus recursos" + project_icon, "Accede a los recursos habilitados para ti", "h2", 0)
            r.resources(user_id, [':closed_book:', 'Saunders Book', 'https://drive.google.com/uc?export=download&id=1-eLwUvGPgXHpmhcrJzi1nlLs2oZhqgXX'], [':closed_book:','Saunders Strategies','https://drive.google.com/uc?export=download&id=1Bkr-4VGyTUOj9rhw6nqKTOItKQiL4jKU'], [':notebook:','Kaplan Book','https://drive.google.com/uc?export=download&id=1zuJ9HOSMrYWwOH-txKmD8o1asgmfVHAL'], [':ledger:','LaCharity Book','https://drive.google.com/uc?export=download&id=1E8DsdgNqXimVWMeQKD9K82-nx3dHFrfJ'])

        if menu == "Ofertas de trabajo":
            tap.title_and_paragraph("Ofertas de trabajo" + project_icon, "Accede a ofertas de trabajo activas en USA", "h2", 0)
            r.resources(user_id, [':hospital:', 'AdventHealth', 'https://jobs.adventhealth.com/jobs/'], [':health_worker:', 'Piedmont Care', 'https://piedmontcareers.org/search/?filter[category][]=Allied+Health&filter[specialty][]=Behavioral+Health+-+Allied+Health&src=DM-10960&utm_source=Google&utm_medium=Search&utm_campaign=Bayard&gclid=Cj0KCQiAgqGrBhDtARIsAM5s0_nfl0k48Akzmv1LYGQkLGRlwlxaI8xxwgnVrKOMEE1Gr1QuZXjHg5caAoFlEALw_wcB'], [':office:', "St Joseph's Candler", 'https://careers.sjchs.org/search/nursing/jobs'], [':metro:', "Indeed", 'https://www.indeed.com/jobs?q=Nurse+RN&l=United+States'], [':left_luggage:', "LinkedIn", 'https://www.linkedin.com/jobs/rn-jobs/'], [':bellhop_bell:', "Recent positions", 'https://www.google.com/search?q=site%3AICIMS.com+OR+site%3Asmartrecruiters.com+OR+site%3Aworkable.com+OR+site%3Ajobs.lever.co+OR+site%3Aboards.greenhouse.io+OR+site%3Amyworkdayjobs.com+OR+site%3Ajobvite.com+OR+site%3Acareers.google.com+OR+site%3Ajobs.apple.com+OR+site%3Ametacareers.com+(%E2%80%9CNurse%E2%80%9D+OR+%E2%80%9CRegistered+Nurse%22+OR+(%E2%80%9CStaff+Nurse%E2%80%9D)&rlz=1CAKDZI_enUS1065&oq=site%3AICIMS.com+OR+site%3Asmartrecruiters.com+OR+site%3Aworkable.com+OR+site%3Ajobs.lever.co+OR+site%3Aboards.greenhouse.io+OR+site%3Amyworkdayjobs.com+OR+site%3Ajobvite.com+OR+site%3Acareers.google.com+OR+site%3Ajobs.apple.com+OR+site%3Ametacareers.com+(%E2%80%9CNurse%E2%80%9D+OR+%E2%80%9CRegistered+Nurse%22+OR+(%E2%80%9CStaff+Nurse%E2%80%9D)&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg60gEIMTQ2OGowajeoAgCwAgA&sourceid=chrome&ie=UTF-8'])



        if menu == "Mis cursos":
            tap.title_and_paragraph("Tus cursos" + project_icon, "Accede a tus cursos de preparación", "h2", 0)
            r.resources(user_id,  [':computer:', 'Uso de la plataforma', 'https://company-data-driven.thrivecart.com/l/introduccin-a-la-plataforma-de-enfermera-en-estados-unidos/'], [':flag-um:', 'English for the NCLEX-RN', 'https://company-data-driven.thrivecart.com/l/english-for-the-nclex-rn/'], [':female-student:', 'PTE Academic', 'https://company-data-driven.thrivecart.com/l/pte-academic/'], [':classical_building:', 'IELTS Preparation', 'https://company-data-driven.thrivecart.com/l/ielts-preparation/'], [':1234:', 'Next Generation NCLEX', 'https://company-data-driven.thrivecart.com/l/next-generation-nclex/'])

        

        if menu == "Progreso":
            tap.title_and_paragraph("Tus progreso" + project_icon, "Verifica tu progreso en el programa", "h2", 0)
            user_actual_step_id = pp.general_progress(user_id, project_name, 'program_steps', 'user_program_steps_progress')
            psg.program_steps_guide(user_actual_step_id)
