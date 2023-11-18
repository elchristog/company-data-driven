import streamlit as st
import pandas as pd
import pandas_gbq
from datetime import date
from dateutil.relativedelta import relativedelta
from io import BytesIO
import time
from googleapiclient import discovery
from pyexcelerate import Workbook
from google_auth_oauthlib.flow import Flow
# import functions as fc
from streamlit_raw_echarts import st_echarts

# https://github.com/ViniciusStanula/Search-Console-API/tree/main

import utils.user_credentials as uc

# Define o período inicial e final padrão para o slider
date = date.today()
data_final = date - relativedelta(days=2)
data_inicial = date - relativedelta(months=16)
data_padrao = date - relativedelta(months=1)

# Convert secrets from the TOML file to strings
clientSecret = st.secrets["clientSecret"]
clientId = st.secrets["clientId"]
redirectUri = 'https://company-data-driven.streamlit.app'
href = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={}&redirect_uri={}&scope=https://www.googleapis.com/auth/webmasters.readonly&access_type=offline&prompt=consent".format(clientId, redirectUri)
credentials = {
    "installed": {
        "client_id": clientId,
        "client_secret": clientSecret,
        "redirect_uris": [],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
    }
}

flow = Flow.from_client_config(
    credentials,
    scopes=["https://www.googleapis.com/auth/webmasters.readonly"],
    redirect_uri=redirectUri,
)
auth_url, _ = flow.authorization_url(prompt="consent")
    
def button_callback():
    try:
        st.session_state.my_token_received = True
        code = st.experimental_get_query_params()["code"][0]
        st.session_state.my_token_input = code
    except KeyError or ValueError:
        st.error("⚠️ The parameter 'code' was not found in the URL. Please log in.")

def check_input_url(input_url):
    # Verificar se a entrada contém "https://" ou "http://"
    if "https://" in input_url or "http://" in input_url:
        return input_url
    # Caso contrário, assume que é um domínio e adiciona "sc-domain:"
    return f'sc-domain:{input_url}'

@st.cache_resource(show_spinner=False)
def get_webproperty(token):
    flow.fetch_token(code=token)
    credentials = flow.credentials
    service = discovery.build(
        serviceName="webmasters",
        version="v3",
        credentials=credentials,
        cache_discovery=False,
    )

    return service

