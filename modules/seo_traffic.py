import streamlit as st

import google.auth.transport.requests

credentials = google.auth.transport.requests.Request()
client = googleapiclient.discovery.build('searchconsole', 'v1', credentials=credentials)
