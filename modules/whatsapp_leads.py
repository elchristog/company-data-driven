import streamlit as st
import time
import datetime
import numpy as np
import pandas as pd
import re
import os


from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc




def plot_echarts_wsp(df_grouped):
    df_grouped['conversion'] = df_grouped['conversion'].apply(lambda conversion: f"{conversion:.2f}")
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
                "conversion": True,        
                "bitly_clicks_total": False,    
                "num_leads_wsp": False,
                "bitly_clicks_web": False,
                "bitly_clicks_yt": False 
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "conversion",
                "data": df_grouped['conversion'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "bitly_clicks_total",
                "data": df_grouped["bitly_clicks_total"].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "num_leads_wsp",
                "data": df_grouped['num_leads_wsp'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BF3F34"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "bitly_clicks_web",
                "data": df_grouped['bitly_clicks_web'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BFB5B4"},
                "showSymbol": False,
            },
            {
                "type": "line",
                "name": "bitly_clicks_yt",
                "data": df_grouped['bitly_clicks_yt'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#84C2BD"},
                "showSymbol": False,
            }
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  
        ],
        "backgroundColor": "#ffffff",
        "color": ["#A6785D", "#394A59", "#BF3F34", "#BFB5B4", "#84C2BD"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')




def whatsapp_leads_show_metrics(project_name, bitly_web_link, bitly_yt_link):
  dates_bitly = uc.run_query_1_h(f"SELECT MIN(date) AS min_date_bitly, MAX(date) AS max_date_bitly FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks`;")
  dates_whatsapp_leads = uc.run_query_1_h(f"SELECT MIN(creation_date) AS min_date_wsp, MAX(creation_date) AS max_date_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
  if len(dates_bitly) < 1 or len(dates_whatsapp_leads) < 1:
      st.warning("Waiting for data")
  else:
      day = st.date_input(
          "Time Range:",
          (np.maximum(dates_bitly[0].get('min_date_bitly'), dates_whatsapp_leads[0].get('min_date_wsp')), np.minimum(dates_bitly[0].get('max_date_bitly'), dates_whatsapp_leads[0].get('max_date_wsp'))),
          min_value=np.maximum(dates_bitly[0].get('min_date_bitly'), dates_whatsapp_leads[0].get('min_date_wsp')),
          max_value=np.minimum(dates_bitly[0].get('max_date_bitly'), dates_whatsapp_leads[0].get('max_date_wsp')),
          format="DD/MM/YYYY",
          help='',
          key = 'day_web'
      )

      df_conversion = pd.DataFrame(uc.run_query_1_h(f"SELECT btl_totals.date, btl_totals.bitly_clicks_web, btl_totals.bitly_clicks_yt, btl_totals.bitly_clicks_total, wsp_leads.num_leads_wsp, ROUND(wsp_leads.num_leads_wsp/NULLIF(btl_totals.bitly_clicks_total, 0), 2) AS conversion  FROM (SELECT date, SUM(CASE WHEN bitly_link IN ('{bitly_web_link}') THEN clicks ELSE 0 END) AS bitly_clicks_web, SUM(CASE WHEN bitly_link IN ('{bitly_yt_link}') THEN clicks ELSE 0 END) AS bitly_clicks_yt, SUM(CASE WHEN bitly_link IN ('{bitly_web_link}', '{bitly_yt_link}') THEN clicks ELSE 0 END) AS bitly_clicks_total FROM `company-data-driven.{project_name}.traffic_analytics_bitly_clicks` GROUP BY date) AS btl_totals INNER JOIN (SELECT creation_date, COUNT(id) AS num_leads_wsp FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE creation_date >= '{day[0].strftime('%Y-%m-%d')}'  AND  creation_date <= '{day[1].strftime('%Y-%m-%d')}'  GROUP BY creation_date) AS wsp_leads ON wsp_leads.creation_date = btl_totals.date ORDER BY btl_totals.date ASC;"))
    
      bitly_clicks_total = df_conversion['bitly_clicks_total'].sum()
      num_leads_wsp = df_conversion['num_leads_wsp'].sum()
      conversion = num_leads_wsp/bitly_clicks_total
      bitly_clicks_web = df_conversion['bitly_clicks_web'].sum()
      bitly_clicks_yt = df_conversion['bitly_clicks_yt'].sum()
    
      met1, met2, met3 = st.columns(3)
      with met1:
          st.metric('bitly_clicks_total:', f'{bitly_clicks_total:,}')
      with met2:
          st.metric('num_leads_wsp:', f'{num_leads_wsp:,}')
      with met3:
          st.metric('conversion:', f'{conversion * 100:.2f}%')
      with st.container():
          plot_echarts_wsp(df_conversion)
      with met1:
          st.metric('bitly_clicks_web:', f'{bitly_clicks_web:,}')
      with met2:
          st.metric('bitly_clicks_yt:', f'{bitly_clicks_yt:,}')






def whatsapp_leads_creation_save(project_name, user_id):
    st.session_state.text_input_1 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_1)
    st.session_state.text_input_2 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_2)
    st.session_state.text_input_3 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_3)

    st.session_state.text_input_1 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_1)
    st.session_state.text_input_2 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_2)
    st.session_state.text_input_3 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_3)

    if st.session_state.text_input_2 is not None and st.session_state.text_input_3 is not None:
            if st.session_state.text_input_2 == st.session_state.text_input_3:
                st.toast("Phone number match!", icon = "🫡")
                verify_phone_created = uc.run_query_instant(f"SELECT * FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` WHERE phone_indicator = '{st.session_state.text_input_1}' AND phone_number = '{st.session_state.text_input_2}';")
                if len(verify_phone_created) > 0:
                    st.toast("Phone already exists in DB", icon = "🥴")
                else:
                    st.toast("Please wait", icon = "☺️")
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` (id, creation_date, phone_indicator, phone_number, creator_user_id) VALUES (GENERATE_UUID(), '{st.session_state.lead_date_input}', '{st.session_state.text_input_1}', '{st.session_state.text_input_2}', {user_id});")
                    selected_phone = st.session_state.text_input_1 + st.session_state.text_input_2
                    time.sleep(2)
                    phone_associated_id = uc.run_query_instant(f"SELECT awl.id FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads` AS awl WHERE CONCAT(awl.phone_indicator,awl.phone_number) LIKE '{selected_phone}';")[0].get("id")
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_groupal_session_crm` (id, contact_date, traffic_analytics_whatsapp_leads_id, creator_id, user_status, contact_description) VALUES (GENERATE_UUID(), '{st.session_state.lead_date_input}', '{phone_associated_id}', {user_id}, 'active', 'Se crea el lead en whatsapp y se entrega enlace de sesion grupal');")
                    st.toast("Lead saved!", icon = "👾")
                    st.balloons()
                    time.sleep(5)
                    uc.run_query_1_h.clear()
                    uc.run_query_half_day.clear()
            else:
                st.toast("The phone number does not match", icon = "🥴")

    


def whatsapp_leads_creation(user_id, project_name):
    st.warning("Do not use line breaks, symbols, double or single quotes", icon = "🙈")
    with st.form("whatsapp_leads_creation_form", clear_on_submit = True):
        text_input_1 = st.text_input(
            "Phone indicator",
            label_visibility = 'visible',
            disabled = False,
            placeholder = '1',
            help = 'Just the number of the country, no symbols',
            key = 'text_input_1'
        )

        text_input_2 = st.text_input(
            "Phone number",
            label_visibility = 'visible',
            disabled = False,
            placeholder = '8136783561',
            help = 'Just the phone number, no symbols or spaces',
            key = 'text_input_2'
        )

        text_input_3 = st.text_input(
            "Confirm Phone number",
            label_visibility = 'visible',
            disabled = False,
            placeholder = '8136783561',
            help = 'Just the phone number, no symbols or spaces',
            key = 'text_input_3'
        )
        lead_date_input = st.date_input("Lead date:", key = 'lead_date_input')

        submitted = st.form_submit_button("Submit", on_click = whatsapp_leads_creation_save, args = [project_name, user_id])









def fix_phone_number_execution():
    os.write(1, '🥏 Executing fix_phone_number_execution \n'.encode('utf-8'))
    if 'fix_phone_number_phone_number_confirmation' in st.session_state:
        os.write(1, '- fix_phone_number_execution: Updating phone number\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.fix_phone_number_project_name}.traffic_analytics_whatsapp_leads` SET phone_indicator = '{st.session_state.fix_phone_number_phone_indicator}', phone_number = '{st.session_state.fix_phone_number_phone_number}' WHERE id = '{st.session_state.fix_phone_number_selected_phone_number_id}';")
        st.toast("Info saved!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.fix_phone_number_selected_phone_number
        del st.session_state.fix_phone_number_user_id
        del st.session_state.fix_phone_number_project_name
        del st.session_state.fix_phone_number_selected_phone_number_id
        del st.session_state.fix_phone_number_phone_indicator
        del st.session_state.fix_phone_number_phone_number 
        del st.session_state.fix_phone_number_phone_number_confirmation 
        

def fix_phone_number(user_id, project_name):
    os.write(1, '🥏 Executing fix_phone_number \n'.encode('utf-8'))
    os.write(1, '- fix_phone_number: Showing form \n'.encode('utf-8'))
    
    os.write(1, '- fix_phone_number: Listing phones \n'.encode('utf-8'))
    rows = uc.run_query_instant(f"SELECT id, CONCAT(phone_indicator,phone_number) AS full_phone_number FROM `company-data-driven.{project_name}.traffic_analytics_whatsapp_leads`;")
    ids = []
    full_phone_numbers = []
    for row in rows:
        ids.append(row.get('id'))
        full_phone_numbers.append(row.get('full_phone_number'))
    selected_phone_number = st.selectbox(
            label = "Select the phone number to fix",
            options = full_phone_numbers,
            index = None,
            key= "fix_phone_number_selected_phone_number"
        )

    if selected_phone_number is not None:
        st.session_state.fix_phone_number_user_id = user_id
        st.session_state.fix_phone_number_project_name = project_name
        st.session_state.fix_phone_number_selected_phone_number_id = ids[full_phone_numbers.index(selected_phone_number)]
        st.text_input('New Phone Indicator', placeholder = '51', key = 'fix_phone_number_phone_indicator', help = 'No spaces or symbols')
        st.text_input('New Phone Number', placeholder = '3138533246', key = 'fix_phone_number_phone_number', help = 'No spaces or symbols')
        st.checkbox("The new phone number is right", key="fix_phone_number_phone_number_confirmation")
        fix_phone_number_button = st.button("Update phone number", on_click = fix_phone_number_execution)
        





def wsp_answer_text(project_id):
    if project_id == 1:
        st.write('---')
        st.write('**Respuesta para el usuario que escribe por primera vez**')
        
        text_answer = '''
        
        Hola buen dia, gracias por comunicarte.

        Con quien tengo el gusto

        XX Un gusto saludarte!

        (Si dice que ya esta en USA): Cuentas con nacionalidad o residencia en Estados Unidos?

        Ya cuentas con tu titulo profesional en enfermeria? (Si es profesional enviarle la invitacion, si es auxiliar no)

        Vale, justo (Hoy, el proximo miercoles...) tendremos una sesion informativa donde explicare como realizar el proceso de homologacion de enfermeria en Estados Unidos, los pasos y los costos.

        Desas que te comparta el link de inscripcion?

        Vale, puedes registrarte en este enlace: https://bit.ly/3vtB3Wi

        En el momento en que te inscribas te llegara un correo electronico con el enlace a la reunion en Google Meet.

        Gracias!
        '''
        st.markdown(text_answer)
        st.write('**Recordar crear el lead en la plataforma, etiquetar el lead en Whatsapp, guardar el contacto con el nombre de la persona**')

        st.write("---")
        st.write('**Respuesta para auxiliares de enfermeria**')
        
        text_answer = '''
        
        Hola [Nombre], mucho gusto!
        
        Cuéntame, ¿ya has podido avanzar algo en el proceso de homologación de tu título?
        
        Entiendo
        
        Disculpame, lamentablemente no estamos asesorando a auxiliares de enfermería, ya que las regulaciones y el proceso difieren mucho de los enfermeros profesionales.
        '''
        st.markdown(text_answer)


        st.write("---")
        st.write('**Respuesta para Cubanos**')
        
        text_answer = '''
        
        Hola [Nombre], mucho gusto!
        
        Cuéntame, ¿ya has podido avanzar algo en el proceso de homologación de tu título?
        
        Entiendo
        
        Disculpame, lamentablemente no estamos asesorando a enfermeros de Cuba, ya que las regulaciones y el proceso difieren mucho.
        '''
        st.markdown(text_answer)
        
