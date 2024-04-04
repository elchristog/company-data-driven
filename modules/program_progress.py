import streamlit as st
import datetime
import time
import os

import utils.user_credentials as uc


def general_progress(user_id, project_name, program_steps_table_tame, program_steps_user_progress_table_name):
    st.header('Program progress and steps')
    user_progress_table = uc.run_query_15_m(f"SELECT ps.id, ps.name, ps.description, COALESCE(CAST(upsp_user.creation_date AS STRING),'pending') AS starting_date FROM `company-data-driven.{project_name}.{program_steps_table_tame}` AS ps LEFT JOIN (SELECT  * FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id}) AS upsp_user ON ps.id = upsp_user.program_step_id  ORDER BY ps.id;")
    user_actual_step= uc.run_query_15_m(f"SELECT program_step_id, creation_date, DATE_DIFF(CURRENT_DATE(), creation_date, DAY) AS days_since_achievemen FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` WHERE user_id = {user_id} AND program_step_id = (SELECT MAX(program_step_id) AS actual_step FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id});")

    if len(user_progress_table) > 0:
        progress = user_actual_step[0].get("program_step_id")/len(user_progress_table)
        if progress >= 0.9 or user_actual_step[0].get("days_since_achievemen") < 5:
            st.balloons()
            st.success("You are the best!", icon = "🥳")
        st.progress(5, text = f"Global progress: **{round(100*progress)}%**")
        st.table(user_progress_table)
        return user_actual_step[0].get("program_step_id") 





