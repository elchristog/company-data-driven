import streamlit as st

import utils.user_credentials as uc


def tester(): # project_name, questions_table_name, num_questions, user_id
    questions = uc.run_query_1_h(f"SELECT * FROM `company-data-driven.enfermera_en_estados_unidos.nclex_questions` ORDER BY RAND() LIMIT 3;")
    st.write(questions)