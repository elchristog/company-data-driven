import pandas as pd
import numpy as np
import streamlit as st
import os
import time


import utils.user_credentials as uc

@st.fragment
def estado_de_resultados():
    os.write(1, '🥏 Executing estado_de_resultados \n'.encode('utf-8'))
    pass
