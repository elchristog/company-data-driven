import streamlit as st

import utils.user_credentials as uc

def tester(project_name, questions_table_name, user_id): 
    questions = uc.run_query_1_day(f"SELECT * FROM `company-data-driven.{project_name}.{questions_table_name}`;")
    st.write(questions)

    tab1, tab2, tab3 = st.tabs(["Question 1", "Question 2", "Question 3"])
    with tab1:
        st.header(questions[0].get("question"))

        st.write("🔹 **A)** " + questions[0].get("option_a"))
        st.write("🔹 **B)** " + questions[0].get("option_b"))
        st.write("🔹 **C)** " + questions[0].get("option_c"))
        st.write("🔹 **D)** " + questions[0].get("option_d"))

        selected_answer_q1 = st.selectbox(
                label="Select the new status",
                options= ['A', 'B', 'C', 'D'],
                index=None
            )
