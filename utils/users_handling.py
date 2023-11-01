import streamlit as st
import streamlit_authenticator as stauth


def hashing():
    hashed_passwords = stauth.Hasher(['abc']).generate()
    st.text(hashed_passwords)