import streamlit as st
import datetime
import re
import time
import pandas as pd
import altair as alt

import utils.user_credentials as uc

# https://docs.streamlit.io/library/api-reference/status


def tester_execution():
    if st.session_state.selected_answer_q1 is None or st.session_state.selected_answer_q2 is None or st.session_state.selected_answer_q3 is None or st.session_state.selected_answer_q4 is None or st.session_state.selected_answer_q5 is None or st.session_state.selected_answer_q6 is None or st.session_state.selected_answer_q7 is None or st.session_state.selected_answer_q8 is None or st.session_state.selected_answer_q9 is None or st.session_state.selected_answer_q10 is None:
        st.toast("you forgot to answer at least one question", icon = "🤧")
    else:
        if st.session_state.tester_user_id != st.session_state.user_id:
            return
        correct_q_1 = 1 if st.session_state.selected_answer_q1_lower == st.session_state.questions[0].get("correct_option") else 0
        correct_q_2 = 1 if st.session_state.selected_answer_q2_lower == st.session_state.questions[1].get("correct_option") else 0
        correct_q_3 = 1 if st.session_state.selected_answer_q3_lower == st.session_state.questions[2].get("correct_option") else 0
        correct_q_4 = 1 if st.session_state.selected_answer_q4_lower == st.session_state.questions[3].get("correct_option") else 0
        correct_q_5 = 1 if st.session_state.selected_answer_q5_lower == st.session_state.questions[4].get("correct_option") else 0
        correct_q_6 = 1 if st.session_state.selected_answer_q6_lower == st.session_state.questions[5].get("correct_option") else 0
        correct_q_7 = 1 if st.session_state.selected_answer_q7_lower == st.session_state.questions[6].get("correct_option") else 0
        correct_q_8 = 1 if st.session_state.selected_answer_q8_lower == st.session_state.questions[7].get("correct_option") else 0
        correct_q_9 = 1 if st.session_state.selected_answer_q9_lower == st.session_state.questions[8].get("correct_option") else 0
        correct_q_10 = 1 if st.session_state.selected_answer_q10_lower == st.session_state.questions[9].get("correct_option") else 0
        success_rate = 100 * ((correct_q_1 + correct_q_2 + correct_q_3 + correct_q_4 + correct_q_5 + correct_q_6 + correct_q_7 + correct_q_8 + correct_q_9 + correct_q_10)/10)
        
        today_answer_already_created = uc.run_query_instant(f"SELECT id FROM `company-data-driven.{st.session_state.tester_project_name}.{st.session_state.attempts_table_name}` WHERE attempt_date = '{st.session_state.today_str}' AND user_id = {st.session_state.tester_user_id};")
        if len(today_answer_already_created) < 1:
            max_id = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.{st.session_state.tester_project_name}.{st.session_state.attempts_table_name}`;")[0].get("max_id") 
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.tester_project_name}.{st.session_state.attempts_table_name}` VALUES({max_id},'{st.session_state.today_str}', {st.session_state.tester_user_id},{st.session_state.questions[0].get('id')},{correct_q_1},{st.session_state.questions[1].get('id')},{correct_q_2},{st.session_state.questions[2].get('id')},{correct_q_3},{st.session_state.questions[3].get('id')},{correct_q_4},{st.session_state.questions[4].get('id')},{correct_q_5},{st.session_state.questions[5].get('id')},{correct_q_6},{st.session_state.questions[6].get('id')},{correct_q_7},{st.session_state.questions[7].get('id')},{correct_q_8},{st.session_state.questions[8].get('id')},{correct_q_9},{st.session_state.questions[9].get('id')},{correct_q_10},{success_rate}, '{st.session_state.selected_answer_q1_lower}', '{st.session_state.selected_answer_q2_lower}', '{st.session_state.selected_answer_q3_lower}', '{st.session_state.selected_answer_q4_lower}', '{st.session_state.selected_answer_q5_lower}', '{st.session_state.selected_answer_q6_lower}', '{st.session_state.selected_answer_q7_lower}', '{st.session_state.selected_answer_q8_lower}', '{st.session_state.selected_answer_q9_lower}', '{st.session_state.selected_answer_q10_lower}');")         
            st.balloons()
            st.toast("Test sent, wait for answers", icon = "☺️")
            time.sleep(2)
            



