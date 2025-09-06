# Rodrigo Bechara 23/08/2025
# Descrição: Armazena funções
import sqlalchemy           as sa
import streamlit            as st
import pandas               as pd
import hashlib
import datetime             as dt
import requests
from dateutil.relativedelta import relativedelta
import psutil
import subprocess

# ||=== ENUMERADORES =======================================================================================================================||
year = 'year'
month = 'month'
day = 'day'
hour = 'hour'
minute = 'minute'
second = 'second'

# ||=== FUNÇÕES DE RPA =====================================================================================================================||
status_runner01 = False

def get_runner01_status() -> bool:
    global status_runner01
    return status_runner01

# Verifica se o runner01 está rodando
def update_status_runner01():
    global status_runner01
    runner01_value = False
    try:
        query_get_status_runner01 = f"""
            SELECT
                BotName
                ,LastUpdate
            FROM Nexus.rpa.Bot
        """
        df_status_runner01 = pd.read_sql(query_get_status_runner01, get_db_conn_dnd())
        last_update = pd.to_datetime(df_status_runner01[df_status_runner01["BotName"] == "Runner01_PD"].iloc[0]["LastUpdate"])
        if last_update >= (dt.datetime.now() - dt.timedelta(minutes=6)):
            runner01_value = True
        else:
            runner01_value = False
    except Exception as e:
        print_console_log(f"Error Update Status Runner01: {e}")
        runner01_value = False
    # Grava status
    status_runner01 = runner01_value


# ||=== FUNÇÕES GERAIS =====================================================================================================================||
# Gera hash SHA-256 de uma senha
def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()

# Retorna primeiro dia do mês
def beginning_of_month(start_date: dt.date, months_to_add: int = 0) -> dt.date:
    return (start_date + relativedelta(months=months_to_add)).replace(day=1)

# Retorna último dia do mês
def end_of_month(start_date: dt.date, months_to_add: int = 0) -> dt.date:
    return (start_date + relativedelta(months=months_to_add + 1)).replace(day=1) - dt.timedelta(days=1)

def parse_date(date_input):
    if isinstance(date_input, dt.datetime):
        return date_input
    elif isinstance(date_input, str):
        # Tenta múltiplos formatos comuns
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y.%m.%d", "%d.%m.%Y"):
            try:
                return dt.datetime.strptime(date_input, fmt)
            except ValueError:
                continue
    raise ValueError("Formato de data inválido. Use datetime ou string como '2025-07-24' ou '24/07/2025'.")

def dateadd(datepart: str, number: int, date: dt.datetime) -> dt.datetime:
    date = parse_date(date)
    if datepart == year:
        return date + relativedelta(years=number)
    elif datepart == month:
        return date + relativedelta(months=number)
    elif datepart == day:
        return date + dt.timedelta(days=number)
    elif datepart == hour:
        return date + dt.timedelta(hours=number)
    elif datepart == minute:
        return date + dt.timedelta(minutes=number)
    elif datepart == second:
        return date + dt.timedelta(seconds=number)
    else:
        raise ValueError("Intervalo de tempo inválido.")

def print_console_log(messagem: str):
    print(f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}: {messagem}")

# ||=== FUNÇÕES DO SERVIDOR ================================================================================================================||
# Verificar validade do login
def check_login(arg_username, arg_password):
    try:
        engine = get_db_conn_dnd()
        with engine.connect() as conn:
            query = sa.text("""
                SELECT
                    username
                    ,password_hash
                    ,campaign_id
                    ,access_level_id
                    ,is_active
                FROM dnd3.auth.user
                WHERE
                    username = :username
            """)
            # Realiza consulta
            result = conn.execute(query, {"username": arg_username}).mappings().fetchone()

        if result and result["is_active"]:
            print(hash_password(arg_password))
            if result["password_hash"] == hash_password(arg_password):
                # Salva dados na sessão
                st.session_state["username"] = result["username"]
                st.session_state["campaign_id"] = result["campaign_id"]
                st.session_state["access_level_id"] = result["access_level_id"]
                st.session_state["is_logged"] = True
                # save_data_localstorage()
                return True
            else:
                st.session_state["is_logged"] = False
                return False
        else:
            st.session_state["is_logged"] = False
            return False
    except Exception as e:
        st.warning(f"Erro no check_login: {e}")
        st.session_state["is_logged"] = False
        return False

