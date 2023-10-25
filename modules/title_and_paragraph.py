import streamlit as st

def title_and_paragraph(title_text, paragraph_text):
    st.write("# " + title_text)
    st.write(paragraph_text)   
    st.write("---") 