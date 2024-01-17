
import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re


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

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT COALESCE(groupal_session_assistants.date, contracts_counts.date) AS date, COALESCE(num_assistants_groupal_session,0) AS num_assistants_groupal_session, COALESCE(num_contracts,0) AS num_contracts FROM (SELECT meeting_date AS date, COUNT(id) AS num_assistants_groupal_session FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` WHERE meeting_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  meeting_date <= '{day[1].strftime('%Y-%m-%d')}' GROUP BY meeting_date) AS groupal_session_assistants FULL OUTER JOIN (SELECT contract_date AS date, COUNT(id) AS num_contracts FROM `company-data-driven.{project_name}.contracts` WHERE contract_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  contract_date <= '{day[1].strftime('%Y-%m-%d')}' GROUP BY contract_date) contracts_counts ON groupal_session_assistants.date = contracts_counts.date  ORDER BY COALESCE(groupal_session_assistants.date, contracts_counts.date) ASC;"))

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
        time.sleep(5)
        uc.run_query_30_m.clear()
        st.toast('User Created!', icon = '🎈')
        st.balloons()
        st.warning('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        st.toast('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        




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






















def plot_echarts_contract_payments(df_grouped):
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
                "groupal_session_clicks": True,        
                "num_assistants": False
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "groupal_session_clicks",
                "data": df_grouped['groupal_session_clicks'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "num_assistants",
                "data": df_grouped["num_assistants"].tolist(),
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




def contract_payments_show_metrics(project_name):
  dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
  if len(dates_bitly) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (dates_bitly[0].get('min_date_bitly'), dates_bitly[0].get('max_date_bitly')),
          min_value=dates_bitly[0].get('min_date_bitly'),
          max_value=dates_bitly[0].get('max_date_bitly'),
          format="DD/MM/YYYY",
          help='',
          key = 'day_gsa'
      )

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT groupal_session_clicks_df.date, groupal_session_clicks_df.groupal_session_clicks, meeting_assistance.num_assistants FROM (SELECT meeting_date, COUNT(id) AS num_assistants FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` GROUP BY meeting_date) AS meeting_assistance RIGHT OUTER JOIN (SELECT date, SUM(clicks) AS groupal_session_clicks FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` WHERE bitly_link = '{bitly_groupal_session_link}' AND date >= '{day[0].strftime('%Y-%m-%d')}'  AND  date <= '{day[1].strftime('%Y-%m-%d')}'   GROUP BY date) AS groupal_session_clicks_df ON meeting_assistance.meeting_date = groupal_session_clicks_df.date ORDER BY groupal_session_clicks_df.date ASC;"))

      df_conversion["num_assistants"] = df_conversion["num_assistants"].fillna(0)
      bitly_clicks_groupal_session = df_conversion['groupal_session_clicks'].sum()
      num_assistants = df_conversion['num_assistants'].sum()
      conversion = num_assistants/bitly_clicks_groupal_session
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('bitly_clicks_groupal_session:', f'{bitly_clicks_groupal_session:,}')
      with met2:
          st.metric('num_assistants:', f'{num_assistants:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_contract_payments(df_conversion)





def add_new_contract_payment_execution(user_id, project_name, selected_contract_id, payment_date, payment_value):
    if payment_value is None:
        st.toast("payment_value can not be null", icon = "🤨")
    else:
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.contracts_payments` (id, contract_id, payment_value, payment_date, creator_id) VALUES (GENERATE_UUID(), '{selected_contract_id}', '{payment_value}', '{payment_date}', {user_id});")
        time.sleep(5)
        st.toast("Payment saved!", icon = "👾")
        st.balloons()




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
            payment_date = st.date_input("Payment date:", key = 'payment_date')
            payment_value = st.text_input("Payment value (USD):", key = 'payment_value', placeholder = "325", help = "Do not use dots, just numbers")
            add_payment_button = st.button("Add payment", on_click = add_new_contract_payment_execution, args = [user_id, project_name, selected_contract_id, payment_date, payment_value])















def add_new_crm_contact_execution(user_id, project_name, selected_phone_id, contact_date, user_status, contact_description):
    st.toast("Please wait", icon = "☺️")
    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.contract_crm_log` (id, contact_date, traffic_analytics_whatsapp_leads_id, creator_id, user_status, contact_description) VALUES (GENERATE_UUID(), '{contact_date}', '{selected_phone_id}', {user_id}, '{user_status}', '{contact_description}');")
    time.sleep(5)
    st.toast("CRM Contact saved!", icon = "👾")
    st.balloons()




def add_new_crm_contact(user_id, project_name):
    rows = uc.run_query_half_day(f"SELECT tawl.id, CONCAT(tawl.phone_indicator,tawl.phone_number) AS full_phone_number, last_user_status_df.last_user_status FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl INNER JOIN `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` AS tagsa ON tawl.id = tagsa.traffic_analytics_whatsapp_lead_id LEFT OUTER JOIN (SELECT traffic_analytics_whatsapp_leads_id, LAST_VALUE(user_status) OVER(PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date) AS last_user_status FROM `company-data-driven.{project_name}.contract_crm_log`) AS last_user_status_df ON tawl.id = last_user_status_df.traffic_analytics_whatsapp_leads_id WHERE tawl.id NOT IN (SELECT traffic_analytics_whatsapp_leads_id FROM `company-data-driven.{project_name}.contracts`) AND (last_user_status_df.last_user_status = 'active' OR last_user_status_df.last_user_status IS NULL);")
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
            contact_date = st.date_input("Contact date:", key = 'contact_date')
            user_status = st.selectbox(
                label = "Select the user status",
                options = ['active', 'lost', 'discarted'],
                index = None,
                key= "user_status",
                placeholder = "active",
                help = "active = active oportunity, lost = the user reject the process, discarted = the user does not meet the requirements such as nurses from cuba or auxiliaries"
            )
            contact_description = st.text_input("Description of the contact", placeholder = "Se contacta entregando enlace de pago y contrato")
            add_contact_button = st.button("Add CRM contact", on_click = add_new_crm_contact_execution, args = [user_id, project_name, selected_phone_id, contact_date, user_status, contact_description])








def contracts_crm_show_metrics(project_name):
    contracts_crm_oportunities = uc.run_query_1_h(f"SELECT tawl.id, CONCAT(tawl.phone_indicator,tawl.phone_number) AS full_phone_number, COALESCE(DATE_DIFF(CURRENT_DATE(),last_user_status_df.last_contact_date, DAY), 99999) AS days_since_last_contact FROM `company-data-driven.enfermera_en_estados_unidos.traffic_analytics_whatsapp_leads` AS tawl INNER JOIN `company-data-driven.enfermera_en_estados_unidos.traffic_analytics_groupal_session_assistance` AS tagsa ON tawl.id = tagsa.traffic_analytics_whatsapp_lead_id LEFT OUTER JOIN (SELECT traffic_analytics_whatsapp_leads_id, LAST_VALUE(user_status) OVER(PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date) AS last_user_status, LAST_VALUE(contact_date) OVER(PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date) AS last_contact_date FROM `company-data-driven.enfermera_en_estados_unidos.contract_crm_log`) AS last_user_status_df ON tawl.id = last_user_status_df.traffic_analytics_whatsapp_leads_id WHERE tawl.id NOT IN (SELECT traffic_analytics_whatsapp_leads_id FROM `company-data-driven.enfermera_en_estados_unidos.contracts`) AND (last_user_status_df.last_user_status = 'active' OR last_user_status_df.last_user_status IS NULL) AND COALESCE(DATE_DIFF(CURRENT_DATE(),last_user_status_df.last_contact_date, DAY), 99999) > 3 ORDER BY COALESCE(DATE_DIFF(CURRENT_DATE(),last_user_status_df.last_contact_date, DAY), 99999) DESC;")
    st.table(contracts_crm_oportunities)
