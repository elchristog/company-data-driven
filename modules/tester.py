import streamlit as st
import datetime
import re

import utils.user_credentials as uc

# https://docs.streamlit.io/library/api-reference/status

def tester(project_name, questions_sample_table_name, user_id): 
    questions = uc.run_query_half_day(f"SELECT * FROM `company-data-driven.{project_name}.{questions_sample_table_name}`;")
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
    with tab6:
        st.header(questions[5].get("question"))
        st.write("🔹 **A)** " + questions[5].get("option_a"))
        st.write("🔹 **B)** " + questions[5].get("option_b"))
        st.write("🔹 **C)** " + questions[5].get("option_c"))
        st.write("🔹 **D)** " + questions[5].get("option_d"))
        selected_answer_q6 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_6"
            ).lower()
    with tab7:
        st.header(questions[6].get("question"))
        st.write("🔹 **A)** " + questions[6].get("option_a"))
        st.write("🔹 **B)** " + questions[6].get("option_b"))
        st.write("🔹 **C)** " + questions[6].get("option_c"))
        st.write("🔹 **D)** " + questions[6].get("option_d"))
        selected_answer_q7 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_7"
            ).lower()
    with tab8:
        st.header(questions[7].get("question"))
        st.write("🔹 **A)** " + questions[7].get("option_a"))
        st.write("🔹 **B)** " + questions[7].get("option_b"))
        st.write("🔹 **C)** " + questions[7].get("option_c"))
        st.write("🔹 **D)** " + questions[7].get("option_d"))
        selected_answer_q8 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_8"
            ).lower()
    with tab9:
        st.header(questions[8].get("question"))
        st.write("🔹 **A)** " + questions[8].get("option_a"))
        st.write("🔹 **B)** " + questions[8].get("option_b"))
        st.write("🔹 **C)** " + questions[8].get("option_c"))
        st.write("🔹 **D)** " + questions[8].get("option_d"))
        selected_answer_q9 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_9"
            ).lower()
    with tab10:
        st.header(questions[9].get("question"))
        st.write("🔹 **A)** " + questions[9].get("option_a"))
        st.write("🔹 **B)** " + questions[9].get("option_b"))
        st.write("🔹 **C)** " + questions[9].get("option_c"))
        st.write("🔹 **D)** " + questions[9].get("option_d"))
        selected_answer_q10 = st.selectbox(
                label="Select your answer",
                options= ['A', 'B', 'C', 'D'],
                index=None,
                key = "question_10"
            ).lower()
        send_answers = st.button("Send Answers")
        
        

    st.write(questions)


def add_question_to_test(project_name, questions_table_name, user_id):
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    max_id = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.{project_name}.{questions_table_name}`;")[0].get("max_id")

    question = st.text_input("Write the question:")
    option_a = st.text_input("Write the option A:")
    option_b = st.text_input("Write the option B:")
    option_c = st.text_input("Write the option C:")
    option_d = st.text_input("Write the option D:")
    letter_correct_answer = st.selectbox(
        label = "Select correct answer",
        options = ['A', 'B', 'C', 'D'],
        index = None
    )
    confirm_letter_correct_answer = st.selectbox(
        label = "Confirm correct answer",
        options = ['A', 'B', 'C', 'D'],
        index = None
    )
    if letter_correct_answer is not None and confirm_letter_correct_answer is not None:
        if letter_correct_answer == confirm_letter_correct_answer:
            st.success("Answer confirmed!", icon = "🎈")
        else:
            st.error('Incorrect answer', icon = '🀄')


    if letter_correct_answer is not None:
        letter_correct_answer_lower = letter_correct_answer.lower()
    explanation = st.text_input("Write the explanation:")
    if explanation is not None:
        cleaned_explanation = re.sub(r'[\"\']', '', explanation)

    add_question_button = st.button("Add question")
    if add_question_button:
        if question is None or option_a is None or option_b is None or option_c is None or option_d is None or letter_correct_answer is None or explanation is None:
            st.error("Please fill in completely all of the required fields.")
        else:
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.{questions_table_name}` (id, creation_date, question	,option_a	,option_b	,option_c	,option_d	,correct_option	,explanation, creator_id) VALUES({max_id}, '{today_str}', '{question}', '{option_a}', '{option_b}', '{option_c}', '{option_d}', '{letter_correct_answer_lower}', '{cleaned_explanation}', {user_id});")
            st.success("Question added!", icon = "🐣")
            st.balloons()




    
