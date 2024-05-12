import streamlit as st
import os
import time
import pandas as pd
import datetime

import utils.user_credentials as uc
import utils.g_gemini_gestor as ggg

def study_plan_execution(study_plan_selected_username, study_plan_user_id, study_plan_project_id, study_plan_project_name, study_plan_selected_user_id, study_plan_selected_contract_id):
  os.write(1, '🥏 Executing study_plan_execution \n'.encode('utf-8'))
  st.toast("Updating, please wait", icon = "☺️")
  
  last_user_tests = uc.run_query_half_day(f'''
    WITH all_attempts AS (
    SELECT attempt_date AS date, subject, lesson, q_success AS success
    FROM (
        SELECT na.attempt_date, nq1.subject, nq1.lesson, na.q1_success AS q_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq1 
        ON na.q1_id = nq1.id 
        WHERE user_id = {study_plan_selected_user_id} 
        
        UNION ALL
        
        SELECT na.attempt_date, nq2.subject, nq2.lesson, na.q2_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq2 
        ON na.q2_id = nq2.id 
        WHERE user_id = {study_plan_selected_user_id} 
        
        UNION ALL
        
        SELECT na.attempt_date, nq3.subject, nq3.lesson, na.q3_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq3 
        ON na.q3_id = nq3.id 
        WHERE user_id = {study_plan_selected_user_id} 

        UNION ALL
        
        SELECT na.attempt_date, nq3.subject, nq3.lesson, na.q3_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq3 
        ON na.q3_id = nq3.id 
        WHERE user_id = {study_plan_selected_user_id} 
        
        UNION ALL
        
        SELECT na.attempt_date, nq4.subject, nq4.lesson, na.q4_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq4 
        ON na.q4_id = nq4.id 
        WHERE user_id = {study_plan_selected_user_id} 

        UNION ALL
        
        SELECT na.attempt_date, nq5.subject, nq5.lesson, na.q5_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq5 
        ON na.q5_id = nq5.id 
        WHERE user_id = {study_plan_selected_user_id} 

        UNION ALL
        
        SELECT na.attempt_date, nq6.subject, nq6.lesson, na.q6_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq6 
        ON na.q6_id = nq6.id 
        WHERE user_id = {study_plan_selected_user_id} 

        UNION ALL
        
        SELECT na.attempt_date, nq7.subject, nq7.lesson, na.q7_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq7 
        ON na.q7_id = nq7.id 
        WHERE user_id = {study_plan_selected_user_id} 

        UNION ALL
        
        SELECT na.attempt_date, nq8.subject, nq8.lesson, na.q8_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq8 
        ON na.q8_id = nq8.id 
        WHERE user_id = {study_plan_selected_user_id} 

        UNION ALL
        
        SELECT na.attempt_date, nq9.subject, nq9.lesson, na.q9_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq9 
        ON na.q9_id = nq9.id 
        WHERE user_id = {study_plan_selected_user_id} 
        
        UNION ALL
        
        SELECT na.attempt_date, nq10.subject, nq10.lesson, na.q10_success
        FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS na 
        INNER JOIN `company-data-driven.{study_plan_project_name}.nclex_questions` AS nq10 
        ON na.q10_id = nq10.id 
        WHERE user_id = {study_plan_selected_user_id} 
        
    ) AS ten_questions
    ORDER BY date DESC LIMIT 60
    )
    SELECT subject, lesson, 
           COUNT(*) AS total_questions,
           ROUND(AVG(CASE WHEN success = 1 THEN 100 ELSE 0 END), 2) AS success_percentage
    FROM all_attempts
    GROUP BY subject, lesson
    ORDER BY subject, lesson;
  ''')

  if len(last_user_tests) < 1:
    st.toast("User has no completed any test", icon = "😵‍💫")
  else:
    os.write(1, '- study_plan_execution: Retrieving habits and evolution \n'.encode('utf-8'))
    user_score_evolution = uc.run_query_1_m(f"SELECT ROW_NUMBER() OVER(ORDER BY ta.id ASC) AS attempt, ta.attempt_date, LAG(ta.attempt_date, 1) OVER(ORDER BY ta.id ASC) AS last_attempt_date, DATE_DIFF(ta.attempt_date, LAG(ta.attempt_date, 1) OVER(ORDER BY ta.id ASC), DAY) AS days_between_tests, ta.success_rate AS score, EXTRACT(YEAR FROM ta.attempt_date) AS year_attempt_date, EXTRACT(MONTH FROM ta.attempt_date) AS month_attempt_date, EXTRACT(WEEK FROM ta.attempt_date) AS week_attempt_date FROM `company-data-driven.{study_plan_project_name}.nclex_attempts` AS ta WHERE ta.user_id = {study_plan_selected_user_id} ORDER BY ta.id ASC;")
    if len(user_score_evolution) < 1 or user_score_evolution is None < 0:
                st.warning(f"You have not presented your test", icon = "🫥")
    else:
        user_score_evolution.sort(key=lambda x: x["attempt"])
        user_score_evolution_df = pd.DataFrame(user_score_evolution, columns = ["attempt","attempt_date","last_attempt_date","days_between_tests","score","year_attempt_date","month_attempt_date","week_attempt_date"])
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        user_score_evolution_df_month = user_score_evolution_df[(user_score_evolution_df["year_attempt_date"] == today.year) & (user_score_evolution_df["month_attempt_date"] == today.month)]
        if len(user_score_evolution_df_month) < 1 or user_score_evolution_df_month is None < 0:
                st.warning(f"You have not presented your test", icon = "🫥")
        else:
            month_tests = user_score_evolution_df_month.shape[0]
            avg_score = round(user_score_evolution_df_month.score.mean(),0)
            percentage_tests_with_score_higer_80 = str(round(100*(user_score_evolution_df_month['score'] >= 80).sum()/user_score_evolution_df_month.shape[0],1))
            avg_days_between_tests = round(user_score_evolution_df_month.days_between_tests.mean(),1)

            
            os.write(1, '- study_plan_execution: Creating performance table \n'.encode('utf-8'))
            st.session_state.performance_analysis = last_user_tests
        
            df_last_user_tests = pd.DataFrame(last_user_tests, columns=['subject', 'lesson', 'total_questions', 'success_percentage'])
            df_subject = df_last_user_tests.groupby('subject').agg(total_questions=('total_questions', 'sum'),     avg_success_percentage=('success_percentage', 'mean') ).reset_index()
            df_last_user_tests_top_strength = df_last_user_tests.sort_values(by=['success_percentage', 'total_questions'], ascending=False).head(3)
            df_last_user_tests_top_weakness = df_last_user_tests.sort_values(by=['success_percentage', 'total_questions'], ascending= [True, False]).head(3)
        
            
            st.write("Ahora transformalo en este formato de markdown incluyendo las tablas, muestramelo en formato de codigo .md y aseguirate que se sienta que habla un humano y no una maquina, que sea tuteando y de forma positiva:")
            st.write('# ' + st.session_state.study_plan_selected_name + ' ' + st.session_state.study_plan_selected_lastname + ': Enfermera en Estados Unidos')
            st.table(st.session_state.performance_analysis)
        
            st.write('### Top 3 fortalezas:')
            st.table(df_last_user_tests_top_strength)
        
            st.write('### Top 3 debilidades:')
            st.table(df_last_user_tests_top_weakness)
        
        
            os.write(1, '- study_plan_execution: Creating study plan \n'.encode('utf-8'))
            st.session_state.study_plan = ggg.gemini_general_prompt('Actua como un asesor experto en NCLEX, analiza el rendimiento de la persona y creale un plan de estudio', 'Ahora soy un asesor experto en NCLEX y en la creacion de planes de estudio y siempre muestro a nivel de subject y lesson', 'EN ESPANOL: actua como un entrenador experto en NCLEX, he estado practicando para el examen con este simulacro, quiero que me des una retroalimentacion en espanol sobre las (subject/lesson) en los que ya tengo un buen performance , sobre las (subject/lesson) que aun tengo debiles y creame una metodologia de estudio muy concreta a una semana (dia a dia) para poder superar el nclex, cuento con el libros Saunders book, indicame los capitulos que debo leer esta semana para apoyarme y reforzar mi estudio que sea dia a dia y realizable, pocos capitulos, haz un analisis de las (subject/lesson) que tengo fuertes guiandote en esta tabla ' + str(df_last_user_tests_top_strength) +', y tambien analiza mis puntos debiles usando esta tabla ' + str(df_last_user_tests_top_weakness) +', Ahora, enfocandote en estas debilidades usa el libro de Saunders y detecta los capitulos que tengo que leer para poder superar dichas debilidades, tambien indicame que me recomiendas que haga un simulacro diario en nuestra plataforma para que siga reforzando y asi el equipo va a poder seguir optimizando el plan de estudios, quiero que la respuesta que des tenga esta estrtuctuta (- Habito: Estas presentando un test cada X dias, muy bien - Fortalezas: Analisis de la tabla de mis fortalezas dandome una opinion estos resultados, - Por mejorar: Analizis de mis debilidades indicando (subject, lesson, justificacion) y un analisis de compo puedo reforzar esto, - Recordatorio de seguir haciendo un test diario - Capitulos a leer esta semana indicando el nombre del libro y los capitulos con metas realistas y faciles de leer y que realmente ayuden a superar las debilidades Lunes: lee xx y practica xxx, martes: xxx, miercoles: xxx, jueves: xxx, viernes: xxx  - Felicitacion o incentivo a hacer test diario segun la frecuencia con que viene presentando los tests y que porcentaje de simulacros han tenido mas de 80% correcto ): [User Performance] Month evolution Month completed Tests:' +str(month_tests)+'  Avg score: '+str(avg_score)+' % tests with score >= 80: '+str(percentage_tests_with_score_higer_80)+' Avg days between tests: '+ str(avg_days_between_tests) +' [NCLEX Categories]: subjects: Adult Health, Child Health, Critical Care, Fundamentals, Leadership & Management, Maternal & Newborn Health, Mental Health, Pharmacology lessons: Cardiovascular, Gastrointestinal/Nutrition, Neurologic, Endocrine, Respiratory, Prioritization, Safety / Infection Control, Mental Health, Urinary/Renal/Fluid and Electrolytes, Antepartum, Basic Care & Comfort, Hematological/Oncological, Infectious Disease, Critical Care Concepts, Musculoskeletal, Psychiatric Medications, Management Concepts, Dosage Calculation, Ethical/Legal, Integumentary, Skills/Procedures, Newborn, Assignment/Delegation, Growth & Development, Perioperative Care, Labor/Delivery, Medication Administration, Visual/Auditory, Analgesics, Postpartum, Reproductive, Immune, Cultural, Spiritual, and Religion Concepts, Blood and Blood Products, Abuse/Neglect, Acid-Base Imbalances, Substance Abuse and other dependencies, Immunizations, Reproductive and Maternity, Environmental Emergencies [Books Content] SAUNDERS content: Unit I NCLEX-RN® Exam Preparation, 1 1 Clinical Judgment and the Next Generation NCLEX (NGN)-RN® Examination, 2 2 Self-Efcacy and Pathways to Success, 17 3 The NCLEX-RN® Examination from a Graduate’s Perspective, 22 4 Clinical Judgment and Test-Taking Strategies, 24 Unit II Professional Standards in Nursing, 38 5 Population Health Nursing, 40 6 Ethical and Legal Issues, 53 7 Prioritizing Client Care: Leadership, Delegation, and Emergency Response Planning, 68 Unit III Foundations of Care, 85 8 Fluids and Electrolytes, 88 9 Acid-Base Balance, 106 10 Vital Signs and Laboratory Reference Intervals, 116 11 Nutrition, 132 12 Health and Physical Assessment of the Adult Client, 143 13 Safety and Infection Control, 166 14 Medication Administration and Intravenous Therapies, 178 15 Perioperative Nursing Care, 189 16 Hygiene, Mobility, and Skin Integrity, 204 17 Urinary and Bowel Elimination, 218 Unit IV Growth and Development Across the Life Span, 234 18 Theories of Growth and Development, 236 19 Growth, Development, and Stages of Life, 244 20 Care of the Older Client, 266 Unit V Maternity Nursing, 275 21 Reproductive System, 277 22 Prenatal Period, 285 23 Risk Conditions Related to Pregnancy, 300 24 Labor and Birth, 323 25 Problems with Labor and Birth, 336 26 Postpartum Period, 343 27 Postpartum Complications, 350 28 Care of the Newborn, 358 29 Maternity and Newborn Medications, 380 Unit VI Pediatric Nursing, 391 30 Integumentary Problems, 392 31 Hematological Problems, 399 32 Oncological Problems, 406 33 Metabolic and Endocrine Problems, 416 34 Gastrointestinal Problems, 425 35 Eye, Ear, and Throat Problems, 444 36 Respiratory Problems, 451 37 Cardiovascular Problems, 467 38 Renal and Genitourinary Problems, 479 39 Neurological and Cognitive Problems, 487 40 Musculoskeletal Problems, 498 41 Immune Problems and Infectious Diseases, 507 42 Pediatric Medication Administration and Calculations, 520 Contents Telegram & Insta: NCLEX_RN_Edu iv Contents Unit VII Integumentary Problems of the Adult Client, 527 43 Integumentary Problems, 528 44 Integumentary Medications, 538 Unit VIII Oncological and Hematological Problems of the Adult Client, 547 45 Oncological and Hematological Problems, 549 46 Oncological and Hematological Medications, 587 Unit IX Endocrine Problems of the Adult Client, 598 47 Endocrine Problems, 599 48 Endocrine Medications, 626 Unit X Gastrointestinal Problems of the Adult Client, 641 49 Gastrointestinal Problems, 643 50 Gastrointestinal Medications, 671 Unit XI Respiratory Problems of the Adult Client, 679 51 Respiratory Problems, 680 52 Respiratory Medications, 701 Unit XII Cardiovascular Problems of the Adult Client, 719 53 Cardiovascular Problems, 720 54 Cardiovascular Medications, 760 Unit XIII Renal and Urinary Problems of the Adult Client, 778 55 Renal and Urinary Problems, 779 56 Renal and Urinary Medications, 811 Unit XIV Eye and Ear Problems of the Adult Client, 821 57 Eye and Ear Problems, 822 58 Eye and Ear Medications, 842 Unit XV Neurological Problems of the Adult Client, 852 59 Neurological Problems, 853 60 Neurological Medications, 877 Unit XVI Musculoskeletal Problems of the Adult Client, 888 61 Musculoskeletal Problems, 889 62 Musculoskeletal Medications, 910 Unit XVII Immune Problems of the Adult Client, 918 63 Immune Problems, 919 64 Immune Medications, 933 Unit XVIII Mental Health Problems of the Adult Client, 940 65 Foundations of Psychiatric Mental Health Nursing, 941 66 Mental Health Problems, 954 67 Addictions, 975 68 Crisis Theory and Intervention, 987 69 Psychotherapeutic Medications, 1001 Unit XIX Complex Care, 1015 70 Complex Care, 1017 References, 1088 Index, 1090  [User strenghts]' + str(df_last_user_tests_top_strength) + '[User weakness]'  + str(df_last_user_tests_top_weakness))
            st.write('### Tu puntaje por subject:')
            st.table(df_subject)
            st.write(st.session_state.study_plan)
            st.write('---')
            st.write("Crea una unica tabla Comparativa sobre que tanto he mejorado de la primera vez a la segunda, es decir que tanto han mejorado mis resultados en cada componentes de la PRIMERA a la segunda vez, mostrando en las Filas las dimensiones evaluadas y tres columnas, en la primera el % de aciertos de la PRIMERA vez y en la segunda el % de aciertos de la segunda vez y en la TERCERA el % de cambio, Asegúrate de siempre mostrarlo de forma numerica :")
            
            st.toast('Study Plan Created!', icon = '🎈')
            st.balloons()
    
  time.sleep(1)
  del st.session_state['study_plan_selected_username']
  del st.session_state['study_plan_user_id']
  del st.session_state['study_plan_project_id']
  del st.session_state['study_plan_project_name']
  del st.session_state['study_plan_selected_user_id']
  del st.session_state['study_plan_selected_contract_id']
  del st.session_state['study_plan_selected_name']
  del st.session_state['study_plan_selected_lastname']
  
  uc.run_query_half_day.clear()
  




