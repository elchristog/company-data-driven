import streamlit as st
import streamlit_authenticator as stauth
import yaml

from yaml.loader import SafeLoader
import utils.user_credentials as uc

@st.cache_data 
def login():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
        name, authentication_status, username = authenticator.login('Login', 'main')
        if st.session_state["authentication_status"]:
            uc.user_credentials(name, authentication_status, username)
            st.write("---") 
            authenticator.logout('Logout', 'main')
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')