import streamlit as st
import pandas as pd
import time
import datetime
import re
import ast

import utils.user_credentials as uc
import utils.g_gemini_gestor as ggg

# callbacks https://discuss.streamlit.io/t/click-twice-on-button-for-changing-state/45633/2


def seo_ideation_execution(project_name, project_keyword, user_id, role_id, text_input_1):
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
    available_contents = uc.run_query_30_m(f"SELECT COUNT(*) AS available_contents FROM `company-data-driven.{project_name}.content_creation` WHERE created_video IS NULL OR created_video = 0;")[0].get('available_contents') 
    if available_contents < 10:
        st.error(f"I need more contents! I just have: {available_contents}", icon = "🤬")
    else:
        st.success(f"Available contents: {available_contents}", icon = "😇")
        
    with st.form("seo_ideation_form", clear_on_submit = True):
        text_input_1 = st.text_area(
            "Ideas extras de keywords",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'pasos para ser enfermera latina en usa, comparacion de agencias de enfermeria, cuanto gana una enfermera en texas',
            help = 'This ideas will be saved an priorized with the time',
            key = 'text_input_1'
        )

        submitted = st.form_submit_button("Generate ideas", on_click = seo_ideation_execution, args = [project_name, project_keyword, user_id, role_id, text_input_1])
    if 'answer' in st.session_state:
        st.download_button('Download answer', st.session_state.answer, file_name = 'content_ideas.txt')

    
    if role_id == 1:
        st.write("---")
        st.header("Keyword research steps")
        st.write("Keywords Everywere suscripcion anual con el plan bronce, son 15 dolares al anio mantener la extension apagada y solo prenderla una vez por cada proyecto busco mi keyword en google  creo un google sheets en la carpeta del emprendimiento con columnas(keyword, volume, cpc, cpm) se llama keywords creo un segundo google sheets llamado keyword_common_questions con la columna question y ahi voy poniendo las pregunats que buscan 1- descargo las related keywords y las  pongo en el archivo, asegurarse de respetar las columnas 2- lo mismo con las Long-Tail Keywords y si hay ams pues a todas  3- le doy click a find long tail keywords, espero que se genere y las descargo todas  4- copio cada una de las preguntas que la gente suele hacer , luego las abro todas y copio todas las nuevas 4- copio los titulos de las 3 primeras paginas a las questions antepongo (que, como, donde, por que, quien, cuanto, comprar, contratar, el mejor, cual es, y todo el funnel del usuario) a la keyword, repito la busqueda eligiendo la primera apcion que google me ofrece (llevandome esa opcion a las questions, si no ofrece nada pues buscar asi) , a descarga de los 3 archivos y la copiada de todas las preguntas al final eliminar duplicados de ambos archivos, y del de keywords mantener todo ordenando de mayor a menor cpc leer en bigquery como tablas con los nombres cambiados: keywords_res y  keyword_common_questions_res, recordar ponerlas como desde drive y luego google sheets, el nombre de la tabla, schema auto detect,  y en ehaders row to skip poner 1 luego hacer un query para leer la tabla, darle a save results, bigquery table, ahi si ponerle el nombre que es y eliminar la primera tabla ")




def video_creation_execution(project_name, user_id):
    st.toast("Please wait", icon = "☺️")
    # uc.run_query_insert_update(f"")
    st.toast("Content saved!", icon = "👾")
    st.balloons()
    time.sleep(5)
    uc.run_query_30_m.clear()

def selected_idea_session_creation(selected_idea):
    st.session_state.video_creation_selected_idea = selected_idea
    st.toast(st.session_state.video_creation_selected_idea)

def video_creation(user_id, project_name):
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
            key= "ideas",
            on_change = selected_idea_session_creation(selected_idea)
        )
    if selected_idea is not None:
        selected_idea_id = ids[ideas.index(selected_idea)]
    
    



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




