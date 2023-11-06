import streamlit as st
import datetime

import utils.user_credentials as uc

def one_resource():
    st.metric(label="# Month Tests", value = '🗂️')
    link = f"[Discuss answers with my group](url)"
    st.markdown(link, unsafe_allow_html=True)
    st.metric(label="# Month Tests", value = st.markdown(link, unsafe_allow_html=True))
