import streamlit as st
import pandas as pd
import time
import datetime
import re
import ast
import os

import utils.user_credentials as uc
import utils.g_gemini_gestor as ggg

# callbacks https://discuss.streamlit.io/t/click-twice-on-button-for-changing-state/45633/2


def seo_ideation_execution(project_name, project_keyword, user_id, role_id, text_input_1):
    os.write(1, '🥏 Executing seo_ideation_execution \n'.encode('utf-8'))
    os.write(1, '- seo_ideation_execution: Generating Ideas\n'.encode('utf-8'))
    st.toast('Generating Ideas:', icon="🤖")  
    if len(text_input_1) < 10:
        st.toast("Ideas extras is to short!", icon = "💣")
    else:
        uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.keyword_seo_ideation_log` (id, creation_date, creator_user_id, ideas) VALUES (GENERATE_UUID(), CURRENT_DATE(), {user_id}, '{text_input_1}')")  
        keyword_research = uc.run_query_10_s(f"SELECT * FROM `company-data-driven.{project_name}.keywords` ORDER BY RAND() LIMIT 50;")        
        longtail_questions = uc.run_query_10_s(f"SELECT * FROM `company-data-driven.{project_name}.keyword_common_questions` ORDER BY RAND() LIMIT 50;")        
        created_content = uc.run_query_10_s(f"SELECT page AS page, SUM(clicks) AS clicks, SUM(impressions) AS impressions, AVG(ctr) AS ctr  FROM `company-data-driven.{project_name}.traffic_analytics_web_pages` GROUP BY page;")  
        st.toast("Keyword research", icon = "☺️")
        time.sleep(1)
        st.toast("IA working", icon = "☺️")
        all_ideas = uc.run_query_10_s(f"SELECT ideas FROM `company-data-driven.{project_name}.keyword_seo_ideation_log`;")  
        answer = ggg.gemini_general_prompt("Eres un experto en SEO, especialmente en ideacion de articulos web que posicionen rapido con palabras clave long tail [KEYWORD]" + str(project_keyword) +  "[/KEYWORD], siempre muestras tus respuestas en forma de array de python donde cada articulo es un elemento del array y no contiene diccionarios dentro ni comentarios, solo strings" , "Ahora soy un experto generando ideas de contenido que se posicionen rapidamente, ideo nuevos articulos y no repito los anteriores, siempre muestro mis respuestas en forma de array de python donde cada articulo es un elemento del array  y no contiene diccionarios dentro  ni comentarios, solo strings", "Eres un experto en SEO, especialmente en ideacion de articulos web que posicionen rapido con palabras clave long tail [KEYWORD]" + str(project_keyword) + " [/KEYWORD] [KEYWORD_RESEARCH]" + str(keyword_research) +  "[/KEYWORD_RESEARCH] [LONGTAIL_QUESTIONS]" +str(longtail_questions) + "[/LONGTAIL_QUESTIONS] [IDEASEXTRA]" + str(all_ideas) + "[/IDEASEXTRA] [YACREADO]" + str(created_content) + "[/YACREADO] [INSTRUCTION] Analiza las metricas, Dame ideas de 6 articulos que posicionen aclarando la keyword que quieres posicionar en cada uno y una descripcion de que debe tratar el articulo, evita estrictamente hablar sobre articulos que ya he creado ya que quiero oportunidades nuevas [YACREADO], que ninguna de las nuevas ideas exista previamente en [YACREADO], asegura que 4 de los articulos vengan de los [LONGTAIL_QUESTIONS] o de los [IDEASEXTRA] y muestra cuales fueron, recuerda que cada articulo ideado se muestra como un elemento de un array de python y no contiene diccionarios dentro  ni comentarios, solo strings:[/INSTRUCTION]")
        answer_array = ast.literal_eval(answer)
        for idea in answer_array:
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.content_creation` (id, creation_date, creator_user_id, idea) VALUES (GENERATE_UUID(), CURRENT_DATE(), {user_id}, '{idea}');") 
        st.toast("IA finished!", icon = "🤩")
        st.write(answer)
        st.session_state.answer = answer
        time.sleep(1)
        uc.run_query_30_m.clear()
        
        
    

def seo_ideation(project_name, project_keyword, user_id, role_id):
    os.write(1, '🥏 Executing seo_ideation \n'.encode('utf-8'))
    os.write(1, '- seo_ideation: Counting previuos ideas\n'.encode('utf-8'))
    available_contents = uc.run_query_30_m(f"SELECT COUNT(*) AS available_contents FROM `company-data-driven.{project_name}.content_creation` WHERE created_video IS NULL OR created_video = 0;")[0].get('available_contents') 
    if available_contents < 10:
        st.error(f"I need more contents! I just have: {available_contents}", icon = "🤬")
    else:
        st.success(f"Available contents: {available_contents}", icon = "😇")
        
    text_input_1 = st.text_input(
        "Ideas extras de keywords",
        label_visibility = 'visible',
        disabled = False,
        placeholder = 'pasos para ser enfermera latina en usa, comparacion de agencias de enfermeria, cuanto gana una enfermera en texas',
        help = 'This ideas will be saved an priorized with the time',
        key = 'text_input_1'
    )

    submitted = st.button("Generate ideas", on_click = seo_ideation_execution, args = [project_name, project_keyword, user_id, role_id, text_input_1])
    if 'answer' in st.session_state:
        st.download_button('Download answer', st.session_state.answer, file_name = 'content_ideas.txt')

    
    if role_id == 1:
        st.write("---")
        st.header("Keyword research steps")
        st.write("Keywords Everywere suscripcion anual con el plan bronce, son 15 dolares al anio mantener la extension apagada y solo prenderla una vez por cada proyecto busco mi keyword en google  creo un google sheets en la carpeta del emprendimiento con columnas(keyword, volume, cpc, cpm) se llama keywords creo un segundo google sheets llamado keyword_common_questions con la columna question y ahi voy poniendo las pregunats que buscan 1- descargo las related keywords y las  pongo en el archivo, asegurarse de respetar las columnas 2- lo mismo con las Long-Tail Keywords y si hay ams pues a todas  3- le doy click a find long tail keywords, espero que se genere y las descargo todas  4- copio cada una de las preguntas que la gente suele hacer , luego las abro todas y copio todas las nuevas 4- copio los titulos de las 3 primeras paginas a las questions antepongo (que, como, donde, por que, quien, cuanto, comprar, contratar, el mejor, cual es, y todo el funnel del usuario) a la keyword, repito la busqueda eligiendo la primera apcion que google me ofrece (llevandome esa opcion a las questions, si no ofrece nada pues buscar asi) , a descarga de los 3 archivos y la copiada de todas las preguntas al final eliminar duplicados de ambos archivos, y del de keywords mantener todo ordenando de mayor a menor cpc leer en bigquery como tablas con los nombres cambiados: keywords_res y  keyword_common_questions_res, recordar ponerlas como desde drive y luego google sheets, el nombre de la tabla, schema auto detect,  y en ehaders row to skip poner 1 luego hacer un query para leer la tabla, darle a save results, bigquery table, ahi si ponerle el nombre que es y eliminar la primera tabla ")




