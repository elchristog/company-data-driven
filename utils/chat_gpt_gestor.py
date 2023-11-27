import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]


def prompt_ia(ia_role, input_prompt, max_tokens_answer):
    response = openai.ChatCompletion.create(
    model = st.secrets["GPT_MODEL"], # gpt-3.5-turbo, gpt-4-1106-preview
    messages = [
            {"role": "system", "content": ia_role},
            {"role": "user", "content": input_prompt}
        ],
    max_tokens = max_tokens_answer  # ajusta según el tamaño de tu artículo, maximo 4000
    )
    return response.choices[0].message['content'].strip()
