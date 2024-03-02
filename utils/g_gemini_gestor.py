import streamlit as st
import google.generativeai as genai

API_KEY = userdata.get(st.secrets["GEMINI_API_KEY"])
genai.configure(api_key = API_KEY)

def gemini_knowledge_base_ia(project_name):
    generation_config = {
      "temperature": 0.9,
      "top_p": 1,
      "top_k": 1,
      "max_output_tokens": 2048,
    }
    
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
      },
    ]
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    
    with open("projects/" + project_name + "/knowledge_base.txt", "r") as file:
        base_knowledge = file.read()
        print(base_knowledge[1])
    
    # convo = model.start_chat(history=[
    #   {
    #     "role": "user",
    #     "parts": [base_knowledge]
    #   },
    #   {
    #     "role": "model",
    #     "parts": ["​Ahora soy un experto en el proceso de homologacion de enfermeria en estados unidos"]
    #   },
    # ])
    
    # convo.send_message("YOUR_USER_INPUT")
    # print(convo.last.text)