def video_creation_execution():
    os.write(1, '🥏 Executing video_creation_execution \n'.encode('utf-8'))
    os.write(1, '- video_creation_execution: Saving created idea\n'.encode('utf-8'))
    st.toast("Please wait", icon = "☺️")
    
    uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.video_creation_project_name}.content_creation` SET created_video = 1, created_video_date = CURRENT_DATE(), video_creator_user_id = {st.session_state.video_creation_user_id} WHERE id = '{st.session_state.video_creation_selected_idea_id}';")
    
    st.toast("Info saved!", icon = "👾")
    st.balloons()
    time.sleep(1)
    uc.run_query_half_day.clear()
    del st.session_state.video_creation_user_id
    del st.session_state.video_creation_project_name
    del st.session_state.video_creation_selected_idea_id
    del st.session_state.video_creation_selected_idea
    



def video_creation(user_id, project_name):
    os.write(1, '🥏 Executing video_creation \n'.encode('utf-8'))
    os.write(1, '- video_creation: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.content_creation` WHERE created_video IS NULL OR created_video = 0 ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "video_creation_selected_idea"
        )
    if selected_idea is not None:
        st.session_state.video_creation_selected_idea_id = ids[ideas.index(selected_idea)]
        st.session_state.video_creation_user_id = user_id
        st.session_state.video_creation_project_name = project_name
        created_video_button = st.button("I already created this video", on_click = video_creation_execution)







def video_edition_execution():
    os.write(1, '🥏 Executing video_edition_execution \n'.encode('utf-8'))
    os.write(1, '- video_edition_execution: Saving created idea\n'.encode('utf-8'))
    st.toast("Please wait", icon = "☺️")
    
    uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.video_edition_project_name}.content_creation` SET edited_video = 1, edited_date = CURRENT_DATE(), video_editor_user_id = {st.session_state.video_edition_user_id} WHERE id = '{st.session_state.video_edition_selected_idea_id}';")
    
    st.toast("Info saved!", icon = "👾")
    st.balloons()
    time.sleep(1)
    uc.run_query_half_day.clear()
    del st.session_state.video_edition_user_id
    del st.session_state.video_edition_project_name
    del st.session_state.video_edition_selected_idea_id
    del st.session_state.video_edition_selected_idea
    



def video_edition(user_id, project_name):
    os.write(1, '🥏 Executing video_edition \n'.encode('utf-8'))
    os.write(1, '- video_edition: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.content_creation` WHERE (created_video IS NOT NULL OR created_video != 0) AND (edited_video IS NULL OR edited_video = 0) ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "video_edition_selected_idea"
        )
    if selected_idea is not None:
        st.session_state.video_edition_selected_idea_id = ids[ideas.index(selected_idea)]
        st.session_state.video_edition_user_id = user_id
        st.session_state.video_edition_project_name = project_name
        edited_video_button = st.button("I already edited this video", on_click = video_edition_execution)







def video_uploading_execution():
    os.write(1, '🥏 Executing video_uploading_execution \n'.encode('utf-8'))
    os.write(1, '- video_uploading_execution: Saving created idea\n'.encode('utf-8'))
    st.toast("Please wait", icon = "☺️")
    
    uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.video_uploading_project_name}.content_creation` SET video_uploaded = 1, video_uploaded_date = CURRENT_DATE(), video_uploaded_user_id = {st.session_state.video_uploading_user_id} WHERE id = '{st.session_state.video_uploading_selected_idea_id}';")
    
    st.toast("Info saved!", icon = "👾")
    st.balloons()
    time.sleep(1)
    uc.run_query_half_day.clear()
    del st.session_state.video_uploading_user_id
    del st.session_state.video_uploading_project_name
    del st.session_state.video_uploading_selected_idea_id
    del st.session_state.video_uploading_selected_idea
    

def video_title_description_generation():
    st.session_state.video_title_description_generation = ggg.gemini_general_prompt("Eres un redactor SEO experto en posicionar keywords y generar contenidos que llaman la atencion", "Ahora soy un redactor SEO experto", "[KEYWORD] "+str(st.session_state.video_uploading_selected_idea)+" [/KEYWORD][EXTRA_KEYWORDS] enfermera, estados unidos, registered nurse, enfermeriamigracionnclex, nclex rnielts, ¿Cómo convertirme en enfermera en Estados Unidos?, Pasos para ser enfermera en Estados Unidos., ¿Cómo puedo ser enfermera en USA?, Guía para ser enfermera en Estados Unidos., ¿Qué necesito para ser enfermera en Estados Unidos?, Consejos para ser enfermera en USA., Proceso para convertirse en enfermera en Estados Unidos., enfermeriamigracionnclexieltssalariohomologacionusa, enfermero, trabajo, como ser enfermera en estados unidos, enfermero en estados unidos, salario enfermera usasalario de enfermerasalario de enfermeria, Cómo ser enfermera en USA, Pasos para ser enfermera en Estados Unidos, Requisitos para ejercer enfermería en USA, Guía para convertirse en enfermera en Estados Unidos, trabajo enfermera, NCLEX, IELTS, Salario, Homologación, USA, Trabajo, Requisitos, #enfermeriaenestadosunidos, #enfermeraestadosunidos, #registerednurse, #enfermeriamigracionnclex, #nclexrnielts [/EXTRA_KEYWORDS][DESCRIPTION] [Descripcion corta que contenga la [KEYWORD] ]luego mostrar Este texto:Agenda una asesoría conmigo:- Whatsapp: https://bit.ly/45SidF6Mis redes: - Web: https://enfermeraenestadosunidos.com/- Instagram: https://www.instagram.com/enfermeraenestadosunidos- TikTok: https://www.tiktok.com/@enfermeraenestadosunidos[Descripción extensa que diga de que se trata el video basandose en la [KEYWORD] y contenga 2 mil palabras] [/DESCRIPTION][INSTRUCTION] Crea el título de un video de YouTube que contenga la [KEYWORD] que contenga menos de 8 palabras, llama la atención usando mayusculas selectivas y emojis. Luego Crea Una descripción que cumpla con todos los requisitos de [DESCRIPTION]. y por último Crea 60 tags exactamente, jugando con la [KEYWORD] y las [EXTRA_KEYWORDS] que ayuden a posicionar el video, Asegúrate de mostrar Este listado de tags en un solo parrafo y separado por comas  y no usar hashtags[/INSTRUCTION]")
    
    

def video_uploading(user_id, project_name):
    os.write(1, '🥏 Executing video_uploading \n'.encode('utf-8'))
    os.write(1, '- video_uploading: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.content_creation` WHERE (created_video IS NOT NULL OR created_video != 0) AND (edited_video IS NOT NULL OR edited_video != 0) AND (video_uploaded IS NULL OR video_uploaded = 0) ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "video_uploading_selected_idea",
            on_change = video_title_description_generation
        )
    if selected_idea is not None:
        st.session_state.video_uploading_selected_idea_id = ids[ideas.index(selected_idea)]
        st.session_state.video_uploading_user_id = user_id
        st.session_state.video_uploading_project_name = project_name
        uploading_video_button = st.button("I already uploaded this video", on_click = video_uploading_execution)
    if 'video_title_description_generation' in st.session_state:
        st.write("---")
        st.write(st.session_state.video_title_description_generation )
        st.download_button('Download Texts', st.session_state.video_title_description_generation, file_name = 'video_title_description_generation.txt')
        




