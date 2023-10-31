import streamlit as st
import os

import utils.project_handler as ph

from google.oauth2 import service_account
from google.cloud import bigquery

# @st.cache
def gcloud_bigquery_client():
    credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
    client = bigquery.Client(credentials=credentials)
    return client

@st.cache
def run_query(query):
    client = gcloud_bigquery_client()
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache
def user_credentials(name, authentication_status, username):
    # @st.cache_data(ttl=600) # Uses st.cache_data to only rerun when the query changes or after 10 min.
    rows = run_query(f"SELECT u.id AS user_id, u.username, u.status, u.project_id, r.id AS role_id, r.name AS role_name, p.icon, p.logo_url, p.name, p.title   FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id INNER JOIN `company-data-driven.global.roles` AS r ON ra.role_id = r.id INNER JOIN `company-data-driven.global.projects` AS p ON u.project_id = p.id WHERE username = '{username}';")

    if len(rows) == 1:
        user_id = rows[0].get('user_id')
        status = rows[0].get('status')
        project_id = rows[0].get('project_id')
        role_id = rows[0].get('role_id')
        role_name = rows[0].get('role_name')
        project_icon = rows[0].get('icon')
        project_logo_url = rows[0].get('logo_url')
        project_name = rows[0].get('name')
        project_title = rows[0].get('title')

    else:
        user_id = rows[0].get('user_id')
        status = rows[0].get('status')
        project_id = rows[0].get('project_id')
        project_icon = rows[0].get('icon')
        project_logo_url = rows[0].get('logo_url')
        project_name = rows[0].get('name')
        project_title = rows[0].get('title')

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
    
    if status != 'active':
            st.error('User is inactive')
    else:
        if len(rows) > 1:
            if all(element == user_ids[0] for element in user_ids):
                pass
            else:
                st.error('User has multiple ids')

            if all(element == statuses[0] for element in statuses):
                pass
            else:
                st.error('User has multiple status')

            if all(element == project_ids[0] for element in project_ids):
                pass
            else:
                st.error('User has multiple projects')
             
        ph.project_handler(user_id, project_id, role_id, role_name, project_name, project_title, project_icon, project_logo_url)






        