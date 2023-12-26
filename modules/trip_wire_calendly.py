
import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_twc(df_grouped):
    df_grouped['conversion'] = df_grouped['conversion'].apply(lambda conversion: f"{conversion:.2f}")
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
                "conversion": True,        
                "number_leads_wsp": False,    
                "number_trip_wire_customers": False
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "conversion",
                "data": df_grouped['conversion'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "number_leads_wsp",
                "data": df_grouped["number_leads_wsp"].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "number_trip_wire_customers",
                "data": df_grouped['number_trip_wire_customers'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BF3F34"},
                "showSymbol": False,
            }
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  
        ],
        "backgroundColor": "#ffffff",
        "color": ["#A6785D", "#394A59", "#BF3F34"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')




def trip_wire_calendly_show_metrics(project_name):
  dates_whatsapp_leads = uc.run_query_1_h(f"SELECT MIN(creation_date) AS min_date_wsp, MAX(creation_date) AS max_date_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
  dates_cold_customers = uc.run_query_1_h(f"SELECT MIN(u.creation_date) AS min_date_users, MAX(u.creation_date) AS max_date_users FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id INNER JOIN `company-data-driven.global.projects` AS p ON u.project_id = p.id WHERE p.name = '{project_name}' AND ra.role_id = 6;")

  if len(dates_whatsapp_leads) < 1 or len(dates_cold_customers) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (np.maximum(dates_whatsapp_leads[0].get('min_date_wsp'), dates_cold_customers[0].get('min_date_users')), np.minimum(dates_whatsapp_leads[0].get('max_date_wsp'), dates_cold_customers[0].get('max_date_users'))),
          min_value=np.maximum(dates_whatsapp_leads[0].get('min_date_wsp'), dates_cold_customers[0].get('min_date_users')),
          max_value=np.minimum(dates_whatsapp_leads[0].get('max_date_wsp'), dates_cold_customers[0].get('max_date_users')),
          format="DD/MM/YYYY",
          help='',
          key = 'day_trip_wire'
      )

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT trip_wire_counts.creation_date AS date, number_wsp_leads.number_leads_wsp, trip_wire_counts.number_trip_wire_customers, ROUND(trip_wire_counts.number_trip_wire_customers / NULLIF(number_wsp_leads.number_leads_wsp, 0), 2) AS conversion FROM (SELECT u.creation_date, COUNT(u.id) AS number_trip_wire_customers FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id INNER JOIN `company-data-driven.global.projects` AS p ON u.project_id = p.id WHERE p.name = '{project_name}' AND ra.role_id = 6 GROUP BY u.creation_date) AS trip_wire_counts INNER JOIN (SELECT creation_date, COUNT(id) AS number_leads_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE creation_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  creation_date <= '{day[1].strftime('%Y-%m-%d')}' GROUP BY creation_date) AS number_wsp_leads ON trip_wire_counts.creation_date = number_wsp_leads.creation_date ORDER BY trip_wire_counts.creation_date ASC;"))

      number_leads_wsp = df_conversion['number_leads_wsp'].sum()
      number_trip_wire_customers = df_conversion['number_trip_wire_customers'].sum()
      conversion = number_trip_wire_customers/number_leads_wsp
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('number_leads_wsp:', f'{number_leads_wsp:,}')
      with met2:
          st.metric('number_trip_wire_customers:', f'{number_trip_wire_customers:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_twc(df_conversion)






# def customer_creation_execution():
#     checking_username_query = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{st.session_state.username_user_creation}';")
#     if len(checking_username_query) < 1:
#         checking_user_role = []
#     else:
#         checking_user_role = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.role_assignment` WHERE user_id = {checking_username_query[0].get('id')};")
#     if len(st.session_state.username_user_creation) < 6:
#         st.toast("The username must be at least 6 characters long.")
#     if len(st.session_state.checking_username_query_user_creation) > 0:
#         st.toast("The username is already in use.")
#     if len(checking_user_role) > 0:
#         st.toast("The username already has a role.")
#     if st.session_state.selected_project_user_creation is None:
#         st.toast("Please select a project.")
#     if st.session_state.selected_project_user_creation != st.session_state.selected_project_confirmation_user_creation:
#         st.toast("The selected project and the confirmation project must match.")
#     if st.session_state.user_role_user_creation is None:
#         st.toast("Please select a user role.")
#     if st.session_state.user_role_user_creation != st.session_state.user_role_confirmation_user_creation:
#         st.toast("The selected user role and the confirmation user role must match.")
#     if st.session_state.user_first_name_user_creation is None:
#         st.toast("Please enter your first name.")
#     if len(st.session_state.user_first_name_user_creation) < 3:
#         st.toast("The first name must be at least 3 characters long.")
#     if st.session_state.user_last_name_user_creation is None:
#         st.toast("Please enter your last name.")
#     if len(st.session_state.user_last_name_user_creation) < 3:
#         st.toast("The last name must be at least 3 characters long.")
#     if st.session_state.user_email_user_creation is None:
#         st.toast("Please enter your email address.")
#     if len(st.session_state.user_email_user_creation) < 3:
#         st.toast("The email address must be at least 3 characters long.")
#     if st.session_state.user_birth_date_user_creation is None:
#         st.toast("Please enter your birth date.")
#     if st.session_state.user_country_user_creation is None:
#         st.toast("Please select your country.")
#     if len(st.session_state.user_country_user_creation) < 3:
#         st.toast("The country name must be at least 3 characters long.")
#     if st.session_state.user_gender_user_creation is None:
#         st.toast("Please select your gender.")
#     if len(st.session_state.user_gender_user_creation) < 3:
#         st.toast("The gender must be at least 3 characters long.")
#     if st.session_state.user_phone_number_user_creation is None:
#         st.toast("Please enter your phone number.")
#     if len(st.session_state.user_phone_number_user_creation) < 6:
#         st.toast("The phone number must be at least 6 characters long.")
#     if st.session_state.user_drive_folder_user_creation is None:
#         st.toast("Please enter the Drive URL.")
#     if len(st.session_state.user_drive_folder_user_creation) < 6:
#         st.toast("The Drive URL must be at least 6 characters long.")
#     if len(st.session_state.username_user_creation) < 6 or len(st.session_state.checking_username_query_user_creation) > 0 or len(checking_user_role) > 0 or st.session_state.selected_project_user_creation is None or st.session_state.selected_project_user_creation != st.session_state.selected_project_confirmation_user_creation or st.session_state.user_role_user_creation is None or st.session_state.user_role_user_creation != st.session_state.user_role_confirmation_user_creation or st.session_state.user_first_name_user_creation is None or len(st.session_state.user_first_name_user_creation) < 3 or st.session_state.user_last_name_user_creation is None or len(st.session_state.user_last_name_user_creation) < 3 or st.session_state.user_email_user_creation is None or len(st.session_state.user_email_user_creation) < 3  or st.session_state.user_birth_date_user_creation is None or st.session_state.user_country_user_creation is None or len(st.session_state.user_country_user_creation) < 3 or st.session_state.user_gender_user_creation is None or len(st.session_state.user_gender_user_creation) < 3 or st.session_state.user_phone_number_user_creation is None or len(st.session_state.user_phone_number_user_creation) < 6 or st.session_state.user_drive_folder_user_creation is None or len(st.session_state.user_drive_folder_user_creation) < 6:
#         st.toast("Please fill in completely all of the required fields.")
#     else:
#         uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.users` (id, username, status, project_id, creation_date, email, name, lastname, birthdate, country, gender, user_creator_id, phone_number, user_drive_folder) VALUES({st.session_state.max_id_users_user_creation}, '{st.session_state.username_user_creation}', 'active', {st.session_state.selected_project_id_user_creation}, '{st.session_state.today_str_user_creation}', '{st.session_state.user_email_user_creation.lower()}', '{st.session_state.user_first_name_user_creation.lower()}', '{st.session_state.user_last_name_user_creation.lower()}', '{st.session_state.user_birth_date_user_creation}', '{st.session_state.user_country_user_creation.lower()}', '{st.session_state.user_gender_user_creation.lower()}', {st.session_state.user_id_user_creation}, '{st.session_state.user_phone_number_user_creation}', '{st.session_state.user_drive_folder_user_creation}');")
#         uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.role_assignment` (id, user_id, role_id) VALUES({st.session_state.max_id_role_assignement_user_creation}, {st.session_state.max_id_users_user_creation}, {st.session_state.selected_role_id_user_creation});")
#         st.toast("Updating, please wait", icon = "☺️")
#         time.sleep(5)
#         uc.run_query_30_m.clear()
#         st.toast('User Created!', icon = '🎈')
#         st.balloons()
#         st.warning('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
#         st.toast('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        




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
    user_phone_number = st.text_input("Write the user phone number:")
    user_birth_date = st.date_input("User birth date:", min_value = datetime.date(1970,1,1)) 
    user_country = st.selectbox(
        label = "Select user country",
        options = ['colombia', 'united states', 'el salvador', 'mexico', 'venezuela', 'costa rica', 'chile'],
        index = None
    )
    user_gender = st.selectbox(
        label = "Select user gender",
        options = ['male', 'female'],
        index = None
    )
    user_drive_folder = st.text_input("Write the user Google Drive folder url:")
    
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
    st.session_state.today_str_customer_creation = today_str
    st.session_state.max_id_users_customer_creation = max_id_users
    st.session_state.max_id_role_assignement_customer_creation = max_id_role_assignement
    
    create_user_button = st.button("Create User", on_click = customer_creation_execution)
