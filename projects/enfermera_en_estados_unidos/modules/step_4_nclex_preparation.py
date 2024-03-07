import streamlit as st
import os

import utils.user_credentials as uc

def study_plan_execution(study_plan_user_id, study_plan_project_id, study_plan_project_name, study_plan_selected_user_id, study_plan_selected_contract_id):
  st.toast(study_plan_selected_user_id)

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
  selected_username = st.selectbox(
          label = "Select the username",
          options = usernames,
          index = None,
          key= "usernames"
      )
  checking_username = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{selected_username}';")
  if len(checking_username) < 1 or checking_username is None:
      st.error('User does not exists', icon = '👻')
  else:
      st.success('User confirmed!', icon = '🪬')
      if selected_username is not None:
          study_plan_user_id = user_id
          study_plan_project_id = project_id
          study_plan_project_name = project_name
          study_plan_selected_user_id = ids[usernames.index(selected_username)]
          study_plan_selected_contract_id = contract_ids[usernames.index(selected_username)]
          study_plan_button = st.button("Create Study plan", on_click = study_plan_execution, args = [study_plan_user_id, study_plan_project_id, study_plan_project_name, study_plan_selected_user_id, study_plan_selected_contract_id])

