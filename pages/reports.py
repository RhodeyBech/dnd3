# Rodrigo Bechara 15/07/2025
# Página de consultas
import streamlit                as st
import pandas                   as pd
import datetime                 as dt
import time
import json
# import plotly.express           as px
# import plotly.graph_objects     as go

# Import local pasta anterior
import sys
sys.path.append("...")
import functions                as fn

# Oculta menu padrão de navegação do Streamlit
st.markdown("""
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Altera tema
fn.alter_theme()

# Obtém dados do armazenamento local
# fn.load_data_localstorage()

# Identifica se o usuário está logado
if not st.session_state.get("is_logged", False):
    st.switch_page("pages/login.py")
    # st.switch_page("pages/login")

# Configuração da página
st.set_page_config(
    page_title="Nexus"
    ,page_icon="https://www.csg.com.br/build/assets/favicon-c752c7b3.png"
    ,layout="wide"
)

# Ajusta cabeçalho da página
fn.hidden_header()

# Define página ativa
st.session_state["active_page"] = "reports"

# Carrega a barra lateral
fn.load_sidebar()

# Título
st.subheader("Relatórios")

# Conexões
engine_pd = fn.get_pd_connection()
engine_attri = fn.get_attri_connection()

# Inicializa flags
show_general_tab = True
show_admin_tab = False
show_financial_tab = False
show_backoffice_tab = False
show_infrastructure_it_tab = False
show_administrative_it_tab = False
show_communication_tab = False
show_personnel_management_tab = False

# Parâmetros de largura
col_menu_width = 3
col_content_width = 20

# Define abas para mostrar
# 1 - Administração
# 2 - Teste de Software
# 3 - Geral
# 4 - Diretoria
# 5 - Backoffice
# 6 - Financeiro
# 7 - TI Infraestrutura
# 8 - TI Administrativa
# 9 - Comunicação
# 10 - Gestão de Pessoas
# Administração
if st.session_state.get("group_id") == 1:
    tab_admin, tab_general, tab_backoffice, tab_financial, tab_infrastructure_it, tab_administrative_it_tab = st.tabs([
        "Administrativo"
        ,"Geral"
        ,"Backoffice"
        ,"Financeiro"
        ,"TI Infraestrutura"
        ,"TI Administrativa"
    ])
    show_admin_tab = True
    show_financial_tab = True
    show_backoffice_tab = True
    show_infrastructure_it_tab = True
    show_administrative_it_tab = True
# Geral
elif st.session_state.get("group_id") == 3:
    tab_general, = st.tabs(["Geral"])
# Diretoria e Teste de Software
elif st.session_state.get("group_id") in {2, 4}:
    tab_general, tab_backoffice, tab_financial, tab_infrastructure_it, tab_administrative_it_tab = st.tabs([
        "Geral"
        ,"Backoffice"
        ,"Financeiro"
        ,"TI Infraestrutura"
        ,"TI Administrativa"
    ])
    show_admin_tab = True
    show_financial_tab = True
    show_backoffice_tab = True
    show_infrastructure_it_tab = True
    show_administrative_it_tab = True
# Backoffice
elif st.session_state.get("group_id") == 5:
    tab_general, tab_backoffice = st.tabs(["Geral", "Backoffice"])
    show_backoffice_tab = True
# Financeiro
elif st.session_state.get("group_id") == 6:
    tab_general, tab_financial = st.tabs(["Geral", "Financeiro"])
    show_financial_tab = True
# TI Infraestrutura
elif st.session_state.get("group_id") == 7:
    tab_general, tab_infrastructure_it = st.tabs(["Geral", "TI Infraestrutura"])
    show_infrastructure_it_tab = True
# TI Administrativa
elif st.session_state.get("group_id") == 8:
    tab_general, tab_administrative_it_tab = st.tabs(["Geral", "TI Administrativa"])
    show_administrative_it_tab = True
# Comunicação
elif st.session_state.get("group_id") == 9:
    tab_general, tab_communication = st.tabs(["Geral", "Comunicação"])
    show_communication_tab = True
# Gestão de Pessoas
elif st.session_state.get("group_id") == 10:
    tab_general, tab_personnel_management = st.tabs(["Geral", "Gestão de Pessoas"])
    show_personnel_management_tab = True



# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    ADMINISTRATIVO                                                                                                                      ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_admin_tab:
    with tab_admin:
        df_jobs_execution = pd.DataFrame()
        col1, col2 = st.columns([col_menu_width, col_content_width])

        with col1:
            # st.markdown("##### Banco de Dados")
            if st.button("Execução de Trabalhos", key="admin_jobs_execution", use_container_width=True):
                st.session_state["report_admin"] = "admin_jobs_execution"
            if st.button("Status Painel da Attri", key="admin_attri_panel_status", use_container_width=True):
                st.session_state["report_admin"] = "admin_attri_panel_status"

        with col2:
            placeholder_admin = st.empty()
            option_admin = st.session_state.get("report_admin")

            if option_admin == "admin_jobs_execution":
                placeholder_admin.warning("Pesquisando...")

                st.write("Execução de Trabalhos")

                # Escreve query
                query = f"""
                    SELECT
                        JobName
                        ,SchemaName
                        ,[Begin]
                        ,[End]
                        ,CASE
                            WHEN Runtime IS NOT NULL
                                THEN LEFT(Runtime, 8)
                            ELSE
                                NULL
                        END AS Runtime
                        ,[Status]
                        ,Progress
                        ,InitialParameter
                        ,EndingParameter
                        ,[Message]
                        ,CASE
                            WHEN [Enabled] = 1
                                THEN 'True'
                            ELSE
                                'False'
                        END AS [Enabled]
                        ,Frequency
                        ,Recurrence
                        ,StartTime
                    FROM PD.dbo.vw_JobsExecution
                    ORDER BY
                        SchemaName
                        ,JobName
                """

                # Consulta ao banco
                df_jobs_execution = pd.read_sql(query, engine_pd)
                
                st.write(f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

                # Constroi dataframe
                if not df_jobs_execution.empty:
                    # Exibe em tela
                    st.dataframe(df_jobs_execution, height=670, hide_index=True)
                    placeholder_admin.empty()
                else:
                    placeholder_admin.error("Nenhum registro encontrado.")

                if "report_admin" in st.session_state:
                    del st.session_state["report_admin"]

            elif option_admin == "admin_attri_panel_status":
                placeholder_admin.warning("Pesquisando...")

                st.write("Status Painel da Attri")

                attri_panel_status = json.loads(fn.get_attri_panel_status())
                attri_panel_status_counts = json.loads(str(attri_panel_status["counts"]).replace("'", '"'))
                attri_panel_status_jobs = json.loads(str(attri_panel_status["jobs"]).replace("'", '"'))
                df_attri_panel_status_counts = [
                    {"key": "waiting", "value": attri_panel_status_counts["waiting"]}
                    ,{"key": "active", "value": attri_panel_status_counts["active"]}
                    ,{"key": "completed", "value": attri_panel_status_counts["completed"]}
                    ,{"key": "failed", "value": attri_panel_status_counts["failed"]}
                    ,{"key": "delayed", "value": attri_panel_status_counts["delayed"]}
                    ,{"key": "paused", "value": attri_panel_status_counts["paused"]}
                ]
                df_attri_panel_status_jobs = [
                    {"key": "waiting", "value": attri_panel_status_jobs["waiting"]}
                    ,{"key": "active", "value": attri_panel_status_jobs["active"]}
                    ,{"key": "completed", "value": attri_panel_status_jobs["completed"]}
                    ,{"key": "failed", "value": attri_panel_status_jobs["failed"]}
                    ,{"key": "delayed", "value": attri_panel_status_jobs["delayed"]}
                ]

                # Mensagem
                st.write(f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                st.text(f"isPaused:\t{attri_panel_status["isPaused"]}")
                # Exibe em tela
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    st.text(f"counts:")
                    st.dataframe(df_attri_panel_status_counts, height=248, hide_index=True)
                with col2:
                    st.text(f"jobs:")
                    st.dataframe(df_attri_panel_status_jobs, height=248, hide_index=True)

                placeholder_admin.empty()

                if "report_admin" in st.session_state:
                    del st.session_state["report_admin"]


            

# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    GERAL                                                                                                                               ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_general_tab:
    with tab_general:
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            st.markdown("##### Movvia")
            if st.button("Saldo por Placa", use_container_width=True):
                st.session_state["report_general"] = "general_movvia_balance_by_plate"
                if "report_general_movvia" in st.session_state:
                    del st.session_state["report_general_movvia"]
            if st.button("Passagens em Aberto", key="general_open_passages", use_container_width=True):
                st.session_state["report_general"] = "general_open_passages"
                if "report_general_movvia" in st.session_state:
                    del st.session_state["report_general_movvia"]
            if st.button("Veículos Cadastrados", use_container_width=True):
                st.session_state["report_general"] = "general_movvia_registered_vehicles"
                if "report_general_movvia" in st.session_state:
                    del st.session_state["report_general_movvia"]

            # st.markdown("##### Kapsch")
            # if st.button("Consulta por Placa", use_container_width=True):
            #     st.session_state["report_general"] = "general_search_passage_by_plate"
            # if st.button("Consulta por Transação Financeira", use_container_width=True):
            #     st.session_state["report_general"] = "search_passage_by_financial_transaction"

        with col_content:
            option_general = st.session_state.get("report_general")

            # ||=== MOVVIA =================================================================================================================||
            if option_general == "general_movvia_balance_by_plate":
                st.write("Movvia -- Saldo por Placa")
                df_movvia_balance_by_plate = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="movvia_balance_by_plate_search", use_container_width=True):
                        st.session_state["report_general_movvia"] = "movvia_balance_by_plate_search"
                    csv_movvia_balance_by_plate = df_movvia_balance_by_plate.to_csv(sep=";", index=False)
                    if "movvia_balance_by_plate_search_df" in st.session_state:
                        if not st.session_state.get("movvia_balance_by_plate_search_df").empty:
                            df_movvia_balance_by_plate = st.session_state.get("movvia_balance_by_plate_search_df")
                            csv_movvia_balance_by_plate = df_movvia_balance_by_plate.to_csv(sep=";", index=False)
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_movvia_balance_by_plate"
                        ,data=csv_movvia_balance_by_plate.encode("utf-8-sig")
                        ,file_name="Saldo por Placa.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    movvia_balance_by_plate_license_plate = st.text_input(label="Placa", key="Placa - Saldo por Placa").upper().strip()
                with col3:
                    st.write("Selecine um aquivo de placas:")
                    movvia_balance_by_plate_license_plate_file = ""
                    movvia_balance_by_plate_license_plate_file = st.file_uploader("Arquivo - Saldo por Placa", type=["xlsx", "xls"], label_visibility="collapsed")

                placeholder_movvia_balance_by_plate = st.empty()

                option_movvia = st.session_state.get("report_general_movvia")
                if option_movvia == "movvia_balance_by_plate_search":
                    placeholder_movvia_balance_by_plate.warning("Pesquisando...")
                    movvia_balance_by_plate_cte_licensePlate = ""

                    if movvia_balance_by_plate_license_plate_file:
                        df_movvia_balance_by_plate_excel = pd.read_excel(movvia_balance_by_plate_license_plate_file)

                        if df_movvia_balance_by_plate_excel.shape[1] == 0:
                            placeholder_movvia_balance_by_plate.error("O arquivo não possui dados.")
                            del st.session_state["report_general_movvia"]
                        else:
                            # Pega a primeira coluna
                            first_col = df_movvia_balance_by_plate_excel.iloc[:, 0].dropna().astype(str).str.strip().str.upper()
                            plates = first_col.unique()

                            if len(plates) == 0:
                                placeholder_movvia_balance_by_plate.warning("Nenhuma placa válida encontrada.")
                                st.stop()

                        # Escreve cte
                        movvia_balance_by_plate_license_plate_file.close()
                        movvia_balance_by_plate_cte_licensePlate = ",\n        ".join([f"('{plate}')" for plate in plates])

                    elif movvia_balance_by_plate_license_plate:
                        movvia_balance_by_plate_cte_licensePlate = f"('{movvia_balance_by_plate_license_plate}')"

                    if not movvia_balance_by_plate_cte_licensePlate:
                        placeholder_movvia_balance_by_plate.error("Forneça um arquivo com placas ou informe uma placa.")
                        st.stop()

                    # Escreve query
                    query_movvia_balance_by_plate = f"""
                        WITH cte_LicensePlate AS (
                            SELECT
                                C1 AS "licensePlate"
                            FROM (VALUES
                                {movvia_balance_by_plate_cte_licensePlate}
                            ) AS TB (C1)
                        )
                        -- ,cte_OCAC AS (
                        --     SELECT
                        --         "chargeId"
                        --         ,MAX("orderId") AS "orderId"
                        --     FROM public.order_charges_arr_charge
                        --     GROUP BY
                        --         "chargeId"
                        -- )
                        SELECT
                            C."licensePlate"                                                    AS "Placa"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(SUM(C."rateAmount")* 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Tarifa"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(SUM(C.discount) * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Desconto"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(SUM(C.fee) * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Acréscimo"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(
                                    (SUM(C."rateAmount") - SUM(C.discount) + SUM(C.fee)
                                ) * 0.01, 'FM999G999G990D00')
                            ,'.', '|' ), ',', '.'), '|', ',')                                   AS "Valor da Passagem"
                            ,REPLACE(REPLACE(REPLACE(
                                TO_CHAR(COUNT(*), 'FM999G999G990')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Qtde de Passagens"
                        FROM public.charge                          AS C
                        -- LEFT JOIN cte_OCAC                          AS OCAC
                        --     ON OCAC."chargeId" = C.id
                        -- LEFT JOIN public."order"                    AS O
                        --     ON O.id = OCAC."orderId"
                        LEFT JOIN cte_LicensePlate                  AS LP
                            ON LP."licensePlate" = C."licensePlate"
                        WHERE
                            C.status = 'open'
                            AND LP."licensePlate" IS NOT NULL
                        GROUP BY
                            C."licensePlate"
                    """

                    # Consulta ao banco
                    df_movvia_balance_by_plate = pd.read_sql(query_movvia_balance_by_plate, engine_attri)

                    st.session_state["movvia_balance_by_plate_search_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                    # Salva o resultado
                    st.session_state["movvia_balance_by_plate_search_df"] = df_movvia_balance_by_plate
                    placeholder_movvia_balance_by_plate.empty()

                    if "report_general_movvia" in st.session_state:
                        del st.session_state["report_general_movvia"]
                        st.rerun()

                if "report_general_movvia" in st.session_state:
                    del st.session_state["report_general_movvia"]

                if "movvia_balance_by_plate_search_df" in st.session_state:
                    if not st.session_state.get("movvia_balance_by_plate_search_df").empty:
                        # Exibe em tela
                        st.write(st.session_state["movvia_balance_by_plate_search_datetime"])
                        st.dataframe(st.session_state.get("movvia_balance_by_plate_search_df"), height=600, hide_index=True, width=860)
                    else:
                        placeholder_movvia_balance_by_plate.error("Nenhum registro encontrado.")
                        if "movvia_balance_by_plate_search_df" in st.session_state:
                            del st.session_state["movvia_balance_by_plate_search_df"]



            elif option_general == "general_open_passages":
                placeholder_general_movvia_open_passages = st.empty()
                st.write("Movvia -- Passagens em Aberto")
                df_general_movvia_open_passages = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="general_movvia_open_passages", use_container_width=True):
                        st.session_state["report_general_movvia"] = "general_movvia_open_passages_search"

                    csv_general_movvia_open_passages = df_general_movvia_open_passages.to_csv(sep=";", index=False)
                    if "general_movvia_open_passages_search_df" in st.session_state:
                        if not st.session_state.get("general_movvia_open_passages_search_df").empty:
                            df_general_movvia_open_passages = st.session_state.get("general_movvia_open_passages_search_df")
                            csv_general_movvia_open_passages = df_general_movvia_open_passages.to_csv(sep=";", index=False)

                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_general_movvia_open_passages"
                        ,data=csv_general_movvia_open_passages.encode("utf-8-sig")
                        ,file_name="Passagens em Aberto Movvia.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    general_movvia_open_passages_initial_date = st.date_input("Data da Passagem:", value=dt.date.today(), format="DD/MM/YYYY", key="general_movvia_open_passages_initial_date")
                    general_movvia_open_passages_end_date = st.date_input("Data da Passagem:", value=dt.date.today(), format="DD/MM/YYYY", key="general_movvia_open_passages_end_date")
                
                option_general_movvia = st.session_state.get("report_general_movvia")
                if option_general_movvia == "general_movvia_open_passages_search":
                    placeholder_general_movvia_open_passages.warning("Pesquisando...")

                    # Escreve query
                    query_general_movvia_open_passages = f"""
                        SELECT
                            TO_CHAR(C."datetimeOccurrence", 'DD/MM/YYYY HH24:MI:SS')            AS "Data da Passagem"
                            ,C."licensePlate"                                                   AS "Placa"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C."rateAmount"* 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Tarifa"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C.discount * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Desconto"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C.fee * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Acréscimo"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(
                                    (C."rateAmount" - C.discount + C.fee
                                ) * 0.01, 'FM999G999G990D00')
                            ,'.', '|' ), ',', '.'), '|', ',')                                   AS "Valor da Passagem"
                            ,C."userId"::TEXT                                                   AS "Id de Usuário"
                            ,CASE
                                WHEN TRIM(UPPER(U.firstname)) = TRIM(UPPER(U.lastname))
                                    THEN TRIM(U.firstname)
                                ELSE
                                    TRIM(U.firstname) || ' ' || TRIM(U.lastname)
                            END                                                                 AS "Nome do Cliente"
                            ,U.phone                                                            AS "Telefone"
                            ,U.email                                                            AS "E-mail"
                        FROM public.charge          AS C
                        LEFT JOIN public.user       AS U
                            ON U.id = C."userId"
                        WHERE
                            C.status = 'open'
                            AND "datetimeOccurrence"::DATE BETWEEN '{general_movvia_open_passages_initial_date.strftime('%Y-%m-%d')}' AND '{general_movvia_open_passages_end_date.strftime('%Y-%m-%d')}'
                        ORDER BY
                            C."datetimeOccurrence"
                    """

                    # Consulta ao banco
                    df_general_movvia_open_passages = pd.read_sql(query_general_movvia_open_passages, engine_attri)

                    st.session_state["general_movvia_open_passages_search_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_general_movvia_open_passages.empty:
                        # Salva o resultado
                        st.session_state["general_movvia_open_passages_search_df"] = df_general_movvia_open_passages
                        st.session_state["general_movvia_open_passages_search_exists_df"] = True
                        # Exibe em tela
                        placeholder_general_movvia_open_passages.empty()
                    else:
                        st.session_state["general_movvia_open_passages_search_exists_df"] = False

                    if "report_general_movvia" in st.session_state:
                        del st.session_state["report_general_movvia"]
                        st.rerun()

                if "report_general_movvia" in st.session_state:
                    del st.session_state["report_general_movvia"]

                if "general_movvia_open_passages_search_exists_df" in st.session_state:
                    if not st.session_state.get("general_movvia_open_passages_search_exists_df", True):
                        placeholder_general_movvia_open_passages.error("Nenhum registro encontrado.")

                if "general_movvia_open_passages_search_df" in st.session_state:
                    if not st.session_state.get("general_movvia_open_passages_search_df").empty and st.session_state.get("general_movvia_open_passages_search_exists_df"):
                        # Exibe em tela
                        st.write(st.session_state["general_movvia_open_passages_search_datetime"])
                        st.dataframe(st.session_state.get("general_movvia_open_passages_search_df"), height=600, hide_index=True)

            elif option_general == "general_movvia_registered_vehicles":
                placeholder_movvia_registered_vehicles = st.empty()
                st.write("Movvia -- Veículos Cadastrados")
                df_movvia_registered_vehicles = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="movvia_registered_vehicles_search", use_container_width=True):
                        st.session_state["report_general_movvia"] = "movvia_registered_vehicles_search"

                    csv_movvia_registered_vehicles = df_movvia_registered_vehicles.to_csv(sep=";", index=False)
                    if "movvia_registered_vehicles_df" in st.session_state:
                        if not st.session_state.get("movvia_registered_vehicles_df").empty:
                            df_movvia_registered_vehicles = st.session_state.get("movvia_registered_vehicles_df")
                            csv_movvia_registered_vehicles = df_movvia_registered_vehicles.to_csv(sep=";", index=False)

                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_movvia_registered_vehicles"
                        ,data=csv_movvia_registered_vehicles.encode("utf-8-sig")
                        ,file_name="Veículos Cadastrados.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                     movvia_registered_vehicles_license_plate = st.text_input(label="Placa", key="Placa - Veículos Cadastrados").upper().strip()
                     movvia_movvia_registered_vehicles_email = st.text_input(label="E-mail", key="E-mail - Veículos Cadastrados").lower().strip()
                with col3:
                    st.write("Selecine um aquivo de placas:")
                    movvia_registered_vehicles_license_plate_file = ""
                    movvia_registered_vehicles_license_plate_file = st.file_uploader("Arquivo - Veículos Cadastrados", type=["xlsx", "xls"], accept_multiple_files=False, label_visibility="collapsed")

                option_movvia = st.session_state.get("report_general_movvia")
                if option_movvia == "movvia_registered_vehicles_search":
                    placeholder_movvia_registered_vehicles.warning("Pesquisando...")
                    movvia_registered_vehicles_cte_licensePlate = ""

                    if movvia_registered_vehicles_license_plate_file:
                        df_movvia_registered_vehicles_excel = pd.read_excel(movvia_registered_vehicles_license_plate_file)

                        if df_movvia_registered_vehicles_excel.shape[1] == 0:
                            placeholder_movvia_registered_vehicles.error("O arquivo não possui dados.")
                            del st.session_state["report_general_movvia"]
                        else:
                            # Pega a primeira coluna
                            first_col = df_movvia_registered_vehicles_excel.iloc[:, 0].dropna().astype(str).str.strip().str.upper()
                            plates = first_col.unique()

                            if len(plates) == 0:
                                placeholder_movvia_registered_vehicles.warning("Nenhuma placa válida encontrada.")
                                st.stop()

                        # Escreve cte
                        movvia_registered_vehicles_license_plate_file.close()
                        movvia_registered_vehicles_cte_licensePlate = ",\n        ".join([f"                                        ('{plate}')" for plate in plates])

                    elif movvia_registered_vehicles_license_plate:
                        movvia_registered_vehicles_cte_licensePlate = f"('{ movvia_registered_vehicles_license_plate}')"

                    if not movvia_registered_vehicles_cte_licensePlate and not movvia_movvia_registered_vehicles_email:
                        placeholder_movvia_registered_vehicles.error("Forneça um arquivo com placas ou informe uma placa.")
                        st.stop()

                    if movvia_registered_vehicles_cte_licensePlate:
                        # Escreve query
                        query_movvia_registered_vehicles = f"""
                            WITH cte_LicensePlate AS (
                                SELECT
                                    C1 AS "licensePlate"
                                FROM (VALUES
                                    {movvia_registered_vehicles_cte_licensePlate}
                                ) AS TB (C1)
                            )
                            SELECT
                                V."licensePlate"                                    AS "Placa"
                                ,V.manufacturer                                     AS "Marca"
                                ,V.model                                            AS "Modelo"
                                ,V.color                                            AS "Cor"
                                ,U.type                                             AS "Tipo"
                                ,CASE
                                    WHEN TRIM(UPPER(U.firstname)) = TRIM(UPPER(U.lastname))
                                        THEN TRIM(U.firstname)
                                    ELSE
                                        TRIM(U.firstname) || ' ' || TRIM(U.lastname)
                                END                                                 AS "Nome do Cliente"
                                ,U.email                                            AS "E-mail"
                                ,U.phone                                            AS "Telefone"
                                ,TO_CHAR(V."createdAt", 'DD/MM/YYYY HH24:MI:SS')    AS "Data de Criação"
                                ,TO_CHAR(V."updatedAt", 'DD/MM/YYYY HH24:MI:SS')    AS "Data de Modificação"
                            FROM public.vehicle                             AS V
                            LEFT JOIN public."user"                         AS U
                                ON U.id = V."userId"
                            LEFT JOIN cte_LicensePlate                      AS LP
                                ON LP."licensePlate" = V."licensePlate"
                            WHERE
                                V."isActive"
                                AND V."isRegular"
                                AND V."deletedAt" IS NULL
                                AND LP."licensePlate" IS NOT NULL
                        """
                    elif movvia_movvia_registered_vehicles_email:
                        # Escreve query
                        query_movvia_registered_vehicles = f"""
                            SELECT
                                V."licensePlate"                                    AS "Placa"
                                ,V.manufacturer                                     AS "Marca"
                                ,V.model                                            AS "Modelo"
                                ,V.color                                            AS "Cor"
                                ,U.type                                             AS "Tipo"
                                ,CASE
                                    WHEN TRIM(UPPER(U.firstname)) = TRIM(UPPER(U.lastname))
                                        THEN TRIM(U.firstname)
                                    ELSE
                                        TRIM(U.firstname) || ' ' || TRIM(U.lastname)
                                END                                                 AS "Nome do Cliente"
                                ,U.email                                            AS "E-mail"
                                ,U.phone                                            AS "Telefone"
                                ,TO_CHAR(V."createdAt", 'DD/MM/YYYY HH24:MI:SS')    AS "Data de Criação"
                                ,TO_CHAR(V."updatedAt", 'DD/MM/YYYY HH24:MI:SS')    AS "Data de Modificação"
                            FROM public.vehicle                         AS V
                            LEFT JOIN public."user"                     AS U
                                ON U.id = V."userId"
                            WHERE
                                V."isActive"
                                AND V."isRegular"
                                AND V."deletedAt" IS NULL
                                AND U.email = '{movvia_movvia_registered_vehicles_email}'
                        """

                    # Consulta ao banco
                    df_query_movvia_registered_vehicles = pd.read_sql(query_movvia_registered_vehicles, engine_attri)

                    st.session_state["movvia_registered_vehicles_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_query_movvia_registered_vehicles.empty:
                        # Salva o resultado
                        st.session_state["movvia_registered_vehicles_df"] = df_query_movvia_registered_vehicles
                        st.session_state["movvia_registered_vehicles_exists_df"] = True
                        # Exibe em tela
                        placeholder_movvia_registered_vehicles.empty()
                    else:
                        st.session_state["movvia_registered_vehicles_exists_df"] = False

                    if "report_general_movvia" in st.session_state:
                        del st.session_state["report_general_movvia"]
                        st.rerun()

                if "report_general_movvia" in st.session_state:
                    del st.session_state["report_general_movvia"]

                if "movvia_registered_vehicles_exists_df" in st.session_state:
                    if not st.session_state.get("movvia_registered_vehicles_exists_df", True):
                        placeholder_movvia_registered_vehicles.error("Nenhum registro encontrado.")

                if "movvia_registered_vehicles_df" in st.session_state:
                    if not st.session_state.get("movvia_registered_vehicles_df").empty and st.session_state.get("movvia_registered_vehicles_exists_df"):
                        # Exibe em tela
                        st.write(st.session_state["movvia_registered_vehicles_datetime"])
                        st.dataframe(st.session_state.get("movvia_registered_vehicles_df"), height=600, hide_index=True, width=1400)


            # ||=== CONSULTA DE PASSAGEM ===================================================================================================||
            elif option_general == "general_search_passage_by_plate":
                placeholder_general_search_passage_by_plate = st.empty()
                st.write("Passagens -- Consulta por Placa")

                df_general_search_passage_by_plate = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="general_search_passage_by_plate_bt",  use_container_width=True):
                        st.session_state["general_search_passage_by_plate"] = True
                    csv_search_passage_by_plate = df_general_search_passage_by_plate.to_csv(index=False, sep=";")
                    if "df_general_search_passage_by_plate" in st.session_state:
                        if not st.session_state.get("df_general_search_passage_by_plate").empty:
                            df_general_search_passage_by_plate = st.session_state.get("df_general_search_passage_by_plate")
                            csv_search_passage_by_plate = df_general_search_passage_by_plate.to_csv(index=False, sep=";")
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_search_passage_by_plate"
                        ,data=csv_search_passage_by_plate.encode("utf-8-sig")
                        ,file_name="Passagens por Placas.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    general_search_passage_by_plate_license_plate = st.text_input(label="Placa do Veículo", max_chars=10, key="general_search_passage_by_plate_license_plate").upper().strip()
                with col3:
                    general_search_passage_by_plate_initial_date = st.date_input("Data Inicial:", value=dt.date.today() - dt.timedelta(days=15), format="DD/MM/YYYY", key="general_search_passage_by_plate_initial_date")
                    general_search_passage_by_plate_ending_date = st.date_input("Data Inicial:", value=dt.date.today() - dt.timedelta(days=1), format="DD/MM/YYYY", key="general_search_passage_by_plate_ending_date")

                if st.session_state.get("general_search_passage_by_plate", False):
                     # Verifica validade das datas
                    general_search_passage_by_plate_date_diff = general_search_passage_by_plate_ending_date - general_search_passage_by_plate_initial_date
                    if general_search_passage_by_plate_date_diff.days < 0:
                        placeholder_general_search_passage_by_plate.error("Processo Cancelado. Período de datas não confere.")
                        if "general_search_passage_by_plate" in st.session_state:
                            del st.session_state["general_search_passage_by_plate"]
                        st.stop()
                    # Verifica placa
                    elif general_search_passage_by_plate_license_plate == "":
                        placeholder_general_search_passage_by_plate.error("Processo Cancelado. Placa Inválida.")
                        if "general_search_passage_by_plate" in st.session_state:
                            del st.session_state["general_search_passage_by_plate"]
                        st.stop()
                    
                    placeholder_general_search_passage_by_plate.warning("Pesquisando...")

                    # Escreve query
                    query = f"""
                        WITH cte_OCAC AS (
                            SELECT
                                ChargeId
                                ,MAX(OrderId) AS OrderId
                            FROM PD.attri.tb_Order_Charges_Arr_Charge WITH (NOLOCK)
                            GROUP BY
                                ChargeId
                        )
                        ,cte_TEMP AS (
                            SELECT DISTINCT
                                TFS.FinancialTransactionID
                                ,T.External_Correlation_Id                          AS TransactionId
                                ,TFS.OccurrenceDate                                 AS OccurrenceDatetime
                                ,L.description                                      AS Location_Descripton
                                ,TFS.LicensePlate
                                ,TFS.BaseAmount                                     AS RateAmount_TFS
                                ,TFS.DiscountWebDBT                                 AS DiscountDbt_TFS
                                ,TFS.DiscountWebDUF                                 AS DiscountDuf_TFS
                                ,TFS.FeeWeb                                         AS Fee_TFS
                                ,TFS.PaidAmount                                     AS NetAmount_TFS
                                ,TFS.TransactionStatus                              AS PaymentStatus_TFS
                                ,TFS.PaymentDatetime                                AS PaymentDatetime_TFS
                                ,C.RateAmount * 0.01                                AS RateAmount_Web
                                ,C.DiscountDbt * 0.01                               AS DiscountDbt_Web
                                ,C.DiscountDuf * 0.01                               AS DiscountDuf_Web
                                ,C.Fee * 0.01                                       AS Fee_Web
                                ,(C.RateAmount + C.Fee - 
                                    (C.DiscountDbt + C.DiscountDuf)) * 0.01         AS NetAmount_Web
                                ,CASE
                                    WHEN O.[Status] IS NOT NULL
                                        THEN O.[Status]
                                    ELSE
                                        C.[Status]
                                END                                                 AS PaymentStatus_Web
                                ,O.PaidAt                                           AS PaymentDatetime_Web
                                ,TFS.VehicleClass
                                ,V.vehicle_class_description                        AS VehicleClassDescription
                            FROM PD.kapsch.vw_TransactionFinalStatus                        AS TFS WITH (NOLOCK)
                            LEFT JOIN PD.kapsch.vw_Transaction                              AS T WITH (NOLOCK)
                                ON T.Passage_Event_Id = TFS.PassageID
                            LEFT JOIN PD.kapsch.tb_Location                                 AS L
                                ON L.[description] = TFS.LocationDescription
                            LEFT JOIN PD.kapsch.tb_VehicleClass                             AS V
                                ON V.vehicle_class_id = TFS.VehicleClass
                            LEFT JOIN PD.attri.tb_Charge                                    AS C WITH (NOLOCK)
                                ON C.FinancialTransactionId = TFS.FinancialTransactionID
                            LEFT JOIN cte_OCAC                                              AS OCAC
                                ON OCAC.ChargeId = C.Id
                            LEFT JOIN PD.attri.tb_Order                                     AS O WITH (NOLOCK)
                                ON O.Id = OCAC.OrderId
                            WHERE
                                TFS.LicensePlate = '{general_search_passage_by_plate_license_plate}'
                                AND CAST(TFS.OccurrenceDate AS DATE) BETWEEN '{general_search_passage_by_plate_initial_date.strftime('%Y-%m-%d')}' AND '{general_search_passage_by_plate_ending_date.strftime('%Y-%m-%d')}'
                        )
                        SELECT
                            FORMAT(FinancialTransactionId, '0')                     AS [Transação Financeira]
                            ,LOWER(TransactionId)                                   AS [Transação]
                            ,FORMAT(OccurrenceDatetime, 'dd/MM/yyyy HH:mm:ss')      AS [Data da Passagem]
                            ,Location_Descripton                                    AS Localidade
                            ,LicensePlate                                           AS Placa
                            ,'R$    ' + FORMAT(CASE
                                WHEN RateAmount_Web IS NOT NULL
                                    THEN RateAmount_Web
                                ELSE
                                    RateAmount_TFS
                                END
                            ,'0.00')                                                AS [Valor da Passagem]
                            ,'R$    ' + FORMAT(CASE
                                WHEN DiscountDbt_Web IS NOT NULL
                                    THEN DiscountDbt_Web
                                ELSE
                                    DiscountDbt_TFS
                                END
                            ,'0.00')                                                AS [Desconto DBT]
                            ,'R$    ' + FORMAT(CASE
                                WHEN DiscountDuf_Web IS NOT NULL
                                    THEN DiscountDuf_Web
                                ELSE
                                    DiscountDuf_TFS
                                END
                            ,'0.00')                                                AS [Desconto DUF]
                            ,'R$    ' + FORMAT(CASE
                                WHEN Fee_Web IS NOT NULL
                                    THEN Fee_Web
                                ELSE
                                    Fee_TFS
                                END
                            ,'0.00')                                                AS [Acréscimo]
                            ,'R$    ' + FORMAT(CASE
                                WHEN NetAmount_Web IS NOT NULL
                                    THEN NetAmount_Web
                                ELSE
                                    NetAmount_TFS
                                END
                            ,'0.00')                                                AS [Valor Cobrado]
                            ,CASE
                                WHEN PaymentStatus_Web = 'open'
                                    THEN 'Aberto'
                                WHEN PaymentStatus_Web = 'paid'
                                    THEN 'Pago'
                                WHEN PaymentStatus_Web = 'canceled'
                                    THEN 'Cancelado'
                                WHEN PaymentStatus_Web = 'free'
                                    THEN 'Isento'
                                WHEN PaymentStatus_Web = 'declined'
                                    THEN 'Recusado'
                                WHEN PaymentStatus_Web IS NULL
                                    THEN PaymentStatus_TFS
                            END                                                     AS [Status Pagamento]
                            ,FORMAT(CASE
                                WHEN PaymentDatetime_Web IS NOT NULL
                                    THEN PaymentDatetime_Web
                                ELSE
                                    PaymentDatetime_TFS
                                END
                            ,'dd/MM/yyyy HH:mm:ss')                                 AS [Data do Pagamento]
                            ,VehicleClass                                           AS [Classificação do Veiculo]
                            ,VehicleClassDescription                                AS [Descrição da Classificação do Veiculo]
                        FROM cte_TEMP
                        ORDER BY
                            OccurrenceDatetime
                            ,Location_Descripton
                    """

                    # Consulta ao banco
                    df_general_search_passage_by_plate = pd.read_sql(query, engine_pd)
                    
                    st.session_state["general_search_passage_by_plate_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_general_search_passage_by_plate.empty:
                        # Exibe em tela
                        st.session_state["df_general_search_passage_by_plate"] = df_general_search_passage_by_plate
                        csv_search_passage_by_plate = df_general_search_passage_by_plate.to_csv(index=False, sep=";")
                        placeholder_general_search_passage_by_plate.empty()
                    else:
                        placeholder_general_search_passage_by_plate.error("Nenhum registro encontrado.")

                    del st.session_state["general_search_passage_by_plate"]
                    st.rerun()

                if "df_general_search_passage_by_plate" in st.session_state:
                    if not st.session_state.get("df_general_search_passage_by_plate").empty:
                        # Exibe em tela
                        st.write(st.session_state["general_search_passage_by_plate_datetime"])
                        st.dataframe(st.session_state.get("df_general_search_passage_by_plate"), height=600, hide_index=True)




# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    BACKOFFICE                                                                                                                          ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_backoffice_tab:
    with tab_backoffice:

        col_menu, col_content = st.columns([col_menu_width, col_content_width])
        with col_menu:
            st.markdown("##### Kapsch")
            if st.button("Status Final da Transação", use_container_width=True):
                st.session_state["report_backoffice"] = "kapsch_tfs"
                if "report_backoffice_kapsch" in st.session_state:
                    del st.session_state["report_backoffice_kapsch"]
            if st.button("Lista de Isentos", use_container_width=True):
                st.session_state["report_backoffice"] = "kapsch_exempt_list"
                if "report_backoffice_kapsch" in st.session_state:
                    del st.session_state["report_backoffice_kapsch"]

            st.markdown("##### Nevada")
            if st.button("Validações", use_container_width=True):
                st.session_state["report_backoffice"] = "nevada_capture"
                if "report_backoffice_nevada" in st.session_state:
                    del st.session_state["report_backoffice_nevada"]

            if st.session_state.get("access_level_id") <= 2:
                st.markdown("##### Próspera")
                if st.button("Placas Cadastradas", use_container_width=True):
                    st.session_state["report_backoffice"] = "prospera_serach_plates"
                    if "report_backoffice_prospera" in st.session_state:
                        del st.session_state["report_backoffice_prospera"]

            st.markdown("##### Consultas Gerais")
            if st.button("Passagens em Aberto", use_container_width=True):
                st.session_state["report_backoffice"] = "general_open_passages"
                if "report_backoffice_general" in st.session_state:
                    del st.session_state["report_backoffice_general"]
            if st.button("Passagens de Isentos", use_container_width=True):
                st.session_state["report_backoffice"] = "general_exempt_passages"
                if "report_backoffice_general" in st.session_state:
                    del st.session_state["report_backoffice_general"]

        with col_content:
            option_backoffice = st.session_state.get("report_backoffice")

            # ||=== GERAL ==================================================================================================================||
            if option_backoffice == "general_open_passages":
                st.write("Consultas Gerais -- Passagens em Aberto")
                df_backoffice_general_open_passages = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="general_open_passages_search",  use_container_width=True):
                        st.session_state["report_backoffice_general"] = "general_open_passages_search"
                    csv_backoffice_general_open_passages = df_backoffice_general_open_passages.to_csv(index=False, sep=";")
                    if "backoffice_general_open_passages_df" in st.session_state:
                        if not st.session_state.get("backoffice_general_open_passages_df").empty:
                            df_backoffice_general_open_passages = st.session_state.get("backoffice_general_open_passages_df")
                            csv_backoffice_general_open_passages = df_backoffice_general_open_passages.to_csv(index=False, sep=";")
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_backoffice_general_open_passages"
                        ,data=csv_backoffice_general_open_passages.encode("utf-8-sig")
                        ,file_name="Passagens em Aberto.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    backoffice_general_open_passages_initial_date = st.date_input("Data Inicial:", value=dt.date.today() - dt.timedelta(days=44), format="DD/MM/YYYY", key="backoffice_general_open_passages_initial_date")
                    backoffice_general_open_passages_ending_date = st.date_input("Data Inicial:", value=dt.date.today() - dt.timedelta(days=30), format="DD/MM/YYYY", key="backoffice_general_open_passages_ending_date")
                with col3:
                    backoffice_general_open_passages_range_date = st.number_input("Intervalo de Dias de Pagamentos por OSA:", value=90, key="backoffice_general_open_passages_range_date")

                placeholder_backoffice_general_open_passages = st.empty()

                option_backoffice_general = st.session_state.get("report_backoffice_general")
                if option_backoffice_general == "general_open_passages_search":
                    start_time = time.time()
                    placeholder_backoffice_general_open_passages.warning("Pesquisando...")

                    # Verifica validade das datas
                    backoffice_general_open_passages_date_diff = backoffice_general_open_passages_ending_date - backoffice_general_open_passages_initial_date
                    if backoffice_general_open_passages_date_diff.days < 0 or backoffice_general_open_passages_date_diff.days > 31:
                        placeholder_backoffice_general_open_passages.error("Processo Cancelado. Período de datas não confere.")
                        if "report_backoffice_general" in st.session_state:
                            del st.session_state["report_backoffice_general"]
                        st.stop()

                    backoffice_general_open_passages_range_date = abs(backoffice_general_open_passages_range_date)

                    # Escreve query
                    query_backoffice_general_open_passages = f"""
                        WITH cte_OCAC AS (
                            SELECT
                                ChargeId
                                ,MAX(OrderId) AS OrderId
                            FROM PD.attri.tb_Order_Charges_Arr_Charge WITH (NOLOCK)
                            GROUP BY
                                ChargeId
                        )
                        ,cte_DateOsa AS (
                            SELECT
                                LicensePlate
                                ,MAX(CASE
                                    WHEN PaymentMethod = 'ConectCar'
                                        THEN OccurrenceDate
                                    ELSE
                                        NULL
                                END)                                            AS ConectCar
                                ,MAX(CASE
                                    WHEN PaymentMethod = 'GreenPass'
                                        THEN OccurrenceDate
                                    ELSE
                                        NULL
                                END)                                            AS GreenPass
                                ,MAX(CASE
                                    WHEN PaymentMethod = 'MoveMais'
                                        THEN OccurrenceDate
                                    ELSE
                                        NULL
                                END)                                            AS MoveMais
                                ,MAX(CASE
                                    WHEN PaymentMethod = 'SemParar'
                                        THEN OccurrenceDate
                                    ELSE
                                        NULL
                                END)                                            AS SemParar
                                ,MAX(CASE
                                    WHEN PaymentMethod = 'Veloe'
                                        THEN OccurrenceDate
                                    ELSE
                                        NULL
                                END)                                            AS Veloe
                            FROM PD.kapsch.vw_TransactionFinalStatus WITH (NOLOCK)
                            WHERE
                                PaymentMethod IN (
                                    'SemParar'
                                    ,'ConectCar'
                                    ,'GreenPass'
                                    ,'Veloe'
                                    ,'MoveMais'
                                )
                                AND TransactionStatus = 'Pago Pela OSA'
                                AND CAST(OccurrenceDate AS DATE) >= DATEADD(DAY, -{backoffice_general_open_passages_range_date}, CAST('{backoffice_general_open_passages_initial_date.strftime('%Y-%m-%d')}' AS DATE))
                            GROUP BY
                                LicensePlate
                        )

                        SELECT DISTINCT
                            LOWER(T.External_Correlation_Id)                    AS [Transação]
                            ,FORMAT(TFS.FinancialTransactionID, '0')            AS [Transação Financeira]
                            ,TFS.OccurrenceDate
                            ,FORMAT(TFS.OccurrenceDate, 'dd/MM/yyyy HH:mm:ss')  AS [Data da Passagem]
                            ,TFS.LocationDescription                            AS [Localidade]
                            ,TFS.LicensePlate                                   AS [Placa]
                            ,CASE
                                WHEN LEFT(TFS.LicensePlate, 4) = 'XXX0'
                                OR TFS.LicensePlate IN ('CSG00001', 'YYY99999')
                                    THEN 'Placa Genérica'
                                ELSE
                                    T.Country_Code
                            END                                                 AS [Código do País]
                            ,TFS.VehicleClass                                   AS [Categoria do Veículo]
                            ,'R$    ' + FORMAT(C.RateAmount * 0.01, '0.00')     AS [Tarifa]
                            ,TFS.TransactionStatus                              AS [Status kapsch]
                            ,CASE
                                WHEN C.[CreatedAt] IS NULL
                                    THEN 'N/D'
                                WHEN C.[Status] = 'paid'
                                    THEN 'Pago'
                                WHEN C.[Status] = 'open'
                                    THEN 'Aberto'
                                WHEN C.[Status] = 'canceled'
                                    THEN 'Cancelado'
                                WHEN C.[Status] = 'free'
                                    THEN 'Isento'
                                WHEN C.[Status] = 'declined'
                                    THEN 'Recusado'
                                ELSE
                                    C.[Status]
                            END                                             AS [Status Plataforma]
                            ,FORMAT(C.CreatedAt, 'dd/MM/yyyy HH:mm:ss')     AS [Data da Criação Plataforma]
                            ,FORMAT(O.PaidAt, 'dd/MM/yyyy HH:mm:ss')        AS [Data de Pagamento]
                            ,CASE
                                WHEN (
                                    OSA.ConectCar IS NOT NULL
                                    AND OSA.ConectCar > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                )
                                OR (
                                    OSA.GreenPass IS NOT NULL
                                    AND OSA.GreenPass > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                )
                                OR (
                                    OSA.MoveMais IS NOT NULL
                                    AND OSA.MoveMais > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                )
                                OR (
                                    OSA.SemParar IS NOT NULL
                                    AND OSA.SemParar > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                )
                                OR (
                                    OSA.Veloe IS NOT NULL
                                    AND OSA.Veloe > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                )
                                    THEN 'Sim'
                                ELSE
                                    'Não'
                            END                                             AS [Pagamento por OSA]
                            ,CASE
                                WHEN OSA.ConectCar > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                    THEN FORMAT(OSA.ConectCar, 'dd/MM/yyyy HH:mm:ss')
                                ELSE
                                    NULL
                            END                                             AS ConectCar
                            ,CASE
                                WHEN OSA.GreenPass > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                    THEN FORMAT(OSA.GreenPass, 'dd/MM/yyyy HH:mm:ss')
                                ELSE
                                    NULL
                            END                                             AS GreenPass
                            ,CASE
                                WHEN OSA.MoveMais > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                    THEN FORMAT(OSA.MoveMais, 'dd/MM/yyyy HH:mm:ss')
                                ELSE
                                    NULL
                            END                                             AS [Move Mais]
                            ,CASE
                                WHEN OSA.SemParar > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                    THEN FORMAT(OSA.SemParar, 'dd/MM/yyyy HH:mm:ss')
                                ELSE
                                    NULL
                            END                                             AS [Sem Parar]
                            ,CASE
                                WHEN OSA.Veloe > DATEADD(DAY, -{backoffice_general_open_passages_range_date}, C.DatetimeOccurrence)
                                    THEN FORMAT(OSA.Veloe, 'dd/MM/yyyy HH:mm:ss')
                                ELSE
                                    NULL
                            END                                             AS Veloe
                        FROM PD.kapsch.vw_TransactionFinalStatus                            AS TFS WITH (NOLOCK)
                        LEFT JOIN PD.attri.tb_Charge                                        AS C WITH (NOLOCK)
                            ON C.FinancialTransactionId = TFS.FinancialTransactionID
                        LEFT JOIN cte_OCAC                                                  AS OCAC
                            ON OCAC.ChargeId = C.Id
                        LEFT JOIN PD.attri.tb_Order                                         AS O WITH (NOLOCK)
                            ON O.Id = OCAC.OrderId
                        LEFT JOIN PD.kapsch.vw_Transaction                                  AS T WITH (NOLOCK)
                            ON T.Passage_Event_Id = TFS.PassageID
                        LEFT JOIN cte_DateOsa                                               AS OSA
                            ON OSA.LicensePlate = TFS.LicensePlate
                        WHERE
                            CAST(TFS.OccurrenceDate AS DATE) BETWEEN '{backoffice_general_open_passages_initial_date.strftime('%Y-%m-%d')}' AND '{backoffice_general_open_passages_ending_date.strftime('%Y-%m-%d')}'
                            AND TFS.TransactionStatus NOT IN (
                                'Pago Pela Cupom VP'
                                ,'Pago Pela OSA'
                                ,'Pago Pela VP Tag'
                                ,'Pago Pela Web'
                                ,'Rejeição de OSA'
                            )
                        ORDER BY
                            TFS.LicensePlate
                            ,TFS.OccurrenceDate
                    """

                    # Consulta ao banco
                    df_backoffice_general_open_passages = pd.read_sql(query_backoffice_general_open_passages, engine_pd)

                    duration_time_float = time.time() - start_time
                    duration_time = dt.timedelta(seconds=duration_time_float)
                    st.session_state["backoffice_general_open_passages_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}|Tempo de Execução: {str(duration_time)[:-3]}"

                    # Constroi dataframe
                    if not df_backoffice_general_open_passages.empty:
                        df_backoffice_general_open_passages = df_backoffice_general_open_passages.drop(columns=["OccurrenceDate"])
                        # Exibe em tela
                        st.session_state["backoffice_general_open_passages_df"] = df_backoffice_general_open_passages
                        csv_backoffice_general_open_passages = df_backoffice_general_open_passages.to_csv(index=False, sep=";")
                        placeholder_backoffice_general_open_passages.empty()
                    else:
                        placeholder_backoffice_general_open_passages.error("Nenhum registro encontrado.")

                    del st.session_state["report_backoffice_general"]
                    st.rerun()

                if "backoffice_general_open_passages_df" in st.session_state:
                    if not st.session_state.get("backoffice_general_open_passages_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("backoffice_general_open_passages_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["backoffice_general_open_passages_datetime"].split("|")[0]}\t\t{st.session_state["backoffice_general_open_passages_datetime"].split("|")[1]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("backoffice_general_open_passages_df"), height=600, hide_index=True)
            
            
            elif option_backoffice == "general_exempt_passages":
                st.write("Consultas Gerais -- Passagens de Isentos")
                df_backoffice_general_exempt_passages = pd.DataFrame()

                st.write("Pesquise por data ou por placa")
                col1, col2, col3, col4, col5, col6 = st.columns([30, 2, 30, 2, 30, 106])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="general_exempt_passages_search",  use_container_width=True):
                        st.session_state["report_backoffice_general"] = "general_exempt_passages_search"
                    csv_backoffice_general_exempt_passages = df_backoffice_general_exempt_passages.to_csv(index=False, sep=";")
                    if "backoffice_general_exempt_passages_df" in st.session_state:
                        if not st.session_state.get("backoffice_general_exempt_passages_df").empty:
                            df_backoffice_general_exempt_passages = st.session_state.get("backoffice_general_exempt_passages_df")
                            csv_backoffice_general_exempt_passages = df_backoffice_general_exempt_passages.to_csv(index=False, sep=";")
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_backoffice_general_exempt_passages"
                        ,data=csv_backoffice_general_exempt_passages.encode("utf-8-sig")
                        ,file_name="Passagens de Isentos.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    fn.vertical_divider(140)
                with col3:
                    backoffice_general_exempt_passages_initial_date = st.date_input("Data Inicial:", value=fn.beginning_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="backoffice_general_exempt_passages_initial_date")
                    backoffice_general_exempt_passages_ending_date = st.date_input("Data Inicial:", value=fn.end_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="backoffice_general_exempt_passages_ending_date")
                with col4:
                    fn.vertical_divider(140)
                with col5:
                    backoffice_general_exempt_passages_license_plate = st.text_input(label="Placa", key="backoffice_general_exempt_passages_license_plate")

                placeholder_backoffice_general_exempt_passages = st.empty()

                option_backoffice_general = st.session_state.get("report_backoffice_general")
                if option_backoffice_general == "general_exempt_passages_search":
                    start_time = time.time()
                    placeholder_backoffice_general_exempt_passages.warning("Pesquisando...")

                    # Verifica placa e validade das datas
                    if not backoffice_general_exempt_passages_license_plate:
                        backoffice_general_exempt_passages_date_diff = backoffice_general_exempt_passages_ending_date - backoffice_general_exempt_passages_initial_date
                        if backoffice_general_exempt_passages_date_diff.days < 0 or backoffice_general_exempt_passages_date_diff.days > 31:
                            placeholder_backoffice_general_exempt_passages.error("Processo Cancelado. Período de datas não confere.")
                            if "report_backoffice_general" in st.session_state:
                                del st.session_state["report_backoffice_general"]
                            st.stop()

                        # Escreve query
                        query_backoffice_general_exempt_passages = f"""
                            WITH cte_Transaction AS (
                                SELECT
                                    External_Correlation_Id
                                    ,Passage_Event_Id
                                FROM PD.kapsch.vw_Transaction
                                WHERE
                                    CAST(Datetime_Local_Occurrence AS DATE) BETWEEN CAST((
                                        SELECT
                                            MIN(DatetimeOccurrence)
                                        FROM PD.attri.tb_Charge
                                        WHERE
                                            CAST(CreatedAt AS DATE) BETWEEN '{backoffice_general_exempt_passages_initial_date.strftime("%Y-%m-%d")}' AND '{backoffice_general_exempt_passages_ending_date.strftime("%Y-%m-%d")}'
                                    ) AS DATE) AND CAST((
                                        SELECT
                                            MAX(DatetimeOccurrence)
                                        FROM PD.attri.tb_Charge
                                        WHERE
                                            CAST(CreatedAt AS DATE) BETWEEN '{backoffice_general_exempt_passages_initial_date.strftime("%Y-%m-%d")}' AND '{backoffice_general_exempt_passages_ending_date.strftime("%Y-%m-%d")}'
                                    ) AS DATE)
                            ),cte_TFS AS (
                                SELECT
                                    PassageID
                                    ,FinancialTransactionID
                                    ,LocationDescription
                                FROM PD.kapsch.vw_TransactionFinalStatus
                                WHERE
                                    CAST(OccurrenceDate AS DATE) BETWEEN CAST((
                                        SELECT
                                            MIN(DatetimeOccurrence)
                                        FROM PD.attri.tb_Charge
                                        WHERE
                                            CAST(CreatedAt AS DATE) BETWEEN '{backoffice_general_exempt_passages_initial_date.strftime("%Y-%m-%d")}' AND '{backoffice_general_exempt_passages_ending_date.strftime("%Y-%m-%d")}'
                                    ) AS DATE) AND CAST((
                                        SELECT
                                            MAX(DatetimeOccurrence)
                                        FROM PD.attri.tb_Charge
                                        WHERE
                                            CAST(CreatedAt AS DATE) BETWEEN '{backoffice_general_exempt_passages_initial_date.strftime("%Y-%m-%d")}' AND '{backoffice_general_exempt_passages_ending_date.strftime("%Y-%m-%d")}'
                                    ) AS DATE)
                            ),cte_Charge AS (
                                SELECT DISTINCT
                                    FinancialTransactionId
                                    ,DatetimeOccurrence
                                    ,LicensePlate
                                    ,VehicleClassRated
                                    ,RateAmount
                                    ,[Status]
                                    ,CreatedAt
                                    ,DiscountDuf
                                    ,DiscountDbt
                                    ,Fee
                                    ,PaymentRegisteredAt
                                FROM PD.attri.tb_Charge WITH (NOLOCK)
                                WHERE
                                    CAST(CreatedAt AS DATE) BETWEEN '{backoffice_general_exempt_passages_initial_date.strftime("%Y-%m-%d")}' AND '{backoffice_general_exempt_passages_ending_date.strftime("%Y-%m-%d")}'
                            )
                            SELECT DISTINCT
                                LOWER(T.External_Correlation_Id)                        AS TransactionId
                                ,C.FinancialTransactionId
                                ,T.Passage_Event_Id
                                ,SI.[Status]                                            AS StatusNevada
                                ,C.CreatedAt
                                ,C.LicensePlate
                                ,C.DatetimeOccurrence
                                ,TFS.LocationDescription
                                ,C.VehicleClassRated
                                ,C.RateAmount * 0.01                                    AS RateAmount
                                ,C.DiscountDuf * 0.01                                   AS DiscountDuf
                                ,C.DiscountDbt * 0.01                                   AS DiscountDbt
                                ,C.Fee * 0.01                                           AS Fee
                                ,CASE
                                    WHEN C.RateAmount > 0
                                        THEN (C.RateAmount + C.Fee -
                                            C.DiscountDuf - C.DiscountDbt) * 0.01
                                    ELSE
                                        0
                                END                                                     AS NetAmount
                                ,CASE
                                    WHEN C.[Status] = 'open'
                                        THEN 'Aberto'
                                    WHEN C.[Status] = 'paid'
                                        THEN 'Pago'
                                    WHEN C.[Status] = 'canceled'
                                        THEN 'Cancelado'
                                    WHEN C.[Status] = 'free'
                                        THEN 'Isento'
                                    ELSE
                                        C.[Status]
                                END                                                     AS [Status]
                                ,C.PaymentRegisteredAt                                  AS PaymentDatetime
                                ,NULL                                                   AS Vazio
                                ,EL.ExemptGroup
                                ,EL.Location                                            AS ExemptLocation
                                ,EL.WeekDays                                            AS ExemptDays
                                ,EL.ActiveFrom
                                ,EL.ActiveTo
                                ,CASE
                                    WHEN EL.Active = 1
                                        THEN 'Sim'
                                    ELSE
                                        'Não'
                                END                                                     AS [Active]
                            FROM cte_Charge                                                     AS C
                            LEFT JOIN PD.kapsch.tb_ExemptList                                   AS EL WITH (NOLOCK)
                                ON EL.LicensePlate = C.LicensePlate
                            LEFT JOIN cte_TFS                                                   AS TFS
                                ON TFS.FinancialTransactionId = C.FinancialTransactionId
                            LEFT JOIN cte_Transaction                                           AS T
                                ON T.Passage_Event_Id = TFS.PassageID
                            LEFT JOIN PD.nevada.tb_CaptureReport                                AS SI WITH (NOLOCK)
                                ON SI.Transaction_Id = TFS.FinancialTransactionID
                            WHERE
                                EL.LicensePlate IS NOT NULL
                                AND C.CreatedAt IS NOT NULL
                            ORDER BY
                                C.DatetimeOccurrence
                        """
                    else:
                        backoffice_general_exempt_passages_license_plate = backoffice_general_exempt_passages_license_plate.upper().strip()

                        # Escreve query
                        query_backoffice_general_exempt_passages = f"""
                            WITH cte_Transaction AS (
                                SELECT
                                    External_Correlation_Id
                                    ,Passage_Event_Id
                                FROM PD.kapsch.vw_Transaction
                                WHERE
                                    License_Plate = '{backoffice_general_exempt_passages_license_plate}'
                            ),cte_TFS AS (
                                SELECT
                                    PassageID
                                    ,FinancialTransactionID
                                    ,LocationDescription
                                FROM PD.kapsch.vw_TransactionFinalStatus
                                WHERE
                                    LicensePlate = '{backoffice_general_exempt_passages_license_plate}'
                            ),cte_Charge AS (
                                SELECT DISTINCT
                                    FinancialTransactionId
                                    ,DatetimeOccurrence
                                    ,LicensePlate
                                    ,VehicleClassRated
                                    ,RateAmount
                                    ,[Status]
                                    ,CreatedAt
                                    ,DiscountDuf
                                    ,DiscountDbt
                                    ,Fee
                                    ,PaymentRegisteredAt
                                FROM PD.attri.tb_Charge WITH (NOLOCK)
                                WHERE
                                    LicensePlate = '{backoffice_general_exempt_passages_license_plate}'
                            )
                            SELECT DISTINCT
                                LOWER(T.External_Correlation_Id)                        AS TransactionId
                                ,C.FinancialTransactionId
                                ,T.Passage_Event_Id
                                ,SI.[Status]                                            AS StatusNevada
                                ,C.CreatedAt
                                ,C.LicensePlate
                                ,C.DatetimeOccurrence
                                ,TFS.LocationDescription
                                ,C.VehicleClassRated
                                ,C.RateAmount * 0.01                                    AS RateAmount
                                ,C.DiscountDuf * 0.01                                   AS DiscountDuf
                                ,C.DiscountDbt * 0.01                                   AS DiscountDbt
                                ,C.Fee * 0.01                                           AS Fee
                                ,CASE
                                    WHEN C.RateAmount > 0
                                        THEN (C.RateAmount + C.Fee -
                                            C.DiscountDuf - C.DiscountDbt) * 0.01
                                    ELSE
                                        0
                                END                                                     AS NetAmount
                                ,CASE
                                    WHEN C.[Status] = 'open'
                                        THEN 'Aberto'
                                    WHEN C.[Status] = 'paid'
                                        THEN 'Pago'
                                    WHEN C.[Status] = 'canceled'
                                        THEN 'Cancelado'
                                    WHEN C.[Status] = 'free'
                                        THEN 'Isento'
                                    ELSE
                                        C.[Status]
                                END                                                     AS [Status]
                                ,C.PaymentRegisteredAt                                  AS PaymentDatetime
                                ,NULL                                                   AS Vazio
                                ,EL.ExemptGroup
                                ,EL.Location                                            AS ExemptLocation
                                ,EL.WeekDays                                            AS ExemptDays
                                ,EL.ActiveFrom
                                ,EL.ActiveTo
                                ,CASE
                                    WHEN EL.Active = 1
                                        THEN 'Sim'
                                    ELSE
                                        'Não'
                                END                                                     AS [Active]
                            FROM cte_Charge                                                     AS C
                            LEFT JOIN PD.kapsch.tb_ExemptList                                   AS EL WITH (NOLOCK)
                                ON EL.LicensePlate = C.LicensePlate
                            LEFT JOIN cte_TFS                                                   AS TFS
                                ON TFS.FinancialTransactionId = C.FinancialTransactionId
                            LEFT JOIN cte_Transaction                                           AS T
                                ON T.Passage_Event_Id = TFS.PassageID
                            LEFT JOIN PD.nevada.tb_CaptureReport                                AS SI WITH (NOLOCK)
                                ON SI.Transaction_Id = TFS.FinancialTransactionID
                            WHERE
                                EL.LicensePlate IS NOT NULL
                                AND C.CreatedAt IS NOT NULL
                            ORDER BY
                                C.DatetimeOccurrence
                        """

                    # Consulta ao banco
                    df_backoffice_general_exempt_passages = pd.read_sql(query_backoffice_general_exempt_passages, engine_pd)

                    duration_time_float = time.time() - start_time
                    duration_time = dt.timedelta(seconds=duration_time_float)
                    st.session_state["backoffice_general_exempt_passages_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}|Tempo de Execução: {str(duration_time)[:-3]}"

                    # Constroi dataframe
                    st.session_state["backoffice_general_exempt_passages_df"] = df_backoffice_general_exempt_passages
                    placeholder_backoffice_general_exempt_passages.empty()

                    del st.session_state["report_backoffice_general"]
                    st.rerun()

                if "backoffice_general_exempt_passages_df" in st.session_state:
                    if not st.session_state.get("backoffice_general_exempt_passages_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("backoffice_general_exempt_passages_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["backoffice_general_exempt_passages_datetime"].split("|")[0]}\t\t{st.session_state["backoffice_general_exempt_passages_datetime"].split("|")[1]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("backoffice_general_exempt_passages_df"), height=600, hide_index=True)
                    else:
                        placeholder_backoffice_general_exempt_passages.error("Nenhum registro encontrado.")
                        if "backoffice_general_exempt_passages_df" in st.session_state:
                            del st.session_state["backoffice_general_exempt_passages_df"]


            # ||=== PRÓSPERA ===============================================================================================================||
            if option_backoffice == "prospera_serach_plates":
                st.write("Próspera -- Placas Cadastradas")
                df_prospera_serach_plates = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="prospera_plates_search",  use_container_width=True):
                        st.session_state["report_backoffice_prospera"] = "prospera_plates_search"
                    csv_prospera_serach_plates = df_prospera_serach_plates.to_csv(index=False, sep=";")
                    if "prospera_serach_plates_df" in st.session_state:
                        if not st.session_state.get("prospera_serach_plates_df").empty:
                            df_prospera_serach_plates = st.session_state.get("prospera_serach_plates_df")
                            csv_prospera_serach_plates = df_prospera_serach_plates.to_csv(index=False, sep=";")
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_prospera_serach_plates"
                        ,data=csv_prospera_serach_plates.encode("utf-8-sig")
                        ,file_name="Próspera - Placas Cadastradas.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    backoffice_prospera_license_plate = st.text_input(label="Placa (opcional)").upper().strip()

                placeholder_prospera_serach_plates = st.empty()

                option_backoffice_prospera = st.session_state.get("report_backoffice_prospera")
                if option_backoffice_prospera == "prospera_plates_search":
                    placeholder_prospera_serach_plates.warning("Pesquisando...")

                    if backoffice_prospera_license_plate:
                        where_prospera_plates_search = f"""
                        WHERE
                            Placa = '{backoffice_prospera_license_plate}'
                        """
                    else:
                        where_prospera_plates_search = f""

                    # Escreve query
                    query = f"""
                        SELECT
                            FORMAT(DataConsulta, 'dd/MM/yyyy')  AS [Data da Consulta]
                            ,Item
                            ,Placa
                            ,Renavam
                            ,Municipio                          AS [Município]
                            ,UF                                 AS [UF]
                            ,UF_Descricao                       AS [UF Descrição]
                            ,Procedencia                        AS [Procedência]
                            ,Marca
                            ,Modelo
                            ,Cor
                            ,TipoDocumento                      AS [Tipo de Documento]
                            ,Documento
                            ,Nome_RazaoSocial                   AS [Nome/Razão Social]
                            ,Endereco                           AS [Endereço]
                            ,Email                              AS [E-mail]
                            ,Telefone
                            ,CASE
                                WHEN PossuiWhatsApp = 1
                                    THEN 'Sim'
                                ELSE
                                    'Não'
                            END                                 AS [Possui WhatsApp]
                            ,CASE
                                WHEN PEP = 1
                                    THEN 'Sim'
                                ELSE
                                    'Não'
                            END                                 AS [PEP]
                        FROM Prospera.consulta.vw_EnriquecimentoPlaca_Atual
                        {where_prospera_plates_search}
                        ORDER BY
                            DataConsulta
                            ,Item
                    """

                    placeholder_prospera_serach_plates.empty()
                    # Consulta ao banco
                    df_prospera_serach_plates = pd.read_sql(query, engine_pd)
                    st.session_state["prospera_serach_plates_df"] = df_prospera_serach_plates
                    st.session_state["prospera_serach_plates_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_prospera_serach_plates.empty:
                        csv_prospera_serach_plates = df_prospera_serach_plates.to_csv(index=False, sep=";")

                    del st.session_state["report_backoffice_prospera"]
                    st.rerun()

                if "prospera_serach_plates_df" in st.session_state:
                    if not st.session_state.get("prospera_serach_plates_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("prospera_serach_plates_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["prospera_serach_plates_datetime"]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("prospera_serach_plates_df"), height=600, hide_index=True)
                    else:
                        placeholder_prospera_serach_plates.error("Nenhum registro encontrado.")



            # ||=== NEVADA =================================================================================================================||
            elif option_backoffice == "nevada_capture":
                st.write("Nevada -- Validações")
                df_backoffice_nevada_capture = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 4, 6, 7])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="bt_backoffice_nevada_capture_search", use_container_width=True):
                        st.session_state["report_backoffice_nevada"] = "nevada_capture_search"

                    csv_backoffice_nevada_capture = df_backoffice_nevada_capture.to_csv(index=False, sep=";")
                    if "backoffice_nevada_capture_df" in st.session_state:
                        if not st.session_state.get("backoffice_nevada_capture_df").empty:
                            df_backoffice_nevada_capture = st.session_state.get("backoffice_nevada_capture_df")
                            csv_backoffice_nevada_capture = df_backoffice_nevada_capture.to_csv(index=False, sep=";")
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_backoffice_nevada_capture"
                        ,data=csv_backoffice_nevada_capture.encode("utf-8-sig")
                        ,file_name="Validações Nevada.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )

                with col2:
                    initial_date_backoffice_nevada_capture = st.date_input("Data Inicial da Passagem:", value=fn.beginning_of_month(dt.date.today(), -2), format="DD/MM/YYYY", key="initial_date_backoffice_nevada_capture")
                    end_date_backoffice_nevada_capture = st.date_input("Data Final da Passagem:", value=fn.end_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="end_date_backoffice_nevada_capture")
                    license_plate_backoffice_nevada_capture = st.text_input(label="Placa (opcional)", key="license_plate_backoffice_nevada_capture")
                with col3:
                    list_location_backoffice_nevada_capture = [
                        "Antônio Prado"
                        ,"Capela de Santana"
                        ,"Carlos Barbosa"
                        ,"Farroupilha"
                        ,"Ipê"
                        ,"São Sebastião do Caí"
                    ]
                    locations_backoffice_nevada_capture = st.multiselect("Localidade", options=list_location_backoffice_nevada_capture, default=list_location_backoffice_nevada_capture, key="locations_backoffice_nevada_capture")
                with col4:
                    # list_backoffice_nevada_capture_status =[
                    #     "Infração"
                    #     ,"Descartado"
                    #     ,"Processamento"
                    # ]
                    list_backoffice_nevada_capture_status =[
                        "Infração"
                        ,"Liberado"
                        ,"Fora do Prazo"
                    ]
                    backoffice_nevada_capture_status = st.multiselect("Status", options=list_backoffice_nevada_capture_status, default=list_backoffice_nevada_capture_status, key="backoffice_nevada_capture_status")
                    list_backoffice_nevada_capture_group_discard =[
                        "2 Horas"
                        ,"Chamado"
                        ,"Cliente Assíduo"
                        ,"CSG - Dezembro de 2023"
                        ,"Erro de Placa"
                        ,"Fora de Padrão"
                        ,"Não Usar"
                        ,"Perda Técnica"
                        ,"Placa Adulterada"
                        ,"Placa Estrangeira"
                        ,"Placa Ilegível"
                        ,"Placa Obstruída"
                        ,"Recuperação de Receita"
                        ,"Registros com Atraso - Kapsch"
                        ,"TAG Ativa"
                        ,"TAG Liberada - Data da Análise"
                        ,"TAG Liberada - Data da Passagem"
                        ,"Teste de Homologação"
                        ,"Transação Fracionada"
                        ,"Transação Paga (Desc. Automático)"
                        ,"Transação Paga (Desc. Manual)"
                        ,"Veículo CSG"
                        ,"Veículo Isento"
                        ,"Veículo Sem Placa"
                    ]
                    backoffice_nevada_capture_group_discard = st.multiselect("Grupo de Descarte", options=list_backoffice_nevada_capture_group_discard, default=list_backoffice_nevada_capture_group_discard, key="backoffice_nevada_capture_group_discard")

                placeholder_nevada_capture = st.empty()

                option_backoffice_nevada = st.session_state.get("report_backoffice_nevada")
                if option_backoffice_nevada == "nevada_capture_search":
                    placeholder_nevada_capture.warning("Pesquisando...")

                    # Define localidade
                    escaped_location_backoffice_nevada_capture = [loc.replace("'", "''") for loc in locations_backoffice_nevada_capture]
                    in_location_backoffice_nevada_capture = ", ".join(f"'{loc}'" for loc in escaped_location_backoffice_nevada_capture)
                    if not in_location_backoffice_nevada_capture:
                        placeholder_nevada_capture.error("Processo Cancelado. Nenhuma localidade informada.")
                        if "backoffice_nevada_capture_df" in st.session_state:
                            del st.session_state["backoffice_nevada_capture_df"]
                        st.stop()

                    # Define status
                    escaped_backoffice_nevada_capture_status = [status.replace("'", "''") for status in backoffice_nevada_capture_status]
                    in_backoffice_nevada_capture_status = ", ".join(f"'{status}'" for status in escaped_backoffice_nevada_capture_status)
                    if not in_backoffice_nevada_capture_status:
                        placeholder_nevada_capture.error("Processo Cancelado. Nenhum status informado.")
                        if "backoffice_nevada_capture_df" in st.session_state:
                            del st.session_state["backoffice_nevada_capture_df"]
                        st.stop()

                    # Define grupo de descarte
                    escaped_group_discard_nevada_capture = [group.replace("'", "''") for group in backoffice_nevada_capture_group_discard]
                    in_group_discard_backoffice_nevada_capture = ", ".join(f"'{group}'" for group in escaped_group_discard_nevada_capture)
                    if not in_group_discard_backoffice_nevada_capture:
                        placeholder_nevada_capture.error("Processo Cancelado. Nenhum grupo de descarte informado.")
                        if "backoffice_nevada_capture_df" in st.session_state:
                            del st.session_state["backoffice_nevada_capture_df"]
                        st.stop()

                    # Escreve query
                    # query_backoffice_nevada_capture_where = f""
                    # if "Descartado" in in_backoffice_nevada_capture_status:
                    #     query_backoffice_nevada_capture_where = f"""
                    #         AND (
                    #             DiscardReasonGroup IN ({in_group_discard_backoffice_nevada_capture})"""
                    # if "Infração" in in_backoffice_nevada_capture_status or "Processamento" in in_backoffice_nevada_capture_status:
                    #     if query_backoffice_nevada_capture_where == "":
                    #         query_backoffice_nevada_capture_where = f"""
                    #             AND ("""
                    #     else:
                    #         query_backoffice_nevada_capture_where = f"""
                    #             {query_backoffice_nevada_capture_where}
                    #                 OR """
                    #     query_backoffice_nevada_capture_where = f"""
                    #         {query_backoffice_nevada_capture_where}
                    #             DiscardReasonGroup IS NULL
                    #     """
                    # query_backoffice_nevada_capture_where = f"""
                    #     {query_backoffice_nevada_capture_where}
                    #         )
                    # """
                    # query_backoffice_nevada_capture = f"""
                    #     SELECT
                    #         Id                                                      AS [Nº]
                    #         ,[Status]
                    #         ,Stage                                                  AS [Etapa]
                    #         ,CAST(PassageEventId AS VARCHAR)                        AS [Evento de Passagem]
                    #         ,CAST(FinancialTransactionId AS VARCHAR)                AS [Transação Financeira]
                    #         ,FORMAT(OccurrenceDatetime, 'dd/MM/yyyy HH:mm:ss')      AS [Data da Passagem]
                    #         ,[Location] + CASE
                    #             WHEN Equipment LIKE '%_NORTE'
                    #                 THEN ' Norte'
                    #             WHEN Equipment LIKE '%_SUL'
                    #                 THEN ' Sul'
                    #             WHEN Equipment LIKE '%_LESTE'
                    #                 THEN ' Leste'
                    #             WHEN Equipment LIKE '%_OESTE'
                    #                 THEN ' Oeste'
                    #         END                                                     AS [Localidade]
                    #         ,LicensePlate                                           AS [Placa]
                    #         ,DiscardReason                                          AS [Motivo do Descarte]
                    #         ,DiscardReasonGroup                                     AS [Grupo do Descarte]
                    #         ,ViolationAuto                                          AS [Auto de Infração]
                    #         ,FORMAT(ViolationAutoDatetime, 'dd/MM/yyyy HH:mm:ss')   AS [Data do Auto de Infração]
                    #     FROM PD.nevada.tb_Capture WITH (NOLOCK)
                    #     WHERE
                    #         CAST(OccurrenceDatetime AS DATE) BETWEEN '{initial_date_backoffice_nevada_capture.strftime('%Y-%m-%d')}' AND '{end_date_backoffice_nevada_capture.strftime('%Y-%m-%d')}'
                    #         AND [Location] IN ({in_location_backoffice_nevada_capture})
                    #         AND [Status] IN ({in_backoffice_nevada_capture_status})
                    #         {query_backoffice_nevada_capture_where}
                    #     ORDER BY
                    #         OccurrenceDatetime
                    # """
                    if license_plate_backoffice_nevada_capture:
                        license_plate_backoffice_nevada_capture = f"""
                            AND Plate = '{license_plate_backoffice_nevada_capture.upper().strip()}'
                        """
                    else:
                        license_plate_backoffice_nevada_capture = ""

                    query_backoffice_nevada_capture = f"""
                        WITH cte_CaptureReport AS (
                            SELECT
                                Id
                                ,[Status]
                                ,Transaction_Id
                                ,Trx_Datetime
                                ,[Location] + CASE
                                    WHEN Equipment LIKE '%_NORTE'
                                        THEN ' Norte'
                                    WHEN Equipment LIKE '%_SUL'
                                        THEN ' Sul'
                                    WHEN Equipment LIKE '%_LESTE'
                                        THEN ' Leste'
                                    WHEN Equipment LIKE '%_OESTE'
                                        THEN ' Oeste'
                                END AS [Location]
                                ,Plate
                                ,Stage
                                ,REPLACE(REPLACE(
                                    [Discard]
                                    ,',Transação Fracionada', '')
                                    ,'Transação Fracionada,', '') AS [Discard]
                                ,PD.nevada.GROUP_DISCARD([Discard]) AS Group_Discard
                                ,[Auto]
                                ,CASE
                                    WHEN [Auto] IS NOT NULL
                                        THEN FORMAT(
                                            CONVERT(DATETIME
                                                ,REPLACE(SUBSTRING([Auto], 13, 10), '.', '/')
                                                + ' ' + REPLACE(SUBSTRING([Auto], 24, 8), '.', ':')
                                                ,103)
                                            ,'dd/MM/yyyy HH:mm:ss')
                                    ELSE
                                        NULL
                                END AS Auto_Datetime
                                ,[User]
                            FROM PD.nevada.tb_CaptureReport WITH (NOLOCK)
                            WHERE
                                CAST(Trx_Datetime AS DATE) BETWEEN '{initial_date_backoffice_nevada_capture.strftime('%Y-%m-%d')}' AND '{end_date_backoffice_nevada_capture.strftime('%Y-%m-%d')}'
                                AND [Location] IN ({in_location_backoffice_nevada_capture})
                                AND [Status] IN ({in_backoffice_nevada_capture_status})
                                {license_plate_backoffice_nevada_capture}
                        )
                        SELECT
                            Id                                              AS [Nº]
                            ,[Status]
                            ,Transaction_Id                                 AS [Transação Financeira]
                            ,FORMAT(Trx_Datetime, 'dd/MM/yyyy HH:mm:ss')    AS [Data da Passagem]
                            ,[Location]                                     AS Localidade
                            ,Plate                                          AS Placa
                            ,Stage                                          AS Etapa
                            ,[Discard]                                      AS [Motivo do Descarte]
                            ,Group_Discard                                  AS [Grupo de Descarte]
                            ,[Auto]                                         AS [Auto de Infração]
                            ,Auto_Datetime                                  AS [Data do Auto de Infração]
                            ,[User]                                         AS [Usuário]
                        FROM cte_CaptureReport
                        WHERE
                            Group_Discard IN ({in_group_discard_backoffice_nevada_capture})
                            OR Group_Discard IS NULL
                        ORDER BY
                            Trx_Datetime
                    """

                    # Consulta ao banco
                    df_backoffice_nevada_capture = pd.read_sql(query_backoffice_nevada_capture, engine_pd)
                    st.session_state["backoffice_nevada_capture_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                    st.session_state["backoffice_nevada_capture_df"] = df_backoffice_nevada_capture
                    placeholder_nevada_capture.empty()

                    del st.session_state["report_backoffice_nevada"]
                    st.rerun()

                if "backoffice_nevada_capture_df" in st.session_state:
                    if not st.session_state.get("backoffice_nevada_capture_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("backoffice_nevada_capture_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["backoffice_nevada_capture_datetime"]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("backoffice_nevada_capture_df"), height=600, hide_index=True)
                    else:
                        placeholder_nevada_capture.error("Nenhum registro encontrado.")
                        if "backoffice_nevada_capture_df" in st.session_state:
                            del st.session_state["backoffice_nevada_capture_df"]


            # ||=== KAPSCH =================================================================================================================||
            elif option_backoffice == "kapsch_tfs":
                st.write("Kapsch -- Status Final da Transação")
                df_kapsch_tfs = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 5, 3, 9])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="kapsch_tfs_search", use_container_width=True):
                        st.session_state["report_backoffice_kapsch"] = "kapsch_tfs_search"
                    csv_kapsch_tfs = df_kapsch_tfs.to_csv(sep=";", index=False)
                    if "kapsch_tfs_search_df" in st.session_state:
                        if not st.session_state.get("kapsch_tfs_search_df").empty:
                            df_kapsch_tfs = st.session_state.get("kapsch_tfs_search_df")
                            csv_kapsch_tfs = df_kapsch_tfs.to_csv(sep=";", index=False)
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_kapsch_tfs"
                        ,data=csv_kapsch_tfs.encode("utf-8-sig")
                        ,file_name="Status Final da Transação.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    kapsch_tfs_transaction_status_list =[
                        "Todos"
                        ,"Disputada"
                        ,"Erro Técnico OBO"
                        ,"Exportado para VP - sem resposta"
                        ,"Indefinido"
                        ,"Isento CSG"
                        ,"Não Pago"
                        ,"OBO Cancelado"
                        ,"OBO Ignorado pelas Operações"
                        ,"Pago Pela Cupom VP"
                        ,"Pago Pela OSA"
                        ,"Pago Pela VP Tag"
                        ,"Pago Pela Web"
                        ,"Perda Técnica"
                        ,"Processamento OBO"
                        ,"Rejeição de OSA"
                        ,"Rejeitado no CBO"
                        ,"Validação Manual"
                    ]
                    kapsch_tfs_transaction_status = st.selectbox("Status da Transação", options=kapsch_tfs_transaction_status_list)
                    kapsch_tfs_initial_date = st.date_input("Data Inicial:", value=dt.date.today() - dt.timedelta(days=14), format="DD/MM/YYYY", key="kapsch_tfs_initial_date")
                    kapsch_tfs_ending_date = st.date_input("Data Inicial:", value=dt.date.today(), format="DD/MM/YYYY", key="kapsch_tfs_ending_date")

                placeholder_kapsch_tfs = st.empty()

                option_backoffice_kapsch = st.session_state.get("report_backoffice_kapsch", "")
                if option_backoffice_kapsch == "kapsch_tfs_search":
                    start_time = time.time()
                    # Verifica validade das datas
                    kapsch_tfs_date_diff = kapsch_tfs_ending_date - kapsch_tfs_initial_date
                    if kapsch_tfs_transaction_status == "Todos":
                        if kapsch_tfs_date_diff.days < 0 or kapsch_tfs_date_diff.days > 15:
                            placeholder_kapsch_tfs.error("Processo Cancelado. Período de datas deve ser de até 15 dias.")
                            if "report_backoffice_kapsch" in st.session_state:
                                del st.session_state["report_backoffice_kapsch"]
                            st.stop()
                    else:
                        if kapsch_tfs_date_diff.days < 0 or kapsch_tfs_date_diff.days > 31:
                            placeholder_kapsch_tfs.error("Processo Cancelado. Período de datas deve ser de até 31 dias.")
                            if "report_backoffice_kapsch" in st.session_state:
                                del st.session_state["report_backoffice_kapsch"]
                            st.stop()

                    if kapsch_tfs_transaction_status == "Todos":
                        where_transaction_status = f""
                    elif kapsch_tfs_transaction_status == f"Indefinido":
                        where_transaction_status = f"AND TFS.TransactionStatus IS NULL"
                    else:
                        where_transaction_status = f"AND TFS.TransactionStatus = '{kapsch_tfs_transaction_status}'"

                    placeholder_kapsch_tfs.warning("Pesquisando...")

                    # Escreve query
                    query_kapsch_tfs = f"""
                        WITH cte_Transaction AS (
                            SELECT DISTINCT
                                Passage_Event_Id
                                ,External_Correlation_Id AS TransactionId
                                ,Country_Code
                            FROM PD.kapsch.vw_Transaction WITH (NOLOCK)
                            WHERE
                                CAST(Datetime_Local_Occurrence AS DATE) BETWEEN '{kapsch_tfs_initial_date.strftime('%Y-%m-%d')}' AND '{kapsch_tfs_ending_date.strftime('%Y-%m-%d')}'
                        )
                        SELECT
                            CAST(TFS.PassageID AS VARCHAR)                          AS [Evento de Passagem]
                            ,LOWER(T.TransactionId)                                 AS [Transação]
                            ,CAST(TFS.FinancialTransactionID AS VARCHAR)            AS [Transação Financeira]
                            ,FORMAT(TFS.OccurrenceDate, 'dd/MM/yyyy HH:mm:ss')      AS [Data da Passagem]
                            ,TFS.LocationDescription                                AS [Localidade]
                            ,TFS.LicensePlate                                       AS [Placa]
                            ,CASE
                                WHEN TFS.LicensePlate LIKE 'XXX0%'
                                OR TFS.LicensePlate IN ('CSG00001', 'YYY99999')
                                    THEN 'Placa Genérica'
                                ELSE
                                    T.Country_Code
                            END                                                     AS [Código do País]
                            ,TFS.VehicleClass                                       AS [Categoria do Veículo]
                            ,'R$    ' + FORMAT(TFS.BaseAmount, '0.00')              AS [Valor da Tarifa]
                            ,'R$    ' + FORMAT(TFS.PaidAmount, '0.00')              AS [Valor Pago]
                            ,TFS.TransactionStatus                                  AS [Status da Transação]
                            ,TFS.PaymentMethod                                      AS [Meio de Pagamento]
                            ,FORMAT(TFS.PaymentDatetime, 'dd/MM/yyyy HH:mm:ss')     AS [Data do Pagamento]
                            ,'R$    ' + FORMAT(TFS.AVI_DBT, '0.00')                 AS [DBT OSA]
                            ,'R$    ' + FORMAT(TFS.AVI_DUF, '0.00')                 AS [DUF OSA]
                            ,'R$    ' + FORMAT(TFS.DiscountWebDBT, '0.00')          AS [DBT Plataforma]
                            ,'R$    ' + FORMAT(TFS.DiscountWebDUF, '0.00')          AS [DUF Plataforma]
                            ,'R$    ' + FORMAT(TFS.FeeWeb, '0.00')                  AS [Acréscimo]
                        FROM PD.kapsch.vw_TransactionFinalStatus    AS TFS WITH (NOLOCK)
                        LEFT JOIN cte_Transaction                   AS T WITH (NOLOCK)
                            ON T.Passage_Event_Id = TFS.PassageID
                        WHERE
                            CAST(TFS.OccurrenceDate AS DATE) BETWEEN '{kapsch_tfs_initial_date.strftime('%Y-%m-%d')}' AND '{kapsch_tfs_ending_date.strftime('%Y-%m-%d')}'
                            {where_transaction_status}
                        ORDER BY
                            TFS.OccurrenceDate
                    """

                    # Consulta ao banco
                    df_kapsch_tfs = pd.read_sql(query_kapsch_tfs, engine_pd)

                    duration_time_float = time.time() - start_time
                    duration_time = dt.timedelta(seconds=duration_time_float)
                    st.session_state["kapsch_tfs_search_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}|Tempo de Execução: {str(duration_time)[:-3]}"
                    st.session_state["kapsch_tfs_search_df"] = df_kapsch_tfs
                    placeholder_kapsch_tfs.empty()

                    if "report_backoffice_kapsch" in st.session_state:
                        del st.session_state["report_backoffice_kapsch"]

                    st.rerun()

                if "report_backoffice_kapsch" in st.session_state:
                    del st.session_state["report_backoffice_kapsch"]

                if "kapsch_tfs_search_df" in st.session_state:
                    if not st.session_state.get("kapsch_tfs_search_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("kapsch_tfs_search_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["kapsch_tfs_search_datetime"].split("|")[0]}\t\t{st.session_state["kapsch_tfs_search_datetime"].split("|")[1]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("kapsch_tfs_search_df"), height=600, hide_index=True, width=1400)
                    else:
                        placeholder_kapsch_tfs.error("Nenhum registro encontrado.")
                        if "kapsch_tfs_search_df" in st.session_state:
                            del st.session_state["kapsch_tfs_search_df"]

            # ||=== KAPSCH =================================================================================================================||
            elif option_backoffice == "kapsch_exempt_list":
                st.write("Kapsch -- Lista de Isentos")
                df_kapsch_exempt_list = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 5, 3, 9])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="kapsch_exempt_list_search", use_container_width=True):
                        st.session_state["report_backoffice_kapsch"] = "kapsch_exempt_list_search"
                    csv_kapsch_exempt_list = df_kapsch_exempt_list.to_csv(sep=";", index=False)
                    if "kapsch_exempt_list_search_df" in st.session_state:
                        if not st.session_state.get("kapsch_exempt_list_search_df").empty:
                            df_kapsch_exempt_list = st.session_state.get("kapsch_exempt_list_search_df")
                            csv_kapsch_exempt_list = df_kapsch_exempt_list.to_csv(sep=";", index=False)
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_kapsch_exempt_list"
                        ,data=csv_kapsch_exempt_list.encode("utf-8-sig")
                        ,file_name="Lista de Isentos.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )

                placeholder_kapsch_exempt_list = st.empty()

                option_backoffice_kapsch = st.session_state.get("report_backoffice_kapsch", "")
                if option_backoffice_kapsch == "kapsch_exempt_list_search":
                    start_time = time.time()

                    placeholder_kapsch_exempt_list.warning("Pesquisando...")

                    # Escreve query
                    query_kapsch_exempt_list = f"""
                        SELECT
                            LicensePlate                                AS Placa
                            ,ExemptGroup                                AS [Grupo de Isenção]
                            ,[Location]                                 AS [Localidade de Isenção]
                            ,WeekDays                                   AS [Dias de Isenção]
                            ,FORMAT(ActiveFrom, 'dd/MM/yyyy HH:mm:ss')  AS [Início da Vigência]
                            ,FORMAT(ActiveTo, 'dd/MM/yyyy HH:mm:ss')    AS [Final da Vigência]
                            ,CASE
                                WHEN [Active] = 1
                                    THEN 'Sim'
                                ELSE
                                    'Não'
                            END                                         AS Ativo
                            ,LastUpdatedBy                              AS [Atualizado por]
                        FROM PD.kapsch.tb_ExemptList
                    """

                    # Consulta ao banco
                    df_kapsch_exempt_list = pd.read_sql(query_kapsch_exempt_list, engine_pd)

                    kapsch_exempt_list_duration_time_float = time.time() - start_time
                    kapsch_exempt_list_duration_time = dt.timedelta(seconds=kapsch_exempt_list_duration_time_float)
                    st.session_state["kapsch_exempt_list_search_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}|Tempo de Execução: {str(kapsch_exempt_list_duration_time)[:-3]}"
                    st.session_state["kapsch_exempt_list_search_df"] = df_kapsch_exempt_list
                    placeholder_kapsch_exempt_list.empty()

                    if "report_backoffice_kapsch" in st.session_state:
                        del st.session_state["report_backoffice_kapsch"]

                    st.rerun()

                if "report_backoffice_kapsch" in st.session_state:
                    del st.session_state["report_backoffice_kapsch"]

                if "kapsch_exempt_list_search_df" in st.session_state:
                    if not st.session_state.get("kapsch_exempt_list_search_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("kapsch_exempt_list_search_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["kapsch_exempt_list_search_datetime"].split("|")[0]}\t\t{st.session_state["kapsch_exempt_list_search_datetime"].split("|")[1]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("kapsch_exempt_list_search_df"), height=600, hide_index=True, width=1400)
                    else:
                        placeholder_kapsch_exempt_list.error("Nenhum registro encontrado.")
                        if "kapsch_exempt_list_search_df" in st.session_state:
                            del st.session_state["kapsch_exempt_list_search_df"]



# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    FINANCEIRO                                                                                                                          ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_financial_tab:
    with tab_financial:
        df_financial = pd.DataFrame()

        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            st.markdown("##### Kapsch")
            if st.button("Base do Faturamento", use_container_width=True, key="bt_financial_kapsch_revenue_base"):
                st.session_state["report_financial"] = "kapsch_revenue_base"
                if "report_financial_kapsch" in st.session_state:
                    del st.session_state["report_financial_kapsch"]

            st.markdown("##### Movvia")
            if st.button("Pesquisa de NSU/TXID", use_container_width=True, key="bt_movvia_nsu_txid"):
                st.session_state["report_financial"] = "movvia_nsu_txid"
                if "report_financial_movvia" in st.session_state:
                    del st.session_state["report_financial_movvia"]
            if st.button("Saldo de Custódia", use_container_width=True, key="bt_movvia_custody_balance"):
                st.session_state["report_financial"] = "movvia_custody_balance"
                if "report_financial_movvia" in st.session_state:
                    del st.session_state["report_financial_movvia"]

        with col_content:
            option_financial = st.session_state.get("report_financial")

            # ||=== MOVVIA =================================================================================================================||
            if option_financial == "movvia_nsu_txid":
                st.write("Movvia -- Pesquisa de NSU/TXID")
                df_movvia_nsu_txid_data = pd.DataFrame()
                df_movvia_nsu_txid_customer = pd.DataFrame()

                col1, col2, col3 = st.columns([3, 6, 11])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="movvia_nsu_txid", use_container_width=True):
                        st.session_state["report_financial_movvia"] = "movvia_nsu_txid"
                    csv_movvia_nsu_txid_data = df_movvia_nsu_txid_data.to_csv(sep=";", index=False)
                    if "financial_movvia_nsu_txid_data_df" in st.session_state:
                        if not st.session_state.get("financial_movvia_nsu_txid_data_df").empty:
                            df_movvia_nsu_txid_data = st.session_state.get("financial_movvia_nsu_txid_data_df")
                            csv_movvia_nsu_txid_data = df_movvia_nsu_txid_data.to_csv(sep=";", index=False)
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_movvia_nsu_txid_data"
                        ,data=csv_movvia_nsu_txid_data.encode("utf-8-sig")
                        ,file_name="Pesquisa de NSU_TXID.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    movvia_nsu_txid_nsu = st.text_input("NSU", key="initial_date_movvia_nsu")
                    movvia_nsu_txid_txid = st.text_input("TXID", key="ending_date_movvia_txid")
                with col3:
                    placeholder_movvia_nsu_txid_custome = st.empty()

                placeholder_movvia_nsu_txid = st.empty()

                option_financial_movvia = st.session_state.get("report_financial_movvia", "")
                if option_financial_movvia == "movvia_nsu_txid":
                    if movvia_nsu_txid_nsu:
                        query_movvia_nsu_txid_where = f"O.nsu = '{movvia_nsu_txid_nsu}'"
                    elif movvia_nsu_txid_txid:
                        query_movvia_nsu_txid_where = f"""OP."txId" = '{movvia_nsu_txid_txid}'"""
                    else:
                        placeholder_movvia_nsu_txid.error("Processo Cancelado. Informe um NSU ou um TXID.")
                        if "report_financial_movvia" in st.session_state:
                            del st.session_state["report_financial_movvia"]
                        if "financial_movvia_nsu_txid_data_df" in st.session_state:
                            del st.session_state["financial_movvia_nsu_txid_data_df"]
                        st.stop()

                    placeholder_movvia_nsu_txid.warning("Pesquisando...")

                    # Escreve query
                    query_movvia_nsu_txid = f"""
                        WITH cte_plaza AS (
                            SELECT
                                "plazaCode"
                                ,"locationDescription"
                            FROM (VALUES
                                ('10', 'São Sebastião do Caí Norte')
                                ,('20', 'Antônio Prado Norte')
                                ,('21', 'Antônio Prado Sul')
                                ,('30', 'Ipê Norte')
                                ,('31', 'Ipê Sul')
                                ,('40', 'Capela de Santana Oeste')
                                ,('41', 'Capela de Santana Leste')
                                ,('50', 'Farroupilha Norte')
                                ,('51', 'Farroupilha Sul')
                                ,('60', 'Carlos Barbosa Norte')
                                ,('61', 'Carlos Barbosa Sul')
                                ,('70', 'São Sebastião do Caí Sul')
                                ,('71', 'São Sebastião do Caí Sul')
                            ) AS TB ("plazaCode", "locationDescription")
                        )
                        ,cet_order_charges_arr_charge AS (
                            SELECT
                                "chargeId"
                                ,MAX("orderId") AS "orderId"
                            FROM public.order_charges_arr_charge
                            GROUP BY
                                "chargeId"
                        )
                        SELECT
                            TO_CHAR(C."datetimeOccurrence", 'DD/MM/YYYY HH24:MI:SS')            AS "Data da Passagem"
                            ,C."licensePlate"                                                   AS "Placa"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C."rateAmount" * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Tarifa"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C.discount * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Desconto"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C."discountDuf" * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "DUF"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C."discountDbt" * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "DBT"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(C.fee* 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Acréscimo"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR((C."rateAmount" + C.fee - C.discount) * 0.01
                                    ,'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')                               AS "Valor da Passagem"
                            ,P."locationDescription"                                            AS "Localidade"
                            ,CASE
                                WHEN C.status = 'paid'
                                    THEN 'Pago'
                                WHEN C.status = 'open'
                                    THEN 'Aberto'
                                WHEN C.status = 'canceled'
                                    THEN 'Cancelado'
                                WHEN C.status = 'free'
                                    THEN 'Isento'
                                WHEN C.status = 'declined'
                                    THEN 'Recusado'
                                ELSE
                                    C.status
                            END                                                                 AS "Status do Pagamento"
                            ,TO_CHAR(C."dueDate", 'DD/MM/YYYY')                                 AS "Data de Vencimento"
                            ,CASE
                                WHEN O."paymentMethod" IN ('credit-card', 'credit-card-pinpad')
                                    THEN 'Cartão de Crédito'
                                WHEN O."paymentMethod" = 'debit-card-pinpad'
                                    THEN 'Cartão de Débito'
                                WHEN O."paymentMethod" = 'pix'
                                    THEN 'PIX'
                                WHEN O."paymentMethod" = 'balance'
                                    THEN 'Saldo'
                                WHEN O."paymentMethod" = 'baixa'
                                    THEN 'Baixa'
                                WHEN O."paymentMethod" = 'cash'
                                    THEN 'Dinheiro'
                                WHEN O."paymentMethod" = 'rekpay'
                                    THEN 'Rek Pay'
                                WHEN O."paymentMethod" IN ('sim-cash', 'sim-pix')
                                    THEN 'SIM'
                                WHEN O."paymentMethod" = 'vvp'
                                    THEN 'VVP'
                                ELSE
                                    O."paymentMethod"
                            END                                                                 AS "Meio de Pagamento"
                            ,TO_CHAR(O."paidAt", 'DD/MM/YYYY HH24:MI:SS')                       AS "Data de Pagamento"
                            ,O.nsu                                                              AS "NSU"
                            ,OP."txId"                                                          AS "TXID"
                            ,TO_CHAR(OP."createdAt", 'DD/MM/YYYY HH24:MI:SS')                   AS "Data de Criação do TXID"
                            ,TRIM(TRIM(U.firstname) || ' ' || TRIM(U.lastname) || ' '
                                || TRIM(U."companyName") || ' ' || TRIM(U."businessName"))      AS "Nome"
                            ,U.document                                                         AS "CPF/CNPJ"
                            ,U.email                                                            AS "E-mail"
                            ,U.phone                                                            AS "Telefone"
                        FROM public.charge                          AS C
                        LEFT JOIN cte_plaza                         AS P
                            ON P."plazaCode" = C."plazaCode"
                        LEFT JOIN cet_order_charges_arr_charge      AS OCAC
                            ON OCAC."chargeId" = C.id
                        LEFT JOIN public.order                      AS O
                            ON O.id = OCAC."orderId"
                        LEFT JOIN public."user"                     AS U
                            ON U.id = O."userId"
                        LEFT JOIN public.order_pix                  AS OP
                            ON OP.id = O."pixId"
                        WHERE
                            {query_movvia_nsu_txid_where}
                        ORDER BY
                            C."datetimeOccurrence" DESC
                    """

                    # Consulta ao banco
                    df_movvia_nsu_txid_customer = pd.read_sql(query_movvia_nsu_txid, engine_attri)

                    st.session_state["financial_movvia_nsu_txid_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_movvia_nsu_txid_customer.empty:
                        df_movvia_nsu_txid_data = df_movvia_nsu_txid_customer[[
                            "Data da Passagem"
                            ,"Placa"
                            ,"Tarifa"
                            ,"Desconto"
                            ,"DUF"
                            ,"DBT"
                            ,"Acréscimo"
                            ,"Valor da Passagem"
                            ,"Localidade"
                            ,"Status do Pagamento"
                            ,"Data de Vencimento"
                            ,"Meio de Pagamento"
                            ,"Data de Pagamento"
                            ,"NSU"
                            ,"TXID"
                            ,"Data de Criação do TXID"
                        ]].copy()
                        # Salva o resultado
                        st.session_state["financial_movvia_nsu_txid_data_df"] = df_movvia_nsu_txid_data
                        st.session_state["financial_movvia_nsu_txid_customer_df"] = df_movvia_nsu_txid_customer
                        st.session_state["financial_movvia_nsu_txid_exists_df"] = True
                        # Exibe em tela
                        placeholder_movvia_nsu_txid.empty()
                    else:
                        st.session_state["financial_movvia_nsu_txid_exists_df"] = False

                    if "report_financial_movvia" in st.session_state:
                        del st.session_state["report_financial_movvia"]
                        st.rerun()

                if "financial_movvia_nsu_txid_exists_df" in st.session_state:
                    if not st.session_state.get("financial_movvia_nsu_txid_exists_df", True):
                        placeholder_movvia_nsu_txid.error("Nenhum registro encontrado.")

                if "financial_movvia_nsu_txid_data_df" in st.session_state:
                    if not st.session_state.get("financial_movvia_nsu_txid_data_df").empty and st.session_state.get("financial_movvia_nsu_txid_exists_df", False):
                        # Exibe em tela
                        st.write(st.session_state["financial_movvia_nsu_txid_datetime"])
                        st.dataframe(st.session_state.get("financial_movvia_nsu_txid_data_df"), height=600, hide_index=True)
                        # Exibe dados no cliente
                        df_movvia_nsu_txid_customer = st.session_state.get("financial_movvia_nsu_txid_customer_df")
                        movvia_nsu_txid_customer_name = st.session_state.get("financial_movvia_nsu_txid_customer_df").loc[0, "Nome"]
                        movvia_nsu_txid_customer_document = st.session_state.get("financial_movvia_nsu_txid_customer_df").loc[0, "CPF/CNPJ"]
                        movvia_nsu_txid_customer_email = st.session_state.get("financial_movvia_nsu_txid_customer_df").loc[0, "E-mail"]
                        movvia_nsu_txid_customer_phone = st.session_state.get("financial_movvia_nsu_txid_customer_df").loc[0, "Telefone"]
                        
                        if not movvia_nsu_txid_customer_name:
                            movvia_nsu_txid_customer_name = ""
                        if not movvia_nsu_txid_customer_document:
                            movvia_nsu_txid_customer_document = ""
                        if not movvia_nsu_txid_customer_email:
                            movvia_nsu_txid_customer_email = ""
                        if not movvia_nsu_txid_customer_phone:
                            movvia_nsu_txid_customer_phone = ""
                        
                        placeholder_movvia_nsu_txid_custome.write(f"""
                            Dados do Cliente                                    {chr(13)}
                            Nome:       {movvia_nsu_txid_customer_name}         {chr(13)}
                            CPF/CNPJ:   {movvia_nsu_txid_customer_document}     {chr(13)}
                            E-mail:     {movvia_nsu_txid_customer_email}        {chr(13)}
                            Telefone:   {movvia_nsu_txid_customer_phone}        {chr(13)}
                        """)

            # movvia_custody_balance
            elif option_financial == "movvia_custody_balance":
                st.write("Movvia -- Saldo de Custódia")
                df_movvia_custody_balance = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="movvia_custody_balance", use_container_width=True):
                        st.session_state["report_financial_movvia"] = "movvia_custody_balance"
                    csv_movvia_custody_balance = df_movvia_custody_balance.to_csv(sep=";", index=False)
                    if "financial_movvia_custody_balance_df" in st.session_state:
                        if not st.session_state.get("financial_movvia_custody_balance_df").empty:
                            df_movvia_custody_balance = st.session_state.get("financial_movvia_custody_balance_df")
                            csv_movvia_custody_balance = df_movvia_custody_balance.to_csv(sep=";", index=False)
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_movvia_custody_balance"
                        ,data=csv_movvia_custody_balance.encode("utf-8-sig")
                        ,file_name="Saldo de Custódia.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    initial_date_movvia_custody_balance = st.date_input("Data Inicial:", value=fn.end_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="initial_date_movvia_custody_balance")
                    ending_date_movvia_custody_balance = st.date_input("Data Final:", value=fn.end_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="ending_date_movvia_custody_balance")

                placeholder_movvia_custody_balance = st.empty()

                option_movvia = st.session_state.get("report_financial_movvia")
                if option_movvia == "movvia_custody_balance":
                    financial_search_movvia_custody_balance_date_diff = ending_date_movvia_custody_balance - initial_date_movvia_custody_balance
                    if financial_search_movvia_custody_balance_date_diff.days < 0:
                        placeholder_movvia_custody_balance.error("Processo Cancelado. Período de datas não confere.")
                        if "report_financial_movvia" in st.session_state:
                            del st.session_state["report_financial_movvia"]
                        st.stop()
                    
                    placeholder_movvia_custody_balance.warning("Pesquisando...")

                    # Escreve query
                    query_movvia_custody_balance = f"""
                        SELECT
                            RBD."userId"                                        AS "Id do Usuário"
                            ,TO_CHAR(RBD.date, 'DD/MM/YYYY')                    AS "Data do Saldo"
                            ,'R$    ' || REPLACE(REPLACE(REPLACE(
                                TO_CHAR(RBD.balance * 0.01, 'FM999G999G990D00')
                                ,'.', '|' ), ',', '.'), '|', ',')               AS "Saldo"
                        FROM public.report_balance_daily AS RBD
                        LEFT JOIN (
                            SELECT
                                RBD."userId"
                                ,RBD.date
                                ,MAX(RBD.id) AS id
                            FROM public.report_balance_daily AS RBD
                            WHERE
                                RBD.date = (date_trunc('month', RBD.date) + INTERVAL '1 month - 1 day')
                                AND RBD.balance > 0
                            GROUP BY
                                RBD."userId"
                                ,RBD.date
                        ) AS TB
                            ON TB.id = RBD.id
                            AND TB."userId" = RBD."userId"
                            AND TB.date = RBD.date
                        WHERE
                            TB.id IS NOT NULL
                            AND TB.date::DATE BETWEEN '{initial_date_movvia_custody_balance.strftime('%Y-%m-%d')}' AND '{ending_date_movvia_custody_balance.strftime('%Y-%m-%d')}'
                        ORDER BY
                            RBD."userId"
                            ,RBD.date
                    """

                    # Consulta ao banco
                    df_movvia_custody_balance = pd.read_sql(query_movvia_custody_balance, engine_attri)
                    st.session_state["financial_movvia_custody_balance_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_movvia_custody_balance.empty:
                        # Salva o resultado
                        st.session_state["financial_movvia_custody_balance_df"] = df_movvia_custody_balance
                        st.session_state["financial_movvia_custody_balance_exists_df"] = True
                        # Exibe em tela
                        placeholder_movvia_custody_balance.empty()
                    else:
                        st.session_state["financial_movvia_custody_balance_exists_df"] = False

                    if "report_financial_movvia" in st.session_state:
                        del st.session_state["report_financial_movvia"]
                        st.rerun()

                if "financial_movvia_custody_balance_exists_df" in st.session_state:
                    if not st.session_state.get("financial_movvia_custody_balance_exists_df", True):
                        placeholder_movvia_custody_balance.error("Nenhum registro encontrado.")

                if "financial_movvia_custody_balance_df" in st.session_state:
                    if not st.session_state.get("financial_movvia_custody_balance_df").empty and st.session_state.get("financial_movvia_custody_balance_exists_df"):
                        # Exibe em tela
                        st.write(st.session_state["financial_movvia_custody_balance_datetime"])
                        st.dataframe(st.session_state.get("financial_movvia_custody_balance_df"), height=600, hide_index=True, width=460)

            # kapsch_revenue_base
            elif option_financial == "kapsch_revenue_base":
                placeholder_kapsch_revenue_base = st.empty()
                st.write("kapsch -- Base do Faturamento")
                df_kapsch_revenue_base = pd.DataFrame()

                col1, col2, col3 = st.columns([3, 3, 14])
                with col1:
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="kapsch_revenue_base", use_container_width=True):
                        st.session_state["report_financial_kapsch_revenue_base"] = "kapsch_revenue_base"
                    csv_kapsch_revenue_base = df_kapsch_revenue_base.to_csv(sep=";", index=False)
                    if "financial_kapsch_revenue_base_df" in st.session_state:
                        if not st.session_state.get("financial_kapsch_revenue_base_df").empty:
                            df_kapsch_revenue_base = st.session_state.get("financial_kapsch_revenue_base_df")
                            csv_kapsch_revenue_base = df_kapsch_revenue_base.to_csv(sep=";", index=False)
                    st.download_button(
                        label="Baixar Tabela de Dados"
                        ,key="csv_kapsch_revenue_base"
                        ,data=csv_kapsch_revenue_base.encode("utf-8-sig")
                        ,file_name="Base do Faturamento.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    initial_date_kapsch_revenue_base = st.date_input("Data Inicial:", value=fn.beginning_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="initial_date_kapsch_revenue_base")
                    ending_date_kapsch_revenue_base = st.date_input("Data Final:", value=fn.end_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="ending_date_kapsch_revenue_base")

                option_movvia = st.session_state.get("report_financial_kapsch_revenue_base")
                if option_movvia == "kapsch_revenue_base":
                    financial_search_kapsch_revenue_base_date_diff = ending_date_kapsch_revenue_base - initial_date_kapsch_revenue_base
                    if financial_search_kapsch_revenue_base_date_diff.days < 0:
                        placeholder_kapsch_revenue_base.error("Processo Cancelado. Período de datas não confere.")
                        if "report_financial_kapsch_revenue_base" in st.session_state:
                            del st.session_state["report_financial_kapsch_revenue_base"]
                        st.stop()
                    
                    placeholder_kapsch_revenue_base.warning("Pesquisando...")

                    # Escreve query
                    query_kapsch_revenue_base = f"""
                        SELECT
                            FORMAT(DataPassagem, 'dd/MM/yyyy')                      AS [Data da Passagem]
                            ,Portico                                                AS [Pórtico]
                            ,CAST(ClassificacaoVeiculo AS VARCHAR)                  AS [Classificação do Veículo]
                            ,'R$ ' + FORMAT(ConectCar, '#,##0.00')                  AS [ConectCar]
                            ,'R$ ' + FORMAT(GreenPass, '#,##0.00')                  AS [GreenPass]
                            ,'R$ ' + FORMAT(MoveMais, '#,##0.00')                   AS [Move Mais]
                            ,'R$ ' + FORMAT(Veloe, '#,##0.00')                      AS [Veloe]
                            ,'R$ ' + FORMAT(SemParar, '#,##0.00')                   AS [Sem Parar]
                            ,'R$ ' + FORMAT(ValePedagio, '#,##0.00')                AS [Vale Pedágio]
                            ,'R$ ' + FORMAT(Plataforma, '#,##0.00')                 AS [Plataforma]
                            ,'R$ ' + FORMAT(AVI_DUF, '#,##0.00')                    AS [OSA DUF]
                            ,'R$ ' + FORMAT(AVI_DBT, '#,##0.00')                    AS [OSA DBT]
                            ,'R$ ' + FORMAT(Plataforma_DUF, '#,##0.00')             AS [Plataforma DUF]
                            ,'R$ ' + FORMAT(Plataforma_DBT, '#,##0.00')             AS [Plataforma DBT]
                            ,'R$ ' + FORMAT(FaturamentoBruto, '#,##0.00')           AS [Faturamento Bruto]
                            ,'R$ ' + FORMAT(DescontoTotal, '#,##0.00')              AS [Desconto Total]
                            ,'R$ ' + FORMAT(ReceitaLiquida, '#,##0.00')             AS [Receita Liquida]
                        FROM PD.fatur.vw_BaseFaturamento
                        WHERE
                            CAST(DataPassagem AS DATE) BETWEEN '{initial_date_kapsch_revenue_base.strftime('%Y-%m-%d')}' AND '{ending_date_kapsch_revenue_base.strftime('%Y-%m-%d')}'
                        ORDER BY
                            DataPassagem
                            ,Portico
                            ,ClassificacaoVeiculo
                    """

                    # Consulta ao banco
                    df_kapsch_revenue_base = pd.read_sql(query_kapsch_revenue_base, engine_pd)
                    st.session_state["financial_kapsch_revenue_base_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"

                    # Constroi dataframe
                    if not df_kapsch_revenue_base.empty:
                        # Salva o resultado
                        st.session_state["financial_kapsch_revenue_base_df"] = df_kapsch_revenue_base
                        st.session_state["financial_kapsch_revenue_base_exists_df"] = True
                        # Exibe em tela
                        placeholder_kapsch_revenue_base.empty()
                    else:
                        st.session_state["financial_kapsch_revenue_base_exists_df"] = False

                    if "report_financial_kapsch_revenue_base" in st.session_state:
                        del st.session_state["report_financial_kapsch_revenue_base"]
                        st.rerun()

                if "financial_kapsch_revenue_base_exists_df" in st.session_state:
                    if not st.session_state.get("financial_kapsch_revenue_base_exists_df", True):
                        placeholder_kapsch_revenue_base.error("Nenhum registro encontrado.")

                if "financial_kapsch_revenue_base_datetime" in st.session_state:
                    st.write(st.session_state["financial_kapsch_revenue_base_datetime"])

                # Resumo e dados da consulta
                tab_financial_kapsch_revenue_base_resume, tab_financial_kapsch_revenue_base_resume_by_electronic_method, tab_financial_kapsch_revenue_base_table = st.tabs(["Resumo", "Resumo por Meio Eletrônico", "Tabela de Dados"])
                    
                with tab_financial_kapsch_revenue_base_resume:
                    if "financial_kapsch_revenue_base_df" in st.session_state:
                        if not st.session_state.get("financial_kapsch_revenue_base_df").empty:
                            # df_kapsch_revenue_base = st.session_state.get("financial_kapsch_revenue_base_df")
                            df_kapsch_revenue_base_resume = st.session_state.get("financial_kapsch_revenue_base_df").drop(
                                columns=[
                                    "Classificação do Veículo"
                                ]
                            )
                            df_kapsch_revenue_base_resume.rename(columns={
                                "Data da Passagem": "Mês da Passagem"
                                ,"Plataforma": "Receita Plataforma"
                            }, inplace=True)
                            # Formata colunas
                            for col in df_kapsch_revenue_base_resume.columns:
                                if col != "Pórtico" and col !="Mês da Passagem":
                                    df_kapsch_revenue_base_resume[col] = (
                                        df_kapsch_revenue_base_resume[col]
                                        .astype(str)
                                        .str.replace(r"R\$\s*", "", regex=True)
                                        .str.strip()
                                        .str.replace(".", "", regex=False)
                                        .str.replace(",", ".", regex=False)
                                        .apply(pd.to_numeric, errors="coerce")
                                    )
                                elif col == "Pórtico":
                                    df_kapsch_revenue_base_resume[col] = (
                                        df_kapsch_revenue_base_resume[col]
                                        .str.replace(r" (Norte|Sul|Leste|Oeste)", "", regex=True)
                                    )
                                elif col == "Mês da Passagem":
                                    df_kapsch_revenue_base_resume[col] = pd.to_datetime(
                                        df_kapsch_revenue_base_resume[col]
                                        ,errors="coerce"
                                        ,dayfirst=True
                                    ).dt.strftime("%m/%Y")
                            # Agrupa colunas
                            df_kapsch_revenue_base_resume = df_kapsch_revenue_base_resume.groupby(["Mês da Passagem", "Pórtico"], as_index=False).sum()
                            # Remove descontos
                            df_kapsch_revenue_base_resume = df_kapsch_revenue_base_resume.drop(
                                columns=[
                                    "OSA DUF"
                                    ,"OSA DBT"
                                    ,"Plataforma DUF"
                                    ,"Plataforma DBT"
                                ]
                            )
                            # Cria coluna Receita Meio Eletrônico
                            df_kapsch_revenue_base_resume["Receita Meio Eletrônico"] = (
                                df_kapsch_revenue_base_resume[[
                                    "ConectCar"
                                    ,"GreenPass"
                                    ,"Move Mais"
                                    ,"Veloe"
                                    ,"Sem Parar"
                                    ,"Vale Pedágio"
                                ]].sum(axis=1)
                            )
                            df_kapsch_revenue_base_resume = df_kapsch_revenue_base_resume.drop(
                                columns=[
                                    "ConectCar"
                                    ,"GreenPass"
                                    ,"Move Mais"
                                    ,"Veloe"
                                    ,"Sem Parar"
                                    ,"Vale Pedágio"
                                ]
                            )
                            # Obtém Totais
                            total_receita_meio_eletronico = df_kapsch_revenue_base_resume["Receita Meio Eletrônico"].sum().astype(float).sum()
                            total_receita_plataforma = df_kapsch_revenue_base_resume["Receita Plataforma"].sum().astype(float).sum()
                            total_faturamento_bruto = df_kapsch_revenue_base_resume["Faturamento Bruto"].sum().astype(float).sum()
                            total_desconto_total = df_kapsch_revenue_base_resume["Desconto Total"].sum().astype(float).sum()
                            total_receita_liquida = df_kapsch_revenue_base_resume["Receita Liquida"].sum().astype(float).sum()
                            # Formata os números com "R$    "
                            for col in df_kapsch_revenue_base_resume.columns:
                                if col != "Pórtico" and col !="Mês da Passagem":
                                    df_kapsch_revenue_base_resume[col] = (
                                        df_kapsch_revenue_base_resume[col]
                                        .apply(
                                            lambda x: f"R$    {x:,.2f}"
                                            .replace(",", "|")
                                            .replace(".", ",")
                                            .replace("|", ".")
                                        )
                                    )
                            # Reorndena colunas
                            df_kapsch_revenue_base_resume = df_kapsch_revenue_base_resume[[
                                "Mês da Passagem"
                                ,"Pórtico"
                                ,"Receita Meio Eletrônico"
                                ,"Receita Plataforma"
                                ,"Faturamento Bruto"
                                ,"Desconto Total"
                                ,"Receita Liquida"
                            ]]
                            # Mostra tabela
                            # placeholder_financial_kapsch_revenue_base = st.empty()
                            # Altura 38 + (37 * Rows)
                            height_df_kapsch_revenue_base_resume = df_kapsch_revenue_base_resume.shape[0]
                            height_df_kapsch_revenue_base_resume = (50 + (35 * height_df_kapsch_revenue_base_resume))
                            if height_df_kapsch_revenue_base_resume > 600:
                                height_df_kapsch_revenue_base_resume = 600
                            st.dataframe(df_kapsch_revenue_base_resume, height=height_df_kapsch_revenue_base_resume, hide_index=True)
                            # Formata totais
                            total_receita_meio_eletronico = (
                                f"""{total_receita_meio_eletronico:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_receita_plataforma = (
                                f"""{total_receita_plataforma:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_faturamento_bruto = (
                                f"""{total_faturamento_bruto:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_desconto_total = (
                                f"""{total_desconto_total:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_receita_liquida = (
                                f"""{total_receita_liquida:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            st.markdown(f"#### Total Receita Liquida: R$ {total_receita_liquida}")
                            max_len = max([len(total_receita_meio_eletronico), len(total_receita_plataforma), len(total_faturamento_bruto), len(total_desconto_total)])
                            st.text(f"""
                                Total Receita Meio Eletrônico:\t\tR$  {" " * round(2.23 * (max_len - len(total_receita_meio_eletronico)))}{total_receita_meio_eletronico}
                                Total Receita Plataforma:\t\t\tR$  {" " * round(2.23 * (max_len - len(total_receita_plataforma)))}{total_receita_plataforma}
                                Total Faturamento Bruto:\t\t\tR$  {" " * round(2.23 * (max_len - len(total_faturamento_bruto)))}{total_faturamento_bruto}
                                Total Desconto:\t\t\t\t\tR$  {" " * round(2.23 * (max_len - len(total_desconto_total)))}{total_desconto_total}
                            """)

                with tab_financial_kapsch_revenue_base_resume_by_electronic_method:
                    if "financial_kapsch_revenue_base_df" in st.session_state:
                        if not st.session_state.get("financial_kapsch_revenue_base_df").empty:
                            df_kapsch_revenue_base_resume_by_osa = st.session_state.get("financial_kapsch_revenue_base_df").drop(
                                columns=[
                                    "Classificação do Veículo"
                                    ,"Plataforma"
                                    ,"Plataforma DBT"
                                    ,"Plataforma DUF"
                                    ,"Faturamento Bruto"
                                    ,"Desconto Total"
                                    ,"Receita Liquida"
                                ]
                            )
                            df_kapsch_revenue_base_resume_by_osa.rename(columns={
                                "Data da Passagem": "Mês da Passagem"
                            }, inplace=True)
                            # Formata colunas
                            for col in df_kapsch_revenue_base_resume_by_osa.columns:
                                if col != "Pórtico" and col !="Mês da Passagem":
                                    df_kapsch_revenue_base_resume_by_osa[col] = (
                                        df_kapsch_revenue_base_resume_by_osa[col]
                                        .astype(str)
                                        .str.replace(r"R\$\s*", "", regex=True)
                                        .str.strip()
                                        .str.replace(".", "", regex=False)
                                        .str.replace(",", ".", regex=False)
                                        .apply(pd.to_numeric, errors="coerce")
                                    )
                                elif col == "Pórtico":
                                    df_kapsch_revenue_base_resume_by_osa[col] = (
                                        df_kapsch_revenue_base_resume_by_osa[col]
                                        .str.replace(r" (Norte|Sul|Leste|Oeste)", "", regex=True)
                                    )
                                elif col == "Mês da Passagem":
                                    df_kapsch_revenue_base_resume_by_osa[col] = pd.to_datetime(
                                        df_kapsch_revenue_base_resume_by_osa[col]
                                        ,errors="coerce"
                                        ,dayfirst=True
                                    ).dt.strftime("%m/%Y")
                            # Agrupa colunas
                            df_kapsch_revenue_base_resume_by_osa = df_kapsch_revenue_base_resume_by_osa.groupby(["Mês da Passagem", "Pórtico"], as_index=False).sum()
                            # Obtém Totais
                            total_conectcar = df_kapsch_revenue_base_resume_by_osa["ConectCar"].sum().astype(float).sum()
                            total_greenpass = df_kapsch_revenue_base_resume_by_osa["GreenPass"].sum().astype(float).sum()
                            total_move_mais = df_kapsch_revenue_base_resume_by_osa["Move Mais"].sum().astype(float).sum()
                            total_veloe = df_kapsch_revenue_base_resume_by_osa["Veloe"].sum().astype(float).sum()
                            total_sem_parar = df_kapsch_revenue_base_resume_by_osa["Sem Parar"].sum().astype(float).sum()
                            total_vale_pedagio = df_kapsch_revenue_base_resume_by_osa["Vale Pedágio"].sum().astype(float).sum()
                            total_osa_dbt = df_kapsch_revenue_base_resume_by_osa["OSA DBT"].sum().astype(float).sum()
                            total_osa_duf = df_kapsch_revenue_base_resume_by_osa["OSA DUF"].sum().astype(float).sum()
                            # Formata os números com "R$    "
                            for col in df_kapsch_revenue_base_resume_by_osa.columns:
                                if col != "Pórtico" and col !="Mês da Passagem":
                                    df_kapsch_revenue_base_resume_by_osa[col] = (
                                        df_kapsch_revenue_base_resume_by_osa[col]
                                        .apply(
                                            lambda x: f"R$    {x:,.2f}"
                                            .replace(",", "|")
                                            .replace(".", ",")
                                            .replace("|", ".")
                                        )
                                    )
                            # Mostra tabela
                            # Altura 50 + (37 * Rows)
                            height_df_kapsch_revenue_base_resume_by_osa = df_kapsch_revenue_base_resume_by_osa.shape[0]
                            height_df_kapsch_revenue_base_resume_by_osa = (50 + (35 * height_df_kapsch_revenue_base_resume_by_osa))
                            if height_df_kapsch_revenue_base_resume_by_osa > 600:
                                height_df_kapsch_revenue_base_resume_by_osa = 600
                            st.dataframe(df_kapsch_revenue_base_resume_by_osa, height=height_df_kapsch_revenue_base_resume_by_osa, hide_index=True)
                            # Formata totais
                            total_conectcar = (
                                f"""{total_conectcar:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_greenpass = (
                                f"""{total_greenpass:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_move_mais = (
                                f"""{total_move_mais:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_veloe = (
                                f"""{total_veloe:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_sem_parar = (
                                f"""{total_sem_parar:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_vale_pedagio = (
                                f"""{total_vale_pedagio:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_osa_dbt = (
                                f"""{total_osa_dbt:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            total_osa_duf = (
                                f"""{total_osa_duf:,.2f}"""
                                .replace(",", "|")
                                .replace(".", ",")
                                .replace("|", ".")
                            )
                            # st.write(f"Total ConectCar: R$ {total_conectcar}")
                            # st.write(f"Total GreenPass: R$ {total_greenpass}")
                            # st.write(f"Total Move Mais: R$ {total_move_mais}")
                            # st.write(f"Total Veloe: R$ {total_veloe}")
                            # st.write(f"Total Sem Parar: R$ {total_sem_parar}")
                            # st.write(f"Total Vale Pedágio: R$ {total_vale_pedagio}")
                            # st.write(f"Total OSA DBT: R$ {total_osa_dbt}")
                            # st.write(f"Total OSA DUF: R$ {total_osa_duf}")
                            max_len = max([len(total_conectcar), len(total_greenpass), len(total_move_mais), len(total_veloe), len(total_sem_parar), len(total_vale_pedagio), len(total_osa_dbt), len(total_osa_duf)])
                            st.text(f"""
                                Total ConectCar:\t\tR$  {" " * round(2.23 * (max_len - len(total_conectcar)))}{total_conectcar}
                                Total GreenPass:\t\tR$  {" " * round(2.23 * (max_len - len(total_greenpass)))}{total_greenpass}
                                Total Move Mais:\t\tR$  {" " * round(2.23 * (max_len - len(total_move_mais)))}{total_move_mais}
                                Total Veloe:\t\t\tR$  {" " * round(2.23 * (max_len - len(total_veloe)))}{total_veloe}
                                Total Sem Parar:\t\tR$  {" " * round(2.23 * (max_len - len(total_sem_parar)))}{total_sem_parar}
                                Total Vale Pedágio:\t\tR$  {" " * round(2.23 * (max_len - len(total_vale_pedagio)))}{total_vale_pedagio}
                                Total OSA DBT:\t\t\tR$  {" " * round(2.23 * (max_len - len(total_osa_dbt)))}{total_osa_dbt}
                                Total OSA DUF:\t\t\tR$  {" " * round(2.23 * (max_len - len(total_osa_duf)))}{total_osa_duf}
                            """)

                with tab_financial_kapsch_revenue_base_table:
                    if "financial_kapsch_revenue_base_df" in st.session_state:
                        if not st.session_state.get("financial_kapsch_revenue_base_df").empty and st.session_state.get("financial_kapsch_revenue_base_exists_df"):
                            st.dataframe(st.session_state.get("financial_kapsch_revenue_base_df"), height=600, hide_index=True)




# ||========================================================================================================================================||
# ||========================================================================================================================================||
# ||    TI ADMINISTRATIVA                                                                                                                   ||
# ||========================================================================================================================================||
# ||========================================================================================================================================||
if show_administrative_it_tab:
    with tab_administrative_it_tab:
        col_menu, col_content = st.columns([col_menu_width, col_content_width])

        with col_menu:
            st.markdown("##### Senior")
            if st.button("Relatório de Fechamento", use_container_width=True):
                st.session_state["report_ti"] = "ti_senior_revenue_report"
                if "report_ti_senior" in st.session_state:
                    del st.session_state["report_ti_senior"]

        with col_content:
            option_ti = st.session_state.get("report_ti")

            # ||=== kapsch ==================================================================================================================||
            if option_ti == "ti_senior_revenue_report":
                st.write("Senior -- Relatório de Fechamento")
                df_ti_senior_revenue_report_to_csv = pd.DataFrame()

                col1, col2, col3, col4 = st.columns([3, 3, 4, 10])
                with col1:
                    csv_ti_senior_revenue_report = df_ti_senior_revenue_report_to_csv.to_csv(sep=";", index=False)
                    fn.shift_top(18)
                    if st.button("Pesquisar", key="ti_senior_revenue_report_search", use_container_width=True):
                        st.session_state["report_ti_senior"] = "ti_senior_revenue_report_search"
                        if "ti_senior_revenue_report_search_df" in st.session_state:
                            del st.session_state["ti_senior_revenue_report_search_df"]
                    if "ti_senior_revenue_report_search_df" in st.session_state:
                        if not st.session_state.get("ti_senior_revenue_report_search_df").empty:
                            df_ti_senior_revenue_report_to_csv = st.session_state.get("ti_senior_revenue_report_search_df").copy()
                            for col in df_ti_senior_revenue_report_to_csv.columns:
                                if "Data" not in col:
                                    df_ti_senior_revenue_report_to_csv[col] = (
                                        df_ti_senior_revenue_report_to_csv[col]
                                        .astype(str)
                                        .str.replace("R$", "")
                                        .str.replace(".", "")
                                        .str.replace(",", ".")
                                        .str.strip()
                                    )
                            csv_ti_senior_revenue_report = df_ti_senior_revenue_report_to_csv.to_csv(sep=";", index=False, header=False)
                    st.download_button(
                        label="Baixar CSV"
                        ,key="csv_ti_senior_revenue_report"
                        ,data=csv_ti_senior_revenue_report.encode("utf-8-sig")
                        ,file_name="Relatório de Fechamento.csv"
                        ,mime="text/csv"
                        ,use_container_width=True
                    )
                with col2:
                    initial_date_ti_senior_revenue_report = st.date_input("Data Inicial:", value=fn.beginning_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="initial_date_ti_senior_revenue_report")
                    ending_date_ti_senior_revenue_report = st.date_input("Data Final:", value=fn.end_of_month(dt.date.today(), -1), format="DD/MM/YYYY", key="ending_date_ti_senior_revenue_report")

                placeholder_ti_senior_revenue_report = st.empty()

                option_movvia = st.session_state.get("report_ti_senior")
                if option_movvia == "ti_senior_revenue_report_search":
                    placeholder_ti_senior_revenue_report.warning("Pesquisando...")

                    # Escreve query
                    query_ti_senior_revenue_report = f"""
                        SELECT
                            FORMAT(DataPassagem, 'dd/MM/yyyy')                      AS [Data da Passagem]
                            ,'R$ ' + FORMAT(SUM(
                                ConectCar
                                + GreenPass
                                + MoveMais
                                + Veloe
                                + SemParar
                                + ValePedagio
                            ), '#,##0.00')                                          AS [Valor Bruto Eletrônico]
                            ,'R$ ' + FORMAT(SUM(AVI_DBT), '#,##0.00')               AS [DBT Eletrônico]
                            ,'R$ ' + FORMAT(SUM(AVI_DUF), '#,##0.00')               AS [DUF Eletrônico]
                            ,'R$ ' + FORMAT(SUM(Plataforma), '#,##0.00')            AS [Valor Bruto Plataforma]
                            ,'R$ ' + FORMAT(SUM(Plataforma_DBT), '#,##0.00')        AS [DBT Plataforma]
                            ,'R$ ' + FORMAT(SUM(Plataforma_DUF), '#,##0.00')        AS [DUF Plataforma]
                        FROM PD.fatur.vw_BaseFaturamento
                        WHERE
                            CAST(DataPassagem AS DATE) BETWEEN '{initial_date_ti_senior_revenue_report.strftime('%Y-%m-%d')}' AND '{ending_date_ti_senior_revenue_report.strftime('%Y-%m-%d')}'
                        GROUP BY
                            CAST(DataPassagem AS DATE)
                        ORDER BY
                            DataPassagem
                    """

                    # Consulta ao banco
                    df_ti_senior_revenue_report = pd.read_sql(query_ti_senior_revenue_report, engine_pd)

                    st.session_state["ti_senior_revenue_report_search_datetime"] = f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                    # Salva o resultado
                    st.session_state["ti_senior_revenue_report_search_df"] = df_ti_senior_revenue_report
                    placeholder_ti_senior_revenue_report.empty()

                    if "report_ti_senior" in st.session_state:
                        del st.session_state["report_ti_senior"]
                        st.rerun()

                if "report_ti_senior" in st.session_state:
                    del st.session_state["report_ti_senior"]

                if "ti_senior_revenue_report_search_df" in st.session_state:
                    if not st.session_state.get("ti_senior_revenue_report_search_df").empty:
                        # Exibe em tela
                        rows_number = "{:,}".format(st.session_state.get("ti_senior_revenue_report_search_df").shape[0]).replace(",", ".")
                        st.text(f"{st.session_state["ti_senior_revenue_report_search_datetime"]}\t\tRegistros: {rows_number}")
                        st.dataframe(st.session_state.get("ti_senior_revenue_report_search_df"), height=600, hide_index=True, width=860)
                    else:
                        placeholder_ti_senior_revenue_report.error("Nenhum registro encontrado.")
                        if "ti_senior_revenue_report_search_df" in st.session_state:
                            del st.session_state["ti_senior_revenue_report_search_df"]


