import streamlit as st
import datetime

import utils.user_credentials as uc


def general_progress(user_id, project_name, program_steps_table_tame, program_steps_user_progress_table_name):
    st.header('Program progress and steps')
    user_progress_table = uc.run_query_3_h(f"SELECT ps.id, ps.name, ps.description, COALESCE(CAST(upsp_user.creation_date AS STRING),'pending') AS starting_date FROM `company-data-driven.{project_name}.{program_steps_table_tame}` AS ps LEFT JOIN (SELECT  * FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id}) AS upsp_user ON ps.id = upsp_user.program_step_id  ORDER BY ps.id;")
    user_actual_step= uc.run_query_3_h(f"SELECT MAX(program_step_id) AS actual_step FROM `company-data-driven.{project_name}.{program_steps_user_progress_table_name}` AS upsp WHERE upsp.user_id = {user_id};")
    st.progress(5, text = f"Global progress: **{5}%**")
    st.table(user_progress_table)
    st.write(user_actual_step)
    