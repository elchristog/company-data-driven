import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re
import os


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_bgs(df_grouped):
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
                "name": "num_groupal_session_clicks",
                "data": df_grouped["num_groupal_session_clicks"].tolist(),
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




def bitly_groupal_session_show_metrics(project_name, bitly_groupal_session_link):
  os.write(1, '🥏 Executing bitly_groupal_session_show_metrics \n'.encode('utf-8'))

  if 'dates_bitly' not in st.session_state:
      dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
      st.session_state.dates_bitly = dates_bitly
  else:
      dates_bitly = st.session_state.dates_bitly

  if 'dates_whatsapp_leads' not in st.session_state:
      dates_whatsapp_leads = uc.run_query_1_h(f"SELECT MIN(creation_date) AS min_date_wsp, MAX(creation_date) AS max_date_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
      st.session_state.dates_whatsapp_leads = dates_whatsapp_leads
  else:
      dates_whatsapp_leads = st.session_state.dates_whatsapp_leads
    
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

      os.write(1, '- bitly_groupal_session_show_metrics: Getting data \n'.encode('utf-8'))
      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT groupal_session.date, groupal_session.num_groupal_session_clicks, whatsapp_leads.num_leads_wsp, ROUND(groupal_session.num_groupal_session_clicks/NULLIF(whatsapp_leads.num_leads_wsp, 0), 2) AS conversion FROM (SELECT date, SUM(clicks) AS num_groupal_session_clicks FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` WHERE bitly_link = '{bitly_groupal_session_link}' GROUP BY date) AS groupal_session INNER JOIN (SELECT creation_date, COUNT(id) AS num_leads_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE creation_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  creation_date <= '{day[1].strftime('%Y-%m-%d')}' GROUP BY creation_date) AS whatsapp_leads ON groupal_session.date = whatsapp_leads.creation_date ORDER BY groupal_session.date ASC;"))
    
      num_leads_wsp = df_conversion['num_leads_wsp'].sum()
      num_groupal_session_clicks = df_conversion['num_groupal_session_clicks'].sum()
      conversion = num_groupal_session_clicks/num_leads_wsp
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('num_leads_wsp:', f'{num_leads_wsp:,}')
      with met2:
          st.metric('num_groupal_session_clicks:', f'{num_groupal_session_clicks:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_bgs(df_conversion)
