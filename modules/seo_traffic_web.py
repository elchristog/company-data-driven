import streamlit as st
import pandas as pd
import time
import datetime


from datetime import date
from dateutil.relativedelta import relativedelta
from googleapiclient import discovery
from google_auth_oauthlib.flow import Flow
from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc

# https://github.com/ViniciusStanula/Search-Console-API/tree/main
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

date = date.today()
data_final = date - relativedelta(days=2)
data_inicial = date - relativedelta(months=16)
data_padrao = date - relativedelta(months=1)

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
    if "https://" in input_url or "http://" in input_url:
        return input_url
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



# @st.cache_data(show_spinner=False)
def get_data(property_url, dimensions, startDate, endDate, url_filter=None, url_operator=None,
            palavra_filter=None, palavra_operator=None):
    service = get_webproperty(st.session_state.my_token_input)
    data = []
    row_limit = 300000
    progress_text = "Retrieving Metrics. Please Wait. 🐈"
    my_bar = st.progress(0, text=progress_text)
    startRow = 0
    while startRow == 0 or startRow % 25000 == 0 and startRow < row_limit:
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
        response = service.searchanalytics().query(siteUrl=property_url, body=request).execute()
        rows = response.get('rows', [])
        startRow = startRow + len(rows)
        data.extend(rows)
        progress_percent = min((startRow / row_limit) * 100, 100)
        progress_value = progress_percent / 100.0
        my_bar.progress(progress_value, text=progress_text)
    
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
    my_bar.progress(1.0, text="Processing is now finished 😸")
    time.sleep(2)
    my_bar.empty()
    return df



# @st.cache_data(show_spinner=False)
def get_data_date(property_url, startDate, endDate, url_filter=None, url_operator=None,
                palavra_filter=None, palavra_operator=None):
        service = get_webproperty(st.session_state.my_token_input)
        data = []
        row_limit = 1000
        progress_text = "Retrieving Metrics. Please Wait. 🐈"
        my_bar = st.progress(0, text=progress_text)
        startRow = 0
        while startRow == 0 or startRow % 25000 == 0 and startRow < row_limit:
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
            response = service.searchanalytics().query(siteUrl=property_url, body=request).execute()
            rows = response.get('rows', [])
            startRow = startRow + len(rows)
            data.extend(rows)
            progress_percent = min((startRow / row_limit) * 100, 100)
            progress_value = progress_percent / 100.0
            my_bar.progress(progress_value, text=progress_text)
        df_clicks = pd.DataFrame([
            {
                'Date': row['keys'][0],
                'Clicks': row['clicks'],
                'Impressions': row['impressions'],
                'CTR': row['ctr'],
                'Position': row['position']
            } for row in data
        ])
        my_bar.progress(1.0, text="Processing is now finished. 😸")
        time.sleep(2)
        my_bar.empty()
        return df_clicks