def video_to_shorts_execution():
    os.write(1, '🥏 Executing video_to_shorts_execution \n'.encode('utf-8'))
    os.write(1, '- video_to_shorts_execution: Updating\n'.encode('utf-8'))
    st.toast("Please wait", icon = "☺️")
    
    uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.video_to_shorts_project_name}.content_creation` SET video_shorts_created = 1, video_shorts_creation_date = CURRENT_DATE(), video_shorts_creator_user_id = {st.session_state.video_to_shorts_user_id} WHERE id = '{st.session_state.video_to_shorts_selected_idea_id}';")
    
    st.toast("Info saved!", icon = "👾")
    st.balloons()
    time.sleep(1)
    uc.run_query_half_day.clear()
    del st.session_state.video_to_shorts_user_id
    del st.session_state.video_to_shorts_project_name
    del st.session_state.video_to_shorts_selected_idea_id
    del st.session_state.video_to_shorts_selected_idea


def short_title_description_generation():
    st.session_state.short_title_description_generation = ggg.gemini_general_prompt("Eres un redactor SEO experto en posicionar keywords y generar contenidos que llaman la atencion", "Ahora soy un redactor SEO experto", "[KEYWORD] "+str(st.session_state.short_description)+" [/KEYWORD][EXTRA_KEYWORDS] enfermera, estados unidos, registered nurse, enfermeriamigracionnclex, nclex rnielts, ¿Cómo convertirme en enfermera en Estados Unidos?, Pasos para ser enfermera en Estados Unidos., ¿Cómo puedo ser enfermera en USA?, Guía para ser enfermera en Estados Unidos., ¿Qué necesito para ser enfermera en Estados Unidos?, Consejos para ser enfermera en USA., Proceso para convertirse en enfermera en Estados Unidos., enfermeriamigracionnclexieltssalariohomologacionusa, enfermero, trabajo, como ser enfermera en estados unidos, enfermero en estados unidos, salario enfermera usasalario de enfermerasalario de enfermeria, Cómo ser enfermera en USA, Pasos para ser enfermera en Estados Unidos, Requisitos para ejercer enfermería en USA, Guía para convertirse en enfermera en Estados Unidos, trabajo enfermera, NCLEX, IELTS, Salario, Homologación, USA, Trabajo, Requisitos, #enfermeriaenestadosunidos, #enfermeraestadosunidos, #registerednurse, #enfermeriamigracionnclex, #nclexrnielts [/EXTRA_KEYWORDS][DESCRIPTION] [Descripcion corta que contenga la [KEYWORD] ]luego mostrar Este texto:Agenda una asesoría conmigo:- Whatsapp: https://bit.ly/45SidF6Mis redes: - Web: https://enfermeraenestadosunidos.com/- Instagram: https://www.instagram.com/enfermeraenestadosunidos- TikTok: https://www.tiktok.com/@enfermeraenestadosunidos[Descripción extensa que diga de que se trata el video basandose en la [KEYWORD] y contenga 2 mil palabras] [/DESCRIPTION][INSTRUCTION] Crea el título de un video de YouTube que contenga la [KEYWORD] que contenga menos de 8 palabras, llama la atención usando mayusculas selectivas y emojis. Luego Crea Una descripción que cumpla con todos los requisitos de [DESCRIPTION]. y por último Crea 60 tags exactamente, jugando con la [KEYWORD] y las [EXTRA_KEYWORDS] que ayuden a posicionar el video, Asegúrate de mostrar Este listado de tags en un solo parrafo y separado por comas  y no usar hashtags[/INSTRUCTION]")
    

def video_to_shorts(user_id, project_name):
    os.write(1, '🥏 Executing video_to_shorts \n'.encode('utf-8'))
    os.write(1, '- video_to_shorts: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.content_creation` WHERE (created_video IS NOT NULL OR created_video != 0) AND (edited_video IS NOT NULL OR edited_video != 0) AND (video_uploaded IS NOT NULL OR video_uploaded != 0) AND (video_shorts_created IS NULL OR video_shorts_created = 0) ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "video_to_shorts_selected_idea"
        )
    if selected_idea is not None:
        st.session_state.video_to_shorts_selected_idea_id = ids[ideas.index(selected_idea)]
        st.session_state.video_to_shorts_user_id = user_id
        st.session_state.video_to_shorts_project_name = project_name

        short_description = st.text_input('Short description', placeholder = 'Como pasar el NCLEX', help = 'Debe ser una keyword que describa de que trata el short', key = 'short_description', on_change = short_title_description_generation)
        
        video_to_shorts_button = st.button("I already created shorts", on_click = video_to_shorts_execution)

        if 'short_title_description_generation' in st.session_state:
                st.write("---")
                st.write(st.session_state.short_title_description_generation )
                st.download_button('Download Texts', st.session_state.short_title_description_generation, file_name = 'short_title_description_generation.txt')
    




