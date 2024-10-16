import streamlit as st
import os
import datetime

import utils.project_handler as ph

from google.oauth2 import service_account
from google.cloud import bigquery

def gcloud_bigquery_client():
    credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
    client = bigquery.Client(credentials=credentials)
    return client

client = gcloud_bigquery_client()

def run_query_insert_update(query):
    client.query(query)

@st.cache_data(ttl=86400, show_spinner=False)
def run_query_insert_update_1_day(query):
    client.query(query)

# @st.cache_resource(show_spinner=False)
# @st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def run_query_instant(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=5, show_spinner=False)
def run_query_5_s(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=10, show_spinner=False)
def run_query_10_s(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=30, show_spinner=False)
def run_query_30_s(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=60, show_spinner=False)
def run_query_1_m(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=120, show_spinner=False)
def run_query_2_m(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=300, show_spinner=False)
def run_query_5_m(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=900, show_spinner=False)
def run_query_15_m(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=1800, show_spinner=False)
def run_query_30_m(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=3600, show_spinner=False)
def run_query_1_h(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=10800, show_spinner=False)
def run_query_3_h(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=21600, show_spinner=False)
def run_query_6_h(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=43200, show_spinner=False)
def run_query_half_day(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

@st.cache_data(ttl=86400, show_spinner=False)
def run_query_1_day(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

def user_credentials(name, authentication_status, username):
    os.write(1, '🥏 Executing user_credentials \n'.encode('utf-8'))
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    if 'user_id' not in st.session_state or 'status' not in st.session_state or 'project_id' not in st.session_state or 'role_id' not in st.session_state or 'role_name' not in st.session_state or 'project_icon' not in st.session_state or 'project_logo_url' not in st.session_state or 'project_name' not in st.session_state or 'project_title' not in st.session_state or 'project_url_clean' not in st.session_state or 'project_keyword' not in st.session_state:
        rows = run_query_1_day(f"SELECT u.id AS user_id, u.username, u.status, u.project_id, r.id AS role_id, r.name AS role_name, p.icon, p.logo_url, p.name, p.title, p.web_url_clean, p.keyword   FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id INNER JOIN `company-data-driven.global.roles` AS r ON ra.role_id = r.id INNER JOIN `company-data-driven.global.projects` AS p ON u.project_id = p.id WHERE username = '{username}';")
        os.write(1, '- user_credentials: Get user data \n'.encode('utf-8'))
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
            project_url_clean = rows[0].get('web_url_clean')
            project_keyword = rows[0].get('keyword')
    
        else:
            user_id = rows[0].get('user_id')
            status = rows[0].get('status')
            project_id = rows[0].get('project_id')
            project_icon = rows[0].get('icon')
            project_logo_url = rows[0].get('logo_url')
            project_name = rows[0].get('name')
            project_title = rows[0].get('title')
            project_url_clean = rows[0].get('web_url_clean')
            project_keyword = rows[0].get('keyword')
    
    
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
        
        run_query_insert_update_1_day(f"UPDATE `company-data-driven.global.users` SET last_login_date = '{today_str}' WHERE id = {user_id};")
        os.write(1, '- user_credentials: Updating last user connection \n'.encode('utf-8'))
        
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
                    
            st.session_state.user_id = user_id
            st.session_state.status = status
            st.session_state.project_id = project_id
            st.session_state.role_id = role_id
            st.session_state.role_name = role_name
            st.session_state.project_icon = project_icon
            st.session_state.project_logo_url = project_logo_url
            st.session_state.project_name = project_name
            st.session_state.project_title = project_title
            st.session_state.project_url_clean = project_url_clean
            st.session_state.project_keyword = project_keyword

    os.write(1, '- user_credentials: Moving forward \n'.encode('utf-8'))
    ph.project_handler(st.session_state.user_id, st.session_state.project_id, st.session_state.role_id, st.session_state.role_name, st.session_state.project_name, st.session_state.project_title, st.session_state.project_icon, st.session_state.project_logo_url, st.session_state.project_url_clean, st.session_state.project_keyword)






        