# @st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def plot_echarts(df_grouped):
    df_grouped['ctr'] = df_grouped['ctr'].apply(lambda ctr: f"{ctr * 100:.2f}")
    df_grouped['position'] = df_grouped['position'].apply(lambda pos: round(pos, 2))
    df_grouped['date'] = df_grouped['date'].astype(str)  # Convert 'date' to string

    options = {
        "xAxis": {
            "type": "category",
            "data": df_grouped['date'].tolist(),
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
                "clicks": True,         # A série "Clicks" está selecionada
                "impressions": True,    # A série "Impressions" está selecionada
                "ctr": False,           # A série "CTR" não está selecionada
                "position": False       # A série "Position" não está selecionada
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "clicks",
                "data": df_grouped['clicks'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "impressions",
                "data": df_grouped['impressions'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "ctr",
                "data": df_grouped['ctr'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BF3F34"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "position",
                "data": df_grouped['position'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BFB5B4"},
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
        "backgroundColor": "#ffffff",
        "color": ["#A6785D", "#394A59", "#BF3F34", "#BFB5B4"],
    }

    st_echarts(option=options, theme='chalk', height=400, width='100%')
    



def get_data_save_to_bq(role_id, project_name, project_url_clean):
    if role_id == 1:
        dates_in_table = uc.run_query_6_h(f"SELECT DATE_DIFF(CURRENT_DATE(), MAX(date), DAY) - 2 AS days_last_update, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AS min_date_first_query, DATE_ADD(MAX(date), INTERVAL 1 DAY) AS min_date_next_query, DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY) AS max_date_next_query FROM `company-data-driven.{project_name}.traffic_analytics_web_clicks`;")
        days_last_update = dates_in_table[0].get("days_last_update")
        min_date_first_query = dates_in_table[0].get("min_date_first_query")
        min_date_next_query = dates_in_table[0].get("min_date_next_query")
        max_date_next_query = dates_in_table[0].get("max_date_next_query")

        if days_last_update is None or days_last_update > 0:
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
            
            st.write("### Update your web data")
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
            get_data_button = st.button("Get data")
            if get_data_button:
                url = project_url_clean
                property_url = check_input_url(url)
                st.session_state.domain = property_url

                url_filter = None
                url_operator = None
                palavra_filter = None
                palavra_operator = None   
                
                if days_last_update is None:
                    starting_date_to_pages = min_date_first_query.strftime("%Y-%m-%d")
                    ending_date_to_pages = max_date_next_query.strftime("%Y-%m-%d")
                elif days_last_update > 0:
                    starting_date_to_pages = min_date_next_query.strftime("%Y-%m-%d")
                    ending_date_to_pages = max_date_next_query.strftime("%Y-%m-%d")

                df_clicks = get_data_date(property_url, starting_date_to_pages, ending_date_to_pages,
                        url_filter=url_filter, url_operator=url_operator,
                        palavra_filter=palavra_filter, palavra_operator=palavra_operator)
                df_pages = get_data(property_url, ['page'], starting_date_to_pages, ending_date_to_pages,
                        url_filter=url_filter, url_operator=url_operator,
                        palavra_filter=palavra_filter, palavra_operator=palavra_operator)
                st.table(df_clicks)
                st.table(df_pages)
                today = datetime.date.today()
                today_str = today.strftime("%Y-%m-%d")
                for index, row in df_clicks.iterrows():
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_web_clicks` (date, clicks, impressions, ctr, position) VALUES ('{row['Date']}', {row['Clicks']}, {row['Impressions']}, {row['CTR']}, {row['Position']});")
                for index, row in df_pages.iterrows():
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_web_pages` (id, ctreation_date, start_query_date, end_query_date, page, clicks, impressions, ctr, position) VALUES (GENERATE_UUID(), '{today_str}', '{starting_date_to_pages}', '{ending_date_to_pages}', '{row['Page']}', {row['Clicks']}, {row['Impressions']}, {row['CTR']}, {row['Position']});")

                st.info("Updating, please wait", icon = "☺️")
                time.sleep(10)
                st.rerun()

    # # pages
    # df = get_data(property_url, ['page'], day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
    # url_filter=url_filter, url_operator=url_operator,
    # palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    # st.table(df)          
    # # keywords
    # df = get_data(property_url, ['query'], day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
    # url_filter=url_filter, url_operator=url_operator,
    # palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    # st.table(df)
    # # keywords per page
    # df = get_data(property_url, ['page', 'query'], day[0].strftime("%Y-%m-%d"), day[1].strftime("%Y-%m-%d"),
    # url_filter=url_filter, url_operator=url_operator,
    # palavra_filter=palavra_filter, palavra_operator=palavra_operator)
    # st.table(df)

    return True




def show_web_metrics(project_name):
    st.write("### 	:earth_americas: Web traffic")
    df = pd.DataFrame(uc.run_query_3_h(f"SELECT * FROM `company-data-driven.{project_name}.traffic_analytics_web_clicks` ORDER BY date ASC;"))
    if df.shape[0] < 1:
        st.warning("Waiting for data")
    else:
        df_grouped = df.groupby('date').agg({
                'clicks': 'sum',
                'impressions': 'sum',
                'ctr': 'mean',
                'position': 'mean'
            }).reset_index()
        Clicks = df['clicks'].sum()
        Impressions = df['impressions'].sum()
        ctr_mean = df['ctr'].mean()
        pos_mean = df['position'].mean()
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
            plot_echarts(df_grouped)