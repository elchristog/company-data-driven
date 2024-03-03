import streamlit as st
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]


def prompt_ia(ia_role, input_prompt, max_tokens_answer):
    os.write(1, '🥏 Executing prompt_ia \n'.encode('utf-8'))
    response = openai.ChatCompletion.create(
    model = st.secrets["GPT_MODEL"], # gpt-3.5-turbo, gpt-4-1106-preview
    messages = [
            {"role": "system", "content": ia_role},
            {"role": "user", "content": input_prompt}
        ],
    max_tokens = max_tokens_answer  # ajusta según el tamaño de tu artículo, maximo 4000
    )
    os.write(1, '- prompt_ia: Generating answer \n'.encode('utf-8'))
    return response.choices[0].message['content'].strip()
