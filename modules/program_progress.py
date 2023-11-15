import streamlit as st
import datetime

import utils.user_credentials as uc


def general_progress(user_id, project_name, program_steps_table_tame, program_steps_user_progress_table_name):
    st.header('Program progress and steps')
    user_progress_table = uc.run_query_3_h(f"SELECT ps.id, ps.name, ps.description, COALESCE(CAST(upsp_user.creation_date AS STRING),'pending') AS starting_date FROM `company-data-driven.{project_name}.{program_steps_table_tame}` AS ps LEFT JOIN (SELECT  * FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id}) AS upsp_user ON ps.id = upsp_user.program_step_id  ORDER BY ps.id;")
    user_actual_step= uc.run_query_3_h(f"SELECT program_step_id, creation_date, DATE_DIFF(CURRENT_DATE(), creation_date, DAY) AS days_since_achievemen FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` WHERE user_id = {user_id} AND program_step_id = (SELECT MAX(program_step_id) AS actual_step FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id});")

    progress = user_actual_step[0].get("program_step_id")/len(user_progress_table)
    if progress >= 0.9 or user_actual_step[0].get("days_since_achievemen") < 5:
        st.balloons()
        st.success("You are the best!", icon = "🥳")
    st.progress(5, text = f"Global progress: **{round(100*progress)}%**")
    st.table(user_progress_table)
    return user_actual_step[0].get("program_step_id") 



def update_customer_progress(user_id, project_id, project_name, program_steps_table_tame, program_steps_user_progress_table_name):
    rows_users = uc.run_query_half_day(f"SELECT u.id, u.username FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE u.project_id = {project_id} AND u.status = 'active' AND ra.role_id = 6 ORDER BY u.username ASC;")
    users_ids = []
    users_username = []
    for row in rows_users:
        users_ids.append(row.get('id'))
        users_username.append(row.get('username'))
    selected_username = st.selectbox(
        label = "Select the username",
        options = users_username,
        index = None,
        key= "creation_task_username"
    )
    if selected_username is not None:
        selected_user_id = users_ids[users_username.index(selected_username)]
        user_next_steps = uc.run_query_6_h(f"SELECT ps.id, ps.name FROM `company-data-driven.{project_name}.{program_steps_table_tame}` AS ps WHERE id > (SELECT MAX(upsp.program_step_id) AS actual_step_id FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {selected_user_id}) ORDER BY id ASC;")
        st.table(user_next_steps)
    

    