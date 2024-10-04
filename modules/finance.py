import pandas as pd
import numpy as np
import streamlit as st
import os
import time


import utils.user_credentials as uc

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

    st.write(estado_de_resultados_data)
