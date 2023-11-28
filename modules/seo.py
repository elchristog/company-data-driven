import streamlit as st
import pandas as pd
import time
import datetime

import utils.user_credentials as uc
import utils.chat_gpt_gestor as cgptg

def content_creation_guide_effective_communication_storytelling():
    with st.form("comm_eff_storytelling_form", clear_on_submit = True):

        text_input_1 = st.text_area(
            "Que va a lograr tu usuario con este contenido?",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Hola soy XX y en este video te voy a ensenar a como hacer que la gente haga click en tu video',
            help = 'ayudigna'
        )

        text_input_2 = st.text_area(
            "Por que?",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Por que de nada sirve que ahgas videos muy buenos si nadie los ve',
            help = 'ayudigna'
        )

        text_input_3 = st.text_area(
            "Demuestra que sirve, resuelve la intencion de busqueda",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Pero antes que eso te voy a mostrar los ingresos que estoy teniendo, pues bien estoy ganando 5 mil dolares al mes mira',
            help = 'ayudigna'
        )

        text_input_4 = st.text_area(
            "Suscribete en momento de alta atencion relativa",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Asi que recuerda suscribirte',
            help = 'ayudigna'
        )

        text_input_4 = st.text_area(
            "Explicar el que y darle contexto",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Para que hagan mas click debes mejorqar el ctr, es decir la cantidad de veces que hacen click en tu video por cada vez que lo muestra, mira te lo muestro en la plataforma, por ejemplo si tienes un ctr del 6 porciento significa que el 6 porciento de las personas que buscaron te eligieron',
            help = 'ayudigna'
        )

        text_input_5 = st.text_area(
            "Por que es importante esto?",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Tu que crees que youtube va a mostrar mas, un video que cada vez que youtube lo muestra nadie le da click o uno que cada que lo muestra todo el mundo hace click',
            help = 'ayudigna'
        )

        text_input_6 = st.text_area(
            "Idea principal",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Si consigues mejorar el ctr y en este video te voy a mostrar la estrategia para lograrlo, entonces vas a lograr que youtube te recomiende',
            help = 'ayudigna'
        )

        text_input_7 = st.text_area(
            "Resolver la intencion de busqueda",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Para que te den mas click mueve estas 2 cosas: la miniatura y el titulo del video',
            help = 'ayudigna'
        )

        text_input_8 = st.text_area(
            "por que del primer como",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Sabes cual es la funcion de la miniatura? llamar la atencion, no es explicar de que trata el video y es ahi donde muchos fallan, si generas expectativa entonces van a dar click, porque la gente esta pasando cosas y solo para en lo que le llama la atebncion, si tu miniatura es igual al resto de miniaturas del mundo nadie te va a preferir, ejemplo, mira lo que hace mr beast',
            help = 'Fijate que aca habla de que hay que llamar la atencion pero no explica como se hacer para llamar la atencion, eso es lo que se vende marcos, caras, emojis, calor distinto al resto....'
        )

        text_input_9 = st.text_area(
            "Ejemplo del primer como",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'mira lo que hace mr beast, esta es su miniatura, la ha cambiado 3 veces',
            help = 'Fijate que aca habla de que hay que llamar la atencion pero no explica como se hacer para llamar la atencion, eso es lo que se vende marcos, caras, emojis, calor distinto al resto....'
        )

        text_input_10 = st.text_area(
            "por que del segundo como",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Y cual es la funcion del titulo? Describir de que va el video generando una respuesta emocional en el usuario, si describe de que va el video pero genera curiosidad',
            help = 'Lo mismo, habla del que y no del como, si hay que mejorar el titulo pero el como es mayuscilas selectivas, diferenciarse del resto, emojis, palabra clave...'
        )

        text_input_11 = st.text_area(
            "Ejemplo del segundo como",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Mira lo que usa mr beast, explamaciones, mayusculas....',
            help = 'Lo mismo, habla del que y no del como, si hay que mejorar el titulo pero el como es mayuscilas selectivas, diferenciarse del resto, emojis, palabra clave...'
        )

        text_input_12 = st.text_area(
            "Conclusiones checklist",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Si consigues mejorar el ctr  entonces vas a lograr que youtube te recomiende y eso se hace logrando que las miniaturas llamen ams la atebncion y que los titulos generen curiosidad',
            help = 'Lo mismo, habla del que y no del como, si hay que mejorar el titulo pero el como es mayuscilas selectivas, diferenciarse del resto, emojis, palabra clave...'
        )

        text_input_13 = st.text_area(
            "CliffHanger",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'De esa manera vas a mejorar mucho tus clicks, pero mira lop que estoy logrando, para conseguir esto necesitaras tambien conoceer el tercer metodo para que youtube te recomiende y eso lo veremos en el siguiente video',
            help = 'Lo mismo, habla del que y no del como, si hay que mejorar el titulo pero el como es mayuscilas selectivas, diferenciarse del resto, emojis, palabra clave...'
        )


        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(text_input_1)





def seo_ideation(project_name, project_keyword):
    with st.form("seo_ideation_form", clear_on_submit = True):
        st.write(project_keyword)
        text_input_1 = st.text_area(
            "Ideas extras de keywords",
            label_visibility = 'visible',
            disabled = False,
            placeholder = 'Hola soy XX y en este video te voy a ensenar a como hacer que la gente haga click en tu video',
            help = 'ayudigna'
        )

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success('Generating Ideas:', icon="🤖")    
            keyword_research = uc.run_query_10_s(f"SELECT * FROM `company-data-driven.{project_name}.keywords`;")        
            longtail_questions = uc.run_query_10_s(f"SELECT * FROM `company-data-driven.{project_name}.keyword_common_questions`;")        
            created_content = uc.run_query_10_s(f"SELECT page AS page, SUM(clicks) AS clicks, SUM(impressions) AS impressions, AVG(ctr) AS ctr  FROM `company-data-driven.{project_name}.traffic_analytics_web_pages` GROUP BY page;")        
            answer = cgptg.prompt_ia("Eres un experto en SEO, especialmente en ideacion de articulos web que posicionen rapido con palabras clave long tail", f"[KEYWORD] {project_keyword} [/KEYWORD] [KEYWORD_RESEARCH] {keyword_research} [/KEYWORD_RESEARCH] [LONGTAIL_QUESTIONS] {longtail_questions} [/LONGTAIL_QUESTIONS] [IDEASEXTRA] {text_input_1} [/IDEASEXTRA] [YACREADO] {created_content} [/YACREADO] [INSTRUCTION] Analiza las metricas, Dame ideas de 6 articulos que posicionen aclarando el titulo que debe tener el articulo y la keyword que quieres posicionar en cada uno, evita hablar sobre articulos que ya he creado [YACREADO], asegura que 2 de los articulos vengan de los [LONGTAIL_QUESTIONS] o de los [IDEASEXTRA]:[/INSTRUCTION]", 600)
            st.write(answer)


