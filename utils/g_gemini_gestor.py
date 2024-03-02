import streamlit as st
import google.generativeai as genai

API_KEY=userdata.get(st.secrets["GEMINI_API_KEY"])
genai.configure(api_key= API_KEY)

def gemini_knowledge_base_ia():
    pass