def study_plan(user_id, project_id, project_name):
  os.write(1, '🥏 Executing study_plan \n'.encode('utf-8'))
  os.write(1, '- study_plan: Retrieving users \n'.encode('utf-8'))
  rows = uc.run_query_half_day(f"SELECT u.id, u.username, u.name, u.lastname, c.id as contract_id FROM `company-data-driven.{project_name}.contracts` AS c INNER JOIN `company-data-driven.global.users` AS u ON u.id = c.user_id;")
  ids = []
  usernames = []
  names = []
  lastnames = []
  contract_ids = []
  for row in rows:
      ids.append(row.get('id'))
      usernames.append(row.get('username'))
      names.append(row.get('name'))
      lastnames.append(row.get('lastname'))
      contract_ids.append(row.get('contract_id'))

  if 'study_plan_selected_username' not in st.session_state:
      selected_username = st.selectbox(
              label = "Select the username",
              options = usernames,
              index = 0,
              key= "usernames"
          )
      st.session_state.study_plan_selected_username = selected_username
      if st.session_state.study_plan_selected_username is not None:
            st.session_state.study_plan_selected_username_index  = usernames.index(st.session_state.study_plan_selected_username)
  else:
      selected_username = st.selectbox(
              label = "Select the username",
              options = usernames,
              index = st.session_state.study_plan_selected_username_index,
              key= "usernames"
          )
      st.session_state.study_plan_selected_username = selected_username
      if st.session_state.study_plan_selected_username is not None:
            st.session_state.study_plan_selected_username_index  = usernames.index(st.session_state.study_plan_selected_username)

  if selected_username is not None:
      st.session_state.study_plan_user_id = user_id
      st.session_state.study_plan_project_id = project_id
      st.session_state.study_plan_project_name = project_name
      st.session_state.study_plan_selected_user_id = ids[usernames.index(selected_username)]
      st.session_state.study_plan_selected_contract_id = contract_ids[usernames.index(selected_username)]
      st.session_state.study_plan_selected_name = names[usernames.index(selected_username)]
      st.session_state.study_plan_selected_lastname = lastnames[usernames.index(selected_username)]
    
    
      study_plan_button = st.button("Create Study plan", on_click = study_plan_execution, args = [st.session_state.study_plan_selected_username, st.session_state.study_plan_user_id, st.session_state.study_plan_project_id, st.session_state.study_plan_project_name, st.session_state.study_plan_selected_user_id, st.session_state.study_plan_selected_contract_id])











