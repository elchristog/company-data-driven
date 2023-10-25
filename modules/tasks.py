import streamlit as st

############ tasks #######
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)
# @st.cache_data(ttl=600) # Uses st.cache_data to only rerun when the query changes or after 10 min.
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows
rows = run_query(f"SELECT id, creation_date, description, commit_finish_date, status  FROM `hacer-storytelling.hacer_storytelling.tasks` WHERE responsable_username = '{username}' AND status IN ('por_iniciar', 'en_ejecucion', 'atrasada')") #finished, canceled, incumplida
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
        label="Select one task",
        options=descriptions,
        index=None
    )
    if selected_task is not None:
        selected_task_status = actual_statuses[descriptions.index(selected_task)]
        if selected_task_status == 'en_ejecucion':
            selected_status = st.selectbox(
            label="Select the new status",
            options= ['finished'],
            index=None
        )
        else:
            selected_status = st.selectbox(
                label="Select the new status",
                options= ['en_ejecucion'],
                index=None
            )
        update_task_status_button = st.button("Update status")
        def update_task_status(task_id, new_status, today_str):
            if new_status == 'en_ejecucion':
                run_query(f"UPDATE `hacer-storytelling.hacer_storytelling.tasks` SET status = '{new_status}', on_execution_date = '{today_str}' WHERE id = {task_id}")
            if new_status == 'finished':
                run_query(f"UPDATE `hacer-storytelling.hacer_storytelling.tasks` SET status = '{new_status}', finished_date = '{today_str}' WHERE id = {task_id}")
        if update_task_status_button:
            selected_task_id = ids[descriptions.index(selected_task)]
            update_task_status(selected_task_id, selected_status, today_str)
            st.rerun()




st.write("---") 
st.markdown(""" ### Your achievements """)
year_fulfillment = run_query(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `hacer-storytelling.hacer_storytelling.tasks` WHERE responsable_username = '{username}' AND canceled_date IS NULL GROUP BY year ORDER BY year DESC LIMIT 2")
month_fulfillment = run_query(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, EXTRACT(MONTH FROM commit_finish_date) AS month, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `hacer-storytelling.hacer_storytelling.tasks` WHERE responsable_username = '{username}' AND canceled_date IS NULL GROUP BY year, month ORDER BY year DESC, month DESC LIMIT 2")
week_fulfillment = run_query(f"SELECT EXTRACT(YEAR FROM commit_finish_date) AS year, EXTRACT(MONTH FROM commit_finish_date) AS month,  EXTRACT(WEEK FROM commit_finish_date) AS week, 100*(SUM(CASE WHEN finished_date IS NOT NULL THEN 1 ELSE 0 END)/COUNT(id)) AS fulfillment  FROM `hacer-storytelling.hacer_storytelling.tasks` WHERE responsable_username = '{username}' AND canceled_date IS NULL GROUP BY year, month, week ORDER BY year DESC, month DESC, week DESC LIMIT 2")

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





st.write("---") 
ia_tips_button = st.button("🤖 Help me!")     
if ia_tips_button:       
    st.success('Tips to prioritize your tasks using the Eisenhower method:', icon="🤖")            
    st.write(tips_tasks_ia(rows))






if username == st.secrets["ADMIN_USER"]:
    st.write("---") 
    st.markdown(""" ### Task creation """)






st.write("---") 