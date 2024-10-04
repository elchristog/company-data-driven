import pandas as pd
import numpy as np
import streamlit as st
import os
import time


import utils.user_credentials as uc

@st.fragment
def pagos():
    os.write(1, '🥏 Executing pagos \n'.encode('utf-8'))
    
    pagos_data = uc.run_query_instant(f'''
    WITH salaries AS (
    SELECT u.id, u.name, u.lastname, es.salarie_value FROM `company-data-driven.global.users` AS u INNER JOIN `company-data-driven.global.role_assignment` AS ra ON u.id = ra.user_id LEFT JOIN `enfermera_en_estados_unidos.employee_salaries` AS es ON u.id = es.employee_user_id WHERE ra.role_id != 6 AND u.status = 'active'
    ),
    video_creation AS (
      SELECT video_creator_user_id, COUNT(*) AS num_created_videos, 30 * COUNT(*) AS video_creation_earnings  FROM `company-data-driven.enfermera_en_estados_unidos.content_creation` WHERE EXTRACT(YEAR FROM created_video_date) = EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM created_video_date) = EXTRACT(MONTH FROM CURRENT_DATE()) GROUP BY video_creator_user_id
    ),
    video_edition AS (
      SELECT video_editor_user_id, COUNT(*) AS num_edited_videos, 30 * COUNT(*) AS video_edition_earnings  FROM `company-data-driven.enfermera_en_estados_unidos.content_creation` WHERE EXTRACT(YEAR FROM edited_date) = EXTRACT(YEAR FROM CURRENT_DATE()) AND EXTRACT(MONTH FROM edited_date) = EXTRACT(MONTH FROM CURRENT_DATE()) GROUP BY video_editor_user_id
    ),
    sales_bonus AS (
      SELECT 19 AS id, 
            COUNT(*) AS num_new_contracts, 
            (FLOOR(COUNT(*) / 5) * 200) + (FLOOR(COUNT(*) / 5) * (FLOOR(COUNT(*) / 5) - 1) * 100) AS sales_bonus
      FROM (
          SELECT contract_id, MIN(payment_date) AS first_payment_date 
          FROM `company-data-driven.enfermera_en_estados_unidos.contracts_payments` AS cp 
          GROUP BY contract_id 
          HAVING EXTRACT(YEAR FROM first_payment_date) = EXTRACT(YEAR FROM CURRENT_DATE()) 
            AND EXTRACT(MONTH FROM first_payment_date) = EXTRACT(MONTH FROM CURRENT_DATE())
      )
    )
    SELECT salaries.id, salaries.name, salaries.lastname, COALESCE(salaries.salarie_value, 0) + COALESCE(video_creation.video_creation_earnings, 0) + COALESCE(video_edition.video_edition_earnings, 0) + COALESCE(sales_bonus.sales_bonus, 0) AS total_to_pay, salaries.salarie_value, video_creation.num_created_videos,  video_creation.video_creation_earnings, video_edition.num_edited_videos, video_edition.video_edition_earnings, sales_bonus.num_new_contracts, sales_bonus.sales_bonus FROM salaries LEFT JOIN video_creation ON salaries.id = video_creation.video_creator_user_id LEFT JOIN video_edition ON salaries.id = video_edition.video_editor_user_id LEFT JOIN sales_bonus ON salaries.id = sales_bonus.id;
    ''')

    st.table(pagos_data)





@st.fragment
def estado_de_resultados():
    os.write(1, '🥏 Executing estado_de_resultados \n'.encode('utf-8'))
    
    estado_de_resultados_data = uc.run_query_instant(f'''
    WITH earnings AS(
      SELECT EXTRACT(YEAR FROM cp.payment_date) AS year, EXTRACT(MONTH FROM cp.payment_date) AS month, SUM(CAST(payment_value AS NUMERIC)) AS earnings
      FROM  `company-data-driven.enfermera_en_estados_unidos.contracts_payments`  AS cp GROUP BY EXTRACT(YEAR FROM cp.payment_date), EXTRACT(MONTH FROM cp.payment_date)
      ),
    expenses AS(
      SELECT year, month, SUM(salarie_value) AS salaries, SUM(video_creation_earnings) AS video_creation_payments, SUM(video_edition_earnings) AS video_edition_payments, SUM(num_new_contracts) AS num_contracts, 300 * SUM(num_new_contracts) AS babbel_archer, SUM(sales_bonus) AS sales_comissions FROM `company-data-driven.enfermera_en_estados_unidos.employee_payments` GROUP BY year, month
    )
      SELECT e.year, e.month, ex.num_contracts AS num_contratos_nuevos, e.earnings AS ingresos_por_ventas, ex.sales_comissions AS descuentos_y_bonificaciones, e.earnings - ex.sales_comissions  AS ingresos_operativos_netos, ex.salaries + ex.babbel_archer AS costo_de_servicios_prestados, e.earnings - ex.sales_comissions - ex.salaries - ex.babbel_archer AS resultado_bruto, ex.video_creation_payments + ex.video_edition_payments AS publicidad_seo, 300 AS publicidad_sem, e.earnings - ex.sales_comissions - ex.salaries - ex.babbel_archer - ex.video_creation_payments - ex.video_edition_payments - 300 AS resultados_de_las_operaciones_ordinarias, (e.earnings - ex.sales_comissions - ex.salaries - ex.babbel_archer)/e.earnings AS rentabilidad_bruta FROM earnings AS e RIGHT JOIN expenses AS ex ON e.year = ex.year AND e.month = ex.month ORDER BY e.year, e.month;
    ''')

    st.table(estado_de_resultados_data)
