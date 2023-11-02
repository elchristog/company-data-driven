import streamlit as st

import utils.user_credentials as uc


def tester(project_name, questions_table_name, num_questions, user_id): 
    new_test = st.button("Start test")
    if new_test:
        questions = uc.run_query_instant(f"SELECT * FROM `company-data-driven.{project_name}.{questions_table_name}` ORDER BY RAND() LIMIT {num_questions};")
        st.write(questions)

        st.write("🔹 **A)** " + "pepe")
