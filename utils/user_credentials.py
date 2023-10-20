import streamlit as st

from google.oauth2 import service_account
from google.cloud import bigquery


def user_credentials(name, authentication_status, username):
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
    rows = run_query(f"SELECT u.id AS user_id, u.username, u.status, u.project_id, r.id AS role_id, r.name AS role_name   FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id INNER JOIN `company-data-driven.global.roles` AS r ON ra.role_id = r.id WHERE username = '{username}';")

    if len(rows) == 1:
        user_id = rows[0].get('user_id')
        status = rows[0].get('status')
        project_id = rows[0].get('project_id')
        role_id = rows[0].get('role_id')
        role_name = rows[0].get('role_name')
    else:
        user_id = rows[0].get('user_id')
        status = rows[0].get('status')
        project_id = rows[0].get('project_id')

        user_ids = []
        statuses = []
        project_ids = []
        role_id = []
        role_name = []

        for row in rows:
                user_ids.append(row.get('user_id'))
                statuses.append(row.get('status'))
                project_ids.append(row.get('project_id'))
                role_id.append(row.get('role_id'))
                role_name.append(row.get('role_name'))
        st.write(status)
        if status != 'active':
             st.error('User is inactive')
        else:
            st.table(rows)
            # project_handler(user_id, status, project_id, role_id, role_name)





        