@st.cache_data(show_spinner=False)
# Definir a função para consultar e processar dados
def get_data(property_url, dimensions, startDate, endDate, url_filter=None, url_operator=None,
            palavra_filter=None, palavra_operator=None):
    service = get_webproperty(st.session_state.my_token_input)

    # Criar uma lista vazia para armazenar as linhas recuperadas da resposta
    data = []
    
    # Definir o limite de linhas desejado para 300.000 linhas
    row_limit = 300000
    
    # Definir o texto de progresso a ser exibido acima da barra de progresso
    progress_text = "Retrieving Metrics. Please Wait. 🐈"

    # Criar o widget de barra de progresso usando o Streamlit
    my_bar = st.progress(0, text=progress_text)

    # Inicializar a variável 'startRow' para rastrear a linha de início de cada solicitação
    startRow = 0

    while startRow == 0 or startRow % 25000 == 0 and startRow < row_limit:
        # Construir o corpo da solicitação com as variáveis especificadas
        request = {
            'startDate': startDate,
            'endDate': endDate,
            'dimensions': dimensions,
            'rowLimit': 25000,
            'startRow': startRow
        }

        if url_filter and url_operator:
            url_dimension_filter = {
                'dimension': 'PAGE',
                'operator': url_filter,
                'expression': url_operator
            }
            request['dimensionFilterGroups'] = [{'filters': [url_dimension_filter]}]

        if palavra_filter and palavra_operator:
            palavra_dimension_filter = {
                'dimension': 'QUERY',
                'operator': palavra_filter,
                'expression': palavra_operator
            }
            if 'dimensionFilterGroups' in request:
                request['dimensionFilterGroups'].append({'filters': [palavra_dimension_filter]})
            else:
                request['dimensionFilterGroups'] = [{'filters': [palavra_dimension_filter]}]

        # Armazenar a resposta da API do Google Search Console
        response = service.searchanalytics().query(siteUrl=property_url, body=request).execute()

        # Obter e atualizar as linhas
        rows = response.get('rows', [])
        startRow = startRow + len(rows)

        # Estender a lista de dados com as linhas
        data.extend(rows)
        
        # Calcular a porcentagem de progresso
        progress_percent = min((startRow / row_limit) * 100, 100)

        # Converter a porcentagem de progresso para um valor entre 0.0 e 1.0
        progress_value = progress_percent / 100.0

        # Atualizar a barra de progresso com o progresso atual
        my_bar.progress(progress_value, text=progress_text)
    
    # Criar um DataFrame a partir da lista de dados
    if dimensions == ['page', 'query']:
        df = pd.DataFrame([
            {
                'Page': row['keys'][0],
                'Keyword': row['keys'][1],
                'Clicks': row['clicks'],
                'Impressions': row['impressions'],
                'CTR': row['ctr'],
                'Position': row['position']
            } for row in data
        ])
    elif dimensions == ['query', 'page']:
        df = pd.DataFrame([
            {
                'Keyword': row['keys'][0],
                'Page': row['keys'][1],
                'Clicks': row['clicks'],
                'Impressions': row['impressions'],
                'CTR': row['ctr'],
                'Position': row['position']
            } for row in data
        ])
    elif dimensions == ['query']:
        df = pd.DataFrame([
            {
                'Keyword': row['keys'][0],
                'Clicks': row['clicks'],
                'Impressions': row['impressions'],
                'CTR': row['ctr'],
                'Position': row['position']
            } for row in data
        ])
    elif dimensions == ['page']:
        df = pd.DataFrame([
            {
                'Page': row['keys'][0],
                'Clicks': row['clicks'],
                'Impressions': row['impressions'],
                'CTR': row['ctr'],
                'Position': row['position']
            } for row in data
        ])
        
    # Atualizar a barra de progresso para 100% para mostrar que o processamento de dados está completo
    my_bar.progress(1.0, text="Processing is now finished 😸")

    # Aguardar por uma curta duração para exibir a mensagem "Processamento de Dados Completo"
    time.sleep(2)

    # Limpar a barra de progresso para removê-la da interface do aplicativo
    my_bar.empty()
        
    return df

