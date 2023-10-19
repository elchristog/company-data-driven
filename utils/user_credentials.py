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
    st.table(rows)

    # esta activo el man y si esta mas de una vez chequeo que este en un solo proyecto y tarer todos sus roles