import streamlit as st
import pandas as pd
import time
import datetime

import utils.user_credentials as uc

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
            "Demuestra que sirve",
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


        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(text_input_1)

