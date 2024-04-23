import streamlit as st
import google.generativeai as genai
import os


API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key = API_KEY)

def gemini_knowledge_base_ia(project_name, model_prompt, user_question):
    os.write(1, '🥏 Executing gemini_knowledge_base_ia \n'.encode('utf-8'))
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }
    
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
      },
    ]
    
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    
    with open("projects/" + project_name + "/knowledge_base.txt", "r") as file:
        base_knowledge = file.read()
        os.write(1, '- gemini_knowledge_base_ia: Reading knowledge_base \n'.encode('utf-8'))
    
    convo = model.start_chat(history=[
      {
        "role": "user",
        "parts": [base_knowledge]
      },
      {
        "role": "model",
        "parts": [model_prompt]
      },
    ])
    
    convo.send_message(user_question)
    os.write(1, '- gemini_knowledge_base_ia: Generating answer \n'.encode('utf-8'))
    return convo.last.text








def gemini_general_prompt(knowledge_prompt, model_prompt, user_question):
    os.write(1, '🥏 Executing gemini_general_prompt \n'.encode('utf-8'))
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }
    
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
      },
    ]
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    
    convo = model.start_chat(history=[
      {
        "role": "user",
        "parts": [knowledge_prompt]
      },
      {
        "role": "model",
        "parts": [model_prompt]
      },
    ])
    
    convo.send_message(user_question)
    os.write(1, '- gemini_general_prompt: Generating answer \n'.encode('utf-8'))
    return convo.last.text