def web_writing_execution():
    os.write(1, '🥏 Executing web_writing_execution \n'.encode('utf-8'))
    if 'web_writing_agree' in st.session_state:
        os.write(1, '- web_writing_execution: Updating\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.web_writing_project_name}.content_creation` SET web_created = 1, web_creation_date = CURRENT_DATE(), web_creator_user_id = {st.session_state.web_writing_user_id} WHERE id = '{st.session_state.web_writing_selected_idea_id}';")
        
        st.toast("Info saved!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.web_writing_user_id
        del st.session_state.web_writing_project_name
        del st.session_state.web_writing_selected_idea_id
        del st.session_state.web_writing_selected_idea
        del st.session_state.web_writing_agree
    else:
        st.toast("If you are sure you have finished, mark the checkbox")


def web_writing_generation():
    length = len(st.session_state.web_writing_transcript)
    half_length = length // 2
    first_half = st.session_state.web_writing_transcript[:half_length]
    second_half = st.session_state.web_writing_transcript[half_length:]
    
    st.session_state.web_writing_generation_part_1 = ggg.gemini_general_prompt("Eres un experto reescribiendo articulos, vas a recibir un articulo y a volverlo a  redactar de forma perfecta sin inventar anda nuevo, usando unicamente la informacion que te voy a entregar", "Ahora soy un experto redactor", f"escribe un articulo de minimo 4 mil palabras sobre '{st.session_state.web_writing_selected_idea}' (Asegurate que la palabra clave '{st.session_state.web_writing_selected_idea}' aparezca 5 veces en el articulo), que todo se explique en detalle y que hable sobre: " + first_half)
    st.session_state.web_writing_generation_part_2 = ggg.gemini_general_prompt("Eres un experto reescribiendo articulos, vas a recibir un articulo y a volverlo a  redactar de forma perfecta sin inventar anda nuevo, usando unicamente la informacion que te voy a entregar", "Ahora soy un experto redactor", f"escribe un articulo de minimo 4 mil palabras sobre '{st.session_state.web_writing_selected_idea}' (Asegurate que la palabra clave '{st.session_state.web_writing_selected_idea}' aparezca 5 veces en el articulo), que todo se explique en detalle y que hable sobre: " + second_half)

    st.session_state.web_writing_generation = st.session_state.web_writing_generation_part_1 + st.session_state.web_writing_generation_part_2
    

def web_writing(user_id, project_name):
    os.write(1, '🥏 Executing web_writing \n'.encode('utf-8'))
    os.write(1, '- web_writing: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.content_creation` WHERE (created_video IS NOT NULL OR created_video != 0) AND (edited_video IS NOT NULL OR edited_video != 0) AND (video_uploaded IS NOT NULL OR video_uploaded != 0) AND (video_shorts_created IS NOT NULL OR video_shorts_created != 0) AND (web_created IS NULL OR web_created = 0) ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "web_writing_selected_idea"
        )
    if selected_idea is not None:
        st.session_state.web_writing_selected_idea_id = ids[ideas.index(selected_idea)]
        st.session_state.web_writing_user_id = user_id
        st.session_state.web_writing_project_name = project_name

        web_writing_transcript = st.text_input('Video transcript', placeholder = 'Para pasar el nclex debes...', help = 'Asegurarse de no dar caracteres extranios', key = 'web_writing_transcript', on_change = web_writing_generation)

        agree = st.checkbox('I finished', key = 'web_writing_agree')
        web_writing_button = st.button("I already created the Web", on_click = web_writing_execution)

        if 'web_writing_generation' in st.session_state:
                st.write("---")
                st.write(st.session_state.web_writing_generation)
                st.download_button('Download Texts', st.session_state.web_writing_generation, file_name = 'web_writing_generation.txt')






def post_idea_creation_execution():
    os.write(1, '🥏 Executing video_creation_execution \n'.encode('utf-8'))
    if 'post_idea_creation_post_idea' in st.session_state:
        if len(st.session_state.post_idea_creation_post_idea) < 20:
            st.toast("To short!", icon = "🤡")
        else:
            os.write(1, '- video_creation_execution: Saving created idea\n'.encode('utf-8'))
            st.toast("Please wait", icon = "☺️")
            uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.post_idea_creation_project_name}.daily_post_creation` (id, creation_date, creator_user_id, idea) VALUES (GENERATE_UUID(), CURRENT_DATE(), {st.session_state.post_idea_creation_user_id}, '{st.session_state.post_idea_creation_post_idea}')")
            st.toast("Info saved!", icon = "👾")
            st.balloons()
            time.sleep(1)
            uc.run_query_half_day.clear()
            del st.session_state.post_idea_creation_user_id
            del st.session_state.post_idea_creation_project_name
            del st.session_state.post_idea_creation_post_idea



def post_idea_creation(user_id, project_name):
    os.write(1, '🥏 Executing post_idea_creation \n'.encode('utf-8'))
    os.write(1, '- post_idea_creation: Showing form \n'.encode('utf-8'))
    count_active_ideas = uc.run_query_half_day(f"SELECT COUNT(*) AS count_active_ideas FROM `company-data-driven.{project_name}.daily_post_creation` WHERE posted IS NULL OR posted = 0;")[0].get("count_active_ideas")
    
    if count_active_ideas < 10:
        st.error(f"I need more ideas! I just have: {count_active_ideas}", icon = "🤬")
    else:
        st.success(f"Available ideas: {count_active_ideas}", icon = "😇")
    
    post_idea = st.text_input(
            label = "Add new post idea",
            key= "post_idea_creation_post_idea",
            placeholder = "Cuando llega el momento de estudiar para el NCLEX, muchas personas lo primero que hacen es comprar tres libros y prometerse que se los van a leer todos para estar listos para el examen. A los quince días ya están cansados y no quieren volver a saber de los libros, sin saber qué hacer. Hay que tener un plan de estudios y saber que ya tenemos fortalezas previas. Hay que recordar que se está preparando para un examen y la mejor forma es practicando de forma estratégica."
        )
    if post_idea is not None:
        st.session_state.post_idea_creation_user_id = user_id
        st.session_state.post_idea_creation_project_name = project_name
        save_post_idea_button = st.button("Save idea", on_click = post_idea_creation_execution)




def posting_posts_execution():
    os.write(1, '🥏 Executing posting_posts_execution \n'.encode('utf-8'))
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
        del st.session_state.posting_posts_selected_idea
        del st.session_state.posting_posts_selected_idea_id 

def post_redaction_generation():
    st.session_state.post_redaction_generation = ggg.gemini_general_prompt("Eres un experto en correccion de ortografia y redaccion", "Ahora soy un experto en redaccion y correccion de ortografia", f"Corrige la ortografia y muestrame unicamente el texto corregido: {st.session_state.posting_posts_selected_idea}")
    

def posting_posts(user_id, project_name):
    os.write(1, '🥏 Executing posting_posts \n'.encode('utf-8'))
    os.write(1, '- posting_posts: Showing form \n'.encode('utf-8'))
    count_active_ideas = uc.run_query_half_day(f"SELECT COUNT(*) AS count_active_ideas FROM `company-data-driven.{project_name}.daily_post_creation` WHERE posted IS NULL OR posted = 0;")[0].get("count_active_ideas")
    if count_active_ideas < 10:
        st.error(f"I need more ideas! I just have: {count_active_ideas}", icon = "🤬")
    else:
        st.success(f"Available ideas: {count_active_ideas}", icon = "😇")

    os.write(1, '- posting_posts: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.daily_post_creation` WHERE (posted IS NULL OR posted = 0)  ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "posting_posts_selected_idea",
            on_change = post_redaction_generation
        )

    if selected_idea is not None:
        st.session_state.posting_posts_user_id = user_id
        st.session_state.posting_posts_project_name = project_name
        st.session_state.posting_posts_selected_idea_id = ids[ideas.index(selected_idea)]
        posting_posts_button = st.button("Post published", on_click = posting_posts_execution)
        
    if 'post_redaction_generation' in st.session_state:
                st.write("---")
                st.write(st.session_state.post_redaction_generation + " #enfermeraenestadosunidos #enfermeriaenusa #enfermerosenestadosunidos")






