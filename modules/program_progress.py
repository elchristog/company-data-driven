import streamlit as st
import datetime
import time

import utils.user_credentials as uc


def general_progress(user_id, project_name, program_steps_table_tame, program_steps_user_progress_table_name):
    st.header('Program progress and steps')
    user_progress_table = uc.run_query_15_m(f"SELECT ps.id, ps.name, ps.description, COALESCE(CAST(upsp_user.creation_date AS STRING),'pending') AS starting_date FROM `company-data-driven.{project_name}.{program_steps_table_tame}` AS ps LEFT JOIN (SELECT  * FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id}) AS upsp_user ON ps.id = upsp_user.program_step_id  ORDER BY ps.id;")
    user_actual_step= uc.run_query_15_m(f"SELECT program_step_id, creation_date, DATE_DIFF(CURRENT_DATE(), creation_date, DAY) AS days_since_achievemen FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` WHERE user_id = {user_id} AND program_step_id = (SELECT MAX(program_step_id) AS actual_step FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id});")

    progress = user_actual_step[0].get("program_step_id")/len(user_progress_table)
    if progress >= 0.9 or user_actual_step[0].get("days_since_achievemen") < 5:
        st.balloons()
        st.success("You are the best!", icon = "🥳")
    st.progress(5, text = f"Global progress: **{round(100*progress)}%**")
    st.table(user_progress_table)
    return user_actual_step[0].get("program_step_id") 



def update_customer_progress_execution():
    if st.session_state.selected_username is None or st.session_state.selected_new_step is None or st.session_state.confirm_new_step is None:
        st.error("Please fill in completely all of the required fields.")
    else:
        if st.session_state.selected_new_step == st.session_state.confirm_new_step:
            today = datetime.date.today()
            today_str = today.strftime("%Y-%m-%d")
            max_id =  uc.run_query_instant(f"SELECT MAX(id)+1 AS max_id FROM `company-data-driven.{st.session_state.project_name}.{st.session_state.program_steps_user_progress_table_name}`")[0].get('max_id')
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.project_name}.{st.session_state.program_steps_user_progress_table_name}` VALUES({max_id}, '{today_str}', {st.session_state.user_id}, {st.session_state.selected_user_id}, {st.session_state.selected_step_id})")
            st.toast("Updating, please wait", icon = "☺️")
            time.sleep(5)
            uc.run_query_15_m.clear()
            st.toast('Status updated! (' + st.session_state.selected_new_step + ')', icon="😎")
            st.balloons()
            st.rerun()
        else:
            st.toast("Step is not confirmed.")



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
        key= "update_progress_step_username"
    )
    if selected_username is not None:
        selected_user_id = users_ids[users_username.index(selected_username)]
        st.session_state.selected_user_id = selected_user_id
        user_next_steps = uc.run_query_15_m(f"SELECT ps.id, ps.name FROM `company-data-driven.{project_name}.{program_steps_table_tame}` AS ps WHERE id > (SELECT MAX(upsp.program_step_id) AS actual_step_id FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {selected_user_id}) ORDER BY id ASC;")
        if len(user_next_steps) < 1 or len(user_next_steps) is None:
            user_next_steps = uc.run_query_15_m(f"SELECT id, name FROM `company-data-driven.{project_name}.{program_steps_table_tame}` WHERE id = (SELECT MIN(id) FROM `company-data-driven.{project_name}.{program_steps_table_tame}`);")
        step_ids = []
        step_names = []

        for row in user_next_steps:
            step_ids.append(row.get('id'))
            step_names.append(row.get('name'))

        selected_new_step = st.selectbox(
            label = "Select the new step",
            options = step_names,
            index = None,
            key= "new_step_names"
        )
        confirm_new_step = st.selectbox(
            label = "Confirm the new step",
            options = step_names,
            index = None,
            key= "confirm_step_names"
        )
        if selected_new_step is not None and confirm_new_step is not None:
            if selected_new_step == confirm_new_step:
                st.success("Step confirmed!", icon = "🎈")
                selected_step_id = step_ids[step_names.index(selected_new_step)]
                st.session_state.selected_step_id = selected_step_id
            else:
                st.error('Incorrect selection', icon = '🀄')

        st.session_state.user_id = user_id
        st.session_state.project_id = project_id
        st.session_state.project_name = project_name
        st.session_state.program_steps_table_tame = program_steps_table_tame
        st.session_state.program_steps_user_progress_table_name = program_steps_user_progress_table_name
        
        st.session_state.selected_username = selected_username
        st.session_state.selected_new_step = selected_new_step
        st.session_state.confirm_new_step = confirm_new_step
        
        
        
        update_step_button = st.button("Update step", on_click = update_customer_progress_execution)





    
