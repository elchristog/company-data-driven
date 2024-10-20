import streamlit as st
import streamlit_authenticator as stauth
import yaml
import os

from yaml.loader import SafeLoader
import utils.user_credentials as uc

def login():
    os.write(1, '🥏 Executing login \n'.encode('utf-8'))
    if 'authentication_status' not in st.session_state or st.session_state["authentication_status"] is None or st.session_state["authentication_status"] is False:
        os.write(1, '- login: Authenticating user \n'.encode('utf-8'))
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
            authenticator = stauth.Authenticate(
                config['credentials'],
                config['cookie']['name'],
                config['cookie']['key'],
                config['cookie']['expiry_days'],
                config['preauthorized']
            )
            name, authentication_status, username = authenticator.login()
            st.session_state.name = name
            st.session_state.authentication_status = authentication_status
            st.session_state.username = username
            # with st.sidebar:
            #     st.write("---") 
            #     authenticator.logout('Logout', 'main')
        if st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect (Ask to the admin if is hashed)')
    if st.session_state["authentication_status"]:
        os.write(1, '- login: Skipping authentication \n'.encode('utf-8'))
        uc.user_credentials(st.session_state.name, st.session_state.authentication_status, st.session_state.username)
        st.write("---") 
