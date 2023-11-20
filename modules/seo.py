import streamlit as st
import pandas as pd
import time
import datetime

import utils.user_credentials as uc

def content_creation_guide_effective_communication_storytelling():
    with st.form("comm_eff_storytelling_form"):

        text_input = st.text_input(
            "Enter some text 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder,
        )

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(text_input)

