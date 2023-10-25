import streamlit as st

def architect(user_id, role_id, project_id, project_name, project_title, project_icon, project_logo_url):
    # admin
    if role_id == 1:
        with st.sidebar:
            st.image(project_logo_url, width=50, use_column_width=False)
            menu = st.sidebar.radio(project_title, ["Home", "Trafico y SEO", "Whatsapp", "Trip Wire"])
            st.write("---") 

        if menu == "Home":
            st.write("---") 
            st.write("# " + project_title + project_icon)
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
            st.write("---") 

    # customer
    if role_id == 6:
        pass