def seo_writing_execution():
    st.toast("IA working!", icon = "🍩")
    selected_content_id = st.session_state.ids[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_main_idea = st.session_state.main_ideas[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_why_1 = st.session_state.why_1s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_why_2 = st.session_state.why_2s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_why_3 = st.session_state.why_3s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_how_1 = st.session_state.how_1s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_how_2 = st.session_state.how_2s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_how_3 = st.session_state.how_3s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_experiment_1 = st.session_state.experiment_1s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_experiment_2 = st.session_state.experiment_2s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_experiment_3 = st.session_state.experiment_3s[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_relevant_content = st.session_state.relevant_contents[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_checklist = st.session_state.checklists[st.session_state.keywords.index(st.session_state.selected_keyword)]
    selected_content_call_to_action = st.session_state.call_to_actions[st.session_state.keywords.index(st.session_state.selected_keyword)]

    article_part_1 = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_checklist} {selected_content_main_idea} [/ARTICLE] [INSTRUCTION] Reescribe este articulo de una forma mas extensa y detallada posible, no omitas ni una parte de lo escrito, como eres un experto SEO vas a posicionar el articulo incluyendo la keyword y todas las distintas formas (keywords longtail) que una persona puede buscar este contenido, asi como de multiples ejemplos y tablas comparativas, no entregues conclusiones ni explicaciones de lo que hiciste, unicamente el articulo usando las etiquetas <h1> <h2> <h3> <p style='text-align: justify;'> <strong> <ul>  <li> <a> <table> <tr> segun corresponda[/INSTRUCTION]", 4000)

    article_part_1_extras = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_checklist} {selected_content_main_idea} [/ARTICLE] [INSTRUCTION] Genera 2 ejemplos que en lugar de resumir logren aclarar dudas especificas y muy utiles que pueden surgir al leer esto. tambien genera 1 tabla comparativa en HTML que aclare y resuma todo, como eres un experto SEO vas a posicionar el articulo incluyendo la keyword y todas las distintas formas (keywords longtail) que una persona puede buscar este contenido, no entregues conclusiones ni explicaciones de lo que hiciste, unicamente el articulo usando las etiquetas <h1> <h2> <h3> <p style='text-align: justify;'> <strong> <ul>  <li> <a> <table> <tr> segun corresponda[/INSTRUCTION]", 4000)

    article_part_2 = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_why_1} {selected_content_how_1} {selected_content_why_2} {selected_content_how_2} {selected_content_why_3} {selected_content_how_3} [/ARTICLE] [INSTRUCTION] Reescribe este articulo de una forma mas extensa y detallada posible, no omitas ni una parte de lo escrito, como eres un experto SEO vas a posicionar el articulo incluyendo la keyword y todas las distintas formas (keywords longtail) que una persona puede buscar este contenido, asi como de multiples ejemplos y tablas comparativas, no entregues conclusiones ni explicaciones de lo que hiciste, unicamente el articulo usando las etiquetas <h1> <h2> <h3> <p style='text-align: justify;'> <strong> <ul>  <li> <a> <table> <tr> segun corresponda[/INSTRUCTION]", 4000)

    article_part_2_extras = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_why_1} {selected_content_how_1} {selected_content_why_2} {selected_content_how_2} {selected_content_why_3} {selected_content_how_3} [/ARTICLE] [INSTRUCTION] Genera 2 ejemplos que en lugar de resumir logren aclarar dudas especificas y muy utiles que pueden surgir al leer esto. tambien genera 1 tabla comparativa en HTML que aclare y resuma todo, como eres un experto SEO vas a posicionar el articulo incluyendo la keyword y todas las distintas formas (keywords longtail) que una persona puede buscar este contenido, no entregues conclusiones ni explicaciones de lo que hiciste, unicamente el articulo usando las etiquetas <h1> <h2> <h3> <p style='text-align: justify;'> <strong> <ul>  <li> <a> <table> <tr> segun corresponda[/INSTRUCTION]", 4000)

    article_part_3 = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_relevant_content} {selected_content_experiment_1} {selected_content_experiment_2} {selected_content_experiment_1} CONCLUSION {selected_content_main_idea} {selected_content_checklist} {selected_content_call_to_action} [/ARTICLE] [INSTRUCTION] Reescribe este articulo de una forma mas extensa y detallada posible, no omitas ni una parte de lo escrito, como eres un experto SEO vas a posicionar el articulo incluyendo la keyword y todas las distintas formas (keywords longtail) que una persona puede buscar este contenido, asi como de multiples ejemplos y tablas comparativas, no entregues conclusiones ni explicaciones de lo que hiciste, unicamente el articulo usando las etiquetas <h1> <h2> <h3> <p style='text-align: justify;'> <strong> <ul>  <li> <a> <table> <tr> segun corresponda[/INSTRUCTION]", 4000)

    article_part_3_extras = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_relevant_content} {selected_content_experiment_1} {selected_content_experiment_2} {selected_content_experiment_1} CONCLUSION {selected_content_main_idea} {selected_content_checklist} {selected_content_call_to_action} [/ARTICLE] [INSTRUCTION] Genera 2 ejemplos que en lugar de resumir logren aclarar dudas especificas y muy utiles que pueden surgir al leer esto. tambien genera 1 tabla comparativa en HTML que aclare y resuma todo, como eres un experto SEO vas a posicionar el articulo incluyendo la keyword y todas las distintas formas (keywords longtail) que una persona puede buscar este contenido, no entregues conclusiones ni explicaciones de lo que hiciste, unicamente el articulo usando las etiquetas <h1> <h2> <h3> <p style='text-align: justify;'> <strong> <ul>  <li> <a> <table> <tr> segun corresponda[/INSTRUCTION]", 4000)

    article_attributes = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] [SEARCH INTENTION] {selected_content_checklist} [/SEARCH INTENTION] {selected_content_main_idea} {selected_content_why_1} {selected_content_how_1} {selected_content_why_2} {selected_content_how_2} {selected_content_why_3} {selected_content_how_3} {selected_content_relevant_content} {selected_content_experiment_1} {selected_content_experiment_2} {selected_content_experiment_1} [/ARTICLE]  [INSTRUCTION] Genera los siguientes contenidos sobre el articulo y presentalos de esa misma forma anteponiendo la etiqueta: [WEB TITLE] titulo del articulo, debe contener la palabra clave, debe generar interes de leer mas y usar mayusculas selectivas y emojis, debe tener maximo 57 caracteres. [WEB META DESCRIPTION] Debe resumir en menos de 140 caracteres lo mas importante de la [SEARCH INTENTION] e incluir la palabra clave, asegurate de que no sea algo al estilo de (descubre como lograr...) lo que quiero es algo al estilo de (La respuesta es .. y ....). [IMAGE NAME] el nombre que debe tener el archivo de la imagen del articulo, debe incluir la palabra clave [IMAGE ALTERNATIVE TEXT] Un texto alternativo para la imagen, debe incluir la palabra clave [IMAGE CAPTION] un caption para la imagen, debe incluir la palabra clave [IMAGE DESCRIPTION] UNA DESCRIPCION PARA LA IMAGEN, debe incluir la palabra clave [YOUTUBE TITLE] titulo del video, debe contener la palabra clave, debe generar interes de leer mas y usar mayusculas selectivas y emojis, debe tener maximo 57 caracteres. [YOUTUBE DESCRIPTION] Una descripcion extensa de 2000 caracteres que incluiya la palabra clave y resuma el articulo [YOUTUBE TAGS] 20 tags cortos basados en palabras clave y presentados en forma de palabra clave sin usar #, y 10 tags largos basados en keywords longtail del articulo presentados de la misma forma, todos estos tags presentados como separados por comas [/INSTRUCTION]", 4000)

    article_insights = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] [SEARCH INTENTION] {selected_content_checklist} [/SEARCH INTENTION] {selected_content_main_idea} {selected_content_why_1} {selected_content_how_1} {selected_content_why_2} {selected_content_how_2} {selected_content_why_3} {selected_content_how_3} {selected_content_relevant_content} {selected_content_experiment_1} {selected_content_experiment_2} {selected_content_experiment_1} [/ARTICLE]  [INSTRUCTION] Escribe los 5 principales insights del articulo de forma detallada, bien explicada, resolutiva y que llame la atencion, expresalos en forma de ideas y no de resumen ya que no quiero algo por el estilo de (El artículo destaca...) lo que si quiero es algo al estilo de (Yo creo que lo mejor es..., o algo como: Yo publico y publico pendejadas útiles (contenido de valor) todos los días para luego agarrar a toda esa gente que interactuó con él y mostrarle anuncios de mis talleres. Así de simple llevo viviendo de esto desde el 2018 y si usted dejara esa mentalidad de empleado podría hacer lo mismo con lo que debe hacer market o al estilo de: Es muy triste cuando alguien me pregunta si al tomar mis talleres recibirá un certificado. No, campeón, mis talleres no se hicieron para crear más subordinados.Son para aprender y emprender, no para que te suban el sueldo…  #startup o al estilo de Ganarse la vida a través de Internet es algo sin sentido para las personas que fueron educadas creyendo que la única forma de vivir es yendo todos los días a meterse en un cubículo a fingir estar ocupada. #startup o al estilo de Cuando arranca su emprendimiento o está creando uno nuevo habrá muchos días en los que tendrá que pasar la prueba de ver a todo el mundo de rumba o de vacaciones, mientras usted solo trabaja. o al estilo de Aléjese de las personas que culpan a los demás de su propio fracaso o usted terminará siendo igual…). [/INSTRUCTION]", 4000)

    uc.run_query_insert_update(f"UPDATE `company-data-driven.{st.session_state.project_name}.effective_communication_content` SET created_content = 1 WHERE id = '{selected_content_id}'")

    
    st.toast("Saving article", icon = "☺️")
    st.session_state.article = f"[KEYWORD] {st.session_state.selected_keyword}" + " ----Recuerda agregar 3 links internos, 3 links externos, anclar el video a la web, agregar comentario fijado al video, comaprtir el video en redes, indexar la web en search console, publicar los contenidos y compartir el pantallazo en otras redes---- [ARTICLE] First add here the [WEB META DESCRIPTION] as the first text. Asegurate que el titulo, meta description, descripcion de youtubecontengan la keyword" + article_part_1 + article_part_1_extras + article_part_2 + article_part_2_extras + article_part_3 + article_part_3_extras + " [EXTRAS] " + article_attributes + " [POSTS] " + article_insights

    st.write(st.session_state.article)
    st.balloons()
    time.sleep(5)
    uc.run_query_30_m.clear()




def seo_writing(project_name, user_id, role_id):
    non_created_contents = uc.run_query_30_m(f"SELECT * FROM `company-data-driven.{project_name}.effective_communication_content` WHERE created_content = 0 ORDER BY creation_date;")
    ids = []
    keywords = []
    main_ideas = []
    why_1s = []
    why_2s = []
    why_3s = []
    how_1s = []
    how_2s = []
    how_3s = []
    experiment_1s = []
    experiment_2s = []
    experiment_3s = []
    relevant_contents = []
    checklists = []
    call_to_actions = []
    
    for row in non_created_contents:
        ids.append(row.get('id'))
        keywords.append(row.get('keyword'))
        main_ideas.append(row.get('main_idea'))
        why_1s.append(row.get('why_1'))
        why_2s.append(row.get('why_2'))
        why_3s.append(row.get('why_3'))
        how_1s.append(row.get('how_1'))
        how_2s.append(row.get('how_2'))
        how_3s.append(row.get('how_3'))
        experiment_1s.append(row.get('experiment_1'))
        experiment_2s.append(row.get('experiment_2'))
        experiment_3s.append(row.get('experiment_3'))
        relevant_contents.append(row.get('relevant_content'))
        checklists.append(row.get('checklist'))
        call_to_actions.append(row.get('call_to_action'))

    with st.form("seo_writing_form", clear_on_submit = True):
        selected_keyword = st.selectbox(
            label = "Select one article idea",
            options = keywords,
            index = None,
            key = 'selected_keyword'
        )

        st.session_state.ids = ids
        st.session_state.keywords = keywords
        st.session_state.main_ideas = main_ideas
        st.session_state.why_1s = why_1s
        st.session_state.why_2s = why_2s
        st.session_state.why_3s = why_3s
        st.session_state.how_1s = how_1s
        st.session_state.how_2s = how_2s
        st.session_state.how_3s = how_3s
        st.session_state.experiment_1s = experiment_1s
        st.session_state.experiment_2s = experiment_2s
        st.session_state.experiment_3s = experiment_3s
        st.session_state.relevant_contents = relevant_contents
        st.session_state.checklists = checklists
        st.session_state.call_to_actions = call_to_actions
        st.session_state.project_name = project_name
        st.session_state.user_id = user_id
        st.session_state.role_id = role_id
        

        seo_writing_button = st.form_submit_button("Generate content", on_click = seo_writing_execution) 

    if 'article' in st.session_state:
        st.download_button('Download article', st.session_state.article, file_name = 'ia_article.txt')





def days_since_last_content(project_name):
    days_since_last_content_created = uc.run_query_1_h(f"SELECT DATE_DIFF(CURRENT_DATE(), MAX(creation_date), DAY) AS days_since_last_content FROM `company-data-driven.{project_name}.effective_communication_content`;")
    if len(days_since_last_content_created) < 1:
        st.warning("Waiting for data", icon = "😴")
    else:
        days_since = days_since_last_content_created[0].get("days_since_last_content")
        if days_since < 5:
            st.success(f"Days since last content: {days_since}", icon = "😎")
        if days_since >= 5 and days_since < 8:
            st.warning(f"Days since last content: {days_since} (Video, YT banner, Content creation guide)", icon = "🤨")
        if days_since >= 8:
            st.error(f"Days since last content: {days_since} (Video, YT banner, Content creation guide)", icon = "🤬")
        
        
        




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
