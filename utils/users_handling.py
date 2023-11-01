import streamlit as st
import streamlit_authenticator as stauth

import utils.user_credentials as uc


def hashing():
    password_to_hash = st.text_input("Write the password to hash:")
    hashed_passwords = stauth.Hasher([password_to_hash]).generate()
    hashing_button = st.button("Start Hashing")
    if hashing_button:
        st.write(hashed_passwords[0])

def user_creation(user_id, project_id, project_name): 
    username = st.text_input("Write the username:")
    check_username_availability = st.button("Check Availability")
    if check_username_availability: #name, birthdate, country, gender, user_creator, email, project_id
        checking_username_query = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{username}';")
        if len(checking_username_query) > 0:
            st.error('Username is not available', icon = '👻')
        else:
            st.success('Username available', icon = '🪬')
    max_id_users = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.global.users`;")[0].get('max_id')
    get_projects = uc.run_query_instant(f"SELECT id, name FROM `company-data-driven.global.projects`;")
    project_ids = []
    project_names = []
    for row in get_projects:
        project_ids.append(row.get('id'))
        project_names.append(row.get('name'))
    selected_project = st.selectbox(
        label = "Select the project for the user",
        options = project_names,
        index = None
    )
    if selected_project is not None:
        selected_project_id = project_ids[project_names.index(selected_project)]
    selected_project_confirmation = st.selectbox(
        label = "Confirm the project for the user",
        options = project_names,
        index = None
    )
    if selected_project is not None and selected_project_confirmation is not None:
        if selected_project == selected_project_confirmation:
            st.success('Project confirmed', icon = '🎈')
        else:
            st.error('Incorrect project', icon = '🀄')
    
    get_roles = uc.run_query_instant(f"SELECT id, name FROM `company-data-driven.global.roles`;")
    roles_ids = []
    roles_names = []
    for row in get_roles:
        roles_ids.append(row.get('id'))
        roles_names.append(row.get('name'))

    user_role = st.selectbox(
        label = "Select user role",
        options = roles_names,
        index = None
    )
    selected_role_id = roles_ids[roles_names.index(user_role)]
    user_role_confirmation = st.selectbox(
        label = "Confirm user role",
        options = roles_names,
        index = None
    )
    if user_role is not None and user_role_confirmation is not None:
        if user_role == user_role_confirmation:
            st.success('Role confirmed', icon = '🎈')
        else:
            st.error('Incorrect role', icon = '🀄')

    user_first_name = st.text_input("Write the user first name:")
    user_last_name = st.text_input("Write the user last name:")
    user_email = st.text_input("Write the user email:")
    commitment_birth_date = st.date_input("User birth date:")
    user_country = st.selectbox(
        label = "Select user country",
        options = ['colombia', 'united states'],
        index = None
    )
    user_gender = st.selectbox(
        label = "Select user gender",
        options = ['male', 'female'],
        index = None
    )
    
    create_user_button = st.button("Create User")
    if create_user_button:
        pass






