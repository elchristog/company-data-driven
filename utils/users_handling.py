import streamlit as st
import streamlit_authenticator as stauth
import datetime
import time

import utils.user_credentials as uc


def hashing_execution():
    st.write(st.session_state.hashed_passwords)

def hashing():
    password_to_hash = st.text_input("Write the password to hash:")
    hashed_passwords = stauth.Hasher([password_to_hash]).generate()
    st.session_state.hashed_passwords = hashed_passwords
    hashing_button = st.button("Start Hashing", on_click = hashing_execution)



def user_creation_execution():
    checking_username_query = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{st.session_state.username}';")
    if len(checking_username_query) < 1:
        checking_user_role = []
    else:
        checking_user_role = uc.run_query_instant(f"SELECT id FROM `company-data-driven.global.role_assignment` WHERE user_id = {checking_username_query[0].get('id')};")
    if len(st.session_state.username) < 6:
        st.toast("The username must be at least 6 characters long.")
    if len(st.session_state.checking_username_query) > 0:
        st.toast("The username is already in use.")
    if len(checking_user_role) > 0:
        st.toast("The username already has a role.")
    if st.session_state.selected_project is None:
        st.toast("Please select a project.")
    if st.session_state.selected_project != st.session_state.selected_project_confirmation:
        st.toast("The selected project and the confirmation project must match.")
    if st.session_state.user_role is None:
        st.toast("Please select a user role.")
    if st.session_state.user_role != st.session_state.user_role_confirmation:
        st.toast("The selected user role and the confirmation user role must match.")
    if st.session_state.user_first_name is None:
        st.toast("Please enter your first name.")
    if len(st.session_state.user_first_name) < 3:
        st.toast("The first name must be at least 3 characters long.")
    if st.session_state.user_last_name is None:
        st.toast("Please enter your last name.")
    if len(st.session_state.user_last_name) < 3:
        st.toast("The last name must be at least 3 characters long.")
    if st.session_state.user_email is None:
        st.toast("Please enter your email address.")
    if len(st.session_state.user_email) < 3:
        st.toast("The email address must be at least 3 characters long.")
    if st.session_state.user_birth_date is None:
        st.toast("Please enter your birth date.")
    if st.session_state.user_country is None:
        st.toast("Please select your country.")
    if len(st.session_state.user_country) < 3:
        st.toast("The country name must be at least 3 characters long.")
    if st.session_state.user_gender is None:
        st.toast("Please select your gender.")
    if len(st.session_state.user_gender) < 3:
        st.toast("The gender must be at least 3 characters long.")
    if st.session_state.user_phone_number is None:
        st.toast("Please enter your phone number.")
    if len(st.session_state.user_phone_number) < 6:
        st.toast("The phone number must be at least 6 characters long.")
    if st.session_state.user_drive_folder is None:
        st.toast("Please enter the Drive URL.")
    if len(st.session_state.user_drive_folder) < 6:
        st.toast("The Drive URL must be at least 6 characters long.")
    if len(st.session_state.username) < 6 or len(st.session_state.checking_username_query) > 0 or len(checking_user_role) > 0 or st.session_state.selected_project is None or st.session_state.selected_project != st.session_state.selected_project_confirmation or st.session_state.user_role is None or st.session_state.user_role != st.session_state.user_role_confirmation or st.session_state.user_first_name is None or len(st.session_state.user_first_name) < 3 or st.session_state.user_last_name is None or len(st.session_state.user_last_name) < 3 or st.session_state.user_email is None or len(st.session_state.user_email) < 3  or st.session_state.user_birth_date is None or st.session_state.user_country is None or len(st.session_state.user_country) < 3 or st.session_state.user_gender is None or len(st.session_state.user_gender) < 3 or st.session_state.user_phone_number is None or len(st.session_state.user_phone_number) < 6 or st.session_state.user_drive_folder is None or len(st.session_state.user_drive_folder) < 6:
        st.toast("Please fill in completely all of the required fields.")
    else:
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.users` (id, username, status, project_id, creation_date, email, name, lastname, birthdate, country, gender, user_creator_id, phone_number, user_drive_folder) VALUES({st.session_state.max_id_users}, '{st.session_state.username}', 'active', {st.session_state.selected_project_id}, '{st.session_state.today_str}', '{st.session_state.user_email.lower()}', '{st.session_state.user_first_name.lower()}', '{st.session_state.user_last_name.lower()}', '{st.session_state.user_birth_date}', '{st.session_state.user_country.lower()}', '{st.session_state.user_gender.lower()}', {st.session_state.user_id_user_creation}, '{st.session_state.user_phone_number}', '{st.session_state.user_drive_folder}');")
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.global.role_assignment` (id, user_id, role_id) VALUES({st.session_state.max_id_role_assignement}, {st.session_state.max_id_users}, {st.session_state.selected_role_id});")
        st.toast("Updating, please wait", icon = "☺️")
        time.sleep(5)
        uc.run_query_30_m.clear()
        st.toast('User Created!', icon = '🎈')
        st.balloons()
        st.warning('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        st.toast('Remember to hash the password and add to config, and create the demo task', icon = '😶‍🌫️')
        




def user_creation(user_id_user_creation, project_id, project_name): 
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    username = st.text_input("Write the username:")
    checking_username_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.global.users` WHERE username = '{username}';")
    if len(checking_username_query) > 0 or len(username) < 6 or username is None:
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
        st.session_state.selected_project = selected_project
        st.session_state.selected_project_id = selected_project_id
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
        options = ['colombia', 'united states', 'el salvador', 'mexico', 'venezuela', 'costa rica', 'chile'],
        index = None
    )
    user_gender = st.selectbox(
        label = "Select user gender",
        options = ['male', 'female'],
        index = None
    )
    user_drive_folder = st.text_input("Write the user Google Drive folder url:")
    
    st.session_state.user_id_user_creation = user_id_user_creation
    st.session_state.project_id_user_creation = project_id
    st.session_state.project_name_user_creation = project_name
    st.session_state.username_user_creation = username
    st.session_state.checking_username_query_user_creation = checking_username_query
    st.session_state.selected_project_confirmation_user_creation = selected_project_confirmation
    st.session_state.user_role_user_creation = user_role
    st.session_state.user_role_confirmation_user_creation = user_role_confirmation
    st.session_state.user_first_name_user_creation = user_first_name
    st.session_state.user_last_name_user_creation = user_last_name
    st.session_state.user_email_user_creation = user_email
    st.session_state.user_birth_date_user_creation = user_birth_date
    st.session_state.user_country_user_creation = user_country
    st.session_state.user_gender_user_creation = user_gender
    st.session_state.user_phone_number_user_creation = user_phone_number
    st.session_state.user_drive_folder_user_creation = user_drive_folder
    st.session_state.username_user_creation = username
    st.session_state.today_str_user_creation = today_str
    st.session_state.max_id_users_user_creation = max_id_users
    st.session_state.max_id_role_assignement_user_creation = max_id_role_assignement
    
    create_user_button = st.button("Create User", on_click = user_creation_execution)