def tester(project_name, questions_sample_table_name, user_id, attempts_table_name, group_chat_url): 
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    today_results = uc.run_query_instant(f"SELECT * FROM `company-data-driven.{project_name}.{attempts_table_name}` WHERE user_id = {user_id} AND attempt_date = '{today_str}';")
    if len(today_results) < 1:
        questions = uc.run_query_6_h(f"SELECT * FROM `company-data-driven.{project_name}.{questions_sample_table_name}`;")
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Q 1", "Q 2", "Q 3", "Q 4", "Q 5", "Q 6", "Q 7", "Q 8", "Q 9", "Q 10"])
        with tab1:
            st.write("#### " + questions[0].get("question"))
            st.write("🔹 **A)** " + questions[0].get("option_a"))
            st.write("🔹 **B)** " + questions[0].get("option_b"))
            st.write("🔹 **C)** " + questions[0].get("option_c"))
            st.write("🔹 **D)** " + questions[0].get("option_d"))
            selected_answer_q1 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_1"
                )
            if selected_answer_q1 is not None:
                selected_answer_q1_lower = selected_answer_q1.lower()
                st.session_state.selected_answer_q1_lower = selected_answer_q1_lower
        with tab2:
            st.write("#### " + questions[1].get("question"))
            st.write("🔹 **A)** " + questions[1].get("option_a"))
            st.write("🔹 **B)** " + questions[1].get("option_b"))
            st.write("🔹 **C)** " + questions[1].get("option_c"))
            st.write("🔹 **D)** " + questions[1].get("option_d"))
            selected_answer_q2 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_2"
                )
            if selected_answer_q2 is not None:
                selected_answer_q2_lower = selected_answer_q2.lower()
                st.session_state.selected_answer_q2_lower = selected_answer_q2_lower
        with tab3:
            st.write("#### " + questions[2].get("question"))
            st.write("🔹 **A)** " + questions[2].get("option_a"))
            st.write("🔹 **B)** " + questions[2].get("option_b"))
            st.write("🔹 **C)** " + questions[2].get("option_c"))
            st.write("🔹 **D)** " + questions[2].get("option_d"))
            selected_answer_q3 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_3"
                )
            if selected_answer_q3 is not None:
                selected_answer_q3_lower = selected_answer_q3.lower()
                st.session_state.selected_answer_q3_lower = selected_answer_q3_lower
        with tab4:
            st.write("#### " + questions[3].get("question"))
            st.write("🔹 **A)** " + questions[3].get("option_a"))
            st.write("🔹 **B)** " + questions[3].get("option_b"))
            st.write("🔹 **C)** " + questions[3].get("option_c"))
            st.write("🔹 **D)** " + questions[3].get("option_d"))
            selected_answer_q4 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_4"
                )
            if selected_answer_q4 is not None:
                selected_answer_q4_lower = selected_answer_q4.lower()
                st.session_state.selected_answer_q4_lower = selected_answer_q4_lower
        with tab5:
            st.write("#### " + questions[4].get("question"))
            st.write("🔹 **A)** " + questions[4].get("option_a"))
            st.write("🔹 **B)** " + questions[4].get("option_b"))
            st.write("🔹 **C)** " + questions[4].get("option_c"))
            st.write("🔹 **D)** " + questions[4].get("option_d"))
            selected_answer_q5 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_5"
                )
            if selected_answer_q5 is not None:
                selected_answer_q5_lower = selected_answer_q5.lower()
                st.session_state.selected_answer_q5_lower = selected_answer_q5_lower
        with tab6:
            st.write("#### " + questions[5].get("question"))
            st.write("🔹 **A)** " + questions[5].get("option_a"))
            st.write("🔹 **B)** " + questions[5].get("option_b"))
            st.write("🔹 **C)** " + questions[5].get("option_c"))
            st.write("🔹 **D)** " + questions[5].get("option_d"))
            selected_answer_q6 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_6"
                )
            if selected_answer_q6 is not None:
                selected_answer_q6_lower = selected_answer_q6.lower()
                st.session_state.selected_answer_q6_lower = selected_answer_q6_lower
        with tab7:
            st.write("#### " + questions[6].get("question"))
            st.write("🔹 **A)** " + questions[6].get("option_a"))
            st.write("🔹 **B)** " + questions[6].get("option_b"))
            st.write("🔹 **C)** " + questions[6].get("option_c"))
            st.write("🔹 **D)** " + questions[6].get("option_d"))
            selected_answer_q7 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_7"
                )
            if selected_answer_q7 is not None:
                selected_answer_q7_lower = selected_answer_q7.lower()
                st.session_state.selected_answer_q7_lower = selected_answer_q7_lower
        with tab8:
            st.write("#### " + questions[7].get("question"))
            st.write("🔹 **A)** " + questions[7].get("option_a"))
            st.write("🔹 **B)** " + questions[7].get("option_b"))
            st.write("🔹 **C)** " + questions[7].get("option_c"))
            st.write("🔹 **D)** " + questions[7].get("option_d"))
            selected_answer_q8 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_8"
                )
            if selected_answer_q8 is not None:
                selected_answer_q8_lower = selected_answer_q8.lower()
                st.session_state.selected_answer_q8_lower = selected_answer_q8_lower
        with tab9:
            st.write("#### " + questions[8].get("question"))
            st.write("🔹 **A)** " + questions[8].get("option_a"))
            st.write("🔹 **B)** " + questions[8].get("option_b"))
            st.write("🔹 **C)** " + questions[8].get("option_c"))
            st.write("🔹 **D)** " + questions[8].get("option_d"))
            selected_answer_q9 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_9"
                )
            if selected_answer_q9 is not None:
                selected_answer_q9_lower = selected_answer_q9.lower()
                st.session_state.selected_answer_q9_lower = selected_answer_q9_lower
        with tab10:
            st.write("#### " + questions[9].get("question"))
            st.write("🔹 **A)** " + questions[9].get("option_a"))
            st.write("🔹 **B)** " + questions[9].get("option_b"))
            st.write("🔹 **C)** " + questions[9].get("option_c"))
            st.write("🔹 **D)** " + questions[9].get("option_d"))
            selected_answer_q10 = st.selectbox(
                    label="Select your answer",
                    options= ['A', 'B', 'C', 'D'],
                    index=None,
                    key = "question_10"
                )
            if selected_answer_q10 is not None:
                selected_answer_q10_lower = selected_answer_q10.lower()
                st.session_state.selected_answer_q10_lower = selected_answer_q10_lower
                

            st.session_state.tester_project_name = project_name
            st.session_state.questions_sample_table_name = questions_sample_table_name
            st.session_state.tester_user_id = user_id
            st.session_state.attempts_table_name = attempts_table_name
            st.session_state.group_chat_url = group_chat_url

            st.session_state.selected_answer_q1 = selected_answer_q1
            st.session_state.selected_answer_q2 = selected_answer_q2
            st.session_state.selected_answer_q3 = selected_answer_q3
            st.session_state.selected_answer_q4 = selected_answer_q4
            st.session_state.selected_answer_q5 = selected_answer_q5
            st.session_state.selected_answer_q6 = selected_answer_q6
            st.session_state.selected_answer_q7 = selected_answer_q7
            st.session_state.selected_answer_q8 = selected_answer_q8
            st.session_state.selected_answer_q9 = selected_answer_q9
            st.session_state.selected_answer_q10 = selected_answer_q10

            st.session_state.questions = questions
            st.session_state.today_str = today_str
            
            send_answers = st.button("Send Answers", on_click = tester_execution)

    else:
        if today_results[0].get("success_rate") >= 80:
            st.success("You got **" + str(today_results[0].get("success_rate")) + "%** of today's questions right", icon = "😎")
            st.balloons()
        else:
            st.warning("You got **" + str(today_results[0].get("success_rate")) + "%** of today's questions right", icon = "🦆")
        
        st.header("Let's check your answers")
        questions = uc.run_query_6_h(f"SELECT * FROM `company-data-driven.{project_name}.{questions_sample_table_name}`;")
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Q 1", "Q 2", "Q 3", "Q 4", "Q 5", "Q 6", "Q 7", "Q 8", "Q 9", "Q 10"])
        with tab1:
            st.write("#### " + questions[0].get("question"))
            st.write("🔹 **A)** " + questions[0].get("option_a"))
            st.write("🔹 **B)** " + questions[0].get("option_b"))
            st.write("🔹 **C)** " + questions[0].get("option_c"))
            st.write("🔹 **D)** " + questions[0].get("option_d"))
            if today_results[0].get("q1_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q1_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q1_selected")).upper() + ", but right answer was " + str(questions[0].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[0].get("explanation"), icon = "⏭️")
        with tab2:
            st.write("#### " + questions[1].get("question"))
            st.write("🔹 **A)** " + questions[1].get("option_a"))
            st.write("🔹 **B)** " + questions[1].get("option_b"))
            st.write("🔹 **C)** " + questions[1].get("option_c"))
            st.write("🔹 **D)** " + questions[1].get("option_d"))
            if today_results[0].get("q2_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q2_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q2_selected")).upper() + ", but right answer was " + str(questions[1].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[1].get("explanation"), icon = "⏭️")
        with tab3:
            st.write("#### " + questions[2].get("question"))
            st.write("🔹 **A)** " + questions[2].get("option_a"))
            st.write("🔹 **B)** " + questions[2].get("option_b"))
            st.write("🔹 **C)** " + questions[2].get("option_c"))
            st.write("🔹 **D)** " + questions[2].get("option_d"))
            if today_results[0].get("q3_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q3_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q3_selected")).upper() + ", but right answer was " + str(questions[2].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[2].get("explanation"), icon = "⏭️")
        with tab4:
            st.write("#### " + questions[3].get("question"))
            st.write("🔹 **A)** " + questions[3].get("option_a"))
            st.write("🔹 **B)** " + questions[3].get("option_b"))
            st.write("🔹 **C)** " + questions[3].get("option_c"))
            st.write("🔹 **D)** " + questions[3].get("option_d"))
            if today_results[0].get("q4_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q4_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q4_selected")).upper() + ", but right answer was " + str(questions[3].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[3].get("explanation"), icon = "⏭️")
        with tab5:
            st.write("#### " + questions[4].get("question"))
            st.write("🔹 **A)** " + questions[4].get("option_a"))
            st.write("🔹 **B)** " + questions[4].get("option_b"))
            st.write("🔹 **C)** " + questions[4].get("option_c"))
            st.write("🔹 **D)** " + questions[4].get("option_d"))
            if today_results[0].get("q5_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q5_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q5_selected")).upper() + ", but right answer was " + str(questions[4].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[4].get("explanation"), icon = "⏭️")
        with tab6:
            st.write("#### " + questions[5].get("question"))
            st.write("🔹 **A)** " + questions[5].get("option_a"))
            st.write("🔹 **B)** " + questions[5].get("option_b"))
            st.write("🔹 **C)** " + questions[5].get("option_c"))
            st.write("🔹 **D)** " + questions[5].get("option_d"))
            if today_results[0].get("q6_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q6_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q6_selected")).upper() + ", but right answer was " + str(questions[5].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[5].get("explanation"), icon = "⏭️")
        with tab7:
            st.write("#### " + questions[6].get("question"))
            st.write("🔹 **A)** " + questions[6].get("option_a"))
            st.write("🔹 **B)** " + questions[6].get("option_b"))
            st.write("🔹 **C)** " + questions[6].get("option_c"))
            st.write("🔹 **D)** " + questions[6].get("option_d"))
            if today_results[0].get("q7_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q7_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q7_selected")).upper() + ", but right answer was " + str(questions[6].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[6].get("explanation"), icon = "⏭️")
        with tab8:
            st.write("#### " + questions[7].get("question"))
            st.write("🔹 **A)** " + questions[7].get("option_a"))
            st.write("🔹 **B)** " + questions[7].get("option_b"))
            st.write("🔹 **C)** " + questions[7].get("option_c"))
            st.write("🔹 **D)** " + questions[7].get("option_d"))
            if today_results[0].get("q8_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q8_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q8_selected")).upper() + ", but right answer was " + str(questions[7].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[7].get("explanation"), icon = "⏭️")
        with tab9:
            st.write("#### " + questions[8].get("question"))
            st.write("🔹 **A)** " + questions[8].get("option_a"))
            st.write("🔹 **B)** " + questions[8].get("option_b"))
            st.write("🔹 **C)** " + questions[8].get("option_c"))
            st.write("🔹 **D)** " + questions[8].get("option_d"))
            if today_results[0].get("q9_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q9_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q9_selected")).upper() + ", but right answer was " + str(questions[8].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[8].get("explanation"), icon = "⏭️")
        with tab10:
            st.write("#### " + questions[9].get("question"))
            st.write("🔹 **A)** " + questions[9].get("option_a"))
            st.write("🔹 **B)** " + questions[9].get("option_b"))
            st.write("🔹 **C)** " + questions[9].get("option_c"))
            st.write("🔹 **D)** " + questions[9].get("option_d"))
            if today_results[0].get("q10_success") == 1:
                st.success("You chose the right answer: " + str(today_results[0].get("q10_selected")).upper(), icon = "🤓")
            else:
                st.error("You chose: " + str(today_results[0].get("q10_selected")).upper() + ", but right answer was " + str(questions[9].get("correct_option")).upper(), icon = "😵‍💫")
            st.info(questions[9].get("explanation"), icon = "⏭️")

        st.toast("Remember to discuss answers with your group", icon = "🐬")
        link = f"[Discuss answers with my group]({group_chat_url})"
        st.markdown(link, unsafe_allow_html=True)
        
            


