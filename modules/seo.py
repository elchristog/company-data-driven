import streamlit as st
import pandas as pd
import time
import datetime

import utils.user_credentials as uc

def content_creation_guide_effective_communication_storytelling():
    with st.form("comm_eff_storytelling_form", clear_on_submit = True):

        text_input = st.text_input(
            "Enter some text 👇",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Un plaveholder',
            help = 'ayudigna'
        )

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(text_input)