@st.cache_data(show_spinner=False)
def get_data_date(property_url, startDate, endDate, url_filter=None, url_operator=None,
                palavra_filter=None, palavra_operator=None):
        service = get_webproperty(st.session_state.my_token_input)

        # Criar uma lista vazia para armazenar as linhas recuperadas da resposta
        data = []
        
        # Definir o limite de linhas desejado para 300.000 linhas
        row_limit = 1000
        
        # Definir o texto de progresso a ser exibido acima da barra de progresso
        progress_text = "Retrieving Metrics. Please Wait. 🐈"

        # Criar o widget de barra de progresso usando o Streamlit
        my_bar = st.progress(0, text=progress_text)

        # Inicializar a variável 'startRow' para rastrear a linha de início de cada solicitação
        startRow = 0

        while startRow == 0 or startRow % 25000 == 0 and startRow < row_limit:
            # Construir o corpo da solicitação com as variáveis especificadas
            request = {
                'startDate': startDate,
                'endDate': endDate,
                'dimensions': 'date',
                'rowLimit': 25000,
                'startRow': startRow
            }

            if url_filter and url_operator:
                url_dimension_filter = {
                    'dimension': 'PAGE',
                    'operator': url_filter,
                    'expression': url_operator
                }
                request['dimensionFilterGroups'] = [{'filters': [url_dimension_filter]}]

            if palavra_filter and palavra_operator:
                palavra_dimension_filter = {
                    'dimension': 'QUERY',
                    'operator': palavra_filter,
                    'expression': palavra_operator
                }
                if 'dimensionFilterGroups' in request:
                    request['dimensionFilterGroups'].append({'filters': [palavra_dimension_filter]})
                else:
                    request['dimensionFilterGroups'] = [{'filters': [palavra_dimension_filter]}]

            # Armazenar a resposta da API do Google Search Console
            response = service.searchanalytics().query(siteUrl=property_url, body=request).execute()

            # Obter e atualizar as linhas
            rows = response.get('rows', [])
            startRow = startRow + len(rows)

            # Estender a lista de dados com as linhas
            data.extend(rows)
            
            # Calcular a porcentagem de progresso
            progress_percent = min((startRow / row_limit) * 100, 100)

            # Converter a porcentagem de progresso para um valor entre 0.0 e 1.0
            progress_value = progress_percent / 100.0

            # Atualizar a barra de progresso com o progresso atual
            my_bar.progress(progress_value, text=progress_text)
        
        df_date = pd.DataFrame([
            {
                'Date': row['keys'][0],
                'Clicks': row['clicks'],
                'Impressions': row['impressions'],
                'CTR': row['ctr'],
                'Position': row['position']
            } for row in data
        ])
            
        # Atualizar a barra de progresso para 100% para mostrar que o processamento de dados está completo
        my_bar.progress(1.0, text="Processing is now finished. 😸")

        # Aguardar por uma curta duração para exibir a mensagem "Processamento de Dados Completo"
        time.sleep(2)

        # Limpar a barra de progresso para removê-la da interface do aplicativo
        my_bar.empty()
            
        return df_date

