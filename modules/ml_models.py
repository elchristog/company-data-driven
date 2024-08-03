import pandas as pd
import numpy as np
import streamlit as st
import os

# from pycaret.classification import *

import utils.user_credentials as uc

def ml_purchase_propension_training():
    os.write(1, '🥏 Executing ml_purchase_propension_training \n'.encode('utf-8'))
    if 'processed_data_query' in st.session_state:
        os.write(1, '- ml_purchase_propension_training: Retraining model\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"CREATE OR REPLACE MODEL `company-data-driven.{project_name}.purchase_propension_model` OPTIONS ( model_type='LOGISTIC_REG',   auto_class_weights=TRUE, enable_global_explain=TRUE,  data_split_method='NO_SPLIT',   input_label_cols=['target_contract'],   max_iterations=15) AS SELECT * EXCEPT(data_frame) FROM( {st.session_state.processed_data_query }  ) WHERE data_frame = 'training';")
        st.toast("Model retrained!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.ml_purchase_propension_user_id
        del st.session_state.ml_purchase_propension_project_name


def ml_purchase_propension(user_id, project_name):
    os.write(1, '🥏 Executing ml_purchase_propension \n'.encode('utf-8'))
    os.write(1, '- ml_purchase_propension: Showing form \n'.encode('utf-8'))

    st.session_state.processed_data_query = f"WITH groupal_session_contacts AS (     SELECT traffic_analytics_whatsapp_leads_id, COUNT(id) AS num_groupal_session_crm_contacts, SUM(CASE WHEN user_status = 'active' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_status, SUM(CASE WHEN user_status = 'active_15_days' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_15_days_status, SUM(CASE WHEN user_status = 'active_30_days' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_30_days_status, SUM(CASE WHEN user_status = 'active_60_days' THEN 1 ELSE 0 END) AS num_groupal_session_crm_active_60_days_status, SUM(CASE WHEN user_status = 'lost' THEN 1 ELSE 0 END) AS num_groupal_session_crm_lost_status, SUM(CASE WHEN user_status = 'discarted' THEN 1 ELSE 0 END) AS num_groupal_session_crm_discarted_status, STRING_AGG(contact_description, '- ') AS groupal_session_contacts_description, MAX(contact_date) AS last_groupal_session_contact_date FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` GROUP BY traffic_analytics_whatsapp_leads_id     ),      groupal_session_assistants AS (     SELECT traffic_analytics_whatsapp_lead_id, MAX(meeting_date) AS groupal_session_assistance_last_assistance_absent_registration, SUM(CASE WHEN status = 'assistant' THEN 1 ELSE 0 END) AS grupal_session_num_times_assisted, SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) AS grupal_session_num_times_absented FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` GROUP BY traffic_analytics_whatsapp_lead_id     ),     contract_contacts AS (     SELECT traffic_analytics_whatsapp_leads_id, COUNT(id) AS num_contract_crm_contacts, SUM(CASE WHEN user_status = 'active' THEN 1 ELSE 0 END) AS num_contract_crm_active_status, SUM(CASE WHEN user_status = 'active_15_days' THEN 1 ELSE 0 END) AS num_contract_crm_active_15_days_status, SUM(CASE WHEN user_status = 'active_30_days' THEN 1 ELSE 0 END) AS num_contract_crm_active_30_days_status, SUM(CASE WHEN user_status = 'active_60_days' THEN 1 ELSE 0 END) AS num_contract_crm_active_60_days_status, SUM(CASE WHEN user_status = 'lost' THEN 1 ELSE 0 END) AS num_contract_crm_lost_status, SUM(CASE WHEN user_status = 'discarted' THEN 1 ELSE 0 END) AS num_contract_crm_discarted_status, STRING_AGG(contact_description, '- ') AS contract_contacts_description, MAX(contact_date) AS last_contract_contact_date FROM `company-data-driven.{project_name}.contract_crm_log` GROUP BY traffic_analytics_whatsapp_leads_id     )     SELECT tawl.creation_date, tawl.phone_indicator, DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(tawl.creation_date AS DATE), DAY) AS days_since_lead, COALESCE(groupal_session_contacts.num_groupal_session_crm_contacts, 0) AS num_groupal_session_crm_contacts, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_status, 0) AS num_groupal_session_crm_active_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_15_days_status, 0) AS num_groupal_session_crm_active_15_days_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_30_days_status, 0) AS num_groupal_session_crm_active_30_days_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_active_60_days_status, 0) AS num_groupal_session_crm_active_60_days_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_lost_status, 0) AS num_groupal_session_crm_lost_status, COALESCE(groupal_session_contacts.num_groupal_session_crm_discarted_status, 0) AS num_groupal_session_crm_discarted_status, groupal_session_contacts.groupal_session_contacts_description, COALESCE(DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(groupal_session_contacts.last_groupal_session_contact_date AS DATE), DAY), 9999) AS days_since_last_groupal_session_crm_contact, CASE WHEN DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(groupal_session_contacts.last_groupal_session_contact_date AS DATE), DAY) IS NULL THEN 1 ELSE 0 END AS indicator_groupal_session_dont_registered, COALESCE(DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(groupal_session_assistants.groupal_session_assistance_last_assistance_absent_registration AS DATE), DAY), 9999) AS days_since_last_absent_assist_registration, COALESCE(groupal_session_assistants.grupal_session_num_times_assisted, 0) AS grupal_session_num_times_assisted, COALESCE(groupal_session_assistants.grupal_session_num_times_absented, 0) AS grupal_session_num_times_absented, COALESCE(contract_contacts.num_contract_crm_contacts, 0) AS num_contract_crm_contacts, COALESCE(contract_contacts.num_contract_crm_active_status, 0) AS num_contract_crm_active_status, COALESCE(contract_contacts.num_contract_crm_active_15_days_status, 0) AS num_contract_crm_active_15_days_status, COALESCE(contract_contacts.num_contract_crm_active_30_days_status, 0) AS num_contract_crm_active_30_days_status, COALESCE(contract_contacts.num_contract_crm_active_60_days_status, 0) AS num_contract_crm_active_60_days_status, COALESCE(contract_contacts.num_contract_crm_lost_status, 0) AS num_contract_crm_lost_status, COALESCE(contract_contacts.num_contract_crm_discarted_status, 0) AS num_contract_crm_discarted_status, contract_contacts.contract_contacts_description, COALESCE(DATE_DIFF(COALESCE(CAST(c.contract_date AS DATE), CURRENT_DATE()), CAST(contract_contacts.last_contract_contact_date AS DATE), DAY), 9999) AS days_since_last_contract_crm_contact, CASE WHEN c.contract_date IS NULL THEN 0 ELSE 1 END AS target_contract, CASE WHEN tawl.creation_date < DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY) THEN 'training' WHEN tawl.creation_date > DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) THEN 'prediction' ELSE 'evaluation' END AS data_frame  FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl LEFT JOIN `company-data-driven.{project_name}.contracts` AS c ON tawl.id = c.traffic_analytics_whatsapp_leads_id LEFT JOIN groupal_session_contacts ON tawl.id = groupal_session_contacts.traffic_analytics_whatsapp_leads_id LEFT JOIN groupal_session_assistants ON tawl.id = groupal_session_assistants.traffic_analytics_whatsapp_lead_id LEFT JOIN contract_contacts ON tawl.id = contract_contacts.traffic_analytics_whatsapp_leads_id  WHERE LENGTH(tawl.phone_number) > 6"

    # Showing confussion matrix and lift chart in last evaluation data
    rows = pd.DataFrame(uc.run_query_half_day(st.session_state.processed_data_query))
    st.table(rows.head(2))

    # showing confussion matrix in last prediction data

    st.session_state.ml_purchase_propension_user_id = user_id
    st.session_state.ml_purchase_propension_project_name = project_name
    
    re_train_model_button = st.button("Re train model", on_click = ml_purchase_propension_training)

    # select threshold and looking confussion matrix and lift chart in evaluation sample

    # save threshold

    # auto predict weekly for all the dataset.

        
