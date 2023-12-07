import streamlit as st
import time
import datetime
import requests
import json

from datetime import datetime

import utils.user_credentials as uc

def get_clicks_for_bitlink(token, bitlink, unit, units):
  url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks"
  headers = {"Authorization": f"Bearer {token}"}
  params = {"unit": unit, "units": units}
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  return response.json()

def save_bitly_metrics_one_link(project_name, bitly_link, link_name):
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
            } for row in clicks_story
        ])
  
  st.write(df_clicks)
    
  
