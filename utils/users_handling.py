import streamlit as st
import streamlit_authenticator as stauth


def hashing():
    password_to_hash = st.text_input("Write the password to hash:")
    hashed_passwords = stauth.Hasher([password_to_hash]).generate()
    hashing_button = st.button("Start Hashing")
    if hashing_button:
        st.success(hashed_passwords)