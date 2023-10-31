import streamlit as st
import utils.login as login
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    @st.cache_data
    login.login()


if __name__ == "__main__":
    run()
