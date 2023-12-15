import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_wsp(df_grouped):
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
                "bitly_clicks_total": False,    
                "num_leads_wsp": False,
                "bitly_clicks_web": False,
                "bitly_clicks_yt": False 
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
                "name": "bitly_clicks_total",
                "data": df_grouped["bitly_clicks_total"].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "num_leads_wsp",
                "data": df_grouped['num_leads_wsp'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BF3F34"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "bitly_clicks_web",
                "data": df_grouped['bitly_clicks_web'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BFB5B4"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "bitly_clicks_yt",
                "data": df_grouped['bitly_clicks_yt'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#84C2BD"},
                "showSymbol": False,
            }
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  
        ],
        "backgroundColor": "#ffffff",
        "color": ["#A6785D", "#394A59", "#BF3F34", "#BFB5B4", "#84C2BD"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')




def whatsapp_leads_show_metrics(project_name, bitly_web_link, bitly_yt_link):
  dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
  dates_whatsapp_leads = uc.run_query_1_h(f"SELECT MIN(creation_date) AS min_date_wsp, MAX(creation_date) AS max_date_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
  if len(dates_bitly) < 1 or len(dates_whatsapp_leads) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (np.maximum(dates_bitly[0].get('min_date_bitly'), dates_whatsapp_leads[0].get('min_date_wsp')), np.minimum(dates_bitly[0].get('max_date_bitly'), dates_whatsapp_leads[0].get('max_date_wsp'))),
          min_value=np.maximum(dates_bitly[0].get('min_date_bitly'), dates_whatsapp_leads[0].get('min_date_wsp')),
          max_value=np.minimum(dates_bitly[0].get('max_date_bitly'), dates_whatsapp_leads[0].get('max_date_wsp')),
          format="DD/MM/YYYY",
          help='',
          key = 'day_web'
      )

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT btl_totals.date, btl_totals.bitly_clicks_web, btl_totals.bitly_clicks_yt, btl_totals.bitly_clicks_total, wsp_leads.num_leads_wsp, ROUND(wsp_leads.num_leads_wsp/NULLIF(btl_totals.bitly_clicks_total, 0), 2) AS conversion  FROM (SELECT date, SUM(CASE WHEN bitly_link IN ('{bitly_web_link}') THEN clicks ELSE 0 END) AS bitly_clicks_web, SUM(CASE WHEN bitly_link IN ('{bitly_yt_link}') THEN clicks ELSE 0 END) AS bitly_clicks_yt, SUM(CASE WHEN bitly_link IN ('{bitly_web_link}', '{bitly_yt_link}') THEN clicks ELSE 0 END) AS bitly_clicks_total FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` GROUP BY date) AS btl_totals INNER JOIN (SELECT creation_date, COUNT(id) AS num_leads_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE creation_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  creation_date <= '{day[1].strftime('%Y-%m-%d')}'  GROUP BY creation_date) AS wsp_leads ON wsp_leads.creation_date = btl_totals.date ORDER BY btl_totals.date ASC;"))
    
      bitly_clicks_total = df_conversion['bitly_clicks_total'].sum()
      num_leads_wsp = df_conversion['num_leads_wsp'].sum()
      conversion = num_leads_wsp/bitly_clicks_total
      bitly_clicks_web = df_conversion['bitly_clicks_web'].sum()
      bitly_clicks_yt = df_conversion['bitly_clicks_yt'].sum()
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('bitly_clicks_total:', f'{bitly_clicks_total:,}')
      with met2:
          st.metric('num_leads_wsp:', f'{num_leads_wsp:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_wsp(df_conversion)
      with met1:
          st.metric('bitly_clicks_web:', f'{bitly_clicks_web:,}')
      with met2:
          st.metric('bitly_clicks_yt:', f'{bitly_clicks_yt:,}')






def whatsapp_leads_creation_save(project_name, user_id):
    st.session_state.text_input_1 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_1)
    st.session_state.text_input_2 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_2)

    st.session_state.text_input_1 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_1)
    st.session_state.text_input_2 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_2)

    st.toast("Please wait", icon = "☺️")
    # uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.effective_communication_content` (id, creation_date, creator_user_id, keyword, main_idea, why_1, why_2, why_3, how_1, how_2, how_3, experiment_1, experiment_2, experiment_3, relevant_content, checklist, call_to_action, created_content) VALUES (GENERATE_UUID(), CURRENT_DATE(), {user_id}, '{st.session_state.text_input_1}', '{st.session_state.text_input_2}', '{st.session_state.text_input_3}', '{st.session_state.text_input_4}', '{st.session_state.text_input_5}', '{st.session_state.text_input_6}', '{st.session_state.text_input_7}', '{st.session_state.text_input_8}', '{st.session_state.text_input_9}', '{st.session_state.text_input_10}', '{st.session_state.text_input_11}', '{st.session_state.text_input_12}', '{st.session_state.text_input_13}', '{st.session_state.text_input_14}' ,0);")
    time.sleep(5)
    st.toast("Content saved!", icon = "👾")
    st.balloons()


def whatsapp_leads_creation(user_id, project_name):
    st.warning("Do not use line breaks, double or single quotes, double or single quotes neither", icon = "🙈")
    with st.form("whatsapp_leads_creation_form", clear_on_submit = True):
        text_input_1 = st.text_input(
            "Phone indicator",
            label_visibility = 'visible',
            disabled = False,
            placeholder = '1',
            help = 'Just the number of the country, no symbols',
            key = 'text_input_1'
        )

        text_input_2 = st.text_input(
            "Phone number",
            label_visibility = 'visible',
            disabled = False,
            placeholder = '8136783561',
            help = 'Just the phone number, no symbols or spaces',
            key = 'text_input_2'
        )

        submitted = st.form_submit_button("Submit", on_click = whatsapp_leads_creation_save, args = [project_name, user_id])


