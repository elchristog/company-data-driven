import streamlit as st

import utils.user_credentials as uc

def tester(project_name, questions_table_name, num_questions, user_id): 
    new_test = st.button("Start test")
    if new_test:
        questions = uc.run_query_instant(f"SELECT * FROM `company-data-driven.{project_name}.{questions_table_name}` ORDER BY RAND() LIMIT {num_questions};")
        st.write(questions)

        tab1, tab2, tab3 = st.tabs(["Question 1", "Question 2", "Question 3"])
        with tab1:
            st.header(questions[0].get("question"))

            st.write("🔹 **A)** " + questions[0].get("option_a"))

            selected_answer_q1 = st.selectbox(
                    label="Select the new status",
                    options= ['A', 'B', 'C', 'D'],
                    index=None
                )
