import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_gsa(df_grouped):
    df_grouped['date'] = df_grouped['date'].astype(str)

    options = {
        "xAxis": {
            "type": "category",
            "data": df_grouped['date'].tolist(),
            "axisLabel": {
                "formatter": "{value}"
            }
        },
        "yAxis": {"type": "value", "name": ""},
        "grid": {
            "right": 20,
            "left": 65,
            "top": 45,
            "bottom": 50,
        },
        "legend": {
            "show": True,
            "top": "top",
            "align": "auto",
            "selected": {  
                "groupal_session_clicks": True,        
                "num_assistants": False
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "groupal_session_clicks",
                "data": df_grouped['groupal_session_clicks'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "num_assistants",
                "data": df_grouped["num_assistants"].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,
            }
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  
        ],
        "backgroundColor": "#ffffff",
        "color": ["#A6785D", "#394A59"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')




def groupal_session_show_metrics(project_name, bitly_groupal_session_link):
  dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
  if len(dates_bitly) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (dates_bitly[0].get('min_date_bitly'), dates_bitly[0].get('max_date_bitly')),
          min_value=dates_bitly[0].get('min_date_bitly'),
          max_value=dates_bitly[0].get('max_date_bitly'),
          format="DD/MM/YYYY",
          help='',
          key = 'day_gsa'
      )

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT groupal_session_clicks_df.date, groupal_session_clicks_df.groupal_session_clicks, meeting_assistance.num_assistants FROM (SELECT meeting_date, COUNT(id) AS num_assistants FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` WHERE status = 'assistant' GROUP BY meeting_date) AS meeting_assistance RIGHT OUTER JOIN (SELECT date, SUM(clicks) AS groupal_session_clicks FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` WHERE bitly_link = '{bitly_groupal_session_link}' AND date >= '{day[0].strftime('%Y-%m-%d')}'  AND  date <= '{day[1].strftime('%Y-%m-%d')}'   GROUP BY date) AS groupal_session_clicks_df ON meeting_assistance.meeting_date = groupal_session_clicks_df.date ORDER BY groupal_session_clicks_df.date ASC;"))

      df_conversion["num_assistants"] = df_conversion["num_assistants"].fillna(0)
      bitly_clicks_groupal_session = df_conversion['groupal_session_clicks'].sum()
      num_assistants = df_conversion['num_assistants'].sum()
      conversion = num_assistants/bitly_clicks_groupal_session
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('bitly_clicks_groupal_session:', f'{bitly_clicks_groupal_session:,}')
      with met2:
          st.metric('num_assistants:', f'{num_assistants:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_gsa(df_conversion)





def add_new_assistant_execution(user_id, project_name, selected_phone_id, meeting_date):
    already_created = uc.run_query_instant(f"SELECT id FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` WHERE traffic_analytics_whatsapp_lead_id = '{selected_phone_id}' AND meeting_date = '{meeting_date}'")
    if len(already_created) > 0:
        st.toast("User already attended this meeting", icon = "☺️")
    else:
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` (id, traffic_analytics_whatsapp_lead_id, meeting_date, creator_user_id, status) VALUES (GENERATE_UUID(), '{selected_phone_id}', '{meeting_date}', {user_id}, 'assistant');")
        st.toast("Assistant saved!", icon = "👾")
        st.balloons()
        time.sleep(5)
        uc.run_query_half_day.clear()
        uc.run_query_30_m.clear()
        uc.run_query_1_h.clear()




def add_new_assistant(user_id, project_name):
    rows = uc.run_query_half_day(f"SELECT id, CONCAT(phone_indicator,phone_number) AS full_phone_number FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
    assistant_ids = []
    assistant_phone_numbers = []
    for row in rows:
        assistant_ids.append(row.get('id'))
        assistant_phone_numbers.append(row.get('full_phone_number'))
    selected_phone = st.selectbox(
            label = "Select the assistant phone number",
            options = assistant_phone_numbers,
            index = None,
            key= "assistant_phone_numbers"
        )
    checking_phone_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE CONCAT(phone_indicator,phone_number) LIKE '{selected_phone}' ")
    if len(checking_phone_query) < 1 or checking_phone_query is None:
        st.error('Phone number does not exists, should be created adding a new lead into Whatsapp', icon = '👻')
    else:
        st.success('Phone number available', icon = '🪬')
        if selected_phone is not None:
            selected_phone_id = assistant_ids[assistant_phone_numbers.index(selected_phone)]
            meeting_date = st.date_input("Meeting date:", key = 'meeting_date')
            add_assistant_button = st.button("Add assistant", on_click = add_new_assistant_execution, args = [user_id, project_name, selected_phone_id, meeting_date])










def add_new_absent_execution(user_id, project_name, selected_phone_id, meeting_date):
    already_created = uc.run_query_instant(f"SELECT id FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` WHERE traffic_analytics_whatsapp_lead_id = '{selected_phone_id}' AND meeting_date = '{meeting_date}'")
    if len(already_created) > 0:
        st.toast("User already absented in this meeting", icon = "☺️")
    else:
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` (id, traffic_analytics_whatsapp_lead_id, meeting_date, creator_user_id, status) VALUES (GENERATE_UUID(), '{selected_phone_id}', '{meeting_date}', {user_id}, 'absent');")
        st.toast("Assistant saved!", icon = "👾")
        st.balloons()
        time.sleep(5)
        uc.run_query_half_day.clear()
        uc.run_query_30_m.clear()
        uc.run_query_1_h.clear()




def add_new_absent(user_id, project_name):
    rows = uc.run_query_half_day(f"SELECT id, CONCAT(phone_indicator,phone_number) AS full_phone_number FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
    assistant_ids = []
    assistant_phone_numbers = []
    for row in rows:
        assistant_ids.append(row.get('id'))
        assistant_phone_numbers.append(row.get('full_phone_number'))
    selected_phone = st.selectbox(
            label = "Select the absent phone number",
            options = assistant_phone_numbers,
            index = None,
            key= "assistant_phone_numbers"
        )
    checking_phone_query = uc.run_query_30_m(f"SELECT id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE CONCAT(phone_indicator,phone_number) LIKE '{selected_phone}' ")
    if len(checking_phone_query) < 1 or checking_phone_query is None:
        st.error('Phone number does not exists, should be created adding a new lead into Whatsapp', icon = '👻')
    else:
        st.success('Phone number available', icon = '🪬')
        if selected_phone is not None:
            selected_phone_id = assistant_ids[assistant_phone_numbers.index(selected_phone)]
            meeting_date = st.date_input("Meeting date:", key = 'meeting_date')
            add_assistant_button = st.button("Add absent", on_click = add_new_absent_execution, args = [user_id, project_name, selected_phone_id, meeting_date])







def groupal_session_absents_and_opportunities(project_name):
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Absents")
        absents_df = uc.run_query_instant(f"SELECT CONCAT(tawl.phone_indicator ,tawl.phone_number) AS phone_number, (COALESCE(DATE_DIFF(CURRENT_DATE(), last_contact_df.last_contact_date, DAY), 99999) - CASE WHEN last_contact_df.last_user_status LIKE '%15%' THEN 15 WHEN last_contact_df.last_user_status LIKE '%30%' THEN 30 WHEN last_contact_df.last_user_status LIKE '%60%' THEN 60 ELSE 0 END) AS days_since_last_contact, DATE_DIFF(CURRENT_DATE(), days_absent_df.last_status_date, DAY) AS days_absent FROM ( SELECT traffic_analytics_whatsapp_lead_id, status AS last_status, meeting_date AS last_status_date, ROW_NUMBER() OVER(PARTITION BY traffic_analytics_whatsapp_lead_id ORDER BY meeting_date DESC) AS meeting_number FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance`) AS days_absent_df INNER JOIN `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl ON days_absent_df.traffic_analytics_whatsapp_lead_id = tawl.id LEFT OUTER JOIN (SELECT tagsc.traffic_analytics_whatsapp_leads_id, LAST_VALUE(tagsc.user_status) OVER(PARTITION BY tagsc.traffic_analytics_whatsapp_leads_id ORDER BY tagsc.contact_date) AS last_user_status, LAST_VALUE(tagsc.contact_date) OVER(PARTITION BY tagsc.traffic_analytics_whatsapp_leads_id ORDER BY tagsc.contact_date) AS last_contact_date FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` AS tagsc) AS last_contact_df ON days_absent_df.traffic_analytics_whatsapp_lead_id = last_contact_df.traffic_analytics_whatsapp_leads_id WHERE days_absent_df.meeting_number = 1 AND last_status = 'absent' AND (last_contact_df.last_user_status LIKE '%active%' OR last_contact_df.last_user_status  IS NULL) AND (COALESCE(DATE_DIFF(CURRENT_DATE(), last_contact_df.last_contact_date, DAY), 99999) - CASE WHEN last_contact_df.last_user_status LIKE '%15%' THEN 15 WHEN last_contact_df.last_user_status LIKE '%30%' THEN 30 WHEN last_contact_df.last_user_status LIKE '%60%' THEN 60 ELSE 0 END) > 3 ORDER BY days_since_last_contact DESC LIMIT 15;")
        if len(absents_df) < 1:
          st.warning("Waiting for data")
        else:
          st.table(absents_df)
    with col2:
        st.write("### Never attended")
        never_attended_df = uc.run_query_instant(f"SELECT CONCAT(tawl.phone_indicator, tawl.phone_number) AS phone_number, (COALESCE(DATE_DIFF(CURRENT_DATE(), last_contact_df.last_contact_date, DAY), 99999) - CASE WHEN last_contact_df.last_user_status LIKE '%15%' THEN 15 WHEN last_contact_df.last_user_status LIKE '%30%' THEN 30 WHEN last_contact_df.last_user_status LIKE '%60%' THEN 60 ELSE 0 END) AS days_since_last_contact, DATE_DIFF(CURRENT_DATE(), tawl.creation_date, DAY) AS days_since_creation FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl LEFT OUTER JOIN (SELECT tagsc.traffic_analytics_whatsapp_leads_id, LAST_VALUE(tagsc.user_status) OVER(PARTITION BY tagsc.traffic_analytics_whatsapp_leads_id ORDER BY tagsc.contact_date) AS last_user_status, LAST_VALUE(tagsc.contact_date) OVER(PARTITION BY tagsc.traffic_analytics_whatsapp_leads_id ORDER BY tagsc.contact_date) AS last_contact_date FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` AS tagsc) AS last_contact_df ON tawl.id = last_contact_df.traffic_analytics_whatsapp_leads_id WHERE (last_contact_df.last_user_status LIKE '%active%' OR last_contact_df.last_user_status IS NULL) AND tawl.id NOT IN (SELECT DISTINCT(traffic_analytics_whatsapp_lead_id) AS whatsapp_id FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance`) AND (COALESCE(DATE_DIFF(CURRENT_DATE(), last_contact_df.last_contact_date, DAY), 99999) - CASE WHEN last_contact_df.last_user_status LIKE '%15%' THEN 15 WHEN last_contact_df.last_user_status LIKE '%30%' THEN 30 WHEN last_contact_df.last_user_status LIKE '%60%' THEN 60 ELSE 0 END) > 3 ORDER BY days_since_last_contact DESC, days_since_creation DESC LIMIT 15;")
        if len(never_attended_df) < 1:
          st.warning("Waiting for data")
        else:
          st.table(never_attended_df)










def add_new_crm_groupal_session_contact_execution(user_id, project_name, selected_phone_id, contact_date, user_status, contact_description):
    # Input validation
    if contact_description is None or len(contact_description) < 36 or user_status is None:
        st.toast("contact_description can not be null or too short", icon="☺️") 
        st.toast("user_status can not be null", icon="☺️")
        return

   # Potentially Combined Query (If performant on your dataset)
    results =  uc.run_query_instant(f"""
        SELECT 
          MAX(contact_date) AS last_contact_date,
          FIRST_VALUE(user_status) OVER (PARTITION BY traffic_analytics_whatsapp_leads_id ORDER BY contact_date DESC) AS last_user_status
        FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm`
        WHERE traffic_analytics_whatsapp_leads_id = '{selected_phone_id}' 
        GROUP BY traffic_analytics_whatsapp_leads_id;
    """)

    last_contact_date_value = results[0].get("last_contact_date") 
    last_user_status = results[0].get("last_user_status")

    # Simplified Condition Checks
    if last_user_status in ("discarted", "lost"):
        st.toast("No se puede realizar la acción. El usuario ya no está activo.", icon="😔")
        return

    if last_contact_date_value and contact_date <= last_contact_date_value:
        st.toast("User already contacted on that date", icon = "☺️")
        return 

    # Main processing logic
    st.toast("Please wait", icon="☺️")
    contact_description = ''.join(i for i in contact_description if not i.isdigit())
    uc.run_query_insert_update(f"...")  # Your insertion query
    st.toast("CRM Contact saved!", icon="👾")
    st.balloons()
    time.sleep(5)
    uc.run_query_half_day.clear()
    uc.run_query_30_m.clear()
    uc.run_query_1_h.clear()



        




def add_new_crm_groupal_session_contact(user_id, project_name):
    rows = uc.run_query_half_day(f"SELECT tawl.id, CONCAT(tawl.phone_indicator,tawl.phone_number) AS full_phone_number, COALESCE(DATE_DIFF(CURRENT_DATE(), last_crm_status.last_contact_date, DAY), 99999) AS days_since_last_contact FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS tawl LEFT OUTER JOIN (SELECT tagsc.traffic_analytics_whatsapp_leads_id, LAST_VALUE(tagsc.user_status) OVER(PARTITION BY tagsc.traffic_analytics_whatsapp_leads_id ORDER BY tagsc.contact_date) AS last_user_status, LAST_VALUE(tagsc.contact_date) OVER(PARTITION BY tagsc.traffic_analytics_whatsapp_leads_id ORDER BY tagsc.contact_date) AS last_contact_date FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` AS tagsc) AS last_crm_status ON tawl.id = last_crm_status.traffic_analytics_whatsapp_leads_id ORDER BY days_since_last_contact DESC;")
    lead_ids = []
    lead_phone_numbers = []
    for row in rows:
        lead_ids.append(row.get('id'))
        lead_phone_numbers.append(row.get('full_phone_number'))
    selected_phone = st.selectbox(
            label = "Select the user phone number",
            options = lead_phone_numbers,
            index = None,
            key= "lead_phone_numbers"
        )
    checking_phone_query = uc.run_query_30_m(f"SELECT awl.id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS awl WHERE CONCAT(awl.phone_indicator,awl.phone_number) LIKE '{selected_phone}';")
    if len(checking_phone_query) < 1 or checking_phone_query is None:
        st.error('Phone number does not exists, be sure this user was created as a Whatsapp lead', icon = '👻')
    else:
        st.success('Phone number available', icon = '🪬')
        if selected_phone is not None:
            selected_phone_id = lead_ids[lead_phone_numbers.index(selected_phone)]
            
            user_history = uc.run_query_instant(f"SELECT contact_date, user_status, contact_description FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` WHERE traffic_analytics_whatsapp_leads_id = '{selected_phone_id}' ORDER BY contact_date ASC;")
            st.table(user_history)
            
            contact_date = st.date_input("Contact date:", key = 'contact_date')
            user_status = st.selectbox(
                label = "Select the user status",
                options = ['active', 'active_15_days', 'active_30_days', 'active_60_days', 'lost', 'discarted'],
                index = None,
                key= "user_status",
                placeholder = "active",
                help = "active = active oportunity, active_x_days = active oportunity, but wait x days to next contact, lost = the user reject the process, discarted = the user does not meet the requirements such as nurses from cuba or auxiliaries"
            )
            contact_description = st.text_input("Contact description", placeholder = "Se contacta invitando a asistir a la sesion grupal")
            add_contact_button = st.button("Add CRM contact", on_click = add_new_crm_groupal_session_contact_execution, args = [user_id, project_name, selected_phone_id, contact_date, user_status, contact_description])






def groupal_session_team_member_performance(user_id, project_name):
    team_member_contacts = uc.run_query_half_day(f"SELECT tagsc.contact_date, EXTRACT(YEAR FROM tagsc.contact_date) AS year_contact, EXTRACT(MONTH FROM tagsc.contact_date) AS month_contact, EXTRACT(WEEK FROM tagsc.contact_date) AS week_contact, tagsc.user_status FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` AS tagsc WHERE tagsc.creator_id = {user_id} AND EXTRACT(YEAR FROM tagsc.contact_date) = EXTRACT(YEAR FROM CURRENT_DATE());")
    team_member_contacts_df = pd.DataFrame(team_member_contacts, columns = ["contact_date","year_contact","month_contact","week_contact","user_status"])
    team_member_user_assistance = uc.run_query_half_day(f"SELECT meeting_date, EXTRACT(YEAR FROM meeting_date) AS year_meeting_date, EXTRACT(MONTH FROM meeting_date) AS month_meeting_date, EXTRACT(WEEK FROM meeting_date) AS week_meeting_date, status FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_assistance` WHERE creator_user_id = {user_id};")
    team_member_user_assistance_df = pd.DataFrame(team_member_user_assistance, columns = ["meeting_date","year_meeting_date","month_meeting_date","week_meeting_date","status"])
    today = datetime.date.today()

    st.header("Your last 10 contacts")
    team_member_last_contacts = uc.run_query_instant(f"SELECT CONCAT(w.phone_indicator, w.phone_number) AS full_phone_number,tagsc.contact_date, tagsc.contact_description, tagsc.user_status FROM `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` AS tagsc INNER JOIN `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS w ON w.id = tagsc.traffic_analytics_whatsapp_leads_id WHERE tagsc.creator_id = {user_id} ORDER BY tagsc.contact_date DESC LIMIT 10;")
    st.table(team_member_last_contacts)
    
    st.header("Week evolution")
    corrected_week = (today.isocalendar()[1] + 1 if today.isocalendar()[2] == 7 else today.isocalendar()[1]) - 1
    col1, col2, col3, col4 = st.columns(4)
    team_member_contacts_week = team_member_contacts_df[(team_member_contacts_df["year_contact"] == today.year) & (team_member_contacts_df["month_contact"] == today.month) & (team_member_contacts_df["week_contact"] == corrected_week)]
    team_member_user_assistance_week = team_member_user_assistance_df[(team_member_user_assistance_df["year_meeting_date"] == today.year) & (team_member_user_assistance_df["month_meeting_date"] == today.month) & (team_member_user_assistance_df["week_meeting_date"] == corrected_week)]
    if len(team_member_contacts_week) < 1 or team_member_contacts_week is None:
            st.warning(f"You have not added new contacts", icon = "🫥")
    else:
        col1.metric(label="# Week Contacts", value = team_member_contacts_week.shape[0])
        col2.metric(label="# Week Active contacts", value = team_member_contacts_week[team_member_contacts_week['user_status'].str.contains('active')].shape[0])
        col3.metric(label="# Week Discarted contacts", value = team_member_contacts_week[team_member_contacts_week['user_status'] == 'discarted'].shape[0])
        col1.metric(label="# Week Lost contacts", value = team_member_contacts_week[team_member_contacts_week['user_status'] == 'lost'].shape[0])
        col2.metric(label="# Week Assistants added", value = team_member_user_assistance_week[team_member_user_assistance_week['status'] == 'assistant'].shape[0])
        col3.metric(label="# Week Absents added", value = team_member_user_assistance_week[team_member_user_assistance_week['status'] == 'absent'].shape[0])

    st.header("Month evolution")
    col1, col2, col3, col4 = st.columns(4)
    team_member_contacts_month = team_member_contacts_df[(team_member_contacts_df["year_contact"] == today.year) & (team_member_contacts_df["month_contact"] == today.month)]
    team_member_user_assistance_month = team_member_user_assistance_df[(team_member_user_assistance_df["year_meeting_date"] == today.year) & (team_member_user_assistance_df["month_meeting_date"] == today.month)]
    if len(team_member_contacts_month) < 1 or team_member_contacts_month is None:
            st.warning(f"You have not added new contacts", icon = "🫥")
    else:
        col1.metric(label="# Month Contacts", value = team_member_contacts_month.shape[0])
        col2.metric(label="# Month Active contacts", value = team_member_contacts_month[team_member_contacts_month['user_status'].str.contains('active')].shape[0])
        col3.metric(label="# Month Discarted contacts", value = team_member_contacts_month[team_member_contacts_month['user_status'] == 'discarted'].shape[0])
        col1.metric(label="# Month Lost contacts", value = team_member_contacts_month[team_member_contacts_month['user_status'] == 'lost'].shape[0])
        col2.metric(label="# Month Assistants added", value = team_member_user_assistance_month[team_member_user_assistance_month['status'] == 'assistant'].shape[0])
        col3.metric(label="# Month Absents added", value = team_member_user_assistance_month[team_member_user_assistance_month['status'] == 'absent'].shape[0])

    st.header("Year evolution")
    col1, col2, col3, col4 = st.columns(4)
    team_member_contacts_year = team_member_contacts_df[(team_member_contacts_df["year_contact"] == today.year)]
    team_member_user_assistance_year = team_member_user_assistance_df[(team_member_user_assistance_df["year_meeting_date"] == today.year)]
    if len(team_member_contacts_year) < 1 or team_member_contacts_year is None:
            st.warning(f"You have not added new contacts", icon = "🫥")
    else:
        col1.metric(label="# Year Contacts", value = team_member_contacts_year.shape[0])
        col2.metric(label="# Year Active contacts", value = team_member_contacts_year[team_member_contacts_year['user_status'].str.contains('active')].shape[0])
        col3.metric(label="# Year Discarted contacts", value = team_member_contacts_year[team_member_contacts_year['user_status'] == 'discarted'].shape[0])
        col1.metric(label="# Year Lost contacts", value = team_member_contacts_year[team_member_contacts_year['user_status'] == 'lost'].shape[0])
        col2.metric(label="# Year Assistants added", value = team_member_user_assistance_year[team_member_user_assistance_year['status'] == 'assistant'].shape[0])
        col3.metric(label="# Year Absents added", value = team_member_user_assistance_year[team_member_user_assistance_year['status'] == 'absent'].shape[0])
        
        
    





def groupal_session_contact_text(project_id):
    if project_id == 1:
        st.write("---")
        st.write("**Texto para ausentes de la reunion grupal**")
        text_wsp = '''
        ¡Hola! Buenos días.
        Este miércoles voy a hacer otra sesión para explicar el proceso de homologación de enfermería en Estados Unidos. Si quieres asistir, puedes reservar tu espacio desde acá: https://bit.ly/3vtB3Wi
        También, si quieres, te enviaré el enlace de la reunión ese día antes de iniciar.
        Me cuentas cualquier cosa. ¡Feliz día!
        '''
        st.markdown(text_wsp)

        st.write("---")
        st.write("**Texto un dia antes de la reunion grupal**")
        text_wsp = '''
        ¡Hola! ¿Cómo estás?
        Quiero contarte que realizaremos otra sesión grupal gratuita donde explicaré detalladamente el proceso de *homologación de enfermería en Estados Unidos*. Esta es una oportunidad para obtener toda la información que necesitas. La sesión se realizará este miércoles 31 de enero a las 6 pm, hora Georgia EEUU. 
        Si deseas participar, puedes reservar tu cupo a través del siguiente link: https://bit.ly/3vtB3Wi
        Esperamos tu asistencia.
        '''
        st.markdown(text_wsp)

        st.write("---")
        st.write("**Texto 15 minutos antes de la sesion grupal**")
        text_wsp = '''
        Hola! Sabemos que tienes interés en conocer el proceso de *homologación de enfermería en Estados Unidos*. Estamos a unos minutos de iniciar la sesión donde resolveremos algunas dudas sobre este proceso.
        Puedes unirte en el siguiente enlace: https://calendly.com/events/524e01bd-76b1-45b5-9052-2058628e6893/google_meet
        ¡Nos vemos en un momento!
        '''
        st.markdown(text_wsp)


        st.write("---")
        st.write("**Texto Al finalizar la sesion**")
        text_wsp = '''
        Hola! te dejo el enlace del programa para que lo puedas revisar: https://enfermeraenestadosunidos.com/validar-enfermeria-en-usa/
        También, si quieres, te llamo en un momento y hablamos de tu caso en particular.
        '''
        st.markdown(text_wsp)
        st.write("**Antes de iniciar la sesion descargar el Excel de registrados y agregar las columnas, Asistio,	Agregado como asistente en plataforma,	Agregado como ausente en plataforma,	Entregado link de producto,	etiquetado como groupal session,	llamado,	agregado en CRM de CONTRATOS. AL dia siguiente dejar la tabla totalmente diligenciada**")
        
    
