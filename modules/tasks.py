import streamlit as st
import datetime
import time
import pandas as pd
import os
from datetime import datetime, date

import utils.user_credentials as uc
import utils.g_gemini_gestor as ggg

@st.fragment
def update_task_status(task_id, project_name): 
    uc.run_query_insert_update(f"UPDATE `company-data-driven.{project_name}.tasks` SET status = 'finished', finished_date = CURRENT_DATE() WHERE id = {task_id}")
    st.toast("Updating, please wait", icon="☺️")
    st.balloons()
    time.sleep(2)
    st.toast("Task status updated!", icon="😎")
    uc.run_query_2_m.clear()
    uc.run_query_1_m.clear()


@st.fragment
def tasks_visualizer(user_id, project_name, divider):
    os.write(1, '🥏 Executing tasks_visualizer \n'.encode('utf-8'))
    
    # Modified SQL query to calculate priority directly
    query = f"""
    SELECT 
        id, 
        creation_date, 
        description, 
        commit_finish_date, 
        status,
        CASE 
            WHEN DATE_DIFF(commit_finish_date, CURRENT_DATE(), DAY) <= 3 THEN 'Alta'
            WHEN DATE_DIFF(commit_finish_date, CURRENT_DATE(), DAY) <= 7 THEN 'Media'
            ELSE 'Baja'
        END AS priority
    FROM `company-data-driven.{project_name}.tasks` 
    WHERE responsible_user_id = {user_id} 
    AND status IN ('to_start', 'on_execution', 'delayed') 
    ORDER BY commit_finish_date ASC;
    """
    
    rows = uc.run_query_2_m(query)
    
    st.markdown("""
    <style>
    .task-container { margin-bottom: 10px; padding: 10px; border-radius: 5px; }
    .task-green { background-color: #e6f3e6; }
    .task-white { background-color: #ffffff; }
    .task-content { display: flex; align-items: center; }
    .task-description { flex-grow: 1; }
    .task-info { display: flex; justify-content: space-between; align-items: center; }
    .small-font { color: #666666 !important; font-size: 0.9em; }
    .header { font-weight: bold; color: #444444 !important; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

    if len(rows) == 0:
        st.success('Nailed it! Nothing left on your plate.', icon="😎")
    else:
        tasks_df = pd.DataFrame(rows)
        tasks_df['commit_finish_date'] = pd.to_datetime(tasks_df['commit_finish_date']).dt.date

        st.markdown('<div class="header">Active Tasks</div>', unsafe_allow_html=True)

        for index, task in tasks_df.iterrows():
            container_class = "task-green" if index % 2 == 0 else "task-white"
            
            with st.container():
                st.markdown(f'<div class="task-container {container_class}">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f'<div class="task-description"><strong>{task["description"]}</strong></div>', unsafe_allow_html=True)
                
                with col2:
                    priority_color = {"Alta": "🔴", "Media": "🟠", "Baja": "🟢"}
                    st.markdown(
                        f'<div class="task-info">'
                        f'<span class="small-font">{priority_color[task["priority"]]} {task["priority"]}</span>'
                        f'<span class="small-font">📅 {task["commit_finish_date"].strftime("%d %b %Y")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                if st.button("Finish", key=f"finish_{task['id']}", use_container_width=True):
                    update_task_status(task['id'], project_name)
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

    if divider == 1:
        st.write("---") 
    return rows



@st.fragment
def tasks_achievements(user_id, project_name, divider):
    os.write(1, '🥏 Executing tasks_achievements \n'.encode('utf-8'))
    if len(uc.run_query_1_m(f"SELECT id  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND finished_date IS NOT NULL LIMIT 1")) < 1:
        st.success("Your achievements will be available when you finish your first task")
    else:
        year_fulfillment = uc.run_query_1_m(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND canceled_date IS NULL AND  EXTRACT(YEAR FROM commit_finish_date) <= EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM commit_finish_date) <= EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(WEEK FROM commit_finish_date) <= EXTRACT(WEEK FROM CURRENT_DATE()) GROUP BY year ORDER BY year DESC LIMIT 2")
        month_fulfillment = uc.run_query_1_m(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, EXTRACT(MONTH FROM commit_finish_date) AS month, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND canceled_date IS NULL AND  EXTRACT(YEAR FROM commit_finish_date) <= EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM commit_finish_date) <= EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(WEEK FROM commit_finish_date) <= EXTRACT(WEEK FROM CURRENT_DATE()) GROUP BY year, month ORDER BY year DESC, month DESC LIMIT 2")
        week_fulfillment = uc.run_query_1_m(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, EXTRACT(MONTH FROM commit_finish_date) AS month,  EXTRACT(WEEK FROM commit_finish_date) AS week, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND canceled_date IS NULL AND  EXTRACT(YEAR FROM commit_finish_date) <= EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM commit_finish_date) <= EXTRACT(MONTH FROM CURRENT_DATE()) AND EXTRACT(WEEK FROM commit_finish_date) <= EXTRACT(WEEK FROM CURRENT_DATE()) GROUP BY year, month, week ORDER BY year DESC, month DESC, week DESC LIMIT 2")

        with st.container(border=True):
            st.write("#### Cumplimiento")
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

        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True): 
                st.write("#### Unfulfilled tasks last 3 months")
                unfulfilled_tasks_table = uc.run_query_1_m(f"SELECT t.description, t.commit_finish_date, t.unfulfilled_date  FROM `company-data-driven.{project_name}.tasks` AS t WHERE responsible_user_id = {user_id} AND t.status = 'unfulfilled' AND t.unfulfilled_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AND EXTRACT(YEAR FROM t.creation_date) = EXTRACT(YEAR FROM CURRENT_DATE()) ORDER BY t.unfulfilled_date DESC;")
                if len(unfulfilled_tasks_table) < 1:
                    st.success("You killed it! I knew you could do it!", icon = "😎")
                else:
                    for task in unfulfilled_tasks_table:
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                                <p style="margin: 0;"><strong>{task['description']}</strong></p>
                                <p style="margin: 0; color: #666666; font-size: 0.9em;">
                                    📅 Due: {task['commit_finish_date'].strftime('%d %b %Y')} | 
                                    ❌ Unfulfilled: {task['unfulfilled_date'].strftime('%d %b %Y')}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

        with col2:
            with st.container(border=True): 
                st.write("#### Completed tasks")
                number_tasks_to_show = st.slider('Select number of tasks to be shown', 0, 30, 5)
                completed_tasks_table = uc.run_query_1_m(f"SELECT t.description, t.commit_finish_date, t.finished_date  FROM `company-data-driven.{project_name}.tasks` AS t WHERE responsible_user_id = {user_id} AND t.status = 'finished' ORDER BY t.finished_date DESC, t.id DESC LIMIT {number_tasks_to_show};")
                for task in completed_tasks_table:
                    with st.container():
                        st.markdown(f"""
                        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <p style="margin: 0;"><strong>{task['description']}</strong></p>
                            <p style="margin: 0; color: #666666; font-size: 0.9em;">
                                📅 Due: {task['commit_finish_date'].strftime('%d %b %Y')} | 
                                ✅ Completed: {task['finished_date'].strftime('%d %b %Y')}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
    if divider == 1:
        st.write("---") 

@st.fragment
def tips_tasks_ia(tasks, divider):
    if len(tasks) > 2:
        ia_tips_button = st.button("🤖 Help me to prioritize!")     
        if ia_tips_button:       
            st.success('Tips to prioritize your tasks using the Eisenhower method:', icon="🤖")   
            answer = ggg.gemini_general_prompt("You are an expert in project management and tasks priorization", "I am an expert in the Eisenhower Matrix methodology", f"Help me to priorize my tasks using the Eisenhower Matrix methodology, find yourself the urgency and importance and give me just the results, solve it and give me the tasks priorized with tips, be specific, return just the list of the task prioritized and one tip of each one, use less than 200 tokens: “ {tasks} ”:")

            st.write(answer)
    if divider == 1:
        st.write("---") 


@st.fragment
def execute_task_creation():
    os.write(1, '🥏 Executing execute_task_creation \n'.encode('utf-8'))
    if st.session_state.selected_user_id is None or st.session_state.task_input is None or len(st.session_state.task_input) < 10 or st.session_state.commitment_date_input is None:
        st.toast("Please fill in completely all of the required fields.")
    else:
        max_id =  uc.run_query_instant(f"SELECT MAX(id)+1 AS max_id FROM `company-data-driven.{st.session_state.project_name}.tasks`")[0].get('max_id')
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.project_name}.tasks` (id, creation_date, description, responsible_user_id, commit_finish_date, status, task_creator_id) VALUES({max_id}, CURRENT_DATE(), '{st.session_state.task_input}', {st.session_state.selected_user_id}, '{st.session_state.commitment_date_input}', 'to_start', {st.session_state.user_id})")
        st.toast("Updating, please wait", icon = "☺️")
        st.toast('Task created! (' + st.session_state.task_input + ')', icon="😎")
        st.balloons()
        time.sleep(5)
        del st.session_state.selected_user_id
        del st.session_state.task_input
        del st.session_state.commitment_date_input
        del st.session_state.project_name
        del st.session_state.user_id
        uc.run_query_5_m.clear()
        uc.run_query_2_m.clear()

@st.fragment
def task_creation(user_id, role_id, project_id, project_name, divider):
    os.write(1, '🥏 Executing task_creation \n'.encode('utf-8'))
    rows = uc.run_query_1_day(f"SELECT id, name FROM `company-data-driven.global.roles` WHERE id >= {role_id} ORDER BY id DESC;")
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
        rows_users = uc.run_query_5_m(f"SELECT u.id, u.username FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE u.project_id = {project_id} AND u.status = 'active' AND ra.role_id = {selected_role_id} ORDER BY u.username ASC;")
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
            st.session_state.selected_user_id = selected_user_id
            st.session_state.task_input = task_input
            st.session_state.commitment_date_input = commitment_date_input
            st.session_state.project_name = project_name
            st.session_state.user_id = user_id
            
            create_task_button = st.button("Create task", on_click = execute_task_creation)

    if divider == 1:
        st.write("---") 


@st.fragment
def task_deletion_execution():
    os.write(1, '🥏 Executing task_deletion_execution \n'.encode('utf-8'))
    if st.session_state.selected_task_description is not None:
        selected_task_id = st.session_state.user_tasks_ids[st.session_state.user_tasks_descriptions.index(st.session_state.selected_task_description)]
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.project_name}.tasks` SET status = 'canceled', canceled_date = CURRENT_DATE(), task_cancelator_id = {st.session_state.user_id} WHERE id = {selected_task_id};")
        st.toast("Updating, please wait", icon = "☺️")
        st.error('Task deleted!', icon="😎")
        st.balloons()
        time.sleep(5)
        uc.run_query_1_m.clear()
        uc.run_query_2_m.clear()
        # st.rerun()


@st.fragment
def task_deletion(user_id, role_id, project_id, project_name, divider):
    os.write(1, '🥏 Executing task_deletion \n'.encode('utf-8'))
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
            rows_user_tasks = uc.run_query_1_m(f"SELECT id, description FROM `company-data-driven.{project_name}.tasks` WHERE finished_date IS NULL AND canceled_date IS NULL AND responsible_user_id = {selected_user_id} ORDER BY description ASC;")
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
            st.session_state.user_id = user_id
            st.session_state.role_id = role_id
            st.session_state.project_id = project_id
            st.session_state.project_name = project_name
            st.session_state.selected_task_description = selected_task_description
            st.session_state.user_tasks_ids = user_tasks_ids
            st.session_state.user_tasks_descriptions = user_tasks_descriptions
            
            cancel_task_button = st.button("Cancel task", on_click = task_deletion_execution)


    if divider == 1:
        st.write("---") 


