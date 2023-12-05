import streamlit as st
import pandas as pd
import time
import datetime
import re

import utils.user_credentials as uc
import utils.chat_gpt_gestor as cgptg

# callbacks https://discuss.streamlit.io/t/click-twice-on-button-for-changing-state/45633/2

def save_new_content(project_name, user_id):
    st.session_state.text_input_1 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_1)
    st.session_state.text_input_2 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_2)
    st.session_state.text_input_3 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_3)
    st.session_state.text_input_4 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_4)
    st.session_state.text_input_5 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_5)
    st.session_state.text_input_6 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_6)
    st.session_state.text_input_7 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_7)
    st.session_state.text_input_8 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_8)
    st.session_state.text_input_9 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_9)
    st.session_state.text_input_10 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_10)
    st.session_state.text_input_11 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_11)
    st.session_state.text_input_12 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_12)
    st.session_state.text_input_13 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_13)
    st.session_state.text_input_14 = re.sub('[^a-zA-Z0-9 \n\.]', ' ', st.session_state.text_input_14)

    st.session_state.text_input_1 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_1)
    st.session_state.text_input_2 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_2)
    st.session_state.text_input_3 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_3)
    st.session_state.text_input_4 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_4)
    st.session_state.text_input_5 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_5)
    st.session_state.text_input_6 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_6)
    st.session_state.text_input_7 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_7)
    st.session_state.text_input_8 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_8)
    st.session_state.text_input_9 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_9)
    st.session_state.text_input_10 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_10)
    st.session_state.text_input_11 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_11)
    st.session_state.text_input_12 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_12)
    st.session_state.text_input_13 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_13)
    st.session_state.text_input_14 = re.sub(r"[\\\'\"']", " ", st.session_state.text_input_14)
    
    
    st.toast("Please wait", icon = "☺️")
    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.effective_communication_content` (id, creation_date, creator_user_id, keyword, main_idea, why_1, why_2, why_3, how_1, how_2, how_3, experiment_1, experiment_2, experiment_3, relevant_content, checklist, call_to_action, created_content) VALUES (GENERATE_UUID(), CURRENT_DATE(), {user_id}, '{st.session_state.text_input_1}', '{st.session_state.text_input_2}', '{st.session_state.text_input_3}', '{st.session_state.text_input_4}', '{st.session_state.text_input_5}', '{st.session_state.text_input_6}', '{st.session_state.text_input_7}', '{st.session_state.text_input_8}', '{st.session_state.text_input_9}', '{st.session_state.text_input_10}', '{st.session_state.text_input_11}', '{st.session_state.text_input_12}', '{st.session_state.text_input_13}', '{st.session_state.text_input_14}' ,0);")
    time.sleep(5)
    st.toast("Content saved!", icon = "👾")
    st.balloons()


def content_creation_guide_effective_communication_storytelling(user_id, project_name):
    st.warning("Do not use line breaks, double or single quotes, to prevent errors write your answers in a local text editor and copy here without any line breaks, double or single quotes", icon = "🙈")
    with st.form("comm_eff_storytelling_form", clear_on_submit = True):
        text_input_1 = st.text_area(
            "Keyword del articulo",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Obtener la licencia de enfermería en Estados Unidos',
            help = 'No se debe poner cualquier cosa, debe ser lo que entrego el ideador',
            key = 'text_input_1'
        )

        text_input_2 = st.text_area(
            "Idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Si quieren obtener la licencia en USA deben aplicar los 10 pasos: Trámite de documentos CGFNS, Inscripción ante la Junta de Enfermería, Preparación NCLEX, 	Preparación de inglés y Visa Screen. Aplicar el modelo incrementara los ingresos en 13%',
            help = 'Es una frase que persuada a la persona para que haga lo que quiero que haga, esta orientada al verbo hacer y al beneficio de hacerlo.',
            key = 'text_input_2'
        )

        text_input_3 = st.text_area(
            "Por que de la primer parte de la idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Por que aplicar 10 pasos? Por que son los mismos pasos que yo tuve que vivir cuando me converti en enfermera en este pais y son los que requiere el gobierno de los estados unidos, pueden revisarse en esta web:',
            help = 'Parte la idea principal en 3 partes y contesta por que de cada una, de forma completa y detallada',
            key = 'text_input_3'
        )

        text_input_4 = st.text_area(
            "Por que de la segunda parte de la idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'por que Trámite de documentos CGFNS, Inscripción ante la Junta de Enfermería, Preparación NCLEX? Porque los estados unidos requieren que cualquier enfermero extranjero que quiera trabajar en los estados unidos debe demostrar que sus estudios equivalen a una enfermera registrada que estudio en el pais, y para eso se deben legalizar y comprobar una serie de documentos y pruebas que demuestren que si es asi',
            help = 'Parte la idea principal en 3 partes y contesta por que de cada una, de forma completa y detallada',
            key = 'text_input_4'
        )

        text_input_5 = st.text_area(
            "Por que de la tercera parte de la idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'por que Preparación de inglés y Visa Screen? porque ese documento es el que expide EU diciendo que efectivamente tu cumples con todos los requisitos de valides de tus estudios, conocimientos en salud y por suepuesto el ingles, y sin ese documento no te dejan tramitar la visa',
            help = 'Parte la idea principal en 3 partes y contesta por que de cada una, de forma completa y detallada',
            key = 'text_input_5'
        )

        text_input_6 = st.text_area(
            "Como de la primera parte de la idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Como se aplican los 10 pasos? Con asesoria, nosotros asesoramos a enfermeros que se quieren ir a estados unidos durante todo el proceso hasta que lleguen al pais y se adapten a la vida, se hace entrando al link de whatsapp y me escriben y citamos la primera reunion',
            help = 'explica como se hace',
            key = 'text_input_6'
        )

        text_input_7 = st.text_area(
            "Como de la segunda parte de la idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'como se hace Trámite de documentos CGFNS, Inscripción ante la Junta de Enfermería, Preparación NCLEX? para la aprte de cgfns pueden entrar a la pagina web de ellos y este es el link, aca explican como se hace por ejemplo vean que aca dice que se necesita esto y esto otro, para la parte del nclex les recomiendo el libro de archer y el de pearson y tambien nuestra asesoria porque los rpeparamos y probamos',
            help = 'Explica como se hace',
            key = 'text_input_7'
        )

        text_input_8 = st.text_area(
            "Como de la tercera parte de la idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Como se hace Preparación de inglés y Visa Screen? hay tres examenes posibles ielts, toefl y el pti primero deben pensar muy bien cual elegir porque aunque hay unos ams faciles que otros no totdos son validos en todos los estados por ejemplo para una maestria que muchas veces las pagan les exigen esto y esto',
            help = 'Explica como se hace',
            key = 'text_input_8'
        )

        text_input_9 = st.text_area(
            "Haga experimentos y tablas comparativas 1",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Comparemos obtener la licencia por nuestra cuenta contra una agencia, miren la agencia los obliga a quedarse en ciertos estados no dodne quiera, ademas tatatta',
            help = 'Debe ser la parte mas larga y detallada: Probemos opcion1 y opcion2, miren lo que da cuando hacemos 1 y lo que da cuando hacemos 2, en una tabla comparativa se ve asi',
            key = 'text_input_9'
        )

        text_input_10 = st.text_area(
            "Haga experimentos y tablas comparativas 2",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Comparemos obtener la licencia por nuestra cuenta contra una agencia, miren la agencia los obliga a quedarse en ciertos estados no dodne quiera, ademas tatatta',
            help = 'Debe ser la parte mas larga y detallada: Probemos opcion1 y opcion2, miren lo que da cuando hacemos 1 y lo que da cuando hacemos 2, en una tabla comparativa se ve asi',
            key = 'text_input_10'
        )

        text_input_11 = st.text_area(
            "Haga experimentos y tablas comparativas 3",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Comparemos obtener la licencia por nuestra cuenta contra una agencia, miren la agencia los obliga a quedarse en ciertos estados no dodne quiera, ademas tatatta',
            help = 'Debe ser la parte mas larga y detallada: Probemos opcion1 y opcion2, miren lo que da cuando hacemos 1 y lo que da cuando hacemos 2, en una tabla comparativa se ve asi',
            key = 'text_input_11'
        )

        text_input_12 = st.text_area(
            "Copia y pega lo mas relevante de lo que escriben los top 3 competidores de esto",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Para trabajar de manera legal en Estados Unidos, además de contar con un título académico de tu país de origen, necesitarás aprobar el examen que realiza la Licenciatura del Consejo Nacional (NCLEX). Una vez que apruebes este examen obtendrás una licencia que te permitirá ejercer la profesión de enfermera',
            help = 'Solo trae lo relevante',
            key = 'text_input_12'
        )

        text_input_13 = st.text_area(
            "Checklist",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'por eso recuerda 1, buscar un programa de acompanamiento, 2 hacer el Trámite de documentos, 3 inscripción ante la Junta de Enfermería...',
            help = 'Resume en un checklists los mensajes principales',
            key = 'text_input_13'
        )

        text_input_14 = st.text_area(
            "llamado a la accion con pasos a seguir",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Suscribete para seguir aprendiendo conmigo y si quieres iniciar el programa dale al enlace de whatsapp',
            help = '',
            key = 'text_input_14'
        )


        submitted = st.form_submit_button("Submit", on_click = save_new_content, args = [project_name, user_id])





def seo_ideation_execution():
    st.toast('Generating Ideas:', icon="🤖")  
    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{st.session_state.project_name}.keyword_seo_ideation_log` (id, creation_date, creator_user_id, ideas) VALUES (GENERATE_UUID(), CURRENT_DATE(), {st.session_state.user_id}, '{st.session_state.text_input_1}')")  
    keyword_research = uc.run_query_10_s(f"SELECT * FROM `company-data-driven.{st.session_state.project_name}.keywords`;")        
    longtail_questions = uc.run_query_10_s(f"SELECT * FROM `company-data-driven.{st.session_state.project_name}.keyword_common_questions`;")        
    created_content = uc.run_query_10_s(f"SELECT page AS page, SUM(clicks) AS clicks, SUM(impressions) AS impressions, AVG(ctr) AS ctr  FROM `company-data-driven.{st.session_state.project_name}.traffic_analytics_web_pages` GROUP BY page;")  
    st.toast("Keyword research", icon = "☺️")
    time.sleep(5)
    all_ideas = uc.run_query_10_s(f"SELECT ideas FROM `company-data-driven.{st.session_state.project_name}.keyword_seo_ideation_log`;")  
    answer = cgptg.prompt_ia("Eres un experto en SEO, especialmente en ideacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.project_keyword} [/KEYWORD] [KEYWORD_RESEARCH] {keyword_research} [/KEYWORD_RESEARCH] [LONGTAIL_QUESTIONS] {longtail_questions} [/LONGTAIL_QUESTIONS] [IDEASEXTRA] {all_ideas} [/IDEASEXTRA] [YACREADO] {created_content} [/YACREADO] [INSTRUCTION] Analiza las metricas, Dame ideas de 6 articulos que posicionen aclarando el titulo que debe tener el articulo y la keyword que quieres posicionar en cada uno, evita hablar sobre articulos que ya he creado [YACREADO], asegura que 2 de los articulos vengan de los [LONGTAIL_QUESTIONS] o de los [IDEASEXTRA]:[/INSTRUCTION]", 600)
    st.toast("IA working", icon = "☺️")
    st.session_state.answer = answer
    st.write(answer)
    






