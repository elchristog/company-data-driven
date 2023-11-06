import streamlit as st
import datetime

import utils.user_credentials as uc

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

def one_resource():
    st.metric(label="# Month Tests", value = '🗂️')
    link = f"[Discuss answers with my group](url)"
    st.markdown(link, unsafe_allow_html=True)
    st.link_button(":file_folder: Go to gallery", "https://streamlit.io/gallery")