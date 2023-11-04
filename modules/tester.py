import streamlit as st
import datetime
import re
import webbrowser

import utils.user_credentials as uc

# https://docs.streamlit.io/library/api-reference/status

def tester(project_name, questions_sample_table_name, user_id, attempts_table_name, group_chat_url): 
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    today_results = uc.run_query_instant(f"SELECT * FROM `company-data-driven.{project_name}.{attempts_table_name}` WHERE user_id = {user_id} AND attempt_date = '{today_str}';")
    if len(today_results) < 1:
        questions = uc.run_query_6_h(f"SELECT * FROM `company-data-driven.{project_name}.{questions_sample_table_name}`;")
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
                )
            if selected_answer_q1 is not None:
                selected_answer_q1_lower = selected_answer_q1.lower()
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
                )
            if selected_answer_q2 is not None:
                selected_answer_q2_lower = selected_answer_q2.lower()
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
                )
            if selected_answer_q3 is not None:
                selected_answer_q3_lower = selected_answer_q3.lower()
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
                )
            if selected_answer_q4 is not None:
                selected_answer_q4_lower = selected_answer_q4.lower()
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
                )
            if selected_answer_q5 is not None:
                selected_answer_q5_lower = selected_answer_q5.lower()
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
                )
            if selected_answer_q6 is not None:
                selected_answer_q6_lower = selected_answer_q6.lower()
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
                )
            if selected_answer_q7 is not None:
                selected_answer_q7_lower = selected_answer_q7.lower()
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
                )
            if selected_answer_q8 is not None:
                selected_answer_q8_lower = selected_answer_q8.lower()
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
                )
            if selected_answer_q9 is not None:
                selected_answer_q9_lower = selected_answer_q9.lower()
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
                )
            if selected_answer_q10 is not None:
                selected_answer_q10_lower = selected_answer_q10.lower()
            send_answers = st.button("Send Answers")
            if send_answers:
                if selected_answer_q1 is None or selected_answer_q2 is None or selected_answer_q3 is None or selected_answer_q4 is None or selected_answer_q5 is None or selected_answer_q6 is None or selected_answer_q7 is None or selected_answer_q8 is None or selected_answer_q9 is None or selected_answer_q10 is None:
                    st.error("you forgot to answer at least one question", icon = "🤧")
                else:
                    correct_q_1 = 1 if selected_answer_q1_lower == questions[0].get("correct_option") else 0
                    correct_q_2 = 1 if selected_answer_q2_lower == questions[1].get("correct_option") else 0
                    correct_q_3 = 1 if selected_answer_q3_lower == questions[2].get("correct_option") else 0
                    correct_q_4 = 1 if selected_answer_q4_lower == questions[3].get("correct_option") else 0
                    correct_q_5 = 1 if selected_answer_q5_lower == questions[4].get("correct_option") else 0
                    correct_q_6 = 1 if selected_answer_q6_lower == questions[5].get("correct_option") else 0
                    correct_q_7 = 1 if selected_answer_q7_lower == questions[6].get("correct_option") else 0
                    correct_q_8 = 1 if selected_answer_q8_lower == questions[7].get("correct_option") else 0
                    correct_q_9 = 1 if selected_answer_q9_lower == questions[8].get("correct_option") else 0
                    correct_q_10 = 1 if selected_answer_q10_lower == questions[9].get("correct_option") else 0
                    success_rate = 100 * ((correct_q_1 + correct_q_2 + correct_q_3 + correct_q_4 + correct_q_5 + correct_q_6 + correct_q_7 + correct_q_8 + correct_q_9 + correct_q_10)/10)
                    
                    max_id = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.{project_name}.{attempts_table_name}`;")[0].get("max_id") 
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.{attempts_table_name}` VALUES({max_id},'{today_str}', {user_id},{questions[0].get('id')},{correct_q_1},{questions[1].get('id')},{correct_q_2},{questions[2].get('id')},{correct_q_3},{questions[3].get('id')},{correct_q_4},{questions[4].get('id')},{correct_q_5},{questions[5].get('id')},{correct_q_6},{questions[6].get('id')},{correct_q_7},{questions[7].get('id')},{correct_q_8},{questions[8].get('id')},{correct_q_9},{questions[9].get('id')},{correct_q_10},{success_rate}, '{selected_answer_q1_lower}', '{selected_answer_q2_lower}', '{selected_answer_q3_lower}', '{selected_answer_q4_lower}', '{selected_answer_q5_lower}', '{selected_answer_q6_lower}', '{selected_answer_q7_lower}', '{selected_answer_q8_lower}', '{selected_answer_q9_lower}', '{selected_answer_q10_lower}');")         
                    st.info("Test sent", icon = "☺️")
                    
                    # st.rerun()
    else:
        if today_results[0].get("success_rate") > 80:
            st.success("You got **" + str(today_results[0].get("success_rate")) + "%** of today's questions right", icon = "😎")
            st.balloons()
        else:
            st.warning("You got **" + str(today_results[0].get("success_rate")) + "%** of today's questions right", icon = "🦆")
        
        st.header("Let's check your answers")
        questions = uc.run_query_6_h(f"SELECT * FROM `company-data-driven.{project_name}.{questions_sample_table_name}`;")
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["Q 1", "Q 2", "Q 3", "Q 4", "Q 5", "Q 6", "Q 7", "Q 8", "Q 9", "Q 10"])
        with tab1:
            st.header(questions[0].get("question"))
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
            st.header(questions[1].get("question"))
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
            st.header(questions[2].get("question"))
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
            st.header(questions[3].get("question"))
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
            st.header(questions[4].get("question"))
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
            st.header(questions[5].get("question"))
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
            st.header(questions[6].get("question"))
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
            st.header(questions[7].get("question"))
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
            st.header(questions[8].get("question"))
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
            st.header(questions[9].get("question"))
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
            st.write(ranking[user_score_and_position[0]])
    pass

    
