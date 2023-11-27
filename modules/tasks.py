import streamlit as st
import datetime
import openai
import time

import utils.user_credentials as uc
import utils.chat_gpt_gestor as cgptg

# openai.api_key = st.secrets["OPENAI_API_KEY"]


def tasks_visualizer(user_id, project_name, divider):
    rows = uc.run_query_instant(f"SELECT id, creation_date, description, commit_finish_date, status  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND status IN ('to_start', 'on_execution', 'delayed');") #finished, canceled, unfulfilled
    if len(rows) == 0:
        st.success('You have no pending tasks, very good!', icon="😎")
    else:
        st.table(rows)
        descriptions = []
        ids = []
        actual_statuses = []
        for row in rows:
            description = row.get('description')
            id = row.get('id')
            actual_status = row.get('status')
            if description is not None:
                descriptions.append(description)
                ids.append(id)
                actual_statuses.append(actual_status)
        selected_task = st.selectbox(
            label = "Select one task",
            options = descriptions,
            index = None
        )
        if selected_task is not None:
            selected_task_status = actual_statuses[descriptions.index(selected_task)]
            if selected_task_status == 'on_execution':
                selected_status = st.selectbox(
                label="Select the new status",
                options= ['finished'],
                index=None
            )
            else:
                selected_status = st.selectbox(
                    label="Select the new status",
                    options= ['on_execution'],
                    index=None
                )
            update_task_status_button = st.button("Update status")
            def update_task_status(task_id, new_status, today_str):
                if new_status == 'on_execution':
                    uc.run_query_insert_update(f"UPDATE `company-data-driven.{project_name}.tasks` SET status = '{new_status}', on_execution_date = '{today_str}' WHERE id = {task_id}")
                    st.info("Updating, please wait", icon = "☺️")
                    time.sleep(5)
                if new_status == 'finished':
                    uc.run_query_insert_update(f"UPDATE `company-data-driven.{project_name}.tasks` SET status = '{new_status}', finished_date = '{today_str}' WHERE id = {task_id}")
                    st.balloons()
                    st.info("Updating, please wait", icon = "☺️")
                    time.sleep(5)
            if update_task_status_button:
                today = datetime.date.today()
                today_str = today.strftime("%Y-%m-%d")
                selected_task_id = ids[descriptions.index(selected_task)]
                update_task_status(selected_task_id, selected_status, today_str)
                st.success('Task status updated!', icon="😎")
                st.rerun()
    if divider == 1:
        st.write("---") 
    return rows


