import streamlit as st

def architect(user_id, role_id):
    # admin
    if role_id == 1:
            
        # st.set_page_config(page_title="Company data driven", page_icon="💺", layout="centered", initial_sidebar_state="expanded")

        with st.sidebar:
            st.image("http://enfermeraenestadosunidos.com/wp-content/uploads/2023/08/enfermera_en_estados_unidos_logo_rn.webp", width=50, use_column_width=False)
            menu = st.sidebar.radio("Enfermera en estados unidos", ["Home", "Proyectos NO rentables", "Proyectos rentables", "Oportunidades"])
            st.write("---") 

        # Display the selected page
        if menu == "Home":

            st.write("# Welcome to Streamlit! 👋")

            # st.sidebar.success("Select a demo above.")

            st.markdown(
                """
                Streamlit is an open-source app framework built specifically for
                Machine Learning and Data Science projects.
                **👈 Select a demo from the sidebar** to see some examples
                of what Streamlit can do!
                ### Want to learn more?
                - Check out [streamlit.io](https://streamlit.io)
            """
            )   

    # customer
    if role_id == 6:
        pass