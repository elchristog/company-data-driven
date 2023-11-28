import streamlit as st
import pandas as pd
import time
import datetime
import json
import tempfile


from datetime import date
from dateutil.relativedelta import relativedelta
from googleapiclient import discovery
from google_auth_oauthlib.flow import Flow
from streamlit_raw_echarts import st_echarts, JsCode

import utils.user_credentials as uc

# https://github.com/ViniciusStanula/Search-Console-API/tree/main
# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
# https://developers.google.com/youtube/analytics/reference/reports/query?hl=es-419

date = date.today()
data_final = date - relativedelta(days=2)
data_inicial = date - relativedelta(months=16)
data_padrao = date - relativedelta(months=1)

clientSecret = st.secrets["clientSecret"]
clientId = st.secrets["clientId"]
redirectUri = 'https://company-data-driven.streamlit.app'
href = "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={}&redirect_uri={}&scope=https://www.googleapis.com/auth/youtube.readonly&access_type=offline&prompt=consent".format(clientId, redirectUri)
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
    scopes=["https://www.googleapis.com/auth/youtube.readonly"],
    redirect_uri=redirectUri,
)
auth_url, _ = flow.authorization_url(prompt="consent")
    


def button_callback():
    try:
        st.session_state.my_token_received = True
        code_yt = st.experimental_get_query_params()["code"][0]
        st.session_state.my_token_input_youtube = code_yt
    except KeyError or ValueError:
        st.error("⚠️ The parameter 'code' was not found in the URL. Please log in.")



def check_input_url(input_url):
    if "https://" in input_url or "http://" in input_url:
        return input_url
    return f'sc-domain:{input_url}'



@st.cache_resource(show_spinner=False)
def get_ytproperty(token):
    flow.fetch_token(code=token)
    credentials = flow.credentials
    service = discovery.build(
        serviceName="youtubeAnalytics",
        version="v2",
        credentials=credentials,
        cache_discovery=False,
    )
    return service