def seo_ideation(project_name, project_keyword, user_id, role_id):
    with st.form("seo_ideation_form", clear_on_submit = True):
        text_input_1 = st.text_area(
            "Ideas extras de keywords",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'pasos para ser enfermera latina en usa, comparacion de agencias de enfermeria, cuanto gana una enfermera en texas',
            help = 'This ideas will be saved an priorized with the time'
        )

        st.session_state.project_name = project_name
        st.session_state.project_keyword = project_keyword
        st.session_state.user_id = user_id
        st.session_state.role_id = role_id
        st.session_state.text_input_1 = text_input_1
        
        submitted = st.form_submit_button("Generate ideas", on_click = seo_ideation_execution)
    if 'answer' in st.session_state:
        st.download_button('Download answer', st.session_state.answer, file_name = 'content_ideas.txt')

    
    if role_id == 1:
        st.write("---")
        st.header("Keyword research steps")
        st.write("Keywords Everywere suscripcion anual con el plan bronce, son 15 dolares al anio mantener la extension apagada y solo prenderla una vez por cada proyecto busco mi keyword en google  creo un google sheets en la carpeta del emprendimiento con columnas(keyword, volume, cpc, cpm) se llama keywords creo un segundo google sheets llamado keyword_common_questions con la columna question y ahi voy poniendo las pregunats que buscan 1- descargo las related keywords y las  pongo en el archivo, asegurarse de respetar las columnas 2- lo mismo con las Long-Tail Keywords y si hay ams pues a todas  3- le doy click a find long tail keywords, espero que se genere y las descargo todas  4- copio cada una de las preguntas que la gente suele hacer , luego las abro todas y copio todas las nuevas 4- copio los titulos de las 3 primeras paginas a las questions antepongo (que, como, donde, por que, quien, cuanto, comprar, contratar, el mejor, cual es, y todo el funnel del usuario) a la keyword, repito la busqueda eligiendo la primera apcion que google me ofrece (llevandome esa opcion a las questions, si no ofrece nada pues buscar asi) , a descarga de los 3 archivos y la copiada de todas las preguntas al final eliminar duplicados de ambos archivos, y del de keywords mantener todo ordenando de mayor a menor cpc leer en bigquery como tablas con los nombres cambiados: keywords_res y  keyword_common_questions_res, recordar ponerlas como desde drive y luego google sheets, el nombre de la tabla, schema auto detect,  y en ehaders row to skip poner 1 luego hacer un query para leer la tabla, darle a save results, bigquery table, ahi si ponerle el nombre que es y eliminar la primera tabla ")




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
                adobe color wheel recuerda subir todas las imagenes en formato webp seguir este video: https://www.youtube.com/watch?v=QCNEeVyRxBk&feature=youtu.be&fbclid=IwAR0mmAFlnZU3_VACC5OQaMOJKTCXiXi9KQNUiuxOwfmRlQMllqAbSJljHhs&ab_channel=OVDIVI tambien lo tengo descargado en mis archivos trabajo/startups/hosting instalar todo lo de arriba agregarle el ssl entrando al cpanel, a mi producto, buscando ssl y ahi agregarselo configurar uno por uno cada plugin hacer el video SEO y optimizar funnel a lo que marca revisar aca que mi pagina ande re bien: https://pagespeed.web.dev/ sobretodo me va a pedir que suba las imagenes en webp y que el wprocket haga lo de cache optimizar todo lo del hosting cpanel pillando que no se me dañe la web pero que puntue mejor en pagespeed la imagen del logito que sea 90x90 ----- para agregar un nuevo sitio web, ir al cpanel, a mi producto, a dominios y agregar el dominio que compre, y ponerle una carpeta raiz con su nombre. luego ya aparece para agregarle el ssl y para instalarle el wordpress para agregarle la verificacion dns en search console, copiar el txt que me da search console y en el hosting ir al cpanel, a dominios seleccionar mi dominio, ir al dns y agregar un registro tipo txt donde el nombre es @ y el valor es lo que copie de search engine para encontrar mi sitemap y darselo al search engine, https://enfermeraenestadosunidos.com/page-sitemap.xml''')




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

    article = cgptg.prompt_ia("Eres un experto en SEO, especialmente en generacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {st.session_state.selected_keyword} [/KEYWORD] [ARTICLE] {selected_content_main_idea} [/ARTICLE] [INSTRUCTION] Reescribe este articulo de una forma mas extensa y detallada posible, no omitas los ejemplos quiero que los muestres, presenta todo en formato de codigo html [/INSTRUCTION]", 600)
    st.toast("Saving article", icon = "☺️")
    st.session_state.article = article
    st.write(article)
    
    time.sleep(5)
    st.balloons()
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

        seo_writing_button = st.form_submit_button("Generate content", on_click = seo_writing_execution) 

    if 'article' in st.session_state:
        st.download_button('Download article', st.session_state.article, file_name = 'ia_article.txt')
        
        