def add_question_to_test_execution():
    if st.session_state.question is None or st.session_state.option_a is None or st.session_state.option_b is None or st.session_state.option_c is None or st.session_state.option_d is None or st.session_state.letter_correct_answer is None or st.session_state.explanation is None or len(st.session_state.question) < 1 or len(st.session_state.option_a) < 1 or len(st.session_state.option_b) < 1 or len(st.session_state.option_c) < 1 or len(st.session_state.option_d) < 1 or len(st.session_state.letter_correct_answer) < 1 or len(st.session_state.explanation) < 1:
        st.toast("Please fill in completely all of the required fields.")
    else:
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.project_name}.{st.session_state.questions_table_name}` (id, creation_date, question	,option_a	,option_b	,option_c	,option_d	,correct_option	,explanation, creator_id) VALUES({st.session_state.max_id}, '{st.session_state.today_str}', '{st.session_state.question}', '{st.session_state.option_a}', '{st.session_state.option_b}', '{st.session_state.option_c}', '{st.session_state.option_d}', '{st.session_state.letter_correct_answer_lower}', '{st.session_state.cleaned_explanation}', {st.session_state.user_id});")
        st.toast("Updating, please wait", icon = "☺️")
        st.toast("Question added!", icon = "🐣")
        st.balloons()
        time.sleep(5)
        




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
        st.session_state.letter_correct_answer_lower = letter_correct_answer_lower
    explanation = st.text_input("Write the explanation:")
    if explanation is not None:
        cleaned_explanation = re.sub(r'[\"\']', '', explanation)
        st.session_state.cleaned_explanation = cleaned_explanation

    st.session_state.project_name = project_name
    st.session_state.questions_table_name = questions_table_name
    st.session_state.user_id = user_id

    st.session_state.today_str = today_str
    st.session_state.max_id = max_id
    st.session_state.question = question
    st.session_state.option_a = option_a
    st.session_state.option_b = option_b
    st.session_state.option_c = option_c
    st.session_state.option_d = option_d
    st.session_state.letter_correct_answer = letter_correct_answer
    st.session_state.confirm_letter_correct_answer = confirm_letter_correct_answer
    st.session_state.explanation = explanation
    
    add_question_button = st.button("Add question", on_click = add_question_to_test_execution)






def test_achievements(project_name, user_id, attempts_table_name): 
    # today's ranking
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    st.header("Today's top 5 ranking")
    ranking = uc.run_query_1_m(f"SELECT ROW_NUMBER() OVER(ORDER BY ta.success_rate DESC) AS position, ta.success_rate AS score, u.name, u.lastname, u.id FROM `company-data-driven.{project_name}.{attempts_table_name}` AS ta INNER JOIN `company-data-driven.global.users` AS u ON ta.user_id = u.id  WHERE attempt_date = '{today_str}' ORDER BY success_rate DESC;")
    if len(ranking) < 1:
        st.info("Waiting for user attempts", icon = "🥱")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.table(ranking[:5])
        with col2:
            user_score_and_position = [index for index, item in enumerate(ranking) if item["id"] == user_id]
            if len(user_score_and_position) < 1 or user_score_and_position is None < 0:
                st.warning(f"You have not presented your test", icon = "🫥")
            else:
                percentile = round(100 * (len(ranking)-ranking[user_score_and_position[0]].get("position"))/len(ranking))
                if percentile > 80:
                    st.success(f"You got **{ranking[user_score_and_position[0]].get('score')}%** of today's questions right", icon = "😸")
                    st.success(f"Your position today is: **{ranking[user_score_and_position[0]].get('position')}**", icon = "😸")
                    st.success(f"Today you surpassed **{percentile}%** of your classmates", icon = "😸")
                if percentile > 60 and percentile <= 80:
                    st.info(f"You got **{ranking[user_score_and_position[0]].get('score')}%** of today's questions right", icon = "😹")
                    st.info(f"Your position today is: **{ranking[user_score_and_position[0]].get('position')}**", icon = "😹")
                    st.info(f"Today you surpassed **{percentile}%** of your classmates", icon = "😹")
                if percentile > 40 and percentile <= 60:
                    st.warning(f"You got **{ranking[user_score_and_position[0]].get('score')}%** of today's questions right", icon = "😼")
                    st.warning(f"Your position today is: **{ranking[user_score_and_position[0]].get('position')}**", icon = "😼")
                    st.warning(f"Today you surpassed **{percentile}%** of your classmates", icon = "😼")
                if percentile < 40:
                    st.error(f"You got **{ranking[user_score_and_position[0]].get('score')}%** of today's questions right", icon = "🙀")
                    st.error(f"Your position today is: **{ranking[user_score_and_position[0]].get('position')}**", icon = "🙀")
                    st.error(f"Today you surpassed **{percentile}%** of your classmates", icon = "🙀")

    # your evolution
    st.header("Your evolution")
    user_score_evolution = uc.run_query_1_m(f"SELECT ROW_NUMBER() OVER(ORDER BY ta.id ASC) AS attempt, ta.attempt_date, LAG(ta.attempt_date, 1) OVER(ORDER BY ta.id ASC) AS last_attempt_date, DATE_DIFF(ta.attempt_date, LAG(ta.attempt_date, 1) OVER(ORDER BY ta.id ASC), DAY) AS days_between_tests, ta.success_rate AS score, EXTRACT(YEAR FROM ta.attempt_date) AS year_attempt_date, EXTRACT(MONTH FROM ta.attempt_date) AS month_attempt_date, EXTRACT(WEEK FROM ta.attempt_date) AS week_attempt_date FROM `company-data-driven.{project_name}.{attempts_table_name}` AS ta WHERE ta.user_id = {user_id} ORDER BY ta.id ASC;")
    if len(user_score_evolution) < 1 or user_score_evolution is None < 0:
                st.warning(f"You have not presented your test", icon = "🫥")
    else:
        user_score_evolution.sort(key=lambda x: x["attempt"])
        
        user_score_evolution_df = pd.DataFrame(user_score_evolution, columns = ["attempt","attempt_date","last_attempt_date","days_between_tests","score","year_attempt_date","month_attempt_date","week_attempt_date"])
        # user_score_evolution_df["attempt"] = user_score_evolution_df["attempt"].astype(str)
        chart_user_score_evolution = alt.Chart(user_score_evolution_df).mark_bar().encode(
            y=alt.Y('score', scale=alt.Scale(domain=[0, 100], clamp=True)),
            x=alt.X('attempt', sort='x')
        ).properties(width = 600)
        st.altair_chart(chart_user_score_evolution)

        # metrics
        st.header("Week evolution")
        corrected_week = today.isocalendar()[1] + 1 if today.isocalendar()[2] == 7 else today.isocalendar()[1]
        col1, col2, col3, col4 = st.columns(4)
        user_score_evolution_df_week = user_score_evolution_df[(user_score_evolution_df["year_attempt_date"] == today.year) & (user_score_evolution_df["month_attempt_date"] == today.month) & (user_score_evolution_df["week_attempt_date"] == corrected_week)]
        if len(user_score_evolution_df_week) < 1 or user_score_evolution_df_week is None < 0:
                st.warning(f"You have not presented your test", icon = "🫥")
        else:
            col1.metric(label="# Week Tests", value = user_score_evolution_df_week.shape[0])
            col2.metric(label="# Avg score", value = round(user_score_evolution_df_week.score.mean(),0))
            col3.metric(label="# % tests with score >= 80", value = str(round(100*(user_score_evolution_df_week['score'] >= 80).sum()/user_score_evolution_df_week.shape[0],1)))
            col4.metric(label="# Avg days between tests", value = round(user_score_evolution_df_week.days_between_tests.mean(),1))

        st.header("Month evolution")
        col1, col2, col3, col4 = st.columns(4)
        user_score_evolution_df_month = user_score_evolution_df[(user_score_evolution_df["year_attempt_date"] == today.year) & (user_score_evolution_df["month_attempt_date"] == today.month)]
        if len(user_score_evolution_df_month) < 1 or user_score_evolution_df_month is None < 0:
                st.warning(f"You have not presented your test", icon = "🫥")
        else:
            col1.metric(label="# Month Tests", value = user_score_evolution_df_month.shape[0])
            col2.metric(label="# Avg score", value = round(user_score_evolution_df_month.score.mean(),0))
            col3.metric(label="# % tests with score >= 80", value = str(round(100*(user_score_evolution_df_month['score'] >= 80).sum()/user_score_evolution_df_month.shape[0],1)))
            col4.metric(label="# Avg days between tests", value = round(user_score_evolution_df_month.days_between_tests.mean(),1))

        st.header("Total evolution")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="# Total Tests", value = user_score_evolution_df.shape[0])
        col2.metric(label="# Avg score", value = round(user_score_evolution_df.score.mean(),0))
        col3.metric(label="# % tests with score >= 80", value = str(round(100*(user_score_evolution_df['score'] >= 80).sum()/user_score_evolution_df.shape[0],1)))
        col4.metric(label="# Avg days between tests", value = round(user_score_evolution_df.days_between_tests.mean(),1))



    
