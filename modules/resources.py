import streamlit as st
import datetime

import utils.user_credentials as uc

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

def resources(user_id, r_1 = [], r_2 = [], r_3 = [], r_4 = [], r_5 = [], r_6 = [], r_7 = [], r_8 = [], r_9 = [], r_10 = [], r_11 = []):
    # Each resource must be: [':selfie:', 'name', 'link_url'] [icon, button_name, link_url]

    g_drive_user_link = uc.run_query_6_h(f"SELECT user_drive_folder FROM `company-data-driven.global.users` WHERE id= {user_id};")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.link_button(":card_index_dividers: Google Drive", g_drive_user_link[0].get("user_drive_folder"))
        st.link_button(f"{r_3[0]} {r_3[1]}", r_3[2]) if len(r_3) > 0 else st.write()
        st.link_button(f"{r_6[0]} {r_6[1]}", r_6[2]) if len(r_6) > 0 else st.write()
        st.link_button(f"{r_9[0]} {r_9[1]}", r_9[2]) if len(r_9) > 0 else st.write()
    with col2:
        st.link_button(f"{r_1[0]} {r_1[1]}", r_1[2]) if len(r_1) > 0 else st.write()
        st.link_button(f"{r_4[0]} {r_4[1]}", r_4[2]) if len(r_4) > 0 else st.write()
        st.link_button(f"{r_7[0]} {r_7[1]}", r_7[2]) if len(r_7) > 0 else st.write()
        st.link_button(f"{r_10[0]} {r_10[1]}", r_10[2]) if len(r_10) > 0 else st.write()
    with col3:
        st.link_button(f"{r_2[0]} {r_2[1]}", r_2[2]) if len(r_2) > 0 else st.write()
        st.link_button(f"{r_5[0]} {r_5[1]}", r_5[2]) if len(r_5) > 0 else st.write()
        st.link_button(f"{r_8[0]} {r_8[1]}", r_8[2]) if len(r_8) > 0 else st.write()
        st.link_button(f"{r_11[0]} {r_11[1]}", r_11[2]) if len(r_11) > 0 else st.write()



