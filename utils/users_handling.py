import streamlit as st
import streamlit_authenticator as stauth

import utils.user_credentials as uc


def hashing():
    password_to_hash = st.text_input("Write the password to hash:")
    hashed_passwords = stauth.Hasher([password_to_hash]).generate()
    hashing_button = st.button("Start Hashing")
    if hashing_button:
        st.write(hashed_passwords[0])

def user_creation():
    username = st.text_input("Write the username:")
    check_username_availability = st.button("Check Availability")
    if check_username_availability:
        checking_username_query = uc.run_query_instant(f"SELECT id, creation_date, description, commit_finish_date, status  FROM `company-data-driven.{project_name}.tasks` WHERE responsible_user_id = {user_id} AND status IN ('to_start', 'on_execution', 'delayed');") #finished, canceled, unfulfilled
