import pandas as pd
import numpy as np
import streamlit as st
import os
import time


import utils.user_credentials as uc

@st.fragment
def pagos(project_name):
    os.write(1, '🥏 Executing pagos \n'.encode('utf-8'))
    
    pagos_data = uc.run_query_instant(f'''
    WITH salaries AS (
    SELECT u.id, u.name, u.lastname, es.salarie_value FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id LEFT JOIN `{project_name}.employee_salaries` AS es ON u.id = es.employee_user_id WHERE ra.role_id != 6 AND u.status = 'active'
    ),
    video_creation AS (
      SELECT video_creator_user_id, COUNT(*) AS num_created_videos, 30 * COUNT(*) AS video_creation_earnings  FROM `company-data-driven.{project_name}.content_creation` WHERE EXTRACT(YEAR FROM created_video_date) = EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM created_video_date) = EXTRACT(MONTH FROM CURRENT_DATE()) GROUP BY video_creator_user_id
    ),
    video_edition AS (
      SELECT video_editor_user_id, COUNT(*) AS num_edited_videos, 30 * COUNT(*) AS video_edition_earnings  FROM `company-data-driven.{project_name}.content_creation` WHERE EXTRACT(YEAR FROM edited_date) = EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM edited_date) = EXTRACT(MONTH FROM CURRENT_DATE()) GROUP BY video_editor_user_id
    ),
    sales_bonus AS (
      SELECT 19 AS id, 
            COUNT(*) AS num_new_contracts, 
            (FLOOR(COUNT(*) / 5) * 200) + (FLOOR(COUNT(*) / 5) * (FLOOR(COUNT(*) / 5) - 1) * 100) AS sales_bonus
      FROM (
          SELECT contract_id, MIN(payment_date) AS first_payment_date 
          FROM `company-data-driven.{project_name}.contracts_payments` AS cp 
          GROUP BY contract_id 
          HAVING EXTRACT(YEAR FROM first_payment_date) = EXTRACT(YEAR FROM CURRENT_DATE()) 
            AND EXTRACT(MONTH FROM first_payment_date) = EXTRACT(MONTH FROM CURRENT_DATE())
      )
    )
    SELECT salaries.id, salaries.name, salaries.lastname, COALESCE(salaries.salarie_value, 0) + COALESCE(video_creation.video_creation_earnings, 0) + COALESCE(video_edition.video_edition_earnings, 0) + COALESCE(sales_bonus.sales_bonus, 0) AS total_to_pay, salaries.salarie_value, video_creation.num_created_videos,  video_creation.video_creation_earnings, video_edition.num_edited_videos, video_edition.video_edition_earnings, sales_bonus.num_new_contracts, sales_bonus.sales_bonus FROM salaries LEFT JOIN video_creation ON salaries.id = video_creation.video_creator_user_id LEFT JOIN video_edition ON salaries.id = video_edition.video_editor_user_id LEFT JOIN sales_bonus ON salaries.id = sales_bonus.id;
    ''')

    st.table(pagos_data)