# @st.cache_data(experimental_allow_widgets=True, show_spinner=False)
def plot_echarts_yt(df_grouped):
    df_grouped['average_view_percentage'] = df_grouped['average_view_percentage'].apply(lambda average_view_percentage: f"{average_view_percentage:.2f}")
    # df_grouped['position'] = df_grouped['position'].apply(lambda pos: round(pos, 2))
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
                "views": True,         # A série "views" está selecionada
                "suscribers_gained": True,    # A série "suscribers_gained" está selecionada
                "average_view_percentage": False,           # A série "average_view_percentage" não está selecionada
                "shares": False       # A série "shares" não está selecionada
            }
        },
        "tooltip": {"trigger": "axis", },
        "series": [
            {
                "type": "line",
                "name": "views",
                "data": df_grouped['views'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#A6785D"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "suscribers_gained",
                "data": df_grouped['suscribers_gained'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#394A59"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "average_view_percentage",
                "data": df_grouped['average_view_percentage'].tolist(),
                "smooth": True,
                "lineStyle": {"width": 2.4, "color": "#BF3F34"},
                "showSymbol": False,  # Remova os marcadores de dados para esta série
            },
            {
                "type": "line",
                "name": "shares",
                "data": df_grouped['shares'].tolist(),
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



# @st.cache_data(show_spinner=False)
def get_data_date(property_url, start_date, end_date, url_filter=None, url_operator=None,
                palavra_filter=None, palavra_operator=None):
        service = get_ytproperty(st.session_state.my_token_input_youtube)
        # st.write(service)
        data = []
        row_limit = 1000
        progress_text = "Retrieving Metrics. Please Wait. 🐈"
        my_bar = st.progress(0, text=progress_text)
        # day views
        startRow = 0
        while startRow == 0 or startRow % 25000 == 0 and startRow < row_limit:
            response = service.reports().query(
                ids='channel==MINE',
                startDate=start_date,
                endDate=end_date,
                metrics='views,subscribersGained,averageViewPercentage,shares',
                dimensions='day',
                sort='day'
            ).execute()
            rows = response.get('rows', [])
            startRow = startRow + len(rows)
            data.extend(rows)
            progress_percent = min((startRow / row_limit) * 100, 100)
            progress_value = progress_percent / 100.0
            my_bar.progress(progress_value, text=progress_text)
        df_clicks = pd.DataFrame([
            {
                'date': row[0],
                'views': row[1],
                'subscribersGained': row[2],
                'averageViewPercentage': row[3],
                'shares': row[4]
            } for row in data
        ])
        time.sleep(2)

        my_bar.empty()
        return df_clicks






def get_youtube_data_save_to_bq(role_id, project_name, project_url_clean):
    if role_id == 1:
        dates_in_table = uc.run_query_instant(f"SELECT DATE_DIFF(CURRENT_DATE(), MAX(date), DAY) - 3 AS days_last_update, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AS min_date_first_query, DATE_ADD(MAX(date), INTERVAL 1 DAY) AS min_date_next_query, DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY) AS max_date_next_query FROM `company-data-driven.{project_name}.traffic_analytics_youtube_views`;")
        days_last_update = dates_in_table[0].get("days_last_update")
        min_date_first_query = dates_in_table[0].get("min_date_first_query")
        min_date_next_query = dates_in_table[0].get("min_date_next_query")
        max_date_next_query = dates_in_table[0].get("max_date_next_query")
        
        if days_last_update is None or days_last_update > 0:
            if "my_token_input_youtube" not in st.session_state:
                st.session_state["my_token_input_youtube"] = ""
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
            
            st.write("### Update your youtube data")
            st.markdown("----")
            link_style = (
                "text-decoration: none;"
                "color: #D95F5F;"
                "padding: 8px 20px;"
                "border-radius: 4px;"
                "background-color: #F2E4DF;"
                "font-size: 16px;"
            )
            url = href
            st.markdown('1 - Log in to your Youtube account:')
            st.markdown(f'<a href="{url}" target="_blank" style="{link_style}">'
                    f'<img src="https://www.youtube.com/s/desktop/af9710b4/img/favicon_32x32.png" alt="Youtube" style="vertical-align: middle; margin-right: 10px;">'
                    f'Login With Youtube'
                    f'</a>', unsafe_allow_html=True)
            st.markdown('2 - Click the Button to grant API access:')
            submit_button = st.button(
                label="Grant API access", on_click=button_callback, key = "youtube_api_access"
            )
            st.markdown('This is your OAuth token:')
            code_yt = st.text_input(
                    "",
                    key="my_token_input_youtube",
                    label_visibility="collapsed",
                )
            get_data_button_yt = st.button("Get data", key = "youtube_get_data")
            if get_data_button_yt:
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
                st.table(df_clicks)
                today = datetime.date.today()
                today_str = today.strftime("%Y-%m-%d")
                st.info("Updating, please wait", icon = "☺️")
                for index, row in df_clicks.iterrows():
                    uc.run_query_insert_update(f"INSERT INTO `company-data-driven.{project_name}.traffic_analytics_youtube_views` (date, views, suscribers_gained, average_view_percentage, shares) VALUES ('{row['date']}', {row['views']}, {row['subscribersGained']}, {row['averageViewPercentage']}, {row['shares']});")
                time.sleep(15)
                st.rerun()






def show_youtube_metrics(project_name):
    st.write("### 	:movie_camera: Youtube traffic")
    min_max_dates_range_yt = uc.run_query_1_h(f"SELECT MIN(date) AS min_date, MAX(date) as max_date FROM `company-data-driven.{project_name}.traffic_analytics_youtube_views`;")
    if len(min_max_dates_range_yt) < 1:
        st.warning("Waiting for data")
    else:
        day_yt = st.date_input(
            "Time Range:",
            (min_max_dates_range_yt[0].get("min_date"), min_max_dates_range_yt[0].get("max_date")),
            min_value=min_max_dates_range_yt[0].get("min_date"),
            max_value=min_max_dates_range_yt[0].get("max_date"),
            format="DD/MM/YYYY",
            help='The available time range is the same as what is available in Google Search Console. DD/MM/YYYY Format',
            key = 'date_input_youtube'
        )
        df = pd.DataFrame(uc.run_query_1_h(f"SELECT * FROM `company-data-driven.{project_name}.traffic_analytics_youtube_views` WHERE date >= '{day_yt[0].strftime('%Y-%m-%d')}' AND date <= '{day_yt[1].strftime('%Y-%m-%d')}' ORDER BY date ASC;"))
        df_grouped = df.groupby('date').agg({
                'views': 'sum',
                'suscribers_gained': 'sum',
                'average_view_percentage': 'mean',
                'shares': 'sum'
            }).reset_index()
        views = df['views'].sum()
        suscribers_gained = df['suscribers_gained'].sum()
        average_view_percentage = df['average_view_percentage'].mean()
        shares = df['shares'].sum()
        met1, met2, met3, met4 = st.columns(4)
        with met1:
            st.metric('views:', f'{views:,}')
        with met2:
            st.metric('suscribers_gained:', f'{suscribers_gained:,}')
        with met3:
            st.metric('average_view_percentage:', f'{average_view_percentage:.2f}%')
        with met4:
            st.metric('shares:', f'{shares:.1f}')
        with st.container():
            plot_echarts_yt(df_grouped)