def add_study_guide_execution():
    os.write(1, '🥏 Executing add_study_guide_execution \n'.encode('utf-8'))
    # if 'posting_posts_selected_idea' in st.session_state:
    #     os.write(1, '- posting_posts_execution: Saving posted idea\n'.encode('utf-8'))
    #     st.toast("Please wait", icon = "☺️")
    #     uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.posting_posts_project_name}.daily_post_creation` SET posted = 1, posted_date = CURRENT_DATE(), poster_user_id = {st.session_state.posting_posts_user_id} WHERE id = '{st.session_state.posting_posts_selected_idea_id}'")
    #     st.toast("Info saved!", icon = "👾")
    #     st.balloons()
    #     time.sleep(1)
    #     uc.run_query_half_day.clear()
    #     del st.session_state.posting_posts_user_id
    #     del st.session_state.posting_posts_project_name
    #     del st.session_state.posting_posts_post_idea
    #     del st.session_state.posting_posts_selected_idea_id 


def add_study_guide(user_id, project_name):
    os.write(1, '🥏 Executing add_study_guide \n'.encode('utf-8'))
    os.write(1, '- add_study_guide: Showing form \n'.encode('utf-8'))
    selected_folder = st.selectbox(
            label = "Select the folder",
            options = ['a', 'b'],
            index = None,
            key= "add_study_guide_selected_folder"
        )
  
    subjects_rows = uc.run_query_half_day(f"SELECT DISTINCT(subject) AS subject FROM `company-data-driven.{project_name}.nclex_questions`;")
    subjects = []
    for row in subjects_rows:
        subjects.append(row.get('subject'))
    selected_subject = st.selectbox(
            label = "Select the subject",
            options = subjects,
            index = None,
            key= "add_study_guide_selected_subject"
        )


    # lessons = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.daily_post_creation` WHERE (posted IS NULL OR posted = 0)  ORDER BY creation_date;")

    

    # if selected_idea is not None:
    #     st.session_state.posting_posts_user_id = user_id
    #     st.session_state.posting_posts_project_name = project_name
    #     st.session_state.posting_posts_selected_idea_id = ids[ideas.index(selected_idea)]
    #     posting_posts_button = st.button("Post published", on_click = posting_posts_execution)
        