# Recarrega dados do usuário ativo
def reload_active_user():
    try:
        engine = get_db_conn_dnd()
        with engine.connect() as conn:
            query = sa.text("""
                SELECT
                    id
                    ,username
                    ,password_hash
                    ,campaign_id
                    ,access_level_id
                    ,is_active
                FROM dnd3.auth.user
                WHERE
                    Username = :username
            """)
            # Realiza consulta
            result = conn.execute(query, {"username": st.session_state.get("username")}).mappings().fetchone()

        if result and result["is_active"] == 1:
            # Salva dados na sessão
            st.session_state["user_id"] = result["Id"]
            st.session_state["campaign_id"] = result["campaign_id"]
            st.session_state["access_level_id"] = result["access_level_id"]
            st.session_state["is_logged"] = True
            # save_data_localstorage()
            return True
        else:
            st.session_state["is_logged"] = False
            # save_data_localstorage()
            return False
    except Exception as e:
        st.warning(f"Erro no check_login: {e}")
        st.session_state["is_logged"] = False
        # save_data_localstorage()
        return False

# Obtém hora da última limpeza do banco e horário da próxima limpeza
# def get_last_reset_cache_pd():
#     query_last_reset_cache_pd = f"""
#         SELECT TOP (1)
#             J.name                                                          AS JobName
#             ,STUFF(STUFF(
#                 CAST(H.run_date AS VARCHAR(8))
#                 ,5, 0, '-'), 8, 0, '-') + ' '
#                 + STUFF(STUFF(
#                     RIGHT('000000' + CAST(H.run_time AS VARCHAR(6)), 6)
#                     , 3, 0, ':'), 6, 0, ':')                                AS StartDatetime
#             ,STUFF(STUFF(
#                 RIGHT('000000' + CAST(H.run_duration AS VARCHAR(6)), 6)
#                 , 3, 0, ':'), 6, 0, ':')                                    AS Runtime
#             ,CASE H.run_status
#                 WHEN 0
#                     THEN 'Falha'
#                 WHEN 1
#                     THEN 'Sucesso'
#                 WHEN 2
#                     THEN 'Tentando Novamente'
#                 WHEN 3
#                     THEN 'Cancelado'
#                 WHEN 4
#                     THEN 'Em andamento'
#                 ELSE
#                     'Desconhecido'
#             END                                                             AS [Status]
#             ,H.message                                                      AS [Message]
#         FROM msdb.dbo.sysjobs               AS J
#         INNER JOIN msdb.dbo.sysjobhistory   AS H
#             ON J.job_id = H.job_id
#         WHERE
#             H.step_id = 0
#             AND J.name = 'Reset_SQLServerCache'
#         ORDER BY
#             H.run_date DESC
#             ,H.run_time DESC
#     """
#     df_last_reset_cache_pd = pd.read_sql(query_last_reset_cache_pd, get_pd_connection())
#     return df_last_reset_cache_pd


# ||=== FUNÇÕES DE APARÊNCIA ===============================================================================================================||

