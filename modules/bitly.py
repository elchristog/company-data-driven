import streamlit as st
import time
import datetime
import requests
import json
import pandas as pd
import numpy as np

from datetime import datetime
from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc

def get_clicks_for_bitlink(token, bitlink, unit, units):
  url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks"
  headers = {"Authorization": f"Bearer {token}"}
  params = {"unit": unit, "units": units}
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  return response.json()

def save_bitly_metrics_one_link(project_name, bitly_link, link_name, max_stored_date, current_date):
  access_token = st.secrets["BITLY_TOKEN"]
  bitlink = bitly_link
  unit = "day"
  units = -1
  clicks_story = get_clicks_for_bitlink(access_token, bitlink, unit, units)
  dates = []
  clicks = []

  df_clicks = pd.DataFrame([
            {
                'date': datetime.strptime(row.get('date') , "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d"),
                'clicks': row.get('clicks')
            } for row in clicks_story.get('link_clicks', [])
        ])

  if max_stored_date is None:
    filtered_clicks =  df_clicks[df_clicks['date'] < current_date.strftime("%Y-%m-%d")]
  else:
    filtered_clicks =  df_clicks[df_clicks['date'] > max_stored_date.strftime("%Y-%m-%d")]
    filtered_clicks =  filtered_clicks[filtered_clicks['date'] < current_date.strftime("%Y-%m-%d")]

  for index, row in filtered_clicks.iterrows():
    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` (date, bitly_link, link_name, clicks) VALUES ('{row['date']}', '{bitly_link}', '{link_name}', {row['clicks']});")





def save_bitly_metrics_bulk(project_name):
  dates_in_table = uc.run_query_half_day(f"SELECT CURRENT_DATE() AS current_date, DATE_DIFF(CURRENT_DATE(), MAX(date), DAY) AS days_last_update, MAX(date) AS max_date FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
  current_date = dates_in_table[0].get('current_date')
  days_last_update = dates_in_table[0].get('days_last_update')
  max_date = dates_in_table[0].get('max_date')
  if days_last_update is None or days_last_update is None:
    st.toast("Updating bitly data", icon = "🥶")
    save_bitly_metrics_one_link(project_name, 'bit.ly/45SidF6', 'enfermera_en_estados_unidos_youtube_to_whatsapp', None, current_date)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6SrJa', 'enfermera_en_estados_unidos_instagram_to_whatsapp', None, current_date)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6RbFW', 'enfermera_en_estados_unidos_web_to_whatsapp', None, current_date)
    uc.run_query_half_day.clear()
  elif days_last_update > 1: # 1 day because today still getting data
    st.toast("Updating bitly data", icon = "🥶")
    save_bitly_metrics_one_link(project_name, 'bit.ly/45SidF6', 'enfermera_en_estados_unidos_youtube_to_whatsapp', max_date, current_date)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6SrJa', 'enfermera_en_estados_unidos_instagram_to_whatsapp', max_date, current_date)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6RbFW', 'enfermera_en_estados_unidos_web_to_whatsapp', max_date, current_date)
    uc.run_query_half_day.clear()
  else:
    pass






def plot_echarts_btl_web_yt(df_grouped, channel_name):
    if channel_name == 'web':
      interaction_variable_name = 'web_clicks'
    elif channel_name == 'yt':
      interaction_variable_name = 'yt_views'
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
                interaction_variable_name: False,    
                "bitly_clicks": False         
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
                "name": interaction_variable_name,
                "data": df_grouped[interaction_variable_name].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "bitly_clicks",
                "data": df_grouped['bitly_clicks'].tolist(),
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







def show_bitly_web_youtube_metrics(project_name, bitly_web_link, bitly_yt_link):
    st.write("### 	:earth_americas: Bitly web conversion")
    dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
    dates_web = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_web, MAX(date) AS max_date_web FROM `company-data-driven.{project_name}.traffic_analytics_web_clicks`;")
    if len(dates_bitly) < 1 or len(dates_web) < 1:
        st.warning("Waiting for data")
    else:
        day = st.date_input(
            "Time Range:",
            (np.maximum(dates_bitly[0].get('min_date_bitly'), dates_web[0].get('min_date_web')), np.minimum(dates_bitly[0].get('max_date_bitly'), dates_web[0].get('max_date_web'))),
            min_value=np.maximum(dates_bitly[0].get('min_date_bitly'), dates_web[0].get('min_date_web')),
            max_value=np.minimum(dates_bitly[0].get('max_date_bitly'), dates_web[0].get('max_date_web')),
            format="DD/MM/YYYY",
            help=''
        )
        df_bitly_web = pd.DataFrame(uc.run_query_1_h(f"SELECT tabc.date, tawc.clicks AS web_clicks, tabc.clicks AS bitly_clicks, ROUND(tabc.clicks/tawc.clicks, 2) AS conversion FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` AS tabc INNER JOIN `company-data-driven.{project_name}.traffic_analytics_web_clicks` AS tawc ON tabc.date = tawc.date WHERE tabc.bitly_link = '{bitly_web_link}'   AND tabc.date >= '{day[0].strftime('%Y-%m-%d')}' AND tabc.date <= '{day[1].strftime('%Y-%m-%d')}'  ORDER BY tabc.date ASC;"))
    
        web_clicks = df_bitly_web['web_clicks'].sum()
        bitly_clicks = df_bitly_web['bitly_clicks'].sum()
        conversion = bitly_clicks/web_clicks
        met1, met2, met3 = st.columns(3)
        with met1:
            st.metric('web_clicks:', f'{web_clicks:,}')
        with met2:
            st.metric('bitly_clicks:', f'{bitly_clicks:,}')
        with met3:
            st.metric('conversion:', f'{conversion * 100:.2f}%')
        with st.container():
            plot_echarts_btl_web_yt(df_bitly_web, 'web')


    st.write("### 	:movie_camera: Bitly youtube conversion")
    dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
    dates_yt = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_yt, MAX(date) AS max_date_yt FROM `company-data-driven.{project_name}.traffic_analytics_youtube_views`;")
    if len(dates_bitly) < 1 or len(dates_yt) < 1:
        st.warning("Waiting for data")
    else:
        day_yt = st.date_input(
            "Time Range:",
            (np.maximum(dates_bitly[0].get('min_date_bitly'), dates_yt[0].get('min_date_yt')), np.minimum(dates_bitly[0].get('max_date_bitly'), dates_yt[0].get('max_date_yt'))),
            min_value=np.maximum(dates_bitly[0].get('min_date_bitly'), dates_yt[0].get('min_date_yt')),
            max_value=np.minimum(dates_bitly[0].get('max_date_bitly'), dates_yt[0].get('max_date_yt')),
            format="DD/MM/YYYY",
            help='',
            key = 'day_yt'
        )
        df_bitly_yt = pd.DataFrame(uc.run_query_1_h(f"SELECT tabc.date, tayv.views AS yt_views, tabc.clicks AS bitly_clicks, ROUND(tabc.clicks/ tayv.views, 2) AS conversion FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` AS tabc INNER JOIN `company-data-driven.{project_name}.traffic_analytics_youtube_views` AS tayv ON tabc.date = tayv.date WHERE tabc.bitly_link = '{bitly_yt_link}'   AND tabc.date >= '{day[0].strftime('%Y-%m-%d')}' AND tabc.date <= '{day[1].strftime('%Y-%m-%d')}'  ORDER BY tabc.date ASC;"))
    
        yt_views = df_bitly_web['yt_views'].sum()
        bitly_clicks = df_bitly_web['bitly_clicks'].sum()
        conversion = bitly_clicks/yt_views
        met1, met2, met3 = st.columns(3)
        with met1:
            st.metric('yt_views:', f'{yt_views:,}')
        with met2:
            st.metric('bitly_clicks:', f'{bitly_clicks:,}')
        with met3:
            st.metric('conversion:', f'{conversion * 100:.2f}%')
        with st.container():
            plot_echarts_btl_web_yt(df_bitly_yt, 'yt')
    
