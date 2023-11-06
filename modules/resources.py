import streamlit as st
import datetime

import utils.user_credentials as uc

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

def one_resource():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button(":card_index_dividers: Go to gallery", "https://streamlit.io/gallery")