# Carrega a barra lateral
def load_sidebar():
    # Oculta menu padrão de navegação do Streamlit
    # st.markdown("""
    #     <style>
    #         div[data-testid="stSidebarNav"] {display: none;}
    #     </style>
    # """, unsafe_allow_html=True)
    # Define o idioma da página como pt-BR
    # st.markdown("""
    #     <meta http-equiv="Content-Language" content="pt-BR">
    #     <script>
    #         document.documentElement.lang = 'pt-BR';
    #     </script>
    # """, unsafe_allow_html=True)
    if st.session_state.get("is_logged", False):
        st.markdown("""
            <style>
                /* Define espaço lateral */
                .block-container {
                    padding-left: 1.5rem !important;
                    padding-right: 1.5rem !important;
                }
                /* Remove margem/padding do primeiro container da sidebar */
                section[data-testid="stSidebar"] > div:first-child {
                    padding-top: 0px !important;
                    margin-top: 0px !important;
                }
                /* Remove qualquer espaço dentro da sidebar */
                section[data-testid="stSidebar"] .block-container {
                    padding-top: 0px !important;
                    margin-top: 0px !important;
                }
                /* Remove margem da área de colapso */
                div[data-testid="collapsedControl"] {
                    margin-top: 0px !important;
                    padding-top: 0px !important;
                    height: 0px !important;
                    visibility: hidden;
                }
                /* Remove padding do próprio botão colapsável (caso esteja visível) */
                [data-testid="stSidebarCollapseButton"] {
                    padding-top: 0px !important;
                    margin-top: 0px !important;
                    height: 0px !important;
                    visibility: hidden;
                }
            </style>
        """, unsafe_allow_html=True)
        with st.sidebar:
            st.markdown("""
                <style>
                    /* Oculta o cabeçalho da sidebar completamente */
                    div[data-testid="stSidebarHeader"] {
                        display: none !important;
                        height: 0px !important;
                        margin: 0px !important;
                        padding: 0px !important;
                    }
                    /* Oculta botão de recolher caso ainda esteja renderizado */
                    div[data-testid="stSidebarCollapseButton"] {
                        display: none !important;
                        height: 0px !important;
                        visibility: hidden;
                    }
                    /* Remove espaço adicional da logo ou espaçador */
                    div[data-testid="stLogoSpacer"] {
                        display: none !important;
                        height: 0px !important;
                    }
                </style>
            """, unsafe_allow_html=True)
            # Título
            st.sidebar.markdown("""
                <h1 style='font-size: 32px; argin-bottom: -2rem; '>
                    Archivist
                </h1>
            """, unsafe_allow_html=True)
            st.markdown("### Sistema pra gente jogar D&D 3.5")

        # Botões
        bt_home = st.sidebar.button("Início", use_container_width=True, key="bt_home")
        bt_grid = st.sidebar.button("Campo", use_container_width=True, key="bt_grid")
        # bt_reports = st.sidebar.button("Relatórios", use_container_width=True, key="bt_reports")
        # bt_power_bi = st.sidebar.button("Power BI", use_container_width=True, key="bt_power_bi")

        # bt_operations = st.sidebar.button("Operações", use_container_width=True, key="bt_operations")
        # if bt_operations and st.session_state.get("active_page") != "operations":
        #     st.switch_page("pages/operations.py")

        # # RPA
        # if st.session_state.get("access_level_id", 3) == 1:
        #     bt_admin_panel = st.sidebar.button("RPA", use_container_width=True, key="bt_rpa")
        #     if bt_admin_panel and st.session_state.get("active_page") != "rpa":
        #         st.switch_page("pages/rpa.py")

        # # Hub de Parceiros
        # if st.session_state.get("access_level_id", 3) == 1 or st.session_state.get("group_id") == 9:
        #     bt_admin_panel = st.sidebar.button("Hub de Parceiros", use_container_width=True, key="bt_partner_hub")
        #     if bt_admin_panel and st.session_state.get("active_page") != "partner_hub":
        #         st.switch_page("pages/partner_hub.py")

        # # Painal Adm
        # if st.session_state.get("access_level_id", 3) <= 2:
        #     bt_admin_panel = st.sidebar.button("Painel Administrativo", use_container_width=True, key="bt_admin_panel")
        #     if bt_admin_panel and st.session_state.get("active_page") != "admin_panel":
        #         st.switch_page("pages/admin_panel.py")

        # Alterna página
        if bt_home and st.session_state.get("active_page") != "home":
            st.switch_page("pages/home.py")
        elif bt_grid and st.session_state.get("active_page") != "grid":
            st.switch_page("pages/grid.py")
        # elif bt_reports and st.session_state.get("active_page") != "reports":
        #     st.switch_page("pages/reports.py")
        # elif bt_power_bi and st.session_state.get("active_page") != "power_bi":
        #     st.switch_page("pages/power_bi.py")
    else:
        st.markdown("""
            <style>
                /* Oculta a barra lateral */
                section[data-testid="stSidebar"] {
                    display: none !important;
                }
                /* Remove o espaço reservado pra barra lateral */
                div[data-testid="collapsedControl"] {
                    display: none !important;
                }
            </style>
        """, unsafe_allow_html=True)