@st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def criar_grafico_echarts(df_grouped):
    # Formate a coluna 'CTR' do DataFrame
    df_grouped['CTR'] = df_grouped['CTR'].apply(lambda ctr: f"{ctr * 100:.2f}")
    df_grouped['Position'] = df_grouped['Position'].apply(lambda pos: round(pos, 2))

    # Translated ECharts options
    options = {
        "xAxis": {
            "type": "category",
            "data": df_grouped['Date'].tolist(),
            "axisLabel": {
                "formatter": "{value}"
            }
        },
        "yAxis": {"type": "value", "name": ""},
        "grid": {
            "right": 20,
            "left": 65,
            "top": 45,
            "bottom": 50,
        },
        "legend": {
            "show": True,
            "top": "top",
            "align": "auto",
            "selected": {  # Definindo a seleção inicial das séries
                "Clicks": True,         # A série "Clicks" está selecionada
                "Impressions": True,    # A série "Impressions" está selecionada
                "CTR": False,           # A série "CTR" não está selecionada
                "Position": False       # A série "Position" não está selecionada
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "Clicks",
                "data": df_grouped['Clicks'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#8be9fd"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "Impressions",
                "data": df_grouped['Impressions'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#ffb86c"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "CTR",
                "data": df_grouped['CTR'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#50fa7b"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
{
    "type": "line",
    "name": "Position",
    "data": df_grouped['Position'].tolist(),
    "smooth": True,
    "lineStyle": {"width": 2.4, "color": "#ff79c6"},
    "showSymbol": False,  # Remova os marcadores de dados para esta série
    "yAxisIndex": 1,  # Indica que esta série usará o segundo eixo Y
    "axisLabel": {
        "show": False  # Oculta os rótulos do eixo Y para esta série
    }
},
        ],

        "yAxis": [
            {"type": "value", "name": ""},
            {"type": "value", "inverse": True, "show": False},  # Segundo eixo Y com a opção "inverse"
        ],
        "backgroundColor": "#f5f5f7",
        "color": ["#8be9fd", "#ffb86c", "#50fa7b", "#ff79c6"],
    }

    # Exibir o gráfico de linha do ECharts usando st_echarts
    st_echarts(option=options, theme='chalk', height=400, width='100%')
    




def createPage(project_url_clean):
    # Inserindo informações de contatos na segunda coluna
    if "my_token_input" not in st.session_state:
        st.session_state["my_token_input"] = ""
    if "my_token_received" not in st.session_state:
        st.session_state["my_token_received"] = False
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None
    if 'domain' not in st.session_state:
        st.session_state.domain = None
    if 'dataframeData' not in st.session_state:
        st.session_state.dataframeData = None
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
               
    st.markdown("----")
    link_style = (
        "text-decoration: none;"
        "color: #FFF;"
        "padding: 8px 20px;"
        "border-radius: 4px;"
        "background-color: #DD4B39;"
        "font-size: 16px;"
    )

    url = href

    st.markdown('1 - Log in to your Google account:')
    st.markdown(f'<a href="{url}" target="_blank" style="{link_style}">'
            f'<img src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/14082/icon_google.png" alt="Google" style="vertical-align: middle; margin-right: 10px;">'
            f'Login With Google'
            f'</a>', unsafe_allow_html=True)

    st.markdown('2 - Click the Button to grant API access:')
    submit_button = st.button(
        label="Grant API access", on_click=button_callback
    )

    st.markdown('This is your OAuth token:')
    code = st.text_input(
            "",
            key="my_token_input",
            label_visibility="collapsed",
        )

    # Obtém a URL para consulta
    url = project_url_clean
    property_url = check_input_url(url)
    
    st.session_state.domain = property_url

    # Seleciona as métricas desejadas
    metricas = st.selectbox(
        'Metrics:',
        ("Keywords", "Pages", "Pages per Keyword", "Keywords per Page"), help='Specify the metric you are interested in filtering for.'
    )

    # Define as dimensões de acordo com as métricas selecionadas
    if metricas == "Keywords per Page":
        dimensions = ['page', 'query']
    elif metricas == "Pages per Keyword":
        dimensions = ['query', 'page']
    elif metricas == "Keywords":
        dimensions = ['query']
    elif metricas == "Pages":
        dimensions = ['page']
        
    # Define valores padrão para as variáveis de filtro
    url_filter = None
    url_operator = None
    palavra_filter = None
    palavra_operator = None    
    
    # Seleciona o período de data desejado
    day = st.date_input(
        "Time Range:",
        (data_padrao, data_final),
        min_value=data_inicial,
        max_value=data_final,
        format="DD/MM/YYYY",
        help='The available time range is the same as what is available in Google Search Console. DD/MM/YYYY Format'
    )
            
    # clicks
    df_date = get_data_date(property_url, day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
            url_filter=url_filter, url_operator=url_operator,
            palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    st.write(df_date)
    st.table(df_date)
    df_grouped = df_date.groupby('Date').agg({
            'Clicks': 'sum',
            'Impressions': 'sum',
            'CTR': 'mean',
            'Position': 'mean'
        }).reset_index()
    Clicks = df_date['Clicks'].sum()
    Impressions = df_date['Impressions'].sum()
    ctr_mean = df_date['CTR'].mean()
    pos_mean = df_date['Position'].mean()
    met1, met2, met3, met4 = st.columns(4)
    with met1:
        st.metric('Clicks:', f'{Clicks:,}')
    with met2:
        st.metric('Impressions:', f'{Impressions:,}')
    with met3:
        st.metric('CTR:', f'{ctr_mean * 100:.2f}%')
    with met4:
        st.metric('Position:', f'{pos_mean:.1f}')
    with st.container():
        criar_grafico_echarts(df_grouped)


    # pages
    df = get_data(property_url, ['page'], day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
    url_filter=url_filter, url_operator=url_operator,
    palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    st.table(df)          
    # keywords
    df = get_data(property_url, ['query'], day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
    url_filter=url_filter, url_operator=url_operator,
    palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    st.table(df)
    # keywords per page
    df = get_data(property_url, ['page', 'query'], day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
    url_filter=url_filter, url_operator=url_operator,
    palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    st.table(df)


    return True