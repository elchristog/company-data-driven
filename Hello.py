import streamlit as st

import utils.login as login

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.write("# Please log in")
    login.login()
    # st.set_page_config(page_title="Company data driven", page_icon="💺", layout="centered", initial_sidebar_state="expanded")

    # with st.sidebar:
    #   # st.image("cell-tower.png", width=100, use_column_width=False)
    #   menu = st.sidebar.radio("Menu", ["Home", "Proyectos NO rentables", "Proyectos rentables", "Oportunidades"])
    #   st.write("---") 

    # # Display the selected page
    # if menu == "Home":

    #   st.write("# Welcome to Streamlit! 👋")

    #   # st.sidebar.success("Select a demo above.")

    #   st.markdown(
    #       """
    #       Streamlit is an open-source app framework built specifically for
    #       Machine Learning and Data Science projects.
    #       **👈 Select a demo from the sidebar** to see some examples
    #       of what Streamlit can do!
    #       ### Want to learn more?
    #       - Check out [streamlit.io](https://streamlit.io)
    #   """
    #   )


if __name__ == "__main__":
    run()