def tasks_achievements(user_id, project_name, divider):
    if len(uc.run_query_5_s(f"SELECT id  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND finished_date IS NOT NULL LIMIT 1")) < 1:
        st.success("Your achievements will be available when you finish your first task")
    else:
        year_fulfillment = uc.run_query_5_s(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND canceled_date IS NULL AND  EXTRACT(YEAR FROM commit_finish_date) <= EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM commit_finish_date) <= EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(WEEK FROM commit_finish_date) <= EXTRACT(WEEK FROM CURRENT_DATE()) GROUP BY year ORDER BY year DESC LIMIT 2")
        month_fulfillment = uc.run_query_5_s(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, EXTRACT(MONTH FROM commit_finish_date) AS month, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND canceled_date IS NULL AND  EXTRACT(YEAR FROM commit_finish_date) <= EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM commit_finish_date) <= EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(WEEK FROM commit_finish_date) <= EXTRACT(WEEK FROM CURRENT_DATE()) GROUP BY year, month ORDER BY year DESC, month DESC LIMIT 2")
        week_fulfillment = uc.run_query_5_s(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, EXTRACT(MONTH FROM commit_finish_date) AS month,  EXTRACT(WEEK FROM commit_finish_date) AS week, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND canceled_date IS NULL AND  EXTRACT(YEAR FROM commit_finish_date) <= EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM commit_finish_date) <= EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(WEEK FROM commit_finish_date) <= EXTRACT(WEEK FROM CURRENT_DATE()) GROUP BY year, month, week ORDER BY year DESC, month DESC, week DESC LIMIT 2")

        if len(year_fulfillment) == 0:
            st.warning("Your achievements will be available since the next week", icon = "😵‍💫")
        else:
            col1, col2, col3 = st.columns(3)
            if len(year_fulfillment) == 1:
                col1.metric(label="Year fulfillment (%)", value = round(year_fulfillment[0].get('fulfillment')), delta= 0)
            else:
                col1.metric(label="Year fulfillment (%)", value = round(year_fulfillment[0].get('fulfillment')), delta= round(year_fulfillment[0].get('fulfillment') - year_fulfillment[1].get('fulfillment')))

            if len(month_fulfillment) == 1:
                col2.metric(label="Month fulfillment (%)", value = round(month_fulfillment[0].get('fulfillment')), delta= 0)
            else:
                col2.metric(label="Month fulfillment (%)", value = round(month_fulfillment[0].get('fulfillment')), delta= round(month_fulfillment[0].get('fulfillment') - month_fulfillment[1].get('fulfillment')))

            if len(week_fulfillment) == 1:
                col3.metric(label="Week fulfillment (%)", value = round(week_fulfillment[0].get('fulfillment')), delta= 0)
            else:
                col3.metric(label="Week fulfillment (%)", value = round(week_fulfillment[0].get('fulfillment')), delta= round(week_fulfillment[0].get('fulfillment') - week_fulfillment[1].get('fulfillment')))
            
            st.write("#### Unfulfilled tasks last 3 months")
            unfulfilled_tasks_table = uc.run_query_5_s(f"SELECT t.description, t.commit_finish_date, t.unfulfilled_date  FROM `company-data-driven.{project_name}.tasks` AS t WHERE responsible_user_id = {user_id} AND t.status = 'unfulfilled' AND t.unfulfilled_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AND EXTRACT(YEAR FROM t.creation_date) = EXTRACT(YEAR FROM CURRENT_DATE()) ORDER BY t.unfulfilled_date DESC;")
            if len(unfulfilled_tasks_table) < 1:
                st.success("You are the best!", icon = "😎")
            else:
                st.table(unfulfilled_tasks_table)

            st.write("#### Completed tasks")
            number_tasks_to_show = st.slider('Select number of tasks to be shown', 0, 30, 5)
            completed_tasks_table = uc.run_query_5_s(f"SELECT t.description, t.commit_finish_date, t.finished_date  FROM `company-data-driven.{project_name}.tasks` AS t WHERE responsible_user_id = {user_id} AND t.status = 'finished' ORDER BY t.finished_date DESC, t.id DESC LIMIT {number_tasks_to_show};")
            st.table(completed_tasks_table)
            

    if divider == 1:
        st.write("---") 


def tips_tasks_ia(tasks, divider):
    if len(tasks) > 2:
        ia_tips_button = st.button("🤖 Help me to prioritize!")     
        if ia_tips_button:       
            st.success('Tips to prioritize your tasks using the Eisenhower method:', icon="🤖")            
            answer = cgptg.prompt_ia("You are an expert in project management and tasks priorization", f"Help me to priorize my tasks using the Eisenhower Matrix methodology, find yourself the urgency and importance and give me just the results, solve it and give me the tasks priorized with tips, be specific, return just the list of the task prioritized and one tip of each one, use less than 200 tokens: “ {tasks} ”:", 200)
            st.write(answer)
    if divider == 1:
        st.write("---") 



