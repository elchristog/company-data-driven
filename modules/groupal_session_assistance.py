import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_gsa(df_grouped):
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




def groupal_session_show_metrics(project_name, bitly_web_link, bitly_yt_link):
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
      # with st.container():
      #     plot_echarts_gsa(df_conversion)





def add_new_assistant_execution():
    pass




def add_new_assistant(project_name):
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
            add_assistant_button = st.button("Add assistant", on_click = add_new_assistant_execution)

