import streamlit as st
import datetime

import utils.user_credentials as uc

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

def resources(project_name, user_id, r_1 = [], r_2 = [], r_3 = [], r_4 = [], r_5 = [], r_6 = [], r_7 = [], r_8 = [], r_9 = [], r_10 = [], r_11 = []):
    # Each resource must be: [':selfie:', 'name', 'link_url'] [icon, button_name, link_url]

    st.write(r_1)
    st.write(len(r_1))

    st.write(r_2)
    st.write(len(r_2))


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.link_button(":card_index_dividers: Google Drive", "https://streamlit.io/gallery")
    with col2:
        st.link_button(":card_index_dividers: Google Drive", "https://streamlit.io/gallery") if len(r_1) > 0 else st.write()
    with col3:
        st.link_button(":card_index_dividers: Google Drive", "https://streamlit.io/gallery") if len(r_2) > 0 else st.write()
