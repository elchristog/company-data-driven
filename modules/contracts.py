
import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re
import os

from datetime import datetime as dtt
from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_c(df_grouped):
    df_grouped['date'] = df_grouped['date'].astype(str)

    options = {
        "xAxis": {
            "type": "category",
            "data": df_grouped['date'].tolist(),
            "axisLabel": {
                "formatter": "{value}"
            }
        },
        "yAxis": {"type": "value", "name": ""},
        "grid": {
            "right": 20,
            "left": 65,
            "top": 45,
            "bottom": 50,
        },
        "legend": {
            "show": True,
            "top": "top",
            "align": "auto",
            "selected": {  
                "num_assistants_groupal_session": True,    
                "num_contracts": True
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "num_assistants_groupal_session",
                "data": df_grouped["num_assistants_groupal_session"].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "num_contracts",
                "data": df_grouped['num_contracts'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,
            }
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  
        ],
        "backgroundColor": "#ffffff",
        "color": ["#A6785D", "#394A59"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')




def contracts_show_metrics(project_name):
  dates_groupal_meeting = uc.run_query_1_h(f"SELECT MIN(meeting_date) AS min_date_gm, MAX(meeting_date) AS max_date_gm, CURRENT_DATE() AS todays_date FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance`;")

  if len(dates_groupal_meeting) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (dates_groupal_meeting[0].get('min_date_gm'), dates_groupal_meeting[0].get('todays_date')),
          min_value=dates_groupal_meeting[0].get('min_date_gm'),
          max_value=dates_groupal_meeting[0].get('todays_date'),
          format="DD/MM/YYYY",
          help='',
          key = 'day_contract'
      )

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT COALESCE(groupal_session_assistants.date, contracts_counts.date) AS date, COALESCE(num_assistants_groupal_session,0) AS num_assistants_groupal_session, COALESCE(num_contracts,0) AS num_contracts FROM (SELECT meeting_date AS date, COUNT(id) AS num_assistants_groupal_session FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` WHERE meeting_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  meeting_date <= '{day[1].strftime('%Y-%m-%d')}' AND status = 'assistant' GROUP BY meeting_date) AS groupal_session_assistants FULL OUTER JOIN (SELECT contract_date AS date, COUNT(id) AS num_contracts FROM `company-data-driven.{project_name}.contracts` WHERE contract_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  contract_date <= '{day[1].strftime('%Y-%m-%d')}' GROUP BY contract_date) contracts_counts ON groupal_session_assistants.date = contracts_counts.date  ORDER BY COALESCE(groupal_session_assistants.date, contracts_counts.date) ASC;"))

      num_assistants_groupal_session = df_conversion['num_assistants_groupal_session'].sum()
      num_contracts = df_conversion['num_contracts'].sum()
      conversion = num_contracts/num_assistants_groupal_session
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('num_assistants_groupal_session:', f'{num_assistants_groupal_session:,}')
      with met2:
          st.metric('num_contracts:', f'{num_contracts:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_c(df_conversion)






def customer_creation_execution():
    checking_username_query = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{st.session_state.username_customer_creation}';")
    if len(checking_username_query) < 1:
        checking_user_role = []
    else:
        checking_user_role = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.role_assignment` WHERE user_id = {checking_username_query[0].get('id')};")
    if len(st.session_state.username_customer_creation) < 6:
        st.toast("The username must be at least 6 characters long.")
    if len(st.session_state.checking_username_query_customer_creation) > 0:
        st.toast("The username is already in use.")
    if len(checking_user_role) > 0:
        st.toast("The username already has a role.")
    if st.session_state.selected_project_customer_creation is None:
        st.toast("Please select a project.")
    if st.session_state.user_first_name_customer_creation is None:
        st.toast("Please enter your first name.")
    if len(st.session_state.user_first_name_customer_creation) < 3:
        st.toast("The first name must be at least 3 characters long.")
    if st.session_state.user_last_name_customer_creation is None:
        st.toast("Please enter your last name.")
    if len(st.session_state.user_last_name_customer_creation) < 3:
        st.toast("The last name must be at least 3 characters long.")
    if st.session_state.user_email_customer_creation is None:
        st.toast("Please enter your email address.")
    if len(st.session_state.user_email_customer_creation) < 3:
        st.toast("The email address must be at least 3 characters long.")
    if st.session_state.user_birth_date_customer_creation is None:
        st.toast("Please enter your birth date.")
    if st.session_state.user_country_customer_creation is None:
        st.toast("Please select your country.")
    if len(st.session_state.user_country_customer_creation) < 3:
        st.toast("The country name must be at least 3 characters long.")
    if st.session_state.user_gender_customer_creation is None:
        st.toast("Please select your gender.")
    if len(st.session_state.user_gender_customer_creation) < 3:
        st.toast("The gender must be at least 3 characters long.")
    if st.session_state.user_phone_number_customer_creation is None:
        st.toast("Please enter your phone number.")
    if len(st.session_state.user_phone_number_customer_creation) < 6:
        st.toast("The phone number must be at least 6 characters long.")
    if st.session_state.user_drive_folder_customer_creation is None:
        st.toast("Please enter the Drive URL.")
    if len(st.session_state.user_drive_folder_customer_creation) < 6:
        st.toast("The Drive URL must be at least 6 characters long.")
    if len(st.session_state.username_customer_creation) < 6 or len(st.session_state.checking_username_query_customer_creation) > 0 or len(checking_user_role) > 0 or st.session_state.selected_project_customer_creation is None or st.session_state.user_first_name_customer_creation is None or len(st.session_state.user_first_name_customer_creation) < 3 or st.session_state.user_last_name_customer_creation is None or len(st.session_state.user_last_name_customer_creation) < 3 or st.session_state.user_email_customer_creation is None or len(st.session_state.user_email_customer_creation) < 3  or st.session_state.user_birth_date_customer_creation is None or st.session_state.user_country_customer_creation is None or len(st.session_state.user_country_customer_creation) < 3 or st.session_state.user_gender_customer_creation is None or len(st.session_state.user_gender_customer_creation) < 3 or st.session_state.user_phone_number_customer_creation is None or len(st.session_state.user_phone_number_customer_creation) < 6 or st.session_state.user_drive_folder_customer_creation is None or len(st.session_state.user_drive_folder_customer_creation) < 6:
        st.toast("Please fill in completely all of the required fields.")
    else:
        st.toast("Updating, please wait", icon = "☺️")
        
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.users` (id, username, status, project_id, creation_date, email, name, lastname, birthdate, country, gender, user_creator_id, phone_number, user_drive_folder) VALUES({st.session_state.max_id_users_customer_creation}, '{st.session_state.username_customer_creation}', 'active', {st.session_state.project_id_customer_creation}, '{st.session_state.today_str_customer_creation}', '{st.session_state.user_email_customer_creation.lower()}', '{st.session_state.user_first_name_customer_creation.lower()}', '{st.session_state.user_last_name_customer_creation.lower()}', '{st.session_state.user_birth_date_customer_creation}', '{st.session_state.user_country_customer_creation.lower()}', '{st.session_state.user_gender_customer_creation.lower()}', {st.session_state.user_id_customer_creation}, '{st.session_state.user_phone_number_customer_creation}', '{st.session_state.user_drive_folder_customer_creation}');")
        
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.role_assignment` (id, user_id, role_id) VALUES({st.session_state.max_id_role_assignement_customer_creation}, {st.session_state.max_id_users_customer_creation}, {st.session_state.selected_role_id_customer_creation});")
        
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.project_name_customer_creation}.contracts` (id, contract_date, user_id, traffic_analytics_whatsapp_leads_id, contract_total_value, contract_agreed_payments, creator_user_id) VALUES (GENERATE_UUID(), '{st.session_state.today_str_customer_creation}', {st.session_state.max_id_users_customer_creation}, '{st.session_state.selected_phone_id}','{st.session_state.contract_value_customer_creation}', '{st.session_state.contract_num_payments_customer_creation}', {st.session_state.user_id_customer_creation});")
        st.toast('User Created!', icon = '🎈')
        st.balloons()
        st.warning('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        st.toast('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        time.sleep(5)
        uc.run_query_30_m.clear()
        
        




def customer_creation(user_id_customer_creation, project_id, project_name): 
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    username = st.text_input("Write the username:")
    checking_username_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{username}';")
    if len(checking_username_query) > 0 or len(username) < 6 or username is None:
        st.error('Username is not available', icon = '👻')
    else:
        st.success('Username available', icon = '🪬')
    max_id_users = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.global.users`;")[0].get('max_id')
    max_id_role_assignement = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.global.role_assignment`;")[0].get('max_id')


    user_first_name = st.text_input("Write the user first name:")
    user_last_name = st.text_input("Write the user last name:")
    user_email = st.text_input("Write the user email:")
    
    rows = uc.run_query_half_day(f"SELECT id, CONCAT(phone_indicator,phone_number) AS full_phone_number FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
    assistant_ids = []
    assistant_phone_numbers = []
    for row in rows:
        assistant_ids.append(row.get('id'))
        assistant_phone_numbers.append(row.get('full_phone_number'))
    user_phone_number = st.selectbox(
            label = "Select the user phone number",
            options = assistant_phone_numbers,
            index = None,
            key= "user_phone_number"
        )
    checking_phone_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE CONCAT(phone_indicator,phone_number) LIKE '{user_phone_number}' ")
    if len(checking_phone_query) < 1 or checking_phone_query is None:
        st.error('Phone number does not exists, should be created adding a new lead into Whatsapp', icon = '👻')
    else:
        st.success('Phone number available', icon = '🪬')
        if user_phone_number is not None:
            selected_phone_id = assistant_ids[assistant_phone_numbers.index(user_phone_number)]
            st.session_state.selected_phone_id = selected_phone_id


    
    user_birth_date = st.date_input("User birth date:", min_value = datetime.date(1970,1,1)) 
    user_country = st.selectbox(
        label = "Select user country",
        options = ['colombia', 'united states', 'el salvador', 'mexico', 'venezuela', 'costa rica', 'chile', 'peru'],
        index = None
    )
    user_gender = st.selectbox(
        label = "Select user gender",
        options = ['male', 'female'],
        index = None
    )
    user_drive_folder = st.text_input("Write the user Google Drive folder url:")
    contract_value = st.text_input("Contract Total Value (USD):", help = "Not dots, just numbers", placeholder = "1200")
    contract_num_payments = st.text_input("Contract num payments:", help = "Number of agreed payments", placeholder = "2")
    
    
    st.session_state.user_id_customer_creation = user_id_customer_creation
    st.session_state.project_id_customer_creation = project_id
    st.session_state.project_name_customer_creation = project_name
    st.session_state.username_customer_creation = username
    st.session_state.checking_username_query_customer_creation = checking_username_query
    st.session_state.selected_project_customer_creation = project_name
    st.session_state.selected_role_id_customer_creation = 6
    st.session_state.user_first_name_customer_creation = user_first_name
    st.session_state.user_last_name_customer_creation = user_last_name
    st.session_state.user_email_customer_creation = user_email
    st.session_state.user_birth_date_customer_creation = user_birth_date
    st.session_state.user_country_customer_creation = user_country
    st.session_state.user_gender_customer_creation = user_gender
    st.session_state.user_phone_number_customer_creation = user_phone_number
    st.session_state.user_drive_folder_customer_creation = user_drive_folder
    st.session_state.contract_value_customer_creation = contract_value
    st.session_state.contract_num_payments_customer_creation = contract_num_payments
    st.session_state.today_str_customer_creation = today_str
    st.session_state.max_id_users_customer_creation = max_id_users
    st.session_state.max_id_role_assignement_customer_creation = max_id_role_assignement
    
    create_user_button = st.button("Create User", on_click = customer_creation_execution)












def contract_payments_show_metrics(project_name):
  dates_payments = uc.run_query_1_h(f"SELECT MIN(payment_date) AS min_payment_date, CURRENT_DATE() AS max_payment_date FROM `company-data-driven.{project_name}.contracts_payments` AS cp;")
  if len(dates_payments) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (dates_payments[0].get('min_payment_date'), dates_payments[0].get('max_payment_date')),
          min_value=dates_payments[0].get('min_payment_date'),
          max_value=dates_payments[0].get('max_payment_date'),
          format="DD/MM/YYYY",
          help='',
          key = 'day_payments'
      )


      df_sales = pd.DataFrame(uc.run_query_1_h(f"SELECT SUM(CAST(c.contract_total_value AS FLOAT64)) AS total_sales FROM `company-data-driven.{project_name}.contracts` AS c WHERE c.contract_date >= '{day[0].strftime('%Y-%m-%d')}' AND c.contract_date <= '{day[1].strftime('%Y-%m-%d')}';"))

      df_payments = pd.DataFrame(uc.run_query_1_h(f"SELECT SUM(CAST(cp.payment_value AS FLOAT64)) AS total_paid FROM `company-data-driven.{project_name}.contracts_payments` AS cp WHERE cp.payment_date >= '{day[0].strftime('%Y-%m-%d')}' AND cp.payment_date <= '{day[1].strftime('%Y-%m-%d')}';"))
      
      total_sales = df_sales['total_sales'].sum()
      total_paid = df_payments['total_paid'].sum()
      total_debt = total_sales-total_paid
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('total_sales:', f'{total_sales:,}')
      with met2:
          st.metric('total_paid:', f'{total_paid:,}')
      with met3:
          st.metric('total_debt:', f'{total_debt:,}')

      st.write("---")

      df_delayed_payments = pd.DataFrame(uc.run_query_1_h(f"SELECT u.username, c.contract_total_value, payments.total_paid, payments.last_payment_date FROM `company-data-driven.{project_name}.contracts` AS c INNER JOIN (SELECT cp.contract_id, SUM(CAST(cp.payment_value AS FLOAT64)) AS total_paid, MAX(cp.payment_date) AS last_payment_date FROM `company-data-driven.{project_name}.contracts_payments` AS cp GROUP BY cp.contract_id) AS payments ON c.id = payments.contract_id INNER JOIN `company-data-driven.global.users` AS u ON c.user_id = u.id WHERE CAST(c.contract_total_value AS FLOAT64) > payments.total_paid  AND DATE_DIFF(CURRENT_DATE(), payments.last_payment_date, DAY) > 30 ORDER BY payments.last_payment_date ASC;"))

      st.write("**Delayed payments**")
      if len(df_delayed_payments) < 1:
          st.success("No delayed payments", icon = "🦈")
      else:
          st.table(df_delayed_payments)






def add_new_contract_payment_execution(user_id, project_name, selected_contract_id, payment_date, payment_value, contract_total_value, total_paid, current_debt, last_payment_date):
  if payment_value is None:
    st.toast("payment_value can not be null", icon="🤨")
  else:
    if current_debt <= 0:
      st.toast("User does not have debts", icon="🤨")
    else:
      if int(payment_value) > int(current_debt):
        st.toast("Payment can't be bigger than debt", icon="🤨")
      else:  
        if len(last_payment_date) < 6:  # Check for null string
            st.toast("Please wait", icon="☺️")
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.contracts_payments` (id, contract_id, payment_value, payment_date, creator_id) VALUES (GENERATE_UUID(), '{selected_contract_id}', '{payment_value}', '{payment_date}', {user_id});")
            st.toast("Payment saved!", icon="👾")
            st.balloons()
            time.sleep(5)
            uc.run_query_1_h.clear()  
        else:
            last_payment_date = dtt.strptime(last_payment_date, '%Y-%m-%d').date()
            if payment_date <= last_payment_date:
                st.toast("Payment can't be before last payment", icon="🤨")
            else:  # Proceed if the date check passes
                st.toast("Please wait", icon="☺️")
                uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.contracts_payments` (id, contract_id, payment_value, payment_date, creator_id) VALUES (GENERATE_UUID(), '{selected_contract_id}', '{payment_value}', '{payment_date}', {user_id});")
                st.toast("Payment saved!", icon="👾")
                st.balloons()
                time.sleep(5)
            uc.run_query_1_h.clear() 
                




def add_new_contract_payment(user_id, project_id, project_name):
    rows = uc.run_query_half_day(f"SELECT u.username, c.id as contract_id FROM `company-data-driven.{project_name}.contracts` AS c INNER JOIN `company-data-driven.global.users` AS u ON u.id = c.user_id;")
    usernames = []
    contract_ids = []
    for row in rows:
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
            selected_contract_id = contract_ids[usernames.index(selected_username)]
            user_debt = uc.run_query_instant(f'''
           SELECT 
                CAST(ROUND(CAST(c.contract_total_value AS NUMERIC)) AS INT64) AS contract_total_value, 
                CAST(ROUND(CAST(total_payments.total_paid AS NUMERIC)) AS INT64) AS total_paid, 
                ROUND(CAST(c.contract_total_value AS NUMERIC), 0) AS current_debt, 
                total_payments.last_payment_date 
            FROM `company-data-driven.{project_name}.contracts` AS c 
            LEFT JOIN (
                SELECT 
                    cp.contract_id, 
                    SUM(CAST(ROUND(CAST(cp.payment_value AS NUMERIC)) AS INT64)) AS total_paid, 
                    MAX(cp.payment_date) AS last_payment_date 
                FROM `company-data-driven.{project_name}.contracts_payments` AS cp 
                WHERE cp.contract_id = '{selected_contract_id}' 
                GROUP BY cp.contract_id
            ) AS total_payments 
            ON c.id = total_payments.contract_id 
            WHERE c.id = '{selected_contract_id}'; 
            ''')
            contract_total_value = user_debt[0].get('contract_total_value')
            total_paid = user_debt[0].get('total_paid')
            current_debt = user_debt[0].get('current_debt')
            last_payment_date = str(user_debt[0].get('last_payment_date'))
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label="Contract total value", value = contract_total_value)
            col2.metric(label="Total paid", value = total_paid)
            col3.metric(label="Current debt", value = str(current_debt))
            col4.metric(label="Last payment date", value = last_payment_date[-8:])

            payment_date = st.date_input("Payment date:", key = 'payment_date')
            payment_value = st.number_input("Payment value (USD):", key = 'payment_value', placeholder = 325, help = "Do not use dots, just numbers")
            add_payment_button = st.button("Add payment", on_click = add_new_contract_payment_execution, args = [user_id, project_name, selected_contract_id, payment_date, payment_value, contract_total_value, total_paid, current_debt, last_payment_date])















def add_new_crm_contact_execution(user_id, project_name, selected_phone_id, contact_date, user_status, contact_description):
    last_contact_date = uc.run_query_instant(f"SELECT MAX(contact_date) AS last_contact_date FROM `company-data-driven.{project_name}.contract_crm_log` WHERE traffic_analytics_whatsapp_leads_id = '{selected_phone_id}';")
    
    if contact_description is None:
        st.toast("contact_description can not be null", icon = "☺️")
    if len(contact_description) < 36:
        st.toast("contact_description too short", icon = "☺️")
    if user_status is None:
        st.toast("user_status can not be null", icon = "☺️")
    if last_contact_date[0].get("last_contact_date") is not None:
        if contact_date <= last_contact_date[0].get("last_contact_date"):
            st.toast("User already contacted on that date", icon = "☺️")
    if (contact_description is not None) and (user_status is not None) and (len(contact_description) >= 36):
        if last_contact_date[0].get("last_contact_date") is None:
            st.toast("Please wait", icon = "☺️")
            contact_description = ''.join(i for i in contact_description if not i.isdigit())
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.contract_crm_log` (id, contact_date, traffic_analytics_whatsapp_leads_id, creator_id, user_status, contact_description) VALUES (GENERATE_UUID(), '{contact_date}', '{selected_phone_id}', {user_id}, '{user_status}', '{contact_description}');")
            st.toast("CRM Contact saved!", icon = "👾")
            st.balloons()
            time.sleep(5)
            uc.run_query_half_day.clear()
            uc.run_query_30_m.clear()
        else:
            if contact_date > last_contact_date[0].get("last_contact_date"):
                st.toast("Please wait", icon = "☺️")
                uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.contract_crm_log` (id, contact_date, traffic_analytics_whatsapp_leads_id, creator_id, user_status, contact_description) VALUES (GENERATE_UUID(), '{contact_date}', '{selected_phone_id}', {user_id}, '{user_status}', '{contact_description}');")
                st.toast("CRM Contact saved!", icon = "👾")
                st.balloons()
                time.sleep(5)
                uc.run_query_half_day.clear()
                uc.run_query_30_m.clear()
                uc.run_query_1_h.clear()
                
        




def add_new_crm_contact(user_id, project_name):
    rows = uc.run_query_half_day(f"SELECT DISTINCT tawl.id, CONCAT(tawl.phone_indicator,tawl.phone_number) AS full_phone_number, last_user_status_df.last_user_status FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl INNER JOIN `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` AS tagsa ON tawl.id = tagsa.traffic_analytics_whatsapp_lead_id LEFT OUTER JOIN (SELECT traffic_analytics_whatsapp_leads_id, LAST_VALUE(user_status) OVER(PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date) AS last_user_status FROM `company-data-driven.{project_name}.contract_crm_log`) AS last_user_status_df ON tawl.id = last_user_status_df.traffic_analytics_whatsapp_leads_id WHERE tagsa.status = 'assistant' AND tawl.id NOT IN (SELECT traffic_analytics_whatsapp_leads_id FROM `company-data-driven.{project_name}.contracts`) AND (last_user_status_df.last_user_status LIKE '%active%' OR last_user_status_df.last_user_status IS NULL);")
    assistant_ids = []
    assistant_phone_numbers = []
    for row in rows:
        assistant_ids.append(row.get('id'))
        assistant_phone_numbers.append(row.get('full_phone_number'))
    selected_phone = st.selectbox(
            label = "Select the user phone number",
            options = assistant_phone_numbers,
            index = None,
            key= "assistant_phone_numbers"
        )
    checking_phone_query = uc.run_query_30_m(f"SELECT awl.id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS awl INNER JOIN `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` AS tagsa ON awl.id = tagsa.traffic_analytics_whatsapp_lead_id WHERE CONCAT(awl.phone_indicator,awl.phone_number) LIKE '{selected_phone}';")
    if len(checking_phone_query) < 1 or checking_phone_query is None:
        st.error('Phone number does not exists, be sure this user assisted at the groupal session', icon = '👻')
    else:
        st.success('Phone number available', icon = '🪬')
        if selected_phone is not None:
            selected_phone_id = assistant_ids[assistant_phone_numbers.index(selected_phone)]
            
            user_history = uc.run_query_instant(f'''
                SELECT 'contract' AS funnel_step, contact_date, user_status, contact_description FROM `company-data-driven.{project_name}.contract_crm_log` WHERE traffic_analytics_whatsapp_leads_id = '{selected_phone_id}'
                UNION ALL (
                  SELECT 'groupal_session' AS funnel_step, contact_date, user_status, contact_description FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` WHERE traffic_analytics_whatsapp_leads_id = '{selected_phone_id}'
                ) ORDER BY contact_date ASC;
            ''')
            st.table(user_history)

            contact_date = st.date_input("Contact date:", key = 'contact_date')
            user_status = st.selectbox(
                label = "Select the user status",
                options = ['active', 'active_15_days', 'active_30_days', 'active_60_days', 'lost', 'discarted'],
                index = None,
                key= "user_status",
                placeholder = "active",
                help = "active = active oportunity, active_x_days = active oportunity, but wait x days to next contact, lost = the user reject the process, discarted = the user does not meet the requirements such as nurses from cuba or auxiliaries"
            )
            contact_description = st.text_input("Contact description", placeholder = "Se contacta entregando enlace de pago y contrato")
            add_contact_button = st.button("Add CRM contact", on_click = add_new_crm_contact_execution, args = [user_id, project_name, selected_phone_id, contact_date, user_status, contact_description])








def contracts_crm_show_metrics(project_name):
    os.write(1, '🥏 Executing contracts_crm_show_metrics \n'.encode('utf-8'))
    os.write(1, '- contracts_crm_show_metrics: Getting data \n'.encode('utf-8'))
    contracts_crm_oportunities = uc.run_query_instant(f"SELECT    CONCAT(tawl.phone_indicator, tawl.phone_number) AS full_phone_number,   (COALESCE(DATE_DIFF(CURRENT_DATE(), last_user_status_df.last_contact_date, DAY), 99999)      - CASE        WHEN last_user_status_df.last_user_status LIKE '%15%' THEN 15        WHEN last_user_status_df.last_user_status LIKE '%30%' THEN 30        WHEN last_user_status_df.last_user_status LIKE '%60%' THEN 60        ELSE 0      END   ) AS days_since_last_contact FROM    `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl   INNER JOIN `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` AS tagsa     ON tawl.id = tagsa.traffic_analytics_whatsapp_lead_id   LEFT JOIN (     SELECT        traffic_analytics_whatsapp_leads_id,       LAST_VALUE(user_status) OVER (PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date) AS last_user_status,       LAST_VALUE(contact_date) OVER (PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date) AS last_contact_date,       ROW_NUMBER() OVER (PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date DESC) AS row_number_contact     FROM `company-data-driven.{project_name}.contract_crm_log`   ) AS last_user_status_df      ON tawl.id = last_user_status_df.traffic_analytics_whatsapp_leads_id AND last_user_status_df.row_number_contact = 1 WHERE    tawl.id NOT IN (SELECT traffic_analytics_whatsapp_leads_id FROM `company-data-driven.{project_name}.contracts`)   AND (last_user_status_df.last_user_status LIKE '%active%' OR last_user_status_df.last_user_status IS NULL)   AND (COALESCE(DATE_DIFF(CURRENT_DATE(), last_user_status_df.last_contact_date, DAY), 99999)      - CASE        WHEN last_user_status_df.last_user_status LIKE '%15%' THEN 15        WHEN last_user_status_df.last_user_status LIKE '%30%' THEN 30        WHEN last_user_status_df.last_user_status LIKE '%60%' THEN 60        ELSE 0      END   ) > 3   AND tagsa.status = 'assistant' ORDER BY days_since_last_contact DESC;")
    st.table(contracts_crm_oportunities)














def contract_team_member_performance(user_id, project_name):
    os.write(1, '🥏 Executing contract_team_member_performance \n'.encode('utf-8'))
    os.write(1, '- contract_team_member_performance: Getting data \n'.encode('utf-8'))
    team_member_contacts = uc.run_query_half_day(f"SELECT tagsc.contact_date, EXTRACT(YEAR FROM tagsc.contact_date) AS year_contact, EXTRACT(MONTH FROM tagsc.contact_date) AS month_contact, EXTRACT(WEEK FROM tagsc.contact_date) AS week_contact, tagsc.user_status FROM `company-data-driven.{project_name}.contract_crm_log` AS tagsc WHERE tagsc.creator_id = {user_id} AND EXTRACT(YEAR FROM tagsc.contact_date) = EXTRACT(YEAR FROM CURRENT_DATE());")
    team_member_contacts_df = pd.DataFrame(team_member_contacts, columns = ["contact_date","year_contact","month_contact","week_contact","user_status"])
    today = datetime.date.today()
    
    st.header("Week evolution")
    corrected_week = (today.isocalendar()[1] + 1 if today.isocalendar()[2] == 7 else today.isocalendar()[1]) - 1
    col1, col2, col3, col4 = st.columns(4)
    team_member_contacts_week = team_member_contacts_df[(team_member_contacts_df["year_contact"] == today.year) & (team_member_contacts_df["month_contact"] == today.month) & (team_member_contacts_df["week_contact"] == corrected_week)]
    if len(team_member_contacts_week) < 1 or team_member_contacts_week is None:
            st.warning(f"You have not added new contacts", icon = "🫥")
    else:
        col1.metric(label="# Week Contacts", value = team_member_contacts_week.shape[0])
        col2.metric(label="# Week Active contacts", value = team_member_contacts_week[team_member_contacts_week['user_status'].str.contains('active')].shape[0])
        col3.metric(label="# Week Discarted contacts", value = team_member_contacts_week[team_member_contacts_week['user_status'] == 'discarted'].shape[0])
        col4.metric(label="# Week Lost contacts", value = team_member_contacts_week[team_member_contacts_week['user_status'] == 'lost'].shape[0])

    st.header("Month evolution")
    col1, col2, col3, col4 = st.columns(4)
    team_member_contacts_month = team_member_contacts_df[(team_member_contacts_df["year_contact"] == today.year) & (team_member_contacts_df["month_contact"] == today.month)]
    if len(team_member_contacts_month) < 1 or team_member_contacts_month is None:
            st.warning(f"You have not added new contacts", icon = "🫥")
    else:
        col1.metric(label="# Month Contacts", value = team_member_contacts_month.shape[0])
        col2.metric(label="# Month Active contacts", value = team_member_contacts_month[team_member_contacts_month['user_status'].str.contains('active')].shape[0])
        col3.metric(label="# Month Discarted contacts", value = team_member_contacts_month[team_member_contacts_month['user_status'] == 'discarted'].shape[0])
        col4.metric(label="# Month Lost contacts", value = team_member_contacts_month[team_member_contacts_month['user_status'] == 'lost'].shape[0])

    st.header("Year evolution")
    col1, col2, col3, col4 = st.columns(4)
    team_member_contacts_year = team_member_contacts_df[(team_member_contacts_df["year_contact"] == today.year)]
    if len(team_member_contacts_year) < 1 or team_member_contacts_year is None:
            st.warning(f"You have not added new contacts", icon = "🫥")
    else:
        col1.metric(label="# Year Contacts", value = team_member_contacts_year.shape[0])
        col2.metric(label="# Year Active contacts", value = team_member_contacts_year[team_member_contacts_year['user_status'].str.contains('active')].shape[0])
        col3.metric(label="# Year Discarted contacts", value = team_member_contacts_year[team_member_contacts_year['user_status'] == 'discarted'].shape[0])
        col4.metric(label="# Year Lost contacts", value = team_member_contacts_year[team_member_contacts_year['user_status'] == 'lost'].shape[0])









def contract_contact_text(project_id):
    if project_id == 1:
        text_answer = '''
        
        ¡Hola! Buenos días.

        Quería preguntarte cómo te ha ido con el proceso de homologación. Si tienes alguna duda o algo en lo que te podamos ayudar.

        Entiendo, si quieres podemos hacer una llamada para revisar tu caso particular.

        Vale, te va a llamar XX de nuestro equipo.

        También te dejo el enlace de suscripción: https://enfermeraenestadosunidos.com/validar-enfermeria-en-usa/
        '''
    st.markdown(text_answer)
        
