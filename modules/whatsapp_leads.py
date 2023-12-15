import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd

import utils.user_credentials as uc

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
      # with st.container():
      #     plot_echarts_btl_web_yt(df_bitly_web, 'web')
      with met1:
          st.metric('bitly_clicks_web:', f'{bitly_clicks_web:,}')
      with met2:
          st.metric('bitly_clicks_yt:', f'{bitly_clicks_yt:,}')