def post_to_web_execution():
    os.write(1, '🥏 Executing post_to_web_execution \n'.encode('utf-8'))
    if 'post_to_web_selected_idea' in st.session_state:
        os.write(1, '- post_to_web_execution: Updating post\n'.encode('utf-8'))
        st.toast("Please wait", icon = "☺️")
        uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.post_to_web_project_name}.daily_post_creation` SET web_created = 1, web_created_date = CURRENT_DATE(), web_creator_user_id = {st.session_state.post_to_web_user_id} WHERE id = '{st.session_state.post_to_web_selected_idea_id}'")
        st.toast("Info saved!", icon = "👾")
        st.balloons()
        time.sleep(1)
        uc.run_query_half_day.clear()
        del st.session_state.post_to_web_user_id
        del st.session_state.post_to_web_project_name
        del st.session_state.post_to_web_selected_idea
        del st.session_state.post_to_web_selected_idea_id 
        del st.session_state.post_to_web_project_keyword

def post_to_web_generation():
    st.session_state.post_to_web_generation = ggg.gemini_general_prompt("Eres un experto en redaccion de contenidos extensos, hablas de forma informal desde una perspectiva personal, diciendo yo..", "Ahora soy un experto en redaccion extensa y detallada, hablo de forma informal desde una perspectiva personal, diciendo yo..", f"Redacta esto de una forma muy extensa: {st.session_state.post_to_web_project_keyword}: {st.session_state.post_to_web_selected_idea}")
    

def post_to_web(user_id, project_name, project_keyword):
    st.session_state.post_to_web_project_keyword = project_keyword
    os.write(1, '🥏 Executing post_to_web \n'.encode('utf-8'))
    os.write(1, '- post_to_web: Listing ideas \n'.encode('utf-8'))
    rows = uc.run_query_half_day(f"SELECT id, idea FROM `company-data-driven.{project_name}.daily_post_creation` WHERE (posted IS NOT NULL OR posted != 0) AND (web_created IS NULL OR web_created = 0)  ORDER BY creation_date;")
    ideas = []
    ids = []
    for row in rows:
        ideas.append(row.get('idea'))
        ids.append(row.get('id'))
    selected_idea = st.selectbox(
            label = "Select the idea",
            options = ideas,
            index = None,
            key= "post_to_web_selected_idea",
            on_change = post_to_web_generation
        )

    if selected_idea is not None:
        st.session_state.post_to_web_user_id = user_id
        st.session_state.post_to_web_project_name = project_name
        st.session_state.post_to_web_selected_idea_id = ids[ideas.index(selected_idea)]
        post_to_web_button = st.button("Post web created", on_click = post_to_web_execution)
        
    if 'post_to_web_generation' in st.session_state:
                st.write("---")
                st.write(st.session_state.post_to_web_generation)





def web_creation_guide():
    st.markdown('''duplicate page Easy Updates Manager, 
                imagify (e158d9b22db474a52c9ef7fa81afb14571d2fe7d)
                UpdraftPlus - Backup/Restore,  
                wordfence security wp rocket (activarle todo a esa gonorrea) 
                Yoast SEO, 
                thrivecart-pasarela de pagos 
                divi-crear paginas web (desactivarle las fuentes de google) 
                bloom- suscribirse optins 
                orbitapixel - plugins wordpress 
                google bard/chatgpt necesito el 4 para el seo 
                clipdrop 
                adobe color wheel recuerda subir todas las imagenes en formato webp seguir este video: https://www.youtube.com/watch?v=QCNEeVyRxBk&feature=youtu.be&fbclid=IwAR0mmAFlnZU3_VACC5OQaMOJKTCXiXi9KQNUiuxOwfmRlQMllqAbSJljHhs&ab_channel=OVDIVI tambien lo tengo descargado en mis archivos trabajo/startups/hosting instalar todo lo de arriba agregarle el ssl entrando al cpanel, a mi producto, buscando ssl y ahi agregarselo configurar uno por uno cada plugin hacer el video SEO y optimizar funnel a lo que marca revisar aca que mi pagina ande re bien: https://pagespeed.web.dev/ sobretodo me va a pedir que suba las imagenes en webp y que el wprocket haga lo de cache optimizar todo lo del hosting cpanel pillando que no se me dañe la web pero que puntue mejor en pagespeed la imagen del logito que sea 90x90 ----- en wp rocket no activar el lazy laod de las imagenes. luego ya aparece para agregarle el ssl y para instalarle el wordpress para agregarle la verificacion dns en search console, copiar el txt que me da search console y en el hosting ir al cpanel, a dominios seleccionar mi dominio, ir al dns y agregar un registro tipo txt donde el nombre es @ y el valor es lo que copie de search engine para encontrar mi sitemap y darselo al search engine, https://enfermeraenestadosunidos.com/page-sitemap.xml''')






def days_since_last_content(project_name):
    os.write(1, '🥏 Executing days_since_last_content \n'.encode('utf-8'))
    os.write(1, '- days_since_last_content: Counting days since last content\n'.encode('utf-8'))
    days_since_last_content_created = uc.run_query_1_h(f"SELECT DATE_DIFF(CURRENT_DATE(), MAX(created_video_date), DAY) AS days_since_last_content FROM `company-data-driven.{project_name}.content_creation`;")
    if len(days_since_last_content_created) < 1:
        st.warning("Waiting for data", icon = "😴")
    else:
        days_since = days_since_last_content_created[0].get("days_since_last_content")
        if days_since < 4:
            st.success(f"Days since last content (Video-web): {days_since}", icon = "😎")
        if days_since >= 4 and days_since < 6:
            st.warning(f"Days since last content (Video-web): {days_since}", icon = "🤨")
        if days_since >= 6:
            st.error(f"Days since last content (Video-web): {days_since}", icon = "🤬")

    os.write(1, '- days_since_last_content: Counting days since last post\n'.encode('utf-8'))
    st.write("test 0")
    days_since_last_post_created = uc.run_query_1_h(f"SELECT DATE_DIFF(CURRENT_DATE(), MAX(posted_date), DAY) AS days_since_last_post  FROM `company-data-driven.{project_name}.daily_post_creation`;")
    st.write("test")
    st.write(days_since_last_post_created)
    if len(days_since_last_post_created) < 1:
        st.warning("Waiting for data", icon = "😴")
    else:
        days_since_post = days_since_last_post_created[0].get("days_since_last_post")
        if days_since_post < 2:
            st.success(f"Days since last post: {days_since_post}", icon = "😎")
        if days_since_post >= 2 and days_since_post < 3:
            st.warning(f"Days since last post: {days_since_post}", icon = "🤨")
        if days_since_post >= 3:
            st.error(f"Days since last post: {days_since_post}", icon = "🤬")
        
        
        




def post_content_prompt():
    st.markdown('''
    Actua como IA, Continua la conversacion manteniendo un estilo de respuesta directo, en un texto corto de menos de 300 palabras, incisivo como un regaño y en un solo parrafo.
    USUARIO: Usar redes sociales para promocionar un negocio es bueno porque permite llegar a muchas personas, permiten segmentar y son más baratos #marketing #emprendimiento
    IA: Usar anuncios en redes sociales es importante para un emprendimiento por varias razones: 1. Las redes sociales cuentan con una gran cantidad de usuarios activos diariamente, lo que brinda la oportunidad de llegar a una audiencia amplia y diversa. Los anuncios en redes sociales permiten aprovechar este alcance masivo y llegar a un público objetivo específico. 2. Ofrecen herramientas de segmentación avanzadas que permiten dirigir los anuncios a personas con características demográficas, intereses y comportamientos específicos.  Esto significa que uno se puede enfocar en los usuarios que son más propensos a estar interesados en lo que ofrece su negocio. 3. En comparación con otros medios publicitarios tradicionales, los anuncios en redes sociales suelen ser más asequibles y ofrecen una mayor flexibilidad en cuanto al presupuesto.  Uno puede establecer sus propios límites de gasto y ajustar las campañas según los resultados obtenidos, lo cual permite controlar y optimizar el presupuesto. 4. Los anuncios en redes sociales no solo permiten mostrar lo que ofrece su negocio, sino también interactuar directamente con sus clientes potenciales.  Puede responder preguntas, resolver dudas, recibir comentarios y obtener una retroalimentación instantánea.  Esta interacción ayuda a construir relaciones sólidas con su audiencia y a mejorar su emprendimiento según las necesidades y opiniones de ellos. 5. Estas plataformas proporcionan herramientas de seguimiento y análisis detalladas que permiten evaluar el rendimiento de los anuncios en tiempo real.  Se puede obtener información sobre el alcance, la interacción, las conversiones y otros indicadores clave que ayudan a medir el retorno de la inversión y a tomar decisiones para optimizar las campañas. Si se tiene un emprendimiento de consumo masivo, es clave usar anuncios 🏪 Siempre que uno dice "hago esto porque me habría gustado que alguien lo hiciera por mí cuando era joven, etcétera", en realidad lo está haciendo porque gana plata o recibe algún tipo de beneficio, fin  (Solo que decirlo así suena más bonito)  #marketing #emprendimiento
    USUARIO: Hay que ser responsable de sus decisiones para mejorar su economia y vida dairia #marketing #finanzaspersonales
    IA: La vida de un adulto es el resultado de las decisiones (buenas y malas) que ha tomado, desde la carrera que estudió, el lugar donde trabaja, hasta la cantidad de hijos que tiene y el sitio donde vive y la gente que lo rodea. Incluso, la cantidad de dinero que tiene en su cuenta. Asuma la responsabilidad, fueron sus decisiones, no las de alguien más, es su resultado, ya está grande, no es resultado de las decisiones de sus papás. Asúmalo y mejore, nadie más lo hará por usted... #marketing #finanzaspersonales
    USUARIO: Hay que rodearse de personas que te incentiven a ser mejor #marketing #crecimientopersonal
    IA: Su entorno le afecta de forma directa. Si se rodea de gente que le dice que no emprenda y que busque un trabajo, difícilmente podrá emprender, esa presión le va a afectar. Igual con lo que sigue en redes sociales. Si se la pasa viendo noticias sobre todas las cosas que están mal, así mismo va a verlas. Uno es el resultado de su entorno... #marketing #crecimientopersonal
    USUARIO: La educacion financiera es muy importante #marketing #finanzaspersonales
    IA: Hay gente a la que el dinero no le alcanza, pero compran ropa, celular, cerveza, viajan y ahí sí les alcanza.  Eso es pura falta de educación financiera, solo saben gastarse lo poco que ganan y viven esperando que les llegue algo a fin de mes para cubrir todo lo que ya deben. Viven por encima de sus posibilidades y aparentando que todo está bien. Es el resultado de no haber aprendido nunca a administrar el dinero, ni preocuparse por su futuro por andar pensando solo en el presente, en el ya...  #marketing #finanzaspersonales
    USUARIO: Emprender es de moverse no de estudiar, de producir en lugar de consumir #emprender #startup #marketing
    IA: Hace unos días en los comentarios alguien decía que para emprender era súper importante la parte académica porque (según ella) se necesitaba saber Excel, inglés, finanzas y las habilidades sociales se aprendían en la academia... Yo le dije que eso sonaba más a un secretariado bilingüe. No me imagino a Arturo Calle hablando en inglés o a Epa Colombia siendo experta en Excel, bilingüe y presumiendo sus habilidades sociales aprendidas en la universidad... Para emprender la habilidad más importante se llama saber vender y las habilidades sociales que se requieren para emprender se aprenden, precisamente, vendiendo. La educación financiera no la enseñan en universidades, la enseñan quienes saben manejar el dinero, a través de sus libros (que escribe un redactor fantasma por ellos), charlas, videos y demás. Y lo de Excel desde que sepa sumar, restar, multiplicar y dividir o usar una calculadora, ya se defiende y el resto lo hace la secretaria bilingüe, contador o cualquier otro empleado...  #emprender #startup #marketing
    USUARIO:Lo mas importante de emprender es ejecutar y aveces no lo notamos #startup #marketing #emprendimiento
    IA: Uno suele emprender solo cuando está bajo presión... Es decir, cuando lo despiden, cuando se le acaban los ahorros, cuando se separa, cuando se va a vivir a un lugar nuevo y situaciones por el estilo. Esos momentos de crisis y desesperación hacen que uno tenga mucha más energía, creatividad y afán de hacer las cosas por puro instinto de supervivencia, lo cual se traduce en lo más importante: ejecutar 🎯  #startup #marketing #emprendimiento
    USUARIO: Automatizar y delegar es fundamental en el emprendimiento: #emprendimiento #startup #marketing
    IA: Entienda esto y su situación financiera mejorará: un negocio es un sistema. La que menos gana es la persona que trabaja para un sistema. Si una persona trabaja por su propia cuenta, se convierte en un sistema. Si una persona delega o automatiza sus tareas, se convierte en la dueña de un sistema y es la que más gana. El 90% de la población trabaja para un sistema o ella misma es el sistema. Su objetivo no es ese, su objetivo es crear y ser la dueña de un sistema...  #emprendimiento #startup #marketing
    USUARIO: No Emprender porque hay mucha competencia es una excusa #startup #marketing #emprendimiento
    IA: Es curioso cuando la gente pregunta si vale la pena poner una agencia de marketing digital, un puesto de empanadas o uno de hamburguesas porque ya están muy saturados. Mi ciela, saturado está el mercado laboral, solo el 10% de la población emprende... #startup #marketing #emprendimiento
    USUARIO: No es bueno renunciar a emprender por un mercado saturado #emprendimiento #marketing
    IA:Entre los temas que me sugirieron el martes alguien menciono qué opinaba sobre abrir una agencia de marketing digital y si ya estaba muy saturado.Lo primero es que todos los días se abren tiendas, panaderías, puestos de empanadas y puestos de hamburguesas, sin importar que sea algo saturado.Conozco barrios repletos de tiendas y panaderías y todas venden.El punto que yo creo importante es qué va a hacer usted en la agencia.¿Va a ser el empleado más importante? ¿Va a ser un autoempleado con ayudantes?Si la idea es esa, realmente no está montando un negocio, solo está siendo freelance en grupo.Eso es lo que le pasa a la mayoría, empiezan así y se quedan así. En las agencias grandes y conocidas, el dueño es el dueño, no es un empleado, delega.Ese es el punto más importante que se ocurre sobre ese tema.Cuando uno empieza un negocio, lo más probable es que le toque hacer de todo los 2 primeros años.Pero el objetivo de abrir un negocio no es ese, el objetivo es dejar de trabajar, precisamente porque el negocio trabaja por usted.Su negocio trabaja y le genera dinero, mientras usted se dedica a hacer lo que le gusta o piensa en el siguiente que va a crear.Su trabajo es ese, pensar. Delega o automatiza para no tener que hacer...#emprendimiento #marketing
    USUARIO: Dar valor es la clave para vender #Marketing
    IA: Si usted quiere que la gente le compre el servicio profesional o el contenido que ofrece, debe publicar contenido gratuito como si no hubiera mañana.El truco de eso consiste en darles tanto valor a las personas, a través de sus publicaciones, que sientan que le deben algo por todo lo que les ha aportado.Una vez llegue a ese punto, le van a devolver el favor... (comprando) #Marketing
    USUARIO: Para vender hay que darse a conocer #Marketing #ventas
    IA: Uno suele comprarle a alguien que ya conoce.Si quiere vender, primero tiene que darse a conocer...(Es lo que yo hago con cada publicación 6 veces al día, 180 veces al mes, 2.190 veces al año) #Marketing #ventas
    USUARIO: Hay que alejarse de las personas que culpan a los demas de su fracaso y no se hacen responsables
    IA: Aléjese de las personas que culpan a los demás de su propio fracaso o usted terminará siendo igual…
    USUARIO: Vi el video de los jefes que maltratan a sus empleados, mejor ocupense de sus proyectos, ejecuten. #startup
    IA: Tranquilas, no es necesario que me sigan etiquetando o enviando el video de unos jefes que le arrean la madre a un poco de gente en una oficina de Ibagué, ya lo vi... 💅🏻
    Por un lado, lo que pienso es que me vale verga.
    Por otra parte, también...
    Emprendan y ya, dejen de estar esperando que su jefe sea el papá que nunca tuvieron.
    Para mí, ser jefe o tener empleados es lo último que quiero en la vida, por eso amo Internet, la automatización y buscar cosas por ese lado, pa' no tener que estar lidiando con nadie.
    No me imagino que un día me graben diciéndoles "fórmense, hijueputas".
    Pero pensándolo bien... 🤔
    Fórmense, hijueputas, aprendan a crear algo propio, usen Internet pa' aprender a emprender, en vez de estar viendo videos que no les aportan ni chimba… #startup
    USUARIO: para emprender se necesita paciencia #startup
    IA: Cuando arranca su emprendimiento o está creando uno nuevo habrá muchos días en los que tendrá que pasar la prueba de ver a todo el mundo de rumba o de vacaciones, mientras usted solo trabaja.
    La recompensa viene después.. #startup
    USUARIO: A muchos les cuesta cambiar la mentalidad de empleado a emprendedor #startup
    IA: Ganarse la vida a través de Internet es algo sin sentido para las personas que fueron educadas creyendo que la única forma de vivir es yendo todos los días a meterse en un cubículo a fingir estar ocupada. #startup
    USUARIO: Emprender da tiempo libre #startup
    IA: Hace unos días, mientras explicaba que la idea de emprender y crear algo propio para delegarlo o automatizarlo es poder tener tiempo libre, alguien hizo un comentario un poco aterrador...Decía algo así como que si dejara de ser empleado, no sabría qué hacer con tanto tiempo libre.Yo respondí que me pasaba al contrario porque siempre quisiera tener más tiempo para jugar videojuegos, salir de rumba, ver series, películas, leer libros, conocer gente, salir a caminar, aprender cosas nuevas, etc.Para otra gente será más importante pasar tiempo con sus hijos, mascotas, pintar, dormir, hacer música, ejercicio, viajar o yo que sé, cualquier hobby.Al rato, la persona volvió a comentar que de tanto que llevaba trabajando, ya hasta había perdido los hobbies que tenía...En serio, emprendan y luego deleguen o automaticen ✌🏻 #startup
    Para los que vivimos de Internet, vivir metidos en una oficina es lo que no tiene sentido 🤷🏼‍♂️
    USUARIO: Los talleres que enseno no son por certificados, sino para que aprendan a ganar plata #startup
    IA: Es muy triste cuando alguien me pregunta si al tomar mis talleres recibirá un certificado. No, campeón, mis talleres no se hicieron para crear más subordinados.Son para aprender y emprender, no para que te suban el sueldo…  #startup
    USUARIO: hay que automatizar y reinvertir #Marketing #ventas
    IA: Cuando uno emprende un negocio en Internet llega un momento en el que ya puede delegar o automatizar la parte operativa.Es decir, la parte operativa del negocio se atiende sola, ya sea a través de gente o de herramientas.En mi caso, esa parte operativa la realiza el sitio web, toda la información y el proceso de compra/entrega está ahí y funciona sin mí.Eso me permite poder atender la cantidad de gente que sea, a la hora que sea, el día que sea, mientras yo uso mi tiempo para otra cosa.Antes, cuando empecé, lo hacía todo yo. Es decir, yo era el sistema.Al reinvertir, ya pude pagar un sistema que hace las cosas por mí.Antes me tocaba usar WhatsApp y atender a la gente, tomar el pedido, uno por uno, todo el día, todos los días, todo era manual.Incluso, antes de eso, me tocaba hacer los talleres en vivo, uno por uno, con cada persona. Eso no es escalable y requiere todo mi tiempo.Hoy no, hoy mi tiempo lo uso para hacer lo que me gusta y para pensar, en lugar de operar.Pensar en cómo puedo optimizar cada proceso automatizado y pensar en qué es lo siguiente que puedo crear, siguiendo el mismo método.Hay gente que se la pasa todo el día en WhatsApp atendiendo, cuando eso podría hacerlo un subordinado o un sitio web.Y no me refiero a un chatbot, me refiero a que su sitio debe ser capaz de vender porque ahí está toda la información y a través de él se hace todo el proceso, para eso es, es una tienda que se atiende sola. Incluso la logística se puede delegar.El problema de los que no logran llegar a ese punto es que se gastan todo lo que ganan para impresionar a gente que ni siquiera les importa, en lugar de invertirlo en salirse de la parte operativa… #Marketing #ventas
    USUARIO: Se debe publicar contenido de valor constantemente para crear un publico y luego promocionar mis anuncios a ese publico caliente #market
    IA: Yo publico y publico pendejadas útiles (contenido de valor) todos los días para luego agarrar a toda esa gente que interactuó con él y mostrarle anuncios de mis talleres. Así de simple llevo viviendo de esto desde el 2018 y si usted dejara esa mentalidad de empleado podría hacer lo mismo con lo que debe hacer market
    USUARIO: No se asusten con el proceso de homologar la enfermeria en USA, sean valientes y consistentes
    IA: Muchos enfermeros que quieren venir a ejercer su profesión en Estados Unidos dan el primer paso y se quedan ahí, se asustan al ver que tienen que pagar una certificación de 100 dólares o pagar 150 dólares por traducir unos documentos. En la mayoría de los casos, todo lo que invierten lo recuperan después de 1 o 2 meses de trabajar acá y, en el fondo, lo saben. Los que dan el paso y son valientes saben que le apuestan al retorno garantizado en términos de calidad profesional, salarial y de vida para ellos y sus familias. Es la mentalidad con que nos educaron.
    #enfermeriaenusa #enfermeria #enfermeraenestadosunidos
    USUARIO: Para venirse como enfermero a USA no hay trucos ni trampas
    IA: Todo este proceso de homologar la enfermería en Estados Unidos es como una maratón; los que lo logran son los que saben que esto no termina en una semana, que son dos años de retos. Los que están finalizando el proceso asumieron el reto del inglés, el reto de pasar el NCLEX y todos los retos de trámites, esperas. Pero aquí están, ganando hasta 10 veces lo que ganaban antes y con su familia como residentes americanos. Si ustedes no asumen el reto, nadie más lo va a hacer por ustedes. #enfermeraenestadosunidos #enfermeriaenusa #enfermeria
    USUARIO: 
    IA:
    ''')
