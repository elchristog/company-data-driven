import streamlit as st
import os
import time

import utils.user_credentials as uc

def study_plan_execution(study_plan_selected_username, study_plan_user_id, study_plan_project_id, study_plan_project_name, study_plan_selected_user_id, study_plan_selected_contract_id):
  os.write(1, '🥏 Executing study_plan_execution \n'.encode('utf-8'))
  st.toast("Updating, please wait", icon = "☺️")
  
  last_user_tests = uc.run_query_half_day(f'''
    SELECT na.attempt_date, nq1.question AS q1question, nq1.option_a AS q1option_a, nq1.option_b AS q1option_b, nq1.option_c AS q1option_c, nq1.option_d AS q1option_d, nq1.correct_option AS q1correct_option, nq1.explanation AS q1_explanation, na.q1_selected, na.q1_success, nq2.question AS q2question, nq2.option_a AS q2option_a, nq2.option_b AS q2option_b, nq2.option_c AS q2option_c, nq2.option_d AS q2option_d, nq2.correct_option AS q2correct_option, nq2.explanation AS q2_explanation, na.q2_selected, na.q2_success, nq3.question AS q3question, nq3.option_a AS q3option_a, nq3.option_b AS q3option_b, nq3.option_c AS q3option_c, nq3.option_d AS q3option_d, nq3.correct_option AS q3correct_option, nq3.explanation AS q3_explanation, na.q3_selected, na.q3_success, nq4.question AS q4question, nq4.option_a AS q4option_a, nq4.option_b AS q4option_b, nq4.option_c AS q4option_c, nq4.option_d AS q4option_d, nq4.correct_option AS q4correct_option, nq4.explanation AS q4_explanation, na.q4_selected, na.q4_success, nq5.question AS q5question, nq5.option_a AS q5option_a, nq5.option_b AS q5option_b, nq5.option_c AS q5option_c, nq5.option_d AS q5option_d, nq5.correct_option AS q5correct_option, nq5.explanation AS q5_explanation, na.q5_selected, na.q5_success, nq6.question AS q6question, nq6.option_a AS q6option_a, nq6.option_b AS q6option_b, nq6.option_c AS q6option_c, nq6.option_d AS q6option_d, nq6.correct_option AS q6correct_option, nq6.explanation AS q6_explanation, na.q6_selected, na.q6_success, nq7.question AS q7question, nq7.option_a AS q7option_a, nq7.option_b AS q7option_b, nq7.option_c AS q7option_c, nq7.option_d AS q7option_d, nq7.correct_option AS q7correct_option, nq7.explanation AS q7_explanation, na.q7_selected, na.q7_success, nq8.question AS q8question, nq8.option_a AS q8option_a, nq8.option_b AS q8option_b, nq8.option_c AS q8option_c, nq8.option_d AS q8option_d, nq8.correct_option AS q8correct_option, nq8.explanation AS q8_explanation, na.q8_selected, na.q8_success, nq9.question AS q9question, nq9.option_a AS q9option_a, nq9.option_b AS q9option_b, nq9.option_c AS q9option_c, nq9.option_d AS q9option_d, nq9.correct_option AS q9correct_option, nq9.explanation AS q9_explanation, na.q9_selected, na.q9_success, nq10.question AS q10question, nq10.option_a AS q10option_a, nq10.option_b AS q10option_b, nq10.option_c AS q10option_c, nq10.option_d AS q10option_d, nq10.correct_option AS q10correct_option, nq10.explanation AS q10_explanation, na.q10_selected, na.q10_success FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq1 ON na.q1_id = nq1.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq2 ON na.q2_id = nq2.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq3 ON na.q3_id = nq3.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq4 ON na.q4_id = nq4.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq5 ON na.q5_id = nq5.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq6 ON na.q6_id = nq6.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq7 ON na.q7_id = nq7.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq8 ON na.q8_id = nq8.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq9 ON na.q9_id = nq9.id INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq10 ON na.q10_id = nq10.id WHERE user_id = {study_plan_selected_user_id} ORDER BY na.attempt_date DESC LIMIT 4;
  ''')

  st.write(last_user_tests)
  
  st.toast('Study Plan Created!', icon = '🎈')
  st.balloons()
  time.sleep(1)
  del st.session_state['study_plan_selected_username']
  del st.session_state['study_plan_user_id']
  del st.session_state['study_plan_project_id']
  del st.session_state['study_plan_project_name']
  del st.session_state['study_plan_selected_user_id']
  del st.session_state['study_plan_selected_contract_id']
  




def study_plan(user_id, project_id, project_name):
  os.write(1, '🥏 Executing study_plan \n'.encode('utf-8'))
  os.write(1, '- study_plan: Retrieving users \n'.encode('utf-8'))
  rows = uc.run_query_half_day(f"SELECT u.id, u.username, c.id as contract_id FROM `company-data-driven.{project_name}.contracts` AS c INNER JOIN `company-data-driven.global.users` AS u ON u.id = c.user_id;")
  ids = []
  usernames = []
  contract_ids = []
  for row in rows:
      ids.append(row.get('id'))
      usernames.append(row.get('username'))
      contract_ids.append(row.get('contract_id'))

  if 'study_plan_selected_username' not in st.session_state:
      selected_username = st.selectbox(
              label = "Select the username",
              options = usernames,
              index = 0,
              key= "usernames"
          )
      st.session_state.study_plan_selected_username = selected_username
      if st.session_state.study_plan_selected_username is not None:
            st.session_state.study_plan_selected_username_index  = usernames.index(st.session_state.study_plan_selected_username)
  else:
      selected_username = st.selectbox(
              label = "Select the username",
              options = usernames,
              index = st.session_state.study_plan_selected_username_index,
              key= "usernames"
          )
      st.session_state.study_plan_selected_username = selected_username
      if st.session_state.study_plan_selected_username is not None:
            st.session_state.study_plan_selected_username_index  = usernames.index(st.session_state.study_plan_selected_username)

  if selected_username is not None:
      st.session_state.study_plan_user_id = user_id
      st.session_state.study_plan_project_id = project_id
      st.session_state.study_plan_project_name = project_name
      st.session_state.study_plan_selected_user_id = ids[usernames.index(selected_username)]
      st.session_state.study_plan_selected_contract_id = contract_ids[usernames.index(selected_username)]
    
      study_plan_button = st.button("Create Study plan", on_click = study_plan_execution, args = [st.session_state.study_plan_selected_username, st.session_state.study_plan_user_id, st.session_state.study_plan_project_id, st.session_state.study_plan_project_name, st.session_state.study_plan_selected_user_id, st.session_state.study_plan_selected_contract_id])

