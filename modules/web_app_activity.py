import streamlit as st
import datetime

import utils.user_credentials as uc

@st.fragment
def login_activity(team_or_customer):
    if team_or_customer == 'customer':
        st.header("Top 5 customers without login")
        top_5_users_without_login = uc.run_query_6_h(f"SELECT u.id, u.username, u.name, u.lastname, u.last_login_date, DATE_DIFF(CURRENT_DATE(), u.last_login_date, DAY) AS days_without_login FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE ra.role_id = 6 AND u.status = 'active' ORDER BY days_without_login DESC LIMIT 5")
    if team_or_customer == 'team':
        st.header("Top 5 team members without login")
        top_5_users_without_login = uc.run_query_6_h(f"SELECT u.id, u.username, u.name, u.lastname, u.last_login_date, DATE_DIFF(CURRENT_DATE(), u.last_login_date, DAY) AS days_without_login FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE ra.role_id <> 6 AND u.status = 'active' ORDER BY days_without_login DESC LIMIT 5")
    st.table(top_5_users_without_login)
