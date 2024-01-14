import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_gsa(df_grouped):
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




def groupal_session_show_metrics(project_name, bitly_groupal_session_link):
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

      st.write(df_conversion)
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
          plot_echarts_gsa(df_conversion)





def add_new_assistant_execution(user_id, project_name, selected_phone_id, meeting_date):
    st.toast("Please wait", icon = "☺️")
    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` (id, traffic_analytics_whatsapp_lead_id, meeting_date, creator_user_id) VALUES (GENERATE_UUID(), '{selected_phone_id}', '{meeting_date}', {user_id});")
    time.sleep(5)
    st.toast("Assistant saved!", icon = "👾")
    st.balloons()




def add_new_assistant(user_id, project_name):
    rows = uc.run_query_half_day(f"SELECT id, CONCAT(phone_indicator,phone_number) AS full_phone_number FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
    assistant_ids = []
    assistant_phone_numbers = []
    for row in rows:
        assistant_ids.append(row.get('id'))
        assistant_phone_numbers.append(row.get('full_phone_number'))
    selected_phone = st.selectbox(
            label = "Select the assistant phone number",
            options = assistant_phone_numbers,
            index = None,
            key= "assistant_phone_numbers"
        )
    checking_phone_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE CONCAT(phone_indicator,phone_number) LIKE '{selected_phone}' ")
    if len(checking_phone_query) < 1 or checking_phone_query is None:
        st.error('Phone number does not exists, should be created adding a new lead into Whatsapp', icon = '👻')
    else:
        st.success('Phone number available', icon = '🪬')
        if selected_phone is not None:
            selected_phone_id = assistant_ids[assistant_phone_numbers.index(selected_phone)]
            meeting_date = st.date_input("Meeting date:", key = 'meeting_date')
            add_assistant_button = st.button("Add assistant", on_click = add_new_assistant_execution, args = [user_id, project_name, selected_phone_id, meeting_date])

