import streamlit as st

import utils.user_credentials as uc

# https://docs.streamlit.io/library/api-reference/status

def tester(project_name, questions_table_name, user_id): 
    questions = uc.run_query_1_day(f"SELECT * FROM `company-data-driven.{project_name}.{questions_table_name}`;")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Q 1", "Q 2", "Q 3", "Q 4", "Q 5", "Q 6", "Q 7", "Q 8", "Q 9", "Q 10"])
    with tab1:
        st.header(questions[0].get("question"))
        st.write("🔹 **A)** " + questions[0].get("option_a"))
        st.write("🔹 **B)** " + questions[0].get("option_b"))
        st.write("🔹 **C)** " + questions[0].get("option_c"))
        st.write("🔹 **D)** " + questions[0].get("option_d"))
        selected_answer_q1 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_1"
            ).lower()
        st.toast('Answer selected: ' + selected_answer_q1.upper(), icon='🥸')
    with tab2:
        st.header(questions[1].get("question"))
        st.write("🔹 **A)** " + questions[1].get("option_a"))
        st.write("🔹 **B)** " + questions[1].get("option_b"))
        st.write("🔹 **C)** " + questions[1].get("option_c"))
        st.write("🔹 **D)** " + questions[1].get("option_d"))
        selected_answer_q2 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_2"
            ).lower()
        st.toast('Answer selected: ' + selected_answer_q2.upper(), icon='🥸')
    with tab3:
        st.header(questions[2].get("question"))
        st.write("🔹 **A)** " + questions[2].get("option_a"))
        st.write("🔹 **B)** " + questions[2].get("option_b"))
        st.write("🔹 **C)** " + questions[2].get("option_c"))
        st.write("🔹 **D)** " + questions[2].get("option_d"))
        selected_answer_q3 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_3"
            ).lower()
        st.toast('Answer selected: ' + selected_answer_q3.upper(), icon='🥸')
    with tab4:
        st.header(questions[3].get("question"))
        st.write("🔹 **A)** " + questions[3].get("option_a"))
        st.write("🔹 **B)** " + questions[3].get("option_b"))
        st.write("🔹 **C)** " + questions[3].get("option_c"))
        st.write("🔹 **D)** " + questions[3].get("option_d"))
        selected_answer_q4 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_4"
            ).lower()
        st.toast('Answer selected: ' + selected_answer_q4.upper(), icon='🥸')
    with tab5:
        st.header(questions[4].get("question"))
        st.write("🔹 **A)** " + questions[4].get("option_a"))
        st.write("🔹 **B)** " + questions[4].get("option_b"))
        st.write("🔹 **C)** " + questions[4].get("option_c"))
        st.write("🔹 **D)** " + questions[4].get("option_d"))
        selected_answer_q5 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_5"
            ).lower()
        st.toast('Answer selected: ' + selected_answer_q5.upper(), icon='🥸')
        
        

    st.write(questions)
    
