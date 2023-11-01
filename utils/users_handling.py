import streamlit as st
import streamlit_authenticator as stauth
import datetime

import utils.user_credentials as uc


def hashing():
    password_to_hash = st.text_input("Write the password to hash:")
    hashed_passwords = stauth.Hasher([password_to_hash]).generate()
    hashing_button = st.button("Start Hashing")
    if hashing_button:
        st.write(hashed_passwords[0])

def user_creation(user_id, project_id, project_name): 
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    username = st.text_input("Write the username:")
    checking_username_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{username}';")
    if len(checking_username_query) > 0 and len(username) < 6 and username is None:
        st.error('Username is not available', icon = '👻')
    else:
        st.success('Username available', icon = '🪬')
    max_id_users = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.global.users`;")[0].get('max_id')
    max_id_role_assignement = uc.run_query_instant(f"SELECT 1 + MAX(id) AS max_id FROM `company-data-driven.global.role_assignment`;")[0].get('max_id')
    get_projects = uc.run_query_30_m(f"SELECT id, name FROM `company-data-driven.global.projects`;")
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
    
    get_roles = uc.run_query_30_m(f"SELECT id, name FROM `company-data-driven.global.roles`;")
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
    if user_role is not None:
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
    user_phone_number = st.text_input("Write the user phone number:")
    user_birth_date = st.date_input("User birth date:", min_value = datetime.date(1970,1,1)) 
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
        checking_username_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{username}';")
        if len(username) < 6:
            st.error("The username must be at least 6 characters long.")
        if len(checking_username_query) > 0:
            st.error("The username is already in use.")
        if selected_project is None:
            st.error("Please select a project.")
        if selected_project != selected_project_confirmation:
            st.error("The selected project and the confirmation project must match.")
        if user_role is None:
            st.error("Please select a user role.")
        if user_role != user_role_confirmation:
            st.error("The selected user role and the confirmation user role must match.")
        if user_first_name is None:
            st.error("Please enter your first name.")
        if len(user_first_name) < 3:
            st.error("The first name must be at least 3 characters long.")
        if user_last_name is None:
            st.error("Please enter your last name.")
        if len(user_last_name) < 3:
            st.error("The last name must be at least 3 characters long.")
        if user_email is None:
            st.error("Please enter your email address.")
        if len(user_email) < 3:
            st.error("The email address must be at least 3 characters long.")
        if user_birth_date is None:
            st.error("Please enter your birth date.")
        if user_country is None:
            st.error("Please select your country.")
        if len(user_country) < 3:
            st.error("The country name must be at least 3 characters long.")
        if user_gender is None:
            st.error("Please select your gender.")
        if len(user_gender) < 3:
            st.error("The gender must be at least 3 characters long.")
        if user_phone_number is None:
            st.error("Please enter your phone number.")
        if len(user_phone_number) < 6:
            st.error("The phone number must be at least 6 characters long.")
        if len(username) < 6 or len(checking_username_query) > 0 or selected_project is None or selected_project != selected_project_confirmation or user_role is None or user_role != user_role_confirmation or user_first_name is None or len(user_first_name) < 3 or user_last_name is None or len(user_last_name) < 3 or user_email is None or len(user_email) < 3  or user_birth_date is None or user_country is None or len(user_country) < 3 or user_gender is None or len(user_gender) < 3 or user_phone_number is None or len(user_phone_number) < 6:
            st.error("Please fill in completely all of the required fields.")
        else:
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.users` (id, username, status, project_id, creation_date, email, name, lastname, birthdate, country, gender, user_creator_id, phone_number) VALUES({max_id_users}, '{username}', 'active', {selected_project_id}, '{today_str}', '{user_email.lower()}', '{user_first_name.lower()}', '{user_last_name.lower()}', '{user_birth_date}', '{user_country.lower()}', '{user_gender.lower()}', {user_id}, '{user_phone_number}');")
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.users` (id, user_id, role_id) VALUES({max_id_role_assignement}, {max_id_users}, {selected_role_id});")
            st.success('User Created!', icon = '🎈')
            st.warning('Remember to has the password and add to config', icon = '😶‍🌫️')









