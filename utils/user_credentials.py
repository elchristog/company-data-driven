import streamlit as st

from google.oauth2 import service_account
from google.cloud import bigquery

def user_credentials(name, authentication_status, username):
    st.write(name) 