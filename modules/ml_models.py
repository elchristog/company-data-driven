import pandas as pd
import numpy as np
import pycaret
import streamlit
import os



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
    # count_active_ideas = uc.run_query_half_day(f"SELECT COUNT(*) AS count_active_ideas FROM `company-data-driven.{project_name}.daily_post_creation` WHERE posted IS NULL OR posted = 0;")[0].get("count_active_ideas")
    # if count_active_ideas < 10:
    #     st.error(f"I need more ideas! I just have: {count_active_ideas}", icon = "🤬")
    # else:
    #     st.success(f"Available ideas: {count_active_ideas}", icon = "😇")

    # os.write(1, '- posting_posts: Listing ideas \n'.encode('utf-8'))
    # rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.daily_post_creation` WHERE (posted IS NULL OR posted = 0)  ORDER BY creation_date;")
    # ideas = []
    # ids = []
    # for row in rows:
    #     ideas.append(row.get('idea'))
    #     ids.append(row.get('id'))
    # selected_idea = st.selectbox(
    #         label = "Select the idea",
    #         options = ideas,
    #         index = None,
    #         key= "posting_posts_selected_idea",
    #         on_change = post_redaction_generation
    #     )

    # if selected_idea is not None:
    #     st.session_state.posting_posts_user_id = user_id
    #     st.session_state.posting_posts_project_name = project_name
    #     st.session_state.posting_posts_selected_idea_id = ids[ideas.index(selected_idea)]
    #     posting_posts_button = st.button("Post published", on_click = ml_purchase_propension_execution)
        
    # if 'post_redaction_generation' in st.session_state:
    #             st.write("---")
    #             st.write(st.session_state.post_redaction_generation + " #enfermeraenestadosunidos #enfermeriaenusa #enfermerosenestadosunidos")
