import pandas as pd
import numpy as np
import streamlit as st
import os

# from pycaret.classification import *

import utils.user_credentials as uc

# def ml_purchase_propension_execution():
#     os.write(1, '🥏 Executing posting_posts_execution \n'.encode('utf-8'))
#     if 'posting_posts_selected_idea' in st.session_state:
#         os.write(1, '- posting_posts_execution: Saving posted idea\n'.encode('utf-8'))
#         st.toast("Please wait", icon = "☺️")
#         uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.posting_posts_project_name}.daily_post_creation` SET posted = 1, posted_date = CURRENT_DATE(), poster_user_id = {st.session_state.posting_posts_user_id} WHERE id = '{st.session_state.posting_posts_selected_idea_id}'")
#         st.toast("Info saved!", icon = "👾")
#         st.balloons()
#         time.sleep(1)
#         uc.run_query_half_day.clear()
#         del st.session_state.posting_posts_user_id
#         del st.session_state.posting_posts_project_name
#         del st.session_state.posting_posts_post_idea
#         del st.session_state.posting_posts_selected_idea_id 


def ml_purchase_propension(user_id, project_name):
    os.write(1, '🥏 Executing ml_purchase_propension \n'.encode('utf-8'))
    os.write(1, '- ml_purchase_propension: Showing form \n'.encode('utf-8'))

    rows = pd.DataFrame(uc.run_query_half_day(f"WITH groupal_session_contacts AS (     SELECT traffic_analytics_whatsapp_leads_id, COUNT(id) AS num_groupal_session_crm_contacts, SUM(CASE WHEN user_status = 'active' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_status, SUM(CASE WHEN user_status = 'active_15_days' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_15_days_status, SUM(CASE WHEN user_status = 'active_30_days' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_30_days_status, SUM(CASE WHEN user_status = 'active_60_days' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_60_days_status, SUM(CASE WHEN user_status = 'lost' THEN 1 ELSE 0 END) AS num_groupal_session_crm_lost_status, SUM(CASE WHEN user_status = 'discarted' THEN 1 ELSE 0 END) AS num_groupal_session_crm_discarted_status, STRING_AGG(contact_description, '- ') AS groupal_session_contacts_description, MAX(contact_date) AS last_groupal_session_contact_date FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` GROUP BY traffic_analytics_whatsapp_leads_id     ),      groupal_session_assistants AS (     SELECT traffic_analytics_whatsapp_lead_id, MAX(meeting_date) AS groupal_session_assistance_last_assistance_absent_registration, SUM(CASE WHEN status = 'assistant' THEN 1 ELSE 0 END) AS grupal_session_num_times_assisted, SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) AS grupal_session_num_times_absented FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` GROUP BY traffic_analytics_whatsapp_lead_id     ),     contract_contacts AS (     SELECT traffic_analytics_whatsapp_leads_id, COUNT(id) AS num_contract_crm_contacts, SUM(CASE WHEN user_status = 'active' THEN 1 ELSE 0 END) AS num_contract_crm_active_status, SUM(CASE WHEN user_status = 'active_15_days' THEN 1 ELSE 0 END) AS num_contract_crm_active_15_days_status, SUM(CASE WHEN user_status = 'active_30_days' THEN 1 ELSE 0 END) AS num_contract_crm_active_30_days_status, SUM(CASE WHEN user_status = 'active_60_days' THEN 1 ELSE 0 END) AS num_contract_crm_active_60_days_status, SUM(CASE WHEN user_status = 'lost' THEN 1 ELSE 0 END) AS num_contract_crm_lost_status, SUM(CASE WHEN user_status = 'discarted' THEN 1 ELSE 0 END) AS num_contract_crm_discarted_status, STRING_AGG(contact_description, '- ') AS contract_contacts_description, MAX(contact_date) AS last_contract_contact_date FROM `company-data-driven.{project_name}.contract_crm_log` GROUP BY traffic_analytics_whatsapp_leads_id     )     SELECT tawl.id, tawl.creation_date, tawl.phone_indicator, DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(tawl.creation_date AS DATE), DAY) AS days_since_lead, COALESCE(groupal_session_contacts.num_groupal_session_crm_contacts, 0) AS num_groupal_session_crm_contacts, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_status, 0) AS num_groupal_session_crm_active_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_15_days_status, 0) AS num_groupal_session_crm_active_15_days_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_30_days_status, 0) AS num_groupal_session_crm_active_30_days_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_60_days_status, 0) AS num_groupal_session_crm_active_60_days_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_lost_status, 0) AS num_groupal_session_crm_lost_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_discarted_status, 0) AS num_groupal_session_crm_discarted_status, groupal_session_contacts.groupal_session_contacts_description, COALESCE(DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(groupal_session_contacts.last_groupal_session_contact_date AS DATE), DAY), 9999) AS days_since_last_groupal_session_crm_contact, CASE WHEN DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(groupal_session_contacts.last_groupal_session_contact_date AS DATE), DAY) IS NULL THEN 1 ELSE 0 END AS indicator_groupal_session_dont_registered, COALESCE(DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(groupal_session_assistants.groupal_session_assistance_last_assistance_absent_registration AS DATE), DAY), 9999) AS days_since_last_absent_assist_registration, COALESCE(groupal_session_assistants.grupal_session_num_times_assisted, 0) AS grupal_session_num_times_assisted, COALESCE(groupal_session_assistants.grupal_session_num_times_absented, 0) AS grupal_session_num_times_absented, COALESCE(contract_contacts.num_contract_crm_contacts, 0) AS num_contract_crm_contacts, COALESCE(contract_contacts.num_contract_crm_active_status, 0) AS num_contract_crm_active_status, COALESCE(contract_contacts.num_contract_crm_active_15_days_status, 0) AS num_contract_crm_active_15_days_status, COALESCE(contract_contacts.num_contract_crm_active_30_days_status, 0) AS num_contract_crm_active_30_days_status, COALESCE(contract_contacts.num_contract_crm_active_60_days_status, 0) AS num_contract_crm_active_60_days_status, COALESCE(contract_contacts.num_contract_crm_lost_status, 0) AS num_contract_crm_lost_status, COALESCE(contract_contacts.num_contract_crm_discarted_status, 0) AS num_contract_crm_discarted_status, contract_contacts.contract_contacts_description, COALESCE(DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(contract_contacts.last_contract_contact_date AS DATE), DAY), 9999) AS days_since_last_contract_crm_contact, CASE WHEN c.contract_date IS NULL THEN 0 ELSE 1 END AS target_contract      FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl LEFT JOIN `company-data-driven.{project_name}.contracts` AS c ON tawl.id = c.traffic_analytics_whatsapp_leads_id LEFT JOIN groupal_session_contacts ON tawl.id = groupal_session_contacts.traffic_analytics_whatsapp_leads_id LEFT JOIN groupal_session_assistants ON tawl.id = groupal_session_assistants.traffic_analytics_whatsapp_lead_id LEFT JOIN contract_contacts ON tawl.id = contract_contacts.traffic_analytics_whatsapp_leads_id  WHERE LENGTH(tawl.phone_number) > 6;"))
    st.table(rows.head(2))

    

    # if selected_idea is not None:
    #     st.session_state.posting_posts_user_id = user_id
    #     st.session_state.posting_posts_project_name = project_name
    #     st.session_state.posting_posts_selected_idea_id = ids[ideas.index(selected_idea)]
    #     posting_posts_button = st.button("Post published", on_click = ml_purchase_propension_execution)
        