@st.fragment
def create_employee_payment_execution():
    os.write(1, '🥏 Executing create_employee_payment_execution \n'.encode('utf-8'))
    if 'posting_posts_selected_idea' in st.session_state:
        os.write(1, '- posting_posts_execution: Saving posted idea\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.posting_posts_project_name}.daily_post_creation` SET posted = 1, posted_date = CURRENT_DATE(), poster_user_id = {st.session_state.posting_posts_user_id} WHERE id = '{st.session_state.posting_posts_selected_idea_id}'")
        st.toast("Info saved!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.posting_posts_user_id
        del st.session_state.posting_posts_project_name
        del st.session_state.posting_posts_post_idea
        del st.session_state.posting_posts_selected_idea_id 


@st.fragment
def create_employee_payment(user_id, project_name, project_id):
    
    os.write(1, '🥏 Executing create_employee_payment \n'.encode('utf-8'))
    
    os.write(1, '- create_employee_payment: Showing form \n'.encode('utf-8'))
    
    completed_payments = uc.run_query_instant(f"SELECT user_id AS employee_id, CONCAT(u.name, '_', u.lastname) AS employee_name, payment_creation_user_id, salarie_value + video_creation_earnings + video_edition_earnings + sales_bonus AS total_paid FROM `company-data-driven.enfermera_en_estados_unidos.employee_payments` AS ep INNER JOIN `global.users` AS u ON ep.user_id = u.id WHERE year = EXTRACT(YEAR FROM CURRENT_DATE()) AND month = EXTRACT(MONTH FROM CURRENT_DATE());")
    
    if len(completed_payments) < 1:
        
        st.info(f"No completed payments", icon = "😇")
        
    else:

        st.write('### Payments already made')
        
        st.table(completed_payments)

    os.write(1, '- create_employee_payment: Listing employees \n'.encode('utf-8'))
    
    rows = uc.run_query_instant(f"SELECT u.id, CONCAT(u.name, '_', u.lastname) AS employee_name FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id WHERE project_id = {project_id} AND ra.role_id <> 6 ORDER BY u.id;")
    
    ids = []
    names = []
    
    for row in rows:
        
        ids.append(row.get('id'))
        
        names.append(row.get('employee_name'))
        
    selected_employee = st.selectbox(
            label = "Select the employee",
            options = names,
            index = None,
            key= "create_employee_payment_selected_employee_name"
        )

    if selected_employee is not None:
        
        st.session_state.create_employee_payment_user_id = user_id
        
        st.session_state.create_employee_payment_project_name = project_name
        
        st.session_state.create_employee_payment_selected_employee_id = ids[names.index(selected_employee)]

        st.session_state.create_employee_payment_base_salarie_value = st.number_input(
            "Base Salarie Value", value=None, placeholder="Type a number..."
        )

        st.session_state.create_employee_payment_num_created_videos = st.number_input(
            "Num Created Videos", value=None, placeholder="Type a number..."
        )

        st.session_state.create_employee_payment_video_creation_earnings = st.number_input(
            "Video Creation Payment Value", value=None, placeholder="Type a number..."
        )

        st.session_state.create_employee_payment_num_edited_videos = st.number_input(
            "Num Edited Videos", value=None, placeholder="Type a number..."
        )

        st.session_state.create_employee_payment_video_edition_earnings = st.number_input(
            "Video Edition Payment Value", value=None, placeholder="Type a number..."
        )

        if st.session_state.create_employee_payment_selected_employee_id = 19: # Comision solo a bingley
            
            st.session_state.create_employee_payment_num_new_contracts = st.number_input(
                "Num New Contracts", value=None, placeholder="Type a number..."
            )

            st.session_state.create_employee_payment_sales_bonus = st.number_input(
                "Sales Bonus Value", value=None, placeholder="Type a number..."
            )

        else:
            st.session_state.create_employee_payment_num_new_contracts = 0
            
            st.session_state.create_employee_payment_sales_bonus = 0
            
        create_employee_payment_button = st.button("Add payment", on_click = create_employee_payment_execution)



@st.fragment
def estado_de_resultados(project_name):
    os.write(1, '🥏 Executing estado_de_resultados \n'.encode('utf-8'))
    
    estado_de_resultados_data = uc.run_query_instant(f'''
    WITH earnings AS(
      SELECT EXTRACT(YEAR FROM cp.payment_date) AS year, EXTRACT(MONTH FROM cp.payment_date) AS month, SUM(CAST(payment_value AS NUMERIC)) AS earnings
      FROM  `company-data-driven.{project_name}.contracts_payments`  AS cp GROUP BY EXTRACT(YEAR FROM cp.payment_date), EXTRACT(MONTH FROM cp.payment_date)
      ),
    expenses AS(
      SELECT year, month, SUM(salarie_value) AS salaries, SUM(video_creation_earnings) AS video_creation_payments, SUM(video_edition_earnings) AS video_edition_payments, SUM(num_new_contracts) AS num_contracts, 300 * SUM(num_new_contracts) AS babbel_archer, SUM(sales_bonus) AS sales_comissions FROM `company-data-driven.enfermera_en_estados_unidos.employee_payments` GROUP BY year, month
    )
      SELECT e.year, e.month, ex.num_contracts AS num_contratos_nuevos, e.earnings AS ingresos_por_ventas, ex.sales_comissions AS descuentos_y_bonificaciones, e.earnings - ex.sales_comissions  AS ingresos_operativos_netos, ex.salaries + ex.babbel_archer AS costo_de_servicios_prestados, e.earnings - ex.sales_comissions - ex.salaries - ex.babbel_archer AS resultado_bruto, ex.video_creation_payments + ex.video_edition_payments AS publicidad_seo, 300 AS publicidad_sem, e.earnings - ex.sales_comissions - ex.salaries - ex.babbel_archer - ex.video_creation_payments - ex.video_edition_payments - 300 AS resultados_de_las_operaciones_ordinarias, (e.earnings - ex.sales_comissions - ex.salaries - ex.babbel_archer)/e.earnings AS rentabilidad_bruta FROM earnings AS e FULL OUTER JOIN expenses AS ex ON e.year = ex.year AND e.month = ex.month ORDER BY e.year, e.month;
    ''')

    st.table(estado_de_resultados_data)
