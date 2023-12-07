import streamlit as st
import time
import datetime
import requests
import json
import pandas as pd

from datetime import datetime

import utils.user_credentials as uc

def get_clicks_for_bitlink(token, bitlink, unit, units):
  url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks"
  headers = {"Authorization": f"Bearer {token}"}
  params = {"unit": unit, "units": units}
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  return response.json()

def save_bitly_metrics_one_link(project_name, bitly_link, link_name, max_stored_date):
  access_token = st.secrets["BITLY_TOKEN"]
  bitlink = bitly_link
  unit = "day"
  units = -1
  clicks_story = get_clicks_for_bitlink(access_token, bitlink, unit, units)
  dates = []
  clicks = []
  st.success("My lord!")

  df_clicks = pd.DataFrame([
            {
                'date': datetime.strptime(row.get('date') , "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d"),
                'clicks': row.get('clicks')
            } for row in clicks_story.get('link_clicks', [])
        ])

  if max_stored_date is None:
    filtered_clicks =  df_clicks
  else:
    filtered_clicks =  df_clicks[df_clicks['date'] > max_stored_date]

  for index, row in filtered_clicks.iterrows():
    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` (date, bitly_link, link_name, clicks) VALUES ('{row['date']}', '{bitly_link}', '{link_name}', {row['clicks']});")



def save_bitly_metrics_bulk(project_name):
  dates_in_table = uc.run_query_half_day(f"SELECT DATE_DIFF(CURRENT_DATE(), MAX(date), DAY) AS days_last_update, MAX(date) AS max_date FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
  days_last_update = dates_in_table[0].get('days_last_update')
  max_date = dates_in_table[0].get('max_date')
  if days_last_update is None or days_last_update is None:
    st.toast("Updating bitly data", icon = "🥶")
    save_bitly_metrics_one_link(project_name, 'bit.ly/45SidF6', 'enfermera_en_estados_unidos_youtube_to_whatsapp', None)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6SrJa', 'enfermera_en_estados_unidos_instagram_to_whatsapp', None)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6RbFW', 'enfermera_en_estados_unidos_web_to_whatsapp', None)
    uc.run_query_half_day.clear()
  elif days_last_update > 0:
    st.toast("Updating bitly data", icon = "🥶")
    save_bitly_metrics_one_link(project_name, 'bit.ly/45SidF6', 'enfermera_en_estados_unidos_youtube_to_whatsapp', max_date)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6SrJa', 'enfermera_en_estados_unidos_instagram_to_whatsapp', max_date)
    save_bitly_metrics_one_link(project_name, 'bit.ly/3R6RbFW', 'enfermera_en_estados_unidos_web_to_whatsapp', max_date)
    uc.run_query_half_day.clear()
  else:
    pass

  
    
  