def customer_success_add_program_step_execution():
    os.write(1, '🥏 Executing customer_success_add_program_step_execution \n'.encode('utf-8'))
    if 'customer_success_add_program_step_selected_program_step' in st.session_state:
        os.write(1, '- customer_success_add_program_step_execution: Saving step\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.customer_success_add_program_step_project_name}.program_steps` SET order_number = order_number + 1 WHERE order_number > {st.session_state.customer_success_add_program_step_selected_step_order_number}")
        
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.customer_success_add_program_step_project_name}.program_steps` (order_number, creation_date, name, description, id, creator_user_id, know_how, tasks, texts, days_to_complete_tasks) VALUES ({st.session_state.customer_success_add_program_step_selected_step_order_number} + 1, CURRENT_DATE(), '{st.session_state.customer_success_add_program_step_step_name}', '{st.session_state.customer_success_add_program_step_step_description}', GENERATE_UUID(), {st.session_state.customer_success_add_program_step_user_id}, '{st.session_state.customer_success_add_program_step_know_how}', '{st.session_state.customer_success_add_program_step_tasks_array}', '{st.session_state.customer_success_add_program_step_chat_texts}', {st.session_state.customer_success_add_program_step_days_to_complete_tasks})")
        st.toast("Info saved!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.customer_success_add_program_step_user_id
        del st.session_state.customer_success_add_program_step_project_name
        del st.session_state.customer_success_add_program_step_step_name
        del st.session_state.customer_success_add_program_step_selected_program_step
        del st.session_state.customer_success_add_program_step_step_description
        del st.session_state.customer_success_add_program_step_know_how 
        del st.session_state.customer_success_add_program_step_tasks_array 
        del st.session_state.customer_success_add_program_step_chat_texts 
        del st.session_state.customer_success_add_program_step_selected_step_id 
        del st.session_state.customer_success_add_program_step_selected_step_order_number 
        del st.session_state.customer_success_add_program_step_days_to_complete_tasks 
        
        
        


def customer_success_add_program_step(user_id, project_name):
    os.write(1, '🥏 Executing customer_success_add_program_step \n'.encode('utf-8'))
    os.write(1, '- customer_success_add_program_step: Showing form \n'.encode('utf-8'))
  
    rows_program_steps = uc.run_query_half_day(f"SELECT order_number, name, id FROM `company-data-driven.{project_name}.program_steps` ORDER BY order_number;")
    step_order_numbers = []
    step_names = []
    step_ids = []
    for row in rows_program_steps:
        step_names.append(row.get('name'))
        step_ids.append(row.get('id'))
        step_order_numbers.append(row.get('order_number'))
    selected_program_step = st.selectbox(
            label = "Add after wich step?",
            options = step_names,
            index = None,
            key= "customer_success_add_program_step_selected_program_step"
        )
    step_name = st.text_input('Step name', placeholder = 'Confirmacion de la activacion de Babbel', key = 'customer_success_add_program_step_step_name')
    step_description = st.text_input('Step description', placeholder = 'Este paso requiere que el usuario confirme haber completado la creacion de su cuenta en los 30 dias que se requieren para no perder la compra', key = 'customer_success_add_program_step_step_description')
    know_how = st.text_input('Know how youtube video link', placeholder = 'https://...', key = 'customer_success_add_program_step_know_how', help = 'Video explicando como se ejecuta este paso')
    tasks_array = st.text_input('Tasks (NO QUOTES, just comma)', key = 'customer_success_add_program_step_tasks_array', help = "Deben ser las tareas SIN NINGUNA COMILLA solo separando por coma", placeholder = "Confirmar la activacion de Babbel antes de 30 dias, segunda tarea")
    chat_texts = st.text_input('Chat texts', key = 'customer_success_add_program_step_chat_texts', help = "Lo que se le debe escribir a la persona", placeholder = "Te recomiendo cuando crees la cuenta de Babbel y actives el producto nos avises por este medio, muchas gracias!")
    days_to_complete_tasks = st.number_input('Days to complete tasks', key = 'customer_success_add_program_step_days_to_complete_tasks', min_value = 5, max_value = 90, step = 5, help = "Dias en que la persona debe cumplir sus tareas")
    
    

    if selected_program_step is not None:
        st.session_state.customer_success_add_program_step_user_id = user_id
        st.session_state.customer_success_add_program_step_project_name = project_name
        st.session_state.customer_success_add_program_step_selected_step_id = step_ids[step_names.index(selected_program_step)]
        st.session_state.customer_success_add_program_step_selected_step_order_number = step_order_numbers[step_names.index(selected_program_step)]
        customer_success_add_program_step_button = st.button("Add step", on_click = customer_success_add_program_step_execution)
        







def customer_success_crm_add_contact_execution():
    os.write(1, '🥏 Executing posting_posts_execution \n'.encode('utf-8'))
    if 'posting_posts_selected_idea' in st.session_state:
        os.write(1, '- posting_posts_execution: Saving posted idea\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.posting_posts_project_name}.daily_post_creation` SET posted = 1, posted_date = CURRENT_DATE(), poster_user_id = {st.session_state.posting_posts_user_id} WHERE id 0 '{st.session_state.posting_posts_selected_idea_id}'")
        st.toast("Info saved!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.posting_posts_user_id
        del st.session_state.posting_posts_project_name
        del st.session_state.posting_posts_post_idea
        del st.session_state.posting_posts_selected_idea_id 


def customer_success_crm_add_contact(user_id, project_name):
    os.write(1, '🥏 Executing customer_success_crm_add_contact \n'.encode('utf-8'))
    os.write(1, '- customer_success_crm_add_contact: Showing form \n'.encode('utf-8'))
  
    rows = uc.run_query_half_day(f"SELECT u.username, u.id, c.id as contract_id FROM `company-data-driven.{project_name}.contracts` AS c INNER JOIN `company-data-driven.global.users` AS u ON u.id = c.user_id;")
    usernames = []
    contract_ids = []
    user_ids = []
    for row in rows:
        usernames.append(row.get('username'))
        contract_ids.append(row.get('contract_id'))
        user_ids.append(row.get('id'))
    selected_username = st.selectbox(
            label = "Select the username",
            options = usernames,
            index = None,
            key= "customer_success_crm_add_contact_selected_username"
        )
    if selected_username is not None:
        st.session_state.customer_success_crm_add_contact_selected_user_id = user_ids[usernames.index(selected_username)]
        active_tasks = uc.run_query_2_m(f"SELECT description, commit_finish_date, status  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {st.session_state.customer_success_crm_add_contact_selected_user_id} AND status IN ('to_start', 'on_execution', 'delayed') ORDER BY commit_finish_date ASC;") #finished, canceled, unfulfilled
        finished_tasks = uc.run_query_2_m(f"SELECT description, commit_finish_date, status  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {st.session_state.customer_success_crm_add_contact_selected_user_id} AND status = 'finished' ORDER BY commit_finish_date DESC LIMIT 5;") #finished, canceled, unfulfilled
        unfulfilled_tasks = uc.run_query_2_m(f"SELECT description, commit_finish_date, status  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {st.session_state.customer_success_crm_add_contact_selected_user_id} AND status = 'unfulfilled' ORDER BY commit_finish_date DESC LIMIT 5;") #finished, canceled, unfulfilled
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("#### Active tasks")
            st.table(active_tasks)
        with col2:
            st.write("#### Finished tasks (Last 5)")
            st.table(finished_tasks)
        with col3:
            st.write("#### Unfulfilled tasks (Last 5)")
            st.table(unfulfilled_tasks)



    rows_program_steps = uc.run_query_half_day(f"SELECT name, id, know_how FROM `company-data-driven.{project_name}.program_steps` ORDER BY order_number;")
    step_names = []
    step_ids = []
    know_hows = []
    for row in rows_program_steps:
        step_names.append(row.get('name'))
        step_ids.append(row.get('id'))
        know_hows.append(row.get('know_how'))
    selected_program_step = st.selectbox(
            label = "Select the step",
            options = step_names,
            index = None,
            key= "customer_success_crm_add_contact_selected_program_step"
        )
    if selected_program_step is not None:
        st.session_state.customer_success_crm_add_contact_step_id = step_ids[step_names.index(selected_program_step)]
        st.session_state.customer_success_crm_add_contact_know_how = know_hows[step_names.index(selected_program_step)]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("#### Step Know How")
            st.write(st.session_state.customer_success_crm_add_contact_know_how)
            st.video(st.session_state.customer_success_crm_add_contact_know_how)


    date_contact = st.date_input("Select the contact date", key = "customer_success_crm_add_contact_date_contact")
    contact_description = st.text_input('Contact description', placeholder = 'Se contacta a Alejandra entregando las credenciales de CGFNS', key = 'customer_success_crm_add_contact_contact_description')
    commitment_score = st.number_input('User Commitment score', key = 'customer_success_crm_add_contact_commitment_score', min_value = 0, max_value = 10, step = 1, help = "0: El usuario no tiene compromiso. 10: El usuario esta absolutamente comprometido")
    



    # if selected_idea is not None:
    #     st.session_state.posting_posts_user_id = user_id
    #     st.session_state.posting_posts_project_name = project_name
    #     st.session_state.posting_posts_selected_idea_id = ids[ideas.index(selected_idea)]
    #     posting_posts_button = st.button("Post published", on_click = posting_posts_execution)
        
    # if 'post_redaction_generation' in st.session_state:
    #             st.write("---")
    #             st.write(st.session_state.post_redaction_generation + " #enfermeraenestadosunidos #enfermeriaenusa #enfermerosenestadosunidos")


    
