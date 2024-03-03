import streamlit as st
import time
import datetime
import requests
import json
import pandas as pd
import numpy as np
import os

from datetime import datetime
from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




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








def plot_echarts_btl_networks(df_grouped):
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
                "network_bitly_clicks": True      
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "network_bitly_clicks",
                "data": df_grouped['network_bitly_clicks'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,
            }
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  
        ],
        "backgroundColor": "#ffffff",
        "color": ["#A6785D"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')







def show_bitly_web_youtube_metrics(project_name, bitly_web_link, bitly_yt_link, bitly_inst_link):
    os.write(1, '🥏 Executing show_bitly_web_youtube_metrics \n'.encode('utf-8'))
    os.write(1, '- show_bitly_web_youtube_metrics: Web data \n'.encode('utf-8'))
    st.write("### 	:earth_americas: Bitly web conversion")

    if 'show_bitly_web_youtube_metrics_dates_bitly' not in st.session_state or 'show_bitly_web_youtube_metrics_dates_web' not in st.session_state:
        dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
        dates_web = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_web, MAX(date) AS max_date_web FROM `company-data-driven.{project_name}.traffic_analytics_web_clicks`;")
        st.session_state.show_bitly_web_youtube_metrics_dates_bitly = dates_bitly
        st.session_state.show_bitly_web_youtube_metrics_dates_web = dates_web
    else:
        dates_bitly = st.session_state.show_bitly_web_youtube_metrics_dates_bitly
        dates_web = st.session_state.show_bitly_web_youtube_metrics_dates_web
    
    if len(dates_bitly) < 1 or len(dates_web) < 1:
        st.warning("Waiting for data")
    else:
        day = st.date_input(
            "Time Range:",
            (np.maximum(dates_bitly[0].get('min_date_bitly'), dates_web[0].get('min_date_web')), np.minimum(dates_bitly[0].get('max_date_bitly'), dates_web[0].get('max_date_web'))),
            min_value=np.maximum(dates_bitly[0].get('min_date_bitly'), dates_web[0].get('min_date_web')),
            max_value=np.minimum(dates_bitly[0].get('max_date_bitly'), dates_web[0].get('max_date_web')),
            format="DD/MM/YYYY",
            help='',
            key = 'day_web'
        )

        if 'df_bitly_web' not in st.session_state:
            df_bitly_web = pd.DataFrame(uc.run_query_1_h(f"SELECT tabc.date, tawc.clicks AS web_clicks, tabc.clicks AS bitly_clicks, ROUND(tabc.clicks/NULLIF(tawc.clicks, 0), 2) AS conversion FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` AS tabc INNER JOIN `company-data-driven.{project_name}.traffic_analytics_web_clicks` AS tawc ON tabc.date = tawc.date WHERE tabc.bitly_link = '{bitly_web_link}'   AND tabc.date >= '{day[0].strftime('%Y-%m-%d')}' AND tabc.date <= '{day[1].strftime('%Y-%m-%d')}'  ORDER BY tabc.date ASC;"))
            st.session_state.df_bitly_web = df_bitly_web
        else:
            df_bitly_web = st.session_state.df_bitly_web
    
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

    
    os.write(1, '- show_bitly_web_youtube_metrics: Youtube data \n'.encode('utf-8'))
    st.write("### 	:movie_camera: Bitly youtube conversion")
    
    if 'dates_yt' not in st.session_state:
        dates_yt = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_yt, MAX(date) AS max_date_yt FROM `company-data-driven.{project_name}.traffic_analytics_youtube_views`;")
        st.session_state.dates_yt = dates_yt
    else: 
        dates_yt = st.session_state.dates_yt
    
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
        df_bitly_yt = pd.DataFrame(uc.run_query_1_h(f"SELECT tabc.date, tayv.views AS yt_views, tabc.clicks AS bitly_clicks, ROUND(tabc.clicks/ NULLIF(tayv.views, 0), 2) AS conversion FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` AS tabc INNER JOIN `company-data-driven.{project_name}.traffic_analytics_youtube_views` AS tayv ON tabc.date = tayv.date WHERE tabc.bitly_link = '{bitly_yt_link}'   AND tabc.date >= '{day_yt[0].strftime('%Y-%m-%d')}' AND tabc.date <= '{day_yt[1].strftime('%Y-%m-%d')}'  ORDER BY tabc.date ASC;"))
    
        yt_views = df_bitly_yt['yt_views'].sum()
        yt_bitly_clicks = df_bitly_yt['bitly_clicks'].sum()
        yt_conversion = yt_bitly_clicks/yt_views
        met1, met2, met3 = st.columns(3)
        with met1:
            st.metric('yt_views:', f'{yt_views:,}')
        with met2:
            st.metric('bitly_clicks:', f'{yt_bitly_clicks:,}')
        with met3:
            st.metric('conversion:', f'{yt_conversion * 100:.2f}%')
        with st.container():
            plot_echarts_btl_web_yt(df_bitly_yt, 'yt')



    os.write(1, '- show_bitly_web_youtube_metrics: Instagram data \n'.encode('utf-8'))
    st.write("### 	:frame_with_picture: Bitly instagram clicks")
    if len(dates_bitly) < 1:
        st.warning("Waiting for data")
    else:
        day_inst = st.date_input(
            "Time Range:",
            (dates_bitly[0].get('min_date_bitly'), dates_bitly[0].get('max_date_bitly')),
            min_value=dates_bitly[0].get('min_date_bitly'),
            max_value=dates_bitly[0].get('max_date_bitly'),
            format="DD/MM/YYYY",
            help='',
            key = 'day_inst'
        )

        df_bitly_inst = pd.DataFrame(uc.run_query_1_h(f"SELECT tabc.date, tabc.clicks AS network_bitly_clicks FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` AS tabc WHERE tabc.bitly_link = '{bitly_inst_link}' AND tabc.date >= '{day_inst[0].strftime('%Y-%m-%d')}' AND tabc.date <= '{day_inst[1].strftime('%Y-%m-%d')}' ORDER BY tabc.date ASC;"))
    
        inst_bitly_clicks = df_bitly_inst['network_bitly_clicks'].sum()
        st.metric('inst_bitly_clicks:', f'{inst_bitly_clicks:,}')
        with st.container():
            plot_echarts_btl_networks(df_bitly_inst)
