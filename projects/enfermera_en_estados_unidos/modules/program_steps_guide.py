import streamlit as st

# https://share.streamlit.io/streamlit/emoji-shortcodes

def program_steps_guide(user_actual_step_id):
    if user_actual_step_id == 1:
        st.success(f"### Inicio del programa")
        st.write(f"¡Bienvenido/a al Programa de Enfermería en Estados Unidos! En esta sección, te proporcionaremos actualizaciones continuas con toda la información necesaria para que tengas claridad sobre las tareas y la manera en que deben llevarse a cabo. Esto te permitirá alcanzar con éxito tu objetivo de convertirte en enfermero/a en Estados Unidos.")
        st.write(f"A medida que progreses en cada etapa, actualizaremos la información y los listados que necesitas para avanzar. En este primer paso de inicio del programa, te familiarizarás con los pasos generales y también con esta herramienta que te ayudará a gestionar tu progreso, tareas, metas, práctica del NCLEX, recursos y todo lo demás que necesites.")
        with st.expander(":trophy: Plataforma"):
            st.write(f"Familiarízate con la plataforma, probando cada uno de los módulos y comprendiendo cómo debe ser tu herramienta de trabajo diario. Practica para el NCLEX y realiza un seguimiento de tu progreso.")
        with st.expander(":pouch: Recursos"):
            st.write(f"Descarga los recursos y familiarízate con tu espacio en la nube para acceder a los recursos y grabaciones de nuestras sesiones.")
        with st.expander(":weight_lifter: Avanzar al paso 2"):
            st.write(f"Ahora que has iniciado el programa, nos estamos preparando para avanzar al paso 2. Para esto, procederemos con la firma del contrato y la aceptación de los acuerdos del programa.")


    # if user_actual_step_id == 2:
        st.success(f"### Trámite de documentos")
        st.write(f"¡Bienvenido/a al Programa de Enfermería en Estados Unidos! En esta sección, te proporcionaremos actualizaciones continuas con toda la información necesaria para que tengas claridad sobre las tareas y la manera en que deben llevarse a cabo. Esto te permitirá alcanzar con éxito tu objetivo de convertirte en enfermero/a en Estados Unidos.")
        tab1, tab2, tab3 = st.tabs(["CGFNS", "New York"])
        with tab1:
            st.header("CGFNS")
            with st.expander(":pouch: Recursos"):
                st.write(f"fsdf")
