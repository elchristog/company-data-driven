import streamlit as st

def title_and_paragraph(title_text, paragraph_text, title_type, divider):
    if title_type == "h1":
        st.write("# " + title_text)
    if title_type == "h2":
        st.write("## " + title_text)
    if title_type == "h3":
        st.write("### " + title_text)
    if title_type == "h4":
        st.write("#### " + title_text)
    st.write(paragraph_text)   
    if divider == 1:
        st.write("---") 