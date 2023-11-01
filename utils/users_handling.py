import streamlit as st
import streamlit_authenticator as stauth

import utils.user_credentials as uc


def hashing():
    password_to_hash = st.text_input("Write the password to hash:")
    hashed_passwords = stauth.Hasher([password_to_hash]).generate()
    hashing_button = st.button("Start Hashing")
    if hashing_button:
        st.write(hashed_passwords[0])

def user_creation(user_id, project_id, project_name): 
    username = st.text_input("Write the username:")
    check_username_availability = st.button("Check Availability")
    if check_username_availability: #name, birthdate, country, gender, user_creator, email, project_id
        checking_username_query = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{username}';")
        if len(checking_username_query) > 0:
            st.error('Username is not available', icon = '👻')
        else:
            max_id_users = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.global.users`;")
            st.write(max_id_users[0].get('max_id'))