def hidden_header():
    # st.markdown("""
    #     <style>
    #         .block-container {
    #             padding-top: 1rem !important;
    #         }
    #         header[data-testid="stHeader"] {
    #             height: 0;
    #             visibility: hidden;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)
    st.markdown("""
        <style>
            /* Oculta o cabeçalho */
            header[data-testid="stHeader"] {
                height: 0;
                visibility: hidden;
            }

            /* Remove o espaçamento no topo do conteúdo */
            .block-container {
                padding-top: 0rem !important;
            }

            /* Garante que o primeiro elemento não crie espaço extra */
            .main > div:first-child {
                margin-top: 0rem !important;
                padding-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Oculta barra de desenvolvimento
def hide_streamlit_elements():
    st.markdown("""
        <style>
            /* Oculta cabeçalho */
            header[data-testid="stHeader"] {
                display: none !important;
            }
            /* Oculta rodapé */
            footer[data-testid="stFooter"] {
                display: none !important;
            }
            /* Oculta botão da barra lateral (colapsar) */
            div[data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }
            /* Oculta barra laranja de carregamento/status */
            [data-testid="stStatusWidget"] {
                display: none !important;
            }
            /* Remove espaçamento superior da barra lateral */
            div[data-testid="stSidebar"] > div:first-child {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)


# Adiciona espaço
def shift_top(space: int = 0):
    st.markdown(f"""
            <div style='position: relative; top: 0px; font-size: {space}px;'><br></div>
        """, unsafe_allow_html=True
    )

# Redireciona para url
def redirect(url):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url={url}" />
    """, unsafe_allow_html=True)

# Altera tema
def alter_theme():
    theme = st.session_state.get("theme", "Padrão")
    # Tema escuro
    if theme == "Escuro":
        st.markdown("""
            <style>
                /* Fundo e Fonte */
                .main, .block-container, .css-1v3fvcr {
                    background-color: #0E1117 !important;
                    color: #FAFAFA !important;
                }
                /* Botões */
                button, .stButton > button {
                    background-color: #303841 !important;
                    color: #FAFAFA !important;
                }
                /* Barra Lateral */
                .css-1d391kg, .css-1v3fvcr {
                    background-color: #1B1F27 !important;
                    color: #FAFAFA !important;
                }
            </style>
        """, unsafe_allow_html=True)

    # Tema claro
    if theme == "Claro":
        st.markdown("""
            <style>
                /* Fundo e Fonte */
                .main, .block-container, .css-1v3fvcr {
                    background-color: #FFFFFF !important;
                    color: #000000 !important;
                }
                /* Botões */
                button, .stButton > button {
                    background-color: #f0f0f0 !important;
                    color: #000000 !important;
                }
                /* Barra Lateral */
                .css-1d391kg, .css-1v3fvcr {
                    background-color: #F5F5F5 !important;
                    color: #000000 !important;
                }
            </style>
        """, unsafe_allow_html=True)

    # Tema CSG
    if theme == "CSG":
        st.markdown("""
            <style>
                /* Fundo e Fonte */
                .main, .block-container, .css-1v3fvcr {
                    background-color: #ffffff !important;
                    color: #000000 !important;
                }
                /* Fundo */
                body {
                    background-color: #ffffff !important;
                    color: #f5f6f6 !important;
                }
                /* Botões */
                button, .stButton > button {
                    background-color: #ea5b0c !important;
                    color: #000000 !important;
                }
                /* Efeito Botões */
                .stButton > button:hover {
                    background-color: #45a049;
                    color: #025fbc;
                }
                /* Barra Lateral */
                .stSidebar {
                    background-color: #f5f6f6 !important;
                    color: #000000 !important;
                }
                .css-1d391kg, .css-1v3fvcr {
                    background-color: #F5F5F5 !important;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Volta ao tema padrão
        # st.query_params = {"theme": "default"}
        # st.query_params.setdefault()
        # st.rerun()
        st.markdown("""
            <style>
                html {
                    filter: none !important;
                }
            </style>
        """, unsafe_allow_html=True)


# Adicona uma divisor horizontal
def horizontal_divider():
    # st.markdown("---")
    st.markdown(
        """
        <style>
        hr.custom-line {
            border: none;
            height: 2px;
            background-color: rgba(0, 0, 0, 0.4); /* tema claro */
        }
        @media (prefers-color-scheme: dark) {
            hr.custom-line {
                background-color: rgba(255, 255, 255, 0.4); /* tema escuro */
            }
        }
        </style>
        <hr class="custom-line">
        """,
        unsafe_allow_html=True
    )

# Adicona uma divisor vertical
def vertical_divider(px_height: int):
    st.markdown(
        """
        <style>
        div[data-testid="column"] > div {
            height: 100%;
        }
        .vertical-divider {
            border-left: 1px solid rgba(255, 255, 255, 0.7);
        }
        [data-baseweb="light-theme"] .vertical-divider {
            border-left: 1px solid rgba(0, 0, 0, 0.7);
        }
        </style>
        """
        ,unsafe_allow_html=True
    )
    st.markdown(f'<div class="vertical-divider" style="height:{px_height}px;"></div>', unsafe_allow_html=True)
    # st.markdown('<div class="vertical-divider" style="height:"100%";"></div>', unsafe_allow_html=True)

# ||=== CONEXÕES ===========================================================================================================================||
# Retorna conxão ao banco
def get_db_conn_dnd():
    # engine = sa.create_engine("mssql+pyodbc://sa:Craft3.5%26@RODRIGO-LAPTOP/DND3?driver=ODBC+Driver+17+for+SQL+Server")
    engine = sa.create_engine(
        "postgresql+psycopg2://dnd3_user:GlcC7Rw59jupwNOMFkDDk3PBYiU8N5uL@dpg-d2u1n8ffte5s73an4lq0-a.oregon-postgres.render.com:5432/dnd3"
        ,connect_args={"sslmode": "require"}  # Render exige SSL
    )
    return engine

# ||=== API ================================================================================================================================||

# NEVADA - DESCARTE DE PASSAGENS PAGAS
# Obtém token de acesso ao banco do Nevada
def get_access_token_nevada(open_passages_user: str, open_passages_access_key: str):
    # print_console_log("get_access_token_nevada")
    url = "https://10.0.50.2/api/v1/session"
    data = {
        "user": open_passages_user
        ,"accessKey": open_passages_access_key
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers, verify=False)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('accessToken')
        else:
            print(f"Erro no POST. Status Code: {response.status_code}, Detalhes: {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao realizar o POST: {e}")
        return None

# Obtém CSV formatado de passagens pagas
def get_csv_body_paid_passages_attri(open_passages_initial_date: dt.datetime, open_passages_end_date: dt.datetime):
    # print_console_log("get_csv_body_paid_passages_attri")
    query = f"""
        SELECT
            '001'                                   AS "concessionId"
            ,C."financialTransactionId"             AS "transactionId"
            ,'DESCARTE AUTOMATICO TRANSACAO PAGA'   AS "reason"
        FROM
            public.charge AS C
        WHERE
            C."status" = 'paid'
            AND "datetimeOccurrence"::DATE BETWEEN '{open_passages_initial_date.strftime('%Y-%m-%d')}' AND '{open_passages_end_date.strftime('%Y-%m-%d')}'
    """
    try:
        df_csv_body_paid_passages = pd.read_sql(query, get_db_conn_dnd())
        if not df_csv_body_paid_passages.empty:
            csv_body_paid_passages_double_quotes = df_csv_body_paid_passages.to_csv(index=False, sep=";", header=False, encoding="utf-8-sig")
            csv_body_paid_passages = csv_body_paid_passages_double_quotes.replace('"', '')
            return csv_body_paid_passages
        else:
            return None
    except:
        return None

# Descarta passagens pagas
def discards_paid_passages(open_passages_initial_date: dt.datetime, open_passages_end_date: dt.datetime, open_passages_user: str, open_passages_access_key: str):
    print_console_log("Discards paid passages")
    url = "https://10.0.50.2/api/v1/register"
    csv_body = get_csv_body_paid_passages_attri(open_passages_initial_date, open_passages_end_date)
    access_token_nevada = get_access_token_nevada(open_passages_user, open_passages_access_key)
    headers = {
        "Authorization": f"Bearer {access_token_nevada}"
        ,"Content-Type": "text/csv"
    }
    try:
        response = requests.delete(url, headers=headers, data=csv_body, verify=False)
        if response.status_code == 200:
            return response.text
        else:
            return (f"DELETE Error. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        return (f"DELETE Function Internal Error: {e}")

# Cria Log de execução do discards_paid_passages
def create_log_discards_paid_passages(initial_date: dt.datetime, end_date: dt.datetime, access_user: str, count_discarded: int, count_already_discarded: int, count_failed: int):
    print_console_log("Create log discards paid passages")
    engine_pd = get_db_conn_dnd()
    with engine_pd.begin() as conn:
        insert_query = sa.text(f"""
            INSERT INTO Nexus.log.Operation_DiscardPaidPassages (
                ExecutedAt
                ,ExecutedBy
                ,InitialDate
                ,EndDate
                ,AccessUser
                ,Count_Discarded
                ,Count_AlreadyDiscarded
                ,Count_Failed
            )
            VALUES (
                GETDATE()
                ,'{st.session_state.get("username")}'
                ,'{initial_date.strftime('%Y-%m-%d')}'
                ,'{end_date.strftime('%Y-%m-%d')}'
                ,'{access_user}'
                ,{count_discarded}
                ,{count_already_discarded}
                ,{count_failed}
            )
        """)
        try:
            conn.execute(insert_query)
            return None
        except Exception as e:
            return e

# GERAIS
# Obtém status do painel da Attri
def get_attri_panel_status():
    url = "https://api.freeflow.csg.com.br/queues/charge/info"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return (f"GET Error. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        return (f"GET Function Internal Error: {e}")