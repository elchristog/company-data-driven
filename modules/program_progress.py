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
  
    rows = uc.run_query_half_day(f"SELECT u.username, c.id as contract_id FROM `company-data-driven.{project_name}.contracts` AS c INNER JOIN `company-data-driven.global.users` AS u ON u.id = c.user_id;")
    usernames = []
    contract_ids = []
    for row in rows:
        usernames.append(row.get('username'))
        contract_ids.append(row.get('contract_id'))
    selected_username = st.selectbox(
            label = "Select the username",
            options = usernames,
            index = None,
            key= "customer_success_crm_add_contact_usernames"
        )

    # if selected_idea is not None:
    #     st.session_state.posting_posts_user_id = user_id
    #     st.session_state.posting_posts_project_name = project_name
    #     st.session_state.posting_posts_selected_idea_id = ids[ideas.index(selected_idea)]
    #     posting_posts_button = st.button("Post published", on_click = posting_posts_execution)
        
    # if 'post_redaction_generation' in st.session_state:
    #             st.write("---")
    #             st.write(st.session_state.post_redaction_generation + " #enfermeraenestadosunidos #enfermeriaenusa #enfermerosenestadosunidos")


    
