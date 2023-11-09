import streamlit as st
import datetime

import utils.user_credentials as uc


def general_progress(user_id, project_name):
    st.header('Program progress and steps')
    user_progress_table = uc.run_query_3_h(f"SELECT ps.name, ps.description, COALESCE(CAST(upsp_user.creation_date AS STRING),'pending') AS starting_date FROM `company-data-driven.{project_name}.program_steps` AS ps LEFT JOIN (SELECT  * FROM `company-data-driven.{project_name}.user_program_steps_progress` AS upsp WHERE upsp.user_id = {user_id}) AS upsp_user ON ps.id = upsp_user.program_step_id  ORDER BY ps.id;")
    st.progress(5, text = f"Global progress: **{5}%**")
    st.table(user_progress_table)
    