def task_creation(user_id, role_id, project_id, project_name, divider):
    rows = uc.run_query_half_day(f"SELECT id, name FROM `company-data-driven.global.roles` WHERE id >= {role_id} ORDER BY id DESC;")
    role_ids = []
    role_names = []
    for row in rows:
        role_ids.append(row.get('id'))
        role_names.append(row.get('name'))
    selected_role = st.selectbox(
            label = "Select the user's role",
            options = role_names,
            index = None,
            key= "creation_task_role"
        )
    if selected_role is not None:
        selected_role_id = role_ids[role_names.index(selected_role)]
        rows_users = uc.run_query_half_day(f"SELECT u.id, u.username FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE u.project_id = {project_id} AND u.status = 'active' AND ra.role_id = {selected_role_id} ORDER BY u.username ASC;")
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
            task_input = st.text_input("Describe the task:")
            commitment_date_input = st.date_input("Select a commitment date:")
            create_task_button = st.button("Create task")
            if create_task_button:
                if selected_user_id is None or task_input is None or len(task_input) < 10 or commitment_date_input is None:
                    st.error("Please fill in completely all of the required fields.")
                else:
                    today = datetime.date.today()
                    today_str = today.strftime("%Y-%m-%d")
                    max_id =  uc.run_query_instant(f"SELECT MAX(id)+1 AS max_id FROM `company-data-driven.{project_name}.tasks`")[0].get('max_id')
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.tasks` (id, creation_date, description, responsible_user_id, commit_finish_date, status, task_creator_id) VALUES({max_id}, '{today_str}', '{task_input}', {selected_user_id}, '{commitment_date_input}', 'to_start', {user_id})")
                    st.info("Updating, please wait", icon = "☺️")
                    time.sleep(5)
                    st.success('Task created! (' + task_input + ')', icon="😎")
                    st.balloons()
                    # st.rerun()

    if divider == 1:
        st.write("---") 



def task_deletion(user_id, role_id, project_id, project_name, divider):
    if role_id == 1:
        rows = uc.run_query_half_day(f"SELECT id, name FROM `company-data-driven.global.roles` WHERE id >= {role_id} ORDER BY id DESC;")
    else:
        rows = uc.run_query_half_day(f"SELECT id, name FROM `company-data-driven.global.roles` WHERE id > {role_id} ORDER BY id DESC;")
    role_ids = []
    role_names = []
    for row in rows:
        role_ids.append(row.get('id'))
        role_names.append(row.get('name'))
    selected_role = st.selectbox(
            label = "Select the user's role",
            options = role_names,
            index = None,
            key= "deletion_task_role"
        )
    if selected_role is not None:
        selected_role_id = role_ids[role_names.index(selected_role)]
        rows_users = uc.run_query_half_day(f"SELECT u.id, u.username FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE u.project_id = {project_id} AND u.status = 'active' AND ra.role_id = {selected_role_id} ORDER BY u.username ASC;")
        users_ids = []
        users_username = []
        for row in rows_users:
            users_ids.append(row.get('id'))
            users_username.append(row.get('username'))
        selected_username = st.selectbox(
            label = "Select the username",
            options = users_username,
            index = None,
            key= "deletion_task_username"
        )
        if selected_username is not None:
            selected_user_id = users_ids[users_username.index(selected_username)]
            rows_user_tasks = uc.run_query_instant(f"SELECT id, description FROM `company-data-driven.{project_name}.tasks` WHERE finished_date IS NULL AND canceled_date IS NULL AND responsible_user_id = {selected_user_id} ORDER BY description ASC;")
            user_tasks_ids = []
            user_tasks_descriptions = []
            for row in rows_user_tasks:
                user_tasks_ids.append(row.get('id'))
                user_tasks_descriptions.append(row.get('description'))
            selected_task_description = st.selectbox(
                label = "Select the task to delete",
                options = user_tasks_descriptions,
                index = None,
                key= "deletion_task_description"
            )
            cancel_task_button = st.button("Cancel task")
            if cancel_task_button:
                if selected_task_description is not None:
                    selected_task_id = user_tasks_ids[user_tasks_descriptions.index(selected_task_description)]
                    today = datetime.date.today()
                    today_str = today.strftime("%Y-%m-%d")
                    uc.run_query_insert_update(f"UPDATE `company-data-driven.{project_name}.tasks` SET status = 'canceled', canceled_date = '{today_str}', task_cancelator_id = {user_id} WHERE id = {selected_task_id};")
                    st.info("Updating, please wait", icon = "☺️")
                    time.sleep(5)
                    st.error('Task deleted!', icon="😎")
                    st.balloons()
                    # st.rerun()

    if divider == 1:
        st.write("---") 


